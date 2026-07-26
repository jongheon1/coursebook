# 00-roadmap — System Programming (CAS3107, 2026-2)

과목명은 시스템프로그래밍이지만 실체는 **Linux kernel programming** 과목이다. 이 문서는 모든 주차 챕터 생성의 앵커다. 챕터를 만들 때는 이 문서의 주차 매핑·정본 소스·Modern kernel notes 를 기준으로 쓴다.

## 1. 깊이 벤치마크

이 과목의 목표 깊이는 다음 기준에 맞춘다:

- **MIT 6.1810 Operating System Engineering** — <https://pdos.csail.mit.edu/6.1810/> — 커널 코드를 직접 읽고 수정하는 lab 중심 수업. 우리 챕터의 lab 도 "실제 코드에서 확인"을 기본으로 한다.
- **Robert Love, *Linux Kernel Development* 3e (LKD, 2010, kernel 2.6.34 기준)** — 이 과목의 주차 구성과 거의 1:1 로 대응하는 사실상의 지정 교재. 설계 의도·트레이드오프 서술의 기준.
- **Bovet & Cesati, *Understanding the Linux Kernel* 3e (ULK, O'Reilly 2005, kernel 2.6.11 기준)** — LKD 보다 한 단계 깊은 자료구조·x86 경로 레벨 디테일의 기준. 시험 서술형 깊이의 상한선.
- **The Linux Kernel Module Programming Guide (LKMPG)** — <https://sysprog21.github.io/lkmpg/> — 5.x/6.x 커널로 업데이트된 모듈 실습 정본. 모든 lab 코드의 출발점.
- **kernel.org Documentation/** — <https://docs.kernel.org/> — 2.6 시대 교재 서술을 현대 커널로 보정하는 1차 근거.
- **LWN.net** — <https://lwn.net/Kernel/Index/> — EEVDF·folio·PREEMPT_RT 처럼 "교재 이후에 바뀐 것"의 정본 해설.

## 2. 정본 소스 (과목 전체)

| 소스 | 용도 | 링크 |
|---|---|---|
| LKD 3e (Robert Love) | 주차별 1차 교재. 2.6.34 기준 → 매 주차 보정 필요 | (서적) |
| ULK 3e (Bovet & Cesati) | 자료구조·경로 레벨 심화. 2.6.11 기준 | (서적) |
| LKMPG | module lab 실습 | <https://sysprog21.github.io/lkmpg/> |
| kernel.org Documentation | 현대 커널 정본 문서 | <https://docs.kernel.org/> |
| Linux source (v6.12 LTS 기준) | 모든 코드 경로 인용의 기준 트리 | <https://elixir.bootlin.com/linux/v6.12/source> |
| LWN.net Kernel Index | 커널 변경사 해설 | <https://lwn.net/Kernel/Index/> |
| Stoica & Abdel-Wahab 1995, *Earliest Eligible Virtual Deadline First* (TR-95-22) | W4 EEVDF 원 논문 | <https://people.eecs.berkeley.edu/~istoica/papers/eevdf-tr-95.pdf> |
| MIT 6.1810 (xv6 기반) | lab 설계·깊이 벤치마크 | <https://pdos.csail.mit.edu/6.1810/> |

코드 경로 표기는 v6.12 LTS 기준 (`elixir.bootlin.com/linux/v6.12/source/<path>`). LKD 3e 는 2.6.34, ULK 3e 는 2.6.11 기준이므로 교재 서술과 현대 커널의 차이는 각 주차의 **Modern kernel notes** 로 반드시 보정한다.

## 3. 주차별 매핑

W8(중간고사)·W16(기말고사)은 제외. W15 는 자율학습주와 겹치지만 콘텐츠 주차로 취급한다.

### W1 — Introduction to Linux

- **서브토픽**: monolithic vs microkernel 논쟁(성능·isolation·IPC 비용 트레이드오프); kernel space/user space 와 mode switch; loadable module 이 monolithic 의 단점을 어떻게 완화하는가; kernel source tree 구조(`kernel/`, `mm/`, `fs/`, `arch/`, `drivers/`); Kconfig/kbuild, `make menuconfig`, `vmlinux` vs `bzImage`; module 생명주기(`insmod`/`rmmod`, `module_init`/`module_exit`, `EXPORT_SYMBOL`, license 와 taint); `printk` 와 log level; 커널 개발 제약(no libc, 작은 고정 stack, no FPU)
- **정본**: LKD ch1–2, ch17(Devices and Modules); ULK ch1; LKMPG ch1–6
- **코드**: `kernel/module/main.c`, `include/linux/module.h`, `Documentation/kbuild/`
- **Modern kernel notes**: 모듈 코드는 `kernel/module.c` 단일 파일 → `kernel/module/` 디렉토리로 분리. Rust 지원이 6.1 부터 머지되어 in-tree 언어가 C 단일이 아님. lab 은 LKMPG 최신판(5.x/6.x 대응) 기준으로 작성.

### W2 — Linux process programming (1)

- **서브토픽**: process vs thread 를 커널이 보는 방식(둘 다 `task_struct`, 구분은 공유 자원뿐); `task_struct` 주요 필드(`__state`, pid/tgid, real_parent, mm, files, signal, thread); process state 전이도(TASK_RUNNING / TASK_INTERRUPTIBLE / TASK_UNINTERRUPTIBLE / __TASK_STOPPED, EXIT_ZOMBIE); `thread_info` 와 kernel stack 배치; `current` 매크로의 per-CPU 구현; process 계보(`init_task`, parent/children/sibling 리스트 순회); pid vs tgid, `getpid()` 가 실제로 반환하는 것
- **정본**: LKD ch3; ULK ch3
- **코드**: `include/linux/sched.h`(task_struct), `include/linux/thread_info.h`, `arch/x86/include/asm/current.h`, `kernel/pid.c`
- **Modern kernel notes**: x86 에서 `thread_info` 는 kernel stack 하단이 아니라 `task_struct` 내장(`CONFIG_THREAD_INFO_IN_TASK`) — LKD 의 "stack 끝에서 thread_info 를 찾아 current 계산" 그림은 구식이며, 현대 x86 은 per-CPU 변수로 `current` 를 얻는다. `state` 필드는 `__state` 로 개명.

### W3 — Linux process programming (2)

- **서브토픽**: `fork()` 경로 전체: syscall → `kernel_clone()` → `copy_process()` 의 단계(dup_task_struct → 자원 copy_* → pid 할당 → wake_up_new_task); clone flags(CLONE_VM/FS/FILES/SIGHAND/THREAD)로 fork·vfork·pthread_create 구분; COW 메커니즘(fork 시 페이지 write-protect → write fault 시 복사)과 비용 분석; `exec` 경로(`fs/exec.c`: `struct linux_binprm`, ELF loader, 주소공간 교체); kernel thread(`kthread_create`, kthreadd 가 낳는 이유); zombie 와 reaping(`wait4`, `release_task`), orphan reparenting; pid namespace 와 `struct pid` 의 다단계 매핑(upid)
- **정본**: LKD ch3; ULK ch3, ch20(Program Execution)
- **코드**: `kernel/fork.c`(kernel_clone, copy_process), `fs/exec.c`, `kernel/kthread.c`, `kernel/pid_namespace.c`, `kernel/exit.c`
- **Modern kernel notes**: `_do_fork` → `kernel_clone()` 으로 개명. `clone3()` syscall(5.3+)과 pidfd 기반 프로세스 관리가 추가됨. vfork 는 COW fork 가 충분히 싸져 존재 이유가 약해졌다는 점을 트레이드오프로 다룬다.

### W4 — Process scheduling in Linux

- **서브토픽**: 스케줄러 계보 O(n) → O(1)(2.6 초기) → CFS(2.6.23) → EEVDF(6.6) 와 각 전환의 이유; CFS: vruntime, nice→weight 변환(`sched_prio_to_weight`), min_vruntime, RB-tree leftmost 선택; CFS 의 한계(latency 요구 표현 불가, sleeper fairness 휴리스틱); EEVDF: eligibility(lag ≥ 0), virtual deadline = eligible time + request/weight, latency-nice 문제 해결; sched class 계층(stop→dl→rt→fair→idle)과 `pick_next_task` 순회; RT 정책(SCHED_FIFO/RR)·SCHED_DEADLINE(CBS); context switch(`__schedule`, `context_switch`, `switch_to`)와 비용; preemption 시점(TIF_NEED_RESCHED, user return vs kernel preemption); load balancing·sched domain 개요
- **정본**: LKD ch4; ULK ch7; Stoica & Abdel-Wahab 1995 (<https://people.eecs.berkeley.edu/~istoica/papers/eevdf-tr-95.pdf>); EEVDF 커널 문서 <https://docs.kernel.org/scheduler/sched-eevdf.html>; LWN "An EEVDF CPU scheduler for Linux" <https://lwn.net/Articles/925371/>
- **코드**: `kernel/sched/core.c`, `kernel/sched/fair.c`, `kernel/sched/sched.h`(sched_class), `kernel/sched/rt.c`, `kernel/sched/deadline.c`
- **Modern kernel notes**: LKD ch4 의 CFS 서술은 6.6 에서 **EEVDF 로 교체**됨 — vruntime 은 계승하되 eligibility + virtual deadline 로 재구성. CFS 는 "역사 + EEVDF 가 고친 문제" 프레임으로 다룬다. 6.12 에는 BPF 커스텀 스케줄러용 sched_ext 도 머지. 스케줄러는 단일 `sched.c` 가 아니라 `kernel/sched/` 디렉토리다.

### W5 — Interrupt handling and processing (1)

- **서브토픽**: interrupt vs exception vs trap 분류; IRQ line·interrupt controller(APIC) 와 vector 매핑; top half 설계 원칙(최소 작업, ack + 지연); `request_irq`/`free_irq` 와 IRQF flags(IRQF_SHARED, IRQF_ONESHOT); interrupt context 제약 — sleep 불가·user memory 접근 불가와 그 이유(어느 task 문맥도 아님, 스케줄 불가); handler 실행 경로(`__handle_irq_event_percpu`); shared IRQ 에서 handler 가 자기 device 인지 판별해야 하는 이유; `/proc/interrupts`·`/proc/irq/` 읽기; `local_irq_save`/`local_irq_disable` 와 필요한 상황
- **정본**: LKD ch7; ULK ch4
- **코드**: `kernel/irq/handle.c`, `kernel/irq/manage.c`(request_threaded_irq), `include/linux/interrupt.h`, `arch/x86/kernel/irq.c`
- **Modern kernel notes**: `request_threaded_irq` 가 표준 API 이고 `request_irq` 는 그 wrapper. per-IRQ kernel stack, IRQ domain 계층(디바이스 트리 기반 매핑)은 LKD 이후 추가.

### W6 — Interrupt handling and processing (2)

- **서브토픽**: bottom half 3종 비교표 — softirq(컴파일 타임 정적 등록, 같은 종류가 여러 CPU 동시 실행, 폭주 시 `ksoftirqd` 위임) vs tasklet(softirq 위 구현, 동일 tasklet 직렬화 보장) vs workqueue(process context, sleep 가능); 각각의 선택 기준과 실패 모드(softirq 남용 → userspace starvation); threaded IRQ 의 primary/thread handler 분리와 IRQF_ONESHOT; workqueue 내부: worker pool, CMWQ(concurrency-managed workqueue), `schedule_work` vs 전용 workqueue; locking 함의: `spin_lock_bh`, softirq ↔ process context 공유 데이터
- **정본**: LKD ch8; ULK ch4; workqueue 문서 <https://docs.kernel.org/core-api/workqueue.html>
- **코드**: `kernel/softirq.c`, `kernel/workqueue.c`, `kernel/irq/manage.c`
- **Modern kernel notes**: tasklet 은 deprecated 방향 — 신규 코드는 threaded IRQ 또는 workqueue 권장. workqueue 는 LKD 시절 per-CPU worker thread 모델이 아니라 CMWQ(공유 worker pool + concurrency 관리). **PREEMPT_RT 가 6.12 에서 mainline 완전 머지**(x86/arm64/riscv) — RT 에서는 hard IRQ handler 도 기본 스레드화된다.

### W7 — Time processing in Kernel

- **서브토픽**: tick 과 HZ 선택 트레이드오프(interrupt overhead vs timer granularity vs 전력); `jiffies` 와 wraparound-safe 비교 매크로(`time_after`); timer wheel 구조와 정확도 특성; hrtimers — RB-tree(timerqueue) 기반, `ktime_t`, clockevents 연동, 왜 wheel 과 별도 체계인가; dynamic tick: NO_HZ_IDLE(idle 시 tick 정지) vs NO_HZ_FULL; timekeeping: clocksource(TSC), `ktime_get` 계열, gettimeofday/vDSO; 지연 API 구분 — `schedule_timeout`/`msleep`(sleep) vs `udelay`/`ndelay`(busy-wait) 와 각각 허용되는 문맥
- **정본**: LKD ch11; ULK ch6; timers 문서 <https://docs.kernel.org/timers/>
- **코드**: `kernel/time/timer.c`, `kernel/time/hrtimer.c`, `kernel/time/tick-sched.c`, `kernel/time/timekeeping.c`, `include/linux/jiffies.h`
- **Modern kernel notes**: timer wheel 은 4.8 에서 cascading 을 제거한 설계로 재작성 — 원거리 타이머의 정확도를 의도적으로 희생(대부분의 타임아웃은 만료 전 취소된다는 관찰). NO_HZ 가 기본이므로 LKD 의 "매 tick 마다 jiffies 증가" 서술은 tickless 보정 필요.

### W9 — System call and signal handling

- **서브토픽**: syscall 경로 전체: `syscall` 명령 → `entry_SYSCALL_64`(entry_64.S: swapgs, stack 전환, pt_regs 구성) → `do_syscall_64` → `sys_call_table[nr]` 디스패치 → `sysret`; syscall ABI(rax = number, rdi/rsi/rdx/r10/r8/r9); syscall table 생성(`syscall_64.tbl`)과 새 syscall 추가 절차(`SYSCALL_DEFINEn`); `copy_from_user`/`copy_to_user` 가 필요한 이유(포인터 검증, fault 처리, SMAP); vDSO 로 syscall 을 생략하는 최적화(gettimeofday); signal 전달 모델: 생성(pending set + sigqueue) → 체크 시점(kernel→user 복귀 직전) → user stack 에 핸들러 프레임 설치 → `rt_sigreturn`; blocked mask, SIGKILL/SIGSTOP 특례; signal 과 syscall 재시작(ERESTARTSYS, SA_RESTART)
- **정본**: LKD ch5; ULK ch10(System Calls), ch11(Signals)
- **코드**: `arch/x86/entry/entry_64.S`, `arch/x86/entry/common.c`(do_syscall_64), `arch/x86/entry/syscalls/syscall_64.tbl`, `kernel/entry/common.c`, `kernel/signal.c`
- **Modern kernel notes**: Meltdown 대응 KPTI(4.15+)와 각종 mitigation 으로 syscall entry 가 LKD 시절보다 비쌈. arch 공통 entry 로직은 `kernel/entry/common.c` 로 분리. 64-bit 는 `syscall` 명령 단일 경로이고 `int 0x80` 은 32-bit legacy.

### W10 — Kernel synchronization

- **서브토픽**: race 의 세 근원(SMP 병렬성, kernel preemption, interrupt) 과 각각을 막는 수단; atomic ops(`atomic_t`, RMW, `atomic_cmpxchg`) 와 한계; spinlock — busy-wait 가 유리한 조건(짧은 critical section, interrupt/atomic context), `spin_lock_irqsave` 가 필요한 데드락 시나리오(IRQ handler 와 lock 공유); mutex — sleep, adaptive spinning(optimistic spin), semaphore 와의 구분; reader-writer lock 과 writer starvation; RCU — read-side 무비용, grace period, publish-subscribe(`rcu_assign_pointer`/`rcu_dereference`), `synchronize_rcu` vs `call_rcu`, 언제 RCU 가 정답인가(read-mostly); memory barrier(smp_mb, acquire/release) 가 필요한 이유(컴파일러·CPU reordering); lockdep 의 lock class 와 순서 위반 검출 원리; deadlock 4조건과 lock ordering 규칙
- **정본**: LKD ch9–10; ULK ch5; RCU 문서 <https://docs.kernel.org/RCU/whatisRCU.html>; `Documentation/memory-barriers.txt` (<https://www.kernel.org/doc/Documentation/memory-barriers.txt>)
- **코드**: `kernel/locking/mutex.c`, `kernel/locking/qspinlock.c`, `kernel/rcu/tree.c`, `include/linux/rcupdate.h`, `kernel/locking/lockdep.c`
- **Modern kernel notes**: spinlock 구현은 ticket lock → **qspinlock**(MCS 기반, 4.2+). RCU 는 flavor 통합 후 Tree RCU 단일 체계. PREEMPT_RT(6.12+ mainline) 에서는 spinlock 이 sleeping lock 으로 대체됨. 공식 메모리 모델 LKMM(`tools/memory-model/`)이 존재. BKL(Big Kernel Lock)은 완전 제거된 역사로만 언급.

### W11 — Linux memory management (1)

- **서브토픽**: page frame 과 `struct page` — 왜 페이지당 메타데이터를 유지하나, 그 공간 비용; zone 구분(ZONE_DMA/DMA32/NORMAL/HIGHMEM) 과 존재 이유 — 64-bit 에서 HIGHMEM 이 사라진 이유(선형 매핑으로 전 물리 메모리 커버); buddy allocator — order, free_area, split/coalesce, 외부 단편화 대응; GFP flags 의미론 — GFP_KERNEL(sleep 가능) vs GFP_ATOMIC(reserve 사용) 구분 기준, `__GFP_ZERO`, `__GFP_HIGHMEM`; 할당 인터페이스 `alloc_pages`/`__get_free_pages`/`get_zeroed_page`; per-CPU page lists(pcp) 로 buddy lock 회피; watermark 와 OOM killer 개요
- **정본**: LKD ch12; ULK ch8
- **코드**: `mm/page_alloc.c`, `include/linux/mmzone.h`, `include/linux/gfp_types.h`, `include/linux/mm_types.h`
- **Modern kernel notes**: `struct page` 중심 서술은 **folio**(5.16+) 로 보정 — compound page 의 head/tail 혼동을 타입으로 제거한 것이 folio 이며, page cache·reclaim 은 folio 단위로 동작. GFP flags 정의는 `include/linux/gfp_types.h` 로 분리(6.0+). ZONE_MOVABLE·memory hotplug 은 개요만.

### W12 — Linux memory management (2)

- **서브토픽**: slab 계층의 존재 이유 — buddy 의 page 단위 할당으로는 작은 객체에서 내부 단편화, 객체 초기화 재사용·cache 친화; SLUB 구조 — `kmem_cache`, per-CPU freelist(lockless fastpath), partial list; `kmalloc` 내부(size class 별 kmem_cache); `kmalloc` vs `vmalloc` vs `alloc_pages` 선택 기준 — 물리 연속 vs 가상 연속, vmalloc 의 page table 조작·TLB 비용; `kmem_cache_create` 로 전용 캐시를 만드는 경우(task_struct, inode); page cache 와 writeback 기초 — dirty page 추적, flusher thread, dirty ratio; reclaim 과 LRU(active/inactive) 개요
- **정본**: LKD ch12, ch16(Page Cache and Page Writeback); ULK ch8, ch15, ch17; LWN "remove the SLAB allocator" <https://lwn.net/Articles/951272/>
- **코드**: `mm/slub.c`, `mm/slab_common.c`, `mm/vmalloc.c`, `mm/filemap.c`, `mm/page-writeback.c`
- **Modern kernel notes**: **SLOB 은 6.4, SLAB 은 6.8 에서 제거 — 현대 커널의 allocator 는 SLUB 단일**. LKD 의 SLAB(per-CPU array cache, cache coloring) 서술은 역사로만 다루고 본문은 SLUB 기준으로 쓴다. reclaim 은 multi-gen LRU(6.1+, 선택 기능)까지는 개요만.

### W13 — Process address space management

- **서브토픽**: `mm_struct` 와 주소공간 레이아웃(text/data/heap/mmap area/stack, ASLR); VMA(`vm_area_struct`) — 시작/끝, 권한(vm_flags), anonymous vs file-backed, `vm_operations_struct`; VMA 조회 자료구조와 `find_vma`; `mmap`/`brk` 경로(`do_mmap`, VMA merge); demand paging — page fault 경로: `arch/x86/mm/fault.c`(exc_page_fault) → `handle_mm_fault` → anonymous(zero page)/file-backed(page cache)/COW(do_wp_page)/swap-in 케이스 분기; minor vs major fault 구분; stack 자동 확장(VM_GROWSDOWN); page table 워크(PGD→P4D→PUD→PMD→PTE) 와 TLB; fault 가 SIGSEGV 가 되는 조건(good area/bad area 판정)
- **정본**: LKD ch15; ULK ch9
- **코드**: `include/linux/mm_types.h`(mm_struct, vm_area_struct), `mm/mmap.c`, `mm/memory.c`(handle_mm_fault), `arch/x86/mm/fault.c`, `lib/maple_tree.c`
- **Modern kernel notes**: VMA 컨테이너는 rbtree + 연결 리스트 → **maple tree**(6.1+, RCU-safe B-tree 변형)로 교체 — LKD 의 "rbtree 로 검색, 리스트로 순회" 서술은 구식. page fault 확장성을 위한 per-VMA lock(6.4+)으로 `mmap_lock` 병목 완화. x86-64 는 5-level page table(P4D 실사용) 가능.

### W14 — Understanding the Linux file system (1)

- **서브토픽**: VFS 가 존재하는 이유 — 공통 파일 모델로 이질적 fs 를 단일 syscall 집합 아래 통합; 4대 객체의 수명·소유 관계 — superblock(fs 인스턴스) / inode(파일 메타데이터, on-disk 표현과 분리) / dentry(경로 구성요소, 디스크에 없음) / file(open file 문맥, offset); dentry cache 와 상태(used/unused/negative — negative dentry 가 왜 유용한가); path lookup(`fs/namei.c`) — 성분별 순회, RCU-walk vs ref-walk; file operations 디스패치 — `read()` → `vfs_read` → `f_op->read_iter`; fs 등록·mount(`file_system_type`, `vfs_get_tree`); hard link vs symlink 의 inode 레벨 차이; `struct file` 과 fd table 의 관계(fork 후 공유)
- **정본**: LKD ch13; ULK ch12; VFS 문서 <https://docs.kernel.org/filesystems/vfs.html>
- **코드**: `include/linux/fs.h`, `fs/super.c`, `fs/inode.c`, `fs/dcache.c`, `fs/namei.c`, `fs/read_write.c`, `fs/open.c`
- **Modern kernel notes**: mount 는 fs_context 기반 새 mount API(5.2+)로 재구성. `read`/`write` 의 실제 디스패치는 `read_iter`/`write_iter`(iov_iter 기반)가 표준이고 구식 `->read`/`->write` 는 legacy.

### W15 — Understanding the Linux file system (2)

- **서브토픽**: page cache 를 통한 buffered read 경로(`filemap_read`, cache miss 시 readpage/readahead) 와 write 경로(dirty 마킹 → writeback); `address_space` 객체 — 파일 오프셋 ↔ 캐시 페이지 매핑, `a_ops`; writeback 트리거(dirty ratio, 주기적 flusher, `fsync`) 와 데이터 유실 윈도우; O_DIRECT 의 트레이드오프(캐시 우회, 정렬 제약); 구체 fs 사례 ext4 — 온디스크 레이아웃(block group, superblock, inode table), extent tree 가 간접 블록을 대체한 이유(연속 할당 압축 표현), delayed allocation, journaling 3모드(journal/ordered/writeback) 와 crash consistency 보장 수준; block I/O 계층 개요 — `struct bio`, 요청 병합, I/O scheduler 의 역할
- **정본**: LKD ch13–14(Block I/O), ch16; ULK ch15–16, ch18(ext2/3 기준 → ext4 로 보정); ext4 문서 <https://docs.kernel.org/filesystems/ext4/>
- **코드**: `mm/filemap.c`, `fs/ext4/`, `fs/jbd2/`, `block/`, `fs/buffer.c`
- **Modern kernel notes**: ULK ch18 의 ext2/ext3 는 **ext4**(extent, jbd2, delayed allocation) 기준으로 대체해 서술. page cache 인덱스는 radix tree → XArray, 단위는 folio. block 계층은 단일 request queue → **blk-mq**(multi-queue, 4.x+) 이고 CFQ 등 구식 I/O scheduler 는 제거됨(mq-deadline, BFQ, kyber). LKD ch16 의 pdflush 는 per-BDI flusher 로 대체된 지 오래.

### Lab 시드 (챕터별 `lab/` 출발점)

- **W1**: hello module 빌드·로드 + `printk` 로그 확인 (LKMPG ch4 기반, QEMU 또는 VM 셋업 절차 문서화)
- **W2–3**: `/proc` 에 task 정보를 노출하는 모듈 — `for_each_process` 로 state·pid·comm 덤프; userspace 에서 `clone()` flags 조합 실험
- **W4**: `sched_setattr` 로 정책 바꿔가며 `perf sched` / `/proc/<pid>/sched` 로 vruntime·deadline 관찰
- **W5–7**: workqueue vs tasklet latency 비교 모듈; `hrtimer` 콜백 모듈; `/proc/interrupts`·`/proc/timer_list` 해석
- **W9**: 최소 syscall 추가(빌드된 커널에) 또는 kprobe 로 syscall entry 후킹; `sigaction` 재시작 동작 실험
- **W10**: race 를 실제로 재현하는 모듈(무보호 counter) → spinlock/atomic/RCU 로 각각 고치고 처리량 비교
- **W11–13**: `kmalloc`/`vmalloc` 주소 비교 모듈, `/proc/buddyinfo`·`/proc/slabinfo` 해석, page fault 를 `perf` 로 관측하며 COW 확인
- **W14–15**: 최소 read-only pseudo-fs 등록 모듈 또는 `debugfs` 실습; `dumpe2fs`/`debugfs(8)` 로 ext4 온디스크 구조 확인

## 4. 예습 우선순위 (챕터 생성 순서)

의존 관계 기준. 화살표는 "먼저 만들어야 뒤가 쉬움".

1. **W1** — module build·실행 환경(QEMU/VM + LKMPG 툴체인)이 이후 모든 lab 의 기반. 셋업 문서화 포함해 최우선.
2. **W2 → W3** — `task_struct` 는 scheduling(W4)·signal(W9)·address space(W13) 전부의 선행 개념.
3. **W4** — W2–3 직후. EEVDF 는 교재(CFS)와 현대 커널의 격차가 가장 큰 주제라 검증 작업량이 가장 많다.
4. **W5 → W6 → W7** — interrupt context 개념(W5)이 bottom half(W6)로, softirq 가 timer(W7)로 직결되는 사슬.
5. **W10** — synchronization 은 W4 의 preemption·W5–6 의 interrupt context 를 전제로 해야 동기 부여가 서고, 역으로 이후 mm·VFS 서술(RCU-walk, per-VMA lock)이 W10 용어를 쓴다. 중간고사 범위(W1–7) 완료 직후 첫 생성 대상.
6. **W9** — 상대적으로 독립적. W2–3(task_struct, fork) 만 선행하면 됨.
7. **W11 → W12 → W13** — buddy/GFP(W11) 없이 slab(W12)을, 둘 없이 page fault 할당 경로(W13)를 설명할 수 없다. 순서 고정.
8. **W14 → W15** — VFS 객체 모델(W14)이 page cache I/O 경로·ext4(W15)의 전제. W15 는 W12 의 page cache 기초도 참조.

요약 생성 순서: **W1 → W2 → W3 → W4 → W5 → W6 → W7 → W10 → W9 → W11 → W12 → W13 → W14 → W15**. 계획서 진도 순서와 거의 같지만, W10(synchronization)을 W9 보다 먼저 만드는 것이 이후 주차의 참조 관계상 효율적이다.
