# Week 5 — Active Recall Quiz

먼저 답을 소리 내어 말한 뒤 펼쳐서 확인한다. 답의 핵심 용어는 영어를 유지한다.

---

**Q1.** 성능 목표를 평균(mean)이 아니라 percentile 로 쓰는 이유는?

<details><summary>답</summary>
응답시간 분포는 right-skewed 라 평균이 소수 outlier 에 끌려가 사용자 경험을 대표하지 못한다. p50 은 절반의 사용자 경험, p99 는 tail latency — SLO 는 "p99 < 200ms" 처럼 percentile 로 쓴다.
</details>

**Q2.** Tail latency amplification: backend 하나가 확률 $p$ 로 느릴 때, $n$ 개 병렬 fan-out 요청이 느릴 확률은? $p=0.01, n=100$ 이면?

<details><summary>답</summary>
$1-(1-p)^n$. $1-0.99^{100} \approx 63\%$ — backend 의 1% 문제가 사용자 다수의 문제가 된다 (Dean & Barroso, "The Tail at Scale").
</details>

**Q3.** Little's law 를 쓰고, 성립 조건과 각 항의 의미를 말하라.

<details><summary>답</summary>
$L = \lambda W$. 정상 상태(stationary)면 분포·스케줄링과 무관하게 성립. $L$ = 시스템 내 평균 요청 수(동시성), $\lambda$ = 도착률(throughput), $W$ = 평균 체류 시간. 스레드 풀·커넥션 풀 크기 산정의 기본 도구.
</details>

**Q4.** Amdahl's law 와 USL 의 차이는? retrograde scaling 은 언제 발생하는가?

<details><summary>답</summary>
Amdahl 은 직렬 비율 $s$ 에 의한 speedup 상한 $1/s$. USL 은 contention $\sigma$ 에 **coherency(crosstalk) 비용 $\kappa N(N-1)$** 을 추가한 모델 — $\kappa>0$ 이면 어느 $N$ 이후 노드를 추가할수록 throughput 이 감소한다 (retrograde scaling). 노드 간 동기화 상태가 스케일링의 적인 이유.
</details>

**Q5.** Horizontal scaling 의 전제조건인 stateless 설계란? 상태는 어디로 가는가?

<details><summary>답</summary>
요청 처리에 필요한 상태를 서버 로컬(메모리 세션 등)에 두지 않는 것 — 그래야 어떤 요청이든 어떤 서버로 보내도 되고 증설·교체가 자유롭다 (12-factor "processes"). 상태는 사라지는 게 아니라 cache/DB/MQ 같은 전문 부품으로 위임된다.
</details>

**Q6.** L4 와 L7 load balancer 의 차이 3가지.

<details><summary>답</summary>
(1) 가시 정보: L4 는 IP/port, L7 은 HTTP 전체(URL, header, cookie). (2) 분배 단위: L4 는 connection, L7 은 request. (3) 비용: L4 는 커널/하드웨어 수준으로 저렴, L7 은 파싱·프록시·TLS 비용. HTTP/2 다중화에서 요청 단위 분산은 L7 만 가능.
</details>

**Q7.** least-connections 가 round-robin 을 크게 이기는 워크로드 조건은? 근거는?

<details><summary>답</summary>
요청 서비스 시간의 분산이 클 때 (heavy-tail 분포). RR 은 상태를 안 보고 elephant request 에 막힌 서버에도 계속 배정하지만 least-conn 은 자동 우회한다. Lab 3 실측: Pareto 서비스 시간에서 p99 대기 139ms vs 988ms (RR). 요청이 균질하면 격차가 줄어 RR 로 충분.
</details>

**Q8.** EWMA load balancing 이 least-connections 보다 나은 감지를 하는 경우는?

<details><summary>답</summary>
connection 수는 같지만 실제 응답이 느려진 서버 (GC pause 중, 과열 노드) — 서버별 최근 latency 의 exponentially-weighted moving average 가 낮은 쪽을 고르므로 latency 악화를 직접 반영한다 (Linkerd 기본 알고리즘).
</details>

