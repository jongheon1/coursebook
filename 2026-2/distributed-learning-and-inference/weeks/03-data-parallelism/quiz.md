# Week 03 — Quiz: Data Parallelism

Active recall 은행. 답을 가리고 소리 내어 답한 뒤 확인할 것. `/quiz` 스킬로 구술 세션 가능.

---

**Q1.** Synchronous data parallelism 에서 각 worker 가 계산하는 것과 allreduce 가 합치는 것은 정확히 무엇인가?

**A.** 각 worker 는 자기 local shard (크기 $b$) 에 대한 **mean loss 의 gradient** $g^{(r)}$ 를 계산하고, allreduce 는 이들의 **평균** $\bar g = \frac{1}{p}\sum_r g^{(r)}$ 을 만든다. 이 평균은 global batch $B=pb$ 전체의 gradient 와 정확히 같다.

**Q2.** DP 에서 매 스텝 파라미터를 다시 broadcast 하지 않아도 replica 들이 동기 상태를 유지하는 이유는?

**A.** 귀납법: identical initialization (construction 시 rank 0 broadcast) + identical averaged gradient + identical deterministic optimizer update ⇒ 모든 스텝에서 bitwise 동일. 통신은 gradient 에만 필요하다.

**Q3.** DP 의 large-batch SGD 등가성이 깨지는 대표적 조건 3가지는?

**A.** (1) loss 가 local batch 의 **sum** 으로 정규화된 경우 ($\bar g = b\cdot\frac{1}{B}\sum\nabla\ell$, effective lr 이 local batch size $b = B/p$ 배), (2) **BatchNorm** — batch 통계가 local batch 에만 걸림 (해결: SyncBatchNorm), (3) rank 별 RNG 를 쓰는 non-deterministic op (dropout 등, single-process run 과의 bitwise 일치가 깨짐).

**Q4.** allreduce 를 두 개의 collective 로 분해하면? 각각의 결과 상태는?

**A.** **allreduce = reduce-scatter + all-gather.** reduce-scatter 후에는 각 rank 가 완전히 합쳐진 결과의 $1/p$ chunk 하나씩을 소유하고, all-gather 후에는 전원이 전체 결과를 가진다.

**Q5.** Ring-allreduce 에서 per-node 총 송신량 공식과 유도는?

**A.** 두 phase 각각 $p-1$ 스텝, 스텝당 chunk 크기 $N/p$ 송신 → $V = 2(p-1)\frac{N}{p} = 2\frac{p-1}{p}N \approx 2N$. **$p$ 에 무관**하다는 것이 확장성의 핵심.

**Q6.** Ring-allreduce 의 $\alpha$–$\beta$ cost model 완성형은? 각 항의 이름은?

**A.** $T = 2(p-1)\alpha + 2\frac{p-1}{p}N\beta$ (+ reduction 항 $\frac{p-1}{p}N\gamma$). 첫 항이 **latency term** ($p$ 에 선형), 둘째가 **bandwidth term** ($p$ 에 거의 무관).

**Q7.** "Ring-allreduce 는 bandwidth-optimal 이지만 latency-optimal 이 아니다" — 각각의 근거는?

**A.** Bandwidth-optimal: 어떤 allreduce 알고리즘도 노드당 최소 $2\frac{p-1}{p}N$ 을 주고받아야 하는데 (자기에게 없는 $\frac{p-1}{p}N$ 을 받고 기여분을 보내야 함) ring 이 이 하한을 달성. latency: $2(p-1)$ 스텝이 $p$ 에 선형이라 작은 메시지·큰 $p$ 에서는 $O(\log p)$ hop 의 tree 계열이 우월.

**Q8.** Latency-bound 와 bandwidth-bound 를 가르는 경계 메시지 크기 $N^*$ 는?

**A.** 두 항을 같게 놓으면 $N^* = p\alpha/\beta$ (= $p$ × latency × bandwidth). 이보다 작은 텐서는 latency-bound — DDP 가 gradient 를 bucket 으로 묶는 이유.

