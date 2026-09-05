# Week 02 — Active Recall Quiz

답을 가리고 스스로 말해본 뒤 확인할 것. 핵심 용어는 영어로 답하는 연습을 한다.

**Q1.** Linux 커널에서 process 와 thread 를 구분하는 별도 자료구조가 있는가?

**A1.** 없다. 둘 다 `task_struct` 하나로 표현되며, 차이는 clone 시 CLONE_* flags 로 어떤 자원(`mm`, `files`, `sighand`, `signal` 등)을 공유했는가뿐이다.

**Q2.** `task_struct` 에서 자원(`mm`, `files`, `fs`, `signal`, `sighand`)이 전부 포인터인 설계상의 이유는?

**A2.** 여러 task 가 같은 자원 구조체를 refcount 로 공유할 수 있게 하기 위해. 이 공유 가능성이 thread = "자원 공유하는 task" 라는 통일 모델의 기반이다.

**Q3.** `getpid()` 와 `gettid()` 는 각각 `task_struct` 의 어느 값을 반환하나?

**A3.** `getpid()` → `tgid` (thread group ID, `task_tgid_vnr`), `gettid()` → `pid` (task 고유 번호, `task_pid_vnr`). 구현은 `kernel/sys.c`.

**Q4.** 5.14 에서 `task_struct` 의 `state` 필드는 무엇으로 개명됐고, 값을 읽는 권장 헬퍼는?

**A4.** `__state` 로 개명. 직접 접근 대신 `set_current_state()`, `task_state_to_char()`, `READ_ONCE(p->__state)` 같은 헬퍼 사용.

**Q5.** `TASK_RUNNING` 상태의 정확한 의미는?

**A5.** "runnable" — CPU 에서 실행 중이거나 runqueue 에서 대기 중. Linux 는 ready 와 running 을 `__state` 로 구분하지 않는다.

**Q6.** `TASK_INTERRUPTIBLE` vs `TASK_UNINTERRUPTIBLE` vs `TASK_KILLABLE` 차이는?

**A6.** INTERRUPTIBLE 은 signal 로 깨어남(S). UNINTERRUPTIBLE 은 signal 완전 무시(D) — I/O 중간 상태 보호용. KILLABLE = `TASK_WAKEKILL | TASK_UNINTERRUPTIBLE` — fatal signal(SIGKILL)만 허용하는 절충.

**Q7.** zombie 상태는 `__state` 와 `exit_state` 중 어디에 기록되나? 값은?

**A7.** `exit_state = EXIT_ZOMBIE` (0x20). reaping 후 최종 상태는 `EXIT_DEAD`.

**Q8.** sleep 관용구에서 `set_current_state(TASK_INTERRUPTIBLE)` 를 조건 검사보다 먼저 하는 이유는?

**A8.** 조건 검사 후 상태를 바꾸면 그 틈에 다른 CPU 가 조건을 만족시키고 `wake_up()` 을 호출해버려 wakeup 을 놓치는 **lost wakeup race** 가 생긴다.

**Q9.** 현대 x86 에서 `current` 매크로는 어떻게 구현되나?

**A9.** per-CPU 변수 읽기: `this_cpu_read_stable(pcpu_hot.current_task)` (`arch/x86/include/asm/current.h`). context switch 때 갱신된다. LKD 의 "stack pointer 마스킹 → thread_info" 방식은 구식.

**Q10.** `CONFIG_THREAD_INFO_IN_TASK` 가 해결한 문제는?

**A10.** kernel stack 하단의 `thread_info` 는 stack overflow 시 가장 먼저 오염되는 급소였다. `thread_info` 를 `task_struct` 의 첫 멤버로 옮겨 이 취약점을 제거했고, vmalloc 기반 guard-page 스택(`CONFIG_VMAP_STACK`)과도 궁합이 맞다.

**Q11.** x86-64 kernel stack 크기와, 그 크기가 코드 작성에 주는 제약은?

