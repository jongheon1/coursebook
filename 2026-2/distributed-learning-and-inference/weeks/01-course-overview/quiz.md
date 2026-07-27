# Week 01 — Quiz: Course Overview & Introduction

Active recall 은행. 답을 가리고 소리 내어 답한 뒤 확인할 것. `/quiz` 스킬로 구술 세션 가능.

---

**Q1.** Gholami et al. (2024) 의 memory wall 수치: 수요 측 2개와 공급 측 4개의 2년당 성장률은?

**A.** 수요: transformer 파라미터 수 **410×/2yrs**, 학습 compute **750×/2yrs**. 공급: 하드웨어 peak FLOPS **3.0×/2yrs**, DRAM(HBM) bandwidth **1.6×/2yrs**, interconnect bandwidth **1.4×/2yrs**, 단일 GPU 메모리 용량 **2×/2yrs**.

**Q2.** 이 성장률 격차에서 나오는 두 가지 병목 이동은?

**A.** (1) device 안: FLOPS (3.0×) 가 memory bandwidth (1.6×) 보다 빨리 자라 병목이 연산 → **메모리 이동** (memory wall). (2) device 간: interconnect (1.4×) 가 가장 느리게 자라 분산 학습의 병목이 계산 → **통신**.

**Q3.** Dense transformer 의 학습 비용 근사식과 유도는?

**A.** $C \approx 6ND$ FLOPs. Forward: 파라미터당 토큰당 1 MAC = $2N$ FLOPs/token. Backward: activation gradient + weight gradient 두 개의 같은 크기 행렬곱 = $4N$ FLOPs/token. 합 $6N$/token × $D$ tokens.

**Q4.** Backward 가 forward 의 약 2배 비용인 이유는?

**A.** Forward 의 행렬곱 1개당 backward 는 같은 크기의 행렬곱 2개를 수행한다 — chain rule 전파용 input(activation) gradient 와 weight gradient.

**Q5.** 1 PF-day 는 몇 FLOPs 인가?

**A.** $10^{15} \times 86{,}400 = 8.64 \times 10^{19}$ FLOPs.

**Q6.** Kaplan et al. 2020 의 세 power-law exponent 와, compute 배분 결론은?

**A.** $\alpha_N \approx 0.076$, $\alpha_D \approx 0.095$, $\alpha_C \approx 0.050$ (power law — 일부 축은 7자릿수 이상 범위, compute 기준). 배분: $N \propto C^{0.73}$ — budget 이 늘면 거의 전부 모델 크기에 쓰고, 큰 모델을 적은 데이터로 수렴 전에 멈춰라.

**Q7.** Chinchilla 의 parametric loss 형태와 각 항의 의미는?

**A.** $L(N,D) = E + A/N^{\alpha} + B/D^{\beta}$ ($E=1.69$, $A=406.4$, $B=410.7$, $\alpha=0.34$, $\beta=0.28$). $E$ 는 자연어의 irreducible entropy, $A/N^\alpha$ 는 모델 용량 부족 페널티, $B/D^\beta$ 는 데이터 부족 페널티.

**Q8.** Chinchilla 의 compute-optimal 결론과 경험 법칙은?

**A.** $N_{opt} \propto C^{0.5}$, $D_{opt} \propto C^{0.5}$ — **모델과 데이터를 같은 비율로** 키워라. 경험 법칙: $D \approx 20N$ (20 tokens/param). 검증: 같은 예산으로 Chinchilla (70B, 1.4T) > Gopher (280B, 300B).

**Q9.** $D = 20N$ 과 $C = 6ND$ 에서 $N_{opt}$ 를 $C$ 로 나타내면?

**A.** $C = 120N^2 \Rightarrow N_{opt} = \sqrt{C/120}$, $D_{opt} = 20N_{opt}$. (예: $C = 5.76\times10^{23}$ → 70B / 1.4T = Chinchilla.)

**Q10.** Chinchilla-optimal 을 알면서도 Llama 3 8B 를 15T+ tokens (~1,900 tokens/param) 으로 학습한 이유는?

**A.** Chinchilla 는 **학습 비용만** 최소화한다. 모델은 배포 후 수없이 서빙되고 추론 비용은 $N$ 에 비례하므로, 총비용 관점에서는 작은 모델을 optimal 보다 훨씬 오래 학습 (over-training) 하는 것이 이득 — train-once, serve-forever 경제학 (LLaMA 가 명시적으로 채택).

