# Week 5 — Exercises

Exam-style problems. Total: 100 points. Answers are in collapsible sections — attempt every part before revealing.

---

## Q1. L4 vs L7 load balancing (6 pts)

(a) State three concrete differences between L4 and L7 load balancing (information visible, unit of distribution, cost). (4 pts)
(b) Explain why per-request load balancing of HTTP/2 traffic is impossible at L4. (2 pts)

<details>
<summary>Model answer</summary>

(a)
- **Information visible**: L4 sees only IP addresses and TCP/UDP ports; L7 parses the application protocol (URL path, headers, cookies).
- **Unit of distribution**: L4 assigns whole **connections** to backends; L7 can route each **request** individually.
- **Cost**: L4 forwarding is cheap (kernel/hardware level, no payload parsing); L7 pays for full proxying and protocol parsing (and often TLS termination), so its throughput ceiling is lower.

(b) HTTP/2 multiplexes many requests over one long-lived TCP connection. An L4 balancer makes its decision once per connection and cannot see request boundaries inside the encrypted/streamed payload, so all requests on that connection are pinned to one backend. Only an L7 proxy, which terminates the protocol and sees individual streams/requests, can spread them across backends.
</details>

---

## Q2. Tail latency amplification (10 pts)

Each backend service has $p99 = 200$ ms (i.e., a call exceeds 200 ms with probability 1%). A user request fans out to $n$ backends **in parallel** and must wait for all of them. Assume independence.

(a) For $n = 50$, compute the fraction of user requests slower than 200 ms. (4 pts)
(b) Find the largest $n$ such that at most 10% of user requests are slower than 200 ms. (4 pts)
(c) Name one technique from Dean & Barroso's "The Tail at Scale" that mitigates this effect, and describe its mechanism in one sentence. (2 pts)

<details>
<summary>Model answer</summary>

(a) $P(\text{slow}) = 1 - 0.99^{50} = 1 - 0.605 \approx \mathbf{39.5\%}$.

(b) Require $1 - 0.99^n \le 0.1 \iff 0.99^n \ge 0.9 \iff n \le \frac{\ln 0.9}{\ln 0.99} = \frac{-0.1054}{-0.01005} \approx 10.48$. So $\mathbf{n = 10}$.

(c) **Hedged requests**: after waiting for, e.g., the p95 latency, send a duplicate of the outstanding request to a different replica and use whichever response arrives first — cutting the tail at a small cost in extra load. (Also acceptable: tied requests with cancellation.)
</details>

---

## Q3. Little's law (10 pts)

A stateless API service receives $\lambda = 2{,}000$ req/s in steady state. The mean residence time per request (including downstream DB waits) is $W = 150$ ms.

(a) How many requests are inside the service on average? (3 pts)
(b) The service uses a thread-per-request model with a pool of 240 threads. Is the pool sufficient? Justify numerically. (3 pts)
(c) A dependency slows down and $W$ rises to 400 ms while $\lambda$ stays at 2,000 req/s. What happens, quantitatively and qualitatively? (4 pts)

<details>
<summary>Model answer</summary>

(a) $L = \lambda W = 2000 \times 0.15 = \mathbf{300}$ concurrent requests.

(b) **No.** Sustaining $\lambda = 2000$ with $W = 150$ ms requires $L = 300$ threads on average, but only 240 exist. The maximum sustainable throughput is $\lambda_{max} = L/W = 240 / 0.15 = 1600$ req/s; the remaining 400 req/s queue up unboundedly (or must be rejected).

(c) Required concurrency becomes $L = 2000 \times 0.4 = \mathbf{800}$ — far above the pool. Requests queue in front of the pool; queueing time adds to $W$, which further inflates $L$: a positive feedback loop (congestion collapse) unless the service sheds load, times out, or applies backpressure. Little's law shows why a *latency* problem in a dependency becomes a *capacity* problem upstream.
</details>

---

## Q4. Consistent hashing (12 pts)

