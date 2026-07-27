# Week 01 — Active Recall Quiz

답을 가리고 스스로 말해본 뒤 확인할 것. 핵심 용어는 영어로 답하는 연습을 한다.

**Q1.** kernel mode 와 user mode 를 가르는 하드웨어 메커니즘 두 가지는?

**A1.** ① CPU privilege level — x86 ring 0(kernel) vs ring 3(user), 특권 명령은 ring 0 전용. ② 페이지 테이블의 U/S(User/Supervisor) 비트 — 커널 페이지는 supervisor 전용 매핑이라 user mode 접근 시 page fault.

**Q2.** mode switch 와 context switch 의 차이를 한 문장씩으로?

**A2.** mode switch = **같은 task** 의 privilege level 전환 (syscall/interrupt/exception 으로 ring 3↔0). context switch = scheduler 가 **CPU 를 점유한 task 자체**를 교체하는 것.

**Q3.** userspace 코드가 커널로 진입하는 세 경로와 각각의 동기성은?

**A3.** system call(자발적·동기), interrupt(하드웨어발·비동기 — 실행 중 명령과 무관), exception(내 명령이 유발·동기, 예: page fault).

**Q4.** syscall 실행 중인 커널 코드는 어떤 문맥·어떤 스택 위에서 도는가?

**A4.** 호출한 프로세스의 **process context**, 그 task 의 kernel stack(x86-64 에서 16 KiB) 위. 커널은 요청을 받는 별도 프로세스가 아니다.

**Q5.** monolithic kernel 과 microkernel 의 핵심 구조 차이와 각각의 대표 비용/이득은?

**A5.** monolithic: 모든 서비스가 한 커널 주소공간 — 내부 호출이 function call 이라 빠르지만 no isolation. microkernel: 서비스를 user-space server 로 분리, message passing(IPC)으로 통신 — isolation 을 얻는 대신 IPC 왕복 비용.

**Q6.** Liedtke SOSP'93 의 핵심 측정치와 논지는?

**A6.** i486-DX50 에서 8-byte IPC 편도(one-way): Mach 115 µs vs 자작 L3 5.2 µs (22배 — ping-pong 10,000회의 총 시간을 20,000 으로 나눈 편도 값). 논지: microkernel 이 원리적으로 느린 게 아니라 Mach 구현이 느린 것 — IPC 를 커널의 제1원칙으로 설계하면 회수 가능 (→ L4 계열).

**Q7.** macOS 의 XNU 를 "hybrid" 라 부르는 이유는?

**A7.** CMU Mach 기반(task/thread/port 추상화 유지)이지만 BSD 계층과 IOKit 드라이버를 **커널 주소공간 안에** 함께 두어 서비스 간 IPC 비용을 회피했기 때문. microkernel 의 구조 + monolithic 의 배치.

**Q8.** loadable module 은 monolithic 의 어떤 약점을 해결하고 어떤 약점은 못 해결하나?

**A8.** 해결: 정적 단일 이미지 문제 — 런타임에 코드를 링크/제거(insmod/rmmod)해 재부팅·재빌드 없이 확장. 미해결: isolation — module 도 같은 주소공간·ring 0 에서 돌아 버그가 커널 전체를 죽인다.

**Q9.** v6.12 트리에서 scheduler, buddy allocator, VFS, x86 syscall entry, task_struct 정의는 각각 어느 디렉토리?

**A9.** `kernel/sched/`, `mm/`(page_alloc.c), `fs/`, `arch/x86/entry/`, `include/linux/sched.h`.

**Q10.** Kconfig 와 Kbuild 의 역할 분담은?

**A10.** Kconfig = "무엇을 넣을지" — 옵션 정의(tristate y/m/n, depends on/select), 결과는 `.config`. Kbuild = "어떻게 빌드할지" — `obj-$(CONFIG_FOO) += foo.o` 가 y→vmlinux 링크, m→module 빌드, n→제외로 라우팅.

