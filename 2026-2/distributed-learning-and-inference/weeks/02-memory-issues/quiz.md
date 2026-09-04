# Week 02 — Quiz: ML Recap & Memory Issues

Active recall 은행. 답을 가리고 소리 내어 답한 뒤 확인할 것. `/quiz` 스킬로 구술 세션 가능.

---

**Q1.** Supervised learning 의 empirical risk minimization 목적식과 mini-batch SGD update rule 은?

**A.** $\min_w L(w) = \frac{1}{|D|}\sum_{(x,y)\in D}\ell(f_w(x),y)$. Update: $w_{t+1} = w_t - \eta\,\hat g_t$, $\hat g_t = \frac{1}{B}\sum_{(x,y)\in\mathcal{B}_t}\nabla\ell(f_{w_t}(x),y)$ — 크기 $B$ 의 random mini-batch 로 full gradient 를 추정.

**Q2.** Mini-batch gradient 추정량의 두 가지 핵심 통계적 성질은?

**A.** (1) **Unbiased**: uniform 샘플링 + mean loss 이면 $\mathbb{E}[\hat g] = \nabla L$. (2) **Variance $\propto 1/B$**: i.i.d. 샘플에서 batch 를 키우면 gradient noise 감소 — W3 linear scaling rule 의 통계적 근거.

**Q3.** Learning rate 가 너무 크면 발산하는 이유를 quadratic 예시로 보이면?

**A.** $L = \frac{\lambda}{2}w^2$ 에서 GD 는 $w_{t+1} = (1-\eta\lambda)w_t$. $|1-\eta\lambda| < 1 \Leftrightarrow \eta < 2/\lambda$ — 가장 가파른 방향의 곡률이 $\eta$ 의 상한을 정한다.

**Q4.** 딥러닝이 forward-mode 가 아니라 reverse-mode AD (backprop) 를 쓰는 이유는?

**A.** Loss 가 **스칼라 하나**이고 파라미터가 $\Psi$ 개이므로, 출력→입력 방향 한 번의 sweep 으로 모든 $\partial L/\partial w_i$ 를 얻는다. forward mode 는 입력 방향마다 한 번씩, $\Psi$ 회 필요.

**Q5.** Linear layer $Y = XW$ 의 backward 두 식과, 그것이 요구하는 저장물은?

**A.** $\delta_X = \delta_Y W^\top$ (필요: $W$ — 이미 상주), $\delta_W = X^\top \delta_Y$ (필요: **입력 $X$** — saved activation). matmul 의 입력 activation 저장이 activation memory 의 주범.

**Q6.** "Backward ≈ 2× forward FLOPs" 의 근거와, 토큰당 학습 비용 $6\Psi$ 의 유도는?

**A.** Forward matmul 하나가 backward 에서 같은 크기의 matmul **둘** ($\delta_X$, $\delta_W$) 을 낳는다. Forward ≈ $2\Psi$ FLOPs/token (param 당 multiply-add 1회) + backward $4\Psi$ → 합 $6\Psi$ (Kaplan et al.).

**Q7.** Backprop 에서 "저장되는 것" 과 "계산되는 것" 을 한 문장씩으로 구분하면?

**A.** 저장: forward 중간값 중 **VJP 가 필요로 하는 텐서** (matmul 입력, softmax 출력, ReLU mask 등) = activations. 계산: upstream gradient 에 op 별 local Jacobian 을 곱한 **vector–Jacobian product** = gradients. Loss 값만으로는 어떤 gradient 도 못 만든다.

**Q8.** SGD / SGD+momentum / Adam 의 파라미터당 persistent state 수는?

**A.** 0 / 1 (velocity $u_t = \mu u_{t-1} + \hat g_t$) / **2** ($m_t$, $v_t$ — PyTorch 의 `exp_avg`, `exp_avg_sq`).

**Q9.** Adam 의 update 식 (bias correction 포함) 은? bias correction 이 필요한 이유는?