**Q9.** Active vs passive health check, 그리고 deep health check 의 양날은?

<details><summary>답</summary>
Passive = 실제 트래픽의 실패 관찰로 제외, active = 별도 probe (`/healthz`) 주기 발사. Deep check (DB 연결까지 검사) 는 shallow check 의 오탐지("probe 만 성공")를 막지만, 공유 의존성 장애 시 전 서버가 동시에 unhealthy 가 되어 장애를 증폭시킬 수 있다.
</details>

**Q10.** 10대→11대 확장 시 mod-N 해싱과 consistent hashing 의 key 재배치 비율은?

<details><summary>답</summary>
mod-N: $1-\frac{1}{11} = 90.9\%$ 이동 (사실상 전체 cache flush). Consistent hashing: $\frac{1}{11} \approx 9.1\%$ (이론 최소) — 새 노드가 successor 의 구간 일부만 가져가고 다른 노드 간 이동은 0.
</details>

**Q11.** Virtual node 의 목적 2가지와 비용은?

<details><summary>답</summary>
(1) load variance 감소 — 노드 부하가 $V$ 개 독립 arc 의 합이 되어 불균형이 $\sim 1/\sqrt{V}$ 로 감소, (2) 노드 제거 시 부하가 여러 노드로 분산 흡수 + 머신 이질성 반영 (Dynamo). 비용: ring 메타데이터가 $N \times V$ 로 증가.
</details>

**Q12.** cache-aside 의 "stale set" race 를 재현 순서로 설명하고 방어책을 말하라.

<details><summary>답</summary>
A miss → DB 에서 $v_1$ 읽음 → B 가 $v_2$ 쓰고 invalidate → A 가 뒤늦게 $v_1$ 을 set → TTL 까지 stale. 방어: **lease** (Facebook memcache — miss 시 토큰 발급, 중간에 delete 가 있으면 그 토큰의 set 거부) 또는 version 기반 CAS.
</details>

**Q13.** write-through / write-back / write-around 의 핵심 구분 축은?

<details><summary>답</summary>
(1) ack 시점의 durability: write-back 만 durable 저장 전에 ack → 캐시 노드 장애 시 데이터 유실. (2) 불일치 창과 latency: write-through 는 동기 이중 기록으로 느리지만 캐시가 항상 warm, write-around 는 캐시를 우회해 pollution 을 막지만 read-after-write miss/stale.
</details>

**Q14.** Cache stampede 의 발생 조건과 방어 3가지.

<details><summary>답</summary>
Hot key 의 TTL 동시 만료(또는 캐시 재시작)로 다수 요청이 동시에 miss → origin 폭주 → 재계산 지연 → 추가 유입의 양성 피드백. 방어: (1) locking/lease + stale-while-revalidate, (2) probabilistic early expiration (XFetch), (3) TTL jitter 로 만료 시각 분산.
</details>

**Q15.** XFetch (probabilistic early expiration) 의 재계산 조건식과 lock 이 필요 없는 이유는?

<details><summary>답</summary>
$\text{now} - \Delta\beta\ln(\text{rand}()) \ge \text{expiry}$ 이면 만료 전 재계산 ($\Delta$ = 재계산 비용, rand ∈ (0,1)). 만료가 가까울수록 확률이 지수적으로 커져 높은 확률로 한 클라이언트만 선제 갱신 — 로컬 정보(만료시각, $\Delta$, 난수)만 쓰므로 조율 불필요 (Vattani et al. 2015).
</details>

**Q16.** Classic LFU 의 aging 문제와 TinyLFU 의 해결책은?

<details><summary>답</summary>
과거 hot key 의 누적 카운트가 캐시를 점거해 새 hot key 가 freq 1 로 들어오자마자 evict — popularity 이동 시 hit rate 붕괴 (Lab 2: 65.6%→26.3%). TinyLFU 는 근사 frequency sketch 를 주기적으로 halving (aging) 하고, "신규 key 추정 빈도 > victim 추정 빈도"일 때만 admit 하는 admission policy (Caffeine 의 W-TinyLFU).
</details>

