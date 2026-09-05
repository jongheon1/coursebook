# Week 01 강의 노트 — Introduction to Linux (오리엔테이션)

> 소스: 2026-09-02 강의 녹음 STT + 강의 슬라이드(`L00-courseIntroduction.pdf`, `_private/2026-2/system-programming/week-01/`). 담당교수: 박성훈(Seonghoon Park) — 이 학기 처음 부임해 진행하는 **본인의 첫 강의**라고 직접 언급.

## 1. 운영 정보

- **담당교수**: 박성훈(Seonghoon Park). 이 학기 연세대에 새로 부임, 이번이 교수로서의 첫 강의라고 밝힘(긴장되지만 기대된다고 언급).
- **TA**: 김건중(Gunjoong Kim) — 박사과정생. 과제·출석 등 문의는 TA 이메일로.
- **출석**: Y-Attend 앱으로 전자 출석. 오늘은 테스트 삼아 진행. 배점표상 10%지만 한두 번 결석은 크게 감점하지 않겠다고 함(연고전 등으로 빠져도 괜찮다는 뉘앙스) — 다만 **3분의 2 출석은 본인 방침이 아니라 학교 규정**이라 반드시 지켜야 한다고 강조.
- **평가**: 중간고사 + 기말고사, 프로그래밍 과제 2개(어쩌면 3개, "아마 2개"). (배점 구체 수치는 이번 오리엔테이션 강의에서 언급 안 됨 — syllabus.md의 기존 수치와 대조 필요.)
- **AI 정책**: 사용을 막을 수는 없지만, 과제는 먼저 스스로 풀어보고 막힐 때만 AI와 상의할 것을 강력 권장. "시행착오 자체가 커널 내부 원리를 이해하게 만드는 과정"이라고 설명.
- **교재**: 정식 교재(Bovet & Cesati, *Understanding the Linux Kernel*)는 출간된 지 10년이 넘어 오래된 리눅스 버전을 다룬다며 구매를 권하지 않음. 대신 최신 슬라이드 + 실제 최신 커널 소스(웹사이트)를 보라고 권장. 슬라이드 이해에 AI를 활용해도 좋다고 언급.

## 2. 과목 성격 — "시스템 프로그래밍"이지만 실체는 리눅스 커널 프로그래밍

- 이 과목의 목표는 OS 커널 프로그래밍의 실전적 측면, 특히 **리눅스 커널**을 배우는 것. 운영체제(OS) 수업을 아직 안 들었다면 먼저 듣고 오길 권장 — OS 수업은 이론 위주로 실제 리눅스 코드를 거의 안 다루는 반면, 이 과목은 **실제 코드**를 다룬다는 게 핵심 차이.
- 배우는 내용: 커널 내부 동작 원리, 커널 커스터마이징 방법. 과제는 커널 수정 또는 커널 모듈 작성 형태.
- 강조점: 리눅스 이해는 커널/시스템 프로그래밍에 국한되지 않고, 상위 레벨 애플리케이션·AI 개발에도 밑바탕이 된다 — "OS가 어떻게 동작하는지 알아야 그 위의 것들을 제대로 만들 수 있다."
- 왜 리눅스인가: 무료·개방(비용 없음), 약 30년간 개발되어 온 성숙한 OS. 스마트폰·워치·가전 등 모든 곳에 있다는 점을 강조("Linux is everywhere").

## 3. 이번 학기 개요 (구두로 설명된 커리큘럼)

기존 OS 수업 개요와 유사하지만, 이론이 아니라 **실제 리눅스 코드** 기준이라는 게 차이. 다룰 주제: 리눅스 프로세스, 스케줄링, 시스템 콜, (커널) 동기화, 메모리 관리, 파일 시스템 등.

## 4. 스마트폰 OS 생태계 맥락 (도입 동기 부여용)

