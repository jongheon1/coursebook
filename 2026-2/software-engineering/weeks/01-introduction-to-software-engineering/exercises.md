# Week 1 — Exercises

Exam-style problems. Total: 100 points. Answers are in collapsible sections — attempt every part before revealing.

---

## Q1. Definitions (6 pts)

(a) Define *software engineering* according to Sommerville, and identify the two phrases in the definition that distinguish it from "programming". (4 pts)
(b) According to Sommerville, why is "software" not the same thing as "programs"? Name two things software includes beyond the program code. (2 pts)

<details>
<summary>Model answer</summary>

(a) "Software engineering is an engineering discipline that is concerned with **all aspects of software production** from the early stages of system specification to maintaining the system after it has gone into use."
- **"All aspects of software production"**: not only coding but specification, design, validation, evolution, plus project management and tool/method development.
- **"Engineering discipline"**: engineers make things work by selectively applying theories, methods, and tools **within organizational and financial constraints** — i.e., trade-off-driven work, not the pursuit of a single perfect solution.

(b) Software products consist of the programs **plus everything needed to make them usable and maintainable**: all associated **documentation** and **configuration data** required to install, configure, and operate the system correctly (also libraries, support websites, etc.). A working binary nobody can deploy, configure, or modify is a program, not a software product.
</details>

---

## Q2. Generic products vs custom systems (8 pts)

(a) State the *defining* criterion that separates generic software products from customized (bespoke) systems, and give one example of each. (4 pts)
(b) A company buys a commercial ERP system and spends 18 months configuring and extending it to fit its business processes. Which category does this fall into, and what makes requirements engineering harder in this case? (4 pts)

<details>
<summary>Model answer</summary>

(a) The criterion is **ownership/control of the specification**.
- **Generic products**: the *developer* owns the specification and decides what to build and when to change it. Sold to an open market. Example: a word processor, a SaaS analytics product.
- **Custom (bespoke) systems**: the *customer* owns and controls the specification and change decisions. Example: an air traffic control system, a company-specific admin system.

(b) It is a **hybrid**: the base product is generic (vendor owns its spec) but the configured system is customer-specific. Requirements engineering is harder because specification authority is **split** — the customer controls requirements for the extensions/configuration, but the vendor controls the base product's behavior and evolution, so requirements must be negotiated against what the product can be made to do, and vendor upgrades can invalidate customer-side assumptions.
</details>

---

## Q3. Brooks's 3×3 frame (10 pts)

Brooks (*The Mythical Man-Month*, ch1) claims a "programming systems product" costs roughly nine times as much as the underlying "program".

(a) Name the two independent axes of this 3× / 3× decomposition and describe what each axis adds. (4 pts)
(b) Classify each of the following efforts as belonging to the *product* axis, the *system* axis, or *neither* (i.e., part of writing the base program): (i) writing tests for malformed inputs a stranger might type; (ii) making the module respect a fixed memory budget agreed with other teams; (iii) getting the algorithm to work on the author's own machine; (iv) writing user documentation; (v) integration testing against other components' interfaces. (5 pts)
(c) What does this frame imply about the share of "coding" in total software cost? (1 pt)

<details>
<summary>Model answer</summary>

(a)
- **Program → Programming Product (×3)**: generalization, thorough **testing** (including boundary/hostile inputs), **documentation**, and maintainability — everything needed so that *anyone* can use, repair, and extend it without the author.
- **Program → Programming System (×3)**: making the code a component in a larger whole — conforming to **precisely defined interfaces**, staying within prescribed **resource budgets** (memory, time), and being tested **in combination** with other components.

(b) (i) product; (ii) system; (iii) neither — base program; (iv) product; (v) system.

