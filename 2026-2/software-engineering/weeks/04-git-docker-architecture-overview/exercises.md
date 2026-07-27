# Week 4 — Exercises

Exam-style problems. 100 points total. Attempt every problem before opening the model answers.

---

## Q1. Content addressing (8 pts)

A file contains exactly the 4 bytes `abc\n`.

(a) Write down the exact byte string that Git hashes to obtain this file's blob id. (3 pts)
(b) Explain why the resulting id is independent of the file's name, path, and modification time, and name one concrete benefit Git derives from this property. (3 pts)
(c) The same 4-byte content appears in 3 different files across 5 different commits. How many blob objects does the object database store for this content? Justify. (2 pts)

<details><summary>Model answer</summary>

(a) `blob 4\0abc\n` — i.e., the header `"blob "`, the content size in ASCII decimal (`4`), a NUL byte, then the content. The blob id is SHA-1 over this concatenation.

(b) A blob stores *only* content; names, paths, and timestamps live in tree and commit objects that point *to* the blob. Benefit (any one): automatic deduplication of identical content; cheap equality checks (same id ⟺ same content) enabling fast `status`/`diff`; integrity verification (recompute hash and compare).

(c) Exactly **one**. The address is a function of content alone, so every occurrence maps to the same key in the object store; trees in different commits simply reference the same blob id.
</details>

---

## Q2. The object graph under change (10 pts)

A repository has this committed structure:

```
/ (root tree)
├── README.md          (blob B1)
└── src/ (tree T_src)
    ├── app.py         (blob B2)
    └── util.py        (blob B3)
```

You edit `src/util.py` only, then `git add` and `git commit`.

(a) List every **new** object created by this add+commit, in dependency order. (4 pts)
(b) Which existing objects are reused (referenced but not recreated)? (3 pts)
(c) At which of these two moments is the new blob written into `.git/objects` — during `git add` or during `git commit`? What does `git commit` itself do? (3 pts)

<details><summary>Model answer</summary>

(a) Four new objects: (1) a new blob B3′ for the new content of `util.py`; (2) a new tree T_src′ (its entry for `util.py` now points at B3′, so its own hash changes); (3) a new root tree (its entry for `src` now points at T_src′); (4) a new commit pointing at the new root tree, with the previous commit as parent. The change "bubbles up" the Merkle path from the modified leaf to the root.

(b) B1 (`README.md`) and B2 (`app.py`) are reused — the new trees reference their unchanged ids. The previous commit object is referenced as parent.

(c) During **`git add`**: the blob is hashed and written to the object DB immediately, and the index entry is updated to point at it. `git commit` freezes the index into tree objects, creates the commit object, and advances the ref that HEAD designates. (Lab A3 verifies the object DB contains the blob while no tree/commit exists yet.)
</details>

---

## Q3. Executing a three-way merge by hand (10 pts)

The merge base version of `config.txt` is:

```
1: timeout = 30
2: retries = 3
3: log = info
4: region = us
5: cache = on
```

- **Ours** changed line 1 to `timeout = 60` and deleted line 5.
- **Theirs** changed line 1 to `timeout = 60` and changed line 3 to `log = debug`.

(a) Produce the merged file, or the conflict markers if any region conflicts. Justify each line using the three-way decision rule. (6 pts)
(b) Now suppose ours had instead changed line 1 to `timeout = 90`. What changes in the outcome, and what exactly does Git leave in the index for this path? (4 pts)

<details><summary>Model answer</summary>

(a) No conflicts. Per region against base: line 1 — both sides changed it **identically** (`60`) → take it. Line 2 — neither changed → keep. Line 3 — only theirs changed → `log = debug`. Line 4 — neither changed → keep. Line 5 — only ours changed (deletion; theirs kept base) → deletion taken. Merged file:

```
timeout = 60
retries = 3
log = debug
region = us
```

Note the region-separation trap: this auto-merges only because every changed region is separated by **at least one unchanged base line** (line 2 between the line-1 edits and line 3; line 4 between line 3 and the deleted line 5). If theirs had *also* edited line 4 — adjacent to ours' deleted line 5 — Git's merge treats the two **touching** changed regions as one overlapping region and reports a content conflict spanning lines 3–5, even though each side changed "a different line" (verified with git 2.39, `ort` strategy).