- 스마트폰 OS: 안드로이드, 아이폰, (과거) 심비안, 윈도우 10 모바일, webOS, 블랙베리, 타이젠 등 — 대부분 **리눅스 기반**(무료 + 잘 관리됨). webOS(LG)·타이젠(삼성)은 스마트폰에서는 밀려났지만 지금은 TV·냉장고 등 가전제품에서 쓰인다.
- 안드로이드/타이젠 스택: 커널(하위, CPU 스케줄링·메모리 관리·파일시스템)과 프레임워크(상위, 애플리케이션 레벨)를 구분. 두 스택 모두 최하단은 리눅스 커널. LG·삼성·구글 같은 기업에서 이 레이어를 다루게 될 수 있다는 커리어 연결 언급.

## 5. 교수 본인 연구 소개 (Mobile AI and Systems Lab)

- 연구실명: **Mobile AI and Systems Lab**. 비전: 증강현실용 실시간 주변 상황 이해, 몰입형 인터랙티브 3D 콘텐츠(Meta Quest 등 XR 기기) 같은 고급 모바일 경험을 사용자에게 제공하는 것.
- 기술적 난제: vision foundation model, vision-language model, LLM, NeRF(Neural Radiance Field), 3D Gaussian Splatting 등은 연산량이 매우 크다. 목표는 이런 무거운 작업을 **자원이 제한된 모바일 기기에서 실시간으로** 돌리는 것 — 서버급 GPU 대비 훨씬 느리고, 배터리·발열 제약까지 있다.
- 최적화 전략: 스마트폰 AP의 NPU/CPU/GPU 간 작업 분배, 동작 주파수(DVFS) 제어, GPU-NPU 세밀 스케줄링. 여기에 AI 쪽 기법(static model configuration, multi-exit/stitchable network 같은 dynamic neural architecture, scalable scene representation)을 결합. **이 모든 최적화가 결국 OS/안드로이드 내부 동작에 대한 깊은 이해를 전제**로 한다는 게 이 소개의 핵심 메시지 — 왜 우리가 커널을 배워야 하는지에 대한 교수 본인의 답.
- 스케줄링·메모리 관리의 세부 내용은 "학부보다는 대학원/박사 수준"이라며 이번 강의에서는 다루지 않는다고 명시. 관심 있는 학생은 인턴/박사과정 지원 문의 환영이라고 언급(연구실 홍보).

## 6. 마무리

과목 개요 소개를 마치며 질문 받음. 1주차는 자유롭게 수강철회 가능하며, 첫 주는 전원 출석으로 처리하겠다고 안내.

---

# Day 2 (2026-09-05) — 리눅스 커널 버전 체계 & 프로세스 개념 입문

> 소스: 2026-09-05 강의 녹음 STT(whisper-1) + 강의 슬라이드 `L01-linuxprocesses.pdf`(`_private/2026-2/system-programming/week-01/`). 이 강의의 도입부(§7)는 슬라이드 없이 음성으로만 진행됐다 — 대응하는 슬라이드 파일을 받지 못해 전사본만을 근거로 정리했다. §8부터는 `L01-linuxprocesses.pdf`와 대응된다. **이 강의는 슬라이드 87장 중 약 앞쪽 40여 장(리눅스 프로세스 리스트 도입부까지)만 다뤘다 — pidhash 테이블 세부, Task Lists Big Picture, Wait Queues, Process Usage Limits, Process Switching 내부 동작(switch_to 어셈블리), Kernel Threads, Process 0/1, Destroying Processes 등 뒷부분 슬라이드는 이번 강의에서 다루지 않았으며 다음 수요일로 예고됐다. 이 노트는 그 뒷부분을 추측해서 채우지 않는다.**

## 7. 리눅스 커널 버전 체계 (도입부, 슬라이드 미제공)