**A.** $m_t = \beta_1 m_{t-1} + (1{-}\beta_1)\hat g_t$, $v_t = \beta_2 v_{t-1} + (1{-}\beta_2)\hat g_t^2$, $\hat m = m_t/(1{-}\beta_1^t)$, $\hat v = v_t/(1{-}\beta_2^t)$, $w_{t+1} = w_t - \eta\,\hat m/(\sqrt{\hat v}+\epsilon)$. $m, v$ 가 0 으로 초기화되어 초기 스텝에 0 쪽으로 편향 — $(1-\beta^t)$ 로 나눠 보정.

**Q10.** Optimizer states 를 fp32 로 유지하는 이유 두 가지는?

**A.** (1) $v_t$ 는 $(1-\beta_2)=10^{-3}$ 단위 증분의 장기 누적 — 저정밀도에서 갱신 소실. (2) $\epsilon = 10^{-8}$ 등 작은 상수가 fp16 subnormal 하한 ($\approx 6\times 10^{-8}$) 근처라 연산 자체가 붕괴.

**Q11.** ZeRO 의 학습 메모리 2대 분류와 각각의 스케일링 변수는?

**A.** **Model states** (weights + gradients + optimizer states) — 파라미터 수 $\Psi$ 만의 함수. **Residual states** (activations, 임시 버퍼, fragmentation) — $b, s$ 에 의존.

**Q12.** fp16 mixed-precision Adam 의 파라미터당 16 bytes 를 항목별로 유도하면?

**A.** fp16 weights $2$ + fp16 grads $2$ + optimizer states $K{=}12$ (fp32 master $4$ + $m$ $4$ + $v$ $4$) $= (4+K)\Psi = 16\Psi$ bytes. master weights 를 optimizer state 로 계상하는 것이 ZeRO 관례.

**Q13.** fp32 Adam 학습의 파라미터당 바이트는? 그 결과 mixed precision 이 실제로 아끼는 것은?

**A.** $4+4+4+4 = 16$ B/param — **mixed precision 과 동일**. 즉 model states 는 안 줄어든다. 실제 절감: activations 절반 (fp16 저장), memory bandwidth 절반, 저정밀 연산 유닛의 throughput.

**Q14.** fp16 과 bf16 의 비트 배치와 트레이드오프는?

**A.** fp16 = 1/5/10 (max 65504, min normal $2^{-14}$), bf16 = 1/8/7 (fp32 와 동일 range). bf16 은 **range 를 얻고 정밀도를 잃는다** — loss scaling 불필요, 하지만 mantissa 7 bits 라 fp32 master weights 는 여전히 필요.

**Q15.** Loss scaling 의 정확한 메커니즘은? 무엇을 막는 것인가?

**A.** **Underflow** 방지: 작은 gradient 들이 fp16 하한 $2^{-24}$ 아래에서 0 이 되는 것. backward 전에 loss 에 $S$ 를 곱해 (미분의 선형성으로 모든 gradient 가 $S$ 배) 히스토그램을 위로 밀고, update 전에 $S$ 로 되나눈다. Dynamic scaling: overflow 시 스텝 스킵 + $S$ 반감, 무사고 2000 스텝마다 $S$ 2배 (PyTorch `GradScaler` 기본).

**Q16.** fp32 master weights 가 필요한 이유를 수치로 말하면?

**A.** fp16 상대 정밀도는 $2^{-11}$: weight 가 update 보다 $2048$ 배 이상 크면 $w + \Delta w$ 가 fp16 덧셈에서 $w$ 로 반올림 — update 소실. 실제 update 는 흔히 weight 의 $10^{-4}$ 이하이므로 fp32 사본에 누적하고 fp16 으로 재캐스팅.

**Q17.** Transformer 파라미터 공식과 layer 내 FFN 비중은?

**A.** $\Psi \approx 12Lh^2 + Vh$ (attention $4h^2$ + FFN $8h^2$ per layer). **FFN 이 layer 파라미터·matmul FLOPs 의 2/3** — W14 의 MoE 가 FFN 을 노리는 이유.

**Q18.** Attention score 계산이 FLOPs 를 지배하는 문맥 길이 조건은?

**A.** 토큰·layer 당: matmul 항 $24h^2$, score 항 $4sh$ → $s > 6h$. GPT-2 XL ($h{=}1600$) 이면 $s > 9600$ — 보통 길이에서는 dense matmul 이 지배.

**Q19.** Transformer layer 당 activation memory 공식과 각 항의 출처는?

