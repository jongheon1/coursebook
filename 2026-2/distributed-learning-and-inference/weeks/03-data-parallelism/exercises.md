# Week 03 — Exercises: Data Parallelism

Exam-style problems. 100 points total. Answer in English; show all derivations and intermediate numbers for calculation problems.

---

**Q1. (4 pts, short answer)**
In synchronous data parallelism, state precisely (a) what is *replicated* across workers, (b) what is *partitioned*, and (c) why no explicit parameter re-synchronization is needed after each optimizer step.

<details><summary>Model answer</summary>

(a) Replicated: the full model parameters, gradients buffer, and optimizer state — every worker holds a complete copy.
(b) Partitioned: the data — each global minibatch is split into disjoint per-worker shards.
(c) All replicas start from identical parameters (broadcast at initialization), receive the *identical* averaged gradient from allreduce every step, and apply the same deterministic optimizer update. By induction the replicas remain bitwise identical forever, so parameters never need to be re-broadcast.
</details>

---

**Q2. (12 pts, derivation)**
Let $p$ workers each compute the gradient of the *mean* loss over a local shard of size $b$, and let the shards be disjoint with global batch size $B = pb$.
(a) (6 pts) Prove that the average of the per-worker gradients equals the gradient of the mean loss over the full global batch.
(b) (6 pts) Give **two** concrete conditions under which one training step of this scheme is *not* equivalent to one large-batch step on a single device, and explain the mechanism of each failure.

<details><summary>Model answer</summary>

(a) With $g^{(r)} = \frac{1}{b}\sum_{x \in \mathcal{B}^{(r)}} \nabla\ell(w;x)$:
$$\frac{1}{p}\sum_{r=0}^{p-1} g^{(r)} = \frac{1}{p}\sum_r \frac{1}{b}\sum_{x\in\mathcal{B}^{(r)}} \nabla\ell(w;x) = \frac{1}{pb}\sum_{x\in\mathcal{B}} \nabla\ell(w;x) = \nabla\Big[\frac{1}{B}\sum_{x\in\mathcal{B}} \ell(w;x)\Big],$$
using disjointness of shards ($\sum_r \sum_{x \in \mathcal{B}^{(r)}} = \sum_{x \in \mathcal{B}}$) and linearity of $\nabla$. This is exactly the large-batch gradient.

(b) Any two of:
- **Sum-normalized loss**: if each worker's loss is a *sum* (not mean) over its shard, each per-worker gradient is $b$ times the local mean, so the averaged gradient equals $\frac{1}{p}\sum_{x\in\mathcal{B}} \nabla\ell = b \cdot \frac{1}{B}\sum \nabla\ell$, i.e., the effective learning rate is multiplied by the local batch size $b = B/p$.
- **BatchNorm**: BN statistics are computed over the *local* batch of size $b$, not the global batch $B$, so the per-sample forward computation differs from a single-device large-batch forward; the schemes optimize different loss functions unless SyncBatchNorm is used.
- **Non-deterministic / rank-dependent ops** (e.g., dropout with per-rank RNG): replicas remain synchronized (gradients are still averaged) but the trajectory no longer bitwise matches the single-process large-batch run.
</details>

---

**Q3. (12 pts, calculation)**
A model has 700M parameters with fp32 gradients ($N = 2.8$ GB). You run ring-allreduce over $p = 16$ workers. Per-message latency is $\alpha = 10\,\mu s$ and each link sustains 50 GB/s ($\beta = 1/(50\times 10^9)$ s/byte). Ignore the reduction-compute term.
(a) (3 pts) How many bytes does each node *send* in total during one allreduce?
(b) (4 pts) Compute the latency term and the bandwidth term of the completion time. Which regime is this allreduce in?
(c) (5 pts) Derive the message size $N^*$ at which the two terms are equal, and evaluate it. What DDP mechanism is justified by this number?

<details><summary>Model answer</summary>

