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
