# Lab — System Design Building Blocks 시뮬레이션 3종

세 실습 모두 **Python 표준 라이브러리만** 사용한다. 가상환경·의존성 설치 불필요:

```bash
python3 consistent_hashing.py
python3 cache_eviction.py
python3 load_balancing.py
```

각 스크립트는 고정 seed 를 쓰므로 아래 출력이 그대로 재현된다 (Python 3.11+ 기준, `random` 모듈 시드 고정).

---

## Lab 1 — `consistent_hashing.py`

**목표**: (1) 노드 추가/제거 시 mod-N 해싱과 consistent hashing 의 key remap 비율을 실측으로 비교하고, (2) vnode 수가 load 균일도에 미치는 효과를 측정한다.

**구현 포인트**
- Python 내장 `hash()` 는 프로세스마다 salt 가 달라 분산 해시 링에 못 쓴다 — MD5 를 64-bit 로 잘라 안정 해시로 사용.
- 링은 `(hash_point, node)` 정렬 리스트 + `bisect_right` 로 clockwise successor 를 O(log VN) 에 찾는다.
- 이론값: N→N+1 노드에서 mod-N 은 키의 $1 - \frac{1}{N+1}$ 이 이동, consistent hashing 은 $\frac{K}{N+1}$ (약 $\frac{1}{N+1}$ 비율)만 이동.

**실제 실행 출력**

```
=== Experiment 1: remap fraction on membership change ===
100,000 keys, 10 nodes -> add 1 node / remove 1 node

mod-N        add node :  90.9% of keys remapped   (theory ~ 1 - 1/11 = 90.9%)
mod-N        rm  node :  90.1% of keys remapped
consistent   add node :   9.3% of keys remapped   (theory ~ K/(N+1) = 1/11 = 9.1%)
consistent   rm  node :   9.2% of keys remapped   (theory ~ K/N = 1/10 = 10.0%)

=== Experiment 2: load uniformity vs vnode count (10 nodes) ===
 vnodes | min/mean | max/mean | CV (std/mean)
------------------------------------------------
      1 |     0.08 |     3.61 |         1.216
     10 |     0.52 |     1.80 |         0.340
    100 |     0.86 |     1.13 |         0.085
   1000 |     0.97 |     1.04 |         0.019
```

**읽는 법**
- mod-N 은 노드 1대 변화에 키의 ~91% 가 이동 — 캐시 클러스터라면 사실상 전체 cache flush. Consistent hashing 은 ~9% (이론 최소치)만 이동. **10배 차이**.
- vnode=1 이면 최대 부하 노드가 평균의 3.6배 — 링 위 arc 길이 분산이 크기 때문. vnode 를 늘리면 각 노드 부하가 여러 arc 의 합이 되어 CV 가 대략 $1/\sqrt{V}$ 로 줄어든다 (1.216 → 0.340 → 0.085 → 0.019, 각 단계 ~$\sqrt{10}$ 배 감소와 일치).
- 트레이드오프: vnode 수 × 노드 수만큼 링 메타데이터와 rebuild 비용 증가.

---

## Lab 2 — `cache_eviction.py`

**목표**: FIFO / LRU / LFU 의 hit rate 를 Zipf 분포 워크로드에서 비교하고, popularity 가 바뀔 때 LFU 의 aging 문제를 관찰한다.

**구현 포인트**
- Zipf(s=1.0): rank $r$ 의 확률 $\propto 1/r^s$. `random.choices(cum_weights=...)` 로 샘플링 (내부적으로 bisect).
- LFU 는 lazy-deletion heap: freq 증가 때마다 `(freq, seq, key)` 를 push, evict 시 stale entry 를 skip. 카운트는 캐시 안에 있는 동안만 유지 (classic in-cache LFU).
- `static-opt` 는 상위 C 개 아이템을 고정으로 pin 했을 때의 hit rate — eviction 정책의 상한 참조값.

**실제 실행 출력**

```
=== Experiment 1: hit rate on stationary Zipf(s=1.0) workload ===
10,000 items, 200,000 requests

capacity |    FIFO |     LRU |     LFU | static-opt
----------------------------------------------------
     100 |   34.2% |   38.9% |   49.6% |      53.0%
     500 |   53.6% |   58.4% |   66.1% |      69.4%
    1000 |   62.8% |   67.2% |   72.9% |      76.5%

=== Experiment 2: popularity shift at t = 50% (capacity 500) ===
 policy | phase-1 hit | phase-2 first 20k | phase-2 all
----------------------------------------------------------
   FIFO |       53.7% |             53.9% |       53.9%
    LRU |       58.3% |             58.5% |       58.6%
    LFU |       65.6% |             25.2% |       26.3%
```

