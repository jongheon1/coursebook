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

## Day 4 (2026-09-14) — Wrapping Up Chapter 1 (Circuits, SDKs, Algorithms), Stern-Gerlach, Double-Slit, Introducing Probability Amplitudes

> Source: as of this session, the slide deck was revised to `ch01_qcp_v2c.pdf` (81 slides) — pages 1–44 are identical to the previously used `ch01_qcp_v2.pdf` (76 slides), but everything from page 45 onward was restructured, with new pages inserted ("The Failure of Probability Theory," "The Birth of Quantum Mechanics," "Some of the Early Quantum Physicists," "Modified Probability Theory (1)-(3)"). All page numbers below refer to the new v2c numbering. This session started around slide 34 (wrapping up Chapter 1's circuits/algorithms) and ran out of time around slide 61 (Wave-Particle Duality) — **slides 62 onward (photon polarization, bits vs. qubits) were not reached this session** and carry over to the next one.

### Wrapping Up Chapter 1 (1) — Circuit Design Rules and the SDK Ecosystem (p.34–37)

- **Basic picture of a circuit**: quantum algorithms are expressed as circuits, and circuits consist of gates. Qubits flow left to right on lines; the input side is usually classical zeros (the classical computer prepares and uploads the circuit — a classical computer cannot create a quantum state in the first place).
- Today's quantum computers only offer operators taking **at most two qubits** as input/output. If an operation needs three or more qubits, the compiler breaks it into smaller ones. This basic gate set isn't arbitrary — it's chosen to be sufficient to express any quantum algorithm.
- **ISA analogy**: this is similar to the instruction set architecture (ISA) of a classical computer — x86 and ARM look different but are both Turing-complete and equally powerful. However, the quantum computer's instructions (gates) must take a very particular form: they must be **unitary**.
- The defining property of a unitary operation $U$ is **reversibility** — a $U^{-1}$ must always exist so you can return to the original state after computing. If this fails, it isn't a proper unitary gate and won't work on a quantum computer.
- Qubits are manipulated via microwave signals — also classically generated and controlled. At the end of the circuit, **measurement** collapses each qubit to a classical 0/1 (the collapse of the wave function / measurement collapse).
- **Programming layers** (introduced from low-level to high-level; vendor-specific):
  - **OpenQASM** (open quantum assembly language) — a low-level assembly-style representation listing gates in sequence.
  - Graphical tools like **IBM Composer**, or the Python library **Qiskit** (provided by IBM) — using Qiskit naturally targets IBM's QPUs.
  - **Amazon Bracket** (AWS) — AWS offers other vendors instead of IBM, so SDKs are somewhat segmented by vendor. Most are Python-based and very similar to each other.
  - **Pulse-level control** — even lower than the instruction set; some SDKs offer low-level interfaces for directly programming the microwave pulses.
- **Expected impact areas of quantum computing**: cryptography (directly tied to factorization), chemistry (simulating nature, e.g., drug design), materials science, optimization problems, and machine learning. However, the entire quantum computing stack (device → compiler → language → applications, plus cross-layer optimization) is still immature — there's a lot of work left in removing noise, achieving fault tolerance, and finding new applications/algorithms. At the compiler layer specifically, minimizing swap operations (the overhead of swapping two qubits that aren't connected on the chip) was mentioned as a task.
- **Two jobs for computer science**: (1) **circuit design** — implementing an already-known algorithm as an efficient circuit that doesn't amplify noise too much and doesn't take too long. (2) **algorithm design** — since quantum computers are inherently probabilistic, designing algorithms so that the random outcomes play out in our favor. A good probabilistic algorithm should succeed with high probability within a few tries (an algorithm that only succeeds once in a million tries is useless).

### Wrapping Up Chapter 1 (2) — Reversibility of Unitary Gates: Proving Fan-in/Fan-out Are Impossible (p.34)

The most rigorously proven point in this session — the reason quantum circuits are a pure left-to-right linear sequence with no if-statements and no loops.

- **Why fan-in (e.g., 2-bit input → 1-bit output) is impossible — proven via the Boolean AND gate**:
  - The classical AND truth table: $(x,y)\to \text{AND}(x,y)$ gives $(0,0)\to0$, $(0,1)\to0$, $(1,0)\to0$, $(1,1)\to1$.
  - Given output 0 and asked to reconstruct the input, it's impossible — an output of 0 could correspond to any of $(0,0)$, $(0,1)$, or $(1,0)$. So you cannot go from the output back to the input — this is **irreversible**.
  - Losing that one bit of information is exactly what makes it irreversible — a fan-in structure ("more coming in, fewer going out") can never be implemented by a unitary gate.