**Q17.** TTL 은 eviction 정책인가?

<details><summary>답</summary>
아니다 — TTL 은 **staleness 의 시간 상한 계약** ("최대 60초 옛것 허용") 이고, capacity 관리(LRU/LFU) 와 직교하며 병용한다. Invalidation 없이 일관성을 시간으로 bound 하는 가장 단순한 수단.
</details>

**Q18.** CDN 의 pull vs push 는 각각 언제 쓰고, versioned URL (`app.3f9a2c.js`) 이 invalidation 문제를 "소거"하는 이유는?

<details><summary>답</summary>
Pull (origin pull): edge 가 miss 시 origin 에서 가져와 캐싱 — 운영 단순, 첫 요청 cold, 기본값. Push: 배포 시 edge 로 선적재 — cold miss 없음, 저장 비용 상시 지불, 첫 요청 폭주가 예정된 대형 릴리스 (게임 패치) 에 정당화. Versioned URL 은 내용이 바뀌면 URL(=cache key) 자체가 바뀌므로 옛 캐시 엔트리가 더 이상 참조되지 않는다 — stale 이 정의상 불가능해져 purge 가 필요 없고 TTL 을 사실상 무한대로 잡을 수 있다 (immutable caching).
</details>

**Q19.** Token bucket ($r$, $b$) 이 시간 $T$ 동안 admit 하는 요청 상한은? Sliding window counter (Cloudflare 방식) 의 근사식은?

<details><summary>답</summary>
Token bucket: $b + rT$ — 장기 평균은 $r$ 로 제한하면서 순간 burst 를 $b$ 까지 허용 (burst 허용량이 명시적 설계 파라미터), fixed window 의 경계 burst (창 양끝에 2배 유입) 문제가 없다. Sliding window counter: $\text{rate} \approx c_{prev}\times\frac{\text{overlap}}{\text{window}} + c_{curr}$ — 이전 창 카운트를 현재 sliding window 와의 겹침 비율로 가중, 카운터 2개만으로 경계 문제를 제거한 실무 절충.
</details>

**Q20.** BFF 패턴이 해결하는 문제와 대가는?

<details><summary>답</summary>
범용 gateway API 하나로 모든 클라이언트를 서빙할 때의 over/under-fetching — 클라이언트 종류별 전용 backend (mobile-BFF, web-BFF) 를 프론트엔드 팀이 소유해 aggregation 을 맞춤화 (Sam Newman). 대가: 클라이언트 수만큼 서버 코드 중복 가능성.
</details>

**Q21.** B-tree vs LSM-tree: 쓰기 경로의 근본 차이와 각각의 amplification 특성은?

<details><summary>답</summary>
B-tree 는 고정 page 를 in-place 수정 (읽기 예측 가능, key 가 한 곳에), LSM 은 memtable → 정렬된 immutable SSTable 순차 flush + 백그라운드 compaction (쓰기가 순차 I/O 라 write throughput 우수). LSM 은 read amplification (여러 SSTable 조회, Bloom filter 로 완화) 과 compaction 부채 (쓰기 유입을 못 따라가면 읽기 악화) 를 지불.
</details>

**Q22.** Broker queue 모델 (RabbitMQ) 과 log 모델 (Kafka) 의 차이 3가지.

<details><summary>답</summary>
(1) 메시지 수명: ack 시 삭제 vs retention 까지 log 유지 (소비와 무관). (2) 소비 추적: broker 가 건별 ack 관리 vs consumer 가 offset 하나만 유지 — offset 되감기로 replay 가능. (3) 분배: 메시지 단위 경쟁 소비 vs partition 단위 배정 (group 내 한 partition = 한 consumer, 병렬성 상한 = partition 수, partition 내 순서 보장).
</details>

