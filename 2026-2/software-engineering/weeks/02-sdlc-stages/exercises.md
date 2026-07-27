# Week 2 — Exercises: SDLC Stages

Exam-style problems. Total: 110 points (100 + 10 bonus). Answers are hidden in `<details>` blocks — attempt each problem before revealing.

---

## Q1. Classifying requirements (8 pts)

Classify each of the following statements for a shared e-scooter platform as a **functional requirement (FR)** or a **non-functional requirement (NFR)**. For NFRs, also state whether it is a *product*, *organizational*, or *external* requirement. One statement is deliberately ambiguous — identify it and explain why the FR/NFR boundary blurs there.

a) "The system shall generate, each morning, a list of scooters whose battery is below 20%."
b) "The rental start API shall respond within 200 ms at the 99th percentile under a load of 500 requests/second."
c) "The system shall be developed following the company's secure coding standard SEC-STD-2."
d) "The system shall store ride location data in accordance with the national location-privacy act."
e) "Only authenticated operators shall be able to force-end a ride."

<details>
<summary>Model answer</summary>

- a) **FR** — a service the system provides (a specific reaction/output).
- b) **NFR, product** — a performance constraint on a service, quantified and verifiable.
- c) **NFR, organizational** — derived from the developing organization's policies/process standards.
- d) **NFR, external** — derived from legislation outside the system and its development process.
- e) The **ambiguous** one. Stated as an access constraint it reads as an NFR (security), but when elaborated it generates clearly functional requirements: an authentication facility, an operator role model, a force-end operation with permission checks. This illustrates Sommerville's point that requirements are not independent — one requirement generates or constrains others, so the FR/NFR distinction is not clear-cut. (Full credit requires naming the generated FRs, not just saying "it's both.")
</details>

## Q2. Making an NFR verifiable (10 pts)

A product manager writes: *"The operator dashboard must be easy to learn and must recover quickly from failures."*

(a) Explain, in one or two sentences, why this statement cannot be accepted as a requirement. (3 pts)
(b) Rewrite it as **two** verifiable non-functional requirements, naming for each the metric used (per Sommerville's metric table) and how it would be verified. (5 pts)
(c) Give one reason why a customer might rationally *refuse* to pay for this quantification. (2 pts)

<details>
<summary>Model answer</summary>

(a) It states **goals**, not requirements: "easy" and "quickly" leave scope for interpretation, so no test can objectively decide whether the delivered system satisfies them — they are unverifiable and become a source of dispute after delivery.

(b) Examples:
- *Learnability*: "A new operator shall be able to perform all dashboard functions after at most 2 hours of training; after training, experienced operators shall make no more than 2 operating errors per hour of use." Metric: **training time / error rate** (ease-of-use metrics). Verified by an instrumented usability test with new operators.
- *Recoverability*: "After a dashboard process failure, the service shall be restored within 5 minutes; monthly availability shall be at least 99.9%." Metric: **time to restart after failure / availability** ($A = MTTF/(MTTF+MTTR)$). Verified from operational monitoring data and fault-injection tests.

(c) Objective verification has real cost (instrumentation, usability sessions, monitoring infrastructure), and for some properties customers cannot relate the numbers to their everyday experience — they may judge the verification cost unjustified (Sommerville §4.1.2).
</details>

## Q3. Why elicitation is hard (8 pts)

(a) List four distinct reasons why requirements elicitation is difficult. (4 pts)
(b) An analyst interviews every warehouse worker for two weeks and still ships a system that workers bypass with paper notes. Using the concepts of *tacit knowledge* and *ethnography*, explain what went wrong and what should have been done. (4 pts)

<details>
<summary>Model answer</summary>

(a) Any four of: (1) stakeholders don't know what they want except in general terms and may make infeasible demands; (2) stakeholders express requirements in their own terms with **implicit (tacit) domain knowledge** the engineer lacks; (3) different stakeholders have diverse, conflicting requirements that must be reconciled; (4) political/organizational factors influence stated requirements; (5) the business environment changes during analysis itself, changing priorities and stakeholders.

(b) Interviews cannot surface knowledge that is *second nature* to workers — practices so obvious to them that they are never mentioned, and cooperative practices (covering for each other, awareness of others' work) that individuals don't recognize as part of "their" work. The paper notes are evidence of actual work practice diverging from the formal process the interviews captured. **Ethnography** — observing the actual work in its social setting — would have revealed requirements derived from how people really work rather than how the process definition says they work, and those requirements should have driven the design (possibly combined with prototyping to focus further observation).
</details>

## Q4. User story vs SRS (8 pts)

(a) Give the canonical user story template and state what "a story is a placeholder for a conversation" means operationally. (3 pts)
(b) State two properties an SRS-style requirement must have that a user story deliberately does *not* have. (2 pts)
(c) Your team builds firmware for an insulin pump under regulatory certification. Argue in 2–3 sentences which documentation form must anchor the project, and what role (if any) stories can still play. (3 pts)

<details>
<summary>Model answer</summary>

(a) `As a <role>, I want <capability>, so that <benefit>`. Operationally: the card intentionally omits detail; the detail is negotiated in a conversation between developers and customer just before implementation, and completion is judged against acceptance criteria agreed in that conversation — the story is *not* a contract.

(b) E.g., **unambiguity** and **verifiability** as written (each requirement uniquely identified, singular, testable without further negotiation); also **traceability** (stable IDs linking to design and tests). Stories are instead *negotiable* and deliberately incomplete.

(c) A certified safety-critical system needs an SRS-style specification: the certifying authority audits against a definitive, verifiable, traceable statement of requirements, and the contract needs a non-negotiable baseline. Stories can still organize the team's internal iteration planning (slicing work, scheduling conversations), but each implemented change must be reflected back into the controlled specification and its traceability records.
</details>

## Q5. Coupling and cohesion classification (12 pts)

For each fragment, name the **worst** coupling or cohesion category it exhibits and justify in one sentence.

a) ```python
   def handle(record, mode):
       if mode == 1: validate(record)
       elif mode == 2: archive(record)
       elif mode == 3: export_csv(record)
   ```
b) Two modules communicate exclusively by reading and writing fields of a shared module-level dictionary `GLOBAL_STATE`.
c) `send_sms(user)` receives the full `User` object (23 fields) but only reads `user.phone`.
d) A module `startup.py` containing `open_log_file()`, `warm_cache()`, `load_feature_flags()` — grouped because they all run at boot.
e) `parse_line() → build_index() → render_page()`, where each function's output is the next one's input, packaged as one module.
f) Module A calls a private helper `B._recompute_internal_table()` of module B to "fix" B's state after mutating B's data directly.

