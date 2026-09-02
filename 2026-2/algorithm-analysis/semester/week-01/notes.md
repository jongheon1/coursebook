# Week 01 강의 노트 — Algorithm Analysis: Maximum Subsequence Sum

> 소스: 판서 사진 4장 + 인쇄 퀴즈 1장(`_private/2026-2/algorithm-analysis/week-01/`). 녹음 없음 — 판서 내용만으로 재구성. 담당교수: Hyung-Chan An. 과목 코드가 판서에는 **CAS3108**, 퀴즈 인쇄물에는 **CSI 3108**로 서로 다르게 적혀 있어 확인이 필요하다.

## 1. 문제 정의 — Maximum Subsequence Sum

정수 수열 $a_1, \dots, a_n$ 이 주어졌을 때, **연속 부분수열(contiguous subsequence)의 합 중 최댓값**을 구하라. 공집합도 합이 0인 유효한 부분수열로 인정한다(따라서 답은 항상 $\ge 0$).

칠판 예시 수열: `0 100 -50 -60 30 -10 40 45 -3 1`

## 2. Alg 1 — 가장 단순한 정의 그대로

```
sol ← 0
for each i, j with 1 ≤ i ≤ j ≤ n do
    if Σ_{k=i}^{j} a_k > sol then
        sol ← Σ_{k=i}^{j} a_k
return sol
```

구간 $(i,j)$ 마다 합을 처음부터 다시 계산한다는 게 핵심 — 구간 하나 평가에 $O(n)$, 구간 수가 $O(n^2)$개이므로 전체 $O(n^3)$이 되는 구조.

## 3. Alg 2 — Alg 1을 명시적인 3중 루프로 재작성

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

**Theorem 1.** Alg 2 runs in $O(n^3)$ time.

*Proof.* 기본 연산 수는
$$\sum_{i=1}^{n} \sum_{j=i}^{n} (j-i+1)$$
에 비례한다. $i' = j-i+1$로 치환하면 $\sum_{i=1}^n \sum_{i'=1}^{n-i+1} i'$가 되고, 이를 정리하면
$$\frac{n(n+1)(n+2)}{6} = \Theta(n^3).$$

**포인트**: Alg 2는 Alg 1을 "다시 쓴" 것일 뿐 알고리즘적으로 다른 게 없다 — 루프를 명시적으로 풀어 썼다고 복잡도가 바뀌지 않는다는 것을 보여주기 위한 대조군. 진짜 개선은 Alg 3에서 나온다.

## 4. Alg 3 — 누적합(prefix-sum) 재귀로 $O(n^2)$

핵심 아이디어: $j$를 하나씩 늘릴 때 구간 합을 처음부터 다시 더하지 않고, 직전 구간 합에 원소 하나만 더한다.

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

**Theorem 2.** Alg 3 runs in $O(n^2)$ time. (이중 루프뿐이므로 자명 — 판서에는 별도 증명 없이 명시만 되어 있음.)

**Theorem 3.** Alg 3 is correct.

*Proof.* 종료성은 Theorem 2에서 따라온다. 알고리즘이 반환하는 값은
$$\max\big(\{\,\mathrm{sum}[i,j] \mid 1 \le i \le j \le n\,\} \cup \{0\}\big)$$
이므로, 다음 Claim만 보이면 충분하다.

**Claim 1.** 모든 $1 \le i \le j \le n$에 대해 $\mathrm{sum}[i,j] = \sum_{k=i}^{j} a_k$.

*Proof (induction on $j-i$).*
- **Base case** ($j-i=0$): $\mathrm{sum}[i,i] = \mathrm{sum}[i,i-1] + a_i = 0 + a_i = \sum_{k=i}^{i} a_k$.
- **Induction step**: $j-i=\ell_0$에서 성립한다고 가정. $j-i=\ell_0+1$일 때,
$$\mathrm{sum}[i,j] = \mathrm{sum}[i,j-1] + a_j = \Big(\sum_{k=i}^{j-1} a_k\Big) + a_j = \sum_{k=i}^{j} a_k. \qquad \blacksquare$$

## 5. 이번 주 배운 것 요약

세 알고리즘이 같은 문제를 푸는데 복잡도가 다른 이유는 **"이전 계산 결과를 재사용하는가"**에 있다. Alg 1/2는 구간마다 합을 처음부터 다시 계산해서 $O(n^3)$, Alg 3는 구간 합을 이전 구간 합 + 원소 하나로 점화식화해서 $O(n^2)$. 이 패턴(구간 합의 증분 계산)은 이후 나올 더 빠른 $O(n)$ Kadane's algorithm으로 가는 중간 단계로 보인다(칠판에는 아직 등장하지 않음).

정확성 증명은 "알고리즘이 반환하는 집합이 실제로 원하는 집합과 같다"는 것을 먼저 재정의하고, 그 안의 각 원소($\mathrm{sum}[i,j]$)가 정의($\sum a_k$)와 일치함을 귀납법으로 보이는 표준적인 2단 구조(termination + 반환값이 올바른 집합의 max임 → 그 집합의 각 원소가 실제로 맞는 값임을 귀납법으로).

## 6. 수업 중 퀴즈 (무기명, 채점 안 됨)

같은 시간에 나눠준 퀴즈(`quiz-01.jpeg`, CSI 3108 Fall 2026 표기) — 본 주차 알고리즘 내용과는 별개로 증명 기법(귀납법·모순법, 비둘기집 원리) 연습:

**(1)** $a_1,\dots,a_n \in \mathbb{Q}$ ($n \ge 2$)이고 $a_1 < a_n$이면, $a_i < a_{i+1}$인 $i \in \{1,\dots,n-1\}$이 존재함을 증명하라.
- 학생 풀이 시작 부분만 판서/필기에 남아 있음: "그런 $i$가 존재하지 않는다고 가정하면 (귀류법/대우법으로 진행하려던 것으로 보임)" — 이후 전개는 기록되지 않음. (대우: 모든 $i$에서 $a_i \ge a_{i+1}$이면 수열이 비증가이므로 $a_1 \ge a_n$, $a_1 < a_n$과 모순.)

**(2)** 정점이 2개 이상인 모든 simple graph에는 차수(degree)가 같은 서로 다른 두 정점이 반드시 존재함을 증명하라.
- 답안 기록 없음. (표준 풀이: $n$개 정점의 차수는 $\{0,\dots,n-1\}$ 중 하나인데, 차수 0인 정점과 차수 $n-1$인 정점은 동시에 존재할 수 없으므로 실제 가능한 차수값은 $n-1$개뿐 — 비둘기집 원리로 두 정점이 같은 차수를 가짐.)