**Q9.** Reduce-scatter 스텝 $t$ 에서 rank $r$ 이 보내는 chunk 와 받는 chunk 의 인덱스는? 끝나면 rank $r$ 은 어느 chunk 를 완전 소유하는가?

**A.** 송신: chunk $(r-t) \bmod p$ → rank $(r{+}1)\bmod p$. 수신·누적: chunk $(r-t-1) \bmod p$. 종료 후 rank $r$ 은 chunk $(r+1) \bmod p$ 의 완전합을 소유.

**Q10.** DDP 의 gradient bucketing: 기본 bucket 크기, 배정 순서, 그리고 그 순서인 이유는?

**A.** 기본 `bucket_cap_mb = 25 MiB` (첫 bucket 은 1 MiB). `model.parameters()` 의 **역순**으로 배정 — backward 가 대략 forward 역순으로 gradient 를 완성하므로, 먼저 완성되는 gradient 들이 같은 bucket 에 모여 allreduce 를 일찍 발사할 수 있다.

**Q11.** DDP 에서 bucket 의 allreduce 는 무엇이 트리거하고, 언제 실행되는가?

**A.** 파라미터마다 등록된 **autograd hook** 이 gradient 완성 시 발화하고, 한 bucket 의 모든 gradient 가 준비되는 순간 **asynchronous allreduce** 가 발사된다 — backward 의 남은 계산과 겹쳐서 (computation–communication overlap). backward 끝에서 전체를 wait 후 평균값을 `param.grad` 에 기록.

**Q12.** DDP 의 첫 iteration 후 bucket rebuild 는 무엇을 하는가?

**A.** 파라미터 역순은 실제 ready 순서의 근사일 뿐이므로, 첫 backward 에서 기록한 **실제 gradient ready 순서**대로 bucket 을 한 번 재구성한다 (`Reducer._rebuild_buckets`, 이후 고정). overlap 품질을 높이는 one-time 최적화.

**Q13.** `no_sync()` 의 정확한 동작과, $K$-step gradient accumulation 에서의 통신 절감률은?

**A.** `require_backward_grad_sync` 플래그를 내려 그 안의 backward 가 allreduce 를 건너뛰고 `param.grad` 에 local 누적만 하게 한다. context 밖의 첫 sync backward 가 누적분 전체를 평균. 절감률 $(K-1)/K$. 결과가 같은 근거는 allreduce 의 **선형성**.

**Q14.** DDP 에서 unused parameter 가 있으면 무슨 일이 생기고, 해결책의 비용은?

**A.** 그 파라미터의 hook 이 영영 발화하지 않아 해당 bucket 이 발사되지 못하고 **전 rank 가 hang**. `find_unused_parameters=True` 는 forward output 에서 autograd graph 를 역추적해 미사용 파라미터를 ready 처리 — 매 iteration 그래프 순회 오버헤드가 든다.

**Q15.** Linear scaling rule 의 내용과, 그것을 정당화하는 근사는?

**A.** Batch 를 $k$ 배 하면 lr 도 $k$ 배 ($\eta \to k\eta$). 근거: 작은 batch $k$ 스텝 ≈ 큰 batch 1 스텝이 성립하려면 $\nabla L(w_{t+j}) \approx \nabla L(w_t)$ (gradient 가 $k$ 스텝 동안 거의 불변) 이어야 하고, 이때 큰 스텝의 lr 은 $k\eta$ 여야 두 update 가 일치.

**Q16.** Warmup 이 필요한 이유와 Goyal et al. 의 구체적 처방은?

**A.** 학습 초반에는 gradient 가 급변해 linear scaling 의 근사가 무효 → 큰 lr 로 시작하면 발산. 처방: **gradual warmup** — lr 을 base 값에서 시작해 첫 5 epochs 동안 선형으로 $k\eta$ 까지 증가. (ResNet-50: batch 8192, lr 0.1→3.2, 256 GPUs 로 1시간.)

**Q17.** Critical batch size 란 무엇이고 무엇으로 예측되는가?

**A.** Batch 를 키워도 목표 loss 까지의 스텝 수가 더 이상 줄지 않는 경계 (perfect scaling → diminishing returns → saturation). **gradient noise scale** (gradient 의 noise/signal 비) 로 예측된다 — noise 가 이미 작으면 averaging 을 늘려도 얻는 정보가 없다.

