# Week 00 — Lab Environment Setup (macOS Apple Silicon + Lima)

이 과목의 모든 lab(kernel module 빌드, `clone(2)`/`/proc` 실험)은 **Linux kernel 6.x** 가 필요하다. macOS 에서는 커널 헤더도 `/proc` 도 없으므로, Apple Silicon Mac 에서는 [Lima](https://lima-vm.io/) 로 aarch64 Ubuntu VM 을 만들어 쓴다. 이 문서 하나로 "빈 Mac → hello world 모듈 insmod 성공" 까지 간다.

목표 확인 기준: 마지막 단계에서 `sudo dmesg` 에 `hello: Hello, kernel world!` 가 찍히면 셋업 완료다.

## 1. Lima 설치

```bash
brew install lima
limactl --version    # 1.x 면 OK
```

Lima 는 macOS Virtualization.framework(vz) 또는 QEMU 위에서 Linux VM 을 돌리는 경량 러너다. Apple Silicon 에서는 vz 가 기본이고, guest 는 호스트와 같은 aarch64 이므로 에뮬레이션 없이 빠르다.

## 2. Ubuntu VM 생성·기동

```bash
# Ubuntu LTS 템플릿으로 인스턴스 생성 + 기동 (수 분 소요: 이미지 다운로드)
limactl start template://ubuntu-lts --cpus 4 --memory 8 --disk 30 --tty=false

# 상태 확인
limactl list
```

- 인스턴스 이름은 `ubuntu-lts` 가 된다. 이후 명령은 `limactl shell ubuntu-lts <cmd>` 또는 셸 진입.
- Ubuntu LTS 템플릿은 kernel 6.x 계열이다 (24.04 = 6.8 기준; 그 이후 LTS 는 더 최신 6.x). 이 과목 기준(6.x API)에 부합한다.
- `--tty=false` 는 대화형 프롬프트 없이 기본값으로 진행하는 옵션.

VM 에 들어가기:

```bash
limactl shell ubuntu-lts        # guest 셸 진입
uname -sr                       # Linux 6.x-... 확인
```

**파일 공유 규칙 (중요)**: Lima 는 기본으로 **호스트 홈 디렉토리를 guest 안 같은 경로에 read-only 로** 마운트하고, `/tmp/lima` 만 양방향 쓰기 가능으로 마운트한다. 따라서:

- lab 소스를 guest 에서 **빌드하려면 writable 위치로 복사**해야 한다 (아래 예시처럼 guest 홈으로 `cp`).
- 결과물을 호스트로 가져올 일이 있으면 `/tmp/lima` 를 경유하거나 `limactl copy` 를 쓴다.

## 3. 빌드 도구 + 커널 헤더 설치 (guest 안에서)

```bash
sudo apt update
sudo apt install -y build-essential make linux-headers-$(uname -r)

# 확인: 이 디렉토리가 있어야 모듈 빌드 가능
ls /lib/modules/$(uname -r)/build
```

트러블슈팅:

- `linux-headers-$(uname -r)` 패키지를 못 찾으면: `sudo apt install -y linux-generic && sudo reboot` 로 커널과 헤더 버전을 맞춘 뒤 재시도 (`limactl shell ubuntu-lts` 로 재진입).
- `apt update` 가 느리면 그냥 기다린다. 미러 문제는 드물다.

## 4. Hello world module

작업 디렉토리를 만들고 (guest 홈은 쓰기 가능):

```bash
mkdir -p ~/hello && cd ~/hello
```

`hello.c`:

```c
// SPDX-License-Identifier: GPL-2.0
#include <linux/init.h>
#include <linux/kernel.h>
#include <linux/module.h>

static int __init hello_init(void)
{
	pr_info("hello: Hello, kernel world! (loaded by %s)\n", current->comm);
	return 0;
}

static void __exit hello_exit(void)
{
	pr_info("hello: Goodbye.\n");
}

module_init(hello_init);
module_exit(hello_exit);

MODULE_LICENSE("GPL");
MODULE_DESCRIPTION("W00 setup smoke test");
```

`Makefile` (탭 들여쓰기 주의 — make 는 스페이스를 거부한다):

```make
obj-m += hello.o

KDIR ?= /lib/modules/$(shell uname -r)/build

all:
	$(MAKE) -C $(KDIR) M=$(CURDIR) modules

clean:
	$(MAKE) -C $(KDIR) M=$(CURDIR) clean
```

빌드와 로드:

```bash
make                      # hello.ko 생성
modinfo hello.ko          # license/description 확인
sudo insmod hello.ko
sudo dmesg | tail -3      # "hello: Hello, kernel world!" 확인
sudo rmmod hello
sudo dmesg | tail -3      # "hello: Goodbye."
```

메모:

- Ubuntu 는 `kernel.dmesg_restrict=1` 이 기본이라 `dmesg` 에 `sudo` 가 필요하다. 매번 치기 싫으면 `sudo sysctl kernel.dmesg_restrict=0` (VM 안이니 부담 없음).
- `MODULE_LICENSE("GPL")` 이 없으면 커널이 taint 되고 GPL-only 심볼을 쓸 수 없다 (W1 참조).
- Lima VM 은 Secure Boot 가 없으므로 모듈 서명은 신경 쓰지 않아도 된다.

## 5. 주차별 lab 소스 가져와서 빌드하기

호스트 홈이 guest 에 read-only 로 보이므로, 예를 들어 Week 02 lab 은:

```bash
# guest 안에서 — 호스트 경로가 그대로 보인다 (read-only)
cp -r /Users/<호스트사용자명>/project/coursebook/2026-2/system-programming/weeks/02-linux-process-programming-1/lab ~/w02-lab
cd ~/w02-lab/module && make
cd ~/w02-lab/userspace && make
```

## 6. VM 수명 관리

```bash
limactl stop ubuntu-lts       # 정지 (상태 보존)
limactl start ubuntu-lts      # 재기동
limactl delete ubuntu-lts     # 완전 삭제 (디스크 반납)
```

kernel module 실습은 커널을 패닉시킬 수 있다 — 그래서 VM 에서 하는 것이다. 망가지면 `limactl delete` 후 이 문서를 처음부터 다시 실행하면 10분 안에 복구된다.

## 검증 상태

이 문서와 각 주차 lab 코드는 kernel 6.x API(v6.12 소스 확인) 기준으로 작성됐다. 단, **이 저장소를 만든 머신에는 VM 이 없어 위 절차의 실행 검증은 아직 수행되지 않았다.** 첫 셋업 때 어긋나는 부분(템플릿 이름, 패키지명 등)이 있으면 이 문서를 직접 갱신할 것.
