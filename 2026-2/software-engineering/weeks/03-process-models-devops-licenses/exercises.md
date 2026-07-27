# Week 3 — Exercises

Exam-style problems. Total: 100 points. Attempt every problem before opening the model answers.

---

## Q1. Royce and the waterfall (6 pts)

Royce's 1970 paper is routinely cited as the origin of the waterfall model.

(a) State, in one sentence, what Royce actually claimed about the purely sequential implementation. (2 pts)
(b) Name **two** of the five improvements he proposed, and for each, name the later practice it anticipates. (4 pts)

<details>
<summary>Model answer</summary>

(a) Royce presented the sequential phase diagram and then warned that "the implementation described above is risky and invites failure" — because testing occurs at the end, where design flaws (e.g., timing/storage) are discovered at maximum cost, forcing a return that can upend the entire design.

(b) Any two of (1 pt each + 1 pt each for the anticipated practice):
- *Do it twice* — build a pilot version first and discard it → throwaway prototyping.
- *Involve the customer* — formal customer commitment points before delivery → agile's on-site customer / customer collaboration.
- *Program design comes first* — preliminary design before detailed analysis → architecture-first / iterative design.
- *Plan, control, monitor testing* → independent test planning, V&V discipline.
- *Document the design* → design documentation supporting iteration.
</details>

---

## Q2. When plan-driven still wins (8 pts)

Sommerville identifies three kinds of systems for which a waterfall-style (plan-driven) process remains appropriate. Name all three and, for each, explain in one sentence **why** the frozen-specification property is a benefit rather than a liability there.

<details>
<summary>Model answer</summary>

1. **Embedded systems** (2–3 pts): the software must conform to hardware whose interfaces are inflexible and expensive to change, so freezing the spec against the hardware is realistic and necessary.
2. **Critical (safety/security) systems** (2–3 pts): certification requires extensive safety/dependability analysis *of the specification and design documents*; if the spec keeps changing, the analyses must be redone, so a stable, approved spec is a precondition for the required V&V evidence.
3. **Large systems developed by several partner companies** (2–3 pts): frozen interface specifications are the coordination contract between independently working organizations; without them, integration across companies is impossible.

(Full marks require the *reason* tied to freezing, not just the list.)
</details>

---

## Q3. Incremental development failure modes (8 pts)

(a) Explain the two problems Sommerville attributes to incremental development: **process invisibility** and **structure degradation (architecture erosion)**. (4 pts)
(b) Which XP practice is the direct countermeasure to erosion, and why does that practice itself depend on test-first development? (4 pts)

<details>
<summary>Model answer</summary>

(a) *Process invisibility*: managers gauge progress through stage deliverables (documents); incremental development produces few of them, and producing documents for every increment destroys the speed advantage — a visibility/speed trade-off. *Architecture erosion*: each new increment is locally cheaper to bolt onto the existing structure than to restructure first, so without deliberate investment the structure degrades, and the cost of change rises over time — eventually worse than a planned design.

(b) **Refactoring** — continuously improving structure as soon as an improvement is seen, paying down the erosion each increment. It depends on **test-first development** because refactoring changes structure while preserving behavior; without an automated regression suite there is no way to verify behavior preservation, making refactoring a gamble teams will rationally avoid.
</details>

---

## Q4. Spiral model — risk arithmetic (12 pts)

A team must integrate with a legacy billing API whose behavior is poorly documented. If they build directly against it and their assumptions are wrong, they estimate a rework loss of \$400k with probability 0.5. Two mitigation options exist for the next spiral cycle:

- **Option A**: a 2-week integration spike (cost \$25k) that would reduce the failure probability to 0.15.
- **Option B**: purchasing a vendor-support contract (cost \$80k) that would reduce the failure probability to 0.05.

(a) Define risk exposure and compute the current $RE$. (3 pts)
(b) Compute the risk reduction leverage $RRL$ of both options. (6 pts)
(c) Which option should the next spiral cycle choose, and what general property of the spiral model does this decision illustrate? (3 pts)

