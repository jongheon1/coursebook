# W1 Lab C — Kernel Source Navigation (elixir + git grep)

커널 코드를 "읽는 근육"을 만드는 연습이다. 필요한 것은 브라우저뿐이다: <https://elixir.bootlin.com/linux/v6.12/source>. 로컬에서 하고 싶으면 `git clone --depth 1 --branch v6.12 https://github.com/torvalds/linux` 후 `git grep` 을 쓴다 (전체 clone 은 수 GiB — `--depth 1` 권장).

elixir 사용법 요약:

- 상단 검색창은 **identifier 검색** — 함수/매크로/구조체 이름을 넣으면 "Defined in N files / Referenced in M files" 로 정의와 참조를 구분해 보여준다.
- 코드 화면에서 identifier 를 클릭해도 같은 결과.
- **문자열(로그 메시지) 검색은 identifier 검색으로 안 된다** — 그건 `git grep` 의 몫이다. 이 구분이 이 lab 의 핵심 스킬이다.

각 문제를 먼저 스스로 풀고 나서 접힌 답을 열 것.

---

**N1. `start_kernel` 을 찾아라.**
elixir 에서 `start_kernel` 을 identifier 검색하고: (a) 정의된 파일, (b) 함수에 붙은 attribute 들, (c) x86-64 에서 이 함수를 호출하는 코드(파일)를 찾아라.

<details><summary>답</summary>

- (a) `init/main.c` — 아키텍처 독립 초기화의 시작점.
- (b) `asmlinkage __visible __init __no_sanitize_address __noreturn __no_stack_protector` — `__init` 은 "부팅 후 버려지는 .init.text 섹션에 배치", `__noreturn` 은 "이 함수는 리턴하지 않는다" (마지막에 `rest_init()` → idle loop 로 사라진다).
- (c) references 목록에서 `arch/x86/kernel/head64.c` — `x86_64_start_reservations()` 가 마지막 줄에서 `start_kernel();` 을 호출한다. 즉 x86-64 부팅은 asm(head_64.S) → `x86_64_start_kernel()`(head64.c) → `x86_64_start_reservations()` → `start_kernel()` 순.
</details>

---

**N2. dmesg 의 문자열에서 코드로 역추적.**
어떤 머신의 부팅 로그에 `No working init found.` 가 찍히고 커널이 panic 했다. 이 메시지를 출력한 함수와, panic 직전까지 커널이 시도한 실행 파일 목록(순서대로)을 소스에서 찾아라. (힌트: elixir 는 문자열 검색이 약하다 — 로컬 트리에서 `git grep "No working init"` 또는 GitHub code search.)

<details><summary>답</summary>

`git grep -n "No working init"` → `init/main.c` 의 `kernel_init()`. panic 직전 시도 순서:

1. `ramdisk_execute_command` (initramfs 의 `/init`, `rdinit=` 로 변경 가능)
2. `execute_command` (커널 커맨드라인 `init=` 값)
3. `/sbin/init` → 4. `/etc/init` → 5. `/bin/init` → 6. `/bin/sh`

전부 실패하면 `panic("No working init found.  Try passing init= option to kernel. ...")`. (주의: 2 의 `init=` 값이 **지정돼 있는데 exec 이 실패**하면 3 이하로 넘어가지 않고 즉시 `panic("Requested init %s failed (error %d).")` — 위 fall-through 는 각 후보가 없거나 미지정일 때의 경로다. `CONFIG_DEFAULT_INIT` 이 설정된 커널은 2 와 3 사이에 그 값도 시도한다.) 교훈: **커널 로그 메시지는 소스로 들어가는 가장 좋은 입구다.** dmesg 한 줄 → `git grep` → 함수 → 콜체인.
</details>

---

**N3. `module_init` 의 이중생활.**
`include/linux/module.h` 에서 `module_init` 매크로의 **정의가 두 개** 있음을 확인하라. 어떤 조건으로 갈리고, 각각 무엇으로 전개되는가?

<details><summary>답</summary>