(a) $V = 2\frac{p-1}{p}N = 2 \cdot \frac{15}{16} \cdot 2.8\,\text{GB} = 5.25$ GB per node.
(b) Latency term: $2(p-1)\alpha = 2 \cdot 15 \cdot 10\,\mu s = 300\,\mu s$. Bandwidth term: $2\frac{15}{16} \cdot \frac{2.8 \times 10^9}{50 \times 10^9} = 105$ ms. Bandwidth term dominates by ~350× → **bandwidth-bound**.
(c) Set $2(p-1)\alpha = 2\frac{p-1}{p} N^* \beta \Rightarrow N^* = \frac{p\alpha}{\beta} = 16 \cdot 10^{-5} \cdot 50\times 10^9 = 8$ MB. Tensors smaller than ~8 MB are latency-bound, so reducing them individually wastes time. This justifies **gradient bucketing**: DDP coalesces gradients into ~25 MiB buckets so every allreduce operates in the bandwidth-bound regime.
</details>

---

**Q4. (8 pts, algorithm trace)**
Consider ring-allreduce with $p = 4$ ranks, chunks $c_0..c_3$.
(a) (3 pts) Give the general rule: at reduce-scatter step $t$, which chunk does rank $r$ send, and which does it receive-and-accumulate?
(b) (3 pts) After the reduce-scatter phase completes, which fully reduced chunk does rank 2 own? Justify from the rule.
(c) (2 pts) How many communication steps does the complete allreduce take, and what is the size of each message?

<details><summary>Model answer</summary>

(a) At step $t$, rank $r$ sends chunk $(r - t) \bmod p$ to rank $(r+1) \bmod p$ and receives chunk $(r - t - 1) \bmod p$ from rank $(r-1) \bmod p$, adding it into its local copy.
(b) Rank $r$ ends the reduce-scatter owning the complete chunk $(r+1) \bmod p$; for $r=2$ that is chunk $c_3$. Check: the last chunk rank 2 receives (at $t = p-2 = 2$) is $(2 - 2 - 1) \bmod 4 = 3$, and it has by then accumulated all four contributions.
(c) $2(p-1) = 6$ steps, each moving one chunk of $N/p = N/4$ bytes per link.
</details>

---

**Q5. (10 pts, essay)**
Explain PyTorch DDP's gradient handling during `backward()`:
(a) (3 pts) why gradients are bucketed rather than reduced per-parameter or as one whole-model tensor;
(b) (3 pts) why buckets are assigned in *reverse* order of `model.parameters()`, and what the one-time bucket rebuild after the first iteration accomplishes;
(c) (2 pts) what mechanism triggers a bucket's allreduce;
(d) (2 pts) why all ranks must launch bucket allreduces in the same order.

<details><summary>Model answer</summary>

(a) Per-parameter reduction sends many small messages that fall in the latency-bound regime ($T \approx 2(p-1)\alpha$ each); one whole-model reduction is bandwidth-efficient but can only start after backward *finishes*, killing overlap. Buckets (~25 MiB) are the middle point: large enough to be bandwidth-bound, small enough that early buckets can be reduced while backward still computes later gradients.
(b) Backward produces gradients roughly in reverse order of the forward pass, so reverse-order bucketing makes gradients that become ready together share a bucket, letting buckets fire early. Since this is only an approximation, DDP records the *actual* gradient-ready order during the first backward and rebuilds buckets once to match it, improving overlap for all subsequent iterations.
(c) Each parameter has an autograd hook that fires when its gradient accumulation completes; when *all* parameters of a bucket have fired, DDP launches an asynchronous allreduce on that bucket.
(d) Allreduce is a collective: ranks are matched by call order, not by content. If ranks launched buckets in different orders, different buckets' data would be reduced together (or the job would hang), so the bucket launch order is fixed and identical on all ranks.
</details>

---

**Q6. (8 pts, short answer + calculation)**
(a) (3 pts) Describe exactly what `ddp.no_sync()` changes, and what happens to the gradients computed inside it.
(b) (3 pts) With $K = 8$ gradient-accumulation micro-batches per optimizer step, what fraction of gradient communication does `no_sync` eliminate relative to naive accumulation, and why is the final result identical?
(c) (2 pts) Why must each micro-batch loss be scaled by $1/K$ (assume mean-reduction loss and equal micro-batch sizes)?

<details><summary>Model answer</summary>

