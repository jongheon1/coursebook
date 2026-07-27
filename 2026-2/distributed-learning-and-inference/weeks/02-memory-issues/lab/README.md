# Lab — Training Memory 를 바이트 단위로 실측하기 (CPU)

본문의 메모리 회계를 종이 위 수식이 아니라 **실제 텐서의 `numel() × element_size()`** 로 검증한다. GPU 불필요 — model states 와 activation 의 회계는 dtype 과 텐서 shape 만의 함수라서 CPU 에서 그대로 성립한다.

| 파일 | 검증하는 것 |
|---|---|
| `tinytransformer.py` | 손으로 짠 decoder-only transformer. 파라미터 수가 $12Lh^2 + 2Vh + Sh + \text{LN}$ 공식과 정확히 일치 (`assert`) |
| `lab1_memory_accounting.py` | 16 bytes/param 규칙: fp32 Adam (4+4+8) 과 fp16+fp32-master Adam (2+2+12) 이 **둘 다 16** 임을 실측. SGD/momentum/pure-bf16 변형 포함 |
| `lab2_activation_scaling.py` | activation memory ∝ batch size (per-sample 상수), seq 에 대해서는 superlinear — `torch.profiler` + `saved_tensors_hooks` 이중 계측 |
| `lab3_checkpointing.py` | `checkpoint_sequential` 적용 전후: saved activation 바이트 ↓, 시간 ↑, gradient 는 bit-identical |

## Setup

레포 루트의 공용 venv 를 사용한다 (macOS arm64, CPU 실행):

```bash
cd <repo-root>
python3 -m venv .venv                     # 이미 있으면 생략
.venv/bin/pip install -r 2026-2/distributed-learning-and-inference/weeks/02-memory-issues/lab/requirements.txt
```

검증된 환경: Python 3.14.3 / torch 2.13.0 / numpy 2.5.1 / macOS (Darwin 24.5.0, arm64).

## Lab 1 — 16 bytes/param 규칙

```bash
cd 2026-2/distributed-learning-and-inference/weeks/02-memory-issues/lab
../../../../../.venv/bin/python lab1_memory_accounting.py
```

각 구성마다 **실제 한 스텝을 학습**해서 (forward → backward → `opt.step()`) params / grads / optimizer states 를 전부 materialize 한 뒤 바이트를 센다. fp16+master 변형은 Megatron/ZeRO layout 을 손으로 구현: fp16 model + static loss scaling (S=1024) + fp32 master weights 를 Adam 이 들고 update 후 fp16 으로 copy-back.

실제 출력:

```
model: TinyGPT  psi = 862,464 params

               configuration | params | grads  | states | B/param | total
------------------------------------------------------------------------------------
                  fp32 + SGD |   4.00 |   4.00 |   0.00 |   8.00 |     6.58 MiB
    fp32 + SGD(momentum=0.9) |   4.00 |   4.00 |   4.00 |  12.00 |     9.87 MiB
                 fp32 + Adam |   4.00 |   4.00 |   8.00 |  16.00 |    13.16 MiB
     fp16 + fp32-master Adam |   2.00 |   2.00 |  12.00 |  16.00 |    13.16 MiB
   pure bf16 + Adam (unsafe) |   2.00 |   2.00 |   4.00 |   8.00 |     6.58 MiB
```

읽는 법:

