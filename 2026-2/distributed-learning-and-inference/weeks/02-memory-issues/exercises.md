# Week 02 — Exercises: ML Recap & Memory Issues in Deep Learning

Exam-style problems. 100 points total. Answer in English; show all derivations and intermediate numbers for calculation problems.

---

**Q1. (6 pts, short answer)**
(a) (3 pts) Write down the empirical risk minimization objective and the mini-batch SGD update rule, defining every symbol.
(b) (3 pts) State the two statistical properties of the mini-batch gradient estimator (with respect to the full-dataset gradient) that make SGD work, and give the condition each requires.

<details><summary>Model answer</summary>

(a) $\min_w L(w) = \frac{1}{|D|}\sum_{(x,y)\in D} \ell(f_w(x), y)$ where $D$ is the training set, $f_w$ the model with parameters $w$, $\ell \ge 0$ the per-example loss. Update: $w_{t+1} = w_t - \eta\,\hat g_t$ with $\hat g_t = \frac{1}{B}\sum_{(x,y)\in\mathcal{B}_t} \nabla_w \ell(f_{w_t}(x), y)$, $\mathcal{B}_t$ a random mini-batch of size $B$, $\eta$ the learning rate.

(b) **Unbiasedness**: $\mathbb{E}[\hat g_t] = \nabla L(w_t)$, requiring uniform sampling and the loss being a *mean* over the batch. **Variance reduction**: $\mathrm{Var}[\hat g_t] \propto 1/B$ for i.i.d. samples, so larger batches give a less noisy gradient (the statistical basis for learning-rate scaling with batch size, W3).
</details>

---

**Q2. (10 pts, backprop trace)**
Consider the scalar computation $u = w_1 x$, $h = \mathrm{ReLU}(u)$, $\hat y = w_2 h$, $L = (\hat y - y)^2$ with $x = 3$, $w_1 = 2$, $w_2 = -1$, $y = -2$.
(a) (3 pts) Run the forward pass and list *every* value that must be saved for the backward pass, stating which backward rule needs it.
(b) (5 pts) Run the backward pass, computing $\partial L/\partial w_2$ and $\partial L/\partial w_1$ step by step.
(c) (2 pts) Explain why knowing only $L$'s value is insufficient to compute any gradient.

<details><summary>Model answer</summary>

