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