- **Why fan-out (e.g., 1-bit input → 2-bit output, i.e., duplicating the input) is impossible — for a different reason: the no-cloning theorem**:
  - Producing two output lines from one input qubit would require copying that qubit.
  - But the **no-cloning theorem** says an arbitrary quantum state cannot be copied — so fan-out is also structurally impossible.
- **Therefore a circuit cannot contain a loop, either**: building a loop-like structure inside a circuit would require both merging back together (fan-in) at some point and splitting again (fan-out), and both are forbidden — so a loop simply cannot exist. This is the underlying reason a quantum circuit "is not a von Neumann program — no if-statement, no loop, just a pure linear sequence of operations flowing left to right."

### Wrapping Up Chapter 1 (3) — Gates Are Matrices: Scaling Qubit Count via the Hadamard Gate (p.38–40)

- Unitary gates cannot be defined by a truth table like classical gates — instead they are defined by a **matrix**.
- The example used is the **Hadamard gate** $H$. Specifically, the **second-order** Hadamard gate $H^{\otimes 2}$ — "second-order" means two qubits in and two out (not "squared"; input count must equal output count since fan-in/fan-out are forbidden).
- A two-qubit quantum state is written in ket notation as $|\psi\rangle_2$ (the subscript 2 means "a state made of 2 qubits"). Each qubit internally has two amplitudes, so the full two-qubit state is a vector of four complex amplitudes $\alpha,\beta,\gamma,\delta$.
- The gate notation $H^{\otimes2}|\psi\rangle$ is exactly **function application** — like $f(A)$ from high-school math, it means applying gate $H$ to state $\psi$.
- **The actual matrix**: the second-order Hadamard gate is $\frac{1}{2}$ times the following $4\times4$ matrix, applied to the two-qubit state vector as a matrix-vector product:
$$
H^{\otimes 2} = \frac{1}{2}\begin{pmatrix}1&1&1&1\\1&-1&1&-1\\1&1&-1&-1\\1&-1&-1&1\end{pmatrix}
$$
- The professor worked this out row by row on the board (the overall $\frac12$ factor is applied at the end), for the input vector $(\alpha,\beta,\gamma,\delta)^T$:
  - Row 1 → $\alpha+\beta+\gamma+\delta$
  - Row 2 $(1,-1,1,-1)$ → $\alpha-\beta+\gamma-\delta$
  - Row 3 $(1,1,-1,-1)$ → $\alpha+\beta-\gamma-\delta$
  - Row 4 $(1,-1,-1,1)$ → $\alpha-\beta-\gamma+\delta$
  - These four values (times $\frac12$) are the two-qubit output state after the gate. This output becomes the input to the next gate, and so on until the end of the circuit, at which point measurement collapses each amplitude to 0 or 1.
- **Where this 4×4 matrix comes from** (previewed in response to a student question): the $\otimes$ symbol is not multiplication but the **tensor product**. The Hadamard gate is originally a **single-qubit gate** (a 2×2 matrix); extending it to two qubits requires taking the tensor product with another single-qubit Hadamard gate — $H \otimes H$. Tensoring two 2×2 matrices produces a 4×4 matrix. (The exact entry-by-entry derivation was not covered this session — previewed for a future lecture.)
- **What scaling qubit count means**: the course's planned order is single-qubit gates → applying them to single qubits in Hilbert space → two qubits and two-qubit gates → n qubits. **Going from one qubit to two qubits is a major leap** — the moment there are two qubits, **entanglement** appears (operating on one qubit instantly affects the other untouched qubit, a phenomenon classical bits don't have: with two classical bits, flipping one never moves the other). By contrast, **going from two qubits to n qubits is comparatively trivial**, since the tensor-product mechanism already exists.

### Wrapping Up Chapter 1 (4) — Algorithm Overview: Deterministic vs. Probabilistic, and the Chapter 1 Outlook (p.41–44)