(a) Forward: $u = 6$, $h = 6$, $\hat y = -6$, $L = 16$. Saved: $x$ (for $\partial u/\partial w_1$), the sign/mask of $u$ (for ReLU's VJP), $h$ (for $\partial \hat y/\partial w_2$), $w_2$ (for $\partial \hat y/\partial h$ — already resident as a weight), $\hat y$ (for the loss VJP).

(b) $\delta_{\hat y} = 2(\hat y - y) = 2(-6 + 2) = -8$.
$\partial L/\partial w_2 = \delta_{\hat y} \cdot h = -8 \cdot 6 = \mathbf{-48}$.
$\delta_h = \delta_{\hat y} \cdot w_2 = -8 \cdot (-1) = 8$.
$\delta_u = \delta_h \cdot \mathbf{1}[u > 0] = 8 \cdot 1 = 8$.
$\partial L/\partial w_1 = \delta_u \cdot x = 8 \cdot 3 = \mathbf{24}$.

(c) Each vector–Jacobian product is a function of forward *intermediates* ($h$, $x$, the ReLU mask), not of the loss value. The gradient is a property of the whole forward trajectory; the scalar $L$ contains none of the local Jacobian information.
</details>

---

**Q3. (8 pts, derivation)**
(a) (5 pts) For a linear layer $Y = XW$, write the two backward-pass matrix products and use them to argue that for matmul-dominated networks, backward FLOPs ≈ 2× forward FLOPs.
(b) (3 pts) Using (a), justify the estimate "training costs ≈ $6\Psi$ FLOPs per token" for a dense model with $\Psi$ parameters.

<details><summary>Model answer</summary>

(a) Backward of $Y = XW$ computes $\delta_X = \delta_Y W^\top$ and $\delta_W = X^\top \delta_Y$. Each of these has the same dimensions (hence the same FLOP count) as the forward product $XW$. So every forward matmul spawns two backward matmuls of equal cost → backward ≈ 2× forward.

(b) A forward pass through a dense model performs ≈ $2\Psi$ FLOPs per token (each parameter participates in one multiply–accumulate = 2 FLOPs). Backward adds ≈ $2 \times 2\Psi = 4\Psi$. Total ≈ $6\Psi$ FLOPs per token (Kaplan et al. 2020).
</details>

---

**Q4. (10 pts, short answer + calculation)**
(a) (4 pts) Write Adam's update equations including bias correction, and state the number of persistent per-parameter states for: vanilla SGD, SGD with momentum, Adam.
(b) (3 pts) In full fp32 training, compute total bytes per parameter (weights + gradients + optimizer states) for SGD-with-momentum and for Adam.
(c) (3 pts) Give two reasons optimizer states are kept in fp32 even when forward/backward run in fp16/bf16.

<details><summary>Model answer</summary>

(a) $m_t = \beta_1 m_{t-1} + (1-\beta_1)\hat g_t$; $v_t = \beta_2 v_{t-1} + (1-\beta_2)\hat g_t^2$; $\hat m_t = m_t/(1-\beta_1^t)$, $\hat v_t = v_t/(1-\beta_2^t)$; $w_{t+1} = w_t - \eta\,\hat m_t/(\sqrt{\hat v_t} + \epsilon)$. States per parameter: SGD **0**, momentum **1** (velocity), Adam **2** ($m$ and $v$).

(b) SGD-momentum: $4 + 4 + 4 = \mathbf{12}$ B/param. Adam: $4 + 4 + (4+4) = \mathbf{16}$ B/param.

(c) (i) $v_t$ (and $m_t$) accumulate tiny increments — $(1-\beta_2) = 10^{-3}$ scaled — over many steps; in low precision these increments fall below the representable update granularity and are lost. (ii) The update $\eta\,\hat m/(\sqrt{\hat v}+\epsilon)$ involves small quantities (e.g., default $\epsilon = 10^{-8}$ is below fp16's subnormal range $\approx 6\times 10^{-8}$), so the arithmetic itself degrades in half precision.
</details>

---

**Q5. (12 pts, derivation + calculation)**
Consider mixed-precision (fp16) training with Adam, in the Megatron/ZeRO layout.
(a) (5 pts) Derive the memory consumed by model states per parameter, itemizing every term, and show it equals $(4+K)\Psi$ bytes with $K = 12$.
(b) (3 pts) Compute the model-state memory for a 7B-parameter model. Does it fit on an 80 GB GPU before counting any activations?
(c) (4 pts) Show that *full fp32* Adam training also consumes 16 bytes/param, and explain what mixed precision actually saves, given that model states are unchanged.

<details><summary>Model answer</summary>

(a) fp16 weights $2\Psi$ + fp16 gradients $2\Psi$ + optimizer states $K\Psi$ where $K = 12$: fp32 master weights ($4$) + fp32 momentum $m$ ($4$) + fp32 variance $v$ ($4$). Total $(2+2+12)\Psi = (4+K)\Psi = 16\Psi$ bytes.

(b) $16 \times 7\times10^9 = 112$ GB. No — it exceeds 80 GB before a single activation byte, which is why sharding (ZeRO, W3) or offload is required even at 7B scale for standard mixed-precision Adam.

(c) fp32 Adam: weights $4$ + grads $4$ + $m$ $4$ + $v$ $4$ = $16$ B/param — identical total. Mixed precision therefore does *not* shrink model states; it (i) halves activation memory (activations are stored in fp16), (ii) roughly halves memory bandwidth per tensor, and (iii) enables fast low-precision matmul units — i.e., it buys speed and activation memory, not model-state memory.
</details>

---

**Q6. (10 pts, essay)**
Mixed-precision training with fp16 requires two specific mechanisms.
(a) (4 pts) Explain *gradient underflow*: which fp16 limit causes it, which tensors it hits, and precisely how loss scaling fixes it (including why gradients must be unscaled before the update, and how *dynamic* loss scaling adapts $S$).
(b) (3 pts) Explain why an fp32 master copy of weights is needed, using the ratio between weight magnitude and update magnitude.
(c) (3 pts) bf16 removes the need for one of these two mechanisms but not the other. Which, and why?

<details><summary>Model answer</summary>

(a) fp16 flushes any magnitude below $2^{-24}$ (smallest subnormal) to zero. Gradients — especially activation gradients — concentrate at small magnitudes while the upper fp16 range stays unused, so a large fraction underflows. Multiplying the loss by $S$ before backward scales every gradient by $S$ (linearity of differentiation), shifting the whole histogram into representable range; gradients are divided by $S$ before the optimizer update so the effective step is unchanged (Micikevicius et al. report $S = 8$ sufficed for their SSD detector). Dynamic scaling: on overflow (inf/NaN in gradients) skip the step and halve $S$; after a window of clean steps (e.g., 2000 in PyTorch's `GradScaler`), double $S$.

(b) In fp16 (10+1 mantissa bits), if $|w| \gtrsim 2^{11} = 2048$ times $|\Delta w|$, then $w + \Delta w$ rounds back to $w$ — the update is annihilated. Typical updates (lr × gradient) are routinely $<10^{-4}$ of the weight, so updates must be accumulated into an fp32 master copy, with fp16 weights re-cast from it each step.

(c) bf16 has fp32's 8 exponent bits, so its range extends to $\sim 10^{-38}$: gradient underflow disappears and **loss scaling is unnecessary**. But bf16 has only 7 mantissa bits (worse than fp16's 10), so update annihilation is *more* severe — **fp32 master weights are still required**.
</details>

---

**Q7. (12 pts, calculation)**
A decoder-only transformer has $L = 48$ layers, hidden size $h = 1600$, $a = 25$ heads, vocabulary $V = 50257$.
(a) (4 pts) Estimate the parameter count, itemizing attention, FFN, and embedding contributions.
(b) (4 pts) Per layer and per token, write the FLOP counts of (i) the four attention projections, (ii) the FFN, (iii) the attention-score computations $QK^\top$ and $\mathrm{Attn}\cdot V$. Derive the sequence length at which (iii) overtakes (i)+(ii).
(c) (4 pts) What fraction of layer parameters (and of layer matmul FLOPs) belongs to the FFN? Name one W14-topic system design that exploits this.

<details><summary>Model answer</summary>

(a) Attention $4h^2 \cdot L = 4 \cdot 1600^2 \cdot 48 = 491.5$M; FFN $8h^2 \cdot L = 983$M; per-layer total $12Lh^2 = 1.47$B. Embedding $Vh = 80.4$M (+ positional $\approx 1.6$M). Total ≈ **1.56B** (this is GPT-2 XL, nominal 1.5B).

(b) Per token per layer (2 FLOPs per multiply–add): (i) projections $8h^2$; (ii) FFN $16h^2$; (iii) scores $2sh + 2sh = 4sh$. Overtake condition: $4sh > 24h^2 \Rightarrow s > 6h = 9600$. Below ~9.6k tokens the dense matmuls dominate compute.

(c) FFN holds $8h^2 / 12h^2 = 2/3$ of layer parameters and $16h^2/24h^2 = 2/3$ of layer matmul FLOPs. Mixture-of-Experts replaces the FFN with sparsely-activated experts precisely because that is where most parameters/FLOPs sit (W14).
</details>

---

**Q8. (12 pts, calculation + analysis)**
Use the per-layer activation formula $A_{\text{layer}} = sbh(34 + 5as/h)$ bytes (fp16, with dropout) for a model with $L = 32$, $h = 4096$, $a = 32$, trained at $s = 2048$, $b = 8$.
(a) (5 pts) Compute total activation memory across all layers.
(b) (3 pts) Compute the model-state memory ($16\Psi$ with $\Psi \approx 12Lh^2$) and compare.
(c) (4 pts) Derive the sequence length at which the quadratic term of $A_{\text{layer}}$ overtakes the linear term, evaluate it for this model, and contrast it with the FLOPs crossover from Q7(b).

<details><summary>Model answer</summary>

(a) $sbh = 2048 \cdot 8 \cdot 4096 = 6.71\times10^7$. $5as/h = 5 \cdot 32 \cdot 2048 / 4096 = 80$; factor $= 34 + 80 = 114$. $A_{\text{layer}} = 6.71\times10^7 \times 114 = 7.65$ GB. Total $= 32 \times 7.65 \approx \mathbf{245}$ **GB**.

(b) $\Psi \approx 12 \cdot 32 \cdot 4096^2 = 6.4$B → model states $16\Psi \approx 103$ GB. Activations are ≈ 2.4× model states — and they scale linearly with $b$, so at $b = 32$ they would be ~10×.

(c) $5as/h = 34 \Rightarrow s^* = \frac{34h}{5a} = 6.8\,\frac{h}{a} = 6.8\,d_h$. Here $d_h = 128$, so $s^* \approx 870$. The *memory* quadratic term dominates from ~870 tokens, while the *FLOPs* quadratic term needs $s > 6h = 24{,}576$ — a ~28× gap. "Attention is $O(s^2)$" therefore bites memory long before it bites compute.
</details>

---

**Q9. (10 pts, derivation + calculation)**
(a) (4 pts) For a homogeneous $n$-layer chain, derive the segment count that minimizes resident activation memory under gradient checkpointing, and the resulting memory order.
(b) (3 pts) Explain why the extra compute is approximately one forward pass, and convert that into a percentage of total training FLOPs using the forward:backward ratio.
(c) (3 pts) For the model of Q8, practical transformer checkpointing stores only each layer's input ($2sbh$ bytes/layer). Compute the checkpointed activation memory (including one layer's recomputation working set) and the reduction factor versus Q8(a).

<details><summary>Model answer</summary>

(a) With $k$ segments, resident memory ≈ $k$ segment-boundary activations + the interior of the one segment being recomputed, $n/k$ layers: $M(k) \propto k + n/k$, minimized at $k = \sqrt n$ → $M = O(\sqrt n)$ (Chen et al. 2016).

(b) During backward each segment's interior is recomputed exactly once — in aggregate one extra full forward. With forward:backward ≈ 1:2, total goes from 3 to 4 forward-equivalents → ≈ **+33%** FLOPs (measured 30–40% in practice).

(c) Stored: $2sbh \cdot L = 2 \cdot 2048 \cdot 8 \cdot 4096 \cdot 32 = 4.3$ GB. Peak adds one layer's interior $\approx 7.65$ GB → ≈ **12 GB**, versus 245 GB uncheckpointed: a ≈ **20×** reduction, bought with ~33% extra compute.
</details>

---

**Q10. (10 pts, analysis + calculation)**
(a) (4 pts) List which training memory components disappear at inference time and why, and state what the peak activation footprint of a non-autoregressive forward pass looks like.
(b) (4 pts) For a 7B model with $L = 32$, $h = 4096$, multi-head attention (no GQA), fp16: compute the KV cache size per token, and the total for a batch of 8 requests each at 4096 context. Compare with the fp16 weight memory.
(c) (2 pts) Name the training-time analogue of the KV cache's role in the memory budget, and justify the analogy in one sentence.

<details><summary>Model answer</summary>

(a) Gradients and optimizer states vanish (no update is computed); saved activations vanish because there is no backward pass demanding them — each layer's activations can be freed as soon as the next layer consumes them, so peak activation footprint ≈ one layer's working set, not the sum over layers. Model states drop from $16\Psi$ to just the $2\Psi$ fp16 weights, or less with quantization (W12).

(b) Per token: $2 \times L \times h \times 2\ \text{bytes} = 2 \cdot 32 \cdot 4096 \cdot 2 = 512$ KB. Total: $8 \times 4096$ tokens $\times$ 512 KB = **16 GiB**. fp16 weights: $2 \times 7\times10^9 = 14$ GB — the KV cache alone exceeds the weights.

(c) Activations. Both are the component that scales with batch × sequence rather than with parameter count, and both therefore dominate the budget as workload grows while the weight term stays fixed.
</details>
