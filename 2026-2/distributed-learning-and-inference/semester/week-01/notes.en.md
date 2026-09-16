# Week 01 Lecture Notes — Course Overview & Introduction

> Source: lecture-audio STT from 2026-09-02 (Wed) + lecture slides (`week1-01-course-overview.pdf`, 38 slides). Instructor: Dong-Jun Han. Originals live only in `_private/`.

## 1. Logistics

- **Instructor**: Dong-Jun Han — Dept. of Computer Science, runs the Edge AI Lab.
  - Education/career: BS in Mathematics & Electrical Engineering, KAIST (2016) → MS/PhD in Electrical Engineering, KAIST (2022) → Postdoc @ KAIST (2022.03–2022.12) → Postdoc @ Purdue (2023.01–2024.08) → Assistant Professor @ Yonsei (2024.09–present)
  - Research areas: distributed/federated learning, trustworthy & robust AI (personalization, OOD generalization), resource/data-efficient learning (parameter-efficient fine-tuning, model compression) — directly connected to this course's focus. The "personalization" and "edge-cloud collaboration" framing that recurs in the lecture comes from his own research.
  - Email: djh@yonsei.ac.kr · Office: Engineering Hall 4, Room D720
- **TAs**: Yonghee Choi (2025321337@yonsei.ac.kr), Sunghyun Shin (sunghyun.shin@yonsei.ac.kr)
- **Classroom**: D408 (the instructor pronounced it "E408" during the lecture, but D408 is correct per the slides — an STT-misrecognition correction)
- **Time**: Wed 11:00–11:50, Fri 11:00–12:50 (official schedule includes a 10-minute break). The instructor mentioned he'll likely skip the Friday break and end at 12:40 instead (to leave time for lunch) — actual practice may differ from the official schedule.
- **Office hours**: No fixed hours; email to arrange a meeting (online or offline).

### Grading

| Item | Weight | Notes |
|---|---|---|
| Attendance | 10% | See lateness/absence policy below |
| Assignments | 30% | Mini-assignment 1 (15%) + Mini-assignment 2 (15%); a template will be provided |
| Midterm | 30% | Slide states: 2025-10-24 (Fri) 11:00–12:50 |
| Final | 30% | Slide states: 2025-12-19 (Fri) 11:00–12:50 |

- **Caution**: the exam dates on the slide are labeled "2025." Since this course runs in the 2026-2 semester, the slide has likely reused last year's template — **the actual 2026 dates need to be confirmed via a LearnUs announcement** (see `delta.md`).
- Exam dates are fixed and cannot be changed — students were told to check in advance for conflicts with other courses.
- **Lateness/absence policy**: 3 late arrivals = 1 absence. Up to 2 absences (including combinations up to 6 late arrivals) incur no penalty. Beyond 2 absences, −1 point per additional absence.
- **Late-submission penalty**: 0–6 hours late, 90% credit; 6–12 hours, 70%; 12–24 hours, 50%; beyond 24 hours, 0%.
- Details (assignments, exams, lecture notes) will be posted on LearnUs.

### Course Style

- No textbook — the field is still emerging, so there isn't a suitable one. The instructor reworks material from recent papers directly into slides for easier understanding.
- Reference links provided as needed; Google Colab lab code for some weeks; problem sets to help prepare for the midterm/final.
- Prerequisites: basic understanding of machine learning/deep learning, linear algebra, Python/PyTorch. He emphasized that "an attitude of enjoying learning new things matters more."

## 2. Unpacking the Course Title: Learning, Inference, Distributed

The instructor opened by explaining "why take this course" through the three keywords in the course title ("Distributed Learning and Inference"), one at a time.

### What is Learning (training)?

- A combination of model + data + algorithm + hardware. A broad definition: "you have a model you want to optimize, and data you want the model to learn from, and from that you obtain a model that can solve a given task." AlphaGo example: past game records (data) → fed into the model → the model learns how to win.
- Rather than the traditional supervised/unsupervised/reinforcement-learning taxonomy, he emphasized the broad definition — "any process that uses data to change a model" — as the working definition for this course.
- Explicitly named **algorithm** and **hardware** as the two axes of training. He specifically noted that "many engineering courses ignore efficiency or hardware, but this course covers it" — a statement of the course's identity.

### What is Inference (serving/deployment)?

- The stage after training finishes, where the model is applied to unseen data to provide or receive a service. He stressed that this course clearly distinguishes training from inference.
- Using ChatGPT as an example: "we don't know exactly how it was trained, but it was trained somehow, and that model gets served to us" — inference = the test/service/deployment phase.

### Foundation Model

- Definition (citing Bommasani et al. 2022, verbatim from the slide): "any model trained on broad data that can be adapted (fine-tuned) to a wide range of downstream tasks."
- Distinguishes **pre-training** (building the foundation model itself, mostly in industry — OpenAI/DeepSeek/Meta as examples) from **fine-tuning** (personalizing for a specific task, doable in both industry and academia). Explicitly stated that pre-training requires far more hardware, time, and data than fine-tuning.
- Drew a clear line that this course does **not** go deep into pre-training/fine-tuning algorithms themselves. **What it does cover is the GPU memory/computation/delay problems that arise during that process** — caused by (1) large-scale datasets and (2) large-scale models.

### Distributed — This Course's Central Question

> "How can we efficiently train large-scale models on large-scale datasets, and how should we efficiently deploy and serve the trained models?"

- The first half (efficient training) is the training side; the second half (efficient deployment) is the inference side. Solving these two problems using "distribution" as the tool is where the course title comes from.

## 3. Two Types of Distributed Learning (Type 1 / Type 2)

The instructor himself split distributed learning into two branches using the terms "Type 1" and "Type 2" — note that this is a **higher-level classification than the taxonomy table in the prep chapter** (`weeks/01-course-overview/README.md`, §7.1: data/pipeline/tensor/sequence/hybrid). All the axes in the prep chapter fall under Type 1.

- **Type 1 — making training more efficient with multiple GPUs within a single organization (server/data center/lab)**
  - Starts from the memory/compute limits of centralized training (a single machine, with the model and data both in one place).
  - Solution: introduce multiple machines → **data parallelism** (split the data) or **model parallelism** (split the model; layer-wise splitting is one example — tensor/pipeline parallelism were also mentioned as sub-types of model parallelism, with details to come in later weeks).
  - It doesn't matter whether the GPUs sit on a cloud server, in a data center, or in a lab's own server — the concept of "splitting across multiple devices" itself is what defines Type 1.
- **Type 2 — multi-user collaboration (federated learning)**
  - A situation where data is already naturally distributed across many users (e.g., different hospitals holding different disease data). Unlike Type 1, the split isn't "intentional" — it's inherent from the start.
  - Goal: multiple users collaboratively training one (or several) models without moving their data.

## 4. Distributed Inference

The instructor explicitly raised — and answered — the question of whether **inference, not just training, also needs distribution**. His supporting example was again ChatGPT: billions of users making requests to OpenAI simultaneously → impossible to handle with a single GPU.