<details>
<summary>Model answer</summary>

- a) **Logical cohesion** (and it induces **control coupling** in callers): elements are grouped as "same category of operation" selected by a flag; the caller must know B's internal dispatch.
- b) **Common coupling**: modules share global mutable data; any change to the dictionary's shape or meaning potentially affects every module that touches it.
- c) **Stamp coupling**: a composite structure is passed where only one elementary item is needed; the function is exposed to irrelevant changes in `User`.
- d) **Temporal cohesion**: elements are related only by *when* they execute (boot time), not by a single task or shared data.
- e) **Sequential cohesion**: output-to-input chaining — second-best category, acceptable; (full marks for naming it and noting it is high, not low, cohesion).
- f) **Content coupling**: A depends on and manipulates B's internal representation and private operations — the worst category; B's internals can no longer change safely.
</details>

## Q6. Parnas and information hiding (12 pts)

(a) State Parnas's proposed criterion for decomposing a system into modules, and the conventional criterion he argued against. (4 pts)
(b) In the KWIC system, the decision "circular shifts are stored as index pairs into the original lines rather than as copied strings" changes. For the flowchart decomposition and for the information-hiding decomposition, state which modules must change and why. (4 pts)
(c) Parnas claimed three benefits of the second decomposition. Name them and explain, in one sentence, the condition under which the benefits fail to materialize. (4 pts)

<details>
<summary>Model answer</summary>

(a) Conventional criterion: make each **processing step of the flowchart** a module. Parnas's criterion: start from a list of **difficult design decisions or decisions likely to change**, and make each module hide one such decision from all the others ("its secret"), exposing only an interface designed to reveal as little as possible.

(b) Flowchart decomposition: the shift representation lives in the shared data structure known to **Circular Shift, Alphabetizer, and Output** (every module that reads shifts) — all must change. Information-hiding decomposition: only the **Circular Shifter** module changes, because other modules access shifts exclusively through its interface functions and never see the representation.

(c) (1) *Managerial* — modules can be developed independently once interfaces are agreed; (2) *product flexibility* — a likely change is confined to one module; (3) *comprehensibility* — a module can be understood without knowing others' internals. The benefits depend on **correctly predicting which decisions will change**: if a decision that was exposed in interfaces changes, or the hidden ones never do, the decomposition pays its costs without the payoff.
</details>

## Q7. Verification vs validation (8 pts)