**Q11.** Compute wall 과 capacity wall 의 차이와, 각각의 해법 계열은?

**A.** Compute wall: 한 device 로는 너무 느림 — device 를 늘리고 데이터를 나누면 됨 (data parallelism, W3). Capacity wall: 모델·학습 상태가 한 device 메모리에 **안 들어감** — device 를 늘리는 것만으로 안 풀리고, 모델/상태를 쪼개는 알고리즘 (ZeRO, tensor/pipeline parallelism, W3–4) 이 필요.

**Q12.** GPT-3 (175B) 의 fp16 weights 용량과, 학습 상태 (16 bytes/param) 저장에 필요한 최소 A100-80GB 수는?

**A.** Weights: $175\text{e}9 \times 2$ B = **350 GB** (80 GB 초과 — forward 도 불가). 학습 상태: $175 \times 16$ = 2.8 TB → **35장** (activations 제외).

**Q13.** A100 기준 memory hierarchy 의 용량·대역폭을 SRAM → HBM → PCIe 순으로?

**A.** L1/SMEM (SRAM): 192 KB/SM × 108, aggregate **~19 TB/s**. L2: 40 MB. HBM2e: **80 GB, ~2.0 TB/s**. Host DRAM: PCIe Gen4 ×16 으로 **32 GB/s** (방향당). H100 은 HBM3 3.35 TB/s, L2 50 MB.

**Q14.** NVLink 3/4, IB HDR/NDR 의 대역폭 수치는? NVLink 수치를 읽을 때의 주의점은?

**A.** NVLink 3 (A100): 600 GB/s, NVLink 4 (H100): 900 GB/s — 둘 다 **양방향 합산** (방향당 300/450). IB HDR: 200 Gb/s = 25 GB/s, NDR: 400 Gb/s = 50 GB/s per port. 스펙 수치는 방향·실효 여부를 항상 확인.

**Q15.** SRAM → HBM → NVLink → network 대역폭 서열의 자릿수 감각과, 이 계층이 낳는 배치 원칙은?

**A.** ~19,000 ≫ 2,000–3,350 ≫ 300–450 (방향당) ≫ 25–50 GB/s: 약 **3자릿수** 차이. 원칙: **통신량이 많고 빈번한 병렬화 축일수록 빠른 링크에** — TP 는 NVLink 안, PP 는 node 간, DP 는 최외곽 (W5 의 3D 배치 규칙의 근거).

**Q16.** Arithmetic intensity 와 roofline model 의 정의는? machine balance 는?

**A.** $I = W/Q$ [FLOPs/byte] (수행 FLOPs / 메모리 이동 bytes). Roofline: $P_{attain} = \min(\pi, I \cdot b_{mem})$. Machine balance $I^* = \pi/b_{mem}$ — 그보다 작으면 memory-bound, 크면 compute-bound. A100 ≈ 156, H100 ≈ 295 FLOPs/byte (BF16): 세대가 갈수록 memory-bound 영역이 넓어진다.

**Q17.** LLM decode 가 극단적 memory-bound 인 이유 한 줄은?

**A.** 토큰을 하나씩 생성하며 매번 전체 weights 를 HBM 에서 다시 읽지만 byte 당 연산은 거의 없다 ($I \approx 1$–$2$ ≪ $I^* \approx 300$) — 그래서 W13 의 serving 최적화는 FLOPs 가 아니라 **byte 이동** 을 줄인다.

**Q18.** Amdahl's law 의 식·상한과, $f = 0.95$, $p = 64$ 일 때의 speedup 은?

**A.** $S(p) = 1/((1-f) + f/p) \le 1/(1-f)$. $f=0.95$: $S(64) = 1/(0.05+0.95/64) \approx 15.4$, 상한 $S(\infty) = 20$ — serial 5% 만으로 상한 20×.

**Q19.** Gustafson's law 의 식과, Amdahl 과 결론이 다른 이유는?