**Q23.** at-least-once 가 실무 기본값인 이유와, "실무의 exactly-once" 는 무엇의 조합인가?

<details><summary>답</summary>
ack 유실 시 재시도 안 하면 유실(at-most-once), 재시도하면 중복 — 유실보다 중복이 다루기 쉽다. 실무의 exactly-once = **at-least-once delivery + idempotent consumer** (idempotency key 로 dedup, `x=5` 형 연산) 또는 처리와 offset 커밋의 원자적 트랜잭션 (Kafka EOS: idempotent producer + transactions + read_committed).
</details>

**Q24.** 생산 속도 > 소비 속도가 지속될 때 시스템의 선택지 3가지는? 큐가 해결책이 아닌 이유는?

<details><summary>답</summary>
(1) backpressure 로 생산자 감속, (2) drop/load shedding, (3) buffering — 버퍼는 유한하므로 결국 (1) 또는 (2) 로 귀결. 정상 상태 $\lambda > \mu$ 면 Little's law 로 대기시간이 무한 성장 — 큐는 일시 스파이크 흡수용이지 용량 부족의 해법이 아니다. Kafka 는 pull 모델이라 소비자가 속도를 통제하고 밀림은 lag 으로 관측된다.
</details>

**Q25.** Poison message 문제와 표준 대응은?

<details><summary>답</summary>
항상 처리 실패하는 메시지가 at-least-once 재시도와 만나 무한 루프 + 뒤 메시지 blocking. 재시도 횟수 상한 후 **dead letter queue (DLQ)** 로 격리해 파이프라인을 계속 진행시키고 격리분은 별도 분석.
</details>

---

## Anki import (TSV)