(a) `no_sync()` clears DDP's `require_backward_grad_sync` flag, so backward passes inside the context skip all bucket allreduces; gradients simply accumulate into `param.grad` locally. The first forward-backward *outside* the context synchronizes the accumulated gradients.
(b) It eliminates $(K-1)/K = 7/8$ of the communication (1 sync instead of 8 per step). The result is identical because allreduce is linear: averaging the sum of $K$ local gradients equals summing $K$ averaged gradients.
(c) Each micro-batch loss is a mean over $m$ samples; accumulating $K$ such gradients yields $\sum_k \bar g_k$, which is $K$ times the mean over the union of $Km$ samples. Scaling each loss by $1/K$ makes the accumulated gradient exactly the mean over the full effective batch, matching the single big-batch step.
</details>

---

**Q7. (10 pts, calculation + explanation)**
A recipe trains a network with batch size 512 and learning rate 0.2. You scale training to 128 workers with a per-worker batch of 128.
(a) (3 pts) What learning rate does the linear scaling rule prescribe? Show the scaling factor.
(b) (4 pts) State the approximation that justifies the rule (with the two update equations being matched) and explain why it fails in early training, and what the standard remedy is.
(c) (3 pts) You further double the batch and observe that the number of steps to reach the target loss no longer decreases. Name this phenomenon and the quantity that predicts it.

<details><summary>Model answer</summary>

(a) New global batch $B = 128 \times 128 = 16{,}384$; $k = 16{,}384 / 512 = 32$; prescribed lr $= 0.2 \times 32 = 6.4$.
(b) $k$ small-batch steps give $w_{t+k} = w_t - \eta\sum_{j<k}\nabla L(w_{t+j};\mathcal{B}_j)$; one large-batch step with lr $k\eta$ gives $\hat w_{t+1} = w_t - k\eta \cdot \frac1k \sum_j \nabla L(w_t;\mathcal{B}_j)$. These coincide iff $\nabla L(w_{t+j}) \approx \nabla L(w_t)$ — gradients change slowly across $k$ steps. Early in training the network changes rapidly, the approximation is invalid, and the large lr diverges; the remedy is **gradual warmup**: ramp the lr linearly from the base value to $k\eta$ over the first few epochs (5 epochs in Goyal et al.).
(c) The **critical batch size** (regime of diminishing returns / maximal data parallelism); it is predicted by the **gradient noise scale** — once the batch is large enough that gradient noise is small relative to the signal, further averaging adds no information.
</details>

---

**Q8. (12 pts, calculation)**
A 13B-parameter model is trained with Adam under fp16 mixed precision ($K = 12$ bytes/param of optimizer state, fp16 params + fp16 grads = 4 bytes/param) across $N_d = 64$ data-parallel GPUs. Ignore activations.
(a) (2 pts) Per-GPU model-state memory for plain DP.
(b) (6 pts) Per-GPU model-state memory for ZeRO stages 1, 2, and 3 (formula + number for each).
(c) (2 pts) Which is the *lowest* stage that fits model states within a 40 GB GPU?
(d) (2 pts) Why is this analysis incomplete for predicting whether training actually fits?

<details><summary>Model answer</summary>

With $\Psi = 13 \times 10^9$:
(a) $(2+2+K)\Psi = 16\Psi = 208$ GB.
(b)
- Stage 1: $4\Psi + \frac{K\Psi}{N_d} = 52 + \frac{156}{64} = 52 + 2.44 = 54.4$ GB
- Stage 2: $2\Psi + \frac{(2+K)\Psi}{N_d} = 26 + \frac{182}{64} = 26 + 2.84 = 28.8$ GB
- Stage 3: $\frac{16\Psi}{N_d} = \frac{208}{64} = 3.25$ GB
(c) Stage 2 (28.8 GB ≤ 40 GB; stage 1 needs 54.4 GB).
(d) It counts only model states. Activation memory (which scales with batch size and sequence length), temporary buffers, and fragmentation are excluded; stage-3/FSDP additionally needs transient memory for the currently gathered unit. Activations may dominate and require checkpointing.
</details>

---

**Q9. (8 pts, derivation)**
(a) (3 pts) Show that the baseline DP communication volume per step is $2\Psi$ (measured in elements moved per rank), using the decomposition of allreduce.
(b) (3 pts) Explain why ZeRO stages 1 and 2 do not increase this volume.
(c) (2 pts) Derive the stage-3 volume and its ratio to baseline.