A cache cluster grows from 8 to 9 nodes. $K$ keys are uniformly hashed.

(a) Under naive `hash(key) mod N` placement, what expected fraction of keys changes owner? Under consistent hashing? Show the reasoning. (5 pts)
(b) Explain why a hash ring with **one point per node** produces poor load balance, and how virtual nodes fix it. Include the approximate scaling of the load imbalance with the number of vnodes $V$. (5 pts)
(c) State one cost of using a large number of virtual nodes. (2 pts)

<details>
<summary>Model answer</summary>

(a) **mod-N**: a key keeps its owner only if $h \bmod 8 = h \bmod 9$, which holds only for $h \bmod 72 \in [0,8)$ — probability $8/72 = 1/9$. So $1 - 1/9 = \mathbf{88.9\%}$ of keys move. **Consistent hashing**: the new node takes only the arc between itself and its predecessor — expected $K/9 \approx \mathbf{11.1\%}$ of keys move, and no key moves between two old nodes.

(b) With one point per node, the arc lengths between $N$ random points on the ring are highly variable (approximately exponentially distributed), so some nodes own several times the average share (lab measurement: max/mean ≈ 3.6 for 10 nodes). With $V$ vnodes, each node's load is the sum of $V$ independent arcs; by variance averaging the relative standard deviation of load shrinks roughly as $1/\sqrt{V}$.

(c) Ring metadata and lookup structure grow as $N \times V$ entries (more memory, slower membership changes/rebuilds); with data stores, more vnodes also fragment data movement into many small transfers.
</details>

---

## Q5. Cache write policies (8 pts)

For each requirement below, name the most appropriate write policy (write-through / write-back / write-around / cache-aside) and justify in one sentence:

(a) Write burst absorption is critical; losing a few seconds of recent writes on a crash is acceptable (e.g., view counters). (2 pts)
(b) Data written must never be lost, and subsequent reads of the just-written data must hit the cache. (2 pts)
(c) Large log-style writes that are almost never read back should not pollute the cache. (2 pts)
(d) Describe the "stale set" race condition in cache-aside and one mechanism that prevents it. (2 pts)

<details>
<summary>Model answer</summary>

(a) **Write-back**: writes are acknowledged at the cache and flushed asynchronously — highest write throughput, at the cost of losing unflushed writes if the cache node dies.

(b) **Write-through**: every write goes synchronously to both cache and store — durable on ack, and the cache is warm for read-after-write. Cost: write latency includes both systems.

(c) **Write-around**: writes go directly to the store, bypassing the cache, so rarely-read data does not evict hot entries.

(d) Stale set: reader A misses and reads value $v_1$ from the DB; writer B updates the DB to $v_2$ and invalidates the cache; A then sets the cache to the outdated $v_1$, which survives until TTL. Prevention: **leases** (memcache-style) — the cache issues a token on miss and rejects sets whose token was invalidated by an intervening delete — or compare-and-set with versions.
</details>

---

## Q6. Cache stampede (10 pts)

A single hot key ("front-page data", recomputation cost 800 ms) is read 5,000 times/sec through a cache with TTL 60 s.

(a) Describe precisely what happens at TTL expiry if no protection is in place, and why the origin DB may fail even though it normally serves this load easily. (4 pts)
(b) Explain the locking/lease defense and one drawback. (3 pts)
(c) Explain probabilistic early expiration (XFetch): give the recompute condition and explain why no coordination between clients is needed. (3 pts)

<details>
<summary>Model answer</summary>

(a) At expiry, all in-flight readers miss **simultaneously**: during the 800 ms recomputation window, up to $5000 \times 0.8 = 4000$ requests pile onto the origin, all performing the same expensive computation. The origin was sized for the cache-miss trickle (a few req/s), not for 4,000 concurrent heavy queries; it saturates, recomputations get slower, more requests arrive meanwhile — a positive feedback loop (congestion collapse), possibly cascading to other queries sharing the DB.