`#ifndef MODULE` (built-in 으로 컴파일될 때): `#define module_init(x) __initcall(x);` — init 함수 포인터를 initcall 섹션에 등록하고, 부팅 중 `do_initcalls()` 가 일괄 호출한다 (주석: "module_init() will either be called during do_initcalls() (if builtin) or at module insertion time (if a module)").

`#ifdef MODULE` (모듈로 컴파일될 때): `int init_module(void) __attribute__((alias(#initfn)));` — 내 init 함수를 `init_module` 이라는 표준 이름의 alias 로 만든다. `insmod` 로 로드되면 커널이 이 심볼을 `mod->init` 으로 잡아 `do_one_initcall(mod->init)` 로 호출한다 (`kernel/module/main.c` 의 `do_init_module()`).

같은 소스가 `=y` 로도 `=m` 으로도 빌드될 수 있는 것은 이 매크로가 두 세계를 흡수해주기 때문이다.
</details>

---

**N4. GPL-only 심볼은 어디서 거부되는가?**
`EXPORT_SYMBOL_GPL` 로 export 된 심볼을 proprietary 모듈이 쓰려 하면 로드가 실패한다. 이 판정이 실제로 일어나는 함수를 `kernel/module/main.c` 에서 찾아라. (힌트: 심볼을 찾아 연결하는 함수, 그리고 `gplok` 이라는 필드.)

<details><summary>답</summary>

`resolve_symbol()` (`kernel/module/main.c`). 심볼 검색 인자 구조체를 이렇게 채운다:

```c
struct find_symbol_arg fsa = {
    .name = name,
    .gplok = !(mod->taints & (1 << TAINT_PROPRIETARY_MODULE)),
    .warn = true,
};
```

즉 "이 모듈이 proprietary taint 를 가지면 gplok=false" 로 검색하고, `find_symbol()` 이 GPL-only 심볼을 gplok=false 요청에 대해 숨긴다. 같은 파일의 `inherit_taint()` 는 반대 방향 — proprietary 모듈이 export 한 심볼을 쓰는 모듈에 taint 를 전염시킨다.
</details>

---

**N5. `container_of` 맛보기 (W2 예고).**
`container_of` 를 identifier 검색해 정의 파일을 찾고, 매크로가 받는 세 인자와 "무엇을 돌려주는지"를 한 문장으로 요약하라. 그리고 references 수를 보고 이 매크로가 커널에서 얼마나 흔한지 체감하라.

<details><summary>답</summary>

정의는 `include/linux/container_of.h` (예전엔 `kernel.h` 에 있다가 분리됨). `container_of(ptr, type, member)` — "type 구조체 안에 member 로 박혀 있는 필드를 가리키는 포인터 ptr 에서, **그 필드를 품은 구조체 전체의 시작 주소를 역산**해 돌려준다". 구현 골자는 `(type *)((char *)ptr - offsetof(type, member))`. 참조가 수만 곳 — 커널의 embedded-struct 패턴(`list_head` 등, W2)의 기반이라서다.
</details>

---

**N6. `git grep` 전략 연습 (로컬 트리 필요).**
다음 각각을 찾는 한 줄 명령을 만들어라: (a) `getpid` syscall 의 구현 위치, (b) `TAINT_PROPRIETARY_MODULE` 이 세팅되는 모든 곳, (c) `Kconfig` 에서 `CONFIG_MODULES` 옵션이 정의된 파일.

<details><summary>답</summary>

```bash
# (a) syscall 구현은 sys_* 가 아니라 SYSCALL_DEFINE 매크로로 정의된다
git grep -n "SYSCALL_DEFINE0(getpid)"          # → kernel/sys.c

# (b) 상수 이름으로 grep — 정의(include/linux/panic.h)와 사용처가 나뉜다
git grep -n "TAINT_PROPRIETARY_MODULE" -- kernel/ include/

# (c) Kconfig 심볼은 CONFIG_ 접두사 없이 정의된다는 것이 함정
git grep -n "^config MODULES$" -- "*Kconfig*"   # → init/Kconfig
```

패턴 요약: **syscall 은 `SYSCALL_DEFINEn(name`, Kconfig 심볼은 `config NAME`(접두사 없음), 로그 문자열은 포맷 지정자(%d 등) 앞에서 끊어서** grep 한다.
</details>