- **역사·사용 현황**: 리눅스는 1995년경 출시(교수 발언 그대로 — "내가 1994년생이라 리눅스는 내 친구 같은 존재"). 개인 데스크톱/노트북 점유율은 약 2%에 불과하지만, 서버·스마트폰·엣지 디바이스·가전제품에서는 압도적으로 많이 쓰인다. 전체 컴퓨팅 기기 중 스마트폰 비중이 현재 약 70%.
- **오픈소스 프로젝트로서의 특징**: 라이선스 제약이 거의 없어 누구나 코드를 읽고 커널을 쓰고 심지어 직접 OS를 만들어볼 수도 있음. 약 33년 된 소프트웨어로 매우 성숙·잘 관리됨. 인텔·삼성·구글 등 대기업 포함 다수 개발자가 기여.
- **C 언어로 작성됨**: 대부분 C 프로그래밍을 어려워하지만, 리눅스는 C를 배우는 최고의 예제라는 게 이 과목이 존재하는 이유 중 하나.
- **라이선스**: GPLv2 — 자유롭게 수정·배포 가능, 상업적 사용도 가능하나 소스 공개·저작권 표시 조건이 있음("근데 큰 문제는 아니라고 생각한다").
- **성장 규모**: 약 4천만 줄까지 성장, 두 달마다 약 40만 줄씩 계속 증가, 릴리스당 약 2,000명 개발자 기여.
- **릴리스 버전 체계**: RC(release candidate, 실험적) → mainline(2~3개월마다, 리누스 토르발스가 결정) → stable(mainline 위에 버그 수정, major.minor.stable 형식) → **LTS**(long-term support, 가장 안정적, Chrome OS·안드로이드·윈도우·아마존 리눅스 등 실제 제품이 사용. 약 1~2년마다 릴리스, 유지보수 기간이 길게 연장됨 — 일부는 최대 6년까지). LTS가 중요한 이유: 제품 입장에서는 새 기능보다 검증된 커널이 훨씬 중요하기 때문.
- **kernel.org**: 최신 mainline/stable/RC 버전을 항상 확인 가능한 사이트. 강의 시점(2026-09) 기준 mainline 7.2, stable 7.2.2, RC 7.3-RC1(슬라이드 날짜가 안 맞아 교수가 직접 정정). LTS는 6.18이 최신(작년 11월 릴리스), LTS는 대략 매년 10~12월경 릴리스.
- **실제 제품 사례**: 안드로이드가 가장 널리 쓰이는 LTS 기반 제품, 그 외 우분투·Chrome OS·WSL·라즈베리파이·아마존 리눅스도 LTS 기반. 스마트폰은 커널 교체 불가하지만 아마존 리눅스/우분투는 더 최신 커널로 교체 가능.
- **안드로이드 공용 커널**: 안드로이드도 자체 커널이 있지만 LTS 리눅스 커널 기반. LTS → 안드로이드 메인라인 커널로 지속적인 머지가 이뤄지고, 그 메인라인 위에서 버전별 안드로이드 커널·OS가 개발되는 브랜칭 모델.
- 이 도입부 내용은 시험(중간/기말) 대상이 아니라고 명시. "지금부터가 진짜 강의이고 시험 범위"라며 Linux Processes로 전환.

## 8. Kernel Outlook (커널 레벨 구성요소)

- User Level(사용자 프로그램: 브라우저·셸·터미널 등) → System Call Interface → Kernel Level의 각 매니저:
  - **Filesystem Manager**(Ext2fs, proc, nfs) — 스토리지의 파일을 읽고 쓰는 것
  - **Process Manager**(Task Management, Scheduler, Signaling) — 교수는 이걸 memory manager와 함께 가장 중요한 컴포넌트로 꼽음
  - **Memory Manager** — 가상 메모리를 물리 메모리로 매핑
  - **Network Manager**(IPv6, ethernet), **Device Manager**(block, character) — Buffer cache를 매개로 서로 연결
- 최하단 HW Level(CPU, GPU, 메모리, 스토리지, 키보드·마우스 등)까지 커버하는 게 이 학기 전체의 목표.

## 9. Linux Cross Reference (LXR) — elixir.bootlin.com

