# Week 01 Lecture Notes — Algorithm Analysis: Maximum Subsequence Sum

> Source: 4 whiteboard photos (`board-01~04`) + 1 printed quiz (`quiz-01`) + the day-1 (09-02) lecture-audio transcript (`transcript.txt`) + the day-2 (09-04) lecture-audio transcript (`transcript-day2.txt`, both whisper-1 verbose_json re-transcriptions — segment-level, so they preserve the original wording almost verbatim) + an older-semester (Fall 2017) slide archive `lec1.pdf`/`lec02.pdf`/`lec03.pdf` from the same instructor's "족보" (exam-archive) materials — the problems and algorithms are essentially identical to this year's, so these were used to cross-check definitions/theorem statements, not to pull in content not yet covered in class. `_private/2026-2/algorithm-analysis/week-01/`. Instructor: Hyung-Chan An. The course email domain mentioned in the day-2 lecture (`CAS3108...`) suggests the official course code is **CAS3108**, but the printed quiz still reads **CSI 3108** — this discrepancy needs to be confirmed.
>
> **Note**: the day-2 attendance roll-call segment (real student names) is intentionally omitted from both this note and the recap document, for student privacy.

## 1. Problem Definition — Maximum Subsequence Sum

Given a sequence of integers $a_1, \dots, a_n$, find the **maximum sum of a contiguous subsequence**. The empty subsequence is accepted as a valid subsequence with sum 0 (so the answer is always $\ge 0$).

Example sequence from the board: `0 100 -50 -60 30 -10 40 45 -3 1`

Example given verbally in class: taking the subsequence `40, -10, 45` gives a sum of $40 + (-10) + 45 = 75$, which is not the best choice. The actual best is the trailing segment from `40` to `45`, whose total is $110$.

**Clarifying the problem statement (a point the instructor raised himself)**: "What if all the given numbers are negative?" This raises a question — should we (a) just return the single maximum number, or (b) allow the empty subsequence as the answer, with sum 0? In this course, we **accept the empty subsequence as valid** and define its sum as 0. That's the full problem definition.

## 2. Alg 1 — The Most Direct Reading of the Definition

```
sol ← 0
for each i, j with 1 ≤ i ≤ j ≤ n do
    if Σ_{k=i}^{j} a_k > sol then
        sol ← Σ_{k=i}^{j} a_k
return sol
```

`sol` starts at 0 because 0 is itself already a valid answer (the empty subsequence). Presented with the remark that "if you've taken a programming course, this algorithm itself should be self-evident."

## 3. Classroom Interaction — "What's the Running Time?" and the Transition to Alg 2

After presenting Alg 1, the instructor directly asked the class: **"What's the running time of this algorithm?"** Students called out answers, and the instructor followed up with "Does everyone agree? Any other answers?" He guessed that most students had answered either $O(n^3)$ or $O(n^2)$, and acknowledged that **both are reasonable guesses**.

However, the instructor pointed out that the question wasn't entirely **fair** at that point — the implementation details (specifically, how the partial sum is computed) hadn't been made explicit yet. So he rewrote the algorithm to spell those details out, moving on to Alg 2.

## 4. Alg 2 — Alg 1 Rewritten as an Explicit Triple Loop

```
sol ← 0
for i ← 1,…,n do
    for j ← i,…,n do
        sum ← 0
        for k ← i,…,j do
            sum ← sum + a_k
        if sum > sol then
            sol ← sum
return sol
```

The point of this rewrite: what Alg 1 collapsed into one line ("compute the subsequence sum") is actually its own loop — initialize `sum` to 0 and accumulate $a_k$ for $k$ from $i$ to $j$. Making this explicit is exactly what's needed for the running-time analysis.

**Theorem 1.** Alg 2 runs in $O(n^3)$ time.