(b) Only the first missing request acquires a lock (or a lease token) and recomputes; others either wait or are served the stale value (stale-while-revalidate). Drawback: lock management adds complexity and a failure mode — if the lock holder dies, others are blocked until a timeout; waiting requests add latency.

(c) Each request, on hit, recomputes early if $\text{now} - \Delta \cdot \beta \cdot \ln(\text{rand}()) \ge \text{expiry}$, where $\Delta$ is the recomputation cost and $\text{rand} \in (0,1)$. The probability of early recomputation rises steeply as expiry approaches, so with high probability exactly one client refreshes before expiry. Each client uses only local information (expiry time, $\Delta$, a local random number), so no locks or shared state are required.
</details>

---

## Q7. Token bucket (10 pts)

A rate limiter uses a token bucket with refill rate $r = 5$ tokens/s and capacity $b = 10$. The bucket is full at $t = 0$. Requests arrive: 12 requests at $t=0$, 8 requests at $t=1$ s, 3 requests at $t=2$ s.

(a) How many requests are admitted / rejected at each arrival instant? Track bucket state. (6 pts)
(b) Give the tight upper bound on requests admitted in any interval of length $T$, and state what property of traffic this expresses. (2 pts)
(c) Contrast with a fixed window counter of "10 per 2 s": construct the boundary-burst anomaly. (2 pts)

<details>
<summary>Model answer</summary>

(a)
- $t=0$: bucket = 10 → **10 admitted, 2 rejected**, bucket = 0.
- $t=1$: refilled $5 \times 1 = 5$ tokens → bucket = 5 → **5 admitted, 3 rejected**, bucket = 0.
- $t=2$: refilled 5 → bucket = 5 → **3 admitted, 0 rejected**, bucket = 2.

(b) At most $b + rT = 10 + 5T$ requests in any window of length $T$: sustained rate is bounded by $r$, while bursts up to $b$ are tolerated — the burst allowance is an explicit design parameter.

(c) Fixed windows $[0,2), [2,4)$: send 10 requests at $t = 1.99$ and 10 at $t = 2.01$ — all 20 admitted within 20 ms, twice the intended rate, because the counter resets at the window boundary. A token bucket caps the same 20 ms at $b = 10$.
</details>

---

## Q8. Storage selection (12 pts)

For each workload, choose the best-fitting storage class (relational / key-value / document / wide-column / graph), justify with the data model **and** one engine-level consideration (indexing/storage engine/partitioning):

(a) Shopping-cart contents keyed by session id; millions of ops/sec; single-item lookups only. (3 pts)
(b) Double-entry financial ledger requiring multi-row ACID transactions and ad-hoc reporting by analysts. (3 pts)
(c) IoT sensor readings: 2 M appends/sec, queries are "last 24 h for device X" range scans. (3 pts)
(d) Fraud detection over accounts, devices, and cards, querying variable-depth relationship paths ("accounts within 4 hops sharing a device"). (3 pts)

<details>
<summary>Model answer</summary>

(a) **Key-value** (Redis/DynamoDB): access is strictly by primary key with no joins or scans; hash/consistent-hash partitioning scales horizontally with O(1) lookups.

(b) **Relational**: multi-row invariants (debits = credits) need ACID transactions; ad-hoc analyst queries need SQL and join flexibility; B-tree storage gives predictable point/range read latency for transactional access.

(c) **Wide-column** (Cassandra/HBase): model as partition key = device id, clustering key = timestamp — writes are sequential appends and the query is exactly one partition's time range. Engine-level: LSM-tree storage turns the massive write load into sequential I/O; range scans within a partition read contiguous SSTable data.

(d) **Graph** (Neo4j-class): the query is a variable-depth traversal, which in SQL becomes an unbounded number of self-joins; a graph store makes each hop a local adjacency access whose cost depends on the neighborhood size, not the total dataset size.
</details>

---

## Q9. Message queues and delivery semantics (12 pts)

