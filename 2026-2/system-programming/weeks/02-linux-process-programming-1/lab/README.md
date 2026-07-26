# Week 02 Lab — Observing `task_struct`, fork/COW, clone flags

두 부분으로 구성된다:

- **Part A (userspace/)** — fork/exec/wait, COW 관찰, `clone()` flags 실험. Linux 전용 (`clone(2)`, `/proc`) 이므로 **macOS 에서는 빌드/실행 불가** — [Week 00 lab setup](../../00-lab-setup/README.md) 의 Lima VM 안에서 실행한다.
- **Part B (module/)** — `for_each_process` 로 task 리스트를 순회하는 kernel module. 역시 VM 안에서 빌드/로드한다.

> **검증 상태**: 이 코드는 kernel 6.x API (v6.12 소스에서 확인한 `__state`/`task_state_to_char`/`for_each_process` 등) 기준으로 작성했으나, 이 저장소를 만든 머신에는 VM 이 없어 **실행 검증은 아직 안 됐다**. VM 셋업(Week 00) 후 첫 실행에서 문제가 있으면 이 README 에 기록할 것.

## Part A — userspace

### 빌드

```bash
cd lab/userspace
make          # cc -Wall -Wextra -O2 로 3개 바이너리 생성
```

### A-1. `fork_exec_wait` — 생명주기와 zombie 육안 확인

```bash
./fork_exec_wait
```

하는 일: ① 즉시 `_exit(42)` 하는 자식을 fork 하고 **일부러 wait 를 늦춰** 그 사이 `ps` 로 자식의 state 를 찍는다 → `Z` (zombie) 가 보여야 한다. ② `waitpid()` 로 reap 후 다시 `ps` → 프로세스가 사라졌고 exit code 42 를 수거했음을 출력. ③ fork + `execlp("uname -sr")` + wait 의 표준 패턴.

예상 출력 (pid 는 다름):

```
parent: pid=1234
--- before wait(): expect state Z (zombie) ---
    PID    PPID S COMMAND
   1235    1234 Z fork_exec_wait
reaped zombie 1235: exit code=42 (WIFEXITED=1)
--- after wait(): the pid is gone ---
child 1236 ran 'uname -sr', exit status=0
```

챕터 연결: §10 — zombie 는 `exit_state = EXIT_ZOMBIE` 로 남아 있다가 `wait4()` → `release_task()` 로 소멸.

### A-2. `cow_observe` — COW 를 숫자로 잡기

```bash
./cow_observe
```

64 MiB 버퍼를 touch 한 뒤 fork 하고, 자식이 **읽기만 할 때 / 절반 write / 전부 write** 각 시점에서 다음을 스냅샷한다:

- `/proc/self/statm` 의 resident (RSS)
- `/proc/self/smaps_rollup` 의 `Shared_Dirty` / `Private_Dirty`
- `getrusage()` 의 `ru_minflt` (minor fault 카운트)

예상 관찰 (page size 4 KiB 기준):

| 시점 | 예상 |
|---|---|
| parent before fork | Private_Dirty ≈ 64 MiB (내 페이지) |
| child after fork, 읽기만 | RSS 는 이미 ≈64 MiB 이지만 **Shared_Dirty ≈ 64 MiB** — 부모와 물리 페이지 공유 중. minflt 거의 0 (fork 가 PTE 를 복사해줬으므로 읽기는 fault 없음) |
| child after write half | **minflt 가 ~8192 (= 32 MiB / 4 KiB) 증가** — write 마다 COW fault. Private_Dirty +32 MiB, Shared_Dirty −32 MiB |
| child after write all | minflt 누적 ~16384, Private_Dirty ≈ 64 MiB, Shared_Dirty ≈ 0 |
| parent after child exit | 다시 Private_Dirty ≈ 64 MiB (공유 상대가 사라져 mapcount=1) |

챕터 연결: §7 — "fork 는 페이지를 복사하지 않는다. write fault 횟수(= minflt 증가분)가 곧 이연된 복사 횟수다."

### A-3. `clone_flags` — CLONE_VM / CLONE_FILES 직접 실험

```bash
./clone_flags
```

`clone(2)` 를 mmap 으로 만든 별도 스택과 함께 직접 호출한다. 세 가지 실험:

1. **flags = SIGCHLD (fork 등가)**: 자식이 전역 counter 에 +1000 → 부모에는 안 보임 (COW 로 격리).
2. **CLONE_VM**: 같은 write 가 부모에 보임 — 주소공간 공유. 단 자식 pid 는 다르다 (CLONE_THREAD 없음 → 별개 process 가 메모리만 공유하는 기묘한 중간형).
3. **CLONE_VM | CLONE_FILES**: 자식이 `open("/dev/null")` 한 fd 번호로 부모가 곧바로 `write()` 성공. CLONE_VM 만 있을 때는 같은 fd 번호가 부모의 fd table 에 없어 `EBADF`.

예상 출력 골자:

```
[exp1 fork-like  ] clone returned pid=... | parent view: counter=0, pid_seen_by_child=-1   (isolated mm: child writes invisible)
[exp2 CLONE_VM   ] clone returned pid=... | parent view: counter=1000, pid_seen_by_child=...  (shared mm)
[exp3 VM only    ] child opened fd=3 | parent write(fd) -> Bad file descriptor   (separate fd table)
[exp3 VM|FILES   ] child opened fd=3 | parent write(fd) -> ok      (shared fd table)
```

(fd 번호·pid 는 환경에 따라 다르다.)

챕터 연결: §5, §11 — process/thread 스펙트럼은 CLONE flags 의 조합 공간이다. `pthread_create` 는 여기에 CLONE_THREAD|SIGHAND 등을 더 얹은 한 점일 뿐이다. (CLONE_THREAD 자체는 `waitpid` 로 기다릴 수 없어 — thread 는 자식이 아니라 형제가 된다 — 이 lab 에선 다루지 않는다.)

## Part B — kernel module: `taskdump`

`for_each_process()` 로 전체 process(thread group leader)를 순회하며 pid/tgid/state/comm/부모/thread 수를 dmesg 로 출력하고, `current` 매크로가 module 코드에서 어떻게 동작하는지 확인한다.

### 빌드·실행 (VM 안에서)

```bash
cd lab/module
make                          # 커널 헤더 필요 — Week 00 셋업 참조
sudo insmod taskdump.ko
sudo dmesg | tail -40
sudo rmmod taskdump
sudo dmesg | tail -5
```

### 예상 출력 골자

```
taskdump: loaded by "insmod" (pid 2301, tgid 2301)   ← current == insmod 를 실행한 task
taskdump: sizeof(task_struct)=..., THREAD_SIZE=16384
taskdump: pid=1     tgid=1     state=S     comm=systemd          threads=1  parent=swapper/0(0)
taskdump: pid=2     tgid=2     state=S [K] comm=kthreadd         threads=1  parent=swapper/0(0)
taskdump: pid=...   ...        state=I [K] comm=kworker/...      ...        parent=kthreadd(2)
...
taskdump: walked N thread-group leaders, M threads total
taskdump: unloaded by "rmmod" (pid ...)
```

확인 포인트:

- **PID 1 과 PID 2 가 두 뿌리**: user process 는 systemd(1) 계열, `[K]` 마크(= `PF_KTHREAD`)가 붙은 것들은 전부 kthreadd(2) 자손 (§4, §9).
- state 문자는 `task_state_to_char()` (v6.12 `include/linux/sched.h` 의 static inline — `__state` 와 `exit_state` 를 합쳐 판정) 사용. kernel thread 다수가 `I` (TASK_IDLE = UNINTERRUPTIBLE|NOLOAD) 인 것 확인.
- 순회는 `rcu_read_lock()` 아래에서 — task 리스트는 RCU 로 보호된다 (W10 예고).
- `current->comm` 이 init 시 `insmod`, exit 시 `rmmod` 인 것: `current` 는 "그 순간 이 커널 코드를 실행 중인 task" 다 — module 에 전용 thread 가 있는 게 아니다.

### 주의

- `MODULE_LICENSE("GPL")` 필수 (없으면 GPL-only 심볼 사용 불가 + kernel taint).
- Ubuntu 는 `kernel.dmesg_restrict=1` 이 기본이라 `dmesg` 에 sudo 필요.
- 출력 줄 수가 많으니 콘솔 로그 레벨에 따라 `journalctl -k` 가 편할 수 있다.
