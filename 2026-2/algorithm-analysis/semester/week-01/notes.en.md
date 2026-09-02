# Week 01 Lecture Notes — Algorithm Analysis: Maximum Subsequence Sum

> Source: 4 whiteboard photos (`board-01~04`) + 1 printed quiz (`quiz-01`) + the full lecture-audio transcript (`transcript.txt`, whisper-1 verbose_json re-transcription — segment-level, so it preserves the original wording almost verbatim). `_private/2026-2/algorithm-analysis/week-01/`. Instructor: Hyung-Chan An. The course code is written as **CAS3108** on the whiteboard but **CSI 3108** on the printed quiz — this discrepancy needs to be confirmed.

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

**"Is this algorithm correct?"** — the instructor asked the question and answered it himself: **No, it isn't.** He did **not** reveal, at this point in the lecture, why it's wrong or what the problem is. Having "already run over the time [he] had planned for today," he left it as something for students **to think about at home**, promising to pick it up right from this point in the next lecture (Friday). (Since the lecture did not disclose the answer up to this point, this note does not speculate about why it's wrong — that will be added when the follow-up lecture is ingested and the delta is updated.)

## 10. In-Class Quiz

With time remaining, the instructor gave a quiz (`quiz-01.jpeg`, marked CSI 3108 Fall 2026). Stated purpose: **not graded — used only to check that students have the prerequisite proof techniques.** Writing your name/student ID is optional since it isn't graded. The instructor said solutions would be looked at, but no numerical feedback would be given.

**(1)** Let $a_1,\dots,a_n \in \mathbb{Q}$ ($n \ge 2$). Prove that if $a_1 < a_n$, there exists $i \in \{1,\dots,n-1\}$ with $a_i < a_{i+1}$.
- Only the start of a student's attempt is visible on the board/notes: "Suppose no such $i$ exists" — apparently heading toward a proof by contradiction/contrapositive, but the rest was not recorded. (Noting only the standard proof direction for reference: the contrapositive — if $a_i \ge a_{i+1}$ for all $i$, the sequence is non-increasing, so $a_1 \ge a_n$, contradicting $a_1 < a_n$.)

**(2)** Prove that every simple graph with at least two vertices has at least two distinct vertices of the same degree.
- No solution was recorded. (Noting only the standard proof direction for reference: the degree of each of the $n$ vertices is one of $\{0,\dots,n-1\}$, but a vertex of degree 0 and a vertex of degree $n-1$ cannot coexist, so there are really only $n-1$ possible degree values — by pigeonhole, two vertices must share a degree.)