**A11.** `THREAD_SIZE` = 16 KiB (PAGE_SIZE << 2), 자동 확장 없음. 커널 코드에서 큰 지역 배열/깊은 재귀 금지.

**Q12.** `fork()`, `vfork()`, `clone()`, `pthread_create()`, `kthread_create()` 의 공통 수렴 지점은?

**A12.** 전부 `kernel_clone(struct kernel_clone_args *)` (`kernel/fork.c`, 구 `_do_fork`) → `copy_process()`. 차이는 넘기는 flags 뿐.

**Q13.** `copy_process()` 가 강제하는 CLONE flag 함의 사슬과 각 근거는?

**A13.** `CLONE_THREAD ⇒ CLONE_SIGHAND ⇒ CLONE_VM`. thread group 은 process-wide signal 의미론상 handler 공유가 필수이고, handler 는 user 주소공간의 함수 포인터라 주소공간 공유 없이는 무의미하다.

**Q14.** `copy_sighand()` 류 `copy_*` 함수들의 공통 패턴은?

**A14.** 해당 CLONE flag 가 있으면 `refcount_inc` 로 **공유**, 없으면 새 구조체 할당 후 내용 **복제**. (copy_files→CLONE_FILES, copy_fs→CLONE_FS, copy_signal→CLONE_THREAD, copy_mm→CLONE_VM)

**Q15.** 자식 프로세스에서 fork() 의 반환값이 0 이 되는 메커니즘은?

**A15.** arch 별 `copy_thread()` 가 자식 kernel stack 의 저장된 user 레지스터 프레임에서 `childregs->ax = 0` 으로 설정 (`arch/x86/kernel/process.c`). 자식이 처음 스케줄되면 syscall 반환 경로에서 그 프레임을 복원하므로 0 을 "반환받는다".

**Q16.** fork 직후 자식의 상태 전이는? (생성~실행 가능까지)

**A16.** `sched_fork()` 가 `p->__state = TASK_NEW` 설정 → `copy_process()` 완료 후 `kernel_clone()` 이 `wake_up_new_task()` 호출 → `TASK_RUNNING` 으로 전이되어 runqueue 진입.

**Q17.** COW fork 에서 실제로 복사되는 것과 안 되는 것은?

**A17.** 복사: VMA 메타데이터 + 페이지 테이블(PTE). 비복사: 데이터 페이지 (양쪽 PTE 를 write-protect 하고 같은 물리 페이지 공유). anonymous 페이지 없는 file-backed VMA 는 페이지 테이블 복사도 생략 (`vma_needs_copy`).

**Q18.** COW 페이지에 write 가 발생하면 커널 경로는?

**A18.** write-protect fault → fault handler 가 "VMA 는 writable, PTE 는 아님" 확인 → `do_wp_page()` (`mm/memory.c`) → 단독 사용이면 PTE 재-writable(reuse), 공유 중이면 `wp_page_copy()` 로 새 페이지 할당·복사·PTE 교체 → 명령 재실행. userspace 에는 minor fault 로만 관측된다.

**Q19.** vfork 의 원래 존재 이유와, 현대에 존재 이유가 약해진 까닭은?

**A19.** eager-copy fork 시절 "fork 후 즉시 exec" 패턴의 복사 낭비를 없애려고 주소공간 공유(`CLONE_VM`) + 부모 블록(`CLONE_VFORK`)으로 설계. COW 도입 후 fork 비용이 페이지 테이블 복사 수준으로 떨어져 이득이 미미해졌고 위험(부모 주소공간 오염)만 남았다.

**Q20.** execve 경로에서 "point of no return" 은 어디이고 왜 그렇게 부르나?

**A20.** `begin_new_exec()` (`fs/exec.c`). `de_thread()` 로 다른 thread 를 모두 제거하고 `exec_mmap()` 으로 옛 `mm_struct` 를 파괴·교체하므로, 이후 실패해도 옛 프로그램으로 복귀 불가 — 실패 시 task 는 죽는 수밖에 없다.

**Q21.** exec 후에도 유지되는 것 세 가지와 리셋되는 것 두 가지를 들라.

