# Week 01 — Exercises

Exam-style problems. Total 100 points. Try each problem before opening the model answer. Calculators allowed; keep 2–3 significant figures.

---

### Q1. The memory wall (6 pts)

State the approximate 2-year growth factors reported by Gholami et al. (2024) for (a) transformer model size, (b) hardware peak FLOPS, (c) DRAM bandwidth, and (d) interconnect bandwidth. Then explain in 2–3 sentences why these numbers imply that the long-run bottleneck of *distributed* training shifts toward communication.

<details>
<summary>Model answer</summary>

(a) Model size: ~410× per 2 years. (b) Peak FLOPS: ~3.0× per 2 years. (c) DRAM bandwidth: ~1.6× per 2 years. (d) Interconnect bandwidth: ~1.4× per 2 years.

Explanation: demand (model size/compute) grows orders of magnitude faster than any hardware supply curve, so scale-out across many devices is unavoidable. Among the supply curves, interconnect bandwidth grows slowest, so each hardware generation the ratio of communication time to computation time for a fixed distributed workload gets worse ($F\beta$ increases). Hence over time the binding constraint of distributed training shifts from FLOPs to moving bytes between devices.

</details>

---

### Q2. Deriving $C \approx 6ND$ (10 pts)

For a dense transformer with $N$ parameters trained on $D$ tokens:

(a) (6 pts) Derive the approximation $C \approx 6ND$ FLOPs, clearly accounting for forward and backward passes.
(b) (2 pts) Which computations does this approximation ignore, and when do they matter?
(c) (2 pts) Why is the backward pass approximately twice the cost of the forward pass?

<details>
<summary>Model answer</summary>

(a) Forward: each parameter participates in one multiply–accumulate per token (2 FLOPs), giving $2N$ FLOPs/token. Backward: each layer computes two gradients — the gradient w.r.t. its input activations (needed to propagate the chain rule) and the gradient w.r.t. its weights. Each is a matrix multiplication of the same dimensions as the forward one, giving $2 \times 2N = 4N$ FLOPs/token. Total $6N$ FLOPs/token, hence $C \approx 6ND$ for $D$ tokens.

(b) It ignores the attention score computation, which is $O(s^2)$ in sequence length $s$ and not proportional to parameter count, plus softmax/LayerNorm/activation functions. These matter when the sequence is long relative to the hidden dimension (long-context training, and the exact accounting in serving analysis). It also excludes any recomputation (that belongs to HFU, not model FLOPs).

(c) Because backward performs two same-shaped matmuls (grad w.r.t. activations, grad w.r.t. weights) for every one matmul in the forward pass: $4N$ vs $2N$ per token.

</details>

---

### Q3. Compute-optimal allocation (12 pts)

You are given a training budget of $C = 1.2 \times 10^{24}$ FLOPs.

(a) (6 pts) Using the Chinchilla rule of thumb $D_{opt} \approx 20\,N_{opt}$ together with $C = 6ND$, compute the compute-optimal parameter count and token count.
(b) (3 pts) A team instead follows the Kaplan-style prescription and trains a 400B-parameter model with this budget. How many tokens does it see, and what is its tokens-per-parameter ratio?
(c) (3 pts) According to Hoffmann et al., which of the two models should reach lower loss, and what real-world model pair demonstrated this?

<details>
<summary>Model answer</summary>

(a) $C = 6ND = 6N(20N) = 120N^2$, so $N_{opt} = \sqrt{C/120} = \sqrt{10^{22}} = 10^{11}$ = **100B parameters**, and $D_{opt} = 20N = 2 \times 10^{12}$ = **2T tokens**. (Check: $6 \times 10^{11} \times 2\times10^{12} = 1.2\times10^{24}$.)

(b) $D = C/(6N) = 1.2\times10^{24}/(6 \times 4\times10^{11}) = 5 \times 10^{11}$ = 500B tokens, i.e. **1.25 tokens/param** — far below 20.

(c) The 100B/2T model: the 400B model is severely undertrained (data-limited term $B/D^{\beta}$ dominates its loss). This is exactly the Chinchilla (70B, 1.4T) vs Gopher (280B, 300B tokens) comparison at equal compute, where Chinchilla uniformly outperformed Gopher.

</details>

---

### Q4. Back-of-the-envelope training time (10 pts)

A 13B-parameter dense model is trained on 260B tokens using 64× A100 GPUs (BF16 peak 312 TFLOPS each) at 45% MFU.

(a) (4 pts) Total training FLOPs.
(b) (4 pts) Wall-clock training time in days.
(c) (2 pts) Name two reasons the real time would exceed your estimate.

<details>
<summary>Model answer</summary>

(a) $C = 6 \times 1.3\times10^{10} \times 2.6\times10^{11} \approx 2.03 \times 10^{22}$ FLOPs.