**Q18.** Adam + fp16 mixed precision 에서 model states 가 파라미터당 16 bytes 인 분해와, ZeRO 의 $K$ 는?

**A.** fp16 params 2 + fp16 grads 2 + optimizer states $K{=}12$ (fp32 master params 4 + momentum 4 + variance 4) = **16 bytes/param**.

**Q19.** ZeRO stage 1/2/3 각각의 shard 대상과 per-device 메모리 공식은?

**A.** Stage 1: optimizer states → $4\Psi + \frac{K\Psi}{N_d}$. Stage 2: + gradients → $2\Psi + \frac{(2+K)\Psi}{N_d}$. Stage 3: + parameters → $\frac{(4+K)\Psi}{N_d} = \frac{16\Psi}{N_d}$.

**Q20.** ZeRO 의 stage 별 통신량은? stage 2 까지 통신이 안 늘어나는 이유는?

**A.** Stage 1·2: $2\Psi$ (baseline allreduce 와 동일), stage 3: $3\Psi$ (**1.5×**). stage 2 는 allreduce 를 reduce-scatter (grads, $\Psi$) + all-gather (updated params, $\Psi$) 로 분해한 것과 같아서 총량 불변. stage 3 만 forward/backward 각각의 파라미터 all-gather 가 추가된다.

**Q21.** "ZeRO-3/FSDP 는 model parallelism 이다" 가 오개념인 이유는?

**A.** 연산 관점에서 각 rank 는 여전히 **서로 다른 데이터로 모델 전체를 계산**한다 — data parallelism 이다. shard 되는 것은 **저장** (model states) 이고 계산 직전 all-gather 로 임시 복원된다. 레이어의 행렬곱 자체를 rank 간에 쪼개는 tensor parallelism (W4) 과 축이 다르다.

**Q22.** FSDP 의 FlatParameter 와 unit 은 무엇이고, unit 크기의 트레이드오프는?

**A.** 모델을 unit (wrapping policy, 예: transformer block) 으로 나누고 unit 내 파라미터를 하나의 flat 텐서로 이어붙여 rank 간 등분 shard 한 것. unit 이 크면 collective 가 커져 bandwidth 효율↑ 이지만 materialize 시 메모리 스파이크↑, 작으면 반대 (latency-bound collective 위험).

**Q23.** FSDP 의 forward/backward 에서 일어나는 collective 순서는? (FULL_SHARD 기준)

**A.** Forward: unit 진입 시 **all-gather** (params) → compute → peer shard 해제 (reshard). Backward: **all-gather** (params 재구성) → grad 계산 → **reduce-scatter** (grads, 각 rank 는 자기 shard 의 평균 grad 만 보유) → local shard 만 optimizer update. prefetch 가 다음 unit 의 all-gather 를 현재 계산과 겹친다.

**Q24.** Parameter server 대비 allreduce 의 구조적 장점 두 가지와, PS 가 유리한 지점 하나는?

**A.** Allreduce: (1) per-node 통신량 $2\frac{p-1}{p}N$ 이 $p$ 에 무관 — 중앙 병목 없음, (2) synchronous 라 large-batch SGD 등가성이 유지되어 수렴이 예측 가능. PS 유리: async/bounded-stale consistency, worker 실패 내성, sparse 갱신 (W7 에서 본격).

---

## Anki import (TSV)