**Q11.** tristate 의 y / m / n 의미와, y 가 강제되는 대표 상황은?

**A11.** y=built-in(커널 이미지에 링크), m=loadable module(.ko), n=빌드 제외. initramfs 없이 root fs 를 마운트해야 하는 드라이버처럼 **부팅 시점부터 존재해야 하는 코드**는 y 강제.

**Q12.** vmlinux 와 bzImage 의 차이는? bzImage 의 bz 는 무슨 뜻?

**A12.** vmlinux = 트리 루트의 비압축 ELF(심볼 포함, 디버깅용) — bootloader 가 직접 못 쓴다. bzImage = 실모드 setup + self-extracting stub + 압축 커널의 부팅용 이미지(`arch/x86/boot/`). bz = "big zImage"(메모리 상위 로드) — bzip2 아님.

**Q13.** `module_init(fn)` 은 built-in 빌드와 module 빌드에서 각각 무엇으로 전개되나?

**A13.** built-in: `__initcall(fn)` — 부팅 중 `do_initcalls()` 가 호출. module: `init_module` 이라는 표준 심볼의 alias — 로더가 `mod->init` 으로 잡아 `do_one_initcall()` 로 호출. built-in 에서 `module_exit` 는 no-op.

**Q14.** module 로드 상태 기계(MODULE_STATE_*)의 전이 순서는?

**A14.** UNFORMED(할당·목록 등록) → COMING(심볼 해결·재배치 완료) → LIVE(init 이 0 반환) / init 실패 시 COMING → GOING 으로 되감아 로드 실패. 언로드는 LIVE → GOING → 해제.

**Q15.** insmod 시 module 파라미터(`foo=3`)는 언제 파싱되나? 그 근거 관찰은?

**A15.** `load_module()` 후반의 `parse_args()` — **init 함수 실행 전**. 그래서 init 이 파라미터 값을 볼 수 있고, `/sys/module/<name>/parameters/` 노드도 로드 시점에 생긴다.

**Q16.** vermagic 이 무엇이고 언제 검사되나?

**A16.** `.ko` 의 `.modinfo` 에 박힌 "빌드 대상 커널 버전+SMP/preempt 플래그" 문자열. 로드 초기 ELF/modinfo 검증 단계에서 실행 중 커널과 비교, 불일치면 `-ENOEXEC` 거부 — 다른 커널용 .ko 를 못 꽂는 이유.

**Q17.** `EXPORT_SYMBOL` vs `EXPORT_SYMBOL_GPL` 의 차이와 집행 지점은?

**A17.** 전자는 모든 module 에, 후자는 GPL-compatible license module 에만 링크 허용. 집행은 `resolve_symbol()`(kernel/module/main.c) — proprietary taint module 은 `gplok=false` 로 검색해 GPL-only 심볼이 숨겨진다.

**Q18.** `MODULE_LICENSE` 를 빼먹으면 어떻게 되나?

**A18.** license "unspecified" 취급 → GPL-incompatible → `module license '...' taints kernel` 경고와 함께 TAINT_PROPRIETARY_MODULE('P') 세팅, EXPORT_SYMBOL_GPL 심볼 사용 불가.

**Q19.** kernel taint 란 무엇이고, 우리 lab module 이 항상 받는 taint 는?

**A19.** "이 커널 상태를 upstream 이 보증 못 함"을 기록하는 플래그 집합(`/proc/sys/kernel/tainted`) — oops 리포트에 찍혀 버그 리포트 신뢰도를 결정. out-of-tree 빌드라서 'O'(TAINT_OOT_MODULE, bit 12)는 항상 받는다.

**Q20.** insmod 와 modprobe 의 차이는?

**A20.** insmod = 지정한 .ko 파일 하나를 그대로 로드. modprobe = `modules.dep`(depmod 생성)로 **의존 module 을 먼저** 로드하고 이름만으로 `/lib/modules/$(uname -r)/` 에서 탐색. 실무 표준은 modprobe.