**A.** $A_{\text{layer}} = sbh(34 + 5as/h)$ bytes (fp16, dropout 포함; Korthikanti et al.). $34sbh$ = attention $11sbh$ + MLP $19sbh$ + LayerNorm 2개 $4sbh$; $5as^2b$ = softmax 출력·dropout mask·dropout 출력 등 $(b,a,s,s)$ 텐서들.

**Q20.** Activation memory 는 $b$ 와 $s$ 에 각각 어떻게 스케일하는가? memory 쪽 $s^2$ 크로스오버는?

**A.** $b$ 에 **정확히 선형** (per-sample 상수 — lab 2 실측), $s$ 에는 superlinear. $5as/h = 34 \Rightarrow s^* = 6.8\,h/a = 6.8\,d_h$ — $d_h{=}64$ 면 $s \approx 435$ 부터 이차 항 지배. FLOPs 크로스오버 ($6h$) 보다 수십 배 이르다.

**Q21.** Gradient checkpointing 의 $O(\sqrt n)$ 유도와 compute 비용은?

**A.** $k$ 개 segment: 상주 = 경계 $k$ + 재계산 중인 segment 내부 $n/k$ → $k + n/k$ 는 $k = \sqrt n$ 에서 최소. 비용 = segment 내부를 backward 중 한 번씩 재계산 = **+1 forward** ≈ 총 FLOPs 의 +33% (fwd:bwd = 1:2), 실측 30–40%.

**Q22.** Transformer 실무의 per-layer checkpointing 이 저장하는 것과 peak memory 는?

**A.** Layer **입력만** — $2sbh$ bytes/layer, 총 $2sbhL$. Peak = $2sbhL$ + backward 중 재계산되는 한 layer 의 내부 ($A_{\text{layer}}$). GPT-2 XL, $s{=}1024$, $b{=}32$: 287 GB → 약 11 GB.

**Q23.** Checkpointing 이 gradient 정확도에 주는 영향은?

**A.** **없음 (bit-identical)** — 같은 커널을 같은 입력에 같은 순서로 재실행할 뿐이다 (lab 3 실측 max diff 0.0). 근사가 아니라 순수한 memory–compute 교환.

**Q24.** Inference 에서 학습 대비 사라지는 메모리 항목과 그 이유, 그리고 activation peak 의 모양은?

**A.** Gradients·optimizer states (update 없음), saved activations (backward 없음 — layer 소비 즉시 해제 가능). Weights 는 $16\Psi \to 2\Psi$. Activation peak ≈ **한 layer 의 working set** (전 layer 합이 아님).

**Q25.** KV cache 의 존재 이유·크기 공식·크기 감각 수치 하나는?

**A.** Autoregressive decode 에서 매 토큰마다 이전 토큰 전체의 $K,V$ 재계산을 피하려 layer 별 캐싱. $M_{KV} = 2 \cdot L \cdot h_{kv} \cdot s \cdot b \cdot \text{bytes}$. OPT-13B fp16: $2 \cdot 40 \cdot 5120 \cdot 2$ B = **토큰당 800 KB**, 2048-토큰 요청당 최대 1.6 GB (vLLM 논문).

---

## From lecture (Week 1 Day 2, 2026-09-04 — DL basics recap)

**Q26.** 비선형 activation function이 신경망에 필요한 이유를 행렬 관점에서 증명하면?

**A.** 비선형성을 제거하면 각 layer는 $\mathbf{z}^{[l]}=\mathbf{W}^{[l]}\mathbf{a}^{[l-1]}$만 남아, $L$개 layer의 출력이 $\mathbf{W}^{[L]}\cdots\mathbf{W}^{[1]}\mathbf{x}$가 되고 이는 항상 단일 행렬 $\mathbf{W}'\mathbf{x}$로 합쳐진다 — 몇 layer를 쌓든 표현력이 늘지 않는다. 비선형 activation이 layer 사이에 있어야만 stacking이 실제로 표현력을 늘린다.

**Q27.** Softmax가 단순 정규화(합으로 나누기) 대신 지수함수를 쓰는 이유와 그 효과는?