**A21.** 유지: pid/tgid, 부모 관계, CLOEXEC 아닌 fd, cwd/umask. 리셋: 주소공간(전면 교체), catch 하던 signal handler 는 SIG_DFL 로 (ignore 는 유지).

**Q22.** 모든 kernel thread 의 부모가 `kthreadd`(PID 2)인 이유는?

**A22.** 호출자 문맥에서 직접 clone 하면 호출자의 namespace/cgroup/rlimit 등을 상속해 오염된다. 요청을 `kthread_create_list` 에 걸고 kthreadd 가 대신 clone 하게 하여 모든 kernel thread 가 균일한 clean context 를 상속하게 한다.

**Q23.** kernel thread 를 일반 process 와 구분하는 두 가지 표식은?

**A23.** `p->flags & PF_KTHREAD`, 그리고 `p->mm == NULL` (user 주소공간 없음; 실행 중엔 직전 task 의 mm 을 `active_mm` 으로 빌리는 lazy TLB).

**Q24.** 고아(orphan) process 의 새 부모를 찾는 우선순위는?

**A24.** ① 같은 thread group 의 살아있는 다른 thread → ② 가장 가까운 조상 subreaper (`PR_SET_CHILD_SUBREAPER`) → ③ 해당 pid namespace 의 `child_reaper`(init). `find_new_reaper()` (`kernel/exit.c`). "무조건 PID 1" 은 현대 커널에선 부정확.

**Q25.** zombie 가 즉시 생기지 않는 경우(autoreap)는?

**A25.** 부모가 SIGCHLD 를 `SIG_IGN` 했거나 `SA_NOCLDWAIT` 를 설정한 경우. `exit_notify()` 가 `EXIT_ZOMBIE` 를 건너뛰고 바로 `release_task()` (`exit_state = EXIT_DEAD`).

---

## From lecture (2026-09-05 강의 기반)

**Q26.** 강의에서 소개한 kernel stack 크기(8KB)와 이 챕터 §2의 THREAD_SIZE(16 KiB)가 다른 이유는?

**A26.** 서로 다른 시대·아키텍처 기준이기 때문. 강의의 8KB는 32비트 x86·Linux 2.6.11 시절 수치(`THREAD_SIZE 8192`, 4KB 페이지 2개)이고, 이 챕터의 16 KiB는 현대 x86-64 기준(`PAGE_SIZE << THREAD_SIZE_ORDER`, order=2)이다. 시험 답안에는 현대 x86-64 기준 16 KiB를 쓸 것.

**Q27.** 강의에서 프로세스 리스트 순회 매크로로 언급한 `for_each_task`가 최신 커널에서는 뭐라고 불리나?

**A27.** `for_each_process` (`include/linux/sched/signal.h`). `for_each_task`는 2.6.11 시절 이름이며 동작(다음 태스크 포인터를 따라 `init_task`까지 순회)은 동일하다.

**Q28.** "process와 thread의 차이는 무엇을 공유하느냐뿐"이라는 결론을 강의는 개념적으로 어떻게 설명했나?

**A28.** process = process context + (code, data, stack) 전부 자기 것. thread가 있으면 code·data·kernel context는 공유하고 stack만 스레드별로 따로 갖는다는 식으로, CLONE flag를 언급하지 않고 "무엇을 공유하는가"라는 사용자 레벨 직관으로 먼저 도입했다 (이후 소스 레벨의 CLONE_* 사슬은 이 챕터 §6에서 다룸).

---

## Anki import (TSV)