(a) Define at-most-once, at-least-once, and exactly-once delivery in terms of what the sender does when an acknowledgment is not received. (3 pts)
(b) Explain why "exactly-once **delivery**" is unachievable in general between independent systems, and what Kafka's exactly-once semantics actually consists of. (4 pts)
(c) You must build a consumer that processes `PaymentRequested` messages (charging a card) from an at-least-once queue. Design the consumer so duplicates cause no double-charging. Be concrete. (5 pts)

<details>
<summary>Model answer</summary>

(a)
- **At-most-once**: never retry — an unacknowledged message may be lost, but is never duplicated.
- **At-least-once**: retry until acknowledged — never lost, but the receiver may see duplicates (the original may have been processed even though its ack was lost).
- **Exactly-once**: every message affects the receiver exactly once — no loss and no duplicate *effect*.

(b) The ack itself can be lost: after a timeout the sender cannot distinguish "message lost" from "message processed, ack lost". Retrying risks duplication, not retrying risks loss — with no shared atomic commit between the two sides, one of the two risks must be taken. Kafka's EOS is exactly-once **processing within Kafka**: an idempotent producer (producer id + per-partition sequence numbers let brokers discard duplicate appends) plus transactions that atomically commit output records and consumer offsets, with consumers reading `read_committed`. Side effects on external systems (e-mail, card networks) are outside this guarantee.

(c) Require an **idempotency key**: the producer stamps each message with a unique `payment_id`. The consumer, in one local DB transaction: (1) `INSERT` `payment_id` into a `processed_payments` table with a uniqueness constraint; (2) if the insert succeeds, execute the charge (or record the charge intent) and commit; (3) if the insert violates uniqueness, the message is a duplicate — ack it and skip. Because the dedup check and the effect commit atomically together, a crash between them re-delivers the message and repeats a not-yet-committed processing, while a committed one is filtered. If the charge itself calls an external PSP, pass the same `payment_id` as the PSP's idempotency key so the retry is deduplicated end-to-end.
</details>

---

## Q10. Diagnosing a cache that made things worse (10 pts)

A team put a Redis cache (cache-aside, TTL 300 s) in front of their product-catalog DB. Mean latency improved, but p99 **worsened**, and twice the DB fell over under load spikes that it previously survived.

(a) Give two distinct mechanisms consistent with these symptoms, referring to concepts from this chapter. (6 pts)
(b) State three criteria for deciding that a cache should be **removed** (or never added) from an architecture. (4 pts)

<details>
<summary>Model answer</summary>

(a) Any two of:
- **Cache stampede / synchronized expiry**: hot keys cached at deploy time expire together (fixed TTL, no jitter); at expiry, thousands of concurrent misses hit the DB simultaneously — a load spike the pre-cache DB never saw, because before the cache, load arrived smoothly instead of in synchronized bursts. This explains both the p99 spikes and the DB falling over. (Fix: jitter, locking/lease, probabilistic early expiration.)
- **Capacity re-sizing effect**: once the cache absorbed 95%+ of reads, the DB was (implicitly or explicitly) sized for the residual trickle — connection pools shrank, query plans went cold, buffer pool no longer holds the hot set. Any cache disruption (restart, eviction storm, stampede) now sends a load the DB is no longer provisioned for.
- **Miss-path latency addition**: on a miss the request pays cache lookup + DB read + cache set (extra round trips); p99 is dominated by the miss path, so mean improves while tail worsens, especially if Redis itself occasionally stalls.

(b) Remove/avoid a cache when: (1) the **hit rate is low** — access distribution is uniform or write-heavy, so the cache adds latency and machinery without absorbing load; (2) the data requires **strong read-after-write consistency** (balances, inventory) — staleness windows are contract violations, and invalidation correctness costs more than the cache saves; (3) the underlying problem is **fixable at the source** (missing index, N+1 queries) — the cache is masking debt while permanently adding an invalidation/stampede failure surface. (Also acceptable: operational cost/SPOF of the cache tier exceeds its benefit at current scale.)
</details>
