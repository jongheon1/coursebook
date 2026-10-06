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

## Day 5 (2026-09-18) — CFS, ULE, and EEVDF: Fairness and the EDF Connection

> Source: 2026-09-18 lecture-audio STT (from the `recap` project's result file, `2026-09-18-system-programming-1.json`, 88 paragraphs, ~75 minutes). **Note a full slide-deck swap**: `L02-processscheduling.pdf`, used in Day 4, was covered only through page 16 of 54 and is not picked back up from here — it's effectively superseded. This session doesn't continue L02's remaining pages; instead it opens a **separate, brand-new deck, `L03-processscheduling.pdf`** ("Lecture 03. Process Scheduling (2)"), starting fresh with a review of scheduler evolution. The first part of the session is Q&A and wrap-up on the O(1) scheduler from last time (`schedule()` invocation, limitations); the middle goes deep on CFS (weight/vruntime/red-black tree, a worked example, comparison with FreeBSD's ULE); the back half introduces the motivation for EEVDF and closes with an EDF worked example. **EEVDF's actual mechanics (lag/eligibility computation, etc.) were not covered this session and were explicitly deferred to next time** — this note does not speculate about that content.

### 43. O(1) Scheduler Wrap-Up Q&A — nice vs. Static/Dynamic Priority, Time-Slice Splitting on `fork()`

- **Question: how do nice value and static priority differ?** The nice value is **set by the user** — via the `nice` (or `setpriority`) system call in user mode. That system call doesn't directly change static priority — it changes the nice value first, and **the kernel then uses that nice value as input to finally update static priority**. So nice is what the user touches, and static priority is what the kernel's scheduler code actually uses — they refer to essentially the same thing, but at different layers.
- **There's a cap on how far a user can push the nice value**: the default nice value is the **maximum** value a user is allowed to set (i.e., the "nicest," lowest-priority value). Users can only move **toward nicer**, never the other way — a fairness constraint. (The name "nicer" comes from the fact that a lower priority means yielding more running opportunities to other tasks.)
- **Static priority and dynamic priority (`prio`) have separate roles**: static priority determines **the length of the time slice**. Dynamic priority is what the scheduler uses **when picking the next process to run** — a distinct role. The design rationale for dynamic priority is to favor I/O-bound/interactive processes over CPU-bound (batch) ones, and internally the kernel calls the adjustment value a **"bonus."** To tune this bonus, the kernel monitors/tracks each task's interactivity — e.g., its average wait time.
- **Relevant `task_struct` fields**: `static_prio` and `prio`. When the user changes the nice value, `static_prio` changes, and `static_prio` determines the time slice. After a task has run on the CPU for a while, the scheduler may adjust its priority based on monitored interactivity — that's `prio` (dynamic priority). When the scheduler picks the next task from the run queue, it picks the task with the **highest `prio`** (i.e., the smallest number).
- **Time-slice splitting on `fork()`**: every time a parent calls `fork()` to create a child, the kernel takes the parent's **remaining** time slice (say, 10) and **splits it in half**, giving 5 to the parent and 5 to the child. (The professor noted the slide's formula had a typo — the concept of "split it in half" matters more than the exact equation shown.) The design rationale: to **prevent a process from hoarding CPU resources by repeatedly forking off descendants** — without this split, repeated forking could let a process hold the CPU for far too long.

### 44. How `schedule()` Gets Invoked — Direct Invocation vs. Lazy Invocation

- `schedule()` is the scheduler's key function — it selects a new process from the run queue and assigns it the CPU. Ultimately it replaces the previous process's virtual address space with the new one's and carries out the **process switch** from the previous task to the next (mechanics covered in Day 3).
- There are four cases where scheduling becomes necessary:
  1. A running process moves from running (or runnable) to **blocked** (e.g., waiting on a timer or I/O event).
  2. The running task **exhausts its time slice** (timeout).
  3. A task with **higher priority than the currently running task becomes ready** — the current task must be preempted.
  4. The running process **terminates**.
- **Cases 1 and 4 require direct invocation** — the task is blocking or terminating right now, so the kernel has no other option. **Cases 2 and 3 use lazy invocation** — since the task can keep running a bit longer without urgency, the kernel just **sets a flag**, and at some later scheduling point it checks that flag and, if set, performs the scheduling.
- **Worked example**: process P1 calls a system call, moving from running/runnable to blocked (case 1, direct invocation) → P2 is selected to run on the CPU. At this point P1 becomes ready again (assume P1 has higher priority than P2) → this is case 3, requiring lazy invocation. So both direct and lazy invocation of `schedule()` are used in the Linux kernel to handle these different situations.

### 45. O(1) Scheduler Limitations (1) — Too Much Riding on One Priority Value, and the Unfair Priority Effect

- **Problem 1 — a single value (nice/priority) affects too many things at once**: priority (nice) affects both responsiveness and overhead simultaneously. A long time slice hurts responsiveness; shrinking the time slice via nice to improve responsiveness (e.g., ~5ms at nice19/priority139) causes more frequent context switches and thus more context-switch overhead. Responsiveness and overhead end up coupled through this one value — not a great design.
- **Problem 2 (the more important one) — the Unfair Priority Effect**: a one-level priority difference doesn't produce a **consistent CPU-share ratio**.
  - Example A: task1 priority=120, task2 priority=121 (difference of 1) → time slices of 100ms and 95ms respectively (actual difference 5ms) → as a ratio, task2 gets a **5% shorter** time slice.
  - Example B: task1 priority=138, task2 priority=139 (same difference of 1, actual difference still 5ms) → but now task2 gets a **50% shorter** time slice. (For this ratio to hold, task1 would be roughly 10ms and task2 roughly 5ms — consistent with the ~5ms minimum time slice near nice19/priority139 mentioned earlier.)
  - Conclusion: **the same one-level priority difference produces wildly different CPU-share ratios (5% to 50%)** — this is the core unfairness of the O(1) scheduler.

### 46. O(1) Scheduler Limitations (2) — Starvation and Perturbation in the Expired Array

- **Starvation**: one of the scheduler's core goals is preventing it — a task or process never getting the opportunity to run in time.
- **The starvation risk in the expired array**: the active↔expired pointer swap only happens once the active array has no active tasks left at all (see §42). But the developers, wanting to **improve interactive-process responsiveness**, allowed an interactive task whose time slice is fully exhausted — which by design should move to the expired array — to instead be **reinserted into the active array**, treating it almost like a real-time task. This can leave batch/CPU-bound processes with essentially no chance of ever running.
- **Perturbation**: this reinsertion practice actually delays the array swap and makes tasks sitting in the expired array wait far longer — a real problem. To mitigate it, O(1) introduced a lot of complex heuristics — e.g., using a task's **sleep-average history** to estimate its interactivity and adjust dynamic priority accordingly. Overall, the design and implementation weren't very clean.

### 47. Enter CFS (Completely Fair Scheduler) — Weight, Vruntime, Red-Black Tree

- **CFS (Completely Fair Scheduler)** emerged to fix O(1)'s unfairness — the goal, as the name says, is to be "completely fair." There's an inventor and someone who inspired the approach (the professor: "you don't need to remember the names"), but based on several research papers, Linux developers brought this algorithm into the kernel — a **significant departure** from the traditional Unix process scheduler.
- **CFS's goal**: guarantee every process its fair share of the CPU — fairness is everything. It also aims to improve on O(1)'s interactive performance.
- **CFS's three core pillars**:
  1. **Weight instead of priority** — there's no more priority concept at all; each task has its own **weight**.
  2. **Virtual runtime (vruntime)** — replaces dynamic priority, computed from weight.
  3. **Red-black tree (RB tree) as the data structure** — instead of O(1)'s simple array/list scheme (140 lists), CFS uses an RB tree, which looks more complex but is actually more efficient (covered below).

### 48. CFS's Fairness Model — the Weight Distribution Formula and the nice→weight Mapping

- **Basic idea**: aiming for an ideal multitasking system, CFS gives each task CPU time **proportional** to its weight. E.g., if the scheduler is distributing 100ms across T1 through Tn, each task gets (its own weight ÷ total weight) × 100ms.
- **nice → weight mapping**: the user input is still the nice value, but instead of mapping it to priority like O(1) did, CFS maps it to **weight**. The philosophy is to avoid the unfair priority effect from §45.
- **Design goal**: a one-level nice difference should always produce roughly a **10-percentage-point** CPU-usage difference. The baseline: **nice=0 → weight=1024** (the same default as O(1)). Two tasks with the same nice value split the CPU 50:50; if one task's nice is one level higher (one level lower priority), the difference is exactly 10 percentage points.
- This relationship **holds regardless of what the baseline nice value is** — unlike O(1), which depended on the specific base value of 120, CFS removes that dependency. That 10-percentage-point CPU-usage difference corresponds to roughly a **25% increase** in the actual weight value (e.g., 1024 → 1277 is about a 25% increase) — every adjacent pair of nice values in the table satisfies this same relationship.

### 49. Defining Vruntime and a Worked Example — Exam-Critical

- **What vruntime is, and the rule for using it**: CFS no longer has O(1)'s dynamic priority — vruntime is the key value used to pick the next process to run. Vruntime reflects how long a task has already run, and, accounting for its weight, how much longer it should still run.
  - **A smaller vruntime** means the task has received **less** CPU time than it should have → the scheduler should give it priority.
  - **A larger vruntime** means the task has received **more** CPU time than it should have → it gets less opportunity going forward.
  - **The scheduling decision = pick the task with the smallest vruntime.**
- **Worked example — stage 1 (baseline: equal weight)**: two tasks both have nice=0 (static priority=120), so they have **equal weight**. With a target latency period of 10ms, that 10ms splits evenly into time slices of **5ms and 5ms**. Their observed actual execution runtimes so far are **task1=40ms, task2=30ms**. Since weight is equal, the vruntime conversion factor is 1 — so **vruntime equals actual runtime**: 40ms and 30ms. (This stage just establishes that equal weight ⇒ vruntime = actual runtime.)
- **Worked example — stage 2 (extended to unequal weight)**: the same example is then extended — task1 stays at static priority **120** (nice0, baseline weight), but task2 becomes static priority **125** (nice5, a lighter weight than baseline) — a priority difference of 5. That weight ratio changes how the 10ms target latency splits into time slices: **task1=7.5ms, task2=2.5ms** (a 3:1 ratio — roughly matching the real CFS nice-to-weight table's nice0=1024 vs. nice5=335, a ratio of 1024/335≈3.06). The actual execution runtimes are kept the same: **task1=40ms, task2=30ms**.
  - Resulting vruntime: **task1=40ms** (baseline weight, conversion factor unchanged), **task2=9ms** (the value stated in lecture — different from its actual runtime of 30ms).
  - **⚠ Flagging a numeric inconsistency**: the professor immediately followed this by explaining that "this task ran more than it should have, so its virtual runtime is higher than expected" — which implies task2's vruntime should be **larger** than 30ms (the standard CFS formula gives 30×(1024/335)≈91.7ms). In other words, the stated figure of "9ms" doesn't match the explanation that follows it — a digit was plausibly dropped somewhere in speech or in the STT pipeline (e.g., "92" becoming "9"). This note preserves the number as actually stated in lecture (9ms) while flagging the inconsistency. **What's solid is the direction**: a task with a weight lighter than baseline (i.e., higher nice) accumulates vruntime faster relative to its actual runtime, gets treated as having "already received more than its fair share," and consequently gets less CPU opportunity going forward.
  - (Note: the lecture also stated, back to back, "if a task's weight is lighter than default, its vruntime increases more slowly" immediately followed by "if the weight is small, the vruntime increment grows larger" — two directly contradictory clauses. The direction adopted above — smaller weight ⇒ faster-growing vruntime — is the one consistent with standard CFS behavior and with the explanation that followed.)

### 50. CFS Time-Slice Computation and Scheduling Flow — Red-Black Tree, the Leftmost Node, Preemption Conditions

- **Time-slice computation**: CFS is still a preemptive, round-robin-like scheduler, so time slices still exist — `time_slice(task) = target_latency × (task_weight ÷ total weight)`. The kernel sets `target_latency` itself based on several factors (roughly 100–200ms; the exact rule was called unnecessary to memorize).
- **How to quickly find the smallest vruntime**: with O(1)-style arrays/lists, the kernel would have to scan everything each time — O(n). To cut this down, CFS introduces a **red-black tree** — insertion, deletion, and search are all **O(log n)**.
- **Run-queue structure**: Linux keeps a real-time run queue (100 priority levels, 100 doubly-linked lists — carried over from the O(1) era) separate from the CFS run queue (for normal tasks, **a single red-black tree**). Ordinary application tasks mostly live in the CFS run queue. CFS's RB tree is ordered by vruntime as the key, and the next task to run is the **leftmost node**.
- **Scheduling flow (on every scheduler tick — a general concept, not specific to CFS)**:
  1. On each scheduler tick, a timer interrupt fires, and the scheduler first checks **preemptibility**.
  2. It subtracts the elapsed tick period from the current task's time slice — if this drops to zero or below, it sets a flag (**condition A: time slice exhausted**).
  3. It updates the current task's vruntime — if the updated vruntime now exceeds the next task's (i.e., the leftmost node's) vruntime, it sets the flag (**condition B: this task has now run more than another task** — e.g., if the next task's vruntime is 50 and the current task's goes from 40 to 42, this condition is met the moment it crosses).
  4. At the actual scheduling point, the scheduler checks this flag — if set, it takes the current task off the CPU and inserts it into the RB tree (**enqueue**), then pulls the leftmost task out of the tree (**dequeue**) to run on the CPU. Both operations are O(log n).
- That completes the full picture of the two key schedulers in Linux history: **O(1) and CFS**.

### 51. "Is CFS Always Good?" — The Battle of the Schedulers Paper (CFS vs. FreeBSD's ULE)

- **The question raised**: is CFS always right? A real research paper is presented as evidence — **"The Battle of the Schedulers: FreeBSD ULE vs. Linux CFS,"** published at USENIX **ATC** (Annual Technical Conference). (The professor's aside: OSDI and SOSP are the top systems venues, with ATC and EuroSys just behind them, often covering practical issues.)
- **What's compared**: FreeBSD's scheduler is called **ULE** (macOS is also BSD-derived, for reference). The paper compares ULE against CFS.
- **The two design philosophies**:
  - **CFS**: pursues complete fairness, true to its name — a single red-black tree, no distinction between interactive and batch tasks. Tasks are ordered by vruntime, the leftmost is always chosen, and a task returns to the run queue once its time slice expires.
  - **ULE**: keeps **two separate run queues**, one for interactive and one for batch. Interactive tasks have **absolute priority** over batch tasks — a batch task can only run once the interactive run queue is completely empty.
  - Why this doesn't break fairness under ULE's design rationale: interactive tasks spend most of their time **sleeping**, so batch/CPU-bound tasks get their opportunity to run in the gaps.
- **Experimental results**: overall, there was no clear performance gap between the two schedulers (sometimes ULE did better, sometimes CFS did, with no obvious pattern). But one striking, somewhat extreme scenario ran an interactive task alongside a CPU-bound (batch) task simultaneously:
  - **CFS**: both tasks get roughly **15%** of the CPU each, with nearly identical slopes — not perfectly but almost fair, with no starvation.
  - **ULE**: the interactive task runs to completion first, and only then does the batch task get to run — the batch task waits roughly **150 seconds** (i.e., starvation). Interactive tasks get shorter latency (higher responsiveness) under ULE, but at the cost of fairness — the batch task starves.

### 52. CFS's Limitation → the Motivation for EEVDF

- CFS focuses purely on fairness — it picks the task with the smallest vruntime, and CPU share is determined entirely by weight. It gives interactive and batch tasks the same "fair" opportunity, with no distinction between them.
- **The core limitation: CFS doesn't account for latency at all.** The nice value controls **how much** CPU time a task receives (its rate/share), but not **how soon** it wants that CPU time. Different tasks can end up with the same CPU-share rate while having very different latency requirements — interactive tasks need shorter latency, but CFS can't express or handle that. **This is the motivation behind EEVDF.**

### 53. Introducing EEVDF — Concept and Goals Only (Mechanics Deferred to Next Time)

- **EEVDF = Earliest Eligible Virtual Deadline First**. A relatively new scheduler, added in **Linux 6.6** in 2023 (the professor noted some Android phones or Ubuntu servers may still run older kernels than this). It's a **successor to, and extension of, CFS** — built on the same underlying concept, still **O(log n)** in complexity.
- The core academic idea actually dates back to the **mid-to-late 1990s** (the professor couldn't recall the exact year — roughly 30 years old), but Linux developers adopted it to solve the CFS problems from §52.
- **Goal**: improve responsiveness for latency-sensitive scheduling while **preserving CFS's fairness**.
- **Key concepts (named but not explained — the computation methods weren't covered this session)**: **lag**, **eligibility**, **eligible time**, and **virtual deadline**. These were only mentioned as the values used in scheduling decisions.
- **A very simplified CFS vs. EEVDF comparison** (the professor: "not entirely accurate, just meant to convey the concept"): assuming two tasks share the same nice value (same weight), under CFS's complete fairness an interactive task might have to wait its turn in real time just like any batch task, since there's no distinction between them — but under EEVDF, that interactive task can get an earlier opportunity to run on the CPU.
- **Important**: EEVDF combines two concepts — CFS (fairness/vruntime) and **EDF (Earliest Deadline First, the deadline-based scheduling policy from real-time systems)** — with the core idea being "the task with the earliest deadline gets the highest priority." **However, exactly how this combination is implemented (how vruntime and virtual deadline are merged) was not covered this session and was explicitly deferred to next time** — this note does not speculate about that mechanism.

### 54. Earliest Deadline First (EDF) — Worked Example

- As background for understanding EEVDF, the classic real-time scheduling policy **EDF** was covered. Core rule: **the task with the earliest deadline gets the highest priority.**
- **Worked example**: three tasks all arrive at **T0**.
  - **Task A**: execution time **3ms**, deadline **7ms**.
  - **Task B**: execution time **2ms**, deadline **4ms**.
  - **Task C**: execution time **1ms**, deadline **6ms**.
- **Scheduling order under EDF**:
  1. At T0, compare the three deadlines (7, 4, 6) → the earliest is B (4ms) → **B runs first**, taking 2ms (finishes at T2).
  2. Comparing the remaining tasks, A (deadline 7ms) and C (deadline 6ms) → C has the earlier deadline → **C runs next**, taking 1ms (finishes at T3).
  3. Finally **A runs**, taking 3ms (finishes at T6 — within its 7ms deadline).
  - **Final order: B → C → A** (total execution time 2+1+3=6ms; all three tasks finish within their own deadlines).
- **EDF's limitations**: it requires **precise deadline information** for every task, and since the scheduler must compare deadlines whenever a new task arrives, it can suffer from **high context-switching overhead** — a new task with an earlier deadline than the currently running one always triggers a context switch. This is why EDF is mainly used in **RTOSes (real-time operating systems)**, with general-purpose schedulers not adopting it directly — the only stated connection is that **EEVDF borrows the deadline concept from it**.
- The lecture ended here, with an explicit note that "**we'll continue with EEVDF next time**" — this note does not speculate about EEVDF's detailed mechanics (lag/eligibility computation, etc.).

---

## Day 6 (2026-09-23) — Deep-Dive Review of CFS/EEVDF and sched_ext

> Source: 2026-09-23 lecture-audio STT (from the `recap` project's result file, `2026-09-23-system-programming-1.json`, titled "CFS/EEVDF Review & Scheduling Classes (incl. sched_ext)", 44 paragraphs, ~44 minutes). This was a regular class session held **the day before Chuseok holiday began**. It covers the EEVDF mechanics (lag/eligibility/virtual deadline) that Day 5 had deferred. The first part quickly reviews CFS and re-establishes the motivation for EEVDF; the middle part works through lag, eligibility, and virtual deadline in depth with a worked example; the back half wraps up with a full history of the scheduler's evolution, Linux's modular scheduling-class concept, and the newest feature, `sched_ext`.

### 55. Announcements — the Chuseok Makeup-Class Plan and Next Week's Assignment

- This session was held the day before Chuseok holiday. Friday's class needs a makeup session per university policy, and between the two options (an in-person makeup class vs. a recorded video class), the professor chose the latter — reasoning: "I don't want to give you a lot of work over the holiday." His plan is to record videos reviewing and summarizing the process-management/scheduling material covered so far, which he says will also help with midterm prep.
- The plan: upload the videos by tomorrow (9/24), to be watched before next Wednesday. Per the rule that "a 30-minute video can replace one hour of class," there will be two 30-minute videos.
- He's considering giving an assignment related to CFS or EEVDF sometime next week — not yet decided, stated as "thinking about it."

### 56. CFS Review — Weight, Vruntime, and the 1.25x Rule

- Restating CFS's core: it's all about fairness — the key idea is fixing the O(1) scheduler's unfairness problem (Day 5 §45). Two key concepts: (1) **weight** — time slices are determined based on weight. (2) **virtual runtime (vruntime)** — indicates how long a task has run and how much longer it should run. Reconfirmed: **larger weight means vruntime increases more slowly** — because higher weight means the task is more important, so the scheduler should give it more CPU share and opportunities (consistent in direction with Day 5 §49's "smaller weight → faster-growing vruntime," just phrased from the opposite side).
- **The 1.25x rule**: a one-level nice-value difference is designed to always mean a **1.25:1 weight ratio** (≈25% increase) — this is the core idea behind CFS making "each step always have a consistent effect" (reconfirming the fix to the unfair priority effect from Day 5 §48). Two tasks with equal priority (nice) get a 1:1 weight ratio and thus equal time slices. Assuming a total time slice of 10ms, a nice difference of 1 gives a 1.25:1 weight ratio, and the two tasks split the time slice according to that ratio. For a difference of 5, or generally n, the weight ratio is always **1.25 to the power of n**. The baseline is reconfirmed: nice=0 maps to weight=1024.
- **Data structures, reconfirmed**: the scheduler uses a red-black tree (RB tree) to pick the next task — insertion and lookup are always O(log n), more efficient than list/queue-based management. The scheduler keeps a pointer to the RB tree's **leftmost node**, making next-task selection very fast. Inserting a new task is also O(log n). Tasks are sorted by vruntime.
- **Run-queue structure, reconfirmed**: each CPU has its own run queue, made up of real-time-related structures (a doubly-linked-list family) plus a single RB tree for normal tasks.

### 57. CFS's Limitation, Reconfirmed → the Goal of EEVDF

- CFS focuses purely on fairness, and fairness doesn't mean low latency — that's the problem. Splitting tasks into interactive and CPU-bound (batch), latency matters more for interactive tasks, but CFS treats the two the same "fairly," which can cause problems for interactive tasks — this is why **EEVDF** was adopted in this version of Linux.
- A very simplified comparison (the professor's own caveat: "not entirely accurate, just meant to convey the concept"): because CFS's RB tree is sorted by vruntime and everything revolves around vruntime, an interactive task may have to wait a long time until it becomes favorable in vruntime terms, leading to higher latency. What EEVDF wants to do is give interactive tasks lower latency through deadline-aware scheduling.
- EEVDF shares the same design philosophy as EDF from real-time systems (the task with the earliest deadline gets the highest priority, Day 5 §54). **EEVDF's goal is to consider both latency and fairness at once.**

### 58. EEVDF's Core Concepts — Lag and Eligibility (an A/B/C Worked Example)

- To achieve this goal, EEVDF introduces two key concepts: **lag** and **eligibility**.
- **Definition of lag**: the difference between the ideal CPU time a task should have received and the CPU time it actually received = (the average runtime across all tasks) − (that task's own runtime). If a task's runtime is larger than the average, its lag goes below zero (negative); if smaller, its lag goes above zero (positive).
- **Eligibility rule**: if lag is below zero, the task is not eligible — it has already been allocated too much CPU time. If lag is zero or above, the task is eligible — it hasn't yet received its fair share of CPU time.
- **Worked example**: assume three tasks A, B, and C have the same nice value (same weight), and their time slices are all 30ms.
  1. Initial state: all three have lag=0 → by the eligibility rule, all three are eligible.
  2. The scheduler picks **A** first (arbitrarily, since there's no priority difference among them), and A runs its full 30ms time slice. Average runtime = (30+0+0)/3 = **10ms**. Based on this: **lag_A = 10−30 = −20** (not eligible), **lag_B = lag_C = 10−0 = +10** (eligible, since they didn't run on the CPU).
  3. Next, the scheduler picks **B** (again arbitrarily, since there's no priority difference), and B also runs its 30ms time slice. Average runtime = (30+30)/3 = **20ms**. Based on this, **both A's and B's lag become −10** — neither is eligible — and **C is the only task left that's eligible**, so C is the one selected next.
  - (Note: since this example assumes equal weight, technically vruntime should be used, but the professor pointed out directly that runtime and vruntime are essentially the same when weight is equal.)
- This example captures the core idea of lag and eligibility, and **EEVDF operates based on this concept.**

### 59. Virtual Deadline and EEVDF's Selection Logic

- Instead of vruntime, EEVDF maintains a **virtual deadline** for every task. CFS's RB tree is sorted by vruntime, whereas EEVDF also manages tasks with an RB tree but sorts it by **virtual deadline** — that's the difference.
- Virtual deadline was described (in the professor's words) as "pretty similar to how vruntime is computed in current implementations," calculated from weight and time slice as inputs — the exact equation itself was on the slide, but wasn't worked through numerically in the lecture. **This note does not speculate about the precise formula.**
- **EEVDF is still "settling"** — i.e., under active development, so implementation details can change, explicitly stated (the professor said he just wanted to convey the key philosophy and design choices). He recommended looking directly at the actual kernel code if interested, and especially when doing the assignment.
- **The role of time slice differs from CFS**: in CFS, weight determines the time slice, but **in EEVDF, weight does not determine the time slice** — normal tasks' time slices are all the same by default (though he noted developers or user programs can specify their own time slice if they want). Weight still determines **long-term CPU share** — if two tasks have the same weight, their CPU share eventually converges to 50:50.
- **Example of controlling latency via time slice**: even if task A is set to a 10ms slice and task B to a 100ms slice, as long as their weights are equal, the long-term CPU share stays 50:50. The difference is that when B gets a chance to run, it runs longer (100ms) — because it runs longer, its deadline value grows larger, so its next deadline is also larger, meaning it waits longer before its next opportunity. Conversely, **a shorter time slice gives an earlier virtual deadline** — a latency-sensitive task can request a shorter slice to get scheduled sooner, without increasing its long-term CPU share. This is the key mechanism by which EEVDF controls latency while preserving fairness.
- **Distinguishing it from SCHED_DEADLINE (explicitly stressed by the professor)**: EEVDF also uses a "deadline" concept, but it's **a different policy from SCHED_DEADLINE** — SCHED_DEADLINE is an EDF-based policy **for real-time tasks**, while EEVDF is **for normal tasks**. The virtual deadline is also different from a general real-time deadline scheduler in that it's not an actual wall-clock deadline but purely a value used for sorting, with no hard-deadline guarantee.
- **Steps of the selection function**: (1) among the runnable tasks in the run queue, filter down to only the eligible ones by checking their lag values (tasks that ran more than average are excluded — e.g., out of A, B, C, D, two tasks that ran more than average get excluded, leaving the rest as candidates). (2) among the remaining eligible candidates, pick the task with the shortest virtual deadline — this is how EEVDF's selection function works. (Note: in the actual kernel source, this selection function is named `pick_eevdf()`, though the lecture itself never named the function.)

### 60. EEVDF's Weakness — Selection Is O(n) (vs. CFS)

- An aside the professor added on the spot, noting it "wasn't written down on the slide": **EEVDF also has a bit of a weakness** — for CFS, task selection is **O(1)** (just pointing at the RB tree's leftmost node), but **for EEVDF, in the current implementation, this becomes O(n)** because of the issue below.
- Why: the leftmost-node pointer that works for CFS can be less useful in EEVDF, because that leftmost node (the one with the earliest virtual deadline) **might not be eligible**. If it isn't, the scheduler has to scan through tasks one by one until it finds an eligible one — which is why the professor directly assessed that "the RB tree isn't as meaningful in EEVDF" (compared to CFS). Still, as far as he understands, the kernel continues to maintain this RB tree structure, and only when the leftmost node isn't eligible does the scheduler scan through all eligible tasks to pick one.
- He mentioned that someone in the community might propose a new data structure to address this — implying no such alternative has settled in yet.

### 61. Scheduler History, Summarized — O(n) → O(1) → CFS (2007) → EEVDF (2023)

- The **original O(n) scheduler**, not covered in this course: described as very simple (naive) but very inefficient — reconfirming that the course instead started from O(1).
- **The O(1) scheduler**: more efficient than O(n), and some of its ideas/design choices are still present in the current Linux kernel — e.g., real-time tasks (SCHED_FIFO/SCHED_RR) are still managed via a doubly linked list today. But it needed too many heuristics to distinguish interactive from batch tasks, and having so many heuristics made the design/implementation inelegant — the core problem was **fairness**, and because that was such a big problem, **CFS was adopted in 2007**.
- **CFS**: based on weight, time slice, and vruntime, it was able to deliver genuinely fair scheduling. But it also had a problem: poor latency for interactive tasks.
- **EEVDF**: the new scheduler **adopted into Linux in 2023** to address this weakness — its key idea is **virtual deadline + eligibility** (eligibility computed from the lag value). EEVDF is still settling, with active development ongoing — he directly encouraged students: "if you have good ideas for this scheduler, go to the open-source community and propose your design; maybe you can change the history of the Linux scheduler."

### 62. Scheduling Classes — the Modular Structure (RT Class / Fair Class / Idle Class)

- Linux has multiple **scheduling classes**, a modular approach that lets different scheduling policies be implemented independently.
- Recapping the policies covered so far: **SCHED_FIFO** and **SCHED_RR** (introduced early in the kernel's history and still used today, for real-time tasks), and **SCHED_DEADLINE** (different from EEVDF but also for real-time tasks).
- For normal tasks, the scheduler is based on CFS or EEVDF. Linux supports multiple scheduling classes — for example, an **RT class**, a **fair class**, and an **idle class**. (The professor explicitly hedged: "I'm not sure the class name is exactly this" — he noted these names are based on the source code from the CFS-era version of Linux.)
- The core message: Linux systems can have very different kinds of tasks and workloads, which is exactly why Linux provides this modular approach to scheduling policies.

### 63. sched_ext — the eBPF-Based Extensible Scheduler Class

- Beyond these existing policies, modern Linux also supports an **extensible scheduler class, `sched_ext`** — meaning you can add your own scheduler to the Linux kernel without recompiling or rebuilding the entire kernel, a very new feature. As of the professor's reference point, the latest LTS (long-term support) Linux kernel is 6.18, with 6.12 just before it — so this is quite a recent addition.
- **How it works**: sched_ext is a scheduling class whose behavior can be defined via **eBPF** — through this, you can insert your own scheduling policy into the Linux kernel. It allows custom scheduling policies without modifying the kernel: it exposes scheduling operations through eBPF, supports custom scheduling logic, and the custom policy can be **dynamically enabled and disabled**.
- **Motivation**: different workloads may require different scheduling policies — for example, there are now many AI-serving systems like ChatGPT, and you could also think of physical AI things like robots, both of which are very different from traditional computers like a laptop or desktop. To support this kind of diversity in computing devices with very different workload characteristics, Linux decided to open up this feature to more people. He also mentioned the benefit of rapid experimentation, implementation, and workload-specific optimization, since testing a new scheduling policy no longer requires modifying or rebuilding the kernel.
- The professor wrapped up by saying, half-joking, "if you want, you can design your own scheduler and easily test it with sched_ext — I could give you this as an assignment... or maybe not, okay, I was just joking," and closed the class with holiday wishes for Chuseok.

---

## Day 7 (2026-09-25) — Makeup Videos: L01 & L02–03 Review

> Source: two makeup videos (posted on LearnUs) that replaced an in-person class due to Chuseok holiday, exactly as announced in Day 6. Video 1, `2026-09-25-system-programming-1.json` (titled "Makeup Video: L01 Review — Kernel Execution, Processes & Threads," 34 paragraphs, ~30 minutes/1778 seconds); Video 2, `2026-09-25-system-programming-2.json` (titled "Makeup Video: L02-03 Review — O(1), CFS & EEVDF Schedulers," 49 paragraphs, ~34 minutes/2029 seconds). **Both videos are pure review** — they summarize and re-explain material already covered in Days 1–6, with no new slide content added, so this note does not re-explain concepts already documented and instead pulls out **only what was freshly phrased or emphasized, plus anything exam-related.**

### 64. Video Structure — No New Slide Content

- **Video 1 (L01 review)**: how the kernel executes kernel code (process-based OS vs. execution-within-user-process), dual-mode operation and the three mode-switch events, the definition/images/context of a process, the motivation for threads and the sharing model, process states, task_struct, process-list management (linked list + hash table), and wait queues — walking back through material already covered in Days 2, 3, and 4, in order. **No new facts or examples** (everything matches the Day 2–4 notes as already recorded).
- **Video 2 (L02–03 review)**: the four process-switching events, hardware context/thread_struct, the kernel implementation of threads (lightweight process, less-lightweight process/COW/vfork), kernel threads (swapper/init), the two stages of process destruction, and the full history of the O(1)/CFS/EEVDF schedulers — a condensed re-summary of material already covered in Days 3, 4, 5, and 6. **Again, no new facts.**
- Both videos repeatedly skip over explanations with remarks like "we already covered this, so you can understand it by going over the slides yourself" (e.g., for the detailed steps of the `switch_to` macro).

### 65. Exam Signal — "What Got Skipped Could Still Be on the Midterm"

- In Video 2, while skipping the explanation of Linux's scheduling principles (the slide summarizing the cases that require task scheduling), the professor explicitly said: "This slide is also very important, so I hope you pay attention to it, but I'll skip the explanation."
- Similarly, while summarizing the run-queue data structures and O(1)'s scheduling policies, he said again: "They're all important, so I hope you study them for the exam, but due to time limits, I'll skip the detailed explanation here."
- **The explicit exam warning at the end of Video 2 (the most important signal)**: "Just so you know, I skipped some materials in this video. But that doesn't mean the materials I skipped won't be on the midterm exam — though it's likely to be rare." He followed this with: "I think most of what I covered in this video is more important than what I didn't cover. But still, I want you to study the points I didn't explain in this video." In other words: **what was actually explained in the video takes priority, but the skipped slide details are explicitly not fully ruled out from the midterm scope either** — a warning that should be read at face value.

---

## Day 8 (2026-09-30) — Multiprocessor Scheduling, Load Balancing & Energy-Aware Scheduling (EAS)

> Source: 2026-09-30 lecture-audio STT (from the `recap` project's result file, `2026-09-30-system-programming-1.json`, titled "Multiprocessor Scheduling, Load Balancing & Energy-Aware Scheduling (EAS)," 41 paragraphs, ~41 minutes/2462 seconds). This lecture is covered on the catch-up site (`system-programming/w03`) along with slide images (pages 30–42 of the full 49-page deck).

### 66. Scheduling-Related System Calls — nice, sched_setscheduler/getscheduler, CPU Affinity

- A few system calls related to scheduling. One sets/adjusts the nice value — the nice value is an input the task provides to set its priority; what the call actually does is just change the nice value, and the scheduler then makes its real decisions based on that value. `sched_getscheduler` retrieves the current scheduling policy, `sched_setscheduler` sets it, and similar calls can get or set more detailed attributes.
- The last one is **CPU affinity** — related to multiprocessor scheduling. With multiple CPUs (e.g., CPU 1, 2, 3), this kind of system call restricts which CPUs a task is allowed to run on. **Worked example**: task 1 is set up to run on CPU 1, 2, or 3; task 2 is restricted to run only on CPU 1.

### 67. Motivation for Multiprocessor Scheduling and the Two Principles of Load Balancing

- Modern computers have 4, 8, or more cores, so distributing workload evenly across CPUs matters for optimal resource utilization, maximizing throughput, and minimizing response time.
- **Analogy (the professor's 4-month-old baby)**: taking care of a baby (feeding, playing, washing bottles, burping, etc.) generates many "tasks," and it's important for the couple to distribute that load evenly. If one parent feeds the baby while the other slowly sterilizes a bottle, the load is balanced. You might think you could just hand the baby to the other parent, but the parent currently holding the baby knows its context — "it just had milk, so it needs to be burped" — and some of that information can be lost in the handoff. This is similar to the **cache** concept, and it illustrates why migrating a task from one CPU to another carries overhead (load-balancing overhead, the cache effect) from moving program state like register state or TLB state.
- Each CPU has its own run queue, and work distribution is based on these run queues. Each task has a load estimate, and since a task must belong to exactly one run queue, the run queue itself also has a load (based on the loads of the tasks belonging to it).
- **The two principles of load balancing**: ① prevent a situation where some CPU is idle while another CPU still has tasks waiting to run — the single most important principle in Linux load balancing (per the baby analogy: it's not a "happy situation" if one parent is just sitting idle while the other does all the work). ② keep CPU utilization as balanced as possible across CPUs. To achieve these goals, Linux checks whether a scheduling domain is significantly unbalanced.

### 68. PELT (Per-Entity Load Tracking) — Load vs. Utilization, Worked Example

- The current Linux kernel's load estimation is based on **PELT (Per-Entity Load Tracking)**. It tracks **load** and **utilization** per task and per run queue — these are two distinct values. The weighting is based on **EWMA (Exponentially Weighted Moving Average)**, with the core idea being that more weight is given to recent activity.
- **Load vs. utilization**: load concerns the **runnable** fraction (not blocked or interrupted), while utilization concerns the fraction of time actually **running** on the CPU — a running task is also runnable, but a runnable task isn't necessarily running.
- **Worked example**: two tasks T1 and T2; in the first one-millisecond window, suppose T1 actually runs for 0.6ms and T2 for 0.4ms. Both were runnable for the entire 1ms, so the runnable fraction is 1 (100%) for both, but the running fraction (the value used for utilization) is 60% and 40% respectively. This value is multiplied by the weight used in CFS and similar, and EWMA folds in historical values to produce the final load estimate for the task and the run queue.
- **Division of use**: the load value is used for **load balancing** (balancing load among peers), while the utilization value is used for **energy-aware scheduling (EAS)** (covered later).

### 69. Scheduling Domains and Scheduling Groups

- **Scheduling domain**: the scope within which load balancing happens — the set of peers across which the scheduler performs load balancing. Each scheduling domain consists of one or more **scheduling groups**.
- **Scheduling group**: the basic unit of load balancing. When the scheduler performs load balancing, it compares groups against each other, comparing their load and capacity, and migrates tasks from a busier group to a less-loaded one.

### 70. Events That Trigger Load Balancing — Time-Driven and Event-Driven, Worked Example

- **Time-driven (periodic, domain balancing)**: triggered by timer interrupts — on every scheduler tick, it periodically checks whether rebalancing is needed.
- **Event-driven**: triggered by scheduling events. The main example is new-task creation, but a task that was blocked becoming runnable again is also treated as a kind of "new task" event — from the Linux scheduler's perspective, there's one more task to place, so the load balancer looks at each CPU's (scheduling component's) load to decide where to send it. In this case, the load balancer picks the least-loaded group in the current domain, then sends the task to the least-loaded CPU within that group.
- Following the other principle (§67), when a CPU becomes newly idle, the load balancer selects the **most-loaded** group in the current domain and moves a task from the most-loaded CPU in that group to this idle CPU.
- **Worked example**: with only two groups, if group 2 is more loaded, and within group 2, CPU 4 is more loaded than CPU 3, the balancer picks a task from CPU 4 to move to the now-idle CPU 1. (With more groups, say 1 through 4, the same logic extends by first finding the most-loaded group.)
- **Task-selection considerations**: since migration always carries some overhead (the cache effect from §67), the load balancer also considers things like cache locality, which is why migration doesn't happen too frequently.
- **Q&A**: "What if CPU 2 is more loaded than CPU 4?" — the first step is comparing groups, so even if CPU 2 is more loaded than CPU 4, as long as CPU 2's group is more loaded than CPU 1's group, the balancer picks that group first, and only then finds the most-loaded CPU within the chosen group — group comparison always comes before CPU comparison.

### 71. The Load Balancer's Symmetric-CPU Assumption and Heterogeneous CPU Architecture

- The load balancer described so far assumes CPUs are **symmetric** — i.e., all have equal performance. Desktops and servers usually have identical cores, but **heterogeneous CPU architecture** also exists — laptops might too (the professor wasn't fully certain), but Android smartphones are definitely heterogeneous.
- **Why**: to reduce battery usage. Users of mobile devices like smartphones and laptops want longer battery life, so heterogeneous CPU architectures like ARM's **big.LITTLE** (big cores + LITTLE cores) are used. Other similarly-named heterogeneous architectures exist too (the professor: mostly a naming issue), but the core reason is that sometimes powerful computation is needed and sometimes energy efficiency matters more — some tasks don't need much compute and can tolerate longer response times.

### 72. Handling Heterogeneous CPUs — From IKS to HMP

- **IKS (In-Kernel Switcher)**: pairs one big core with one LITTLE core, treating big.LITTLE pairs as four groups (four CPUs), with each group deciding which core to use. The professor's assessment: not very efficient, since it doesn't fully exploit the potential of heterogeneous CPU architecture.
- **HMP (Heterogeneous Multi-Processing)**: what most smartphones and computers use today. For example, with 8 cores that are non-symmetric, the Linux scheduler treats them as 4 big cores and 4 LITTLE cores — cores within the same group are symmetric with each other, but not across groups. This structure makes the best use of big.LITTLE's potential.

### 73. DVFS (Dynamic Voltage and Frequency Scaling) Basics

- Beyond CPU architecture, mobile systems have a more sophisticated mechanism for energy efficiency: **DVFS (dynamic voltage and frequency scaling)**. Big and LITTLE cores' operating frequencies vary (e.g., up to 4GHz), and this maximum clock isn't always needed — games and AI tasks need big cores and maximum frequency, but lightweight tasks like a phone call, or idle periods, don't.
- DVFS lets a device adjust clock frequency and supply voltage when it wants to reduce power/energy usage. Another reason to reduce frequency is **heat** — running at maximum frequency continuously makes the device very hot.
- **The relationship**: power is determined by voltage and frequency, and voltage and frequency are themselves related — reducing frequency reduces voltage, which reduces power, generating less heat, using less energy, and extending battery life.

### 74. Limitations Before EAS — Independent, Sampling-Based Governors

- Previous Linux schedulers didn't account for heterogeneous CPU architecture or DVFS at all, making them inefficient — previous scheduling policies were throughput-oriented, with energy/power efficiency not a consideration.
- **The core problem**: DVFS itself already existed in computers, but the scheduler didn't control it — device drivers like GPU drivers each had their own **governor**, operating independently of the scheduler. Governors had to periodically **sample** CPU load, making them slow to respond. A task's utilization can change dynamically, and when the scheduler and governor operate independently, it's hard to respond to these changes quickly — this is why **EAS (Energy-Aware Scheduling)** was introduced into Linux.
- EAS differs in character from CFS/EEVDF: CFS/EEVDF operate within the scope of a single CPU/single run queue, while EAS is more about **group-level balancing** across multiple CPUs and **directly controls DVFS** — this is the key difference from general-purpose schedulers. Now the scheduler and the governor work together.

### 75. EAS's Task-Placement Policy — the Energy Model and OPP

- When a new task appears or wakes up, the scheduler must decide where to place it. Previous schedulers assumed all cores were symmetric, but EAS can view the system as **heterogeneous** — EAS is designed for **asymmetric CPU-capacity systems** like big.LITTLE.
- **OPP (Operating Performance Point)**: to decide which processor to pick, the scheduler needs to know the energy model of each CPU at each operating frequency. Operating frequency isn't continuous but **discrete** — there might be only, say, five steps, so you can't set an arbitrary value in between. These supported frequency-voltage operating points are called OPPs, and a typical computer has roughly 10–20 of them. Each OPP's energy model can be known offline in advance, so the Linux kernel keeps tables for this. The energy model describes the performance and power cost of each supported OPP within a performance domain.
- **Worked example (a waking task)**: if the scheduler places the task on CPU 3, no P-state (operating frequency) change is needed, so overall power stays the same; if placed on CPU 1, the OPP changes and power usage increases. When a task wakes up, EAS uses that task's CPU utilization, CPU capacity, and this energy model to pick the most energy-efficient CPU.

### 76. EAS's Scheduler-Driven DVFS

- Another key feature of EAS is **scheduler-driven DVFS**: whenever the scheduler's load tracking (PELT) is updated (on wakeup, migration, or utilization update), EAS's governor can immediately request a new CPU frequency. Previous sampling-based governors periodically sampled CPU load and were slow to respond, whereas EAS's governor reacts directly to scheduler events and computes the target frequency immediately, responding far faster to workload changes — this is the key difference between EAS and traditional sampling-based governors.

---

## Day 9 (2026-10-02) — EAS Research Papers & the Preemptive vs. Non-Preemptive Kernel

> Source: 2026-10-02 lecture-audio STT (from the `recap` project's result file, `2026-10-02-system-programming-1.json`, titled "EAS Research Papers & Preemptive vs. Non-Preemptive Kernel," 98 paragraphs, ~103 minutes/6206 seconds). **This lecture splits into two main parts**: (1) **an off-deck first half, with no corresponding slide deck** — after some pre-class chatter about the Yonsei-Korea rivalry week and a brief recap, this part goes deep on three real research papers related to EAS; no slide deck corresponds to this material. (2) **a second half covered on the catch-up site (`system-programming/w03`)** (pages 43–49 of the full 49-page deck) — covering the preemptive/non-preemptive kernel distinction and the `preempt_count` mechanism, completing that 49-page slide deck in this session. Toward the end of the lecture there's a logistics note that the TA's trip to Europe will delay the assignment announcement, and the session winds down by transitioning naturally into the next lecture's topic, Interrupts and Exceptions — that material itself belongs to the next deck, so this note doesn't cover it (see §87).

### 77. Pre-Class Chatter — Rivalry Week and a Brief Recap

- Before class started, the professor briefly recounted his Yonsei-Korea rivalry week ("Yeongbodan") experience — he went to the baseball game to pay his respects to seniors, ran into the Dean of the College of Computing there, and called it a "somewhat obligatory" occasion; he also had lunch with other professors. The game ended in a 2–0 loss (close to 0–0 until late), and he remarked that Korea University's cheering was "amazing." (A sentence in this part of his remarks translates to "that's why I had to cancel class today," but since class was clearly proceeding normally, exactly which class or day this refers to is unclear from this session alone — this note does not speculate about it.)
- He then moved straight into recapping last time (Day 8): load balancing in symmetric and heterogeneous CPU architectures, the fact that heterogeneous architectures were introduced for energy efficiency in the first place, and how EAS (energy-aware scheduling) works and why it was adopted into the Linux kernel.
- He announced that in the first hour today he'd show some real research on energy-aware scheduling — **explicitly stating this material itself isn't exam material, but the limitations of EAS and of governors in general could appear on the exam** — telling students they just need to take away the key points, not the details.

### 78. Paper 1 — Graphics-Aware Power Governing for Mobile Devices (2019)

- Introduced as research presented in 2019, with the professor using "we" throughout (suggesting it's his own lab's work, though no paper title, co-authors, or venue were named in this session). It covers the Android OS **before EAS was adopted**; it doesn't address EAS directly but shows the limitations of Linux's governing and energy management.
- **Background**: AP (application processor) performance improved dramatically (the professor's estimate: roughly 30x from an original "S" model to the "S26"), while battery capacity has barely moved due to the physical constraints of lithium-ion batteries — why energy matters so much.
- **Graphics-rendering constraints**: at the time (2019), the target frame rate was a strict 60fps rendering deadline, meaning every frame's rendering work had to finish within that window. Reducing frequency via DVFS reduces power, but that doesn't always mean better energy efficiency — energy = latency × power, so, for example, "10ms at 4W" isn't necessarily less efficient than "30ms at 2W" (though in general, reducing frequency does tend to improve energy efficiency).
- **Two core problems**: ① the CPU's and GPU's DVFS governors operate **independently of each other** (in the graphics pipeline, the CPU processes first and the GPU handles the rest, each with its own frame deadline). ② the load (or utilization) estimation used by governors at the time was fairly "naive."
- **Preliminary experiments** (running 60 different apps on a relatively old smartphone of the time): there was waiting time, and in many real applications, frame rendering had already finished while the Linux kernel kept running at a higher frequency and on bigger cores (the big cluster) than actually needed — **the root cause being that the Linux kernel doesn't know each task's deadline**. A swipe-gesture experiment showed a similar pattern, with UI and render threads running on the big cluster even when they didn't need to.
- **Proposed fix — joint CPU/GPU governing**: applying **GPU min capping** (raising the GPU's minimum frequency) together with **CPU max capping** (lowering the CPU's maximum frequency). The observation was that raising CPU and GPU frequency together creates a bottleneck at a certain stage, so instead the GPU frequency is raised (cutting GPU-side latency) while the CPU frequency is lowered correspondingly — an evaluation sought a near-optimal CPU/GPU frequency combination and reportedly showed substantial energy savings in real-world usage (no exact figures were given).
- Conclusion: the core point of this paper is that the **CPU and GPU governors were very inefficient because they weren't aware of specific deadlines**.

### 79. Paper 2 — EAS-Based Mobile Web-Browser Scheduling: Reinforcement-Learning-Tuned SchedTune/UCLAMP Boost Values

- Once EAS is adopted, frequency can no longer be controlled **directly** as in the previous paper — the scheduler (EAS) controls frequency. So the question became "what can actually be controlled within EAS," and this research focused on **mobile web browsers** (to look at CPU alone, rather than CPU and GPU together). The background: web browsers are the most widely used mobile app and are CPU-heavy.
- **The kernel's fundamental difficulty**: it's very hard to estimate a task's actual utilization — some tasks, like rendering, must finish within a specific deadline (e.g., 33ms), while others, like background tasks, have no deadline at all (whether they take 1 second or 1 hour doesn't matter) — and the kernel has a hard time telling these apart.
- So the kernel exposes a **utilization-clamping** interface at the user level (to developers, Android framework developers, or app developers) — before EAS this was called **SchedTune** (about 5–6 years ago), and it's now called **UCLAMP (utilization clamping)**. Setting the boost value to its minimum (-100) makes the estimated utilization very small, so EAS sends the task to a middle core at minimum frequency; setting it to the maximum (100) sends it to a big core at higher frequency. The professor directly assessed that this kind of decision "should be made at the kernel level, not the user level" and that exposing it this way "isn't ideal" — though there's a practical reason: web-browser processes vary enormously in processing speed depending on the situation, making it hard for the kernel to estimate actual utilization. The optimal clamping factor differs per web page.
- **Experimental setup**: the goal was to maximize energy efficiency while maintaining page-load performance (noting that researchers generally assume people can tolerate up to 10 seconds for a page to load — the professor joked "I don't think Koreans would agree"). Fast-response actions like swipes were examined separately.
- **Method — reinforcement-learning-based search for the SchedTune boost value**: the input (state) was measurable process data like the number of tasks, the reward was CPU energy, response time, and dropped frames, and the action was choosing the SchedTune boost value. The goal was to find **the optimal SchedTune boost value for each mobile web page**. This value had previously always been fixed at zero (different from how Android normally handles it, the professor added); the method lowered the clamping factor, leading to lower CPU frequency and reportedly substantial energy savings.
- (Aside: Android systems typically split into 3–4 groups — e.g., background and top-app groups — each with its own clamping value; touching the screen raises it sharply, and the screen turning off lowers it a lot, as the professor also noted.)

### 80. Paper 3 — A Follow-Up: Finding the Clamping Value from Kernel-Level Signals Alone (Wake-Up Sequence + Touch-Driven Inference)

- Introduced as a **follow-up** paper published last year (2025, per the professor's "last year"), again on mobile web browsing (with figures updated to the Galaxy S24), and it directly addresses the problem left by the §79 paper.
- **Critique of the previous paper**: the §79 method relied on **application-level (user-level) data**, such as webpage type and structure — which violates the important design philosophy that "kernel-level and user-level information should be kept separate," i.e., the kernel should rely on kernel-level data, not user-level data.
- **Goal**: achieve energy efficiency using only system-level (kernel) data. Two mechanisms exist in general: **boosting** (raising estimated utilization above the actual value so EAS uses the inflated value, typically applied to the top-app group) and **capping** (lowering utilization below actual, typically applied to background apps) — Android's way of getting both responsiveness and energy efficiency, but this still doesn't work well, which is this paper's starting point.
- **Core idea — the task wake-up sequence**: from the observation that the sequence of **wake-up events** — one task waking another — can hint at a web application's usage context (e.g., how long it's being used), the paper introduces a **two-factor task wake-up sequence embedding**. This follows the design philosophy (echoing §68/§78's polling-vs-interrupt logic) that an object-based (poll-like) approach is never efficient while an event-driven approach always is.
- **Predictors and touch-driven inference**: using this embedding as input, two predictors — one based on **linear regression**, one on a **neural network** — are introduced to find the optimal clamping value. In addition, since a touch triggers a change in the user's context, **touch-driven inference** is introduced — every time a touch happens, these predictors recompute the optimal clamping value. The result reportedly showed better energy efficiency than EAS's default behavior at the time.

### 81. EAS's Limitations, Summed Up — "Not a Perfect Solution"

- Wrapping up the three papers, the professor **explicitly concluded that EAS is not a perfect solution**: because it's inherently hard to know each task's goal and characteristics, estimating each task's utilization remains fundamentally difficult — the core challenge EAS still faces. He closed this section with the same kind of remark he made about EEVDF in Day 6 (§61): "maybe one of you will come up with a new version of EAS for the community."
- (While the three papers themselves were stated at the outset not to be exam material, as noted in §77 the professor explicitly warned that **the limitations of EAS and of governors** could appear on the exam.)

### 82. The Preemptive vs. Non-Preemptive Kernel Distinction

- The preemption discussed so far concerned **scheduling** (round-robin, CFS, etc. are preemptive scheduling), but a **preemptive kernel** is a somewhat different concept — it's about whether **the kernel itself** can be preempted.
- **Setup**: when a user process calls a system call, the mode switches from user mode to kernel mode (a mode switch). Kernel mode has two contexts — **process context** and **interrupt context**. Suppose that while the kernel is in interrupt context handling an interrupt handler, a new task P2 — previously blocked — becomes runnable, and P2's priority is higher than that of process 1 (which made the system call).
- **Non-preemptive kernel**: the kernel-mode operation runs the system-call handler (running in process 1's context) to completion, and only performs the context switch once it's about to return to user mode (i.e., once kernel-mode operation finishes and the system call is about to return). From process 1's point of view, it was ultimately "preempted," but from the kernel/user-mode point of view, the kernel simply finishes its work for process 1 and then switches — because this is non-preemptive, the process switch is **deferred**.
- **Preemptive kernel**: when P2 wakes up, the process switch happens immediately, **even in the middle of** kernel-function execution — i.e., a kernel in which the scheduler is permitted to perform a context switch during a kernel function's execution, rather than cooperatively waiting for that function to finish and return control of the processor.
- **The purpose of a preemptive kernel**: to reduce latency for user-facing processes — it can give a higher-priority process a faster response. Conversely, in a non-preemptive kernel, a task running inside the kernel cannot be scheduled (preempted) while it's there.

### 83. Why Implementing a Preemptive Kernel Is Harder — Critical Sections and Identifying a "Safe State"

- **Question**: which kernel is easier to implement? **Answer: non-preemptive.**
- **Why**: a non-preemptive kernel works by the simple rule of never replacing the current process until it's about to switch to user mode, but there are moments when rescheduling genuinely isn't safe — such as when a **critical section** is executing inside the kernel. Implementing a preemptive kernel critically depends on **identifying** whether the kernel is currently in a "safe state" or not — which is exactly why a preemptive kernel is harder to implement.

### 84. Linux Kernel Version 2.6 — From Non-Preemptive to Preemptive, Planned vs. Forced Process Switch

- **Very old Linux kernels were non-preemptive** — a process switch could only happen after kernel code ran to completion. Mechanism: whenever the kernel is about to return to user mode after handling an interrupt or a system call, it explicitly checks a flag, and if set, the scheduler is invoked there to pick a new process — in a non-preemptive kernel, the process switch already happens exactly at this point.
- **Rationale**: if the kernel is returning to user mode, it means it has finished everything it needed to do, so rescheduling is safe — if it's safe to keep running the current task, it's equally safe to switch to a new one. This is a very conservative preemption policy, with the downside of **reduced responsiveness** — the kernel might already be in a safe state before finishing its current job, yet rescheduling is deferred until completion anyway.
- **Since kernel version 2.6, the Linux kernel became preemptive** — a task can now be preempted at **any point** in kernel mode, as long as the kernel is in a state where rescheduling is safe. There was no drastic change to the kernel's design itself; the only difference is how the kernel knows whether it's in a safe state.
- **Two kinds of process switch**: ① **Planned process switch** — a process blocks waiting for a resource, or explicitly calls the scheduler. Here, both non-preemptive and preemptive kernels have the process **voluntarily** give up the CPU (since the scheduler knows it's safe to reschedule right now). ② **Forced process switch** — e.g., an interrupt handler waking a higher-priority process — where non-preemptive and preemptive kernels behave **differently**. In a non-preemptive kernel, the current process can't be replaced except right before it's about to switch to user mode; in a preemptive kernel, it can be replaced in the middle of kernel-function execution.

### 85. The `preempt_count` Mechanism — a Bit Field in thread_info

- **When is rescheduling safe?**: a process can be preempted in kernel mode as long as it's **not holding a lock** — holding a lock while rescheduling happens can cause trouble, so holding a lock is itself treated as a marker of non-preemptibility. Besides locks, there are a few other conditions.
- **Structure**: kernel preemption is disabled whenever this field is positive; the field lives in the kernel's `thread_info` structure as a **bit field** (28 bits in reality, simplified to 6 bits in the lecture for illustration). Some bits represent the **hardirq count**, some the **softirq count**, and the remaining bits represent the **preempt count** (the explicit-disable counter). The right mask extracts each sub-field's value, but if **any single sub-field is positive, the whole value becomes positive** — this is how the kernel tracks the overall `preempt_count`.
- **Three cases that make `preempt_count` positive**: ① the kernel is executing an **interrupt service routine (ISR)**. ② the kernel is executing the deferred handler called **softirq** (hardirq and softirq themselves will be covered in detail in the next lecture, so this note doesn't cover them). ③ preemption has been **explicitly disabled** by setting a counter — this small sub-field is the explicit-disable counter.
- **The condition for preemptibility**: if none of these three cases hold (i.e., the whole `preempt_count` is 0), rescheduling is safe and preemption can happen. (At one point the lecture stated, "the kernel can be preempted only when it is executing an exception handler and preemption has not been explicitly disabled" — this is inconsistent with the surrounding explanation, namely that executing an ISR/softirq **disables** preemption, and that preemption is possible "when this value is not positive." A phrase was likely dropped somewhere in the STT/translation pipeline; this note follows the rule stated immediately beforehand — preemptible when none of the three cases hold — since that one is internally consistent.)

### 86. Worked Example — Whether Preemption Can Actually Happen, Given the `preempt_count` State

- **Setup**: while the kernel is executing an interrupt service routine (ISR), preemption doesn't happen (because the hardirq-count sub-field is positive). Right at the point where interrupt handling finishes and the kernel returns to kernel context, the kernel checks ① the need-resched flag and ② the `preempt_count` value.
- **Case 1 — preemption happens**: if the flag is set (a more important task is among the runnable ones, i.e., a newly-runnable process has higher priority than the current one) and `preempt_count` is 0, the kernel knows it's in a "safe state" and reschedules immediately — the scheduler is invoked and the context switch (process switch) happens.
- **Case 2 — preemption is deferred**: if the flag is set (the process that just woke up has higher priority than the current one) but `preempt_count` is positive (preemption is explicitly disabled), rescheduling isn't safe right now. The kernel must defer rescheduling until all these counters are released — i.e., until the kernel returns to a safe state.
- **Upon release**: once all the counters are released and the value becomes 0, the unlock code checks whether the need-resched flag is set, and if so, the scheduler is invoked at that point and performs the rescheduling — i.e., the same situation as Case 1, just happening at a deferred point.

### 87. Logistics — Assignment Delay and the Next Lecture

- Wrapping up the lecture, the professor said that everything covered so far (process scheduling, load balancing, heterogeneous CPU architecture, EAS, kernel preemption) is **the most important part for the midterm**, and urged students to focus their study especially on the scheduler.
- **Assignment delayed**: the TA is in Europe to attend **SOSP**, one of the top venues in computer systems, so the assignment likely won't be posted for another week or two. The assignment is expected to be **kernel-mode programming** (writing an actual kernel module) on the topic of **process scheduling related to CFS and EEVDF**. He also reaffirmed the AI policy (the same as Day 1 §1): can't be prohibited outright, but he recommends attempting the assignment yourself first and consulting AI only when stuck, recalling that in his own student days he had to rely on Stack Overflow instead.
- **Next lecture preview**: the next topic is **Interrupts and Exceptions**, explicitly tied to the kernel preemption just covered (since kernel preemption is disabled while the kernel handles interrupts). **The session actually continued right from this point into a substantial amount of material — the definition of an interrupt, the synchronous/asynchronous interrupt distinction, and the process-context/interrupt-context distinction — but this belongs to a new topic (the next deck) beyond the scope of the catch-up deck (`system-programming/w03`, pages 43–49), so this note does not cover it — it does not speculate about that content.**
