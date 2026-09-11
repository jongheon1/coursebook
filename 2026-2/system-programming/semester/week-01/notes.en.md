# Week 01 Lecture Notes — Introduction to Linux (Orientation)

> Source: lecture-audio STT from 2026-09-02 + lecture slides (`L00-courseIntroduction.pdf`, `_private/2026-2/system-programming/week-01/`). Instructor: Seonghoon Park — explicitly mentioned that this is **his own first lecture**, having just joined the university this semester.

## 1. Logistics

- **Instructor**: Seonghoon Park. Newly joined Yonsei this semester; stated that this is his first lecture as a professor (mentioned being nervous but excited).
- **TA**: Gunjoong Kim — a PhD student. Questions about assignments, attendance, etc. should go to the TA's email.
- **Attendance**: electronic attendance via the Y-Attend app. Today was just a test run. Attendance is 10% on the syllabus, but he said he won't deduct much for missing one or two classes (with a nuance that it's fine to skip for things like the Yonsei-Korea rivalry games) — however, he stressed that **the two-thirds attendance requirement is university policy, not his own**, and must be followed.
- **Grading**: midterm + final exams, two programming assignments (possibly three, "probably two"). (Exact weight percentages were not stated in this orientation lecture — needs to be cross-checked against the existing figures in `syllabus.md`.)
- **AI policy**: can't be prohibited outright, but he strongly recommends attempting assignments on your own first and only consulting AI when stuck. Explained that "the trial-and-error process itself is what builds understanding of the kernel's internal principles."
- **Textbook**: does not recommend buying the official textbook (Bovet & Cesati, *Understanding the Linux Kernel*), since it's over a decade old and covers outdated Linux versions. Recommends the up-to-date slides plus the real, current kernel source (a website) instead. Said it's fine to use AI to help understand the slides.

## 2. Nature of the Course — "System Programming" in Name, Linux Kernel Programming in Substance

- The course's goal is the practical side of OS kernel programming, specifically the **Linux kernel**. Recommends taking the Operating Systems course first if you haven't — the key difference is that the OS course is theory-focused and barely touches real Linux code, while this course covers **real code**.
- What you'll learn: how the kernel works internally, how to customize the kernel. Assignments take the form of modifying the kernel or writing kernel modules.
- Emphasis: understanding Linux isn't limited to kernel/systems programming — it's the foundation for building higher-level applications and AI systems too. "You need to know how the OS works to properly build the things on top of it."
- Why Linux: free and open (no cost), a mature OS developed over roughly 30 years. Stressed that it's everywhere — smartphones, watches, appliances ("Linux is everywhere").

## 3. This Semester's Overview (curriculum as described verbally)

Similar in outline to a regular OS course, but the difference is that it's grounded in **real Linux code** rather than theory. Topics to be covered: Linux processes, scheduling, system calls, (kernel) synchronization, memory management, file systems, and so on.

## 4. Smartphone OS Ecosystem Context (used as motivation for the intro)

- Smartphone OSes: Android, iPhone, and (in the past) Symbian, Windows 10 Mobile, webOS, BlackBerry, Tizen, etc. — most are **Linux-based** (free + well-maintained). webOS (LG) and Tizen (Samsung) have been pushed out of smartphones but are now used in home appliances like TVs and refrigerators.
- Android/Tizen stacks: distinguishes the kernel (low-level — CPU scheduling, memory management, file systems) from the framework (high-level — the application layer). Both stacks have the Linux kernel at the very bottom. Mentioned the career relevance — you might end up working on this layer at companies like LG, Samsung, or Google.

## 5. Introduction to the Instructor's Own Research (Mobile AI and Systems Lab)

- Lab name: **Mobile AI and Systems Lab**. Vision: providing users with advanced mobile experiences such as real-time scene understanding for AR and immersive, interactive 3D content (via XR devices like the Meta Quest).
- Technical challenges: vision foundation models, vision-language models, LLMs, NeRF (Neural Radiance Field), 3D Gaussian Splatting, etc. are all extremely compute-heavy. The goal is to run these heavy workloads **in real time on resource-constrained mobile devices** — which are far slower than server-grade GPUs and also face battery and thermal constraints.
- Optimization strategies: distributing work across a smartphone AP's NPU/CPU/GPU, controlling operating frequency (DVFS), fine-grained GPU-NPU scheduling. Combined with AI-side techniques (static model configuration, dynamic neural architectures like multi-exit/stitchable networks, scalable scene representations). **The core message of this introduction is that all of this optimization ultimately requires a deep understanding of OS/Android internals** — his own answer to why we need to learn the kernel.
- Explicitly stated that the details of scheduling and memory management are "graduate/PhD level rather than undergraduate," so they won't be covered in this lecture. Mentioned that interested students are welcome to reach out about internships or PhD positions (lab recruiting).

## 6. Closing

Wrapped up the course overview and took questions. Noted that week 1 allows free withdrawal from the course, and that everyone will be marked present for the first week.

---

# Day 2 (2026-09-05) — Linux Kernel Versioning & Introduction to Processes

> Source: 2026-09-05 lecture-audio STT (whisper-1) + lecture slides `L01-linuxprocesses.pdf` (`_private/2026-2/system-programming/week-01/`). The opening part of this lecture (§7) had no corresponding slides — it was delivered purely verbally, so it's reconstructed from the transcript alone. From §8 onward it maps to `L01-linuxprocesses.pdf`. **This lecture covered only roughly the first 40 of the deck's 87 slides (through the introduction of the process list) — the pidhash table's internal details, Task Lists Big Picture, Wait Queues, Process Usage Limits, the mechanics of process switching (the `switch_to` assembly walkthrough), Kernel Threads, Process 0/1, and Destroying Processes were all NOT covered and were explicitly deferred to the following Wednesday. This note does not speculate about that later material.**