```tsv
성능 목표를 평균이 아닌 percentile 로 쓰는 이유는?	응답시간 분포가 right-skewed 라 평균은 outlier 에 끌려감. p50 = median 경험, p99 = tail latency. SLO 는 "p99 < 200ms" 형태로 기술.
Tail latency amplification 공식과 p=0.01, n=100 의 값은?	P(slow) = 1-(1-p)^n. 1-0.99^100 ≈ 63% — backend 의 1% 문제가 다수 사용자의 문제가 됨 (Dean & Barroso).
Little's law 공식·조건·활용은?	L = λW. 정상 상태면 분포 무관 성립. L=동시 요청 수, λ=도착률, W=체류시간. 스레드/커넥션 풀 크기 산정 도구.
Amdahl's law 와 USL 의 차이는?	Amdahl: 직렬 비율 s 로 speedup ≤ 1/s. USL: contention σ + coherency κN(N-1) 추가 — κ>0 이면 retrograde scaling (노드 추가가 throughput 감소).
Stateless 설계가 horizontal scaling 의 전제인 이유는?	상태가 서버 로컬에 없어야 임의 서버로 라우팅·증설·교체 가능 (12-factor). 상태는 cache/DB/MQ 전문 부품으로 위임됨.
L4 vs L7 load balancer 차이 3가지는?	가시 정보 IP/port vs HTTP 전체; 분배 단위 connection vs request; 비용 커널 수준 vs 파싱·프록시·TLS. HTTP/2 요청 단위 분산은 L7 만 가능.
least-connections 가 RR 을 크게 이기는 조건은?	요청 서비스 시간이 heavy-tail 일 때 — elephant 에 막힌 서버를 자동 우회. 실측 p99 139ms vs 988ms. 균질 워크로드면 RR 충분.
EWMA LB 가 least-conn 보다 나은 경우는?	connection 수는 같지만 latency 가 악화된 서버 (GC 등) 감지 — 최근 latency 의 지수가중이동평균 최소 서버 선택 (Linkerd 기본).
Deep health check 의 양날은?	shallow check 오탐 방지 vs 공유 의존성 장애 시 전 서버 동시 unhealthy 로 장애 증폭.
10→11 노드 확장 시 mod-N vs consistent hashing 의 remap 비율은?	mod-N: 1-1/11 = 90.9% 이동. consistent hashing: 1/11 ≈ 9.1% (이론 최소, 타 노드 간 이동 0).
Virtual node 의 목적과 비용은?	load variance 를 ~1/√V 로 감소 + 제거 시 부하 분산 흡수 + 이질성 반영 (Dynamo). 비용: ring 메타데이터 N×V.
cache-aside stale set race 와 방어책은?	A miss 로 v1 읽음 → B 가 v2 쓰고 invalidate → A 가 v1 을 늦게 set → TTL 까지 stale. 방어: lease (memcache) 또는 version CAS.
write-back 캐시의 고유 리스크는?	durable 저장 전에 ack — 캐시 노드 장애 시 미flush 쓰기 유실. 대가로 쓰기 throughput 최고.
Cache stampede 의 조건과 방어 3가지는?	hot key TTL 동시 만료로 대량 동시 miss → origin 폭주 피드백. 방어: lock/lease(+stale-while-revalidate), probabilistic early expiration, TTL jitter.
XFetch 재계산 조건식은?	now - Δ·β·ln(rand()) ≥ expiry 면 선제 재계산. 만료 근접할수록 확률 급증, 로컬 난수만 사용 — 조율 불필요 (Vattani 2015).
Classic LFU 의 aging 문제와 TinyLFU 의 해법은?	옛 hot key 의 누적 카운트가 새 hot key 진입을 차단 (shift 시 hit rate 붕괴). TinyLFU: 주기 halving 하는 frequency sketch + admission filter (Caffeine W-TinyLFU).
TTL 의 정확한 역할은?	eviction 이 아니라 staleness 의 시간 상한 계약. capacity 정책 (LRU/LFU) 과 직교, 병용.
CDN pull vs push 선택 기준과, versioned URL 이 invalidation 을 소거하는 이유는?	pull: miss 시 origin fetch, 단순, 기본값. push: 선적재로 cold miss 제거, 저장 비용 상시 — 첫 요청 폭주가 예정된 릴리스에. versioned URL: 내용 변경 = URL(cache key) 변경이라 stale 이 정의상 불가능 — purge 불필요, TTL 무한대 (immutable caching).
Token bucket (r, b) 의 T 초간 admit 상한과 sliding window counter 근사식은?	token bucket: b + rT — 평균 r 제한 + burst b 허용이 명시적 파라미터, fixed window 의 경계 2배 burst 문제 없음. sliding window: rate ≈ c_prev × (overlap/window) + c_curr — 카운터 2개로 경계 문제 제거 (Cloudflare).
BFF 패턴의 문제의식과 대가는?	범용 API 의 over/under-fetching → 클라이언트 종류별 전용 backend 를 프론트 팀이 소유. 대가: 코드 중복.
B-tree vs LSM-tree 핵심 차이는?	in-place page 수정 (읽기 예측성, 트랜잭션) vs memtable→SSTable 순차 flush + compaction (write throughput). LSM 은 read amplification + compaction 부채.
Broker queue vs log 모델 차이 3가지는?	ack 시 삭제 vs retention 유지(replay 가능); 건별 ack vs offset 하나; 메시지 단위 경쟁 소비 vs partition 단위 배정 (병렬성 상한 = partition 수, partition 내 순서 보장).
실무의 exactly-once 는 무엇의 조합인가?	at-least-once delivery + idempotent consumer (idempotency key dedup) 또는 처리·offset 커밋의 원자 트랜잭션 (Kafka: idempotent producer + transactions + read_committed).
과부하 지속 시 시스템의 선택지 3가지는?	backpressure (생산자 감속), drop/load shedding, buffering — 버퍼는 유한하므로 결국 앞 둘로 귀결. λ>μ 지속이면 Little's law 로 대기 무한 성장.
Poison message 의 표준 대응은?	재시도 상한 + dead letter queue (DLQ) 격리 — 무한 재시도 루프와 head-of-line blocking 방지.
```
