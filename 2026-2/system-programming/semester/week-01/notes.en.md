# Week 01 Lecture Notes — Introduction to Linux (Orientation)

> Source: lecture-audio STT from 2026-09-02 + lecture slides (`L00-courseIntroduction.pdf`, `_private/2026-2/system-programming/week-01/`). Instructor: Seonghoon Park — explicitly mentioned that this is **his own first lecture**, having just joined the university this semester.

## 1. Logistics

- **Instructor**: Seonghoon Park. Newly joined Yonsei this semester; stated that this is his first lecture as a professor (mentioned being nervous but excited).
- **TA**: Gunjoong Kim — a PhD student. Questions about assignments, attendance, etc. should go to the TA's email.
- **Attendance**: electronic attendance via the Y-Attend app. Today was just a test run. Attendance is 10% on the syllabus, but he said he won't deduct much for missing one or two classes (with a nuance that it's fine to skip for things like the Yonsei-Korea rivalry games) — however, he stressed that **the two-thirds attendance requirement is university policy, not his own**, and must be followed.
- **Grading**: midterm + final exams, two programming assignments (possibly three, "probably two"). (Exact weight percentages were not stated in this orientation lecture — needs to be cross-checked against the existing figures in `syllabus.md`.)
- **AI policy**: can't be prohibited outright, but he strongly recommends attempting assignments on your own first and only consulting AI when stuck. Explained that "the trial-and-error process itself is what builds understanding of the kernel's internal principles."
- **Textbook**: does not recommend buying the official textbook (Bovet & Cesati, *Understanding the Linux Kernel*), since it's over a decade old and covers outdated Linux versions. Recommends the up-to-date slides plus the real, current kernel source (a website) instead. Said it's fine to use AI to help understand the slides.

## 2. Nature of the Course — "System Programming" in Name, Linux Kernel Programming in Substance

- The course's goal is the practical side of OS kernel programming, specifically the **Linux kernel**. Recommends taking the Operating Systems course first if you haven't — the key difference is that the OS course is theory-focused and barely touches real Linux code, while this course covers **real code**.
- What you'll learn: how the kernel works internally, how to customize the kernel. Assignments take the form of modifying the kernel or writing kernel modules.
- Emphasis: understanding Linux isn't limited to kernel/systems programming — it's the foundation for building higher-level applications and AI systems too. "You need to know how the OS works to properly build the things on top of it."
- Why Linux: free and open (no cost), a mature OS developed over roughly 30 years. Stressed that it's everywhere — smartphones, watches, appliances ("Linux is everywhere").

## 3. This Semester's Overview (curriculum as described verbally)

Similar in outline to a regular OS course, but the difference is that it's grounded in **real Linux code** rather than theory. Topics to be covered: Linux processes, scheduling, system calls, (kernel) synchronization, memory management, file systems, and so on.

## 4. Smartphone OS Ecosystem Context (used as motivation for the intro)

- Smartphone OSes: Android, iPhone, and (in the past) Symbian, Windows 10 Mobile, webOS, BlackBerry, Tizen, etc. — most are **Linux-based** (free + well-maintained). webOS (LG) and Tizen (Samsung) have been pushed out of smartphones but are now used in home appliances like TVs and refrigerators.
- Android/Tizen stacks: distinguishes the kernel (low-level — CPU scheduling, memory management, file systems) from the framework (high-level — the application layer). Both stacks have the Linux kernel at the very bottom. Mentioned the career relevance — you might end up working on this layer at companies like LG, Samsung, or Google.

## 5. Introduction to the Instructor's Own Research (Mobile AI and Systems Lab)

- Lab name: **Mobile AI and Systems Lab**. Vision: providing users with advanced mobile experiences such as real-time scene understanding for AR and immersive, interactive 3D content (via XR devices like the Meta Quest).
- Technical challenges: vision foundation models, vision-language models, LLMs, NeRF (Neural Radiance Field), 3D Gaussian Splatting, etc. are all extremely compute-heavy. The goal is to run these heavy workloads **in real time on resource-constrained mobile devices** — which are far slower than server-grade GPUs and also face battery and thermal constraints.
- Optimization strategies: distributing work across a smartphone AP's NPU/CPU/GPU, controlling operating frequency (DVFS), fine-grained GPU-NPU scheduling. Combined with AI-side techniques (static model configuration, dynamic neural architectures like multi-exit/stitchable networks, scalable scene representations). **The core message of this introduction is that all of this optimization ultimately requires a deep understanding of OS/Android internals** — his own answer to why we need to learn the kernel.
- Explicitly stated that the details of scheduling and memory management are "graduate/PhD level rather than undergraduate," so they won't be covered in this lecture. Mentioned that interested students are welcome to reach out about internships or PhD positions (lab recruiting).

## 6. Closing

Wrapped up the course overview and took questions. Noted that week 1 allows free withdrawal from the course, and that everyone will be marked present for the first week.