## 7. Linux Kernel Versioning (opening segment, no slides provided)

- **History and usage**: Linux was released around 1995 (verbatim from the lecture — "I was born in 1994, so Linux is kind of my friend"). Desktop/laptop share is only around 2%, but Linux dominates servers, smartphones, edge devices, and home appliances; smartphones now account for roughly 70% of all computing devices.
- **As an open-source project**: the license imposes almost no constraints — anyone can read the code, use the kernel, or even try building their own OS. About 33 years old, very mature and well-maintained, with major companies (Intel, Samsung, Google) among its many contributors.
- **Written in C**: most people don't enjoy programming in C, but Linux is, in the professor's view, the best example for learning to program in C — one reason this course exists.
- **License**: GPLv2 — free to modify and distribute, commercial use allowed too, with conditions (disclose source, include copyright notice — "but I don't think this is a big deal").
- **Scale of growth**: grown to about 40 million lines, still growing roughly 400,000 lines every two months, with about 2,000 developers contributing per release.
- **Release versioning model**: RC (release candidate, experimental) → mainline (every 2–3 months, decided by Linus Torvalds) → stable (bug fixes on top of mainline, `major.minor.stable`) → **LTS** (long-term support — the most stable, used by real products like Chrome OS, Android, Windows, Amazon Linux; released roughly every 1–2 years with an extended maintenance window, some maintained up to six years). LTS matters because products care far more about a verified, tested kernel than about new features.
- **kernel.org**: the site to always check the latest mainline/stable/RC versions. At lecture time (Sept 2026), it showed mainline 7.2, stable 7.2.2, and RC 7.3-RC1 (the professor noted the slide's date was stale and corrected it live). Latest LTS is 6.18 (released last November); LTS releases tend to land around October–December each year.
- **Real-world products**: Android is the most widely used LTS-based product; Ubuntu, Chrome OS, WSL, Raspberry Pi, and Amazon Linux are also LTS-based. You can't swap kernels on a smartphone, but you can on something like Amazon Linux or Ubuntu.
- **Android common kernel**: Android has its own kernel, but it's based on the LTS Linux kernel — continuous merges flow from LTS into the Android mainline kernel, and from that mainline, version-specific Android kernels and OS releases are developed (the Android kernel branching model).
- This intro material is explicitly not exam material. He then transitioned: "now this is the real lecture, and it's exam material" — moving into Linux Processes.

## 8. Kernel Outlook (kernel-level components)

- User Level (user programs: browsers, shells, terminals, etc.) → System Call Interface → Kernel Level's managers:
  - **Filesystem Manager** (Ext2fs, proc, nfs) — reading/writing files from storage
  - **Process Manager** (Task Management, Scheduler, Signaling) — the professor called this, along with the memory manager, probably the most important component
  - **Memory Manager** — mapping virtual memory to physical memory
  - **Network Manager** (IPv6, ethernet), **Device Manager** (block, character) — connected to each other via a buffer cache
- The whole-semester goal is to work down through these to the HW Level (CPU, GPU, memory, storage, keyboard/mouse, etc.).

## 9. Linux Cross Reference (LXR) — elixir.bootlin.com

- A website for browsing and searching Linux kernel source from the earliest version to the latest. Searching any variable, macro, or function shows exactly where it's defined and where it's referenced/used.
- Because core concepts stay the same even as details change, buying the textbook isn't recommended (though it's still worth reading) — this site is a very convenient source of information. Expected to be used very frequently once assignments are given (assignment details not yet finalized).

## 10. Opening Question — Is Kernel Code Itself a Process?

- "Kernel code functions the same way an ordinary program does, since a processor executes it, and it frequently relinquishes control and depends on the processor to return control to it." So is kernel code a process? If so, how is it controlled?
- The answer ("a process is an instance of a running program") can be confusing right now — promised to revisit it later (§13).

## 11. Two Models for Running an OS — Process-Based vs. Execution Within User Process