*Proof.* The number of basic operations is proportional to
$$\sum_{i=1}^{n} \sum_{j=i}^{n} (j-i+1)$$
Substituting $j' = j-i+1$ gives $\sum_{i=1}^n \sum_{j'=1}^{n-i+1} j'$, and substituting $i' = n-i+1$ again and simplifying shows this equals
$$\frac{n(n+1)(n+2)}{6} = \Theta(n^3)$$
by induction (the second-to-last step of the derivation is the part proven by induction). The instructor explicitly said "since today is our first lecture, I'll be more thorough than strictly necessary and walk through the full derivation," and carried out the whole thing on the board.

## 5. Can We Beat Alg 1/2? — Spotting Repeated Computation

**The key question**: can we solve this in asymptotically better time than $O(n^3)$?

**The key observation**: depending on how the partial-sum computation inside Alg 1 is implemented, the very same algorithm can run in either cubic or quadratic time. For example, at $i=2, j=10$ we compute $a_2 + a_3 + \dots + a_{10}$, and at the very next iteration, $i=2, j=11$, we compute $a_2 + \dots + a_{11}$ — **recomputing almost the entirety of the previous sum from scratch**.

The instructor stated a general **algorithm-design principle** explicitly: start from some naive solution, then ask whether there's any **repeated computation** in its execution, and if so, whether there's a **systematic way to eliminate it**. Here, there is — at the next iteration we can just reuse the previously computed value and add one more element to get the new partial sum in constant time.

## 6. Alg 3 — A Prefix-Sum Approach in $O(n^2)$

```
sol ← 0
for i ← 1,…,n do
    sum[i, i-1] ← 0
    for j ← i,…,n do
        sum[i, j] ← sum[i, j-1] + a_j
        if sum[i, j] > sol then
            sol ← sum[i, j]
return sol
```

$\mathrm{sum}[i,j]$ is obtained by taking $\mathrm{sum}[i,j-1]$, already computed in the previous iteration, and adding just $a_j$. A starting value is needed, so $\mathrm{sum}[i,i-1]$ is simply initialized to 0.

**Supplementary index-substitution step for the runtime derivation**: applying the same style of derivation used for Theorem 1 to Alg 3's inner loop, we again substitute $j - i + 1$ with $j'$. Since $j$ ranges from $i$ to $n$, $j'$ ranges from $i - i + 1 = 1$ to $n - i + 1$ — as the instructor noted, this is just relabeling the same range.

**Theorem 2.** Alg 3 runs in $O(n^2)$ time. (Presented as self-evident from the double loop; no separate proof was given.)

## 7. Correctness of Alg 3

**Theorem 3.** Alg 3 is correct.

*Proof.* The instructor first noted that proving an algorithm correct requires **two things**: (1) that it produces the correct answer if it terminates, and (2) that it does terminate. Theorem 2 already gives us termination — since the algorithm runs in quadratic time, it certainly finishes — so all that remains is to show that, assuming termination, the algorithm produces the correct answer.

Looking at the algorithm's behavior, the value returned is
$$\max\big(\{\,\mathrm{sum}[i,j] \mid 1 \le i \le j \le n\,\} \cup \{0\}\big)$$
(the initial value 0 is one of the candidates). Here the instructor raised a subtle point: $\mathrm{sum}[i,j]$ is **just the name of a variable in the algorithm** — in principle it could hold any value. What we actually need to show is that this variable holds a value equal to the true partial sum $\sum_{k=i}^j a_k$, as its name suggests. That's the next claim.

**Claim 1.** For all $1 \le i \le j \le n$, $\mathrm{sum}[i,j] = \sum_{k=i}^{j} a_k$.

*Proof (induction on $j-i$).* For each $l \ge 0$, define a predicate $P(l)$: "for all $i, j$ with $j-i=l$, $\mathrm{sum}[i,j]$ equals the partial sum." Showing $P(0), P(1), P(2), \dots$ all hold is what "induction on $j-i$" means here.

- **Base case** ($j-i=0$): $\mathrm{sum}[i,i] = \mathrm{sum}[i,i-1] + a_i = 0 + a_i = \sum_{k=i}^{i} a_k$.
- **Induction step**: Assume the claim holds when $j-i=\ell_0$. When $j-i=\ell_0+1$,
$$\mathrm{sum}[i,j] = \mathrm{sum}[i,j-1] + a_j = \Big(\sum_{k=i}^{j-1} a_k\Big) + a_j = \sum_{k=i}^{j} a_k. \qquad \blacksquare$$

