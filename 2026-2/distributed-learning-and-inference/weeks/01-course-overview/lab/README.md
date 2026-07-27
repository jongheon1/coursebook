# Lab — Baseline 학습 루프 계측 (CPU)

이후 모든 주차의 비교 기준점이 될 **single-device baseline** 을 만들고 계측한다. 작은 MLP/CNN 을 synthetic 데이터로 학습하며 파라미터 수·step time·throughput 을 재고, `torch.profiler` 로 한 스텝을 forward/backward/optimizer 로 분해한다. 본문의 두 주장 — "backward ≈ 2× forward" (§1.2) 와 "$C \approx 6NB$ 는 dense layer 근사" — 를 실측으로 검증·반증하는 것이 목표다.

| 파일 | 역할 |
|---|---|
| `common.py` | 공용 부품: `build_model("mlp"/"cnn")`, `synthetic_batches`, `count_params` — **이후 주차 lab 이 재사용** |
| `train_baseline.py` | 학습 루프 + 계측: step time (mean/p50/p90), samples/s, $6NB$ FLOPs 추정 |
| `profile_breakdown.py` | `torch.profiler` 로 fwd/bwd/opt 시간 분해 + 실측 FLOPs vs $6NB$ 비교 |

Synthetic 데이터 (사전 생성된 random tensor) 를 쓰는 이유: data loading 비용을 ~0 으로 만들어 측정이 순수 compute (fwd/bwd/opt) 만 반영하게 하기 위해서다. 실제 파이프라인에서는 $T_{data}$ 가 스텝 분해의 한 항으로 추가된다 (본문 §6.1).

## Setup

레포 루트의 공용 venv 를 사용한다 (macOS arm64, CPU 실행):

```bash
cd <repo-root>
python3 -m venv .venv                     # 이미 있으면 생략
.venv/bin/pip install -r 2026-2/distributed-learning-and-inference/weeks/01-course-overview/lab/requirements.txt
```

검증된 환경: Python 3.14.3 / torch 2.13.0 / macOS (Darwin 24.5.0, arm64).

## Lab 1 — baseline 학습 루프 계측

```bash
cd 2026-2/distributed-learning-and-inference/weeks/01-course-overview/lab
../../../../../.venv/bin/python train_baseline.py --model mlp --batch-size 256 --steps 50
../../../../../.venv/bin/python train_baseline.py --model cnn --batch-size 256 --steps 50
```

실제 출력 (Apple Silicon, CPU):

```
model=mlp  optimizer=sgd  batch=256  steps=50 (+10 warmup)  threads=5  torch=2.13.0
parameters:       1,863,690
step time:        mean     3.87 ms | p50     3.72 ms | p90     3.98 ms
throughput:       66,101 samples/s
6*N*B estimate:   2.86 GFLOPs/step -> achieved ~739.1 GFLOP/s
final loss:       2.1702
```

```
model=cnn  optimizer=sgd  batch=256  steps=50 (+10 warmup)  threads=5  torch=2.13.0
parameters:       1,625,866
step time:        mean   109.14 ms | p50   106.61 ms | p90   116.95 ms
throughput:       2,346 samples/s
6*N*B estimate:   2.50 GFLOPs/step -> achieved ~22.9 GFLOP/s  (UNDERestimate for CNN: weight sharing)
final loss:       2.2331
```

읽는 법:

- **Warmup 을 버리는 이유**: 첫 스텝들은 memory allocator·kernel dispatch 캐시가 차가워 수 배 느리다. 대규모 학습 벤치마크가 항상 "steady-state throughput" 을 보고하는 것과 같은 이유. p90/p50 격차는 스텝 시간의 꼬리 (OS 스케줄링 등) — 분산 학습에서는 이 꼬리가 straggler 가 되어 전원을 기다리게 한다 (W7, W9 예고).
- **파라미터 수가 비슷한데 (1.86M vs 1.63M) CNN 이 28배 느리다**: FLOPs 는 파라미터 수가 아니라 "파라미터가 몇 번 재사용되는가" 에 달렸다. Conv 는 같은 kernel 을 모든 위치에 재사용 (weight sharing) 하므로 $6NB$ 는 CNN 의 FLOPs 를 크게 과소평가한다 — 정량 확인은 Lab 2.
- MLP 의 achieved ~739 GFLOP/s 는 이 CPU 의 GEMM 실효 성능이다. 본문 §6.2 의 MFU 를 계산하려면 이 값을 peak FLOPS 로 나누면 된다 (CPU peak 는 스펙이 애매해 여기서는 생략 — GPU 에서는 datasheet 값으로 나눈다).