**Q21.** 커널 코드의 4대 제약은? (userspace C 와 다른 점)

**A21.** ① no libc(printf/malloc 없음 — printk/kmalloc), ② 작은 고정 kernel stack(16 KiB, 자동 확장 없음), ③ FPU 기본 사용 불가(kernel_fpu_begin/end 필요), ④ 자기 보호 없음(잘못된 접근 = oops/panic).

**Q22.** printk log level 체계와 콘솔 출력 조건은?

**A22.** 0(KERN_EMERG)~7(KERN_DEBUG), 낮을수록 긴급. 메시지는 링 버퍼(dmesg)로 가고, **메시지 레벨 < console_loglevel**(`/proc/sys/kernel/printk` 첫 값)이면 콘솔에도 출력. 현대 표기는 pr_info()/pr_err() 계열.

**Q23.** rest_init() 이 PID 1 을 PID 2 보다 먼저 만드는 이유와, 그로 인한 동기화 장치는?

**A23.** init 이 pid **1** 을 받아야 하므로 먼저 생성. 그러나 kernel_init 이 kthread 를 만들려면 kthreadd 가 필요 → kernel_init 은 `kthreadd_done` completion 을 기다리고, rest_init 이 kthreadd(PID 2) 생성 후 complete() 로 풀어준다. 부팅 문맥 자신은 PID 0 idle task(swapper) 로 은퇴.

**Q24.** kernel_init 이 시도하는 init 실행 파일 순서와 전부 실패 시 결과는?

**A24.** initramfs `/init` → 커맨드라인 `init=` 값 → `/sbin/init` → `/etc/init` → `/bin/init` → `/bin/sh`. 전부 실패하면 `panic("No working init found. ...")`. 단 `init=` 로 **명시한** 프로그램의 exec 이 실패하면 다음 후보 없이 즉시 `panic("Requested init %s failed (error %d).")`.

**Q25.** 커널 릴리스 모델에서 merge window·-rc·stable·LTS 를 각각 한 줄로?

**A25.** merge window = 릴리스 직후 2주, 신기능 유입 기간. -rc = 그 후 주 단위 안정화 후보(보통 rc6~rc9 에서 릴리스, 전체 주기 2~3개월). stable = 릴리스 후 버그픽스만 backport 하는 6.12.y 시리즈. LTS = 수년 유지되는 지정 시리즈(예: 6.12, EOL 2028-12 예정) — 이 과목의 기준 트리.

---

## Anki TSV