- **fp32 Adam 도, fp16 mixed-precision Adam 도 정확히 16 B/param** — 본문 §5 의 핵심. mixed precision 은 model states 를 줄여주지 않는다 (회계가 4+4+8 → 2+2+12 로 재배치될 뿐). 줄어드는 것은 activations (dtype 절반) 과 연산 시간이다.
- fp16+master 의 states 열 12 = fp32 master 4 + momentum 4 + variance 4 — ZeRO 의 $K=12$ 가 그대로 보인다.
- `pure bf16 + Adam` 이 8 B/param 으로 절반인 이유: `torch.optim.Adam` 은 state 를 **param 과 같은 dtype** 으로 만들므로 m/v 까지 bf16 이 된다. 싸지만 위험한 구성 — bf16 의 7-bit mantissa 로 $v_t$ 같은 장기 누적 통계를 유지하면 정밀도 손실이 쌓인다 (본문 §5.4). `eps` 도 기본 `1e-8` 대신 `1e-4` 를 쓰는데, 이유는 underflow 가 아니다: bf16 은 exponent 가 fp32 와 같아 `bf16(1e-8)` ≈ `1.0e-08` 로 멀쩡히 표현된다 (본문 §5.2). 문제는 mantissa — $\sqrt{v} + \epsilon$ 덧셈에서 $\epsilon \lesssim \sqrt{v}\cdot 2^{-8}$ 이면 반올림으로 **흡수**되어 `eps` 가 무력화된다. (fp16 state 였다면 얘기가 다르다: `fp16(1e-8) = 0` — subnormal 하한 $2^{-24} \approx 6\times10^{-8}$ 아래라 진짜 언더플로.)
- Adam 의 per-tensor `step` 스칼라 (37개 × 4 B) 는 반올림에 묻힌다.

## Lab 2 — activation ∝ batch, superlinear in seq

```bash
../../../../../.venv/bin/python lab2_activation_scaling.py 2>/dev/null
```

같은 forward 를 두 방법으로 계측한다:

1. **`torch.profiler(profile_memory=True)`** — forward 동안의 net CPU 할당 바이트 (`sum(e.cpu_memory_usage)`). autograd graph 를 살려둔 채 측정하므로 saved activations + 살아있는 임시 텐서 + logits 가 포함된다.
2. **`torch.autograd.graph.saved_tensors_hooks`** — autograd 가 backward 용으로 실제 stash 하는 텐서를 pack hook 에서 계수. `(data_ptr, numel, element_size)` 로 dedup (같은 텐서를 여러 op 이 저장 — 예: softmax 출력 `att` 는 `att@v` 의 backward 에도 쓰이지만 메모리는 한 번), **파라미터는 제외** (matmul backward 가 $W$ 를 저장하지만 이미 있는 텐서의 참조라 추가 메모리가 아니다).

실제 출력:

```
sweep 1 — batch size b at fixed s=64 (expect: bytes/sample constant)
   b     s | profiler net (MiB) | saved acts (MiB) | saved/sample (KiB)
----------------------------------------------------------------------
   4    64 |              35.26 |             9.54 |             2441.6
   8    64 |              70.45 |            19.06 |             2439.6
  16    64 |             140.84 |            38.10 |             2438.5
  32    64 |             281.61 |            76.19 |             2438.0

sweep 2 — seq length s at fixed b=8 (expect: bytes/token GROWS ~ s term)
   b     s | profiler net (MiB) | saved acts (MiB) |  saved/token (KiB)
----------------------------------------------------------------------
   8    32 |              32.22 |             9.03 |               36.1
   8    64 |              70.45 |            19.06 |               38.1
   8   128 |             164.96 |            42.15 |               42.1
   8   256 |             426.18 |           100.42 |               50.2
```

읽는 법:

- **Sweep 1**: batch 를 2배 하면 두 계측 모두 정확히 2배 — per-sample 2438 KiB 상수. activation memory 가 $b$ 에 선형이라는 본문 §6 의 실측.
- **Sweep 2**: per-token 바이트가 36 → 50 KiB 로 **증가** — `(b, a, s, s)` attention 행렬 (softmax 출력, dedup 후 1회) 이 $s^2$ 항을 만든다. Korthikanti 공식의 $34 + 5as/h$ 구조 (상수항 + $s$ 에 비례하는 항) 가 그대로 보인다.
- 손 계산 대조: 이 모델 (fp32, dropout 없음) 의 block 당 저장 ≈ $16\,sbh$ (LN 입력 2, LN 출력 2, q/k/v 3, attn 출력 1, GELU 입출력 8) × 4 B + $as^2b$ × 4 B. $s{=}64$: $16 \cdot 64 \cdot 128 \cdot 4 = 512$ KiB/sample/block + att 64 KiB → block 4개 + embedding/head ≈ **2.4 MiB/sample** — 실측 2438 KiB 와 일치.
- profiler net 이 saved 의 ~3.7배인 이유: masked_fill 전의 score 행렬 같은 (backward 에 저장되지 않는) 임시 텐서, cross-entropy 내부 버퍼, logits 등이 포함되고, 측정 창 밖에서 할당된 블록의 해제 이벤트는 매칭이 안 되기 때문 (실행 시 profiler 가 그 경고를 stderr 로 찍는다). **스케일링 결론은 두 계측이 동일**하고, 절대값의 ground truth 는 saved 열이다.