**A.** $S_{scaled}(p) = (1-f) + fp$ ($p$ 에 선형). Amdahl 은 **문제 크기 고정** (strong scaling) — serial 이 점점 큰 비중이 됨. Gustafson 은 **문제를 $p$ 와 함께 키움** (weak scaling) — serial 이 상수 비중. 같은 $f$ 라도 가정이 다르다.

**Q20.** Strong vs weak scaling 의 정의와, weak scaling 의 진짜 한계는?

**A.** Strong: global batch $B$ 고정, $p$↑ → per-device $b = B/p$↓. Weak: $b$ 고정, $B = pb$↑. Weak 의 한계는 시스템이 아니라 **통계**: batch 를 키우는 것이 공짜가 아니다 (critical batch size, W3 §5).

**Q21.** DP 의 comm-to-comp ratio 유도 결과와 핵심 관찰 두 가지는?

**A.** $R = \frac{2gN\beta}{6Nb_{tok}/F} = \frac{gF\beta}{3b_{tok}}$ ($g$ = grad bytes/param; fp32 면 $\frac{4}{3}F\beta/b_{tok}$). 관찰: (1) **모델 크기 $N$ 소거** — 통신·계산 둘 다 $N$ 에 비례. (2) 하드웨어 균형 $F\beta$ 는 세대마다 악화되고, strong scaling 은 $b_{tok}$ 을 줄여 $R$ 을 키운다.

**Q22.** MFU 의 정의식과, `nvidia-smi` utilization 과의 차이는?

**A.** $\text{MFU} = \frac{X_{tokens/s} \times 6N}{p \times \pi_{peak}}$ — 모델에 **필수인** FLOPs 처리율 / peak FLOPS. `nvidia-smi` utilization 은 "커널이 돌고 있던 시간 비율" 로, memory-bound 대기도 100% 로 찍힌다 — utilization 100% 에 MFU 15% 가 흔하다.

**Q23.** HFU 와 MFU 의 관계, recomputation 을 켜면 각각 어떻게 되나?

**A.** HFU 는 하드웨어가 실제 실행한 FLOPs (recomputation 포함) 기준, MFU 는 모델 필수 FLOPs 만 — 항상 **HFU ≥ MFU**. Full recomputation (토큰당 $8N$ 실행) 을 켜면 HFU ↑, MFU ↓ 동시 가능. 비교·보고에는 MFU.

**Q24.** 대규모 학습의 MFU 기준선 실측치 두 개는?

**A.** PaLM 540B: **46.2%**. Llama 3 405B: **38–43%** (16,384 H100, BF16 380–430 TFLOP/s/GPU). "잘 튜닝된 대규모 학습 ≈ 40%±".

**Q25.** 이 과목의 병렬화 축 4개가 각각 쪼개는 것과 발생시키는 통신은?

**A.** **Data** (W3): batch 를 쪼갬 — step 당 gradient allreduce. **Pipeline** (W4): layer 묶음으로 쪼갬 — stage 경계 activation 전달. **Tensor** (W4): layer 내부 행렬을 쪼갬 — layer 마다 allreduce (고빈도). **Sequence** (W4): sequence 축을 쪼갬 — activation 재분배. 조합·배치가 W5 hybrid.

---

## Anki TSV