- **Circuits as algorithms**: "algorithm" might conjure up multi-page Python code full of subroutines, but quantum circuits are surprisingly simple and compact. The first algorithm's circuit structure introduced today: $n$ zero-state qubits → an **n-fold Hadamard gate** ($H^{\otimes n}$, on the lower $n$ qubits) → a $U_f$ operation → measure the lower $n$ qubits → apply another Hadamard gate to the upper qubits → measure the upper $n$ qubits.
- **Access points**: an analysis method of writing down the quantum state explicitly at each stage of the circuit (right after input, right after the first Hadamard, right after $U_f$, right after the second Hadamard) to track what's happening — the professor previewed spending considerable time on this algorithm going forward.
- **Deterministic algorithms**: a type with no randomness at all except for the final measurement. Run the circuit **exactly once** and measure — that value is the final answer (assuming a perfect quantum computer; in practice, noise could interfere). Typical shape: run the circuit once → if the output is such-and-such, the answer is this; if different, the answer is that.
  - By contrast, **running the same computation classically requires running the circuit many times** — this difference is exactly **quantum parallelism**: a quantum state carries multiple possibilities at once.
  - **Student question**: "When we use these deterministic algorithms on a quantum computer, are we using algorithms a classical computer could also run, or only ones a classical computer cannot run?"
  - **Instructor's answer**: a quantum computer **can simulate any classical computation without issue**. Going the other way (a classical computer simulating a quantum computer) requires **memory that grows exponentially** with qubit count, becoming intractable already around 50 qubits — that contrast is the crux of the answer.
  - In the course of this answer, the earlier-mentioned $U_f$ was clarified further: $U_f$ is **a classical AND gate converted into a unitary operator**. The original AND gate is irreversible (as proven above) and can't be used as-is, but modifying it to **preserve inputs $x,y$ at the output** (copying $x$ and $y$ through to the output, plus one additional element not yet explained) makes it a reversible "quantum AND gate" — because the output now retains enough information to reconstruct the full input. **What exactly this additional element is was not explained this session — deferred to later**; this gap is recorded as-is, without speculation.
- **Probabilistic algorithms**: most real quantum algorithms are of this type. Run it, check the measurement to judge success/failure, and rerun on failure — what counts as success or failure is always clearly specified per algorithm. A good probabilistic algorithm is designed to succeed with very high probability — **Shor's algorithm** was cited as an example: it may fail on the first try for factoring, but has a very high probability of succeeding within very few retries.
- **Chapter 1 outlook/perspective**: quantum computing is a new way of computing that exploits microscopic quantum effects (superposition, entanglement, interference, measurement) — problems like factorization get faster, and problems like simulating atoms/molecules that were previously intractable become tractable. However, **the quantum computer should not be expected to replace the classical computer** — smartphones and desktops will stay classical for a very long time, perhaps forever (classical computers are already very efficient at what they do). Superconducting quantum computers must be cooled to minus 273°C, so they're not portable, and factoring prime numbers isn't a daily need anyway. Problems classical computers already handle well will stay classical, while quantum computers will carve out their own niche among problems that are hard for classical computers.

### Entering Part 3 — Physical Foundations of Quantum Mechanics: Previewing Three Experiments (p.45)

- Physics originally only dealt with the macroscopic world — there were no instruments to measure atoms, electrons, or photons. Only in the early 1900s did devices emerge that could observe the microscopic world, and the results obtained then showed **contradictions that classical physics could not explain** — this is how quantum effects suddenly appeared on physics' radar.
- **Three experiments** were previewed as a good entry point into quantum effects (only the first two were covered this session): (1) the Stern-Gerlach experiment, (2) the double-slit experiment, (3) a third experiment whose name was not even mentioned this session — not speculated on here.

### The Stern-Gerlach Experiment (p.46)

- **Experimental setup**: performed around 1920 by two researchers, Stern and Gerlach. Individual silver atoms, heated in a furnace, were shot one at a time through a magnetic field (a magnet with North and South poles) onto a screen — each hit left a dot.
- **Mechanism via the bar-magnet analogy**: think of a silver atom as a bar magnet. The apparatus's magnetic field is uneven — **stronger at the top (North pole, pointed shape) and weaker at the bottom (South pole, flat)** — by design.
  - A bar magnet with South up / North down is attracted toward the apparatus's North pole; since the field is stronger up top, it gets pulled upward and hits near the top of the screen.
  - A bar magnet with North up / South down is repelled by like poles; since the field is weaker at the bottom, it gets pushed down and hits near the bottom.
  - A horizontal orientation (equidistant from N/S) keeps its trajectory and hits the middle. Tilting it gradually shifts the hit point up or down proportionally.
  - **Classical expectation**: shooting bar magnets at random orientations should produce hits spread **continuously across the entire range** from top to bottom.
