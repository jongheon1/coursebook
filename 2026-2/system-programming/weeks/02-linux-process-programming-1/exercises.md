# Week 02 — Exercises (Exam Style)

All questions in English, as in the real exam. Total: 100 points. Kernel version references are Linux v6.12 unless stated otherwise.

---

**Q1. (6 pts, short answer)**
A process has two threads. Thread A has `pid = 700, tgid = 700` and thread B has `pid = 701, tgid = 700`. What do `getpid()` and `gettid()` return when called from thread B? Which kernel functions implement these two syscalls' return values?

<details><summary>Model answer</summary>

From thread B: `getpid()` returns **700** (the tgid), `gettid()` returns **701** (the task's own pid). In `kernel/sys.c`, `getpid` returns `task_tgid_vnr(current)` and `gettid` returns `task_pid_vnr(current)`. The POSIX "process ID" is the thread group ID in kernel terms.
</details>

---

**Q2. (10 pts, essay)**
Explain why modern x86 kernels moved `thread_info` from the bottom of the kernel stack into `task_struct` itself (`CONFIG_THREAD_INFO_IN_TASK`), and describe how the `current` macro is implemented after this change. Name one additional stack-related hardening feature that this change enabled or complemented.

<details><summary>Model answer</summary>

Old layout: `thread_info` lived at the low end of the kernel stack, and `current` was computed by masking the stack pointer with `~(THREAD_SIZE-1)` and dereferencing `thread_info->task`. Problems: (1) a kernel stack overflow corrupts `thread_info` first — the kernel's own identity data — making overflows both dangerous and exploitable; (2) it ties `current` to the physical stack layout.

With `CONFIG_THREAD_INFO_IN_TASK` (x86 since 4.9), `thread_info` became the **first member of `task_struct`**, reduced to low-level flags (`TIF_*`, `syscall_work`). `current` is now a **per-CPU variable read**: on v6.12 x86, `get_current()` returns `this_cpu_read_stable(pcpu_hot.current_task)` (`arch/x86/include/asm/current.h`), updated at context switch. The hot per-CPU fields (`current_task`, `preempt_count`, ...) are packed into one 64-byte cache line (`struct pcpu_hot`).

Complementary hardening: `CONFIG_VMAP_STACK` — the kernel stack is allocated in vmalloc space with guard pages, so an overflow faults immediately instead of silently corrupting adjacent data.
</details>

---

**Q3. (8 pts, short answer)**
For each of the following, give the exact task state (macro name) the kernel would report, and the corresponding `ps` state letter:
(a) a task waiting for terminal input, wakeable by signals;
(b) a task in a short disk I/O wait that must not be disturbed by any signal;
(c) a task that has called `exit()` but whose parent has not called `wait()`;
(d) a task stopped by SIGSTOP.

<details><summary>Model answer</summary>

(a) `TASK_INTERRUPTIBLE` — `S`.
(b) `TASK_UNINTERRUPTIBLE` — `D`.
(c) `exit_state = EXIT_ZOMBIE` — `Z` (note: this is in `exit_state`, not `__state`).
(d) `__TASK_STOPPED` — `T`.
</details>

---

**Q4. (10 pts, essay)**
The kernel enforces the following in `copy_process()` (v6.12 `kernel/fork.c`):

```c
if ((clone_flags & CLONE_THREAD) && !(clone_flags & CLONE_SIGHAND))
    return ERR_PTR(-EINVAL);
if ((clone_flags & CLONE_SIGHAND) && !(clone_flags & CLONE_VM))
    return ERR_PTR(-EINVAL);
```

State the implication chain these checks enforce and justify **each** implication semantically (why would the alternative be meaningless or unsound?).

<details><summary>Model answer</summary>

Chain: **CLONE_THREAD ⇒ CLONE_SIGHAND ⇒ CLONE_VM**.

- *CLONE_THREAD ⇒ CLONE_SIGHAND*: POSIX defines signal dispositions as process-wide; all threads of a group must observe the same handler table. A thread group whose members had private handler tables would break the process-wide signal semantics that `CLONE_THREAD` promises (shared pending signals, one visible "process").
- *CLONE_SIGHAND ⇒ CLONE_VM*: a signal handler is a **function pointer into the user address space**. Sharing a handler table between tasks with different address spaces is meaningless — the same address would point to different (or no) code in each task. Sharing handlers is only coherent if the address space is shared too. (The comment in fork.c adds that blocking this case also simplifies other kernel code.)
</details>

---

**Q5. (12 pts, essay)**
Describe the copy-on-write mechanism of `fork()` at the page-table level: what exactly does `copy_page_range()` do to parent and child PTEs for a private writable mapping, what happens on the first subsequent write by either side, and which functions handle that event? Also explain the `vma_needs_copy()` optimization.

<details><summary>Model answer</summary>

During `dup_mmap()` → `copy_page_range()` (`mm/memory.c`), for each present PTE in a COW-able mapping (`is_cow_mapping()`: private and potentially writable): the parent's PTE is write-protected in place (`ptep_set_wrprotect`), the copy inserted into the child is also write-protected (`pte_wrprotect`), both PTEs point to the **same physical page**, and the page's refcount/mapcount is raised. No data pages are copied.

On the first write by either task: the CPU raises a **page fault** (write to a write-protected page). The fault handler sees that the VMA permits writes but the PTE does not ⇒ COW fault ⇒ `do_wp_page()`. If the faulting task is the sole user of the page, the PTE is simply made writable again (reuse). Otherwise `wp_page_copy()` allocates a new page, copies the contents, maps the new page writable in the faulting task, and drops a reference on the original. The faulting instruction is restarted; user space observes only a minor fault.

`vma_needs_copy()`: for a VMA with no anonymous pages (typical file-backed mappings, e.g., program text), no userfaultfd-wp, and no PFN/mixed map, `copy_page_range()` skips copying the page tables entirely — the child can repopulate them lazily from the page cache via normal faults.
</details>

---

**Q6. (10 pts, calculation)**
A parent process has an RSS of 1 GiB in 4 KiB pages. Assume: memory copy bandwidth 20 GB/s, PTE size 8 bytes, page-fault overhead $t_f = 1\ \mu s$ per fault (excluding the copy itself).

(a) Estimate the data volume copied by an *eager* (pre-COW) fork and the time it takes.
(b) Estimate the PTE data volume a COW fork copies.
(c) The child then writes to 5% of the pages. Estimate the total deferred COW cost (faults + copies).
(d) At what fraction of written pages does COW stop being cheaper than eager copy? Comment qualitatively.

<details><summary>Model answer</summary>

Pages: $N = 1\,\text{GiB} / 4\,\text{KiB} = 262{,}144$.

(a) Eager: copies 1 GiB ⇒ $1\,\text{GiB} / 20\,\text{GB/s} \approx 54\ \text{ms}$ (plus 1 GiB extra memory immediately).

(b) COW: $262{,}144 \times 8\,\text{B} = 2\,\text{MiB}$ of PTEs (plus ~512 page-table pages), i.e. copy time on the order of 0.1 ms — roughly 500× less data than eager.

(c) $W = 0.05N = 13{,}107$ pages. Fault overhead: $13{,}107 \times 1\,\mu s \approx 13.1\ \text{ms}$. Copy volume: $13{,}107 \times 4\,\text{KiB} = 51.2\,\text{MiB}$ ⇒ $\approx 2.7\ \text{ms}$. Total ≈ **16 ms**, still well under the 54 ms eager cost, and memory overhead is only 51 MiB.

(d) Break-even: $W (t_f + t_{copy}) \approx N \cdot t_{copy}$. Per page $t_{copy} = 4\,\text{KiB}/20\,\text{GB/s} \approx 0.2\,\mu s$, so $W \cdot 1.2\,\mu s = N \cdot 0.2\,\mu s \Rightarrow W/N \approx 17\%$. Beyond roughly one-sixth of pages written, the per-page fault overhead makes COW *slower* than one bulk eager copy. COW is a bet that most children (e.g., fork-then-exec) touch few pages; write-heavy children (and the parent, whose pages are also write-protected) pay latency spread across many faults.
</details>

---

**Q7. (8 pts, short answer)**
`fork()` returns 0 in the child and the child's pid in the parent — yet `copy_process()` runs entirely in the parent's context. Explain the exact mechanism (function and field) by which the child observes a return value of 0, and how the parent obtains the child's pid.

<details><summary>Model answer</summary>

In the arch-specific `copy_thread()` (x86: `arch/x86/kernel/process.c`), the child's saved user-register frame is initialized from the parent's (`*childregs = *current_pt_regs()`) and then the child's saved `%rax` is overwritten: `childregs->ax = 0;`. When the scheduler first runs the child, it resumes at the syscall-return path and pops this frame — so the syscall "returns" 0 in the child. The parent simply takes the normal return value of `kernel_clone()`, which computes the child's pid via `get_task_pid()` / `pid_vnr()` after `copy_process()` succeeds.
</details>

---

**Q8. (10 pts, essay)**
Explain why all kernel threads are children of `kthreadd` (PID 2) rather than being cloned directly by whatever task calls `kthread_create()`. Describe the creation protocol (list, wakeup, two-step start) as implemented in `kernel/kthread.c`, and state two properties that distinguish a kernel thread's `task_struct` from a normal process's.

<details><summary>Model answer</summary>

If kernel threads were cloned directly in the caller's context, they would inherit the caller's attributes — namespaces, cgroup, signal state, rlimits — producing kernel threads with inconsistent, possibly user-controlled inherited state. Instead `kthread_create()` only queues a request (`kthread_create_info`) on `kthread_create_list` and wakes `kthreadd_task`. The `kthreadd()` loop (PID 2) dequeues requests and performs the actual `kernel_thread()` clone, so every kernel thread inherits from the same clean ancestor.

Two-step start: the new thread runs the common trampoline `kthread()`, which puts itself into `TASK_UNINTERRUPTIBLE` sleep before running the payload. The creator can then configure it (e.g., `kthread_bind()` to a CPU) and must call `wake_up_process()` to start it (`kthread_run` = create + wake).

Distinguishing properties: `p->flags & PF_KTHREAD` is set, and `p->mm == NULL` — a kernel thread has no user address space and borrows the previous task's `active_mm` (lazy TLB).
</details>

---

**Q9. (10 pts, essay)**
"Zombie processes are a kernel memory leak." Argue against this statement precisely: what does a zombie still hold, what has already been freed and when, which mechanism finally frees the rest, and in which case does the kernel skip the zombie state entirely?

<details><summary>Model answer</summary>

At `do_exit()`, the dying task releases its major resources **before** becoming a zombie: `exit_mm`, `exit_files`, `exit_fs`, etc. free the address space and fd table. `exit_notify()` then sets `exit_state = EXIT_ZOMBIE` and signals the parent (SIGCHLD). What remains is only a stub: the `task_struct` (a few KiB) and the `struct pid` — the kernel stack is gone too, freed by `put_task_stack()` in `finish_task_switch()` at the task's final context switch (`TASK_DEAD`), before the zombie is ever observed. The stub is deliberately retained because the parent has a right (and obligation) to collect the exit status and rusage via `wait()`. It is a contract, not a leak; the practical hazard of mass zombies is **pid exhaustion**, not memory.

Final teardown: the parent's `wait4()` → `do_wait()` → `wait_task_zombie()` copies the status out and calls `release_task()`, which unhashes the pid, unlinks the task from all lists, and (after an RCU grace period) frees the task_struct.

Skip case (autoreap): if the parent has set SIGCHLD to `SIG_IGN` or used `SA_NOCLDWAIT`, `exit_notify()` skips the zombie state (`exit_state = EXIT_DEAD`) and calls `release_task()` immediately. Orphans are reparented (subreaper or pid-namespace init), and init always reaps — so zombies never outlive their reaper.
</details>

---

**Q10. (8 pts, design)**
You must implement a "process snapshot" feature à la Redis BGSAVE: a 10 GiB in-memory database forks a child that serializes memory to disk while the parent keeps serving writes. Using this week's material: (a) why is fork the right primitive here? (b) identify two performance/memory failure modes of this design under a write-heavy parent, with the mechanism behind each.

<details><summary>Model answer</summary>

(a) Fork gives the child a **consistent point-in-time snapshot for free**: COW freezes the logical content of the shared pages at fork time. The child reads the old pages; any parent write after the fork copies the page privately first, so the child's view never changes. No application-level locking of the whole dataset is needed.

(b) Failure modes:
1. **Latency spikes in the parent**: at fork, all of the parent's writable pages are write-protected (`copy_page_range`), so every first write to each page after fork takes a COW page fault (`do_wp_page` → `wp_page_copy`) — trap + 4 KiB copy per page. Also the fork itself must copy page tables for 10 GiB (~20 MiB of PTEs), a noticeable pause.
2. **Memory blow-up**: every page the parent dirties during the snapshot gets duplicated. Worst case (parent rewrites everything before the child finishes), memory usage approaches 2× (20 GiB), potentially triggering the OOM killer. Mitigations: write throttling, incremental snapshotting, or `MADV_DONTFORK`-style exclusion of regions.
</details>

---

**Q11. (8 pts, short answer + essay)**
During `execve()` of an ELF binary: (a) name the struct that carries the new program's loading context; (b) which function is the documented "point of no return", and what two irreversible things happen at that stage? (c) Why must exec kill all other threads of the group (`de_thread`)?

<details><summary>Model answer</summary>

(a) `struct linux_binprm` (`fs/exec.c`), built by `do_execveat_common()` and passed through `search_binary_handler()` to `load_elf_binary()`.

(b) `begin_new_exec()` — the comment in `fs/exec.c` marks it as the point of no return. Irreversible steps: `de_thread()` destroys all other threads of the group, and `exec_mmap()` replaces the old `mm_struct` with the new one — after which the old program image no longer exists, so any later failure cannot return `-errno` to the old program; the task can only be killed (SIGSEGV).

(c) POSIX requires that after exec the process consists of a single thread executing the new image. Other threads reference the old address space, old handlers, old TLS — none of which survive; letting them run across the mm swap would be memory-unsafe, so they are terminated and the exec'ing thread (taking over group leadership if needed) becomes the only one.
</details>

---

**Q12. (bonus 5 pts, short answer)**
Give the CLONE flag set glibc's `pthread_create()` passes to `clone()`, and explain for any **two** of the flags what user-visible behavior would break if that flag were omitted.

<details><summary>Model answer</summary>

`CLONE_VM | CLONE_FS | CLONE_FILES | CLONE_SIGHAND | CLONE_THREAD | CLONE_SYSVSEM | CLONE_SETTLS | CLONE_PARENT_SETTID | CLONE_CHILD_CLEARTID` (documented in clone(2)).

Examples: without `CLONE_VM`, the "thread" would get a COW copy of the address space — writes to globals would not be visible across threads, breaking the shared-memory model. Without `CLONE_THREAD`, the new task would get its own tgid — `getpid()` would differ between threads, signals sent to the process would not be delivered group-wide, and the "thread" would appear as a separate process needing its own `wait()`. Without `CLONE_FILES`, an fd opened in one thread would not exist in another. Without `CLONE_CHILD_CLEARTID`, `pthread_join()` would not be woken via the tid futex when the thread exits.
</details>