- **Process-based OS**: OS functions run as separate processes alongside user processes. Switching between processes (a full process switch) is like walking out of one building and into another — costly overhead (the professor's building/apartment analogy).
- **Execution within user process** (the model Linux chose): OS functions run inside the user process's own context — more like going upstairs or downstairs within the same building, which is more efficient.
- **The cost**: from the user's perspective, part of the address space must be given up to the kernel. In a 32-bit system, the virtual address space is 4GB total; under a process-based OS, the user process could use all 4GB, but under execution-within-user-process, 3GB goes to the user process and 1GB to the kernel — every process gives up 25% of its address space. Analogy: the kernel/OS is the landlord who owns the building, and user programs are tenants who must follow the landlord's rules.
- **The payoff**: this design avoids the costly full context switch when the OS only needs to do kernel-related work, doing a much cheaper **mode switch** within the same process instead — the model's key advantage ("virtually all OS code gets executed within the context of a user process").
- Re-emphasized after the break: benefit = low mode-switch overhead / downside = from the user's perspective, part of the address space (1GB) simply can't be used — explicitly flagged as important enough to repeat.

## 12. Dual-Mode Operation — User Mode / Kernel Mode

- Modern CPUs provide hardware support for distinguishing at least two modes (user/kernel). (Some architectures support more levels than this, but that's very architecture-specific and out of scope for this course — only these two modes matter here.)
- **User mode**: executes on behalf of the user, with no permission to touch kernel-level things like physical memory or files directly.
- **Kernel mode**: executes on behalf of the OS, with complete control over the processor, instructions, registers, and memory — this separation exists precisely because letting user programs directly control the CPU would be very unsafe.
- Concrete example (PowerPoint): while it's just running normally, that's user mode; when you click, type, or hit a runtime error, that's something the user program can't handle itself, and a mode switch happens. A full process switch (the scheduler picking an entirely different process) only happens when actually needed — the design's big advantage.

## 13. Three Events That Trigger a Mode Switch

1. **Hardware interrupt**: keyboard input, a network packet arriving, etc. — the user program can't handle these itself.
2. **Software interrupt (exception)**: runtime errors like divide-by-zero (severe) or a page fault (accessing memory not mapped to physical memory) — again not something the user program can handle, nor something it wants to see.
3. **System call**: something the user program actively wants to do — reading a file (e.g., PowerPoint opening your .ppt file), creating a process (fork — since most modern programs are multi-process), or network communication (sockets/TCP-IP, handled by the network manager).
- **Worked example — printf → write syscall**: a user-mode program calls the C library's `printf()`, which internally calls the `write()` system-call interface. Invoking this system call switches the mode to kernel — kernel code begins there, and the kernel communicates with the real hardware (e.g., the monitor), producing the output you see on screen.
- (A short break followed around 3:15.)

## 14. What Is a Process?

- Textbook definition: "a process is an instance of a running program." The professor noted this can be confusing these days, since multi-process and multi-threaded programs are common.
- A phrase he actually asked ChatGPT to help redefine: **"a process is a running instance with its own virtual address space and resources."** He liked this because it foregrounds that a process owns its own virtual address space and its own resources.
- What a process includes: **images** (code, data, stack, heap — stored in virtual memory) + **process context**:
  - **Program context**: data registers, program counter (PC), stack pointer (SP)
  - **Kernel context**: PID, GID, SID, VM structures, open files, signal-related information

## 15. Process Image Layout — Code/Data/Stack/Heap

- Code area and data area: data splits into **initialized**/**uninitialized** depending on how it's written in source — e.g., `int i;` (no assignment, uninitialized) vs. `int i = 1;` (initialized).
- **Heap**: for dynamic memory allocation (malloc-style), grows upward. **Stack**: automatic/temporary variables, return addresses, caller environment (ordinary C variables), grows downward.
- **Worked example (a real C program)**: a global array (fixed size 100, so lands in the uninitialized data area even though not dynamically allocated), a global `bufsize` variable (initialized data area), the `main()`/`f1()` function code (text area, read line by line by the OS), a `malloc(bufsize)` call inside `f1()` (goes to the heap), and local variables `i`/`buf` inside `main()` (stored on the stack). Summary: globals → data area, locals → stack, code → code area, malloc-style results → heap.
- **The init process (process 1) example**: the very first process started when Linux boots. It has its own user stack, data structures, heap, and code, and part of its kernel-side data structures are saved in kernel address space.

## 16. Limitations of the Process Model → Why Threads Are Needed

1. **Cooperating processes problem**: imagine there's no thread concept at all (as in the early days) — many applications need to handle multiple tasks at once, but plain processes don't share address space or resources with each other, which is very inefficient.
2. **Multiprocessing problem**: a traditional process runs on only one CPU core at a time — so even with multiple cores available, the plain multi-process model alone can't exploit that hardware.

## 17. Process vs. Thread — What Gets Shared

- Traditional view: **process = process context + (code, data, stack)**. With threads: each thread has its own logical control flow (obviously), but **code, data, and kernel context are shared**, and only the **state (specifically, the stack) is per-thread**. So the process/thread distinction ultimately comes down to what is shared.
- Concretely: a process owns its own virtual memory and resources (stack/heap/data/code/kernel context). If a process has multiple threads, those threads share heap, data, and code, and the only thing each fully owns is its own stack. Plain processes without threads have a parent-child-sibling hierarchy but share nothing at all — each has completely separate code/data/context/stack.
- **Creation**: a process is created via a system call like `fork()`; a thread is created via the standard **pthread** API. pthread is just an interface/API — the real implementation is up to library developers (only inputs/outputs are specified) — today, most multi-threaded applications are written using the pthread library (e.g., `pthread_create()`).
- **Communication cost**: separate processes need **IPC** (inter-process communication) to talk to each other, which has real overhead; threads share code/data directly, so no IPC is needed — part of why Linux adopted the thread concept.
- **Synchronization**: multi-process is safer since each process has a fully separate address space, but threads share memory and data structures, so one thread can do something to a shared resource that another thread doesn't want — a real problem. That's exactly why the pthread API defines synchronization mechanisms like **mutexes** and **condition variables**.

## 18. Process States

- **General (textbook) model**: **new** (being created, temporary/one-time) → **ready** (ready to be scheduled, hasn't gotten the chance yet) → **running** (the scheduler picked it to run on a real CPU — modern schedulers give fair, short time slices before returning it to ready) → **exit** (finished). Plus **blocked**: waiting for a specific event (network, keyboard, elapsed time, etc.) — neither running nor ready to be scheduled (e.g., a program sleeping for 10 seconds).
- **Linux's implementation** (updated in recent kernels, in the professor's brief framing): `TASK_RUNNING` covers both ready and running. Blocked processes are `TASK_INTERRUPTIBLE` or `TASK_UNINTERRUPTIBLE` (both waiting for some event, becoming schedulable again once it occurs). `TASK_STOPPED` was briefly mentioned here as roughly corresponding to an exit-like state (the fuller `exit_state` breakdown was not covered).

## 19. task_struct / thread_info — the Process Control Block (PCB)

- `sched.h` is the key file defining data structures for processes and the CPU scheduler. **task_struct** = the data structure representing a Linux process, i.e., the **PCB (process control block)** — holding task information, the task image (code/data/stack/heap), and program context.
- In Linux, a process is called a **task**, and a thread is also a task — task is the unit the CPU scheduler works with. (Noted the terminology mix: "process" from a textbook perspective vs. "task" from a Linux perspective.)
- Version comparison: task_struct was short in Linux 2.6.11, but as fields kept getting added it's grown to nearly 1,000 lines in recent versions (the basic idea remains similar). **task_struct is architecture-independent**, while **thread_info is architecture-dependent** (Intel, ARM, etc. each design their own) because it's closely tied to the actual CPU. Shown side by side for ARM vs. x86 in the recent LTS as well.
- Every process needs its own process descriptor because the kernel must identify and manage every process, and every task/context needs its own descriptor to store this information (process context, code, data, etc.).

## 20. User Stack / Kernel Stack

- Dual-mode operation means the kernel needs its own stack too — running kernel code requires somewhere to store local variables, and that's the **kernel stack**.
- On entering kernel mode (a mode switch), the task's registers (stack pointer, instruction pointer, etc.) are saved onto the kernel stack — so the kernel knows exactly where the program was when it eventually returns to user mode. Local variables of kernel functions are also stored there during kernel execution.
- The small kernel memory area allocated per process (which used to hold both thread_info and the kernel stack, but **nowadays only holds the kernel stack since thread_info is no longer stored there**, 8KB in size). Every user process needs two stacks (user and kernel); the kernel stack lives in the kernel data segment, and stack switching happens at mode-switch time.

## 21. Identifying the "Current" Process — Old vs. Modern Approach

- Why the kernel needs to identify the current process: once kernel mode finishes, the system must return to user mode, and the kernel needs to know exactly which process that was.
- **Linux 2.6.11**: a complicated approach — assembly-level stack-pointer masking to derive the current process from information at the base of the kernel stack.
- **Modern approach**: each CPU/core maintains its own data structure with a direct pointer to its currently running task — the CPU directly knows what the current task is (shown via architecture-dependent code from Linux 6.18.48).

## 22. The Process List

- The Linux kernel runs many processes at once (the professor guessed "maybe a thousand or so"), so it needs an efficient way to manage them.
- **Doubly linked list**: each task_struct has prev/next pointers, starting from `init_task`, with other processes linked in. The kernel provides macros to insert, remove, and scan this list — e.g., `for_each_task` (follows the next-task pointer repeatedly to visit every process).
- **The limitation, and why pidhash exists (left unfinished)**: using only the linked-list traversal to find a specific PID (say, PID 1000) directly would mean scanning sequentially from the first task up to 1,000 times — very time-wasting. "That's why the Linux kernel also maintains a hash table" (pidhash) — right after saying this, with time running short (4:46), the lecture ended. **The actual structure and lookup mechanics of pidhash were not covered in this lecture and were explicitly deferred to the following Wednesday ("process list and related things"). This note does not speculate about that content.**

---

## Day 3 (2026-09-09) — Process Organization, Process Switching, Threads

> Source: the same slide deck (`L01-linuxprocesses.pdf`), continuing past slide 42. A brief recap of process/thread definitions, `task_struct`, and process states opened the session.

### 23. Managing the Process List — Linked List + Hash Table

- Two data structures the kernel uses to manage processes: a **linked list** (for full traversal/insertion/removal, via macros like `for_each_task`) and a **hash table** (for fast PID lookup — picking up exactly where last session's pidhash teaser left off, since list-only lookup is a slow sequential scan).
- **Relationships among processes**: parent (a single pointer — each process has exactly one), children (a linked list — can be multiple), and siblings (also a linked list) maintain the hierarchy.

### 24. Run Queues and Wait Queues

- From the CPU's perspective, a process is either **runnable (ready/running)** or **blocked**. Two structures manage this:
  - **Run queue**: what the CPU scheduler traverses to pick the next process to run. Each CPU/core has its own run queue, which internally keeps separate lists per scheduling algorithm (CFS, RT, DL, etc.).
  - **Wait queue**: the set of blocked (task interruptible/uninterruptible) processes sleeping while waiting on some hardware/device/timer event. When that event occurs, the device driver or kernel subsystem wakes the process and moves it back to the run queue.
- (In passing) the OS also assigns per-process resource usage limits (max CPU time, file size, heap/stack size, etc.) — mentioned briefly as "not that important."

### 25. Process Switching — the Four Triggering Events

Task switching happens in four cases:
1. A process puts itself to sleep (runnable → blocked).
2. A process terminates.
3. A process is about to return to user mode from a system call, but isn't the most eligible process to run next (some other runnable process may have higher priority or lower virtual runtime — there's no reason for the kernel to insist on resuming the original one).
4. A process is about to return to user mode after the kernel finishes handling an interrupt, and again isn't the most eligible candidate (essentially the same logic as case 3).
- When any of these four happen, the kernel decides whether to context-switch, saves the previous process's (prev's) context, schedules the next process (next), and restores its context.

### 26. Hardware Context, `thread_struct`, and the `switch_to` Macro

- In Linux, both processes and threads are called "tasks" (the scheduling unit), so **"task switching" (context switching)** is the more accurate term than "process switching."
- **Hardware context**: the register values (stack pointer, instruction pointer, etc.) the CPU needs to resume a process — these must be reloaded into the CPU registers to resume execution.
- The hardware context is **split across two locations**: part of it lives in **`thread_struct`** inside the process descriptor (`task_struct`) — the architecture-dependent part (e.g., EIP/ESP) — and the rest lives on the **kernel-mode stack**. `task_struct` itself is architecture-independent (maintained by core kernel code), but CPU-register-related information is architecture-specific, which is exactly why it's split out into its own structure (`thread_struct`).
- Context switching has two steps: **(1) switching the kernel-mode stack**, and **(2) switching the hardware context** — handled by the Linux kernel's **`switch_to` macro**, written in assembly for performance (recent kernels are moving parts of the codebase to Rust, but this very low-level code stays in assembly).
- **Step-by-step walkthrough of `switch_to`**:
  1. Save a few register values (flags, EBP, etc.) onto the previous process's (prev's) kernel-mode stack.
  2. Save prev's stack pointer into prev's `thread_struct` — **the stack pointer itself cannot be saved on the kernel stack** (since that value is exactly what identifies where the kernel stack is — saving it inside the stack would lose track of the stack's location, which is precisely why part of the context goes to the stack and part goes to a separate global structure).
  3. Load next's stack pointer from next's `thread_struct` into the CPU register — at this point the kernel can identify next's kernel-stack area.
  4. The rest (notably the instruction pointer, which marks how far the process has progressed) is handled by the `__switch_to` macro, restored last.
  - Once these steps finish, the CPU registers point to the next process's state, completing the switch.

### 27. Threads — Why They Were Introduced

- **Traditional model (no threads)**: resource ownership (virtual address space, process context) and execution were bundled into a single process — one process = resources + exactly one thread of execution.
- **Modern model (with threads)**: resources and execution are separated — multiple threads share resources (address space, file handles, etc.) while each keeps its own execution flow (stack, context).
- **Motivation**: exploiting parallelism inside an application without threads meant spawning a separate process for every part that needed to run in parallel — but processes share no address space or resources at all, making this inefficient and clumsy. Threads solve this by sharing a common context (code/data) while each thread keeps its own stack and execution context.
- Threads are (like processes) a **unit of scheduling**; from the Linux kernel's perspective, both processes and threads are just "tasks" — the distinction is purely a matter of how much they share.
- **Two implementation approaches**:
  - **User-level threads**: (e.g., a custom Python/Java thread library) the kernel has no awareness of them at all — from the kernel's point of view it's still a single process (single thread). Problem: the kernel can't schedule them.
  - **Kernel-level threads**: the kernel directly recognizes threads as a scheduling unit — the more realistic approach, in the professor's assessment. **Linux uses kernel-level threads.**
- At 3:47, with time running short, the lecture wrapped up here, with the remaining time given to questions.

---

## Day 4 (2026-09-11) — Kernel Implementation of Threads, Process Destruction, Intro to Process Scheduling

> Source: two lecture recordings back to back this session. The first half wraps up the existing slide deck (`L01-linuxprocesses.pdf`) — lightweight processes (clone/do_fork), kernel threads, process 0/1, process destruction. The second half moves to a new deck (`L02-processscheduling.pdf`, announced as freshly uploaded right before class) and starts process scheduling. The session opened with a brief recap of last time's (9/9) list/hash, run queue/wait queue, the four process-switching events, and thread_struct/switch_to.

### 28. Lightweight Processes — Why Threads Weren't Given a Separate Data Structure

- **Motivation**: relying purely on multiple processes for parallelism inside an application is inefficient — processes share no data with each other, so exchanging information requires **IPC**, which is difficult to use and inefficient. This is exactly why kernel developers wanted a thread feature, which is why Linux ended up with threads.
- **Restating the practical difference between the two implementation approaches**: a user-level thread is invisible to the kernel entirely — it's built purely at the user level (e.g., one big while loop with if-branches dispatching different pieces of work). The problem: if one user-level thread blocks on I/O, the kernel — which sees the whole program as a single thread — cannot schedule the remaining threads either. A kernel-level thread is directly recognized and managed by the kernel, so every thread is individually schedulable — if one blocks on I/O, the rest keep running. This difference is decisive, and **Linux chose kernel-level threads**.
- **Design decision (Linus Torvalds)**: one option would have been to introduce an entirely new data structure/class/functions for threads, separate from processes. Instead, **Linus Torvalds decided against extending the kernel with a separate thread implementation** and instead let processes share resources. In other words, **there is no separate data structure for processes and threads — a single data structure (task_struct) implements both**. At creation time, the parent can specify what resources to share with the child, and depending on that configuration the child ends up being a "process" or a "thread."
- **Why "lightweight process"**: this is why a thread can also be called a **lightweight process** — because some resources are shared, it doesn't need the full set of resources/data structures a regular process has, which is what makes it "lightweight."
- **Thread group**: lightweight processes are organized into thread groups. The first process in a group (the leader) is the **thread group leader**, and its PID becomes the **thread group ID (TGID)**. Processes in the same group can be called "threads"; processes with different TGIDs share nothing. **Example (Firefox)**: modern web browsers are multi-process, multi-threaded — running Firefox gives you one process with multiple threads inside it, and those threads share the same TGID, which is exactly the lightweight-process mechanism showing they're threads.

### 29. `clone()` — the Wrapper Function and Its Path to do_fork

- `clone()` is a **wrapper function defined in the C library**, used to create a new process or a new thread (process and thread creation are essentially the same mechanism under the hood). Parameters: the function to run when the new process starts, plus state/flags/an argument for that function.
- **Key point**: calling `clone()` lets you decide, via flags, **how much kernel context to share**. Things threads typically share: virtual address space, filesystem information, open file descriptors. If the new child is set to share these with the parent, it becomes a **thread**; if not, it becomes a **process**. So whether something is a process or a thread comes down to **the degree of sharing**. (There's also a flag for signal-related settings, but that one is for processes, not threads.)
- **Flow**: a user program calls `clone()` → internally invokes a system call in user address space → being a system call, a mode switch occurs → in kernel mode, a `do_fork()`-family kernel function is called.
- The **`CLONE_VFORK`** flag was explicitly named — related to the `vfork()` system call (see #29 for context, and #31 for how do_fork handles it).

### 30. Less Lightweight Processes — Copy-on-Write in `fork()`, and `vfork()`

- Separate from the lightweight-process (thread) concept, Linux also has a mechanism to save resources when creating **ordinary processes** — called a **less lightweight process**. The purpose is efficiency: kernel developers didn't want to waste resources every time a new process or thread is created.
- **`fork()` and Copy-on-Write (COW)**: when `fork()` creates a child, the child gets its own virtual address space, but there's no need to immediately copy all of the parent's code/data/stack into physical memory — at creation time, parent and child can simply **refer to the same physical pages**. If the child only reads that data, physical memory never changes, so there's no reason to copy anything. But the moment **either the parent or the child tries to write** to that area, the kernel copies the page into a new physical page. This "copy only when a write happens" scheme is **Copy-on-Write (COW)**.
- **`vfork()`**: used when the parent intends to call `fork()` immediately followed by `exec()`. Two cases: (1) the parent only calls `fork()` — then parent and child keep running the same program, so distinguishing their data matters; (2) the parent goes on to call `exec()` — the child ends up running an entirely new program. `vfork()` targets case (2): until `exec()` is called, parent and child can share the same memory address, since there's no reason to copy parent-related data before the new program even starts (the child is about to become a completely different program, so the parent's data is useless to it anyway). When `vfork()` is called, **the parent's execution blocks** — it waits until the child either exits or execs a new program.
- Both `fork()` and `vfork()` end up implemented through **the same kernel function** (originally introduced to implement lightweight processes, i.e., threads) — nowadays that same function is reused by fork/vfork to configure the degree of sharing between parent and child. The professor's summary point: **the highlight here is that Linux implements threads elegantly** — a thread is ultimately just a process that shares kernel context.

### 31. The `do_fork()` Function — Step by Step

`do_fork()` is the kernel function that actually handles process creation:
1. Allocates a **new process ID (PID)** for the child.
2. Calls **`copy_process()`** to copy the parent's process descriptor (`task_struct`) for the child — copying is needed because parent and child may share some of this data. This also sets up a new `thread_struct` and a **new kernel-mode stack** (since every thread/process needs its own kernel-mode stack).
3. Checks whether the user has exceeded their allowed number of processes — a safety limit against the system accumulating too many processes. In practice this rarely triggers, but it's a **safety net** against, e.g., malware trying to crash the system by spawning huge numbers of processes.
4. Copies file descriptors, page tables, and other process/program/kernel-context-related items.
5. Sets the child's state to **`TASK_RUNNING`** (runnable/ready).
6. **Sets up the parent-child relationship and the thread-group relationship** — each `task_struct` carries pointers to its parent, siblings, and children, so this hierarchy is wired up at creation time.
7. Once initialization is done, inserts the new process descriptor into one of the **run queues** (there can be multiple, since there are multiple CPUs and each CPU may keep several run queues).
8. If **`CLONE_VFORK`** is specified: since `vfork()` assumes the child will soon be replaced by a new program, the parent is placed on the **wait queue**. Only after the child starts its new program does the parent go back onto the run queue.
9. Once this is done, `do_fork()` **returns the child's PID** and terminates.

### 32. Kernel Threads — Not to Be Confused with "Kernel-Level Threads"

- Every process discussed so far has been an ordinary user process — Firefox, PowerPoint, a reader app. But the kernel (the OS itself) also has time-consuming background work to do — flushing disk caches, swapping out unused page frames — and it needs threads of its own to do this. These are **kernel threads**.
- **A terminology warning the professor stressed explicitly**: **kernel thread** and **kernel-level thread** are completely different concepts. Kernel-level threads (covered in #28–#31) are one of the two implementation approaches for threads, and they're about **threads belonging to an ordinary user program**. The kernel threads being discussed now have nothing to do with any user program at all — they **carry out actual kernel functions themselves**.
- Kernel threads are also implemented as lightweight processes — they have their own process descriptor and are schedulable. What's different from a regular process: they have **no ordinary user mode**. A kernel thread runs only in kernel mode and has no user-mode address space. It shares the kernel address space and other kernel data structures (filesystems, file descriptors, etc.) with other kernel threads.
- **Regular process vs. kernel thread**: a regular process executes kernel functions **only through system calls** (a brief aside on this: when a user program needs OS help — via a system call or a hardware interrupt — it switches to kernel mode; a system call handles kernel work "on behalf of" that user program, whereas an interrupt isn't for any particular user program but is very urgent and handled very briefly). A kernel thread, in contrast, **directly executes a single, specific kernel C function** — typically a long-running kernel task like swapping or cache flushing, unrelated to any user process.

### 33. Kernel Thread vs. Regular Process — the `mm` Field and Virtual Address Space

- **Address space difference**: on x86, the total virtual address space is 4GB — 3GB for user mode, 1GB for kernel mode. A regular process moves between user mode and kernel mode, so it uses the full 4GB, but a kernel thread has no user mode, so it **only uses linear addresses above `PAGE_OFFSET`** (i.e., only the 1GB kernel-mode region).
- (A point of possible confusion, addressed directly) OS code and data structures are not copied per process — **every process shares the OS's own data structures and code**. So each process's "kernel-mode area" is virtually linked to the actual OS rather than each process holding its own private copy of the OS.
- **How to tell them apart (via `task_struct` fields)**: `task_struct` has fields including `mm` and `thread`. The `thread` field (type `thread_struct`) is used for context switching and stores hardware-dependent info like the stack pointer. The `mm` field describes the **virtual address space (the user-mode area)** — code, data, stack. **If a task's `mm` is a null pointer, that task is a kernel thread** — because kernel threads have no user-mode area. This is the practical way to distinguish a regular process from a kernel thread.

### 34. Process 0 (swapper) and Process 1 (init) — the Two Special Kernel Threads

- A typical system has many kernel threads; two representative, special ones are **Process 0** and **Process 1**.
- **Process 0 = "swapper"**: the **ancestor of all processes**. Created during Linux's initial boot phase by the `start_kernel()` function. Its job: initializes some of the data structures the kernel needs, enables kernel features like interrupts, and creates another kernel thread — the **init process**. After creating init, swapper runs `cpu_idle()`, repeatedly executing the HLT instruction — meaning that when this process is "running" on a CPU, that CPU is actually in the **idle state**. The scheduler picks process 0 (swapper) **only when there is no other process in the `TASK_RUNNING` state** — i.e., only during genuine idle time. On multi-CPU systems, **each CPU has its own swapper process**, since each CPU can go idle independently.
- **Process 1 = "init"**: created by swapper via the `init` function. Completes the rest of kernel initialization — for example, spawning other kernel threads (e.g., `bdflush` and similar) that handle things like memory cache swapping. **init never terminates** — it keeps creating and monitoring the activity of all processes, so it's always running and is a very important kernel thread in Linux.

### 35. Process Destruction — Two Stages: Termination and Removal

- There are two ways to **trigger** termination: the process calls **`exit()`** itself, or it receives a **signal** (e.g., from a terminal `kill` command), which the kernel handles by terminating that process. Regardless of how it's triggered, though, **destruction itself always happens in two stages**: **(1) process termination** and **(2) process removal** — genuinely distinct stages.
- **Stage 1 — termination via `exit()`**: the kernel removes **most (not all)** references to the terminating process from kernel data structures — its virtual-address-space (`mm`) references, open files, filesystem references, signal-handling references. It also updates parent/child/sibling relationships since this process is going away. At this point the process becomes a **zombie**.
- **Orphan processes (mentioned in passing)**: if the terminating process still has children (rare in practice — normally a parent waits for its children to finish before terminating itself), those children lose their parent and are **reassigned as children of the init process** — called **orphan processes**. (Don't confuse this with a zombie: the zombie is the terminating process itself, not its children.)
- **What a zombie is**: at this stage some of the process's data has already been removed, so it's effectively terminated already, but it hasn't fully disappeared yet — hence "zombie," dead but still alive in a sense. This zombie stage is usually very short and the zombie is cleaned up quickly.
- After this stage, the kernel calls **`schedule()`** to pick the next process to run (since the CPU now needs a new process). But the zombie is still technically "alive," so it eventually has to be removed — it can cause problems otherwise — which is what stage 2 is for.
- **The key rule**: **Unix kernels are not allowed to discard a process's data right after it terminates**, because the parent may still need information about the terminated child (e.g., its exit status). Stage 2 only proceeds once the parent has issued a **`wait()`-style system call** referring to this zombie.
- **Stage 2 — removal, via `release_task()`**: the OS releases the zombie's process descriptor (`task_struct`) — now assumed no longer needed. It also releases the **8KB kernel-mode memory area** allocated per process (the same area holding the kernel stack, discussed in #20). Once both of these — the `task_struct` and the 8KB kernel-mode area — are released, the process is **fully destroyed**.

### 36. Process Scheduling — Goals and Principles

- **Motivation**: many processes want the CPU at once, but CPU time can't all go to one process — the rest would never get a chance to run. Efficiently distributing CPU time across processes is therefore a central OS topic.
- **The principle of scheduling**: multiple processes appear to run "simultaneously" by switching from one process to another. The scheduler has to decide two things: **when to switch**, and **which process to pick**. Many algorithms/approaches exist, and kernel developers must settle on (one or a few) scheduling policy.
- **Scheduling goals (reconciling conflicting objectives)**: fast process response time, throughput for background jobs, avoiding process starvation, and balancing the needs of low- vs. high-priority processes. In the end, the goal is to **give a fair opportunity to multiple processes**.

### 37. Classifying Processes — I/O-Bound/CPU-Bound, and Linux's Interactive/Batch/Real-Time Scheme

- **Traditional classification**: **I/O-bound** (heavy I/O device use — e.g., database applications sending lots of I/O requests) vs. **CPU-bound** (needs a lot of CPU time — e.g., compiling a program or an OS). The professor's anecdote: compiling a full Linux kernel on his laptop used to take 3–4 hours; modern laptops are faster now.
- A single process alternates between a **CPU burst** (executing instructions) and an **I/O burst** (waiting on I/O). If CPU bursts dominate, it's CPU-bound; if I/O bursts dominate, it's I/O-bound. (Example shown: one process with a long CPU burst is CPU-bound; another, with a short CPU burst, is I/O-bound.)
- **Linux's own classification (a different scheme)**: **interactive**, **batch**, and **real-time**.
  - **Interactive**: spends a lot of time waiting for keyboard/mouse I/O, and must **respond quickly** once input arrives — target delay is roughly **50–150ms** (the professor noted gamers might feel even that's too slow).
  - **Batch**: runs in the background and consumes a lot of CPU — compilers, database search engines, scientific computation, and (as mentioned) AI-related workloads. The scheduler **penalizes** these because they hold the CPU too long.
  - **Real-time**: has exact deadlines — video/audio applications, robot controllers like drones. Must meet deadlines, must never be blocked by lower-priority processes, and must be highly responsive.
  - The scheduler penalizes batch processes and instead **favors interactive processes**, to give users a responsive experience.

### 38. Linux Scheduling Principles — Preemptive Scheduling and Time Quantum

- The scheduler has to decide **when and how** to pick the next process to run.
- **Preemptive scheduling**: Linux uses preemptive scheduling — even if the currently running task still has time slice remaining, the scheduler can **preempt** it in favor of another task judged more suitable (e.g., higher priority).
- **Multiple scheduling policies**: Linux supports several scheduling policies, implemented via **scheduling classes** — the actual scheduling behavior depends on which scheduling class a task belongs to.
- Normal tasks — interactive and batch — get CPU time distributed according to **task weight**, and **nice values** determine that weight (details promised for a later lecture). The kernel distributes CPU time in units called **time quantum** (= time slice) to each process/task; once a process uses up its time slice, it can't run again **until all other processes have also used up theirs**.
- **Two ways preemption happens (per the state diagram)**: `TASK_RUNNING` covers both ready and running; `TASK_INTERRUPTIBLE`/`TASK_UNINTERRUPTIBLE` represent the blocked state.
  1. When a running process's **time quantum expires**, it gives up the CPU and returns to the ready state.
  2. When a blocked process on the wait queue **becomes runnable (ready)** and its priority is higher than the currently running process, the kernel **preempts** the current process and the scheduler picks the next process to run.

### 39. The Scheduler's Evolution — O(1) → CFS → EEVDF

- The Linux scheduler has evolved considerably. Around 2001 (the professor's phrasing: "right after the World Cup in South Korea"), the **O(1) scheduler** was introduced — quite outdated by today's standards. The reason to study it now is to understand why **CFS (Completely Fair Scheduler)** was later adopted.
- Evolution order: **O(1) scheduler → CFS → EEVDF** (the newest). EEVDF is an **extension of CFS**, and the professor calls CFS "almost the best answer" for Linux scheduling.
- The O(1) scheduler was introduced (by someone the professor believes was at Red Hat) to fix performance problems in the earlier scheduler — the general pattern being that a new scheduler always shows up to solve the previous one's problems. O(1) is a **priority-based time-sharing** scheme, but it has limitations, which is why it was eventually replaced by CFS.
- Why schedulers keep getting updated: new applications and computing devices keep appearing — e.g., today's need to handle **AI-serving/LLM workloads** and **resource-constrained devices like mobile**, which is part of what drives newer schedulers like EEVDF.

### 40. The O(1) Scheduler — Three Policies, 140 Priority Levels, and the Runqueue

- The O(1) scheduler defines **three scheduling policies**: **`SCHED_FIFO`** (first-in-first-out — the same idea as FCFS from a general OS course), **`SCHED_RR`** (round-robin), and **`SCHED_OTHER`** (for general processes).
- `SCHED_FIFO` and `SCHED_RR` are **for real-time processes only** (a rare, specialized use case) — usable **only in supervisor mode**, meaning ordinary user processes cannot use them directly. The difference between the two comes down to **time quantum**: `SCHED_FIFO` specifies no time quantum, so a process can hold the CPU until it terminates itself (forever, if it wants); `SCHED_RR` has a time quantum, so the process must give up the CPU once it expires.
- The rest of the general processes run under `SCHED_OTHER`-style O(1) scheduling, where the kernel **implicitly favors I/O-bound processes over CPU-bound ones** to give interactive applications good response time (games/typing need low delay; compilers don't need this as much).
- **Priority scheme**: there are **140 priority levels**, and **a smaller number means a higher priority** (a counterintuitive rule the professor noted even confused him mid-lecture). **0–99** are reserved for real-time tasks (supervisor mode only, scheduled via `SCHED_FIFO`/`SCHED_RR`). **100–139** (40 levels) are for normal tasks — and within this range too, smaller numbers still mean higher priority.
- **Runqueue structure**: each CPU has its own run queue, and in the O(1) scheduler, each CPU's run queue is made up of **140 lists, one per priority level**. It's called "O(1)" because the scheduler only needs to check the **single highest-priority non-empty list** to pick the next task — constant time, versus older schedulers that had to scan every list/task to find the highest-priority one. The runqueue data structure has two arrays plus two pointers, **`active`** and **`expired`** (mechanics covered in #42).

### 41. `SCHED_FIFO` and `SCHED_RR` Behavior, Worked Through an Example

- **`SCHED_FIFO`**: the **highest-priority** runnable task gets the CPU and keeps it until one of three things happens:
  1. **A higher-priority task becomes runnable** — the current task is preempted, but the preempted task goes to the **front, not the back**, of its own priority queue (going to the back would be unfair among same-priority peers — FIFO semantics still require the original order to be respected within a priority level). Once the higher-priority task later gives up the CPU, the preempted task resumes and can run as long as it likes.
  2. **The current task blocks itself** (e.g., waiting for I/O) — it voluntarily leaves the queue and, once runnable again, is enqueued at the **back**.
  3. **The current task voluntarily yields the CPU** by calling a specific function — necessary because a `SCHED_FIFO` task would otherwise run forever if it never yielded; this also sends it to the **back** of the queue.
  - Barring these three events, a running `SCHED_FIFO` task keeps the CPU forever. Newly runnable tasks are always added to the back of the queue, and among same-priority tasks, the one at the front of the queue gets the CPU.
- **Example**: four real-time processes — D (highest priority), B and C (lower than D, and equal to each other), and A (lowest of the four). Under `SCHED_FIFO`, the schedule is simply **D → B → C → A** (each runs to completion before moving to the front of the next occupied priority queue).
- **`SCHED_RR`**: identical to `SCHED_FIFO` except that **each process also gets a time slice**. When B's time slice expires, it's preempted and sent to the back of its priority queue, and C runs next; once B and C have each had a turn, the cycle repeats — so the resulting order becomes **D → B → C → B → C → A**. (**The key point: time-sharing only happens among processes of the same priority** — across different priority levels, the higher priority still always wins, which is why A only runs last, after D/B/C are all done.)
- Both policies apply only to real-time processes running in supervisor mode; normal-class processes are only scheduled under the O(1) policy **when no real-time process is runnable at all**.

### 42. Active/Expired Queues — the Trick Behind O(1) Complexity

- The kernel keeps two kinds of per-priority queues: **`active`** and **`expired`**. A process that hasn't used up its full time slice stays on the **active** queue; once its time slice is fully consumed, it's moved to the **expired** queue.
- Scheduling always happens **from the active queue only** (tasks on the expired queue have no time slice left, so there's no reason to pick them). Processes on the active queue get moved to expired one by one as their slices run out, until eventually the active queue is completely empty and every task sits on the expired queue.
- **At that point, all the kernel does is swap the pointers**: there are really only two arrays, and `active`/`expired` are just pointers to whichever array is currently playing which role. So the moment every task's time slice is used up, the kernel simply **swaps which pointer points to which array**, and every task effectively gets a fresh time slice at once — no need to individually move each task to a new queue, which is a very elegant implementation.
- The lecture wrapped up here for time, with process scheduling (CFS and beyond) **explicitly deferred to the next lecture** — this note does not speculate about that content.