- **Applied to silver atoms**: the apparatus detects the outermost electron of the silver atoms coming from the furnace. An electron can be thought of as a rotating sphere, and this rotation (**spin**, i.e., angular momentum) generates its own magnetic field. Electron spin orientation is random (vertical up/down or any direction in between), so **the classical expectation, just as with bar magnets, was hits spread continuously across the whole screen**.
- **Key observation (actual result)**: electrons were detected at **only two positions** — half at the top, half at the bottom. **Nothing in between.** Unlike bar magnets, no intermediate orientation produced an intermediate hit position.
- **Origin of the name "quantum"**: quantum comes from "quanta" (a fixed, definite amount) — nature, when measured, expresses itself **only in quanta**: up or down, nothing in between (discrete). The electron itself can still have spin pointing in any direction, but **once measured, that information is inaccessible — you only ever get one of two values, up or down**.
- **Connection to qubits**: this is an example of a **two-state system** — qubits are two-state systems too. A qubit lives in a very large Hilbert space, but **measuring it always yields exactly one of two values, 0 or 1** — you can never directly obtain a superposition (a little 0, a little 1) as a measurement outcome.
- **Limits of measurement — observables theory and Heisenberg uncertainty**: this apparatus can only measure the vertical component of the spin axis — the actual spin axis is a full 3D orientation, but you cannot freely measure the x, y, and z components in any order you like (unlike measuring height, width, and depth of furniture in any order). This is governed by **observables theory** — which dictates what can be measured, and that the order of measurement affects the outcome. There is also the **Heisenberg uncertainty principle**: measuring the z-direction precisely necessarily makes the x-direction measurement imprecise (the same kind of constraint as position-momentum uncertainty).
- Conclusion: nature is fundamentally **discrete** — this is the basis for the name "quantum mechanics." (A 10-minute break followed, then the next experiment.)

### The Double-Slit Experiment — Setup and the Classically Expected Pattern (p.47–49)