- 리눅스 커널의 최초 버전부터 최신 버전까지 코드를 검색·열람 가능한 웹 사이트. 변수·매크로·함수를 검색하면 정의 위치와 참조·사용 위치를 바로 보여줌.
- 세부사항은 바뀌어도 핵심 개념은 그대로라서 교재 구매를 권하지 않음(그래도 읽어볼 가치는 있다고 언급). 과제 진행 시 이 사이트를 매우 자주 쓰게 될 거라고 예고(과제 세부는 아직 미확정).

## 10. 도입 질문 — 커널 코드도 프로세스인가?

- "커널 코드는 프로세서가 실행한다는 점에서 일반 프로그램과 똑같이 동작하고, 자주 제어권을 넘겼다가 프로세서로부터 다시 돌려받는다." 그렇다면 커널 코드 자체가 process인가? 그렇다면 어떻게 제어되는가?
- 답("process는 실행 중인 프로그램의 인스턴스")은 지금은 헷갈릴 수 있다며 뒤에서(§13) 다시 설명하겠다고 예고.

## 11. OS 실행 모델 두 가지 — Process-based OS vs Execution within User Process

- **Process-based OS**: OS 기능도 사용자 프로세스들과 나란히 별도 프로세스로 돎. 프로세스 간 전환(풀 프로세스 스위치)은 한 건물에서 나가 다른 건물로 걸어 들어가는 것과 같아 오버헤드가 큼(교수의 건물/아파트 비유).
- **Execution within User Process**(리눅스가 택한 모델): OS 기능이 사용자 프로세스 자신의 컨텍스트 안에서 실행 — 같은 건물 안에서 위/아래층을 오가는 것에 가까워 더 효율적.
- **대가**: 사용자 입장에서 주소 공간 일부를 커널에 내줘야 함. 32비트 시스템 기준 가상 주소 공간 4GB 중, process-based OS라면 사용자가 4GB를 다 쓸 수 있지만 execution-within-user-process에서는 3GB(사용자) / 1GB(커널)로 나뉨 — 모든 프로세스가 주소 공간의 25%를 내주는 셈. 교수의 비유: 커널/OS = 건물주(land lord), 사용자 프로그램 = 세입자(tenant), 세입자는 건물주 규칙을 따라야 함.
- **얻는 이득**: 이 방식은 커널 관련 작업만 할 때 비용이 큰 풀 컨텍스트 스위치를 피하고, 대신 같은 프로세스 안에서 훨씬 저렴한 **mode switch**만 하면 됨 — 이게 이 모델의 핵심 장점("virtually all OS code gets executed within the context of a user process").
- 휴식 후 다시 강조한 정리: 장점 = mode switch 오버헤드가 낮음 / 단점 = 사용자 입장에서 주소 공간 일부(1GB)를 아예 못 씀 — "중요한 내용이라 다시 짚고 싶었다"고 직접 언급.

## 12. Dual-Mode Operation — User Mode / Kernel Mode

- 최신 CPU는 최소 두 가지 모드(user/kernel)를 구분하는 하드웨어 지원 제공. (세부적으로 더 많은 레벨을 지원하는 아키텍처도 있지만 이는 매우 architecture-specific이라 이 과목에서는 이 두 모드만 다룸.)
- **User mode**: 사용자를 대신해 실행, 물리 메모리·파일 등 커널 요소에 직접 접근할 권한 없음.
- **Kernel mode**: OS를 대신해 실행, 프로세서·명령어·레지스터·메모리에 대한 완전한 제어권. 사용자 프로그램이 CPU를 직접 제어하게 두면 매우 위험하기 때문에 이렇게 분리됨.
- 구체적 예시(파워포인트): 그냥 켜져서 돌아가는 동안은 user mode. 클릭/타이핑하거나 런타임 에러가 나면 유저 프로그램이 스스로 처리 못 하는 일이라 이때 mode switch가 일어남. 풀 프로세스 전환(스케줄러가 완전히 다른 프로세스를 고르는 것)은 정말 필요할 때만 발생 — 이게 이 설계의 큰 장점.