```tsv
Memory wall: 2년당 성장률 — 모델 크기 / 학습 compute / peak FLOPS / DRAM BW / interconnect BW / GPU 메모리 용량	410× / 750× / 3.0× / 1.6× / 1.4× / 2× per 2yrs (Gholami et al. 2024)
Dense transformer 학습 비용 근사식과 유도	C ≈ 6ND FLOPs — forward 2N/token (param 당 1 MAC), backward 4N/token (activation grad + weight grad 행렬곱 2개)
Backward 가 forward 의 2배인 이유	forward 행렬곱 1개당 backward 는 같은 크기 행렬곱 2개 (input grad + weight grad)
1 PF-day = ? FLOPs	8.64e19 (= 1e15 × 86,400)
Kaplan 2020 의 exponents α_N, α_D, α_C	0.076 / 0.095 / 0.050 (power law; 일부 축은 7+ 자릿수 범위 — compute 기준)
Kaplan 의 compute 배분 결론	N ∝ C^0.73 — budget 증가분 대부분을 모델 크기에; 큰 모델 + 적은 데이터 + 조기 종료
Chinchilla parametric loss	L(N,D) = E + A/N^α + B/D^β; E=1.69, A=406.4, B=410.7, α=0.34, β=0.28
Chinchilla 의 compute-optimal 결론	N 과 D 를 같은 비율로 (N_opt ∝ C^0.5); 경험 법칙 D ≈ 20N tokens/param
D=20N 일 때 N_opt(C) 공식	N_opt = sqrt(C/120) (C = 6ND = 120N²)
Chinchilla vs Gopher 실물 검증	같은 예산: Chinchilla 70B/1.4T > Gopher 280B/300B (MMLU 67.5%, +7%p)
Llama 3 8B 가 ~1,900 tokens/param 으로 over-training 한 이유	추론 비용 ∝ N — train-once serve-forever 총비용 관점에선 작은 모델을 오래 학습하는 게 이득 (LLaMA 관점)
Compute wall vs capacity wall	느려서 (GPU 추가+데이터 분할로 해결) vs 안 들어가서 (모델/상태를 쪼개는 알고리즘 필요 — ZeRO, TP/PP)
GPT-3 175B: fp16 weights 용량 / 학습상태 2.8TB 저장에 필요한 80GB GPU 수	350 GB (단일 80GB 초과) / 35장 (16 bytes/param, activations 제외)
A100 메모리 계층: SRAM aggregate BW / HBM 용량·BW / PCIe Gen4 BW	~19 TB/s / 80 GB, ~2.0 TB/s / 32 GB/s per direction (H100: HBM3 3.35 TB/s)
NVLink 3 / NVLink 4 / IB HDR / IB NDR 대역폭	600 / 900 GB/s (양방향 합산; 방향당 300/450) — 25 / 50 GB/s per port
대역폭 서열 (자릿수)	SRAM ~19,000 ≫ HBM 2,000–3,350 ≫ NVLink 300–450 ≫ network 25–50 GB/s — 약 3자릿수 격차
계층 → 병렬화 배치 원칙	통신 많고 빈번한 축일수록 빠른 링크에: TP 는 node 내 NVLink, PP 는 node 간, DP 는 최외곽 (W5)
Arithmetic intensity / roofline / machine balance	I = FLOPs/byte; P = min(peak, I × BW_mem); I* = peak/BW_mem (A100 ≈ 156, H100 ≈ 295) — I < I* 면 memory-bound
LLM decode 가 memory-bound 인 이유	토큰마다 전체 weights 를 다시 읽고 byte 당 연산 거의 없음 (I ≈ 1–2 ≪ I* ≈ 300) → serving 최적화는 byte 이동 감소가 본질
Amdahl's law 식과 상한	S(p) = 1/((1−f) + f/p) ≤ 1/(1−f); f=0.95 → S(64)≈15.4, 상한 20
Gustafson's law 식과 가정	S = (1−f) + f·p; 문제 크기를 p 와 함께 키우는 weak scaling 가정 (Amdahl 은 고정 문제 = strong)
Strong vs weak scaling	strong: B 고정, per-device b=B/p 감소. weak: b 고정, B=pb 증가 — 한계는 통계 (critical batch size)
DP comm-to-comp ratio 공식과 두 관찰	R = gFβ/(3·b_tok) — (1) 모델 크기 N 소거, (2) F·β 는 세대마다 악화, strong scaling 은 b_tok 을 줄여 R 증가
MFU 정의식	(tokens/s × 6N) / (p × peak FLOPS) — 모델 필수 FLOPs 처리율 / peak. nvidia-smi utilization 과 무관
HFU vs MFU	HFU 는 실행된 전체 FLOPs (recomputation 포함), MFU 는 모델 필수만; HFU ≥ MFU, recompute 켜면 HFU↑ MFU↓ 가능
대규모 MFU 실측 기준선	PaLM 46.2%, Llama 3 405B 38–43% (16,384 H100) — 40%± 가 잘 튜닝된 수준
Scaling efficiency (strong / weak)	E_strong = T(1)/(p·T(p)), E_weak = X(p)/(p·X(1)) — 논문의 linear scaling 그래프는 대부분 weak
병렬화 축 4개: 쪼개는 것 → 통신	data: batch → grad allreduce / pipeline: layer 블록 → 경계 activation / tensor: layer 내 행렬 → layer 당 allreduce / sequence: seq 축 → activation 재분배
```