(b) Effective cluster rate $= 64 \times 3.12\times10^{14} \times 0.45 \approx 8.99\times10^{15}$ FLOP/s. $T = 2.03\times10^{22} / 8.99\times10^{15} \approx 2.26\times10^{6}$ s $\approx$ **26 days**.

(c) Any two of: job interruptions/restarts and checkpoint overhead (Llama 3 reported 466 interruptions in 54 days); MFU degrading at scale or during unstable phases; evaluation/data pipeline stalls; recomputation increasing executed FLOPs beyond model FLOPs.

</details>

---

### Q5. Capacity wall (6 pts)

Explain why a 175B-parameter model cannot even run a pure-fp16 forward pass on a single 80 GB GPU, and compute the minimum number of 80 GB GPUs required merely to *store* its full training state (fp16 weights + fp16 gradients + Adam states, 16 bytes/param), ignoring activations.

<details>
<summary>Model answer</summary>

fp16 weights alone occupy $175\times10^9 \times 2$ B $= 350$ GB $> 80$ GB, so the weights do not fit in HBM even before allocating activations — no forward pass is possible without partitioning the model or offloading. Training state: $175\times10^9 \times 16$ B $= 2.8$ TB; $2.8\,\text{TB} / 80\,\text{GB} = 35$ GPUs minimum just for storage. This is the *capacity wall*: it cannot be solved by adding independent GPUs, only by algorithms that shard the model/states (ZeRO, tensor/pipeline parallelism).

</details>

---

### Q6. Amdahl and Gustafson (10 pts)

A training step has a 2% serial fraction (non-overlapped communication + launch overheads); 98% parallelizes perfectly.

(a) (4 pts) Compute the strong-scaling speedup at $p = 256$ and the asymptotic limit $p \to \infty$.
(b) (2 pts) Compute the parallel efficiency at $p = 256$.
(c) (4 pts) Compute Gustafson's scaled speedup at $p = 256$, and explain in one sentence why the two laws give such different numbers for the same $f$.

<details>
<summary>Model answer</summary>

(a) $S(256) = 1/(0.02 + 0.98/256) = 1/(0.02 + 0.00383) \approx 42$. Limit: $1/(1-f) = 50$.

(b) $E = S(256)/256 \approx 42/256 \approx 16\%$.

(c) $S_{scaled}(256) = 0.02 + 0.98 \times 256 \approx 251$. Amdahl fixes the total problem size so the serial part becomes a growing *fraction* of shrinking per-device work; Gustafson grows the problem with $p$ so the serial part stays a constant fraction of a growing total — i.e., strong vs weak scaling assumptions.

</details>

---

### Q7. Communication-to-computation ratio (12 pts)

Consider synchronous data parallelism for a dense transformer with $N$ parameters. Per step, each device processes $b_{tok}$ tokens at an effective compute rate $F$ FLOP/s. Gradients are exchanged by ring-allreduce, which sends approximately $2 g N$ bytes per device ($g$ = bytes per gradient element), over links of bandwidth $1/\beta$ bytes/s.

(a) (6 pts) Derive the ratio $R = T_{comm}/T_{comp}$ and show that the model size $N$ cancels.
(b) (4 pts) Evaluate $R$ for fp16 gradients ($g = 2$), $F = 300$ TFLOP/s, link bandwidth 25 GB/s, $b_{tok} = 4096$.
(c) (2 pts) List two levers that reduce $R$, and the course week that studies each.

<details>
<summary>Model answer</summary>

(a) $T_{comp} = 6 N b_{tok} / F$ and $T_{comm} = 2 g N \beta$. So

$$R = \frac{2 g N \beta}{6 N b_{tok}/F} = \frac{g F \beta}{3\, b_{tok}}.$$

$N$ appears in both numerator (communication volume $\propto N$) and denominator (compute $\propto N$) and cancels: the ratio depends only on the hardware balance $F\beta$ (FLOPs per byte of network bandwidth) and the per-device workload $b_{tok}$.

(b) $F\beta = 3\times10^{14} / 2.5\times10^{10} = 1.2\times10^{4}$ FLOPs/byte. $R = 2 \times 1.2\times10^{4} / (3 \times 4096) = 24000/12288 \approx$ **1.95** — without overlap, communication takes ~2× longer than computation.

(c) Any two of: compress/quantize gradients, reducing $g$ (W6); overlap communication with backward computation (W3, DDP bucketing); increase $b_{tok}$ via gradient accumulation / larger local batch (W3 — bounded by memory (W2) and critical batch size); synchronize less often (W7 async / W14 DiLoCo).

</details>

---

### Q8. MFU calculation (10 pts)

A 405B-parameter dense model trains on H100 GPUs (BF16 dense peak 989 TFLOPS). Measured throughput is 160 tokens/s *per GPU*.

(a) (6 pts) Compute the MFU (use $C_{token} \approx 6N$).
(b) (2 pts) Is this a good result for large-scale training? Give one reference point.
(c) (2 pts) Why is MFU preferred over tokens/s when comparing two different training setups?