- **A Type-1-like approach**: splitting the model across multiple GPUs (to speed up inference) or keeping multiple copies of the model (to handle concurrent users).
- **Edge-cloud collaboration**: keeping a model locally on the user's device as well as on the cloud server, and choosing "where should the prediction happen?" — local inference vs. sending the request to the server and receiving the result back — with the server-side burden growing as the number of users increases as the key trade-off.

## 5. Course Agenda (as verbally described)

1. Background studies (deep-learning basics, W1–2) — a recap for those who already know the material, a first pass for those who don't.
2. Issues in centralized training → distributed training: data parallelism, several types of model parallelism.
3. The fundamental problem of distributed training — communication and delay can't be avoided, and safety/robustness must also be addressed when some devices are malicious or faulty.
4. Type 2 (multi-user, federated learning).
5. Inference strategies (multi-GPU serving, edge-cloud collaboration).
6. Study week → final exam.

He noted the overall structure might shift slightly depending on circumstances, but the big picture is fixed.

## 6. Closing

The instructor summarized the purpose of the first lecture himself: "to explain what this course is about, and why it's important enough to learn." He closed by emphasizing that distributed training and inference techniques are genuinely needed in practice because of large-scale data and model issues. Starting next class (Friday), the plan is a deep-learning-basics warm-up, followed the week after by the memory/compute/delay issues in centralized training.

---

# Day 2 (2026-09-04, Fri) — Basics of Deep Learning (Week 1 & 2)

> Source: lecture-audio STT from 2026-09-04 (Fri) (whisper-1 verbose_json, real per-segment timestamps) + slides `week1-02-dl-basics.pdf` ("Week 1 & 2 — Basics of Deep Learning"). **The slide title spans Week 1&2 as a whole, but what was actually covered in this lecture only goes up through the definition of DNNs, the loss function, and mini-batch SGD from the "This Week's Goal" list — backpropagation, overfitting, batch normalization, and applications to CNN/attention architectures are all in the deck but were explicitly NOT covered today (the instructor deferred them to next Wednesday).** The notes below only cover what was actually taught.

## 7. Logistics

- Attendance will start being checked via the Y-Attend app code from the next session (Fri) on, but the instructor explicitly noted that in past courses there had been a large gap between "students who checked in" and "students who were actually present," so he won't verbally check attendance often. He mentioned that "gaming attendance like that doesn't help you in the long run — you're only cheating yourself." He may still spot-check verbally if the app shows everyone present but the room looks sparse.
- For students unfamiliar with PyTorch/ML, additional PyTorch-basics material has been uploaded to LearnUs/Colab.
- He reiterated that today's (and probably next week's) session won't have attendance checked, since it's a deep-learning-basics recap — students who already know the material can leave, and those who don't should prioritize understanding fundamentals over memorization.

## 8. Definition of a Deep Neural Network

- Nowadays most machine learning models are deep neural networks (DNNs). Structure: input data (an image or a sentence) → DNN → prediction (next-word prediction, image classification, object detection, solving a math problem, etc.). The running example is image classification — feeding in a dog image and getting the decision "dog."
- **Structure of a single neuron** (biologically inspired): inputs $x_0, x_1, x_2$ (real-valued numbers such as RGB values of an image patch, or word embeddings) are each multiplied by a weight $w_0, w_1, w_2$ and summed (weighted sum) → a bias $b$ is added → the result goes through a non-linear activation function to produce the neuron's output. The $w$'s and $b$ are the model parameters, and the goal of training is to optimize them for the task.
- This output becomes the input to a neuron in the next layer, and the same process (multiply → sum → add bias → non-linear activation) repeats. Stacking these neurons vertically and horizontally is what forms a deep neural network.

## 9. Why Stack Layers, and Why Non-Linearity Is Needed

- **Why stack layers**: a neural network is, in the end, just a function. More layers (= more parameters) means the function can express more complex, more varied relationships. Designing a neural network really means designing a specific, complicated function that solves the task well — that's why people keep adding more layers.
- **Why a non-linear activation function is needed (derived directly)**: the instructor directly asked the class whether a non-linear activation function is really needed. If you remove all non-linear activations, the network collapses into a plain chain of matrix multiplications. With input $x$ and layer-1 weights $W_1$ (e.g. a 5-by-4 matrix), layer 1's output is $W_1x$. Without non-linearity, this feeds straight into layer 2 and then layer 3, so the final output becomes $W_3 W_2 W_1 x$ — and the product of these three matrices can always be collapsed into a single matrix $W'$. **In other words, without non-linear activations, a 3-layer network (or even a 100-layer one) can always be rewritten as a single-layer network — stacking layers doesn't increase expressiveness at all.** So the non-linear activation function is what actually gives the network its added expressiveness.
- Which activation function is best depends on the application, dataset, and model architecture — there's no universally "best" one, but non-linearity itself is necessary. Examples given: ReLU (outputs $z$ if $z>0$, else 0 — the most intuitive form), and mentions of Leaky ReLU, sigmoid, and tanh.

## 10. The Softmax Layer

- The network's output is supposed to be a probability, but without any conversion there's no guarantee the raw output falls between 0 and 1. The softmax layer converts the model's output into probability values.
- Method: exponentiate each value, then normalize by dividing by the sum of those exponentials (as opposed to simply normalizing by the raw sum). Because of the exponentiation, the relative gap between output values becomes larger once converted to probabilities — e.g. a 3–4× gap before softmax can become roughly a 40× gap after softmax.
- For a plain classification task, the class with the highest probability is chosen; for an LLM's next-word prediction, the highest-probability next word is chosen. The whole network is often described as a "stack of weights and activations" — this kind of architecture is called a multi-layer perceptron (MLP), or just a deep neural network.

## 11. Forward Propagation

- Forward propagation is the whole process of inputting an image or word into the network and computing the output.
- **Dimension walkthrough (worked in class)**: given a data sample $x$ as a 784-dimensional vector ($x_1,\dots,x_{784}$), the number of columns of layer-1 weights $W_1$ must equal 784 (matching the input dimension), and the number of rows equals the number of neurons in the next layer. Computing $W_1x$, adding the bias, and applying the element-wise non-linear activation gives $a_1$ (whose length equals the number of neurons in that layer). The same repeats for $W_2$ (e.g. with 10 rows if there are 10 output classes), ending with softmax to obtain the probability vector $y$. This entire computation is forward propagation.
- Knowing forward propagation lets you evaluate a model's performance on a new test sample (feed it in → compute → check the prediction). But we still haven't covered **how to actually train** the model — training means optimizing all the $W$ and $b$ parameters for the task, and this isn't solvable by hand, since changing one parameter cascades through the whole downstream computation.

## 12. Loss Function — Cross-Entropy