**Note (from the recording)**: the instructor explicitly pointed out that the variable name $\mathrm{sum}[i,i-1]$ doesn't have to mean "the partial sum from $a_i$ to $a_{i-1}$" — it's just a name, initialized to 0, and Claim 1 only concerns the case $j \ge i$.

## 8. Q&A — Relationship to the Textbook

A student asked whether the lecture material follows the textbook. The instructor's answer: **about 60–70% of the lectures will closely follow the textbook** — its title can be found on the syllabus or the course portal — but the remaining 30% or so goes beyond it, and **today's lecture in particular isn't in the textbook at all**.

## 9. Alg 4 — A Divide-and-Conquer (Merge-Sort-Style) Attempt

Following the lesson from Alg 1→2→3 ("look for repeated computation and eliminate it"), the instructor introduced **recursion as another tool** for designing efficient algorithms. "You've probably already seen at least one recursive algorithm — merge sort — in your data structures course," he said, suggesting we mimic its structure.

**Recap of merge sort's structure (as the instructor described it)**: split the sequence to be sorted into a left half and a right half, recursively sort each half — i.e., solve the exact same problem on two smaller pieces — and then use the results of the two recursive calls to obtain the answer to the original problem; that combining step is merge sort's "merge" step. The same approach is applied here: split the sequence into two halves, recursively find the maximum subsequence sum on each half, and then use those two answers to obtain the answer for the whole sequence.

```
function MSS(s, t):        # returns the maximum subsequence sum of a[s..t]
    if s == t:
        return max(a[s], 0)     # base case: a[s] alone might be negative, so compare against 0
    m ← midpoint(s, t)
    solutionLeft  ← MSS(s, m)
    solutionRight ← MSS(m+1, t)
    return max(solutionLeft, solutionRight)

# main: return MSS(1, n)
```

For the base case, the instructor asked directly: "When $s=t$, i.e. a single element $a_s$, is the answer just $a_s$? Is that really correct? When would it be wrong?" Answer: it's wrong when $a_s$ is negative, in which case the correct answer is 0. Hence we return $\max(a_s, 0)$.

The recursive case mirrors merge sort exactly: compute the midpoint $m$, recurse on $[s,m]$ and $[m+1,t]$, and return the better of the two results. The main body calls this function on the whole range $[1,n]$.

**"Is this algorithm correct?"** — the instructor asked the question and answered it himself: **No, it isn't.** He did **not** reveal, at this point in the lecture, why it's wrong or what the problem is. Having "already run over the time [he] had planned for today," he left it as something for students **to think about at home**, promising to pick it up right from this point in the next lecture (Friday).

**→ The answer revealed on day 2 (09-04) is in §11 below.**

## 10. In-Class Quiz

With time remaining, the instructor gave a quiz (`quiz-01.jpeg`, marked CSI 3108 Fall 2026). Stated purpose: **not graded — used only to check that students have the prerequisite proof techniques.** Writing your name/student ID is optional since it isn't graded. The instructor said solutions would be looked at, but no numerical feedback would be given.

**(1)** Let $a_1,\dots,a_n \in \mathbb{Q}$ ($n \ge 2$). Prove that if $a_1 < a_n$, there exists $i \in \{1,\dots,n-1\}$ with $a_i < a_{i+1}$.
- Only the start of a student's attempt is visible on the board/notes: "Suppose no such $i$ exists" — apparently heading toward a proof by contradiction/contrapositive, but the rest was not recorded.

**(2)** Prove that every simple graph with at least two vertices has at least two distinct vertices of the same degree.
- No solution was recorded.