(a) Define verification and validation using Boehm's two questions. (2 pts)
(b) Give a concrete scenario in which a system passes verification completely yet fails validation, and name which requirements-engineering failure typically causes this. (3 pts)
(c) Inspections and testing are complementary. Give one class of defect that only inspections can address and one that only testing can address, with reasons. (3 pts)

<details>
<summary>Model answer</summary>

(a) Verification: "are we building the product **right**?" — conformance to the stated functional and non-functional requirements. Validation: "are we building the **right** product?" — meeting the customer's actual expectations and needs, beyond the specification.

(b) E.g., a clinic scheduling system implements every requirement in the SRS, but nurses never use it because it assumes the formal appointment process while actual work relies on informal cross-clinic lookups — the spec itself was wrong. Root cause: elicitation failure (tacit knowledge / actual-vs-formal work practice not captured), so the specification did not reflect real needs.

(c) Inspections: defects in **non-executable artifacts** (requirements documents, designs, incomplete code) — nothing needs to run, and reviewers find many defects in one pass without one failure masking another. Testing: defects in **non-functional behavior and unexpected interactions** (performance under load, emergent integration behavior) — these only exist when the real system executes, so no static reading can observe them.
</details>

## Q8. V-model (8 pts)

(a) Draw (or describe precisely) the V-model, pairing each left-side artifact with its right-side test level. (4 pts)
(b) Which pairing embodies *validation* rather than *verification*, and why? (2 pts)
(c) State the structural weakness of the V-model and how incremental processes answer it. (2 pts)

<details>
<summary>Model answer</summary>

(a) Left (top→bottom): user requirements → system requirements → architectural design → detailed design, with **coding at the vertex** of the V (unpaired). Right (bottom→top): unit test (basis: detailed design, together with the code itself) → integration test (basis: architectural design and interface definitions) → system test (basis: system requirements) → acceptance test (basis: user requirements/needs). Each left-side artifact is the *test basis* for the test level directly opposite it, and tests can be designed as soon as the artifact exists.

(b) User requirements ↔ **acceptance test**: it checks the system against the users' actual needs and expectations (right product), whereas the lower pairs check conformance of one artifact to another (product right).

(c) Validation sits at the *end* of the chain, so the most expensive failure — building the wrong product — is discovered last. Incremental processes shrink the V and repeat it every iteration, so acceptance-level feedback arrives after each small slice instead of once at the end.
</details>

## Q9. Release strategy design (12 pts)

Your service runs 20 identical stateless instances behind a load balancer, with a single shared PostgreSQL database. The new release changes an API response field and renames a database column.

(a) For rolling, blue-green, and canary deployment, state the key operational property each provides and its main cost or precondition. (6 pts)
(b) Explain why the *column rename* is dangerous under **all three** strategies, and describe the expand/contract (parallel change) sequence that makes it safe. (4 pts)
(c) A defect makes 0.5% of requests fail only in the new version. With total traffic 12,000 req/min and a canary at 2% of traffic, how many canary requests fail per minute, and what is the worst-case fraction of all traffic affected while the canary runs? (2 pts)

<details>
<summary>Model answer</summary>

(a)
- **Rolling**: gradual instance replacement; near-zero extra infrastructure; requires old and new versions to serve concurrently, hence N-1 compatibility of API/schema; rollback is a slow reverse roll.
- **Blue-green**: two identical environments and a router switch; near-instant cutover and rollback; costs double infrastructure and requires DB schema compatible with both versions (the DB is not duplicated).
- **Canary**: exposes a small traffic fraction to the new version and compares live metrics before widening; bounds worst-case blast radius; requires a metrics pipeline plus automated comparison/rollback, and the same dual-version compatibility.

(b) In every strategy there is a period when **both versions run against the same database** (rolling/canary: mixed fleet; blue-green: green is validated, and instant rollback re-activates blue). A renamed column breaks whichever version doesn't expect it. Expand/contract: (1) *expand* — add the new column, dual-write (or trigger/backfill) so both names stay correct; (2) migrate readers to the new column across releases; (3) *contract* — drop the old column only after no deployed version references it. Each step is individually backward-compatible.

(c) Canary traffic: $0.02 \times 12{,}000 = 240$ req/min; failures: $240 \times 0.005 = 1.2$ req/min. Worst case while the canary runs, only canary traffic can be affected: $2\% \times 0.5\% = 0.01\%$ of all requests — the canary fraction caps the blast radius.
</details>

## Q10. Maintenance economics (8 pts)