**A.** 지수함수 $e^{z_i}/\sum_j e^{z_j}$를 쓰면 출력값들 사이의 상대적 격차가 증폭된다 — 예: softmax 이전에 3~4배였던 차이가 이후 약 40배로 벌어질 수 있다. 이는 cross-entropy loss와 결합했을 때 정답 클래스에 확실히 높은 확률을 주도록 유도하는 효과와 맞물린다.

**Q28.** SGD momentum과 RMSProp의 차이, 그리고 Adam이 이 둘을 어떻게 결합하는가?

**A.** Momentum은 **방향**을 이전 업데이트 방향과 현재 gradient의 가중합으로 바꾼다($m_t=\alpha m_{t-1}+g_t$) — 빠른 수렴이 가능하지만 momentum이 커지면 좋은 minimum까지 지나칠 수 있다. RMSProp은 방향은 그대로 두고 **step size**만 최근 gradient 제곱의 이동평균 $v_t$에 반비례하게 조절한다 — 가파른(최근 gradient가 큰) 영역은 정밀하게, 평평한 영역은 빠르게. Adam은 두 아이디어를 합쳐 momentum과 적응적 step size를 동시에 적용한다.

**Q29.** Optimizer 선택이 단일 GPU의 OOM(out-of-memory) 여부를 가를 수 있는 이유는 (정성적 설명)?

**A.** SGD는 weights+gradient만 저장하면 되어 모델 크기의 약 2배, momentum 추가 시 약 3배, Adam은 momentum류 항과 추가 항($v_t$)까지 weights·gradient와 동시에 유지해야 해서 더 많은 메모리가 필요하다. 그래서 SGD로는 돌아가는 모델이 Adam에서는 메모리 부족을 겪을 수 있다 — 이 정성적 설명은 이 챕터 §5.3의 $16\Psi$ bytes 정밀 회계(파라미터당 fp16 weights 2 + fp16 grads 2 + optimizer states 12)의 도입부에 해당한다.

---

## Anki TSV