## Lab 2 — torch.profiler 로 스텝 분해

```bash
../../../../../.venv/bin/python profile_breakdown.py --model mlp --batch-size 256
../../../../../.venv/bin/python profile_breakdown.py --model cnn --batch-size 256
```

실제 출력 (MLP, 상위 op 표는 생략):

```
model=mlp  batch=256  params=1,863,690  profiled steps=10

phase split (avg per step, 10 steps):
  forward             1.54 ms  ( 38.1%)
  backward            2.02 ms  ( 50.1%)
  optimizer_step      0.48 ms  ( 11.8%)
  backward/forward ratio: 1.31x  (chapter prediction for dense layers: ~2x)

FLOPs per step:   measured   2.45 GFLOPs  |  6*N*B estimate   2.86 GFLOPs  |  ratio 0.86x
```

실제 출력 (CNN):

```
model=cnn  batch=256  params=1,625,866  profiled steps=10

phase split (avg per step, 10 steps):
  forward            31.93 ms  ( 27.4%)
  backward           84.17 ms  ( 72.2%)
  optimizer_step      0.50 ms  (  0.4%)
  backward/forward ratio: 2.64x  (chapter prediction for dense layers: ~2x)

FLOPs per step:   measured   9.98 GFLOPs  |  6*N*B estimate   2.50 GFLOPs  |  ratio 4.00x
```

읽는 법 — 예측과 실측의 편차가 전부 정보다:

- **MLP 의 FLOPs 0.86×**: $6NB$ 보다 **적게** 나온 이유는 첫 layer 의 input gradient 가 생략되기 때문이다. 입력 $x$ 는 `requires_grad=False` 라 autograd 가 첫 Linear 의 $\partial L/\partial x$ matmul 을 건너뛴다: $2 \times 784 \times 1024 \times 256 = 0.41$ GFLOPs, 정확히 $2.86 - 0.41 = 2.45$. 본문 §1.2 의 "backward = 2 matmuls per layer" 가 첫 layer 에서만 1개가 되는 것.
- **MLP 의 bwd/fwd 1.31×** (< 2×): 위의 생략을 반영한 이론 FLOPs 비는 $1.50/0.95 \approx 1.6\times$ 이고, 남은 격차는 phase 공통의 고정 오버헤드 (op dispatch, ReLU backward 등 non-GEMM) 가 분모·분자에 더해진 것. 모델이 크고 layer 가 깊을수록 2× 에 수렴한다.
- **CNN 의 FLOPs 4.0×**: weight sharing 의 정량 증거 — conv kernel 하나가 $28\times28$ 위치에 재사용되므로 FLOPs 는 파라미터 기반 추정의 4배 (fc layer 가 파라미터의 대부분을 갖지만 FLOPs 는 conv 가 지배). **주의**: profiler 의 `with_flops` 는 `convolution_backward` 에 FLOPs 를 계상하지 않으므로 9.98 G 는 하한이다 — conv backward 까지 손으로 세면 ~25 GFLOPs/step, 즉 실제 비율은 ~10×.
- **CNN 의 bwd/fwd 2.64×** (> 2×): `convolution_backward` 는 input grad 와 weight grad 를 모두 계산하면서, forward 가 쓰는 NNPACK 경로만큼 최적화돼 있지 않다 — "이론 2×" 는 kernel 구현이 대칭적일 때 이야기다. 상위 op 표에서 `aten::convolution_backward` 가 self CPU 의 57% 를 차지하는 것으로 확인 가능.
- 이 분해가 이후 주차의 도구가 된다: W3 의 DDP 는 **backward 시간의 절반 이상** 뒤에 통신을 숨길 수 있는지의 게임이고 (overlap 대상이 바로 이 bwd 구간), W2 의 recomputation 은 fwd 시간을 한 번 더 지불하는 트레이드오프다.

## Gotchas

- 출력 맨 앞의 `USDT: ... profiler_start/stop` 두 줄은 이 머신의 tracing 환경이 찍는 로그다. 무시.
- `record_function` 스코프의 `cpu_time_total` 은 자식 op 포함이므로 세 phase 의 합 ≈ 스텝 전체가 된다. `self_cpu_time` 과 혼동하지 말 것.
- 스텝 시간은 머신 상태에 따라 ±20% 흔들린다. 비교 실험은 같은 세션에서 연달아 돌릴 것.
- `synthetic_batches` 는 batch 8개를 순환한다 — loss 는 내려가지만 일반화와는 무관한 오버핏이다. 여기서 loss 는 "학습이 돌아간다" 는 sanity check 용도뿐.
