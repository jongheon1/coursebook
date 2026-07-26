# Lab — Data Parallelism 손으로 만져보기 (CPU + gloo)

GPU 없이 단일 머신에서 data parallelism 의 핵심 세 가지를 검증한다. `torch.multiprocessing.spawn` 으로 프로세스 `world_size` 개를 띄우고, loopback TCP 위에서 **gloo** backend 로 process group 을 구성한다. 통신 스택(collective, DDP internals)은 GPU/NCCL 과 개념적으로 동일하다 — 다른 것은 링크가 loopback 이라 bandwidth 항이 사실상 공짜라는 점뿐이다.

| 파일 | 검증하는 것 |
|---|---|
| `lab1_ring_allreduce.py` | `isend`/`recv` 만으로 구현한 ring-allreduce == `dist.all_reduce`, 성능 비교 |
| `lab2_ddp_equivalence.py` | manual gradient averaging == DDP == single-process large-batch SGD (동일 파라미터 궤적) |
| `lab3_no_sync_accumulation.py` | gradient accumulation + `no_sync()` 등가성, comm hook 으로 allreduce 횟수 계수 |
| `common.py` | process group setup/teardown 공용 헬퍼 |

## Setup

레포 루트의 공용 venv 를 사용한다 (macOS arm64, CPU 실행):

```bash
cd <repo-root>
python3 -m venv .venv                     # 이미 있으면 생략
.venv/bin/pip install -r 2026-2/distributed-learning-and-inference/weeks/03-data-parallelism/lab/requirements.txt
```

검증된 환경: Python 3.14.3 / torch 2.13.0 / numpy 2.5.1 / macOS (Darwin 24.5.0, arm64). `torch.distributed.is_gloo_available() == True` 이면 준비 완료.

## Lab 1 — ring-allreduce 직접 구현

```bash
cd 2026-2/distributed-learning-and-inference/weeks/03-data-parallelism/lab
../../../../../.venv/bin/python lab1_ring_allreduce.py 4    # world_size=4
```

구현 포인트:

- **reduce-scatter + all-gather 2단계**, 각 p−1 스텝. 스텝마다 rank r 은 오른쪽 이웃 `(r+1)%p` 에게 chunk 하나를 보내고 왼쪽 이웃에게서 하나를 받는다. 인덱스 공식은 본문 §3 과 동일: reduce-scatter 스텝 t 에 chunk `(r−t)%p` 송신, `(r−t−1)%p` 수신·누적.
- **deadlock 회피**: 모든 rank 가 동시에 blocking `send` 를 하면 링 전체가 순환 대기에 빠질 수 있다. `isend` (non-blocking) 를 먼저 걸고 blocking `recv` 를 하는 것으로 해소.
- N 이 p 로 나눠떨어지지 않으면 zero-padding (N=1,000,003 으로 일부러 테스트).

실제 출력 (Apple Silicon, world=4):

```
[correctness] world=4  N=1,000,003  max|ring - all_reduce| = 1.907e-06

  N (floats) |  ring (ms) | dist.all_reduce (ms) |  ratio
------------------------------------------------------------
       4,096 |      0.548 |                0.658 |   0.8x
      65,536 |      0.485 |                0.469 |   1.0x
   1,048,576 |      3.013 |                2.341 |   1.3x
   4,194,304 |     11.166 |                9.598 |   1.2x
```

읽는 법:

- `max|ring - all_reduce| ≈ 2e-6 ≠ 0` — 버그가 아니다. 두 알고리즘의 **덧셈 순서가 달라서** fp32 rounding 이 다르게 쌓인 것 (floating-point 덧셈은 결합법칙이 성립하지 않는다). 크기 ~수 단위 값에서 ulp 몇 개 수준.
- Python 루프로 짠 ring 이 native collective 와 1.0~1.3x 로 비슷한 이유: gloo 의 CPU allreduce 도 내부적으로 ring 계열 알고리즘을 쓰고, loopback 에서는 bandwidth 항이 작아 per-step 오버헤드(Python, 버퍼 할당)가 상대적으로 덜 불리하다. 실제 네트워크에서는 native 구현의 chunk pipelining·버퍼 재사용이 훨씬 유리해진다.

## Lab 2 — manual gradient averaging == DDP == large-batch SGD

```bash
../../../../../.venv/bin/python lab2_ddp_equivalence.py 4
```

같은 초기값(고정 시드 + deepcopy)에서 시작한 3개 모델을 같은 데이터로 30 스텝 학습:

1. `ref` — 한 프로세스가 global batch B=64 전체로 SGD (모든 rank 가 결정론적으로 동일 계산)
2. `manual` — 각 rank 가 local shard b=16 로 backward 후 `all_reduce(p.grad); p.grad /= world`
3. `ddp` — 같은 루프를 `DistributedDataParallel` 로 감쌈

실제 출력:

```
world=4  local batch b=16  global batch B=64  steps=30  SGD(lr=0.1, momentum=0.9)

step | loss(ref) | max|manual-ddp| | max|manual-ref|
-------------------------------------------------------
   1 |    2.3134 |       7.451e-09 |       7.451e-09
   5 |    2.3053 |       1.490e-08 |       1.490e-08
  10 |    2.3170 |       1.490e-08 |       1.490e-08
  20 |    2.2676 |       2.980e-08 |       2.980e-08
  30 |    2.3215 |       2.980e-08 |       2.980e-08

cross-rank spread: manual=0.000e+00  ddp=0.000e+00
final: max|manual-ddp|=2.980e-08  max|manual-ref|=2.980e-08
OK: manual DP == DDP (~bitwise), both == large-batch SGD (fp noise)
```

읽는 법:

- `~3e-8` 은 fp32 의 ulp 수준 — 본문 §1 의 등가성 정리가 수치로 확인된다. 차이의 근원은 "64개 평균" vs "16개 평균 4개의 평균" 의 summation order 차이뿐.
- `cross-rank spread = 0.0` (bitwise) — 모든 rank 의 replica 가 완전히 동일하게 유지된다. 같은 init + 같은 averaged gradient + 같은 deterministic optimizer ⇒ 귀납적으로 영원히 동일.
- 이 등가성은 모델에 BatchNorm 이 없어서 성립한다 (본문 §1 조건 참조). BN 을 넣으면 `manual-ref` 가 즉시 벌어진다.

## Lab 3 — gradient accumulation 과 `no_sync()`

```bash
../../../../../.venv/bin/python lab3_no_sync_accumulation.py 4
```

동일 초기값의 DDP 모델 3개, 매 optimizer step 마다 rank 당 같은 32개 샘플 처리:

- `big` — K·m=32 를 한 번의 forward/backward 로
- `no_sync` — micro-batch 4개, 앞의 3번은 `no_sync()` 안에서 backward (통신 없음, local 누적), 마지막 1번만 동기화
- `naive` — micro-batch 4개, 매번 그냥 backward (매번 allreduce)

`register_comm_hook` 으로 default `allreduce_hook` 을 감싸 bucket 단위 allreduce 호출을 센다.

실제 출력:

```
world=4  K=4 micro-batches x m=8 per rank, 10 optimizer steps

 variant | allreduce bucket calls | max|param - big|
-------------------------------------------------------
     big |                     10 |        0.000e+00
 no_sync |                     10 |        1.490e-08
   naive |                     40 |        1.490e-08

max|no_sync - naive| = 1.490e-08
OK: identical trajectories; no_sync cut communication by 4x (=10 vs 40 bucket allreduces)
```

읽는 법:

- 세 변형 모두 **같은 파라미터 궤적** (fp noise ~1e-8). `naive` 조차 같은 이유: allreduce 는 linear operator 라 "누적 후 평균" == "평균 후 누적". 차이는 오직 통신량 — `naive` 는 스텝당 K=4 번, `no_sync` 는 1번.
- 모델이 작아 bucket 이 1개 (DDP 첫 bucket 기본 1 MiB > 모델 전체 ~27 KB) → `big` 의 호출 수 = 10 steps × 1 bucket. 큰 모델이면 스텝당 bucket 수만큼 곱해진다.
- micro-batch loss 를 `/K` 로 스케일해야 mean-of-means == mean-over-union 이 성립한다 (equal-size micro-batch 전제).
- 주의: 마지막 micro-batch 는 **forward 도 `no_sync()` 밖에서** 해야 한다. DDP 는 forward 시점에 backward 의 동기화 여부(`require_backward_grad_sync`)를 기록하기 때문.

## Gotchas

- macOS 에서 gloo 가 인터페이스를 못 찾으면 `GLOO_SOCKET_IFNAME=lo0` — `common.py` 가 자동 설정.
- `torch.set_num_threads(1)` — 프로세스 4개가 코어를 나눠 쓰므로, 스레드 경합을 없애야 타이밍이 공정하다.
- CPU 모드 DDP 는 `device_ids` 를 넘기지 않는다.
- 모든 스크립트는 `if __name__ == "__main__"` 가드 필수 (spawn start method).
