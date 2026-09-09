# Week 01 Lecture Notes — Quantum Computer Programming (Course Administration)

> Source: lecture-audio STT from 2026-09-02 + lecture slides (`ch00_adm.pdf`, `_private/2026-2/quantum-computer-programming/week-01/`). Instructor: Bernd Burgstaller (CAS3140-01). This is the first time the course is registered in coursebook, so there is no prep chapter (`weeks/`) yet — this pass produces only the lecture notes.

## 1. Logistics

- **Instructor**: Bernd Burgstaller — originally from Austria; MSc and PhD from the Vienna University of Technology (PhD 2005); 3 years at Philips Consumer Electronics; pre-doc at Vienna UT; postdoc at the University of Sydney (2005–2007); professor in the Dept. of Computer Science at Yonsei since 2007. His original field was programming languages / static program analysis.
- **Contact**: email; office is on the 9th floor of the engineering building, room 910. Personal inquiries should be arranged by email.
- **TAs**: 4 people (transcribed as J.P. Lee, Hyunwoo Nam, Inho Lee, Axel Petit — STT pronunciation was imprecise, so the exact spelling needs to be confirmed against the slides). Course-related inquiries go to the shared inquiry address (`inquiry.cas3140@gmail.com`).
- **Class time**: Mon 13:00–14:50, Wed 14:00–14:50, Room D408.
- **Course language**: English (the instructor stated he isn't fluent in Korean). No safety nets — lectures, assignments, exams, and email are all in English. That said, he said he'll prioritize understanding over perfectly correct sentences, and told students not to worry about the language barrier when asking questions or emailing.

### AI Policy (given considerable emphasis on the slides)

- Cited a Google paper ("What do professional software developers need to know to succeed in an age of Artificial Intelligence?", Kam et al., FSE Companion '25) to explain the "proficiency gap" concept: automating assignments with generative AI doesn't build skill (risk of de-skilling), and that gap shows up at the midterm (a paper-and-pencil exam).
- For lab assignments, AI is allowed as a supporting tool (e.g., web search), but solving the assignment itself with AI and submitting that is prohibited. Exams (midterm and final) are paper-and-pencil, with AI use completely prohibited.

## 2. How He Got Into Quantum Computing (personal background)

- During his PhD (around 2000, at Vienna UT), he attended a talk by Professor Zeilinger on photon-entanglement experiments, but recalled that at the time, with no real quantum computer yet, it all felt very far away.
- Since around 2015, commercial quantum computers became accessible via the cloud, which shifted perception in both academia and the public — once real, working quantum computers existed, understanding and using them became important.
- He first offered a quantum computing seminar at Yonsei around 2023, and this semester marks its first offering as a regular undergraduate course (CAS3140). He thanked the students, noting they're "the first ones taking this course."

## 3. Nature and Goals of the Course

- An introduction to quantum computing from a computer-science perspective. Focuses on mathematical/algorithmic foundations, combined with hands-on work writing real quantum programs in Qiskit and simulating/running them on the IBM Quantum Platform (including Yonsei's own Eagle QPU).
- Goals: (1) build a solid understanding of the quantum-mechanical foundations — qubit superposition, entanglement, interference; (2) understand early quantum algorithms — Quantum Key Distribution, Quantum Teleportation, Deutsch's Problem, Bernstein-Vazirani, QFT — and be able to run them on a QPU; (3) get a grasp of recent near-term quantum algorithms (e.g., simulating Hamiltonian dynamics); (4) understand the quantum circuit compilation pipeline and error-mitigation techniques.
- No quantum-mechanics prerequisite is needed — the course covers as much as is needed (the two-state-system level) from scratch. Mentioned that programming (Python), linear algebra, and basic algorithms/data structures are helpful background. The fact that quantum states live in a complex vector space is the genuinely new part.

## 4. Course Format and Materials

- Lectures (Mon/Wed) plus labs running in parallel (6–8 of them, roughly a week's deadline each, expected to take 2–4 hours). **Lab deadlines are strict — no late submissions** (the reasoning: accepting one late submission causes a domino effect). That said, if the whole class finds the workload too heavy, an extension can be requested from the instructor.
- Labs are Jupyter-notebook based (interactive execution — the explanation being that the point isn't to write large software but to understand short, powerful quantum circuits).
- Three reference books (per the slides): Michael Loceff's free online textbook (an introduction for computer scientists, covering only pure quantum states, about 700 pages — said to have originated as a free course); Yanofsky & Mannucci's *Quantum Computing for Computer Scientists* (one of the few textbooks written for computer scientists); Nielsen & Chuang's *Quantum Computation and Quantum Information* (the field's standard reference, written by physicists for physicists, about 800 pages, much more condensed since it also covers error correction). He repeatedly emphasized how rare textbooks written for computer scientists are — directly tied to this course's identity of approaching the subject without a physics background.

## 5. Attendance and Participation

- Starting next Monday (9/7), electronic attendance via the Y-Attend app (entering a 4-digit code shown at the start of class — this is the only method recognized; card taps, etc. are not accepted).
- No separate penalty for absence itself, but **university policy fails (F) any student who misses more than 1/3 of classes**. Documentable excuses (illness, hospital visits, military training, etc.) are accepted if submitted as supporting documents to the course inquiry email. Absence due to employment is not accepted as an excuse (explicitly stated that in that case, taking the course itself would be difficult).
- Mentioned that Y-Attend sometimes has a bug that reverts a successful check-in back to "not attended" — recommended taking a screenshot of a successful check-in and keeping it on file with the course inquiry email, to be used for relief only at the end of the semester if a student ends up short of the 1/3 threshold (individual records are not restored mid-semester; for that you'd need to contact the LearnUs admin team directly).
- **Participation Points (PPs)**: 4% of the total grade. Awarded for asking or answering a question. Must be self-recorded on your personal PP board on LearnUs, following a format (title: a course-specific tag; body: what the contribution was) — one post per point. The scoring curve is very steep — getting even 1–2 points already secures most of the 4%, with diminishing returns after that.

## 6. Grading and Academic Policy

- Grade breakdown (per the slides): midterm exam 32% + final exam 32% + individual lab assignments 32% + participation points 4%. These four items are exhaustive — no other items (e.g., a report) are accepted.
- Absolute grading: A 100–80, B 79–70, C 69–60, D 59–50, F 49–0.
- **Plagiarism policy**: university regulations are very harsh if caught — an F in that course plus a W (withdrawal) in every other course whose exams haven't yet concluded that semester — but the instructor stated he **won't apply this rule on a first offense, treating it as a warning instead** (formal action follows on repeat offenses). Sharing code/text is prohibited, but discussing concepts/ideas together is encouraged. He also gave specific advice: "when helping a colleague, don't just hand over the solution — make them articulate where they're stuck themselves" (because of the risk that a colleague copies it without understanding).
- **Copyright notice**: all course materials (slides, assignments, notebooks, code, recordings included) are copyrighted and may only be used for personal study. Posting them to public GitHub repositories or web servers is prohibited — use private repositories only.

---

## Day 2 (2026-09-07) — Overview, History, Hardware, Schrödinger's Cat

> Source: `ch01_qcp_v2.pdf` (76 slides). Full slide-by-slide detail already lives in the preview chapter [`weeks/01-quantum-computing-overview/README.md`](../../weeks/01-quantum-computing-overview/README.md) — this note only records **what the lecture actually reached (slides 1–25)** plus the examples/analogies/Q&A that came up live. The session covered quantum advantage / the 2019 Google supremacy controversy, Feynman's quotes and the historical timeline, superconducting/trapped-ion/neutral-atom hardware comparisons, physical vs. logical qubits, the definition of Quantum Information Science and its six subfields, and "why powerful / why hard" (decoherence). At the end the professor jumped ahead to use **Schrödinger's cat** to build intuition for superposition (the 1-minute/12-hour/2-week check-in examples, code-switching into the Korean word "goyangi" for cat, the point that a real cat never actually enters superposition since it keeps interacting with its environment). The probability factor (amplitude) itself was deferred — "I'll show you tomorrow (Wednesday)" — continued in Day 3.

## Day 3 (2026-09-09) — NISQ, Scalability, Computing Models, Quantum Circuits

> Source: the same deck (`ch01_qcp_v2.pdf`), roughly slides 26–33. This session followed the slide order directly.

- **Recap**: revisited the cat analogy — why a qubit must be perfectly isolated, why leaking information (measurement) collapses it to a classical state, and how a probability amplitude expresses how much "0" and "1" are mixed in.
- **NISQ era (Preskill)**: noisy 50–100-qubit devices already exist. They can be useful without error correction, but won't change the world by themselves — they're a stepping stone toward future fault-tolerant machines.
- **The steep climb to scalability**: revisited why the physical-qubit overhead per protected logical qubit is so large. The professor's own comment on how undergrad/grad students should read "nobody knows exactly when real quantum advantage arrives" — stay careful, but don't be overly pessimistic either.
- **Quantum speedups in the NISQ era**: revisited deterministic vs. probabilistic algorithms, and historically why probabilistic algorithms were invented in classical computing (randomness makes certain problems easier). Cited **John von Neumann's 1951 paper on the Monte Carlo method**, noting that generating random numbers was itself a research problem — contrasted with quantum computers, which have randomness built in natively (probabilistic collapse upon measurement), unlike classical pseudorandom number generation.
- **Equivalence of quantum computing models**: introduced Quantum Turing Machines, quantum circuits, MBQC, and adiabatic QC as computationally equivalent models, and the "patched" version of the Church-Turing thesis ("any algorithmic process can be simulated efficiently by a probabilistic Turing machine" — "probabilistic" was added because of randomized algorithms).
- **Quantum circuit formalism**: explained concretely why gates must be **reversible** — if a gate takes two qubits in and produces two qubits out, you must be able to reconstruct the input purely from the output. Illustrated via an analogy to a computer architecture's **instruction set architecture (ISA)** — contrasting why classical AND/OR gates are not reversible (a single output bit can't recover the input combination), and therefore why quantum computers cannot use such gates.
- Next class was previewed as moving into the mathematical definition of the qubit (Hilbert space), but this note only records what was explicitly announced in class, not speculation.