<details><summary>Model answer</summary>

(a) Allreduce = reduce-scatter + all-gather. Each moves $\frac{N_d - 1}{N_d}\Psi \approx \Psi$ elements per rank, so allreduce of the full gradient costs $\approx 2\Psi$.
(b) Stage 2: gradients are *reduce-scattered* ($\Psi$) so each rank receives only its shard's averaged gradient; after the sharded optimizer step, updated parameter shards are *all-gathered* ($\Psi$). Total $2\Psi$ — the same two halves of the original allreduce, just with the optimizer step inserted between them. Stage 1 needs the same accounting: with optimizer states sharded, rank $r$ can produce updated parameters only for its own slice, so an all-gather of updated parameter shards ($\Psi$) is unavoidable — keeping a full gradient allreduce ($2\Psi$) on top of it would cost $3\Psi$. Stage 1 reaches $2\Psi$ by the same rearrangement as stage 2: reduce-scatter of gradients ($\Psi$) + all-gather of updated parameters ($\Psi$).
(c) Stage 3 adds parameter reconstruction: all-gather of parameters in forward ($\Psi$) + all-gather again in backward ($\Psi$) + reduce-scatter of gradients ($\Psi$) $= 3\Psi$, i.e., **1.5×** baseline.
</details>

---

**Q10. (6 pts, short answer)**
Give two structural differences between the parameter-server architecture and allreduce-based data parallelism, and one reason why dense large-model training converged on allreduce. (Full PS treatment comes in Week 7.)

<details><summary>Model answer</summary>

Differences (any two): (1) PS is asymmetric — workers push gradients to and pull parameters from dedicated servers, while allreduce is a symmetric peer collective with no central node; (2) the PS server ingress scales as $O(pN)$ unless sharded over many servers, while ring-allreduce keeps per-node traffic at $2\frac{p-1}{p}N$, independent of $p$; (3) PS naturally supports asynchronous/bounded-stale updates, allreduce is inherently synchronous.
Why allreduce won for dense training: per-node bandwidth is constant in $p$ (no central bottleneck) and synchronous execution preserves exact large-batch SGD semantics, which keeps convergence behavior predictable on homogeneous datacenter interconnects.
</details>

---

**Q11. (10 pts, design)**
You have 64 GPUs (8 nodes × 8 GPUs; fast NVLink within a node, 100 Gb/s Ethernet between nodes), 40 GB memory per GPU, Adam + fp16 ($16$ bytes/param of model states).
(a) (5 pts) For a **1.3B**-parameter model, choose between plain DDP and FSDP `FULL_SHARD`, justifying with the memory formula and communication considerations.
(b) (5 pts) For a **13B**-parameter model, propose a configuration (sharding strategy and its scope) and justify it, referring to the stage-3 communication cost and the cluster's two-tier bandwidth.

<details><summary>Model answer</summary>

(a) Model states: $16 \times 1.3 = 20.8$ GB < 40 GB, so plain DDP fits with room for activations. Choose **DDP**: it communicates only $2\Psi$ (vs $3\Psi$ for FULL_SHARD), overlaps allreduce with backward, and avoids per-unit all-gathers on the slow inter-node link. Sharding would trade unneeded memory savings for 1.5× communication.
(b) $16 \times 13 = 208$ GB per GPU is impossible unsharded, so sharding is mandatory (from Q8, sharding over ≥ 8-way at stage 2 or full stage 3 fits). The stage-3 penalty is $3\Psi$ of communication with all-gathers on the critical path, so the shard group should live on the *fast* interconnect: use **hybrid sharding** — fully shard within each 8-GPU NVLink node (per-GPU model states $= 208/8 = 26$ GB, fits) and replicate/allreduce across the 8 nodes like ordinary DP. This confines frequent all-gather/reduce-scatter traffic to NVLink and sends only the DP gradient reduction over the 100 Gb/s inter-node links (this is FSDP `HYBRID_SHARD`; the same placement logic returns as the "TP inside, DP outside" principle in W5).
</details>