```tsv
DP에서 allreduce가 합치는 것은?	각 worker의 local mean-loss gradient의 평균 = global batch 전체의 gradient (equivalence to large-batch SGD)
DP에서 파라미터 re-broadcast가 불필요한 이유는?	identical init + identical averaged gradient + deterministic optimizer ⇒ 귀납적으로 replica가 bitwise 동기 유지
DP의 large-batch 등가성이 깨지는 조건 3가지	sum-normalized loss (lr이 local batch size b = B/p 배), BatchNorm (local batch 통계; SyncBatchNorm으로 해결), per-rank RNG ops (dropout)
allreduce의 2단계 분해는?	reduce-scatter (각 rank가 결과의 1/p chunk 소유) + all-gather (전원이 전체 복원)
ring-allreduce per-node 송신량 공식	2(p-1)/p x N ≈ 2N — p에 무관 (bandwidth-optimal)
ring-allreduce 시간 모델	T = 2(p-1)α + 2((p-1)/p)Nβ; latency term은 p에 선형, bandwidth term은 p에 거의 무관
ring이 bandwidth-optimal인 근거	모든 allreduce는 노드당 최소 2(p-1)/p x N 통신 필요 (남의 몫 수신 + 자기 기여 송신), ring이 하한 달성
latency/bandwidth regime 경계 크기 N*	N* = pα/β; 이보다 작은 텐서는 latency-bound → gradient bucketing의 근거
reduce-scatter step t에서 rank r의 송수신 chunk	send (r-t) mod p, recv+accumulate (r-t-1) mod p; 종료 후 rank r은 chunk (r+1) mod p 완전 소유
DDP 기본 bucket 크기와 배정 순서	25 MiB (첫 bucket 1 MiB), model.parameters()의 역순 — backward의 gradient 완성 순서 근사
DDP bucket allreduce의 트리거	per-param autograd hook 발화 → bucket 내 전 gradient 준비 시 async allreduce 발사 (backward와 overlap)
DDP 첫 iteration 후 bucket rebuild가 하는 일	첫 backward에서 기록한 실제 gradient ready 순서로 bucket을 1회 재구성 (Reducer._rebuild_buckets)
no_sync()의 동작	require_backward_grad_sync를 내려 backward의 allreduce를 건너뛰고 param.grad에 local 누적; 다음 sync backward에서 일괄 평균
K-step accumulation에서 no_sync의 통신 절감률	(K-1)/K; 결과 동일성의 근거는 allreduce의 linearity (sum of avg = avg of sum)
DDP unused parameter의 증상과 해결	bucket이 영영 발사 안 돼 전 rank hang; find_unused_parameters=True로 graph 역추적 (매 iteration 오버헤드)
linear scaling rule	batch를 k배 하면 lr도 k배; ∇L(w_{t+j}) ≈ ∇L(w_t) (k스텝간 gradient 불변) 근사가 근거
warmup이 필요한 이유	학습 초반 gradient 급변으로 linear scaling 근사 무효 → base lr에서 target k·lr까지 첫 5 epochs 선형 ramp (Goyal et al.)
critical batch size를 예측하는 양	gradient noise scale — noise가 signal 대비 작아지면 batch를 키워도 스텝 수가 안 줄어든다
Adam+fp16의 파라미터당 16 bytes 분해	fp16 params 2 + fp16 grads 2 + K=12 (fp32 master 4 + momentum 4 + variance 4)
ZeRO stage별 per-device 메모리	S1: 4Ψ+12Ψ/N_d, S2: 2Ψ+14Ψ/N_d, S3: 16Ψ/N_d
ZeRO stage별 통신량	S1·S2: 2Ψ (baseline과 동일 — allreduce의 RS+AG 분해 재배치), S3: 3Ψ = 1.5x (forward/backward param all-gather 추가)
ZeRO가 여전히 data parallelism인 이유	각 rank가 다른 데이터로 모델 전체를 계산; shard되는 건 저장(model states)뿐, 계산 직전 all-gather로 복원
FSDP FlatParameter란	unit 내 전 파라미터를 하나의 flat tensor로 이어붙여 rank간 등분 shard — unit당 1회의 큰 collective로 latency 회피
FSDP FULL_SHARD의 collective 순서	forward: all-gather→compute→reshard; backward: all-gather→grad→reduce-scatter; prefetch로 다음 unit과 overlap
FSDP sharding strategy와 ZeRO 매핑	FULL_SHARD≈ZeRO-3, SHARD_GRAD_OP≈ZeRO-2, NO_SHARD≈DDP, HYBRID_SHARD=node내 shard+node간 replicate
PS 대비 allreduce의 장점	per-node 통신 p에 무관 (중앙 병목 없음), sync라 large-batch 등가성 유지; PS는 async·내결함·sparse에 유리 (W7)
```