- To train, you first need an objective/loss function that defines "what to optimize." The goal of neural network training: find the best $W^*$ (all model parameters) that minimizes the loss function.
- Training is based on training data: for AlphaGo, past game records; for image classification, labeled images (this one labeled "dog," that one "horse," another "car"). **The overall loss function is typically defined as the average of the per-sample loss**: for $n$ samples, with $L_k(w)$ the loss on the $k$-th sample, the function should be small when a sample is predicted correctly and large when it's predicted incorrectly.
- **Cross-entropy loss defined (derived via a 5-class example)**: $C$ is the number of classes, $t_i$ is the one-hot-encoded ground truth (1 if $i$ is the correct class, else 0), $y_i$ is the network's softmax output, and $q_k$ is the correct class for sample $k$. Cross-entropy loss is $L_k(w) = -\sum_i t_i \log y_i$; since $t_i$ is 1 only at the correct class and 0 everywhere else, the sum collapses to a single term, $-\log y_{q_k}$. In the slide's worked example (softmax output [0.2, 0.1, 0.4, 0.15, 0.15], with the correct class at the first, 0.2, position), this gives $-\log(0.2)$.
  - (STT correction) The audio alone sounds like "minus log 0.02," but the slide's actual number is 0.2, and $-\log(0.2)$ is the correct computation — the slide is treated as authoritative here.
- Minimizing cross-entropy means pushing $y$ toward the ground truth $t$ — the correct-class probability toward 1, everything else toward 0. Mean squared error (MSE), which directly measures the distance between the two vectors, is mentioned as an alternative, but cross-entropy is more common in practice.
- The final loss is the average cross-entropy over the whole training set. "The model is well trained" means this average loss has been minimized so that as many samples as possible are predicted correctly.

## 13. Gradient Descent

- We now have an objective (the loss function), but not yet a way to optimize it — this is a very high-dimensional, non-convex problem with millions of parameters, not solvable analytically.
- **1D intuition**: plotting $L(w)$ against $w$, if the slope is negative move right, if positive move left ($w_{new} = w_{prev} \mp \Delta$), and if the slope is zero stay put — like a ball rolling downhill. The slope's **magnitude** matters too: it's large far from the minimum and shrinks toward zero near it, so a larger magnitude means moving more aggressively and a smaller one means moving more precisely. This is captured in the update rule $w_{new} = w_{prev} - \eta \cdot \text{slope}$ ($\eta$ = step size / learning rate).
- The gradient is defined as the derivative of the loss with respect to $w$. Since the loss is the average of per-sample losses, its gradient is likewise the average of the per-sample gradients.
- **Full algorithm**: randomly initialize $w_0$ → compute the gradient using the entire training set → update to get $w_1$ → recompute the gradient over the entire set again → get $w_2$ → ... repeated hundreds of times. **One epoch = one complete pass through the entire training dataset** (in this basic form of GD, every single gradient computation uses the whole dataset, so one update = one epoch).
- **Trade-offs**: using the whole dataset each step is stable but computationally expensive, and it's prone to getting stuck in local minima (a real DNN's loss landscape isn't a simple bowl — it's a high-dimensional, non-convex function with a global minimum plus many local minima).

## 14. Mini-Batch SGD

- Same philosophy as GD (repeatedly compute a gradient and update), but **each update uses only a subset (a mini-batch) of the data rather than all of it**. Example: split the full dataset into 3 mini-batches; compute the gradient and update using the first mini-batch, then the next, and so on.
- **Why it's less stable**: the data distribution of a specific mini-batch can differ from that of the full dataset, so the "optimal" gradient direction computed on a mini-batch can diverge from the true full-dataset direction — the path becomes noisier rather than heading straight for the target. The upside is that this noise can actually help escape local minima.
- **Epochs and shuffling**: with 3 mini-batches, one epoch = 3 mini-batch updates. Once an epoch finishes, the dataset must be reshuffled before forming new mini-batches — reusing the exact same mini-batch composition biases the model toward it and hurts performance.
- **GD vs. mini-batch SGD vs. SGD (batch size 1)**: all three share the same update rule ($w_{t+1} = w_t - \eta g_t$), differing only in how many samples $g_t$ is computed over (the whole set / a mini-batch / a single sample). The name "stochastic" comes from the randomness of mini-batch sampling.

## 15. SGD with Momentum, RMSProp, Adam

All of these just swap in a different update formula for the same underlying gradient-descent template (referred to in class as "line 5 of page 27").