```tsv
kernel mode 와 user mode 를 가르는 하드웨어 메커니즘 2가지	CPU privilege level (x86 ring 0 vs ring 3, 특권 명령은 ring 0 전용) + 페이지 테이블 U/S 비트 (커널 페이지는 supervisor 전용)
mode switch vs context switch	mode switch = 같은 task 의 ring 3↔0 전환 (syscall/interrupt/exception). context switch = scheduler 가 실행 task 자체를 교체
커널 진입 세 경로와 동기성	syscall (자발·동기), interrupt (하드웨어·비동기), exception (내 명령 유발·동기, 예: page fault)
syscall 중 커널 코드가 도는 문맥	호출 프로세스의 process context, 그 task 의 kernel stack (x86-64 16 KiB) 위. 커널은 별도 프로세스가 아님
monolithic vs microkernel 한 줄 비교	monolithic: 한 주소공간, function call, 빠름, no isolation. microkernel: user-space server + IPC, isolation, IPC 비용
Liedtke SOSP'93 핵심 수치	8-byte IPC 편도(one-way): Mach 115 µs vs L3 5.2 µs (i486-DX50, 22배) — 느린 건 Mach 구현이지 microkernel 원리가 아니다
XNU 가 hybrid 인 이유	Mach 기반 구조에 BSD 계층·IOKit 을 커널 주소공간 안에 co-locate — IPC 비용 회피. microkernel 구조 + monolithic 배치
loadable module 이 해결한 것 / 못 한 것	해결: 정적 단일 이미지 (런타임 링크로 확장). 미해결: isolation (같은 주소공간 ring 0 — module 버그 = 커널 사망)
scheduler / buddy / VFS / x86 entry / task_struct 위치	kernel/sched/ · mm/page_alloc.c · fs/ · arch/x86/entry/ · include/linux/sched.h
Kconfig vs Kbuild 역할	Kconfig = 무엇을 (옵션 정의 → .config). Kbuild = 어떻게 (obj-$(CONFIG_FOO) += foo.o 가 y/m/n 라우팅)
tristate y/m/n	y = built-in (이미지에 링크), m = loadable module (.ko), n = 제외. 부팅 필수 코드 (initramfs 없는 root fs 드라이버) 는 y 강제
vmlinux vs bzImage	vmlinux = 비압축 ELF (심볼, 디버깅용). bzImage = setup + self-extracting stub + 압축 커널 (부팅용). bz = big zImage (bzip2 아님)
module_init 의 이중 전개	built-in: __initcall(fn) → 부팅 중 do_initcalls() 호출. module: init_module alias → 로더가 do_one_initcall(mod->init). built-in 에서 module_exit 는 no-op
MODULE_STATE 전이	UNFORMED (할당) → COMING (심볼 해결 완료) → LIVE (init==0) / init<0 이면 GOING 으로 되감아 로드 실패
module 파라미터 파싱 시점	load_module() 의 parse_args() — init 실행 전. /sys/module/<name>/parameters/ 도 로드 시 생성
vermagic	.ko 에 박힌 빌드 대상 커널 버전+플래그 문자열. 로드 초기 검증에서 불일치 시 -ENOEXEC — 다른 커널용 .ko 거부 메커니즘
EXPORT_SYMBOL vs EXPORT_SYMBOL_GPL	후자는 GPL-compatible module 에만 보임. 집행: resolve_symbol() 이 proprietary taint module 에 gplok=false 로 검색
MODULE_LICENSE 누락 시	unspecified → GPL-incompatible 취급 → 'P' taint (module license taints kernel) + GPL-only 심볼 사용 불가
kernel taint 란	upstream 이 보증 못 하는 상태 기록 비트 (/proc/sys/kernel/tainted). out-of-tree module 은 항상 'O' (bit 12)
insmod vs modprobe	insmod = 파일 하나 그대로. modprobe = modules.dep 로 의존성 선로드 + 이름으로 탐색. 실무 표준 modprobe
커널 코드 4대 제약	no libc / 고정 16 KiB kernel stack / no FPU (kernel_fpu_begin 필요) / 자기 보호 없음 (버그 = oops/panic)
printk 콘솔 출력 조건	level 0(EMERG)~7(DEBUG). 메시지 레벨 < console_loglevel (/proc/sys/kernel/printk 첫 값) 이면 콘솔 출력. 링 버퍼는 dmesg
rest_init 의 생성 순서와 이유	kernel_init 먼저 (pid 1 확보) → kthreadd (pid 2). kernel_init 은 kthreadd_done completion 대기. 부팅 문맥은 PID 0 swapper (idle) 로 은퇴
init 시도 순서	initramfs /init → init= → /sbin/init → /etc/init → /bin/init → /bin/sh → 전부 실패 시 panic("No working init found."). 단 init= 명시값의 exec 실패는 즉시 panic("Requested init ... failed")
릴리스 모델	merge window 2주 → -rc 주단위 (rc6~9) → 릴리스 (주기 2~3개월). stable = 버그픽스 backport. LTS = 수년 유지 (6.12: EOL 2028-12)
goto error handling 관용구	자원 A→B→C 획득 실패 시 역순 해제를 label 사다리로 중앙화 (out_unlock: 등 서술적 이름). coding-style §7 이 공식 권장
```