**읽는 법**
- 정상 상태(stationary)에서는 **LFU > LRU > FIFO**. Zipf 처럼 popularity 가 안정적으로 skew 된 워크로드에서는 frequency 가 recency 보다 좋은 미래 예측자다. LFU 는 static-opt 에 3~4%p 까지 근접.
- Experiment 2 에서 인기 순위를 통째로 회전시키면 (어제의 hot key 가 오늘 cold): LRU/FIFO 는 수천 요청 안에 적응해 hit rate 유지, **LFU 는 26% 로 붕괴하고 100,000 요청이 지나도 회복하지 못한다**. 캐시에 남은 old-hot 키들의 누적 카운트가 수백인데, new-hot 키는 freq 1 로 들어와 카운트를 쌓기 전에 즉시 evict 되기 때문 — frequency pollution. 이것이 TinyLFU 가 주기적 카운트 halving (aging) 과 admission filter 로 해결하는 문제다 (README 본문 §Cache 참조).

---

## Lab 3 — `load_balancing.py`

**목표**: heavy-tail 서비스 시간 분포에서 RR / random / least-connections 의 대기시간 p99 를 비교한다.

**구현 포인트**
- Discrete-event 시뮬레이션: 10대의 single-worker FIFO 서버, Poisson arrival ($\lambda = 160$ req/s), $\rho = 0.8$.
- 서비스 시간: Pareto($\alpha=2.5$, mean 50ms) — heavy tail (분산은 유한하지만 tail 이 두꺼움). 비교 기준으로 같은 평균의 exponential 도 측정.
- **Paired comparison**: arrival 시각과 서비스 시간을 미리 생성해 세 정책에 동일 워크로드를 재생 — 정책 차이만 분리.
- least-connections 는 dispatch 시점에 각 서버의 미완료 요청 수(departure time deque)를 세어 최소 서버 선택.

**실제 실행 출력**

```
=== Waiting time by dispatch policy (paired workloads) ===

--- service time: Pareto(alpha=2.5) — heavy tail, 10 servers, rho = 0.8, 200,000 requests ---
     policy |     mean |      p50 |      p95 |      p99 |      max
------------------------------------------------------------------
     random |  192.7ms |   76.4ms |  613.5ms | 1513.8ms | 13418.6ms
         rr |   96.3ms |    1.3ms |  335.3ms |  987.6ms | 13473.6ms
 least-conn |   13.3ms |    0.0ms |   63.4ms |  138.9ms | 12583.2ms

--- service time: Exponential — light tail (baseline), 10 servers, rho = 0.8, 200,000 requests ---
     policy |     mean |      p50 |      p95 |      p99 |      max
------------------------------------------------------------------
     random |  196.3ms |  116.2ms |  672.8ms | 1067.2ms | 2704.4ms
         rr |   97.9ms |   40.9ms |  385.2ms |  617.2ms | 1411.1ms
 least-conn |   18.6ms |    0.0ms |  108.4ms |  202.0ms |  773.5ms
```

**읽는 법**
- Heavy tail 에서 p99 대기시간: **least-conn 139ms vs RR 988ms vs random 1514ms** — least-conn 이 RR 대비 7배, random 대비 11배 낮다. RR/random 은 상태를 안 보므로 elephant request 에 막힌 서버에도 계속 요청을 밀어 넣고, 그 뒤에 줄 선 요청들이 tail 을 만든다. least-conn 은 막힌 서버를 즉시 우회한다.
- exponential 에서는 격차가 상대적으로 줄어든다 (p99 기준 RR/LC 비율 7.1 → 3.1). **정교한 LB 알고리즘의 가치는 서비스 시간 분산이 클수록 커진다.**
- least-conn 도 max 는 ~12.5초 — dispatch 가 non-preemptive 라서 이미 elephant 뒤에 배정된 요청은 구제 못 한다. 이것이 README 본문의 tail latency 논의(hedged request 등)로 이어진다.