- **SGD with Momentum**: considers not just the current gradient $g_t$ but also the previous update direction (momentum) — analogous to driving a car: turning the wheel doesn't make the car instantly change direction, it goes somewhere in between. Momentum is computed as $m_t = \alpha \cdot m_{t-1} + g_t$, and the update is $w_{t+1} = w_t - \eta \cdot m_t$. With $\alpha=0$, $m_t = g_t$, reducing exactly to plain GD with no momentum. Upside: faster convergence, easier escape from local minima. Downside: momentum that gets too large can overshoot past not just bad local minima but even the global minimum or other good local minima.
- **RMSProp**: keeps the direction unchanged and only adjusts the **step size (learning rate)** based on recent gradient magnitude. $v_t$ is an exponential moving average of squared gradients (element-wise, e.g. the vector [1,2,3] squares to [1,4,9]) — a large recent gradient magnitude makes $v_t$ large, which shrinks the effective learning rate (roughly $\eta / \sqrt{v_t}$), leading to more precise exploration; a small recent magnitude makes the effective learning rate larger (moving through quickly). Rationale: a steep region (large recent gradients) is likely near a promising minimum, so explore it carefully; a flat region (small recent gradients) probably has no good minimum, so move through it fast — this directly addresses momentum's problem of overshooting a good minimum.
- **Adam**: combines momentum (SGD-momentum's $m_t$) with RMSProp's adaptive learning rate. There are also bias-correction terms, which the instructor noted aren't that critical to dwell on right now. It's the most widely used optimizer in practice, and the plots shown indicate most modern optimizers (RMSProp, Adam, etc.) outperform plain SGD. **That said, there's no guarantee Adam is always best** — depending on model architecture, dataset, and amount of data, a different optimizer can perform better.

## 16. Memory Cost by Optimizer (Tied Back to This Course's Focus)

The one point in this lecture where the instructor explicitly tied the material back to the course's systems/memory angle: different optimizers require different amounts of GPU memory during training.
- Plain SGD: only needs to store the model (weights) and the gradient — roughly 2× the model size.
- SGD with Momentum: also stores the momentum buffer — roughly 3×.
- Adam: keeps the momentum-like term plus the additional RMSProp-style $v_t$ term, plus weights and gradient, all simultaneously — even more memory.
→ He gave the practical example that on a single GPU, a model that fits under SGD might run out of memory (OOM) under Adam — offered as the reason it's worth understanding exactly what each optimizer stores.

## 17. Preview of Next Session, and What Was Not Covered Today

- The remaining open question, stated explicitly: "how do we actually compute the gradient $g_t$ that all these optimizers use?" — that answer is backpropagation, which he explicitly said would be covered next Wednesday.
- The class ran without a break, and closed by noting that next Wednesday will cover backpropagation, followed by the issues in centralized training (memory/compute/delay — the Week 2 chapter's territory).
- **In the slide deck but not covered in this lecture** (per the no-speculation policy, these are intentionally not written up here yet): the detailed derivation of backpropagation itself, overfitting and its remedies (data augmentation, L2 regularization/weight decay, dropout/dropconnect), batch normalization, and applications to other architectures like CNNs/attention. These will be added, along with an updated `delta.md`, once the lecture(s) that actually cover them are ingested.

---

## Day 3 (2026-09-09) — Backpropagation, Overfitting, and Regularization

> Source: the same deck (`week1-02-dl-basics.pdf`), picking up backpropagation as promised last session. A brief recap of gradient descent and the optimizers opened the class.

- **Finishing the backpropagation derivation**: applied the chain rule layer by layer, propagating the gradient of the final loss with respect to each layer's weights from back to front, worked through with concrete notation (e.g. $a^{(L-1)}$). The key idea: "assuming this value is already known, this one follows directly by the chain rule" — earlier layers reuse gradient values already computed at later layers (hence "back"propagation).
- **Why split train/test**: measuring performance on the training data itself is meaningless (the model was optimized to fit exactly that data), so performance must be measured on validation/test data the model never trained on.
- **Overfitting vs. underfitting**: worked through cross-entropy loss on the **CIFAR-10 dataset** as an example, then illustrated (via a graph) the case where a model is too complex (overfitting — training error keeps dropping while validation error eventually rises again) versus too simple (underfitting).
- **Mitigating overfitting**:
  - **Collect more data** — most direct, but not always feasible.
  - **Data augmentation** — transform existing data to synthesize more.
  - **L2 regularization (weight decay)** — add a penalty on weight magnitude to the loss function. Intuition: prevents the model from relying too heavily on any single weight. Tradeoff: too much regularization prevents the model from learning sufficiently complex patterns.
  - **Dropout** — randomly zero out some neurons during training. Why it helps: it blocks "weird" optimization paths that rely too heavily on specific neuron combinations; the difference in behavior between training and inference time (and their actual performance comparison) was also mentioned.
- **Closing logistics**: PyTorch materials to be uploaded to LearnUs. **Preview for Friday**: batch normalization, CNNs, and the motivation for why distributed training is needed. Next week proceeds into distributed learning proper, as originally planned.

---

## Day 4 (2026-09-11) — Batch Normalization, CNNs, Issues in Centralized Training

> Source: two lecture-audio STT files from 2026-09-11 (one continuous recording session, in chronological order) + slides. The first file finishes off the remainder of the `week1-02-dl-basics.pdf` deck (batch normalization, CNNs) as promised last session. At t=2163 the instructor explicitly announces "the title of this lecture note is Issues in Centralized Training" and switches to a completely new deck — **this new deck was covered start to finish in this single class, from its introduction through its conclusion (next week's preview).**

### 18. Batch Normalization — Motivation

- Brief recap of everything covered so far: defining the loss function → gradient descent → backpropagation to compute gradients → mitigating overfitting (regularization, dropout). Today adds one more concept on top: batch normalization.
- **Motivation derived via example**: predicting house price from inputs (house size, number of rooms).
  - (1) **Within a single mini-batch**, different input features can have different scales/ranges — a large-scale feature risks dominating training. Normalizing lets both features contribute more equally.
  - (2) **Across mini-batches**, scales can also differ (e.g. one mini-batch's values are much larger than another's) — without normalization, a large-scale mini-batch can dominate and destabilize training.
  - (3) Value ranges can also differ **across layers** of the network, letting certain neurons/layers dominate.
- These three observations motivate normalizing the input to each hidden layer, done on a mini-batch-by-mini-batch basis — the core idea of batch normalization.
- **Caveat**: even the original paper doesn't give a fully clear theoretical explanation for why it works, and recent papers are still trying to explain it — there's no universally agreed theory. The motivation above is only an intuitive account.

### 19. Batch Normalization — Mechanics ($\mu$, $\sigma$, $\gamma$, $\beta$)

- Without normalization, a single neuron computes: input $x_k$ → weighted multiply-sum → $z_k$ → non-linear activation. Batch norm **leaves the computation of $z_k$ unchanged** and inserts a normalization layer before $z_k$ goes through the non-linear activation.
- **Normalization procedure**: for one mini-batch ($B$ samples, $k=1,\dots,B$), compute $z_k$ for every sample → compute the mini-batch mean $\mu$ and variance $\sigma^2$ → $\hat z_k = (z_k - \mu)/\sigma$. This puts all values in a statistically similar range.
- **It doesn't stop there — introducing $\gamma, \beta$**: rather than feeding the normalized $\hat z_k$ directly into the activation function, batch norm feeds in a **scaled-and-shifted** version, $\gamma \hat z_k + \beta$. $\gamma$ and $\beta$ are **trainable parameters** that exist per neuron — using batch norm means training additional parameters on top of the original model parameters $W$.
- **Why scale/shift at all**: the intuition is that forcing a fixed normalized range (mean 0, variance 1) isn't guaranteed to be optimal. Making $\gamma, \beta$ learnable gives each neuron the flexibility to have training automatically find its own best normalization range — more room for improvement.
- $\gamma, \beta$ are also **updated via backpropagation** (though their backprop equations differ in form from $W$'s, and the derivation wasn't covered). The key point is that this is easy to implement — even without fully understanding the mechanism, you can just add these layers and run backprop, and $\gamma, \beta$ get learned automatically.

### 20. Batch Normalization — Training vs. Inference

- **The problem**: once training finishes, $\gamma, \beta$ are fixed, but how do you define $\mu, \sigma$ at inference time? Test samples usually arrive one at a time, so there's no way to compute "mini-batch statistics" on the spot (unless multiple test samples are fed in together).
- **The fix**: during training, take a **moving average** of the $\mu, \sigma$ values computed across mini-batches, fix that value, and reuse it at inference along with the trained $\gamma, \beta$.
- **Effect**: batch normalization makes training substantially more stable and faster (in the lecture's plot, the blue curve = with batch norm, orange = without — blue is clearly more stable). It does have limitations, and mini-batch-independent alternatives — **group normalization, layer normalization** — were mentioned (not covered in detail, since understanding batch norm makes them easy to infer).

### 21. CNNs — the Convolution Operation

- Background: backprop has been covered so far using fully-connected layers, but other well-known architectures exist, like CNNs and attention/transformers. This lecture covers CNNs only at a high level (understanding CNNs isn't central to this course, but they'll come up as examples later, hence this background).
- **Basic idea**: a filter (kernel) is placed over an image and scans across it to extract what information it contains. The filter/kernel is the CNN's **model parameter**.
- **The 2D convolution operation**: place the filter at one position on the image, take an element-wise product and sum (a weighted sum) to get a single output value → slide the filter over → repeat the same computation → fill in the entire output feature map.
- **Using multiple filters**: analogous to having multiple neurons in a fully-connected layer, using multiple filters (e.g. a blue filter and a red filter) means each filter independently scans the image to produce its own output, and stacking these gives an output with depth. **Output depth = number of filters** (the same logic as adding more neurons increasing a fully-connected layer's output dimension). A non-linear activation follows, just as in the fully-connected case.
- **Multi-channel input (e.g. RGB)**: real images typically have 3 RGB channels → input depth = 3. In that case **the filter's depth must match the input depth** (e.g. depth 3). Even with depth 3, this still counts as a "single" filter (convolution is applied per R/G/B channel, then the three results are summed into one value) — **output depth is determined by the number of filters, not by filter depth**.
- **General case (multi-channel input + multiple filters)**: with input depth 3, each filter's depth must also be 3, but using 2 filters produces one result per filter (filter 1's result, filter 2's result), stacked into a final output depth of 2. The core rule: **filter depth is matched to input depth, while output depth is determined by the number of filters.**

### 22. CNNs — Overall Architecture, Pooling, and Training

- The big picture: stack (convolution + non-linear activation) blocks across multiple layers (the same logic as stacking layers in a fully-connected network), then attach a fully-connected layer at the end for the final prediction (e.g. classification).
- **Max pooling**: an operation unique to CNNs that compresses information — a mask operation that picks a value (max) or averages values over a region. Purpose: (a) reduces computational burden, (b) makes the model somewhat invariant to small rotations and local distortions — a heuristic established from experience. The convolution + non-linearity + pooling block is repeated multiple times.
- **Why "local" processing makes sense**: each object in an image is highly localized, so nearby pixels are more correlated than distant ones — hence it's reasonable for a filter to process only neighboring pixels together.
- **Training is exactly the same as for fully-connected networks**: forward propagation → compute the loss → backpropagation to compute the gradient → update via mini-batch SGD/momentum/RMSProp/Adam, etc. The specific backprop equations change to match the architecture (the convolution operation), but the procedure itself doesn't change — **only the architecture differs**. Overfitting remedies (dropout, weight decay) and batch normalization also apply equally to CNNs.
- This wraps up the "basics of deep learning" portion (DNN structure, loss function, optimizers, backpropagation, overfitting remedies, batch normalization, and CNNs as a representative architecture). Transformers will be introduced with background as needed later in the course.

---

**(New deck begins here: "Issues in Centralized Training" — t=2163)**

### 23. Issues in Centralized Training — Definition and Motivation

- The instructor opens the new lecture note by emphasizing that all the deep-learning background built up so far was preparation for understanding this problem (and the distributed training to come next week) technically.
- **Definition of centralized training (for this course)**: training where the model and dataset both live on a **single GPU / single machine**.
- **Motivating the problem**: model sizes are growing faster than GPU memory, making it hard or outright impossible to train very large models on a single machine (out-of-memory). Large datasets also add burden not just in memory but in computation and delay.
- **On-device training example**: mobile AI hardware such as Qualcomm's or Apple's has far less memory than expensive server-grade GPUs, so the gap between model size and available memory is even larger — on-device training is a particularly hard version of this problem.
- Conclusion: large models plus large datasets are the fundamental issue in centralized training, and **distributed training is one direction for closing this gap** (introducing multiple machines to train collaboratively).

### 24. The Three Key Metrics: Memory, Computation, Delay

- Stated explicitly in answer to a student's question: the key metrics for looking at issues in centralized training are **memory, computation, and delay**.
- Memory further splits into two: **parameter memory** and **activation memory** — explained in order below.

### 25. Parameter Memory

- Motivating question: if a GPU has 96GB and the model is 120GB, OOM is obvious. But **even an 80GB model, smaller than a 96GB GPU, often still fails to train** — parameter memory is one reason why.
- **SGD**: with $m$ model parameters, the gradient also has $m$ elements (assuming the whole model is updated) → model + gradient ≈ $2m$.
- **SGD with Momentum**: model + gradient + a momentum buffer of the same dimension → ≈ $3m$.
- **Adam**: keeps the momentum-like term, RMSProp's $v_t$ term, the weights, and the gradient all simultaneously → ≈ $4m$ (assuming momentum, $v_t$, weights, and gradient all share the same dimension).
- **Counting parameters**: a linear layer has (input dim $c_i$) × (output dim $c_o$) parameters; a conv layer has (number of filters $c_o$) × $c_i \times k_h \times k_w$ ($c_i$ = input channels, $k_h, k_w$ = filter height/width).
- **Model size = number of parameters × bit width**. Worked example (including a Q&A): with 61 million parameters stored as 32-bit floats, model size ≈ 244MB (61M × 4 bytes). The memory needed per optimizer then scales as **SGD 244×2, SGD+Momentum 244×3, Adam 244×4 (MB)**. Quantizing to 8-bit, etc. reduces total storage but it's still proportional to the parameter count.
- **Two key takeaways**: (1) a GPU with more memory than the model size doesn't guarantee training will fit — because of the gradient and optimizer state. (2) A more complex optimizer (SGD < Momentum < Adam) needs more memory — which is why a model that OOMs under Adam can sometimes run fine under plain SGD.
- Parameter memory is **proportional to model size** and **independent of mini-batch size or dataset size** — the key contrast with activation memory, discussed next.

### 26. Activation Memory

- A **less intuitive** concept than parameter memory, requiring a revisit of how backpropagation is structured.
- **Defining the number of activations**: for a single input sample, the number of activations at a layer equals that layer's number of output neurons (e.g. input 5 → layer 1 output 4 → layer 2 output 3 → layer 3 output 2). **When mini-batch SGD stacks $n$ samples into a tensor**, each layer's activation count scales up by $n$ (e.g. 4n, 3n, 2n). The same holds for conv layers: per-sample activation count is $c_o \times h_o \times w_o$, multiplied by $n$ for a batch of size $n$.
- **Why activations must be stored (the link to backprop)**: in forward propagation, layer $L$'s computation takes $a^{(L-1)}$ (the previous layer's activation, a matrix of "input dimension × batch size") through weights $W$ to get $z$ → non-linear activation → $a^{(L)}$. **Computing the gradient of that layer's weights via backpropagation requires $a^{(L-1)}$ (that layer's input activation), by the chain rule.**
- **No problem for inference alone**: during inference (forward propagation only), once $a^{(L)}$ is obtained from $a^{(L-1)}$, $a^{(L-1)}$ can be discarded immediately (it's not needed for anything downstream) — this repeats all the way to the final output, discarding earlier activations along the way.
- **Cannot discard immediately during training**: since computing each layer's gradient during backpropagation needs that layer's input activation from the forward pass, **all intermediate activations $a^{(L-2)}, a^{(L-1)}, a^{(L)}, \dots$ must be kept until forward propagation finishes** (more precisely, until that layer's backward pass is done). Backward passes run from the output side toward the input side, and once a layer's gradient computation finishes, the activation it used can be discarded — in order, starting with the one closest to the output.
- **Why it's a bottleneck**: the more layers a model has, or the more neurons per layer, the larger the total activation storage needed (→ **a component proportional to model size**). At the same time, each layer's activation dimension **scales with mini-batch size** — e.g. a mini-batch of 1,000 makes the activation dimension 1,000× larger than processing a single sample.
- **Conclusion**: activation memory is simultaneously proportional to both model size and mini-batch size (summed across all layers). This is why **training memory is much larger than inference memory** — training needs activation memory on top of parameter memory. This connects directly to real experience: the same model that OOMs at a mini-batch size of 112 can often train fine once the batch size is reduced to 8 or 16.
- **Mitigation strategy (mentioned only, not detailed)**: instead of keeping every activation, store only some and recompute the rest when needed — **recomputation (activation checkpointing)**, trading memory for extra computation.
- Parameter memory and activation memory don't add up exactly (other memory components exist too), but these two are the primary bottlenecks people try to reduce. When later covering distributed training techniques, the instructor previewed that each technique will be framed in terms of whether it reduces parameter memory or activation memory (e.g. splitting the model across machines reduces both per-machine parameter memory and activation memory; splitting only the dataset across GPUs leaves parameter memory unchanged but reduces activation memory).

### 27. Computation Metrics — MAC and FLOPs

- **MAC (Multiply-Accumulate) operations**: a common operation in a network's forward propagation — one multiplication paired with one accumulation. For a fully-connected layer's forward propagation with input dimension $c_i$, output dimension $c_o$, and mini-batch size $N$, the number of MAC operations is of the form $N \times c_i \times c_o$. More complex structures like CNNs require more MACs, but the detailed derivation wasn't covered.
- **FLOPs (Floating Point Operations)**: a more general, more intuitive metric that treats every arithmetic operation — addition, subtraction, multiplication, division — equally (one operation = one FLOP). One multiplication = 1 FLOP, one addition = 1 FLOP, so a single MAC (multiply + accumulate) = 2 FLOPs.
- Backpropagation's computational cost (in FLOPs) is roughly 2x that of forward propagation (mentioned via a reference link, not derived in detail).
- **Why FLOPs is the standard metric in papers**: it's a **formal** metric independent of any specific hardware, reflecting the computational burden of the algorithm/model itself — which is why research papers arguing for computational efficiency typically report FLOPs (though counting FLOPs precisely during training is harder than during inference).

### 28. The Delay (Latency) Metric

- Another way to measure computational burden is to **measure actual delay on a given piece of hardware** — measuring algorithm A's and algorithm B's delay on the same GPU, and calling whichever takes less time "more computationally efficient." This is easier to measure than FLOPs but has a key limitation: it's **hardware-dependent** — a slow machine can make the gap between two algorithms look larger, while a fast machine might show almost no difference. That's why FLOPs is treated as the more formal metric.
- Latency is determined by both (a) **algorithm/model-side factors** — model size, output activation size, which optimizer is used — and (b) **hardware-side factors** — the processor's operations-per-second throughput, memory bandwidth. Formally modeling this delay is always hard, and the course doesn't need to model it formally — the goal is simply to make training faster in practice (on a single or multiple machines). Some hardware researchers pursue hardware-algorithm co-optimization.
- As with memory, **larger models or larger datasets/mini-batch sizes increase both computation (FLOPs/MAC) and latency**.

### 29. Q&A — Model Size, Trade-offs, and "No Universal Answer"

- **Q: How large should a model ideally be?** A: it depends on the target application. For a strong, general-purpose foundation model, people try to keep growing it as much as possible, but at some point performance can stop improving — even with data continuously being generated, growing the model indefinitely risks overfitting and worse performance unless data volume keeps pace (mentioned as the reason OpenAI keeps collecting data from users — exactly how it's used isn't known, but it's presumably used to keep improving the model). Conversely, for a specific target task far less complex than what OpenAI builds, an infinitely large model isn't needed — the right size has to be found empirically. Also, **architecture choice sometimes matters more than raw size** — e.g. Transformer-based architectures have contributed significantly to performance gains.
- **Q: How much memory margin above model size is actually needed to make training feasible?** A: there's no universal answer — it depends on the mini-batch size and choice of optimizer (mentioned example: even 20GB or 10GB-class models have caused OOM issues in the instructor's own lab). In practice this is approached by trial and error, but the principles learned narrow down the options: reduce the mini-batch size, reduce the model size, or use a simpler optimizer (e.g. SGD instead of Adam). **If keeping the model size fixed matters most for a task**, simplify the optimizer and reduce the mini-batch size; **if keeping the mini-batch size fixed matters most**, simplify the optimizer and reduce the model size instead.
- **General remark**: much of machine learning (why batch normalization works, why Adam performs well, etc.) still has **no definitive answer and relies on experience/heuristics**, and remains an active area of theoretical research (mentioned that math-plus-ML courses in the department go deeper into this theoretical background).

### 30. Conclusion and Next Week's Preview

- Recap of today's issues in centralized training: **memory issues** (parameter memory + activation memory), **computation issues** (MAC/FLOPs), and **delay issues** — all stemming from the fundamental problem that models and datasets are large while a single machine's memory, compute, and time are limited.
- **Next week's preview**: moving directly into distributed training techniques to mitigate these problems. Next week covers **data parallelism** (parallelizing over data without splitting the model); **week 4** covers strategies for splitting the model across machines (model-parallelism approaches). **DeepSeek** was mentioned as a concrete example — DeepSeek's training combined data parallelism with several model-parallelism strategies to reduce memory issues and speed up training.
- The class ran without a break and closed here.

---

## Day 5 (2026-09-16) — Data Parallelism: Parameter Server and Gradient Synchronization

> Source: lecture-audio STT from 2026-09-16 (Wed) + slides (new deck, "Week 3 — Data Parallelism," 49 slides). t=0–419 is a Q&A follow-up recap of last Friday's material (Day 4); at t=419 the instructor announces "today's lecture title is Data Parallelism" and switches to the new deck. **This new deck started its introduction this session but ran out of time (t=2772, 11:00) partway into "Comparison with Centralized Training" — that section's conclusion, and everything remaining in the outline (memory/delay analysis, extension to other optimizers, the fully decentralized setting), were explicitly deferred to Friday.**

### 31. Recap: Follow-up Q&A on Last Week (Activation Memory, Computation/Delay, GPU OOM)

- **When activation memory peaks**: activation memory hits its **maximum** right when forward propagation finishes, then gradually decreases as backpropagation proceeds. Specifically, $A_L$ can only be discarded once the gradient with respect to $W_{L+1}$ is done, and $A_{L-1}$ only once the gradient with respect to $W_L$ is done — i.e., **activations closest to the output are freed first, in order** (a more precise version of Day 4's "freed in reverse order").
- Restated: activation memory dimension is proportional to **both model size (number of layers, neurons per layer) and mini-batch size**. E.g., more neurons in a layer increases $D_{in}$, increasing activation memory; more layers means more activations to store in total (activation memory = the sum across all layers).
- **Q: why is delay approximated as $T_{computation} + T_{memory}$?** A: because of the assumption that memory access (reading) and computation can proceed in parallel — technically the maximum delay is the sum of the two, but under the assumption that computation can proceed on data already read from memory, the approximation roughly holds. **Explicitly noted as not something to dwell on for this course.**
- **Q: why does OOM happen on the GPU, and can things be offloaded to the CPU?** A: yes — for example, offloading **optimizer state (like momentum) to the CPU** is an actual area of research. But without explicitly setting this up, **nothing is offloaded by default**: the CPU's role is limited to loading the model and dataset and constructing mini-batches, while gradient computation, backpropagation, and the optimizer step all run on the GPU. This is the real bottleneck causing GPU OOM — without offloading, **once parameter memory + activation memory exceeds the GPU's VRAM, OOM follows directly.**

### 32. Introducing Data Parallelism — This Week's Motivation and Goals

- Having wrapped last week's recap, the instructor declares "now we're ready to talk about distributed training strategy" — **today's lecture title: Data Parallelism**. "Parallelism" is flagged as a keyword that will recur throughout the course, and there are multiple kinds of parallelism methods to come.
- **Recap of last week (the starting point for this week)**: centralized training = training a model on a specific dataset using a **single machine**. Large-scale datasets and large-scale models cause memory, computation, and delay issues. **Large models** affect both parameter memory and activation memory, and also increase computation delay. **Large datasets** increase the delay to finish one epoch. **Larger mini-batch size** also increases activation memory.
- **Scope for this week**: data parallelism is primarily a technique for mitigating the **large-scale dataset / mini-batch size** problem, not the large-scale model problem (the model-size problem is addressed later, by model-parallelism approaches).
- **Recap of full-batch gradient descent (motivating example)**: in the extreme case of using the entire dataset to compute the gradient and update the model (full-batch gradient descent), **batch size = dataset size**. In that case, since mini-batch size equals dataset size, **activation memory also depends on dataset size** (in contrast to using a small, fixed mini-batch size, where activation memory can be independent of dataset size).
- **Two key questions opening this week's topic**: (1) what if the mini-batch/dataset size you want causes **memory issues** due to the GPU's limited VRAM? (2) what if it causes **delay issues** due to the GPU's limited compute power? → **Data parallelism is presented as the solution that mitigates both of these (memory and delay).**

### 33. Industry Example: How DeepSeek Combines Parallelism Strategies

- The instructor cites DeepSeek's technical report (DeepSeek-V3, published roughly a year and a half ago, cited very heavily) to show that data parallelism, today's topic, is genuinely used in industry.
- **Training framework**: DeepSeek-V3 uses **16-way pipeline parallelism** (next week's topic), **64-way expert parallelism** (a topic before the midterm), and **data parallelism** (this week's topic) together.
- **Inference/deployment strategy**: uses **tensor parallelism** (a topic within the next three weeks), data parallelism, and expert parallelism together.
- **Key takeaway**: different parallelism techniques are **not mutually exclusive alternatives — they're combined together.** In research, people often study a single technique (DP or pipeline parallelism, say) in isolation, but in practice, training a genuinely good model typically means **combining several parallelism techniques at once**. Recent DeepSeek models have also adopted data parallelism, for the several advantages it offers (advantages to be covered this week and going forward, per the instructor's preview).

### 34. Outline for Data Parallelism

The order to be covered this week (through Friday):
1. **How it works** — what the training process looks like (easy to follow if you already know mini-batch/full-batch gradient descent).
2. **Comparison with centralized training** — does it really converge to the same result?
3. **Memory and delay** analysis.
4. **Extension to other optimizers** — since plain SGD can be slow, how to integrate data parallelism with SGD with Momentum or Adam.
5. **(Friday)** **Fully decentralized setting** — applying data parallelism without a central parameter server (only named as a preview today, since the background concepts aren't in place yet).

This note (Day 5) covers **item 1 (how it works)** and only the introduction of **item 2 (comparison with centralized training)** — the rest was deferred to Friday due to time (see §40).

### 35. The Data Parallelism Setup — Splitting the Dataset, Replicating the Model

- **The basic setup is identical to centralized training**: a specific model plus a specific target dataset. The difference is that now **multiple machines** are available — training is no longer confined to a single machine.
- **The key idea — splitting the dataset**: the dataset is distributed across multiple machines. Example (from the slide): with 3,000 data samples, the first 1,000 go to GPU 1, the next 1,000 to GPU 2, and so on → **each GPU is responsible for only its own portion (shard) of the dataset.**
- **The allocation is fixed for the entire training run**: once GPU 1 is assigned its "blue" chunk of data and GPU 2 its "green" chunk, that assignment never changes until training ends.
- **The model is not split (pure data parallelism)**: the original model is **copied as-is** onto every GPU. So while the dataset is distributed across GPUs, **every GPU shares the same model throughout training.**
- **Why the model isn't split**: (1) splitting both data and model at the same time is too complicated, so data parallelism and model parallelism are typically **studied separately**. (2) (as seen in §33) real companies **combine** data parallelism with other model-parallelism strategies, so "never splitting the model" isn't a strict requirement — but replicating the full model is, by definition, what **basic data parallelism** does.
- **Implication flagged for later**: because the model is fully replicated, data parallelism **may not reduce parameter memory** (the model's own size doesn't change). The actual details (under what conditions it does reduce parameter memory) are deferred to when different optimizers are covered (after Friday).
- **Why it's called "data" parallelism**: each GPU computes a gradient from its allocated data, and **multiple GPUs process different data samples simultaneously, at the same time step** — i.e., the computation over the data is what's parallelized across GPUs.

### 36. The Two Key Components: Worker Nodes and the Parameter Server

- **Worker node**: one of several nodes in the data parallelism process, which **can be thought of as a GPU.** Data samples are split across multiple GPUs, and each worker node's role is **to compute a gradient based on its allocated dataset.**
- **Why worker nodes alone aren't enough**: the core of training is "compute the gradient → update the model," but with multiple nodes each producing **its own gradient**, the question becomes how to update a **single model** that reflects the gradients produced by all the different GPUs.
- **Parameter server**: the central component that **aggregates** the gradients computed at the different nodes/GPUs. Its role: receive gradients from the worker nodes, then send back the aggregated result (the updated model).
- **What can serve as the parameter server**: in a data-center setting, worker nodes are GPUs, and the parameter server can be any other node — a CPU, another GPU, whatever — the specific hardware doesn't really matter. What does matter: if the parameter server is **geographically too far from the GPUs, it causes communication delay**, so it shouldn't be placed too far away. In practice, one available node is designated as the parameter server and the rest as worker nodes.

### 37. The Synchronous Training Process — the Parameter-Server Training Loop

Suppose the full dataset $D$ is split into as many pieces as there are worker nodes (4, in the worked example) — $D_1, D_2, D_3, D_4$ — assigned to workers 1 through 4. **$D_1 \cup D_2 \cup D_3 \cup D_4 = D$ (the union is the full dataset), with no overlap between the shards.** This assignment is fixed for the entire training run.

1. **Model initialization + download**: as in centralized training, the first step is to randomly initialize the model ($W_0$). Here an extra step is added: this randomly initialized model must be **transmitted (downloaded) to every worker machine** — the first point where **communication** is added relative to centralized training.
2. **Each worker computes its gradient**: assume for now that every machine uses **full-batch gradient descent** — i.e., each worker computes one gradient using its entire allocated shard. Worker 1 uses its data $D_1$ to compute $G_1$, worker 2 uses $D_2$ to compute $G_2$, and so on — **workers 1 through 4 compute $G_1, G_2, G_3, G_4$** respectively (the definition of each gradient is the ordinary one we already know). **Key point**: every worker uses different data, but **the model must be identical across all of them** (each received the same copy from the parameter server) — since the goal is to optimize a single model that works well across all the data, it wouldn't make sense if the received models differed to begin with.
3. **Gradient upload + aggregation**: each worker uploads its computed gradient to the parameter server, which aggregates them. **Worked example (symbolic)**: assuming all four datasets have the **same number of samples**, the aggregated gradient is
   $$G = \frac{G_1+G_2+G_3+G_4}{4}$$
   (the average of the four gradients). This $G$ is interpreted as a direction reflecting all four datasets — a direction that optimizes the model to perform well on all four of them. *(No concrete numeric values were given in the lecture — $G_1$–$G_4$ are treated purely symbolically; the averaging procedure itself is the point.)*
   - **A note on communication cost**: since a gradient's size equals the model's size (assuming every parameter is updated), the communication cost of this upload step can be quite significant. *(The instructor's exact wording was that "if the model size becomes very large, this communication burden becomes very low," which contradicts the immediately preceding statement that "the communication cost here is very significant" — this reads as a verbal slip that likely meant the burden grows larger, but it is recorded here verbatim as spoken.)*
4. **Model update**: the parameter server updates the model using the aggregated gradient $G$. Under full-batch gradient descent, the update takes the form $W_1 = W_0 - \eta G$ (the ordinary gradient descent update, with the aggregated gradient substituted in). Integrating other optimizers (SGD with Momentum, Adam) is **deferred to Friday's detailed treatment** — today only assumes plain full-batch GD.
5. **Broadcasting the updated model back**: the parameter server transmits $W_1$ back out to every worker node.
6. **Repeat**: steps 2–5 (compute gradient → upload/aggregate → update model → broadcast) are repeated over multiple **training rounds** until satisfactory performance is achieved — the same philosophy as repeating over multiple epochs in centralized training. E.g., with 3 rounds, the models obtained are $W_0 \to W_1 \to W_2 \to W_T$.

**In-class Q&A on this training loop**:
- **Q: is averaging the gradients and updating enough to "exactly" reflect the data across all machines?** A: **yes** — but only under the assumptions that (a) the model is updated on the parameter server, and (b) every machine has the **same number of data samples**. Whether this is exactly identical to centralized training's process is where the next section (§40) begins, but **this session did not reach a conclusion.**
- **Q: when broadcasting the model to multiple machines, does the number of machines affect the delay?** A: on a **wireline-based data center**, the delay isn't exactly proportional but does **increase** as machines are added (because communication can't be fully parallelized) — the number of machines can't be ignored. On **wireless communication** (which covers many real cases), broadcasting means all machines can receive simultaneously, so it **doesn't depend much on the number of machines.**
- **Q: does data parallelism solve the problem of the model itself becoming very large?** A: **no** — data parallelism doesn't address the large-model problem. That's why, in practice, data parallelism is **combined with pipeline parallelism or expert parallelism** to address both problems at once (reaffirming that data parallelism's goal is the dataset problem, not the model-size problem).
- **Q: can it be guaranteed that computation on all machines finishes at the same time?** A: **no** — different machines may have different computational capability or be doing other work concurrently, so completion times can vary significantly. This issue is deferred to the lecture note's **delay section**, and is also the reason **synchronous** vs. **asynchronous distributed learning** need to be distinguished — a topic that will resurface around **week 10** (schedule subject to change), as already previewed in the course overview shown in the first lecture.

### 38. "A Simpler Illustration" — Restating the Same Process

- The same process from §37, restated with a simpler picture: start from a **central parameter server** holding the whole training dataset → distribute the dataset across machines → transmit the current model to all nodes (model download) → each node computes a gradient from its allocated data (different datasets → different gradients) → each gradient is transmitted to the parameter server → the server aggregates and updates the model → repeat until good performance is achieved.
- **Not yet covered** at this point in the lecture: (1) whether this training process yields **exactly the same result** as centralized training, (2) **memory and delay** analysis, (3) how to extend this process to **other optimizers** — all deferred to upcoming lectures (mainly Friday).

### 39. The Communication Bottleneck and a Preview of the Fully Decentralized Setting

- Tying back to today's questions: as the number of machines grows, both the **model-broadcast** burden and the **gradient-upload** communication burden grow, which ultimately creates a **serious bottleneck at the parameter server itself.**
- The **fully decentralized setting** — applying data parallelism without a central parameter server (no central server connected to all machines) — was developed to mitigate this. **To be covered on Friday.**
- The instructor explicitly noted that today's questions (number of machines vs. communication delay, mismatched completion times, etc.) will mostly be addressed **in upcoming lectures.**

### 40. Comparison with Centralized Training — Only the Introduction Was Covered; Deferred to Friday

- The question this section sets out to answer: **does data parallelism's training process guarantee anything?** — does it converge to an arbitrary model, or does it actually follow the **same training process** as centralized training?
- As a reference point, the instructor pulls up centralized training's process from **page 26** of the "Deep Learning Basics" lecture note: $W_0$ is randomly initialized, then trained over multiple epochs/iterations — **each iteration computes the gradient using the entire dataset $D$** and updates the model, repeated across iterations ($T$ = iteration index). This assumes **full-batch gradient descent**, so the notation does not include $N$ (the number of workers).
- On the data-parallelism side, an **additional process** is layered on top of this, introducing a new parameter **$N$ (the number of worker nodes)**: because every worker node received the **same model** from the parameter server, an additional step is introduced where **all workers compute their gradients in parallel** — this is as far as the instructor got.
- **Time ran out here (t=2772, 11:00)**: the instructor explicitly said "starting from this slide, I'll talk about this on Friday" and ended class. In other words, **the actual comparison with centralized training (the proof/explanation of whether the two converge to the same result) was not completed this session and was explicitly deferred to the next class (Friday).** Likewise, the remaining outline items from §34 — memory/delay analysis, extension to other optimizers, and the fully decentralized setting — were all left for after Friday.