## 13. Mode Switch를 유발하는 3대 이벤트

1. **Hardware Interrupt**: 키보드 입력, 네트워크 패킷 도착 등 — 유저 프로그램이 스스로 처리 불가.
2. **Software Interrupt (exception)**: divide-by-zero(매우 심각), page fault(물리 메모리에 매핑 안 된 영역 접근 시도) 등 런타임 에러 — 유저 프로그램이 보고 싶어 하는 상황도 아니고 스스로 처리도 불가.
3. **System Call**: 유저 프로그램이 능동적으로 원하는 작업 — 파일 읽기(예: 파워포인트가 .ppt 파일을 열 때), 프로세스 생성(fork — 요즘 프로그램 대부분이 멀티프로세스), 네트워크 통신(소켓/TCP-IP, 네트워크 매니저가 처리).
- **워크드 예제 — printf → write 시스템 콜**: user mode의 프로그램이 C 라이브러리의 `printf()`를 호출 → 내부적으로 `write()` 시스템 콜 인터페이스 호출 → 이 시점에 mode가 커널로 전환됨 → 커널 코드가 시작되고 실제 하드웨어(모니터 등)와 통신 → 화면에 출력이 나타남.
- (여기서 3시 15분경 짧은 휴식.)

## 14. 프로세스의 정의

- 교과서 정의: "process는 실행 중인 프로그램의 인스턴스(an instance of a running program)." 교수는 이 정의가 요즘은(멀티프로세스/멀티스레드 프로그램이 흔해서) 헷갈릴 수 있다고 지적.
- 교수가 실제로 ChatGPT에게 재정의를 요청해서 얻은 표현: **"process는 자기만의 virtual address space와 자원(resources)을 가진 실행 중인 인스턴스."** 프로세스가 자기만의 가상 주소와 자기만의 자원을 갖는다는 점을 잘 짚어줘서 이 표현이 마음에 든다고 언급.
- 프로세스가 포함하는 것: **images**(code, data, stack, heap — 가상 메모리에 저장) + **process context**:
  - **Program context**: data registers, program counter(PC), stack pointer(SP)
  - **Kernel context**: PID, GID, SID, VM 구조체, 열린 파일, 시그널 관련 정보

## 15. 프로세스 이미지 레이아웃 — code/data/stack/heap