(b) Line 1 now satisfies the conflict condition: ours ≠ base ∧ theirs ≠ base ∧ ours ≠ theirs → **conflict** on that region only (the other regions still auto-merge: `log = debug` is taken, line 5 stays deleted). The working file gets `<<<<<<< / ======= / >>>>>>>` markers around `timeout = 90` vs `timeout = 60`, and the index holds **three stages** for `config.txt`: stage 1 = base version, stage 2 = ours, stage 3 = theirs. Resolving and running `git add` collapses them back to a single stage-0 entry.
</details>

---

## Q4. Why a base is needed; multiple bases (8 pts)

(a) Using a concrete one-line example, show why a **two-way** merge (comparing only ours and theirs) cannot be correct in general. (4 pts)
(b) Define what `git merge-base A B` computes in DAG terms. In a criss-cross history it can return multiple candidates — what do the `recursive`/`ort` strategies do in that case? (4 pts)

<details><summary>Model answer</summary>

(a) Suppose ours contains the line `DEBUG = true` and theirs does not. Two-way comparison cannot distinguish: (i) the line existed in the common ancestor and *theirs deleted it* (correct merge: drop it) from (ii) *ours added it* (correct merge: keep it). The two cases demand opposite outcomes, so any base-free rule is wrong on one of them. The base disambiguates by revealing who changed what.

(b) It computes a **best common ancestor** of A and B in the commit DAG — a common ancestor not an ancestor of any other common ancestor (a "lowest" common ancestor). With criss-cross merges there can be several such commits; `recursive`/`ort` first **merge the candidate bases with each other**, recursively, and use the resulting *virtual base* tree as the reference for the final three-way merge. `ort` is the default strategy since Git 2.34.
</details>

---

## Q5. The rebase incident (10 pts)

Alice and Bob share branch `feature` (both have pushed and pulled it). Alice runs `git rebase main` on `feature` and pushes with `--force`. Bob, unaware, runs `git pull` on his old `feature`.

(a) Explain, at the object-model level, why Alice's rebase necessarily created new commit ids rather than "moving" her commits. (3 pts)
(b) Describe the history Bob ends up with after his pull, and why every subsequent merge gets worse. (4 pts)
(c) State the rule that prevents this class of incident, and explain why `--force-with-lease` is safer than `--force` for the cases where rewriting *is* legitimate. (3 pts)

<details><summary>Model answer</summary>

(a) A commit's id is a hash over its content, which includes its **parent id** and root tree. Rebase re-applies each commit onto a new parent, so parent (and possibly tree) change ⇒ the hash changes ⇒ these are new objects. Objects are immutable; Git can only add new ones and move refs.

(b) Bob's pull merges the remote's rewritten `feature` (commits C1′..Cn′) with his local old `feature` (C1..Cn). Git sees them as unrelated commits (different ids), so the merge result contains **both copies of every change** — duplicated commits, often with conflicts since the same diffs apply twice. Each later merge between divergent copies compounds the duplication and conflicts.

(c) The golden rule: **never rebase commits that have been pushed/shared** — rebase only commits that exist solely in your local repo (e.g., tidying your own PR branch). When force-pushing your own branch is legitimate, `--force-with-lease` refuses to push unless the remote ref still points where your last fetch saw it, so it cannot silently discard a teammate's push that happened in between; bare `--force` overwrites unconditionally.
</details>

---

## Q6. Choosing a collaboration model (8 pts)

For each team, choose git-flow, GitHub flow, or trunk-based development, and justify with the mechanism that fits (release branches, hotfix path, PR cadence, feature flags, DORA evidence). One model per team.

(a) A mobile-app team: releases go through 1-week app-store review; versions 3.1 and 3.2 must both receive security patches. (3 pts)
(b) An 8-person SaaS team deploying the single production version several times a day from `main`. (2 pts)
(c) A 200-developer organization with mature CI, aiming to maximize integration frequency; incomplete features must still ship dark. (3 pts)

<details><summary>Model answer</summary>

(a) **git-flow.** Versioned releases with a review/hardening window map to release branches (stabilize while `develop` moves on); supporting multiple in-production versions requires hotfix branches cut from the tagged releases and merged back — exactly the machinery git-flow standardizes.

(b) **GitHub flow.** One always-deployable `main`, short PR branches, deploy-on-merge. No version branches needed because deployment *is* the release; git-flow's develop/release overhead buys nothing here (Driessen's own 2020 note says as much).

