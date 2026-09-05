# Week 01 Delta — 실제 강의 vs 예습 챕터(`weeks/01-introduction-to-linux/README.md`)

> 예습 챕터는 kernel/user space 경계, mode switch vs context switch, monolithic vs microkernel 논쟁(Liedtke IPC 벤치마크, Tanenbaum–Torvalds 논쟁, macOS/XNU 사례), loadable module 메커니즘, Kconfig/Kbuild, 부팅 흐름까지 다루는 상당히 기술적인 챕터다. 실제 Week 1 강의는 **신임 교수의 오리엔테이션 강의**였고, 예습 챕터의 기술적 내용은 전혀 다루지 않았다 — 자기소개, 과목 성격 설명, 로지스틱스, 그리고 본인 연구 소개가 전부였다. 그래서 이번 delta도 "정정"보다는 "예습 챕터에 없는 맥락/운영 정보"와 "프레이밍 참고사항" 위주다.

## Emphasized (교수가 강조했는데 예습 챕터에서 비중이 작았던 것)

- **"이 과목은 리눅스 코드를 실제로 다룬다"는 차별점을 여러 번 강조** — OS 수업은 이론 위주이고 실제 코드를 거의 안 본다는 대비를 통해서다. 예습 챕터도 실제 v6.12 소스를 인용하는 방식으로 이미 이 방향이지만, "OS 수업을 먼저 듣고 오라"는 선수과목 권고는 새로운 정보(§2 참고, syllabus.md의 "선수 추천"과 일치하는 방향이라 정정은 아님).
- **커널 이해가 상위 레벨(AI 등) 개발에도 중요하다**는 프레이밍 — 교수 본인 연구(모바일 AI 최적화가 결국 OS 내부 이해를 필요로 함)로 구체화됨. 예습 챕터의 "Why this matters"가 시스템적 관점을 이미 취하고 있어 방향은 일치.

## New (교재에 없던 내용 — 교수 자체 맥락·운영 정보)

1. **교수 본인이 이 학기 신규 부임, 이번이 교수로서 첫 강의**라는 사실. 정서적 맥락(긴장되지만 기대된다는 언급)일 뿐 시험 신호는 아니지만, 왜 오리엔테이션이 이례적으로 개인적인 톤인지 설명해준다.
2. **연구실 정보**: "Mobile AI and Systems Lab", 비전(AR 실시간 장면 이해, XR 몰입형 콘텐츠), 기술 스택(NPU/CPU/GPU 이종 스케줄링, DVFS, static/dynamic model 최적화). 이 연구 맥락이 W11-13(메모리 관리)이나 향후 "왜 이 주제가 중요한가" 서술에 참고할 수 있는 real-world motivation이 될 수 있음.
3. **AI 사용 정책 구체화**: 막지는 않지만 먼저 스스로 풀고 막힐 때만 AI와 상의하라는 권고, 이유는 "시행착오 과정 자체가 내부 원리 이해를 만든다"는 것. syllabus.md에 이미 "과제에 생성형 AI 부분 허용 명시"라고 요약돼 있어 방향은 일치하지만 구체적 근거·표현은 새로움.
4. **교재 비권장 사유**: Bovet & Cesati 교재가 10년 이상 오래돼 최신 커널과 괴리가 크다며 구매를 권하지 않고, 대신 강의 슬라이드 + 실제 최신 소스(웹사이트) 참조를 권장. 이는 예습 챕터가 이미 "교재는 2.6.34 기준, 최신 부분은 Modern kernel note로 표시"라고 밝힌 것과 **정확히 같은 문제의식**이라 오히려 예습 챕터의 접근을 뒷받침하는 근거로 인용 가능.
5. **출석 완화 발언**: 배점표상 출석 10%지만 한두 번 결석에 크게 감점하지 않겠다는 개인 재량, 단 "3분의 2 출석은 학교 규정이라 반드시 지켜야 한다"는 구분을 명확히 함. 구체적인 결석 허용 횟수나 감점 규정 수치는 이번 강의에서 언급되지 않음 — syllabus.md 갱신은 이번 라운드에서 보류(요청 범위상 원본 소스 정리까지만 진행).