```tsv
ERM 목적식과 mini-batch SGD update rule 은?	$\min_w \frac{1}{|D|}\sum \ell(f_w(x),y)$; $w_{t+1} = w_t - \eta \hat g_t$, $\hat g_t = \frac{1}{B}\sum_{\mathcal{B}_t} \nabla\ell$
Mini-batch gradient 의 두 통계적 성질은?	Unbiased ($\mathbb{E}[\hat g]=\nabla L$, uniform 샘플 + mean loss), variance $\propto 1/B$ (i.i.d.)
Learning rate 발산 조건 (quadratic $\frac{\lambda}{2}w^2$)?	$w_{t+1}=(1-\eta\lambda)w_t$ 이므로 $\eta \ge 2/\lambda$ 면 발산 — 최대 곡률이 상한
딥러닝이 reverse-mode AD 를 쓰는 이유는?	Loss 가 스칼라 하나 — backward 한 번으로 모든 $\partial L/\partial w_i$; forward mode 는 $\Psi$ 회 필요
$Y=XW$ 의 backward 두 식과 저장 필요물은?	$\delta_X = \delta_Y W^\top$, $\delta_W = X^\top \delta_Y$ — 입력 $X$ (saved activation) 필요
Backward ≈ 2× forward 인 이유는?	forward matmul 1개가 backward matmul 2개 ($\delta_X$, $\delta_W$) 를 낳음 → 토큰당 학습 $6\Psi$ FLOPs
Backprop 에서 저장되는 것 vs 계산되는 것?	저장: VJP 가 요구하는 forward 중간값 (activations). 계산: VJP = gradients
SGD / momentum / Adam 의 파라미터당 state 수?	0 / 1 (velocity) / 2 ($m$, $v$)
Adam update 식 (bias correction 포함)?	$m_t=\beta_1 m_{t-1}+(1{-}\beta_1)g$, $v_t=\beta_2 v_{t-1}+(1{-}\beta_2)g^2$, $\hat m = m_t/(1{-}\beta_1^t)$, $\hat v = v_t/(1{-}\beta_2^t)$, $w \mathrel{-}= \eta \hat m/(\sqrt{\hat v}+\epsilon)$
Optimizer state 를 fp32 로 두는 이유는?	작은 증분의 장기 누적 소실 방지 + $\epsilon=10^{-8}$ 등이 fp16 하한 근처
Model states vs residual states?	Model: weights+grads+opt states ($\Psi$ 만의 함수). Residual: activations 등 ($b,s$ 의존)
fp16 mixed-precision Adam 의 16 B/param 분해는?	fp16 weights 2 + fp16 grads 2 + $K{=}12$ (fp32 master 4 + $m$ 4 + $v$ 4)
fp32 Adam 의 B/param 은? 시사점은?	$4{+}4{+}4{+}4=16$ — mixed precision 과 동일. MP 가 아끼는 건 activations·bandwidth·연산 시간
fp16 vs bf16 비트 배치는?	fp16 = 1/5/10 (max 65504), bf16 = 1/8/7 (fp32 range) — bf16 은 range↑ 정밀도↓, loss scaling 불필요
Loss scaling 이 막는 것과 메커니즘은?	Underflow ($2^{-24}$ 미만 gradient 소실): loss 에 $S$ 곱해 히스토그램 상향, update 전 $/S$; dynamic 은 overflow 시 반감·무사고 시 2배
fp32 master weights 가 필요한 수치적 이유는?	$|w| \ge 2^{11}{=}2048 \times |\Delta w|$ 면 fp16 덧셈에서 update 소실 — update 는 흔히 weight 의 $10^{-4}$ 이하
Transformer 파라미터 공식은?	$\Psi \approx 12Lh^2 + Vh$ (attention $4h^2$, FFN $8h^2$ per layer; FFN 이 2/3)
Attention score 가 FLOPs 를 지배하는 조건은?	$4sh > 24h^2 \Rightarrow s > 6h$
Layer 당 activation memory 공식은?	$sbh(34 + 5as/h)$ bytes (fp16; attention 11 + MLP 19 + LN 4, 이차항은 $(b,a,s,s)$ 텐서들)
Activation memory 의 $s^2$ 항 지배 시작점은?	$s^* = 34h/(5a) = 6.8\,d_h$ — $d_h{=}64$ 면 $\approx 435$ 토큰 (FLOPs 크로스오버 $6h$ 보다 수십 배 이름)
Checkpointing 의 $O(\sqrt n)$ 유도는?	상주 $\approx k + n/k$ ($k$ 경계 + 재계산 중 segment 내부) → $k=\sqrt n$ 최적
Checkpointing 의 compute 비용은?	+1 forward = 총 FLOPs +33% (fwd:bwd 1:2 기준), 실측 30–40%
Transformer per-layer checkpointing 이 저장하는 것은?	layer 입력만: $2sbhL$ bytes 총량, peak 는 + 한 layer 재계산분
Checkpointing 이 gradient 를 바꾸는가?	아니오 — 같은 커널·같은 입력 재실행이라 bit-identical. 비용은 시간뿐
Inference 에서 사라지는 학습 메모리 항목은?	gradients, optimizer states, saved activations (backward 없음) — weights 는 $16\Psi \to 2\Psi$
KV cache 크기 공식과 OPT-13B 수치는?	$2 L h_{kv} s b \cdot$bytes; OPT-13B fp16 = 800 KB/token, 2048 토큰 요청당 1.6 GB
비선형 activation이 신경망에 필요한 이유 (행렬 관점)?	제거하면 $\mathbf{W}^{[L]}\cdots\mathbf{W}^{[1]}\mathbf{x}$가 단일 행렬 $\mathbf{W}'\mathbf{x}$로 붕괴 — layer를 쌓아도 표현력 불변
Softmax가 단순 정규화 대신 지수함수를 쓰는 효과는?	출력값 간 상대 격차를 증폭 (예: 3~4배 → 약 40배) — cross-entropy와 결합해 정답 클래스에 확실히 높은 확률 부여
Momentum vs RMSProp의 차이는?	Momentum은 방향을 바꿈($m_t=\alpha m_{t-1}+g_t$), RMSProp은 방향은 그대로 두고 step size만 $v_t$(최근 gradient 제곱 이동평균)에 반비례해 조절
Optimizer 선택이 단일 GPU OOM을 가르는 정성적 이유는?	SGD ~2× model size(weights+grad), momentum ~3×(+velocity), Adam은 momentum항+$v_t$까지 동시 유지해 더 필요 — §5.3의 $16\Psi$ 회계의 직관적 도입부
```