```tsv
Linux 커널에서 process 와 thread 를 구분하는 자료구조는?	없음 — 둘 다 task_struct. 차이는 CLONE_* flags 로 공유한 자원뿐
getpid() 와 gettid() 가 반환하는 task_struct 필드는?	getpid() → tgid (thread group ID), gettid() → pid (kernel/sys.c)
task_struct 의 state 필드는 5.14 에서 무엇으로 개명?	__state (헬퍼: set_current_state, task_state_to_char)
TASK_RUNNING 의 정확한 의미는?	runnable — 실행 중이거나 runqueue 대기 중 (ready/running 미구분)
TASK_KILLABLE 의 정의와 목적은?	TASK_WAKEKILL | TASK_UNINTERRUPTIBLE — D state 이지만 SIGKILL 은 허용하는 절충
zombie 는 어느 필드에 어떤 값으로 기록되나?	exit_state = EXIT_ZOMBIE (0x20); reap 후 EXIT_DEAD
sleep 관용구에서 상태 설정을 조건 검사보다 먼저 하는 이유?	lost wakeup race 방지 — 조건 성립+wake_up 이 상태 변경 전에 끼어들 수 있음
현대 x86 에서 current 매크로 구현은?	per-CPU 변수 읽기: this_cpu_read_stable(pcpu_hot.current_task) (arch/x86/include/asm/current.h)
CONFIG_THREAD_INFO_IN_TASK 가 해결한 문제는?	stack overflow 시 stack 하단 thread_info 오염 — thread_info 를 task_struct 첫 멤버로 이동
x86-64 kernel stack 크기와 제약은?	THREAD_SIZE = 16 KiB 고정, 자동 확장 없음 → 큰 지역 배열 금지
fork/vfork/clone/pthread_create/kthread_create 의 공통 수렴 지점은?	kernel_clone() → copy_process() (kernel/fork.c, 구 _do_fork)
fork() 가 넘기는 clone flags 는?	flags = 0, .exit_signal = SIGCHLD 뿐 — 아무 자원도 공유하지 않는 clone
copy_process() 의 CLONE flag 함의 사슬은?	CLONE_THREAD ⇒ CLONE_SIGHAND ⇒ CLONE_VM (handler 는 주소공간 내 함수 포인터, thread group 은 signal 공유 필수)
copy_* 함수들의 공통 패턴은?	flag 있으면 refcount_inc 로 공유, 없으면 새로 할당 후 복제
자식에서 fork() 반환값이 0 인 메커니즘은?	copy_thread() 가 자식의 저장된 레지스터에 childregs->ax = 0 설정
fork 직후 자식의 상태 전이는?	sched_fork: TASK_NEW → wake_up_new_task: TASK_RUNNING
COW fork 에서 복사되는 것은?	VMA 메타데이터 + 페이지 테이블만. 데이터 페이지는 양쪽 write-protect 후 공유
COW 페이지 write 시 커널 경로는?	write fault → do_wp_page → (공유 중이면) wp_page_copy 로 새 페이지 복사 후 PTE 교체
vfork 가 쇠퇴한 이유는?	COW 로 fork 가 페이지 테이블 복사 수준으로 싸져 이득 소멸, 부모 주소공간 오염 위험만 잔존
exec 의 point of no return 은?	begin_new_exec() — de_thread 로 타 thread 제거 + exec_mmap 으로 옛 mm 파괴, 복귀 불가
exec 에서 살아남는 것 / 리셋되는 것 예시	유지: pid, 부모, non-CLOEXEC fd, cwd / 리셋: 주소공간, caught handler → SIG_DFL
모든 kernel thread 가 kthreadd(PID 2) 자식인 이유는?	호출자 속성(namespace/cgroup 등) 상속 오염 방지 — clean context 를 가진 단일 조상에서만 clone
kernel thread 의 두 가지 표식은?	PF_KTHREAD flag, mm == NULL (active_mm 을 빌리는 lazy TLB)
orphan 의 새 부모 우선순위는?	같은 thread group 생존 thread → 가장 가까운 subreaper → pid namespace 의 init (find_new_reaper)
autoreap 조건은?	부모가 SIGCHLD 를 SIG_IGN 또는 SA_NOCLDWAIT — zombie 건너뛰고 즉시 release_task
pthread_create 의 clone flags 조합은?	CLONE_VM|FS|FILES|SIGHAND|THREAD|SYSVSEM|SETTLS|PARENT_SETTID|CHILD_CLEARTID
```