## Corrected (교재 서술과 다르거나 더 정확한 서술)

- 없음. 오리엔테이션 강의가 예습 챕터의 기술적 내용(경계·mode switch·module 로드 절차·Kconfig 등)을 전혀 다루지 않아 직접 충돌하는 지점이 없었다.

---

# Day 2 Delta (2026-09-05) — 실제 강의 vs 예습 챕터(`weeks/02-linux-process-programming-1/README.md`)

> 비교 대상은 `weeks/02-linux-process-programming-1/README.md`("Linux Process Programming (1)") — task_struct/copy_process/COW를 v6.12 소스 레벨로 깊게 다루는 챕터다. 실제 Day 2 강의는 그보다 훨씬 **기초적인 OS 개론 수준**(dual mode, process 정의, process image layout, process vs thread, process states, task_struct를 PCB 개념으로만 소개, pidhash 도입부에서 시간 종료)이었다. 그래서 이번 delta는 "정정"보다 "예습 챕터가 전제하고 건너뛴 기초를 실제 강의가 어떻게 채우는지"와, 실제로 확인된 **수치 불일치 1건**이 핵심이다.

## Emphasized (교수가 강조했는데 예습 챕터에서 비중이 작았던 것)

- **"Linux에는 thread라는 별도 개체가 없다 — process와 thread의 차이는 오직 무엇을 공유하느냐(code/data/kernel context)뿐"** (notes.md §17) — 이건 예습 챕터의 결론 문장("모든 실행 단위는 task_struct 하나이고, 차이는 CLONE_* flags로 어떤 자원을 공유했는가뿐")과 **정확히 같은 결론**이다. 다만 실제 강의는 이걸 소스 레벨(`copy_process`, CLONE flags)이 아니라 개념 레벨(사용자 관점에서 "무엇을 share하는가")로 먼저 도입했다 — 다음 주 강의가 이걸 소스 레벨로 얼마나 빨리 좁혀 가는지 확인할 가치가 있음.
- **Execution-within-user-process 모델과 3GB/1GB 주소공간 분할의 "왜"** (notes.md §11) — 예습 챕터는 kernel/user space 경계를 이미 아는 것으로 전제하고 바로 task_struct로 들어가는데, 실제 강의는 "왜 사용자가 주소 공간의 25%를 커널에 내줘야 하는가"를 process-based OS와의 비교(건물 비유)로 상당히 공들여 설명했다. 이 프레이밍은 W1(`weeks/01-introduction-to-linux/`)의 mode switch vs context switch 논의와도 연결되므로, 향후 W1 챕터 개정 시 이 "왜 1GB를 내주는가" 비용 프레임을 인용할 만하다.

## New (예습 챕터에 아예 없던 내용 — 더 기초적인 온보딩 또는 강의 진행 맥락)

