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