- 코드 영역과 데이터 영역: 데이터는 소스 코드 작성 방식에 따라 **initialized**/**uninitialized**로 나뉨 — 예: `int i;`(대입 없음, uninitialized) vs `int i = 1;`(initialized).
- **Heap**: 동적 메모리 할당(malloc류)용, 아래에서 위로 자람. **Stack**: 자동/임시 변수·리턴 주소·호출 환경(C 코드의 일반적인 변수들), 위에서 아래로 자람.
- **워크드 예제(실제 C 코드)**: 전역 배열(크기 100 고정이라 uninitialized data 영역에 들어감, 동적 할당은 아님), 전역 변수 `bufsize`(initialized data 영역), `main()`/`f1()` 함수 코드(text 영역, OS가 한 줄씩 읽으며 실행), `f1()` 안의 `malloc(bufsize)` 호출(heap에 할당), `main()`의 지역 변수 `i`/`buf`(stack에 저장). 정리: 전역 변수 → data 영역, 지역 변수 → stack, 코드 → code 영역, malloc류 결과물 → heap.
- **init 프로세스(process 1) 예시**: 리눅스 부팅 시 최초로 시작되는 프로세스. 자기만의 user stack, 데이터 구조, heap, code를 가지며, 커널 주소 공간에는 이 프로세스의 커널 쪽 데이터 구조 일부가 저장됨.

## 16. 프로세스 모델의 한계 → 스레드가 필요한 이유

1. **Cooperating processes 문제**: 스레드 개념이 아예 없다고 가정(초기에는 실제로 그랬음) — 많은 애플리케이션이 여러 작업을 동시에 처리해야 하는데, 순수 프로세스들은 주소 공간·자원을 공유하지 않아 매우 비효율적.
2. **Multiprocessing 문제**: 전통적인 프로세스는 한 번에 CPU 코어 하나에서만 돎 — 기기에 멀티코어가 있어도 순수 멀티프로세스 모델만으로는 이를 활용할 수 없음.

## 17. Process vs Thread — 무엇을 공유하는가

- 전통적 관점: **process = process context + (code, data, stack)**. 스레드가 등장하면: 각 스레드는 자기만의 논리적 실행 흐름을 갖지만(당연히), **code·data·kernel context는 공유**하고 **state(구체적으로 stack)만 스레드별로 다름**. 즉 process와 thread의 차이는 결국 "무엇을 공유하느냐"로 귀결됨.
- 구체적으로: 프로세스는 자기만의 virtual memory와 자원(stack/heap/data/code/kernel context)을 가짐. 한 프로세스가 여러 스레드를 가지면 그 스레드들은 heap·data·code를 공유하고, 각자 온전히 갖는 건 stack뿐. 스레드가 없는 순수 프로세스들은 parent-child-sibling 계층은 갖지만 아무것도 공유하지 않음(각자 완전히 별도의 code/data/context/stack).
- **생성 방식**: process는 `fork()` 같은 시스템 콜로, thread는 표준 API인 **pthread**로 생성. pthread는 인터페이스/API일 뿐이고 실제 구현은 라이브러리 개발자 몫(입출력 규격만 정의) — 오늘날 대부분의 멀티스레드 애플리케이션이 pthread 라이브러리로 작성됨(예: `pthread_create()`).
- **통신 비용**: 별도 프로세스끼리 통신하려면 **IPC**(inter-process communication)가 필요해 오버헤드가 있지만, 스레드는 code/data를 공유하므로 IPC가 필요 없음 — 이게 리눅스가 스레드 개념을 도입한 이유 중 하나.
- **동기화**: 멀티프로세스는 각자 완전히 분리된 주소 공간이라 더 안전하지만, 스레드는 메모리·데이터 구조를 공유해서 한 스레드가 공유 자원에 다른 스레드가 원치 않는 작업을 할 수 있는 문제가 생김 — 그래서 pthread API가 **mutex**, **condition variable** 같은 동기화 메커니즘을 정의.

## 18. Process States

- **일반(교과서) 모델**: **new**(생성 중, 일시적 1회성) → **ready**(스케줄될 준비는 됐지만 아직 기회를 못 받음) → **running**(스케줄러가 골라서 실제 CPU에서 실행 중 — 최신 CPU 스케줄러는 공정한 시간 분배를 위해 짧은 시간 후 다시 ready로 되돌림) → **exit**(종료). 추가로 **blocked**: 특정 이벤트(네트워크·키보드·시간 경과 등)를 기다리는 동안 CPU에서 돌지도, ready 상태도 아닌 상태(예: 프로그램이 10초를 기다리는 경우).
- **리눅스 구현**(최근 커널에서 갱신됨, 교수의 간략한 프레이밍): `TASK_RUNNING`이 ready와 running을 모두 포괄. blocked 프로세스는 `TASK_INTERRUPTIBLE` 또는 `TASK_UNINTERRUPTIBLE`(둘 다 특정 이벤트를 기다리며, 이벤트 발생 시 다시 스케줄 가능해짐). `TASK_STOPPED`은 이 자리에서 exit에 가까운 상태로 간단히 언급됨(자세한 exit_state 세분화는 다루지 않음).

## 19. task_struct / thread_info — Process Control Block(PCB)

- `sched.h`가 프로세스·CPU 스케줄러 관련 데이터 구조를 정의하는 핵심 파일. **task_struct** = 리눅스 프로세스를 나타내는 데이터 구조, 즉 **PCB(process control block)** — task information, task image(code/data/stack/heap), program context를 담음.
- 리눅스에서는 process를 **task**라고 부르며, thread도 task다 — task가 CPU 스케줄러가 다루는 단위. (교과서 관점 "process" vs 리눅스 관점 "task"라는 용어 혼용에 유의하라고 언급.)
- 버전 비교: Linux 2.6.11 시절 task_struct는 짧았지만, 계속 필드가 추가되면서 최신 버전은 거의 1,000줄에 달함(기본 개념은 유사). **task_struct는 architecture-independent**, 반면 **thread_info는 architecture-dependent**(Intel·ARM 등이 각자 설계) — 실제 CPU와 밀접하게 연관되기 때문. 최신 LTS 기준으로도 ARM/x86 thread_info를 각각 비교해서 보여줌.
- 모든 프로세스가 자기만의 process descriptor를 가져야 하는 이유: 커널이 모든 process/task를 식별·관리해야 하고, 각 task/context가 자기 정보(process context, code, data 등)를 저장할 자기만의 디스크립터가 필요하기 때문.

## 20. User Stack / Kernel Stack

- Dual-mode 동작은 커널도 자기만의 스택이 필요하다는 뜻 — 커널 코드 실행 중 지역 변수를 저장할 곳이 **kernel stack**.
- 커널 모드 진입 시(mode switch 발생 시) task의 레지스터(스택 포인터, 인스트럭션 포인터 등)가 kernel stack에 저장됨 — 나중에 다시 user mode로 돌아갈 때 프로그램이 정확히 어디까지 진행됐는지 알기 위함. 커널 함수 실행 중의 지역 변수도 kernel stack에 저장됨.
- 프로세스당 할당된 작은 커널 메모리 영역(예전엔 thread_info + kernel stack 두 가지를 담았으나, **요즘은 thread_info가 여기 저장되지 않아 kernel stack만 남음**, 8KB 영역). 모든 사용자 프로세스는 스택 2개(user, kernel)가 필요하며, 커널 스택은 커널 데이터 세그먼트에 위치하고 스택 전환은 mode switch 시점에 일어남.

## 21. "current" 프로세스 식별 — 옛날 방식 vs 현대 방식

- 커널이 "지금 실행 중인 프로세스가 뭔지" 알아야 하는 이유: 커널 모드가 끝나면 다시 user mode로 돌아가야 하는데, 그게 정확히 어느 프로세스였는지 알아야 하기 때문.
- **Linux 2.6.11**: 복잡한 방식 — 어셈블리 레벨의 스택 포인터 마스킹으로 커널 스택 하단의 정보에서 현재 프로세스를 알아냄.
- **현대 방식**: 각 CPU/코어가 현재 실행 중인 task를 가리키는 포인터를 담은 자기만의 데이터 구조를 유지 — CPU가 current task를 바로 알 수 있음(Linux 6.18.48의 architecture-dependent 코드로 예시 제시).

## 22. Process List

- 리눅스 커널은 한 번에 많은(교수 추정 "천 개 정도?") 프로세스를 돌리므로 이를 효율적으로 관리할 방법이 필요.
- **이중 연결 리스트(doubly linked list)**: 각 task_struct가 prev/next 포인터를 가지며 `init_task`에서 시작해 다른 프로세스들이 연결됨. 커널이 삽입·삭제·스캔용 매크로 제공 — 예: `for_each_task`(다음 태스크 포인터를 계속 따라가며 전체 순회).
- **한계와 pidhash 도입 동기(미완)**: 연결 리스트 순회만으로 특정 PID(예: PID 1000)를 직접 찾으려면 첫 태스크부터 순차적으로 최대 1,000번 스캔해야 해서 매우 비효율적 — "그래서 리눅스 커널은 해시 테이블(pidhash)도 함께 유지한다"고 언급한 직후, 시간 관계상(4:46) 강의를 마무리. **pidhash의 실제 구조·조회 방식 등 세부 내용은 이번 강의에서 다루지 않았고, 다음 수요일 강의("process list and related things")에서 이어가겠다고 예고했다 — 이 노트는 그 내용을 추측해서 채우지 않는다.**