(c) Coding the working program is roughly **1/9 of the cost** of an industrial-strength systems product — programming is a minority share of software engineering effort (consistent with Sommerville's figures: ~60% development / ~40% testing, and evolution exceeding development for custom systems).
</details>

---

## Q4. Essential vs accidental complexity (10 pts)

(a) Define *essential* and *accidental* complexity in Brooks's sense (one sentence each). (2 pts)
(b) Classify each as primarily essential or accidental: (i) slow build times; (ii) the intertwined business rules of an insurance domain; (iii) manual memory management in C; (iv) the requirement to interoperate with a 30-year-old file format mandated by regulators; (v) the impossibility of drawing the whole system as one diagram; (vi) flaky CI infrastructure. (3 pts)
(c) Reconstruct Brooks's core argument for why no single development can deliver an order-of-magnitude improvement. Your answer must use the 9/10 fraction argument. (4 pts)
(d) Name the four properties Brooks assigns to the essence of software. (1 pt)

<details>
<summary>Model answer</summary>

(a)
- **Essential complexity**: the difficulty inherent in the software's conceptual structure itself — specifying, designing, and verifying the interlocking concepts (data sets, relationships, algorithms, invocations) — which no change of representation can remove.
- **Accidental complexity**: difficulty that arises from the technology used to *express* the solution (languages, tooling, builds, environments) and can in principle be engineered away.

(b) (i) accidental; (ii) essential (and partly *conformity*); (iii) accidental; (iv) essential — *conformity* to arbitrary human institutions; (v) essential — *invisibility*; (vi) accidental.

(c) Past order-of-magnitude gains (high-level languages, time-sharing, unified environments) all removed **accidental** difficulties. Let the accidental share of total effort be $a$. Even if a new technology removed *all* remaining accidental effort, the speedup would be $1/(1-a)$; for this to reach 10×, we would need $a > 9/10$. Brooks argues the accidental share is already well below 9/10, so eliminating it entirely cannot yield 10×. What remains is essential difficulty, and there is no known technique that attacks the essence exponentially — hence no silver bullet.

(d) **Complexity, conformity, changeability, invisibility.**
</details>

---

## Q5. Team scaling (8 pts)

A project team of 10 engineers is 2 months behind schedule. Management proposes adding 5 more engineers.

(a) Compute the number of pairwise communication paths before and after, and the ratio of increase. (3 pts)
(b) Give two further reasons (beyond communication paths) why the addition can make the project *later*, per Brooks. (3 pts)
(c) State Brooks's law verbatim or near-verbatim. (2 pts)

<details>
<summary>Model answer</summary>

(a) Paths $= n(n-1)/2$. Before: $10 \cdot 9/2 = \mathbf{45}$. After: $15 \cdot 14/2 = \mathbf{105}$. Ratio $105/45 \approx \mathbf{2.3\times}$ — while raw capacity rises only 1.5×.

(b)
- **Ramp-up cost**: new members must be trained by productive members, so existing engineers' output *drops* during onboarding.
- **Task divisibility limits**: parts of the work are sequential/indivisible (cf. Amdahl's serial fraction), so extra people cannot be applied to them; repartitioning work and re-planning also consumes time.

(c) "**Adding manpower to a late software project makes it later.**"
</details>

---

## Q6. Case analysis: Ariane 5 Flight 501 (10 pts)

(a) Describe the proximate technical cause of the failure, naming the variable, the conversion involved, and why the value went out of range on Ariane 5 but not Ariane 4. (4 pts)
(b) Why did the backup SRI not save the mission? Name the general phenomenon. (2 pts)
(c) The unprotected conversion was *not* an oversight. Explain the deliberate engineering decision behind leaving it unprotected, how it was (not) documented, and why that decision became invalid. (2 pts)
(d) Name the validation activity that the inquiry board identified as missing and that would have caught the fault. (2 pts)

<details>
<summary>Model answer</summary>

(a) In the SRI (inertial reference system), the alignment function computed the **horizontal bias (BH)** variable, proportional to horizontal velocity. A conversion of BH from **64-bit floating point to 16-bit signed integer** was unprotected; Ariane 5's early trajectory has **much higher horizontal velocity** than Ariane 4's, so at H0+36.7 s (≈30 s after lift-off) BH exceeded 32,767, causing an Ada **Operand Error**. Per the SRI's exception policy the processor shut down and emitted a diagnostic bit pattern that the on-board computer interpreted as flight data, commanding full nozzle deflection and structural breakup. The function itself served no purpose after liftoff on Ariane 5 — it was an Ariane 4 requirement (fast realignment after a countdown hold) left running ~50 s into flight mode.

(b) Both SRIs ran **identical software** on identical inputs, so the backup failed the same way — in fact 72 ms *before* the active unit — leaving the OBC nothing to switch to. This is a **common-mode failure**: redundancy protects against independent random hardware faults, not design faults.

(c) For **Ariane 4**, the reasoning was that the unprotected variables were either physically limited or had a large margin of safety — the inquiry board found *no evidence that any trajectory data were used* to analyse them — and a performance requirement (keep processor load below ~80%) motivated protecting only 4 of 7 at-risk variables. The decision was deliberate and *jointly agreed by project partners at several contractual levels*, but its justification was documented neither in the source code nor in the specification, so it was "essentially obscured, though not deliberately, from any external review." It was valid *only under Ariane 4 environmental assumptions*; those assumptions were not stated in the requirements nor re-analyzed for Ariane 5's trajectory — reuse without revalidation.

(d) **System-level closed-loop simulation/testing of the SRI with actual Ariane 5 trajectory data** — not part of the test plan; the board stated such a test would have exposed the failure.
</details>

---

## Q7. Case analysis: Therac-25 (12 pts)

(a) Explain the race-condition failure mechanism: what the operator did, what the software failed to detect, and what physical configuration resulted. (4 pts)
(b) The same software bugs existed in the Therac-20 without harming anyone. Explain why, and state the design principle this illustrates. (3 pts)
(c) Leveson & Turner argue that "fixing the bug" would not have made the system safe. Give three system-level (non-code) factors that contributed to the accidents. (3 pts)
(d) The machine frequently displayed cryptic malfunction codes that operators could dismiss with one keystroke. Explain how this contributed to the accidents. (2 pts)

<details>
<summary>Model answer</summary>

(a) After parameter entry, setting the bending magnets took ~8 seconds. If the operator **edited the mode/energy on the terminal within that window** (e.g., correcting an X→E typo), the concurrent tasks — communicating through shared variables with a completion flag checked only once — **missed the edit**. The machine could then deliver the **X-ray-mode high-current electron beam (~100× electron-mode current) with the tungsten target retracted**, i.e., a massive overdose. The bug only manifests with fast operators, which is why it appeared after operators became proficient and why AECL could not reproduce it.

(b) The Therac-20 retained **hardware interlocks** that physically prevented the unsafe beam/target configuration; when the software erred, a fuse blew and nothing more. Principle: **defense in depth** — safety must not depend on a single (software) layer; equivalently, safety is a **system property**, not a software property.

(c) Any three of: removal of hardware interlocks (single point of protection); **risk analysis that excluded software** faults (fault trees covered hardware only); reuse of software from earlier machines assumed safe ("proven in use"); poor human–machine interface and cryptic error messages; **inadequate incident investigation** by the manufacturer (claimed overdose impossible, no root-cause analysis); weak reporting/regulatory follow-up allowing recurrence.

(d) Frequent, low-consequence malfunction messages **habituated** operators: alarms carried no diagnostic meaning (e.g., "MALFUNCTION 54") and proceeding with "P" was routine, so genuine hazard states were treated as noise. An alarm channel with a high false-alarm rate loses its ability to convey danger.
</details>

---

## Q8. Case analysis: Knight Capital (12 pts)

(a) Put these events into the correct causal order and state, for each, why it was necessary for the disaster: (i) manual deployment misses one of eight servers; (ii) an obsolete function's fill-tracking is silently broken by a refactoring; (iii) a message flag formerly used for Power Peg is repurposed for the new RLP feature; (iv) Power Peg code is retired but left deployed. (5 pts)
(b) During the incident, engineers uninstalled the new code from the seven correctly deployed servers. Explain precisely why this made things worse. (3 pts)
(c) Name three process controls, each of which alone would plausibly have prevented or sharply bounded the loss. (3 pts)
(d) What was the SEC's charge focused on — the bug, or something else? (1 pt)

<details>
<summary>Model answer</summary>

(a) Order: **(iv) → (ii) → (iii) → (i)**.
- (iv) Power Peg retired (2003) but its code left in SMARS: creates the latent hazard — dead code that can still execute.
- (ii) 2005 refactoring moves the cumulative-fill counter, silently breaking Power Peg's stop condition: turns the dead code from "obsolete" into "unbounded order generator" — unnoticed because the code was presumed dead.
- (iii) RLP feature reuses the old activation flag: creates a live execution path into the dead code; the flag's meaning now depends on which code version a server runs.
- (i) Manual deploy misses 1 of 8 servers: creates exactly the mixed-version state in which the same flag means "RLP" on seven servers and "activate Power Peg" on one. Orders routed to that server sent child orders continuously without tracking fills — 212 parent orders became millions of orders, >4M executions, ~397M shares, ≈$460M loss in ~45 minutes.

(b) The seven servers' *previous* code also interpreted the flag as Power Peg activation. Rolling back removed the only correct interpretation of the flag, so **all eight servers** now routed flagged orders into Power Peg — multiplying the runaway rate instead of stopping it. A rollback is a deployment; unverified, it carries the same risk as the original deploy.

(c) Any three of: **automated deployment with post-deploy verification** (version/checksum consistency across all servers, refuse to start on mismatch); **deleting dead code** (or making unknown/retired flags hard-reject); **not reusing flag semantics** (new field for new meaning); **automated risk kill switch** (position/loss limits that halt order flow — the Market Access Rule requirement); a **second-technician review** of the deployment; treating the 97 pre-open "Power Peg disabled" e-mails as actionable real-time alerts.

(d) Not the bug: the **absence of adequate risk management controls and supervisory procedures** around market access (Rule 15c3-5) — i.e., the process and controls failure ($12M penalty).
</details>

---

## Q9. Essential attributes of good software (10 pts)

(a) Name and define Sommerville's four essential attributes of good software. (4 pts)
(b) For each scenario, identify the primary attribute at issue: (i) a nurse cannot tell what "MALFUNCTION 54" means; (ii) a batch job holds 60 GB of RAM for a 2 GB dataset; (iii) a one-line tax-rule change requires modifying 14 modules; (iv) a hospital system leaks patient records to an attacker. (4 pts)
(c) Using Ariane 5, give a concrete example of two attributes coming into conflict. (2 pts)

<details>
<summary>Model answer</summary>

(a)
- **Maintainability**: software should be written so it can **evolve to meet changing customer needs** — change is inevitable in a changing business environment.
- **Dependability & security**: reliability + safety + security — failure should not cause physical or economic damage, and malicious users should not be able to access or damage the system.
- **Efficiency**: no wasteful use of system resources — includes responsiveness, processing time, memory utilization.
- **Acceptability**: understandable, usable, and compatible with other systems for the intended type of user.

(b) (i) acceptability (usability failing into safety); (ii) efficiency; (iii) maintainability; (iv) dependability & security.

(c) In the SRI, a performance requirement (processor load ≤ ~80% — **efficiency**) was part of the justification for leaving three conversions, including BH, unprotected — trading away runtime checking that supported **dependability**. The trade-off was reasonable under Ariane 4 assumptions and catastrophic when the environment changed.
</details>

---

## Q10. The four fundamental activities (6 pts)

(a) Name the four fundamental activities common to all software processes and give a one-sentence definition of each. (4 pts)
(b) Assign each course topic to the activity it primarily serves: requirements elicitation (W2); design patterns (W10–12); coverage-based testing (W13–14); DevOps/CI-CD (W3). (2 pts)

<details>
<summary>Model answer</summary>

(a)
- **Software specification**: customers and engineers define the software to be produced and the constraints on its operation.
- **Software development**: the software is designed and programmed.
- **Software validation**: the software is checked to ensure it is what the customer requires.
- **Software evolution**: the software is modified to reflect changing customer and market requirements.

(b) Requirements elicitation → specification. Design patterns → development. Coverage-based testing → validation. DevOps/CI-CD → evolution (continuous delivery of change; also spans development).
</details>

---

## Q11. Professional ethics (8 pts)

Your manager instructs you to ship a firmware update for an insulin pump on Friday to meet a contractual deadline. You know of an intermittent dosing miscalculation that QA could not reliably reproduce; your manager says "it passed the release tests, and the contract penalty is severe."

(a) Which two principles of the ACM/IEEE Software Engineering Code of Ethics are in direct tension here, and how does the Code resolve that tension? (4 pts)
(b) Describe a defensible course of action, referencing at least two specific principles by name. (3 pts)
(c) Name the two organizations that jointly published the Code. (1 pt)

<details>
<summary>Model answer</summary>

(a) **Principle 2 (CLIENT AND EMPLOYER)** — act in the employer's best interest (meet the deadline, avoid penalties) — versus **Principle 1 (PUBLIC)** — act consistently with the public interest, with the public's health, safety, and welfare **primary**. The Code resolves it explicitly: obligations to employer and clients hold only *insofar as they are consistent with the public interest*; where they conflict, the public interest governs. "Passing release tests" does not discharge the obligation — a known safety-relevant defect in a medical device implicates public safety directly (cf. Therac-25: intermittent, hard-to-reproduce faults are exactly the dangerous class).

(b) Defensible course: document the defect, its safety implications, and the reproduction evidence, and formally raise the objection (Principle 1 — PUBLIC; Principle 3 — PRODUCT: products must meet the highest professional standards, and known defects must be disclosed and addressed); propose alternatives that serve the employer within safety limits (delay, restricted release, mitigation/monitoring) (Principle 2); if overruled on a genuine safety risk, escalate through management (Principle 5 — MANAGEMENT) and, if internal escalation fails, consider disclosure to the appropriate regulator (Principles 1 and 6 — PROFESSION). Judgment must remain independent of schedule pressure (Principle 4 — JUDGMENT).

(c) The **ACM** and the **IEEE Computer Society**.
</details>