(c) **Trunk-based development.** Daily (or more frequent) integration into trunk with branches living under a day keeps divergence — and merge/semantic-conflict risk — minimal at scale; incomplete work ships behind **feature flags** (deploy ≠ release). Accelerate/DORA found short-lived branches and daily trunk integration correlate with higher delivery performance.
</details>

---

## Q7. Designing protected-branch policy (10 pts)

After two incidents — (i) a developer force-pushed to `main` and destroyed two days of history; (ii) an urgent fix was pushed directly to `main` without review and broke production — you must configure branch protection for `main` on GitHub. List **four** distinct protection settings, and for each state the invariant it enforces and which incident (i/ii, or a new failure mode) it addresses.

<details><summary>Model answer</summary>

Any four of:

1. **Block force pushes (and deletions)** — `main`'s history is append-only; refs move only forward. Directly prevents (i).
2. **Require a pull request before merging + N approving reviews** — no commit reaches `main` without at least one other person approving the diff. Directly prevents (ii).
3. **Required status checks** — the CI suite (build + tests) must be green on the PR head before merge; prevents the "urgent fix breaks production" half of (ii) even when reviewed, wiring the W3 pipeline in as a gate.
4. **Dismiss stale approvals on new pushes** — an approval applies only to the reviewed snapshot; pushing new commits invalidates it, closing the "approve, then sneak in changes" hole.
5. **CODEOWNERS-based review requirement** — changes under sensitive paths require approval from the owning team, not just anyone.
6. **Require branches to be up to date before merging (or a merge queue)** — the tested combination is the one that lands, preventing semantically conflicting but textually clean parallel merges.

(Each: setting + invariant + mapped failure mode.)
</details>

---

## Q8. Namespaces vs cgroups (10 pts)

Two containers on one host misbehave differently:

- Container A (`docker run --memory=256m ...`) dies intermittently; `docker inspect` shows exit code 137.
- Container B (`docker run --cpus=0.5 ...`) never dies, but its p99 latency shows periodic spikes of hundreds of ms while host CPU is mostly idle.

(a) Explain each symptom by naming the kernel mechanism and its enforcement behavior. (4 pts)
(b) State the one-line division of labor between namespaces and cgroups. (2 pts)
(c) A colleague says: "processes inside a container are invisible to the host, that's the point of containers." Correct this statement precisely, referencing the pid namespace. (4 pts)

<details><summary>Model answer</summary>

(a) A: the **memory cgroup** (`memory.max`) is a hard limit; when the group's usage exceeds it, the kernel invokes the **OOM killer scoped to that cgroup** — the process is SIGKILLed (128+9 = exit 137). B: the **cpu cgroup** (`cpu.max` quota/period) enforces by **throttling**, not killing: once the quota within a period is consumed, the group's threads are descheduled until the period ends, which appears as periodic latency spikes even on an idle host. Memory limits kill; CPU limits stall.

(b) Namespaces isolate **what a process can see** (visibility of PIDs, mounts, network, ...); cgroups limit **how much it can use** (CPU, memory, IO, pids).