<details>
<summary>Model answer</summary>

(a) Model FLOPs per token: $6 \times 4.05\times10^{11} = 2.43\times10^{12}$. Achieved per GPU: $160 \times 2.43\times10^{12} = 3.89\times10^{14}$ FLOP/s. MFU $= 3.89\times10^{14} / 9.89\times10^{14} \approx$ **39%**.

(b) Yes — Llama 3 405B reported 38–43% MFU (380–430 TFLOPs/GPU) on 16,384 H100s, and PaLM reported 46.2%; ~40% is a strong large-scale result.

(c) Tokens/s depends on the model size and the hardware; MFU normalizes by both (model-required FLOPs and peak FLOPs), making it comparable across models, cluster sizes, and GPU generations.

</details>

---

### Q9. MFU vs HFU (8 pts)

A team enables full activation recomputation, so the hardware executes approximately $8N$ FLOPs per token instead of $6N$ (one extra forward pass). The measured *hardware* FLOPs utilization is HFU = 42%.

(a) (4 pts) Compute the MFU.
(b) (4 pts) Explain why enabling recomputation can simultaneously *increase* HFU and *decrease* MFU, and which metric should be reported for cross-system comparison.

<details>
<summary>Model answer</summary>

(a) MFU $=$ HFU $\times \frac{6N}{8N} = 0.42 \times 0.75 =$ **31.5%**.

(b) Recomputation adds FLOPs that keep the GPU busy (raising the fraction of peak FLOPs executed → HFU up) but those FLOPs are not required by the model — the useful-work throughput (tokens/s) can drop, lowering MFU. MFU should be reported for comparison: it counts only model-required FLOPs, so it is invariant to implementation tricks like recomputation. (HFU ≥ MFU always.)

</details>

---

### Q10. Bandwidth hierarchy (4 pts)

Order the following by bandwidth, fastest first, with an approximate number for each (order-of-magnitude credit): H100 HBM3, A100 aggregate SRAM, NVLink 4 (per direction), NDR InfiniBand (per port), PCIe Gen5 ×16 (per direction).

<details>
<summary>Model answer</summary>

1. A100 aggregate SRAM: ~19 TB/s
2. H100 HBM3: ~3.35 TB/s
3. NVLink 4 per direction: ~450 GB/s (900 GB/s aggregate bidirectional)
4. PCIe Gen5 ×16 per direction: ~64 GB/s
5. NDR InfiniBand per port: ~50 GB/s

(≈3 orders of magnitude from SRAM to the network — the gradient every parallelism placement decision descends.)

</details>

---

### Q11. Roofline analysis (6 pts)

An LLM decode kernel has arithmetic intensity $I = 2$ FLOPs/byte. The GPU is an H100: peak 989 TFLOPS (BF16), HBM bandwidth 3.35 TB/s.

(a) (3 pts) Compute the attainable performance and the fraction of peak it represents. Is the kernel compute- or memory-bound?
(b) (3 pts) Batching 128 requests raises the effective intensity to $I \approx 256$. Recompute the attainable performance. What does this say about how LLM serving systems fight the memory wall?

<details>
<summary>Model answer</summary>

(a) $P = \min(989\,\text{TF},\ 2 \times 3.35\,\text{TB/s}) = \min(989, 6.7)$ TFLOP/s $= 6.7$ TFLOP/s $\approx 0.7\%$ of peak. Severely memory-bound: every generated token re-reads the weights while doing almost no arithmetic per byte.

(b) $P = \min(989, 256 \times 3.35) = \min(989, 857.6) = 857.6$ TFLOP/s — still (barely) memory-bound but near the ridge point ($I^* = 989/3.35 \approx 295$). Batching amortizes each byte of weights over many requests, multiplying arithmetic intensity; this is why continuous batching and KV-cache management (W13) are the core of serving throughput.

</details>

---

### Q12. Mapping problems to the course map (6 pts)

For each scenario, name the parallelism axis or course topic (and week) that addresses it, in one sentence each:

(a) A 7B model fits on one GPU, but one epoch takes three weeks.
(b) A 530B model's layers cannot fit even on one 8-GPU node.
(c) Ten hospitals want to train jointly but cannot legally export patient data.
(d) A chat service's GPU bill is dominated by generating tokens one at a time for thousands of users.

<details>
<summary>Model answer</summary>

(a) Data parallelism (W3): replicate the model, split the batch, allreduce gradients — throughput problem, not capacity.
(b) Pipeline parallelism across nodes combined with tensor parallelism within nodes (W4, composed as hybrid/3D parallelism in W5) — capacity problem requiring the model itself to be partitioned.
(c) Federated learning (W10–11): keep data local, communicate model updates instead, handling non-IID data and privacy.
(d) LLM serving optimization (W13, plus W12 compression): decode is memory-bound, so use batching, KV-cache management (PagedAttention), quantization to cut bytes moved per token.

</details>