- Feynman (originator of the quantum computer idea) called the double-slit experiment "the heart of quantum mechanics" — because it shows electrons/photons propagating as a **wave** at some stage, then reverting to a **particle** at the moment of measurement (a preview of wave-particle duality).
- **Apparatus**: an electron gun (or a source firing photons one at a time) shoots particles one by one at a wall with two slits. Hitting the wall absorbs and destroys the particle; passing through a slit lets it continue to a detector screen behind, where it registers as a single dot.
- **Starting with a single slit**: even with just one slit open, an interesting pattern already appears — a bright central region with many hits, flanked by dead zones with no hits, and then faint hits again further out.
- **Tennis-ball analogy (classical expectation)**: imagine opening a window and randomly throwing paint-coated tennis balls at a building across the way. Classically, you'd expect a **smoothly decreasing single distribution** — many hits centered in the middle, tapering off to the sides — and you should never see "many hits, then a dead zone, then a few more hits further out." Yet the photon experiment **already deviates from this classical expectation with just a single slit**.
- **Opening the second slit — the truly counterintuitive part**: the interference pattern becomes more complex — a narrower center, and alternating zones with and without hits. Crucially: **a region that received many hits with only one slit open receives zero hits once the second slit is also opened.**
- **Why this is unexpected (classical argument)**: opening one window gives some probability of hitting a particular spot across the way. Opening a second window creates an additional path to that same spot, so the probability of hitting it should **only increase or, at worst, stay the same — it can never decrease, let alone drop to zero** (opening a window can't make balls that used to land there suddenly stop landing there). But the experiment shows exactly the opposite.

### The Failure of Classical Probability Theory — Kolmogorov's Additivity Axiom Violated (p.50–51)

- **Andrei Kolmogorov**, in his 1933 book *Foundations of the Theory of Probability*, formalized classical probability theory as requiring three things:
  1. The outcomes of an experiment are called **events** (e.g., "slit 1 is open and the ball hits a given region" is one event).
  2. Each event is assigned a **probability** — always a real number in $[0,1]$. A certain event has probability 1.
  3. The **additivity axiom**: the probability that either of two events occurs ("this event or that event") is the **sum** of their individual probabilities. (P(hit via slit 1) + P(hit via slit 2) = P(hit overall via either slit).)
- **The double-slit experiment clearly violates this additivity axiom**: if the probability of hitting a given region is high with only slit 1 open, then opening slit 2 as well should make that probability **higher, or at worst unchanged** (per additivity) — you can never "subtract" probability. Yet in reality that probability **drops to zero**. Nature (photons/electrons) does not obey this additivity axiom — fundamentally unlike the tennis balls thrown through the windows.

### The Birth of Quantum Mechanics — Early Physicists and Copenhagen (p.52)

- In the early 1900s, physicists kept finding results — from Stern-Gerlach, the double-slit experiment, and others — that classical theory could not explain. Early attempts at explanation were "hacky," but physicists soon arrived at a **sound model** — **quantum mechanics**.
- Early figures mentioned: **Max Planck** (one of the very first), **Niels Bohr**, **Heisenberg**, **Pauli**, **Schrödinger**.
- A photo from a **Copenhagen** conference was shown: Bohr was already a major figure leading his own research group, with Heisenberg as his assistant. Pauli, Gamow, and Landau also appear (though not everyone is in the photo — Schrödinger and Bohr himself, among others, were noted as missing from it).
- **Anecdote**: the photo depicts a trumpet, a cannon, and a drummer — a playful tradition where a universally accepted theory got a trumpet fanfare ("theory accepted"), a flawed theory got shot down with the cannon, and something important got a drum roll. Despite fierce debate, they kept a playful spirit.

### Modified Probability Theory — Introducing Probability Amplitudes (p.53–57)

To explain the additivity violation in the double-slit experiment, quantum physicists changed how probability itself is computed. (The professor previewed complex numbers, conjugates, etc. before formally covering them — repeatedly saying "we'll cover this in detail next week." This section records only what was explicitly previewed.)

- **Probability amplitude**: classical probability (a real number in [0,1]) is discarded and replaced by a **complex-number** amplitude $\alpha$ — real and imaginary parts, either sign, freely.
- **Born's rule (Max Born)**: to get a probability from an amplitude $\alpha$, take its **absolute value squared** (norm squared / mod-squared) $|\alpha|^2 = \mathrm{Re}(\alpha)^2+\mathrm{Im}(\alpha)^2$. The norm squared equals $\alpha \cdot \bar{\alpha}$ (the amplitude times its conjugate) — the conjugate $\bar\alpha$ flips the sign of the imaginary part. Conjugation distributes over addition: $\overline{\alpha_1+\alpha_2} = \bar\alpha_1+\bar\alpha_2$.
- **Combined amplitude for sequential events = product**: if a system goes from state A to B with amplitude $\alpha_1$, then from B to C with amplitude $\alpha_2$, the combined amplitude for A→C overall is the product $\alpha_1 \cdot \alpha_2$ — analogous to classical probability multiplication (e.g., winning a lottery with probability $p$ twice in a row has probability $p \times p$).
- **Combined amplitude for alternative events = sum**: if an electron can pass through slit 1 with amplitude $\alpha_1$, or slit 2 with amplitude $\alpha_2$, then the combined amplitude for "reaching a given point via slit 1 or slit 2" is the sum $\alpha_1+\alpha_2$. (This looks deceptively like Kolmogorov's additivity axiom, but the decisive difference is that $\alpha_1,\alpha_2$ are **complex numbers**.) Any system observable in multiple outcomes — a qubit, or a photon in the double-slit setup — needs one amplitude per possible observed event; both a qubit and the double-slit photon need **two amplitudes**.
- **Deriving the cross (interference) term — expanding via Born's rule**:
  - Probability $= |\alpha_1+\alpha_2|^2 = (\alpha_1+\alpha_2)\overline{(\alpha_1+\alpha_2)} = (\alpha_1+\alpha_2)(\bar\alpha_1+\bar\alpha_2)$
  - $= \alpha_1\bar\alpha_1 + \alpha_2\bar\alpha_2 + \alpha_1\bar\alpha_2 + \alpha_2\bar\alpha_1 = |\alpha_1|^2 + |\alpha_2|^2 + \underbrace{(\alpha_1\bar\alpha_2 + \alpha_2\bar\alpha_1)}_{\text{cross term}}$
  - The first two terms $|\alpha_1|^2, |\alpha_2|^2$ are simply the probabilities of "slit 1 open only" and "slit 2 open only" — straightforward so far.
  - **Evaluating the cross term**: introducing polar form $\alpha = |\alpha|e^{i\varphi}$ gives $\alpha_1\bar\alpha_2 = |\alpha_1||\alpha_2|e^{i(\varphi_1-\varphi_2)}$ and $\alpha_2\bar\alpha_1 = |\alpha_1||\alpha_2|e^{i(\varphi_2-\varphi_1)}$; being mutual conjugates, their sum is twice the real part:
$$
\alpha_1\bar\alpha_2+\alpha_2\bar\alpha_1 = 2|\alpha_1||\alpha_2|\cos(\varphi_2-\varphi_1)
$$
  - **Final formula**: $P = |\alpha_1|^2+|\alpha_2|^2+2|\alpha_1||\alpha_2|\cos(\varphi_2-\varphi_1)$.
  - **Kolmogorov did not know about this cross (interference) term** — his additivity axiom only covers the first two terms. This cosine term is the new piece, and **since cosine can be negative**, the combined probability can end up **smaller** than either individual probability — even dropping exactly to zero, as observed. This is the mathematical basis for "opening a second slit makes hits disappear."
- **The professor's actual worked numerical example**: $\alpha_1 = \tfrac12$, $\alpha_2 = -\tfrac12$ (both taken as real numbers).
  - Probability with only one slit open, for each: $|\alpha_1|^2 = |\alpha_2|^2 = \left(\tfrac12\right)^2 = \tfrac14$ → **25% each**.
  - With both slits open: $\alpha_1\bar\alpha_2 = \tfrac12\times\left(-\tfrac12\right) = -\tfrac14$, $\alpha_2\bar\alpha_1 = -\tfrac12\times\tfrac12 = -\tfrac14$ (the conjugate of a real number is itself).
  - Sum: $\tfrac14+\tfrac14-\tfrac14-\tfrac14 = 0$.
  - So the probability of hitting that spot is 25% with one slit, but **exactly 0** once the second slit is opened — precisely reproducing the observed "dark fringe."
- **Student question 1 (left unresolved)**: if the cosine in the cross term can be negative, couldn't the total probability $P$ itself go negative? Instructor's response: "I don't think so," but admitted he **could not explain right now why it doesn't go negative**, and awarded a participation point. **This question was explicitly left unresolved — no answer is invented here.**
- **Student question 2 (left unresolved)**: in the "classical case," shouldn't this cross term (the cosine term) become zero for consistency — and if so, what condition must $\varphi_1,\varphi_2$ satisfy? Instructor: "good point, I need to think about this more," deferring rather than answering, and awarded a participation point. **This question was also explicitly left unresolved.**
- Physical interpretation: the interference term contains both $\varphi_1$ and $\varphi_2$ — i.e., information about "the photon went through the left slit" and "the photon went through the right slit" **simultaneously**. This is the basis for interpreting it as "the photon goes through both slits at once," the same kind of phenomenon as a qubit being in **superposition** (a little 0, a little 1) rather than strictly 0 or 1.

### Toward Wave-Particle Duality — Physical Interpretation of the Double Slit, and Running Out of Time (p.58–61)

- The session ran out of time here (the instructor explicitly said he "probably won't finish today").
- **Intuitive picture**: as it heads toward the slits, a photon propagates **as a wave, not a particle** — not a single tennis ball going through one specific slit, but something spreading out like a water wave. Just as a water wave passes through **both** holes if there are two, the photon passes through both slits at once, as a wave.
- **Interference**: the two waves emerging from the two slits meet and reinforce or cancel each other — waves pushing up together in phase double in amplitude (**constructive interference**); waves moving in opposite directions cancel out (**destructive interference**).
- **Measurement = wave collapse = "Schrödinger's box"**: the moment the interference-patterned wave hits the screen is the measurement — at that point the wave collapses back into behaving as a single particle, landing at one specific point on the screen according to those probabilities (interference pattern); it never hits the whole screen at once.
- **Final takeaway**: at points of destructive interference, the probability is zero and no electrons land there at all — this is exactly the mechanism behind "a spot that received many hits with one slit open receives none once the second slit is opened." Classical probability theory failed here because the particle exhibits this **wave pattern** — this is **wave-particle duality**.

### Carried Over to Next Session (facts only, no speculation)

- **Slides 62 onward (photon polarization, bits vs. qubits) were not reached this session** — carried over to next time.
- The instructor gave **no formal answer this session** to either student question about probability amplitudes (whether the cross term could make $P$ negative; why $\varphi_1=\varphi_2$ would be required in the classical limit) — both remain explicitly unresolved.
- What exactly the "additional element" is that makes $U_f$ (the AND gate converted to a unitary operator) reversible was also not explained this session.
- The formal introduction of complex numbers, conjugates, and polar form, as well as how the entries of $H\otimes H$ are actually derived, were all previewed as "next week" material — not yet covered.