(c) Backwards. Container processes are ordinary host processes and **are visible from the host** (`ps` on the host shows them, under host PID numbers). The pid namespace only restricts the view **from inside**: within the container, processes see a private PID space where the first process is PID 1 and host processes are invisible. The same task thus has different PIDs in different namespaces (the kernel's multi-level pid mapping).
</details>

---

## Q9. OverlayFS reasoning (10 pts)

An image is built from these steps (each producing a layer, bottom to top):

- L1: adds `/app/secret.pem` (2 KB) and `/app/data.bin` (1 GB)
- L2: `RUN rm /app/secret.pem`
- L3: adds `/app/app.py`

A container starts from this image and appends one line to `/app/data.bin`.

(a) What does the container see under `/app`, and via which OverlayFS rule is `secret.pem` absent? (3 pts)
(b) What physically happens on the first append to `data.bin`, and what is the cost? Name the mechanism. (3 pts)
(c) Is `secret.pem` recoverable by someone who obtains the image? Why? Give the standard fix for (i) image size bloat from build tools and (ii) secrets needed at build time. (4 pts)

<details><summary>Model answer</summary>

(a) The container sees `/app/data.bin` and `/app/app.py`. `secret.pem` is hidden because L2 contains a **whiteout** entry (a 0/0 character device with that name); the merged view suppresses any lower-layer file shadowed by a whiteout. Nothing was removed from L1 — layers are immutable.

(b) **Copy-up**: OverlayFS copies the *entire* 1 GB file from the read-only lowerdir into the container's writable upperdir, then applies the append there. Copy-on-write is at file granularity, so the first write costs ~1 GB of IO and disk; subsequent writes hit the upper copy directly.

(c) Yes. The bytes of `secret.pem` are intact inside L1's tar; `docker save` (or pulling layers from the registry) exposes every layer regardless of later whiteouts. Fixes: (i) **multi-stage build** — compile in a builder stage, `COPY --from` only artifacts into the final stage, so toolchain/source layers never enter the shipped image; (ii) **build secrets** (e.g., BuildKit secret mounts), which expose the secret to a RUN step without recording it in any layer.
</details>

---

## Q10. Layer-cache-aware Dockerfile (8 pts)

Given:

```dockerfile
FROM node:22
WORKDIR /app
COPY . .
RUN npm ci          # ~3 minutes
RUN npm run build
CMD ["node", "dist/server.js"]
```

(a) Explain why every source-code commit pays the full 3-minute `npm ci` in CI, citing the two cache-key rules involved. (3 pts)
(b) Rewrite the Dockerfile so that a source-only change skips `npm ci`, and state which steps re-run after (i) a source change, (ii) a `package-lock.json` change. (3 pts)
(c) Why must `apt-get update` and `apt-get install ...` be a single RUN instruction in cache terms? (2 pts)

<details><summary>Model answer</summary>

(a) `COPY . .` is keyed on the **checksum of the copied files**; any source edit changes it → cache miss at that step. A miss **invalidates every subsequent step** (each step's key includes its parent layer), so `RUN npm ci` re-runs even though `package-lock.json` did not change.

(b)

```dockerfile
FROM node:22
WORKDIR /app
COPY package.json package-lock.json ./
RUN npm ci
COPY . .
RUN npm run build
CMD ["node", "dist/server.js"]
```

(i) Source change: `COPY package*.json` and `RUN npm ci` are CACHED; only `COPY . .` and `npm run build` re-run. (ii) Lock-file change: the first COPY misses → `npm ci` and everything after re-run (cascade). (The chapter's lab measures this: 3791 ms vs 649 ms rebuild for the same simulated install.)

(c) `RUN` is keyed on the **command string only**, not its outputs. A standalone `RUN apt-get update` layer stays cached forever, so a later modified `RUN apt-get install pkg` would install from a stale package index. Combining `apt-get update && apt-get install -y pkg` in one instruction ensures the index is refreshed whenever the install line changes.
</details>

---

## Q11. 4+1 views and quality tradeoffs (8 pts)

(a) Assign each decision to exactly one 4+1 view (logical / process / development / physical / scenarios): (4 pts)

1. "Order processing consumes payment events from a Kafka topic with 12 partitions."
2. "The codebase is split into `domain`, `application`, and `infrastructure` Gradle modules owned by two teams."
3. "The `Order` aggregate owns `OrderLine` entities; discounts are a strategy object."
4. "Each availability zone runs two replicas behind the regional load balancer."

(b) Sommerville's guidance says performance-critical systems should localize critical operations in a few large-grain components, while maintainability favors fine-grain replaceable components. Explain why both cannot be maximized in one structure, and name what an architect produces instead of a "correct" answer. (4 pts)

<details><summary>Model answer</summary>

(a) 1 → **process** view (runtime concurrency and communication). 2 → **development** view (module organization and team ownership). 3 → **logical** view (functional/domain decomposition). 4 → **physical** view (deployment onto nodes/zones). (Scenarios is the "+1" that walks a use case through the other four; none of these is a scenario.)

(b) The prescriptions pull the same design variable — component granularity — in opposite directions: performance wants **fewer, larger** components to minimize inter-component communication on the critical path; maintainability wants **many, small** components so changes and replacements stay localized. One structure has one granularity per boundary, so improving one attribute degrades the other. The architect's output is therefore a **prioritized tradeoff** — an explicit, documented decision (e.g., an ADR) about which attribute wins where, and by how much — not an optimum. Quality attributes emerge from structure, which is also why these decisions are early and expensive to reverse.
</details>
