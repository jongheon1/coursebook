# Week 01 Lab — Module Lifecycle, /proc·/sys Tour, Source Navigation

세 부분으로 구성된다:

- **Part A (hello_param/)** — `module_param` 을 받는 kernel module 을 빌드·로드하고 `dmesg` 로 라이프사이클을 관찰한다.
- **Part B (kernel_tour/)** — 커널이 `/proc`, `/sys` 로 스스로에 대해 노출하는 정보를 도는 read-only 스크립트.
- **Part C (source_navigation.md)** — elixir/`git grep` 으로 커널 소스를 추적하는 가이드 문제.

> **검증 상태**: Part A 는 이 저장소를 만든 macOS 머신에서 **Docker(ubuntu:24.04) + `linux-headers-6.8.0-136-generic`(aarch64) 로 컴파일 검증 완료** — `hello_param.ko` 생성과 `modinfo` 출력(param 3종, license GPL)까지 확인했다. Part B 는 같은 컨테이너의 Linux 환경에서 실행 검증 완료. 단 **insmod/rmmod 실행 검증은 VM 셋업([Week 00](../../00-lab-setup/README.md)) 후에만 가능**하다 — 컨테이너는 호스트 커널을 공유하므로 모듈 로드는 컨테이너 안에서 하면 안 되고(호스트 커널에 로드된다), Lima VM 안에서 한다.

## Part A — `hello_param` module

### 빌드·로드 (Lima VM 안에서 — Week 00 셋업 완료 가정)

```bash
# guest 안: 호스트 경로는 read-only 이므로 writable 위치로 복사
cp -r <repo-root>/2026-2/system-programming/weeks/01-introduction-to-linux/lab/hello_param ~/w01-hello
cd ~/w01-hello
make                      # hello_param.ko 생성
modinfo hello_param.ko    # parm: whom / howmany / shout 확인

sudo insmod hello_param.ko
sudo dmesg | tail -5
sudo rmmod hello_param
sudo dmesg | tail -3
```

예상 `dmesg` (기본 파라미터):

```
hello_param: (1/1) hello, kernel world
hello_param: init ran in the context of "insmod" (pid 2xxx)
hello_param: goodbye kernel world (howmany is now 1), unloaded by "rmmod"
```

### 실험 시퀀스

**A-1. 파라미터 전달.** `sudo insmod hello_param.ko whom="Linus" howmany=3` → 인사 3줄. `charp`/`int`/`bool` 파싱은 커널의 `parse_args()` 가 로드 시점(`load_module()` 후반)에 수행한다.

**A-2. init 실패 = 로드 실패.** `sudo insmod hello_param.ko howmany=99` → `insmod: ERROR: could not insert module ...: Invalid parameters`. init 함수가 `-EINVAL` 을 반환하면 커널이 로드를 되감는다(`do_init_module()` 의 fail 경로) — 모듈은 목록에 남지 않는다. `lsmod | grep hello` 로 확인.

**A-3. printk 레벨 체감.** `sudo insmod hello_param.ko shout=1` → `pr_alert` 는 (콘솔 로그레벨보다 높은 우선순위이므로) VM 콘솔에 즉시 뜰 수 있다. `cat /proc/sys/kernel/printk` 의 첫 번째 숫자(console_loglevel)와 비교해볼 것. `pr_info` 레벨(6)은 기본 콘솔 레벨에서 콘솔에는 안 찍히고 링 버퍼(`dmesg`)에만 남는 경우가 일반적이다.

**A-4. /sys 로 노출된 파라미터.** 로드된 상태에서:

```bash
cat /sys/module/hello_param/parameters/howmany     # 0644 → 읽기 가능
echo 7 | sudo tee /sys/module/hello_param/parameters/howmany
sudo rmmod hello_param && sudo dmesg | tail -2     # "howmany is now 7"
cat /sys/module/hello_param/taint                  # 'OE' — out-of-tree + unsigned
```

`perm` 인자가 sysfs 노출을 결정한다: `0444` 읽기 전용, `0644` root 쓰기 가능, `0` 이면 아예 노출 안 됨.

**A-5. taint 관찰.** 로드 전후로 `cat /proc/sys/kernel/tainted` 비교. out-of-tree 모듈이므로 bit 12(값 4096, 'O')가 켜지고, 첫 로드 때 dmesg 에 `loading out-of-tree module taints kernel.` 이 찍힌다. 그리고 Ubuntu 커널은 `CONFIG_MODULE_SIG=y`(단 SIG_FORCE 아님)라 미서명 .ko 에 bit 13(값 8192, 'E')도 켜져 합계는 12288 이 되고, dmesg 에 `module verification failed: signature and/or required key missing - tainting kernel` 도 찍힌다. `MODULE_LICENSE("GPL")` 를 지우고 다시 빌드하면 bit 0('P', proprietary)도 추가되고 GPL-only 심볼을 못 쓰게 된다 — 시도해보고 원상복구할 것.

### 컨테이너에서 컴파일만 해보기 (macOS 에서 즉시 가능)

```bash
docker run --rm -v "$PWD/hello_param":/src:ro ubuntu:24.04 bash -c '
  apt-get update -qq && apt-get install -y -qq build-essential linux-headers-generic kmod
  KDIR=$(ls -d /usr/src/linux-headers-*-generic | head -1)
  cp -r /src /build && cd /build && make KDIR=$KDIR && modinfo hello_param.ko'
```

`uname -r` 이 컨테이너 밖 커널(linuxkit)을 가리키므로 `KDIR` 를 명시해야 한다. **컴파일 확인용일 뿐, 이 .ko 를 insmod 하지 말 것** — vermagic 이 실행 커널과 달라 거부되는 것이 정상이고, 그 거부가 바로 본문에서 말한 vermagic 검사다.

## Part B — kernel tour script

```bash
sh kernel_tour/tour.sh            # VM 안에서. 일부 항목은 sudo 시 더 보임
```

9개 스테이션: ① `/proc/version` ② `/proc/cmdline`(bootloader 가 넘긴 커맨드라인) ③ PID 1 정체 ④ `/proc/modules` ⑤ taint 비트 해독 ⑥ printk 로그레벨 4값 ⑦ `/sys/module/<name>/`(parameters/refcnt/taint) ⑧ `/boot/config-$(uname -r)`(빌드 시 `.config` 스냅샷) ⑨ `/proc/kallsyms` 에서 `start_kernel` 찾기.

읽는 법 메모:

- ④ `/proc/modules` 열: `name size refcount dependents state address`. `lsmod` 는 이 파일의 pretty-printer 일 뿐이다.
- ⑥ `/proc/sys/kernel/printk` 의 4값 = `console_loglevel default_message_loglevel minimum_console_loglevel default_console_loglevel`. 메시지 레벨 < console_loglevel 이면 콘솔로 나간다.
- ⑨ 주소가 전부 0 으로 보이면 정상 — `kptr_restrict` 때문이며 `sudo` 로 실행하면 실제 주소가 보인다.
- Docker 컨테이너에서 돌리면 ③ 이 systemd 가 아니라 컨테이너의 첫 프로세스로 나온다 — PID namespace 가 "PID 1" 의 의미를 바꾸기 때문 (W3 예고).

## Part C — source navigation

[source_navigation.md](source_navigation.md) 의 N1~N6. 브라우저만 있으면 macOS 에서도 바로 할 수 있다. N2·N6 은 로컬 트리가 필요하다:

```bash
git clone --depth 1 --branch v6.12 https://github.com/torvalds/linux ~/linux-v6.12
```