## Lab 3 — gradient checkpointing 트레이드오프

```bash
../../../../../.venv/bin/python lab3_checkpointing.py
```

8개 Block 스택을 (a) 그대로, (b) `checkpoint_sequential(model, k, x, use_reentrant=True)` 로 실행. `use_reentrant=True` 는 checkpointed segment 의 forward 를 `no_grad` 로 돌리므로 segment 내부는 아무것도 저장되지 않고, `CheckpointFunction.save_for_backward` 가 stash 하는 **segment 경계 입력**만 pack hook 에 잡힌다 (hook 은 custom Function 의 saved tensor 에도 적용된다).

실제 출력:

```
stack of 8 Blocks (h=256, b=8, s=64), fp32

               variant | saved acts (MiB) |  ratio | fwd+bwd (ms) | slowdown | max|dgrad|
--------------------------------------------------------------------------------------------
         no checkpoint |            68.59 |   1.00 |         44.6 |    1.00x |          —
   checkpoint k=4 segs |            19.02 |   0.28 |         51.4 |    1.15x |    0.0e+00
   checkpoint k=2 segs |            35.05 |   0.51 |         48.6 |    1.09x |    0.0e+00
```

읽는 법:

- **k=4 의 ratio 0.28 을 분해하면**: `checkpoint_sequential` 은 **마지막 segment 를 checkpoint 하지 않으므로** 저장분 = 경계 입력 3개 (각 $bsh \cdot 4$ B = 512 KiB) + 마지막 segment (block 2개) 의 내부 activation 전부 ≈ $2/8 \times 68.6 + 1.5$ MiB ≈ 18.6 MiB — 실측 19.0 MiB 일치. k=2 도 같은 산수로 0.51.
- **slowdown**: k=4 는 block 6개를 backward 중 재계산 (recompute = forward 의 6/8), k=2 는 4개 — k 가 클수록 (마지막 segment 가 작을수록) 메모리는 덜 쓰고 재계산은 많다. 이 CPU 실측 (+15%/+9%) 은 이론 상한 "+1 forward ≈ +33%" (전 layer checkpoint 시) 보다 작은데, 재계산 대상이 전체 forward 의 일부이기 때문.
- **max|dgrad| = 0.0** (bitwise): 재계산은 같은 입력에 같은 커널을 같은 순서로 다시 실행하므로 gradient 가 완전히 동일하다. checkpointing 은 **근사가 아니다** — 수치 결과를 바꾸지 않는 순수한 memory–compute 교환.

## Gotchas

- `torch.profiler` 가 stderr 로 `USDT ... profiler_start` / "Memory block of unknown size..." 를 찍는다 — 계측 노이즈가 아니라 정보성 로그. `2>/dev/null` 로 가려도 된다.
- pack hook 안에서 저장 텐서를 **dedup 하지 않으면** softmax 출력처럼 여러 op 이 공유하는 텐서가 중복 계상된다. 파라미터 제외도 필수 — 안 하면 "activation" 에 weight 가 섞인다.
- `checkpoint_sequential` 의 마지막 segment 는 checkpoint 되지 않는다 (구현 확인: `torch/utils/checkpoint.py`). "k segments = 메모리 1/k" 로 외우면 틀린다.
- lab1 의 pure-bf16 변형은 `eps=1e-4` 를 쓴다. bf16 에서 기본 `eps=1e-8` 은 언더플로하지 **않는다** (fp32 와 같은 exponent range) — 문제는 7-bit mantissa 로 인한 $\sqrt{v}+\epsilon$ 에서의 흡수, 즉 정밀도다. "eps 언더플로" 는 fp16 state 의 문제 (`fp16(1e-8) = 0`, subnormal 하한 $2^{-24}$ 아래) 고, 이 lab 은 fp16 state 를 만들지 않는다.
- `torch.set_num_threads(1)` — 타이밍 측정의 스레드 경합 제거 (lab2/3).