**Official solutions revealed on day 2 (09-04)** — the instructor worked through both solutions on the board himself (mentioning he'd also post them separately on LearnUs) and shared submission stats: over 30% of students got (1) correct or nearly correct, over 20% got (2) — "I guess the second one was harder."

- **(1) Solution.** He first demonstrated trying a counterexample to build intuition before proving anything: with $n=10$, $a_1=3$, $a_{10}=10$, if you try to fill in a sequence with no such $i$, you get $a_2 \le 3$, $a_3 \le 2$, … — the value can only stay the same or decrease at each step, so by $a_9$ it can't exceed the starting value $a_1=3$, contradicting $a_1 < a_n$. This confirms proof-by-contradiction is the right approach, so the formal proof: suppose no such $i$ exists; then $a_i \ge a_{i+1}$ for all $i$, so $a_1 \ge a_2 \ge \dots \ge a_n$, i.e. $a_1 \ge a_n$ — contradicting $a_1 < a_n$. $\blacksquare$ (Matches the standard proof direction.)
- **(2) Solution.** Since the graph is simple, every vertex's degree lies between $0$ and $n-1$ ($n$ = number of vertices). If all $n$ values from $0$ to $n-1$ actually occurred, that would be the counterexample candidate — but a vertex of degree $n-1$ (adjacent to everything) and a vertex of degree $0$ (adjacent to nothing) cannot coexist, so at least one of the $n$ possible values is necessarily absent, leaving at most $n-1$ distinct degree values actually available for $n$ vertices. By pigeonhole, two vertices must share a degree. $\blacksquare$ (Matches the standard proof direction.)

---

# Day 2 (2026-09-04) — From Fixing Alg 4 to Introducing Closest Pair

> Day 2 actually opened with the quiz solutions above (already folded into §10) and then went straight back to Alg 4. §11 onward follows the actual lecture order from that point.

## 11. Why Alg 4 (§9) Is Wrong, and Algorithm 5 (an $O(n\log n)$ Algorithm That Handles the Boundary)

**Why Alg 4 is wrong.** `solLeft` and `solRight` are simply assumed to be the correct answers for each half. But the true answer for the whole range $[s,t]$ is one of three things: (1) entirely inside the left half → `solLeft` is right, (2) entirely inside the right half → `solRight` is right, or (3) **it crosses the boundary** (between $a_m$ and $a_{m+1}$) — in which case the answer is neither `solLeft` nor `solRight`. Alg 4 simply returns the better of the two, so it completely ignores case (3) — that's the root reason a counterexample exists.

**A naive fix, and its limitation.** Enumerating every possible starting index in $[s,m]$ and ending index in $[m+1,t]$ for a subsequence containing the boundary gives roughly $(n/2)^2 = O(n^2)$ possibilities just for the very first call (length $n$). Since we already have an $O(n^2)$ algorithm (Alg 3), paying this cost on the very first recursive call leaves no room for improvement.

**Key observation.** Under the restriction that the boundary must be contained, the answer is exactly the concatenation of the maximum subsequence ending precisely at the boundary and the maximum subsequence starting precisely at the boundary — if either half weren't locally maximal, swapping in the locally-maximal one could only help.

**Algorithm 5** (run after the two recursive calls):

```
subsolLeft ← 0
for i ← m, m-1, …, s do          # max subsequence ending at the boundary
    partial ← Σ_{k=i}^{m} a_k     # updated in O(1) from the previous partial (same trick as Alg 3)
    if partial > subsolLeft then subsolLeft ← partial

subsolRight ← 0
for i ← m+1, …, t do              # max subsequence starting at the boundary
    partial ← Σ_{k=m+1}^{i} a_k
    if partial > subsolRight then subsolRight ← partial

return max(solLeft, solRight, subsolLeft + subsolRight)
```

The index $i$ runs **decreasing** from $m$ to $s$ for the same reason as in Alg 3 — so the partial sum can be updated in $O(1)$ from the previous value instead of recomputed from scratch. So this merge step runs in $O(t-s+1)$.

**Running time.** "Two recursive calls plus a linear-time merge" is structurally identical to Mergesort — different problem, same time complexity. So Algorithm 5 is $O(n\log n)$: a meaningful improvement over Alg 3's $O(n^2)$.

## 12. From "Wishing" to an $O(n)$ Algorithm

**Thought experiment.** If we somehow knew in advance that "the answer must contain the boundary between $a_{10}$ and $a_{11}$," we could just run §11's merge step with $m$ fixed at 10 and get the answer in $O(n)$. **Knowing the boundary location is enough for a linear-time solution.**

**Algorithm 6 (not an algorithm)**: (1) wish, magically, for an $m$ such that the boundary between $a_m$ and $a_{m+1}$ is contained in the answer; (2) find the max subsequence ending at that boundary; (3) find the max subsequence starting at that boundary; (4) return their sum. Since "wishing" isn't a legal algorithmic step, this isn't a real algorithm.

**The replacement strategy**: if you don't know a piece of information, try every possibility it could have been and take the best. The boundary is one of $1,\dots,n-1$, so try all $n-1$.

**Algorithm 7**:

```
for m ← 1, …, n-1 do
    subsolLeft[m]     ← max({ Σ_{k=i}^{m} a_k | 1 ≤ i ≤ m } ∪ {0})       # max subsequence ending at boundary m
    subsolRight[m+1]  ← max({ Σ_{k=m+1}^{i} a_k | m+1 ≤ i ≤ n } ∪ {0})   # max subsequence starting at boundary m

sol ← 0
for m ← 1, …, n-1 do
    if subsolLeft[m] + subsolRight[m+1] > sol then
        sol ← subsolLeft[m] + subsolRight[m+1]
return sol
```

Implemented naively: $O(n)$ iterations $\times$ $O(n)$ cases $\times$ $O(n)$ per partial sum = $O(n^3)$. Reapplying Alg 3's running-partial-sum trick easily brings this to $O(n^2)$ — the instructor's comment: "after all this hard work, we've come up with... another $O(n^2)$ algorithm." But that trick alone can't reach $O(n)$, since each iteration still has to look at a linear number of distinct partial sums.

## 13. Getting to $O(n)$: a Recurrence Among the `subsolLeft` Values

**Observation.** For all $m>1$:
$$\mathrm{subsolLeft}[m] = \max(\mathrm{subsolLeft}[m-1] + a_m,\ 0)$$

**Proof (given verbally in class).** If $\mathrm{subsolLeft}[m]$ is nonzero, its optimal subsequence is nonempty and must end exactly at boundary $m$, so it must include $a_m$. Given that $a_m$ is included, the rest of the subsequence must be whatever gives the maximum subsequence sum ending at the previous boundary — otherwise you could swap it out for $\mathrm{subsolLeft}[m-1]$ and do better. The zero case is handled separately (choosing the empty subsequence).

**What this buys us.** Starting from $\mathrm{subsolLeft}[1] = \max(a_1, 0)$, each subsequent $\mathrm{subsolLeft}[m]$ is obtained from $\mathrm{subsolLeft}[m-1]$ in $O(1)$ — so **the entire left-subsolution array can be computed in linear time**. By symmetry (just flip direction), the right subsolutions can likewise be computed right-to-left in linear time — this needs two separate for-loops (left computed left-to-right, right computed right-to-left). Adding §12 Algorithm 7's final linear combining loop, **Algorithm 7 as a whole runs in linear time** — not at all obvious from pseudocode that looks $O(n^2)$, as the instructor pointed out.

## 14. A Simpler Linear-Time Algorithm — `MaxEndingAt` (Kadane's Algorithm)

The instructor didn't spell out §13's linear-time version in full detail, because there's a **much simpler** version. Revisiting §12's "wishing" idea: instead of wishing for a boundary "contained in" the answer, wish for the boundary that marks the **end** of the answer — then `subsolRight` becomes entirely unnecessary. The only subtlety: now that it marks an ending rather than an interior boundary, we need one extra case where the sequence ends at the very last position, so $n$ cases instead of $n-1$.

Deleting every `subsolRight`-related line from Algorithm 7, and renaming the now-misleadingly-named "left subsolution" to `MaxEndingAt`, gives the final algorithm:

```
MaxEndingAt[1] ← max(a_1, 0)
for m ← 2, …, n do
    MaxEndingAt[m] ← max(MaxEndingAt[m-1] + a_m, 0)

sol ← 0
for m ← 1, …, n do
    if MaxEndingAt[m] > sol then sol ← MaxEndingAt[m]
return sol
```

**Intuition (the instructor's own re-description, "pretend this is the first algorithm I ever showed you")**: scan from the left, always maintaining the maximum subsequence ending precisely at the current position — either extend the best-so-far by the new element, or, if the running sum goes negative, reset to the empty subsequence. The best value seen over the whole scan is the answer. (In-class Q&A: "so if the running sum becomes negative, you reset it to 0?" — "Yes, because once it's smaller (negative), you're better off with 0.")

## 15. Theorem: No Sublinear Deterministic Algorithm Exists

**Theorem.** No deterministic algorithm for the maximum subsequence sum problem runs in sublinear time. (Presented explicitly as a "proof sketch," not a full proof.)

**Proof sketch.** Suppose such an algorithm exists. Since its running time $f(n)$ is not $\Omega(n)$, for some sufficiently large $n_0$ there exists an input $a_1,\dots,a_{n_0}$ for which the number of basic operations performed is strictly less than $n_0$ — meaning there's some element $a_k$ the algorithm never accesses at all.

- **Case 1**: if every maximum-sum subsequence contains $a_k$, replace $a_k$ with $-\infty$ and imagine rerunning the algorithm on this input. Since the algorithm never accesses $a_k$, its output is unchanged — but every subsequence that used to achieve the maximum now sums to $-\infty$, so the true new answer must be strictly smaller than the algorithm's (unchanged) output — wrong.
- **Case 2**: otherwise, replace $a_k$ with $+\infty$ instead. The true new answer must be $+\infty$, but the algorithm still outputs some finite number — wrong.

Either way, a slight change to a value the algorithm never even looks at breaks correctness — the intuition for why no sublinear algorithm can exist.

## 16. What This Problem Previewed for the Rest of the Course, and Defining "Efficient"

The instructor summarized that this single problem (max subsequence sum) had essentially **previewed nearly every algorithm-design technique for the first half of the semester** — except one, which he did not name at this point (not speculated on here). The rest of the first half will apply these same techniques to other problems: "I can describe the techniques in sentences, but that alone will never let you learn them — you learn them by working through problems and seeing the techniques applied."

**Two major topics for the second half**:
1. **Network flow** — unlike many first-half problems, which mainly exist to illustrate design techniques, network flow is a problem people actually want to solve, with applications throughout computer science. We'll solve and analyze it, then see how it's used as a subroutine for other problems.
2. **NP-completeness** — the mathematical framework for identifying and classifying problems for which no efficient algorithm is known (and, for many, believed not to exist).

**Definition 1 (efficient algorithm).** An algorithm is **efficient** if its running time is bounded by a polynomial in the input size.

Under this definition, the maximum subsequence sum problem was actually an "easy" problem — even the most naive first algorithm (Alg 1/2) was $O(n^3)$, already polynomial. Many of the other problems ahead won't even have a naive polynomial-time algorithm, he noted.

## 17. Course Logistics (Syllabus, Covered Mid-Way Through Day 2)

After a break, the instructor went through the syllabus in detail. (The attendance roll-call segment is omitted per the note at the top of this document.)

- **2 TAs**: Yongchan Ahn (office B721, office hours Mon 3-4pm, Tue 4-5pm); the other TA (office B713, office hours Fri 4-5pm — absent from this particular class, so no self-introduction). Two TAs introduced themselves in class, but the STT rendering of their names is uncertain ("Hongjun Zhang," "Jaehyuk Park" as heard — unclear whether one of these is Yongchan Ahn under a different transliteration or a distinct third TA; needs confirmation).
- **Shared inquiry email**: use the dedicated course email only (not individual emails) — monitored by the whole staff. Policies are strictly enforced, so ask about policy questions in advance, not after the fact.
- **Prerequisites**: everything covered in Data Structures (graphs, basic graph-search algorithms, asymptotic notation, etc.) plus a level of mathematical maturity comparable to Discrete Mathematics (not its specific content, but the ability to read/write proofs at that level). Yonsei's system can't enforce prerequisites, but he strongly discouraged taking the course without this background — students would neither follow the course nor learn much.
- **Format**: mostly blackboard lectures, so students need to take their own notes. "Preview Notes" will be posted once or twice a semester for students who have trouble following lectures in English.
- **Attendance**: authentication-code method via the electronic attendance app (must be installed). No manual attendance credit except where required by university policy (e.g. military training). Questions may be asked in Korean and translated if needed, answered in English.
- **Assignment submission**: via LearnUs; verifying the correct file was uploaded is the student's own responsibility (he mentioned past cases of students uploading the wrong question's solution, or even another course's assignment). No late submissions — LearnUs's server clock has historically drifted from standard time, so submit well in advance. Programming assignments (if any) must be in Java, submitted as source (not bytecode), with exact required class/file names (misspellings make the autograder show zero passing cases).
- **Written solutions**: English, typed with a word processor (no handwriting), no code allowed ("TAs are not compilers").
- **Grading policy (a point he stressed)**: assignments (not exams) are graded **all-or-nothing** — a reasonable attempt gets full credit, with detailed TA feedback given as if it were graded in full, but the official score follows the all-or-nothing rule — explicitly designed to remove the incentive to just have an LLM solve it.
- **Collaboration rules**: no collaboration on programming assignments. Written assignments are the opposite — collaboration is actually **encouraged** (but the write-up must be done entirely alone — no notes leave a group discussion in written form; go home and write your own solution; list all collaborators). External resources (books, other courses' notes) only for reviewing prerequisites, and must be listed. **No LLM-based tools** (ChatGPT, Gemini, Claude, etc.).
- **Academic integrity**: violations can mean a negative grade, a reduced final grade, failing the course, or referral to the disciplinary committee. You must be able to explain your solution orally if asked (failure to do so draws the same penalties). Keeping your own solution from others' access is also your responsibility.
- **Textbook**: *Algorithm Design* (Kleinberg & Tardos), required. Assignments won't directly reference specific textbook problems — it's meant as a self-study aid.
- **Grade breakdown**: prelim 35% + final 40% + assignments 20% + class participation 5%.
- **Exam dates**: prelim **October 21**, final **December 18** (both during regular class hours, room TBA). No leaving the exam room during the first 65 minutes or last 10 minutes; latecomers aren't admitted once someone has already left.
- **Participation/attendance rule**: missing up to 12% of total class hours doesn't affect the score. One late arrival counts as missing 1/3 of that day's class; missing an exam counts as 3 hours. **Reaching 15 total absence-hours (hours, not lecture count, including any missed before adding the course) results in an automatic F, no exceptions.**
- The instructor clarified last week's quiz was purely a prerequisite check, not part of the assignments, and (at least as currently planned) won't be repeated.

## 18. Introducing Closest Pair (To Be Continued Next Class)

The first-half's first real problem: **Closest Pair**.

**Problem statement.** Given $n$ points in the 2D Euclidean plane, find the pair of points that are closest.

A naive all-pairs comparison trivially gives $O(n^2)$, so the goal is to improve on that.

**Starting from the 1D special case.** The instructor suggested first considering points on a single line. A student's answer: starting from the leftmost point, compute the distance to each successive point and take the minimum. Asked for the running time, a student answered $O(n \log n)$, because of the **sorting** needed first — since the input is given in arbitrary order ("if you could assume an ordering, why not just assume the first two points are the closest?"), the algorithm has to sort by $x$-coordinate before it can even identify "leftmost."

**A spoiler, and the next question.** The only two recursive algorithms seen so far — Mergesort and the max-subsequence-sum algorithm — both split the input in half. The same question was posed again for the 1D Closest Pair case: **"Can this be solved recursively? How, and what's the running time?"** — time ran out, and **this question was explicitly left unanswered, to be picked up in the next lecture.** (This note does not speculate here — `lec02.pdf`/`lec03.pdf` appear to contain the formal continuation, but that material was not pulled in until it's actually covered in class.)