<details>
<summary>Model answer</summary>

(a) $RE = P(UO) \times L(UO)$ — probability of the unsatisfactory outcome times the loss if it occurs. Current $RE = 0.5 \times 400\text{k} = \$200\text{k}$.

(b) $RRL = (RE_{before} - RE_{after}) / \text{cost}$.
- A: $RE_{after} = 0.15 \times 400\text{k} = 60\text{k}$; $RRL_A = (200 - 60)/25 = 5.6$.
- B: $RE_{after} = 0.05 \times 400\text{k} = 20\text{k}$; $RRL_B = (200 - 20)/80 = 2.25$.

(c) Choose **A**: it buys more risk reduction per dollar ($RRL_A > RRL_B$; both exceed 1, but A dominates on leverage; a follow-up cycle can re-evaluate whether the residual $60\text{k}$ exposure justifies further spending). This illustrates that the spiral model is **risk-driven**: the activity performed in each cycle (prototype, spike, buy, or just proceed) is selected by explicitly quantifying and comparing risk-resolution alternatives, not by a fixed phase sequence.
</details>

---

## Q5. Scrum vocabulary — precision test (10 pts)

Using the exact terminology of the 2020 Scrum Guide:

(a) Name the three accountabilities and state, for each, the one thing it alone controls or is responsible for. (3 pts)
(b) Name the five events and give the timebox of the Daily Scrum and the maximum Sprint length. (4 pts)
(c) Name the three artifacts and the commitment attached to each. (3 pts)

<details>
<summary>Model answer</summary>