1. **리눅스 커널 버전 체계 전체** (notes.md §7) — RC/mainline/stable/LTS 구분, kernel.org 활용법, 안드로이드 공용 커널 브랜칭 모델. 예습 챕터엔 전혀 없는 내용이지만, 교수 본인이 "이건 시험에 안 나온다"고 명시했으므로 시험 신호는 아니고 순수 배경 지식으로만 기록.
2. **Process image의 기초 워크스루** (notes.md §15) — initialized/uninitialized data, 실제 C 코드로 code/data/heap/stack이 각각 메모리 어디에 배치되는지 손으로 짚어준 예제. 예습 챕터는 이런 기초 온보딩 없이 바로 task_struct 필드 표로 들어가므로, 이 워크스루는 예습 챕터를 읽기 전 배경지식으로 유용.
3. **Process state의 일반 모델(new/ready/running/blocked/exit)** (notes.md §18) — 예습 챕터 §3은 `__state` 비트값·`TASK_KILLABLE`·`TASK_IDLE`·`TASK_NEW`·lost wakeup race 등 훨씬 깊은 내용을 다루는데, 이번 강의는 그 전 단계인 교과서적 5-state 모델과 Linux의 `TASK_RUNNING`/`TASK_INTERRUPTIBLE`/`TASK_UNINTERRUPTIBLE`/`TASK_STOPPED`까지만 다뤘다. 예습 챕터의 세부 내용과 **충돌하지 않고**, 그 앞 단계를 채워주는 관계.
4. **pidhash 도입은 됐지만 세부는 다음 강의로 예고** (notes.md §22) — 예습 챕터 §4는 이미 **최신 방식**(`struct pid`/`upid`, IDR 기반 `alloc_pid()`, RCU 기반 `find_pid_ns`/`find_vpid`)을 다루는데, 다음 강의에서 실제로 소개될 pidhash는 슬라이드 원본이 2.6.11 세대(`struct pid pids[PIDTYPE_MAX]`, 체이닝 해시 테이블)라서 **오래된 설계**일 가능성이 높다. **다음 주 강의를 소화할 때 이 구식 pidhash 설명이 예습 챕터의 최신 IDR 기반 설명과 정확히 어떻게 다른지 Modern kernel note로 짚어줄 필요가 있음 — 미리 표시해둔다.**

## Corrected / 확인 필요 (교재 서술과 다르거나, 수치가 다를 수 있는 지점)

- **커널 스택 크기 불일치 (확인됨)**: 실제 강의(notes.md §20)는 "프로세스당 8KB 커널 메모리 영역(thread_info + kernel stack)"이라고 말했는데, 이는 **32비트 x86, Linux 2.6.11 시절의 옛 슬라이드 수치**(`#define THREAD_SIZE 8192`, 4KB 페이지 2개)다. 반면 예습 챕터 §2는 **현대 x86-64 기준 THREAD_SIZE = 16 KiB**(`PAGE_SIZE << THREAD_SIZE_ORDER`, KASAN 끄면 order=2)라고 정확히 밝히고 있다. **두 수치 모두 각자의 시대·아키텍처 기준으로는 맞지만, 서로 다른 숫자라 혼동하기 쉽다** — 시험 답안에는 반드시 "x86-64 현대 커널 기준 16KiB"를 써야 하며, 강의에서 나온 8KB는 32비트/구버전 컨텍스트임을 구분해서 기억할 것.
- **매크로 이름 변경**: 강의(2.6.11 슬라이드 기준)는 프로세스 리스트 순회 매크로를 `for_each_task`라고 소개했다(notes.md §22). 예습 챕터 §4는 최신 커널 기준 정확한 이름인 `for_each_process`(`include/linux/sched/signal.h`)를 이미 쓰고 있다 — `for_each_task`는 구버전 이름이고 최신 커널의 실제 매크로명은 `for_each_process`이므로 시험 답안엔 후자를 쓸 것.

## 다음 액션 아이템 (Day 2)

- [ ] 다음 강의(예정: 수요일)에서 pidhash를 실제로 다루면, 그 내용이 2.6.11식 체이닝 해시 테이블인지 아니면 최신 커널 관점(IDR/RCU 기반)까지 언급하는지 확인하고, 예습 챕터 §4와의 관계를 Modern kernel note로 정리할 것.
- [ ] `weeks/02-linux-process-programming-1/README.md`에 "커널 스택 크기는 아키텍처·버전에 따라 다르다(32비트 2.6.x: 8KB, 현대 x86-64: 16KiB)"는 한 줄 각주를 추가할지 검토 — 학생이 강의와 교재에서 서로 다른 숫자를 보고 혼란스러워할 여지가 있음.
- [ ] `for_each_task`(구) vs `for_each_process`(신) 이름 차이를, 예습 챕터의 다른 "Modern kernel note" 항목들과 같은 형식으로 명시적으로 각주 처리할지 검토.