(a) Name the four ISO/IEC 14764 maintenance categories and give Sommerville's alternative names for the first three. (4 pts)
(b) Quote the approximate empirical effort distribution among fault repair / environmental adaptation / functionality addition, and state the design implication of that distribution. (2 pts)
(c) Give two reasons why adding a feature during maintenance costs more than adding the same feature during initial development. (2 pts)

<details>
<summary>Model answer</summary>

(a) **Corrective** (Sommerville: fault repair), **adaptive** (environmental adaptation), **perfective** (functionality addition and modification), **preventive** (restructuring/refactoring to reduce future faults and change cost — Sommerville leaves it out of his three-way effort distribution, but in ch9 he does describe refactoring as "preventative maintenance" that reduces the problems of future change; he also notes the corrective/adaptive/perfective terms are used inconsistently in the literature).

(b) Roughly **24% fault repair, 19% environmental adaptation, 58% functionality addition/modification** (Sommerville Fig 9.12, after Davidsen & Krogstie 2010; stable across ~30 years of studies). Implication: maintenance is dominated by *evolution*, so the economically decisive quality is changeability (low coupling, information hiding), not just correctness.

(c) Any two of: (1) the maintaining team must first *understand* an unfamiliar program and the rationale of its design decisions; (2) development and maintenance are often contractually separated, so developers have no incentive to invest in maintainability; (3) maintenance work is unpopular and assigned lower-skilled/less experienced staff.
</details>

## Q11. Lehman's laws applied (8 pts)

A 12-year-old E-type billing system gets a new VP who announces: "We will freeze all feature work for two years — only security patches — and the system will stay exactly as useful as today. Then we'll double the team and evolve it twice as fast."

Using at least **three** of Lehman's laws (name them), critique both claims. Also state why the laws would *not* apply if the "system" were a pure mathematical library with a fixed formal specification.

<details>
<summary>Model answer</summary>

- **Continuing change**: an E-type system that is not adapted to its changing environment becomes progressively *less* useful — freezing features means declining usefulness, not preserved usefulness. (**Declining quality** makes the same point for perceived quality.)
- **Increasing complexity**: two years of patch-only change without complexity-reducing work will degrade structure, making the later "fast evolution" phase start from a worse baseline.
- **Conservation of organizational stability** (invariant work rate) and **conservation of familiarity**: global evolution activity is roughly invariant with respect to resources, and per-release change is bounded by what the organization can absorb — doubling headcount does not double evolution speed (communication/assimilation costs dominate).
- Non-application: a library fully defined by a fixed formal specification is an **S-type** program; its correctness is judged against the spec, not against a changing world, so the feedback loop (installation changes environment → environment generates new requirements) that drives the laws is absent.
</details>

## Q12. Technical debt — original meaning (8 pts)

(a) Reconstruct Cunningham's debt metaphor from the 1992 report: what is the debt, what is the interest, and what is the repayment? (4 pts)
(b) Using Fowler's technical debt quadrant, classify: (i) "we shipped with a simplistic domain model to hit the trade show, and scheduled the rewrite for next sprint"; (ii) "we don't have time for design". Then state where Fowler himself places the debt Cunningham described, and why that placement is not simply "prudent–deliberate". (4 pts)

<details>
<summary>Model answer</summary>

(a) **Debt**: shipping code that embodies your current, incomplete understanding of the problem ("not-quite-right code") in order to ship — and learn — sooner. **Interest**: every future minute spent working on/around that not-quite-right code; it accrues continuously and can bring an organization to a standstill. **Repayment**: promptly rewriting the code to reflect the improved understanding gained after shipping. The danger is not incurring debt but failing to repay it.

(b) (i) **Prudent–deliberate**: a conscious, scheduled trade of quality-now for time/learning, with a repayment plan ("we must ship now and deal with consequences"). (ii) **Reckless–deliberate**: knowingly skipping design without any repayment strategy — Cunningham explicitly rejected the reading that the metaphor licenses writing bad code; unrepaid, unplanned mess is not the metaphor, it is the failure mode the metaphor warns about. Cunningham's own debt is two-layered: the *decision to ship* is prudent and deliberate, but the not-quite-rightness itself stems from incomplete understanding that only shipping reveals — which is why Fowler places "the kind of debt that Ward talked about" in the **prudent–inadvertent** quadrant ("now we know how we should have done it"): it is inevitable even for excellent design teams, because the right design is only learnable by building.
</details>

---

*Point total: 8+10+8+8+12+12+8+8+12+8+8+8 = 110 → scale to 100 or treat 10 as bonus.*