(a) **Product Owner** — sole authority over the content and ordering of the Product Backlog (maximizing product value); **Scrum Master** — accountable for Scrum being understood and effective (in the 2020 Guide's wording, a "true leader who serves the Scrum Team and the larger organization" — the 2017 term "servant-leader" was dropped — with no command authority over people); **Developers** — accountable for creating a usable Increment each Sprint and solely decide *how* to do the work (self-managing).

(b) **The Sprint** (container, fixed length ≤ 1 month), **Sprint Planning** (≤ 8h for a one-month sprint), **Daily Scrum** (15 minutes), **Sprint Review** (≤ 4h), **Sprint Retrospective** (≤ 3h). Daily Scrum = 15 min; max Sprint = one month.

(c) **Product Backlog** ↔ **Product Goal**; **Sprint Backlog** ↔ **Sprint Goal**; **Increment** ↔ **Definition of Done**.
</details>

---

## Q6. Agile Manifesto (6 pts)

(a) Complete the four value statements of the Agile Manifesto ("X over Y" form). (4 pts)
(b) The manifesto ends the value list with a qualifying sentence. Quote or paraphrase it, and explain the misreading it forecloses. (2 pts)

<details>
<summary>Model answer</summary>

(a) Individuals and interactions **over processes and tools**; Working software **over comprehensive documentation**; Customer collaboration **over contract negotiation**; Responding to change **over following a plan**.

(b) "That is, while there is value in the items on the right, we value the items on the left more." It forecloses the misreading that agile abolishes process, documentation, contracts, and planning — these retain value; the manifesto only re-orders priorities when the two sides conflict.
</details>

---

## Q7. DORA four key metrics — computation (12 pts)

A service records the following over a 30-day window. Ten production deployments occurred; for each, commit-to-production times were (hours): 3, 3, 4, 4, 5, 6, 30, 48, 3, 4. Three deployments caused degraded service; their restoration times were 30 min, 90 min, and 6 h.

(a) Compute all four DORA metrics. Use the median for lead time and justify that choice. (8 pts)
(b) The team's manager proposes bonusing engineers on deployment frequency alone. Using the structure of the four metrics, explain the failure mode of this proposal. (4 pts)

<details>
<summary>Model answer</summary>

(a)
- **Deployment frequency**: 10 / 30 days ≈ 0.33 deploys/day (≈ 2–3 per week).
- **Lead time for changes**: sorted = 3,3,3,4,4,4,5,6,30,48 → median = (4+4)/2 = **4 h**. Median because the distribution is right-skewed (two outliers at 30 h and 48 h drag the mean to 11 h, which describes no typical change) — same argument as percentile latency reporting.
- **Change failure rate**: 3/10 = **30%**.
- **Time to restore service**: (0.5 + 1.5 + 6)/3 = **2.67 h** (mean; median 90 min also acceptable if stated).

(b) The four metrics are two throughput measures (frequency, lead time) *paired with* two stability measures (CFR, restore time) precisely so each pair guards the other. Rewarding frequency alone incentivizes shipping many small but poorly verified changes: frequency rises while change failure rate and restore time silently degrade — the metric becomes a target and stops measuring delivery performance (Goodhart's law). Accelerate's finding is that genuine high performers improve on *all four together*; any single-metric bonus scheme selects for gaming, not performance.
</details>

---

## Q8. Deployment pipeline — failure semantics (10 pts)

For each incident below, name the pipeline stage that should have caught it (commit / acceptance / staging / production) and state what class of defect the failure signals:

(a) A unit-tested service passes all its own tests, but returns HTTP 500 when the order service calls it, because the two teams disagree about a field's nullability. (2 pts)
(b) A migration script runs fine on developers' laptops but times out against a production-sized table. (2 pts)
(c) A change compiles but violates the lint rule set and one pure-function unit test. (2 pts)
(d) A new feature performs correctly everywhere but causes a 40% checkout drop for users in one country due to a payment-provider quirk no test environment reproduces. (2 pts)
(e) Explain why stages after the commit stage must reuse the **same build artifact** rather than rebuilding, citing the relevant twelve-factor principle. (2 pts)

<details>
<summary>Model answer</summary>

(a) **Acceptance/integration stage** — the units are individually correct but the *assembly* violates an inter-component contract; unit tests structurally cannot catch cross-service contract drift.
(b) **Staging** — the code is correct but an *environmental assumption* (data scale) is wrong; only a production-like environment exposes it.
(c) **Commit stage** — code-local logic/convention defects, fixable immediately by the committer; this is why the commit stage must be fast (~10 min feedback).
(d) **Production** — reality differs from every prior assumption; such failures cannot be eliminated, so the pipeline design goal shifts to limiting blast radius (canary) and restore time (rollback, monitoring).
(e) Twelve-factor **V: build, release, run** — strict separation with an immutable build artifact. Rebuilding per environment breaks the identity between what was tested and what is deployed (different dependency resolution, compiler state, timestamps), invalidating all confidence accumulated by earlier stages.
</details>

---

## Q9. Cloud models and serverless economics (8 pts)

(a) NIST SP 800-145 lists five essential characteristics of cloud computing. Name four. (2 pts)
(b) Classify each: (i) renting VMs where you patch the OS; (ii) Gmail used by a company; (iii) uploading only Python functions triggered by HTTP events; (iv) a managed platform where you `git push` application code and the provider runs it. (2 pts)
(c) A FaaS platform charges \$0.20 per million invocations plus \$0.0000167 per GB-second. A function uses 1 GB and runs 200 ms per invocation. A reserved VM able to serve the same workload costs \$75/month. At how many invocations per month do the two costs cross? State one *non-cost* argument for each side at that traffic level. (4 pts)

<details>
<summary>Model answer</summary>

(a) On-demand self-service; broad network access; resource pooling; rapid elasticity; measured service (any four).

(b) (i) IaaS; (ii) SaaS; (iii) FaaS; (iv) PaaS.

(c) Per-invocation cost = \$0.20/10⁶ + 1 GB × 0.2 s × \$0.0000167 = \$0.0000002 + \$0.00000334 = \$0.00000354. Crossover: $75 / 0.00000354 \approx 21.2$ million invocations/month (≈ 8 invocations/s sustained). Below that, FaaS is cheaper (scale-to-zero: no idle charge); above, the VM wins.
Non-cost arguments: for FaaS even above crossover — no capacity planning/ops, automatic scaling for spikes far beyond one VM. For the VM even below crossover — no cold-start latency in the tail (p99), no per-invocation duration cap, less vendor lock-in.
</details>

---

## Q10. License audit — distribution mode flips the verdict (12 pts)

Your proprietary analytics product has these dependencies:

| Dependency | License | Integration |
|---|---|---|
| web framework | BSD-3-Clause | imported |
| HTTP client | Apache-2.0 | imported |
| DB driver | LGPL-3.0 | dynamically linked, unmodified |
| plotting library | GPL-3.0-only | imported |
| PDF engine | AGPL-3.0 | invoked as a separate process via `exec`, unmodified |

(a) The product is offered **only as SaaS**. For each dependency, state whether any source-disclosure obligation is triggered, and why. (5 pts)
(b) The company now ships the product as an **on-premises appliance** to customers. Re-evaluate each dependency and identify the one that now blocks proprietary distribution. Give two remediation options. (5 pts)
(c) Suppose the team patches the AGPL PDF engine to add a feature, still SaaS-only. What changes? (2 pts)

<details>
<summary>Model answer</summary>

(a) SaaS = no conveying. BSD/Apache: no trigger (notice obligations attach only on distribution). LGPL driver: no trigger. GPL plotting lib: **no obligation triggered** — copyleft triggers on conveying, not use; but it is a latent liability. AGPL PDF engine: §13 triggers only for **modified** versions offered over a network; it is unmodified and runs as a separate arm's-length process → no obligation.

(b) Shipping = conveying; everything is re-evaluated. BSD/Apache: include license texts, NOTICE, mark modifications (compliance, not disclosure). LGPL driver: OK to stay proprietary **if** users can relink/replace the library (dynamic linking satisfies this) and any modifications to the library itself are released. GPL plotting lib: **blocker** — the shipped work combines with GPL code at the module level, so conveying requires releasing the whole combined work under GPL-3.0. Remediations (any two): remove/replace the library with a permissive alternative; negotiate a commercial/dual license from its copyright holder; (partial) re-architect it behind a genuinely separate process at arm's length — riskier, fact-dependent. AGPL engine: as a separate unmodified program it can be aggregated, but its own source must be offered; a commercial license is the safe path if coupling is intimate.

(c) Modification + network interaction triggers AGPL §13: all users interacting with the modified engine remotely must be offered the **Corresponding Source of the modified version** — even though nothing is distributed.
</details>

---

## Q11. Compatibility and SPDX (8 pts)

(a) Why is Apache-2.0 code compatible with GPL-3.0 but not with GPL-2.0-only? (3 pts)
(b) Why can code licensed "GPL-2.0-only" not be combined with "GPL-3.0-only" code in one distributed work? (2 pts)
(c) Interpret each SPDX expression: (i) `MIT OR Apache-2.0`; (ii) `GPL-2.0-only WITH Classpath-exception-2.0`; and explain what the Classpath exception enables in practice. (3 pts)

<details>
<summary>Model answer</summary>

(a) GPL-3.0 was drafted (via its §7 additional-permissions mechanism) to tolerate Apache-2.0's extra conditions, notably its patent-retaliation clause; under GPL-2.0 the FSF regards those same conditions as impermissible "further restrictions", so the combination cannot satisfy both licenses — compatibility is one-way, permissive → GPL-3.0.

(b) Each license demands that the combined work be distributed under *itself* and permits no additional restrictions from the other; "GPL-2.0-only" excludes the "or any later version" upgrade path, so no single license can satisfy both simultaneously — the works cannot be combined and conveyed.

(c) (i) The recipient may choose **either** MIT or Apache-2.0 (disjunctive choice — commonly used to let both permissive and patent-conscious consumers pick). (ii) The work is GPL-2.0-only but with the Classpath exception attached: programs that merely **link** against this library (e.g., every Java application linking the OpenJDK class library) are *not* pulled into GPL obligations — the exception carves linking out of the copyleft scope, which is what makes proprietary Java applications on OpenJDK possible.
</details>
