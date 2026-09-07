# Quantum Computing: Overview, History & Recent Trends

> 소스: 강의 슬라이드(`ch01_qcp.pdf`, Bernd Burgstaller, CAS3140-01 Quantum Computer Programming, Fall 2026, Yonsei University). **이 챕터는 강의 전 슬라이드만으로 준비한 예습 자료다** — 실제 강의(강의 녹음 확보 시)는 `semester/week-01/`에 Day 2 섹션으로 정리하고, 이 챕터와 대조해 강조점·정정 사항을 `delta.md`로 남길 것. 이 과목은 coursebook에 처음 등록되는 과목이라 전체 학기 로드맵(`00-roadmap.md`)이 아직 없다 — 이 챕터는 슬라이드 1개 분량만 우선 다룬다.

## Learning goals

- 양자컴퓨팅을 "계산 패러다임"으로 정의할 때, superposition·entanglement·interference를 "이용한다"는 것이 구체적으로 무엇을 뜻하는지 설명할 수 있다.
- Feynman이 1981년에 제기한 문제 — 고전 컴퓨터로 양자역학적 시스템을 시뮬레이션하는 것이 왜 본질적으로 어려운지 — 를 상태 공간의 크기로 설명할 수 있다.
- 슬라이드가 언급하는 응용 후보(입자 충돌, 분자 화학, 얽힌 전자계, 초전도체, 블랙홀, 초기 우주)와, "아직 증명되지 않은 기대"라는 슬라이드 자체의 단서를 구분할 수 있다.
- 양자컴퓨터를 물리적으로 구현하는 주요 기술(초전도 큐비트, trapped ion, photonic, neutral atom)의 트레이드오프를 비교할 수 있다.
- 이 챕터가 왜 "역사·동기" 챕터이고 아직 큐비트의 수학적 정의(Hilbert space, 게이트)를 다루지 않는지 이해한다 — 그건 다음 챕터의 몫이다.

## Why this matters

이 과목은 물리학 배경 없는 컴퓨터과학 전공자를 대상으로 한다(교수가 첫 강의에서 반복 강조). 그래서 본격적으로 큐비트의 선형대수적 정의에 들어가기 전에, "왜 이걸 배우는가"를 역사적·동기적으로 먼저 짚는다. 이 챕터를 건너뛰고 바로 수학으로 들어가면 "복소 벡터공간에서 노름 1인 벡터를 다룬다"는 형식적 정의만 남고, 그게 왜 고전 비트로 못 하는 일을 하게 해주는지에 대한 직관이 없어진다. 이후 챕터(Hilbert space, 큐비트, 게이트, QKD/teleportation/Deutsch 알고리즘)는 전부 여기서 나온 세 가지 효과 — superposition, entanglement, interference — 를 수학적으로 정확히 다루는 것이 목표이므로, 이 챕터의 개념적 지도를 먼저 갖고 들어가는 게 유용하다.

## 1. 양자컴퓨팅이란 무엇인가

슬라이드의 정의: **양자컴퓨팅은 물질의 양자역학적 성질(superposition, entanglement, interference 등)을 계산에 이용하는 계산 패러다임이다.**

이 정의가 형식적으로 들리지만, 고전 계산과 대비하면 왜 근본적으로 다른 패러다임인지 보인다.

- 고전 비트 $n$개는 항상 $2^n$개의 이산 상태(bitstring) 중 **정확히 하나**에 있다. 상태를 기술하는 데 필요한 정보량은 $n$비트다.
- 큐비트 $n$개의 상태는 $2^n$차원 복소 벡터공간(Hilbert space)의 벡터다. 일반적인 상태는 그 $2^n$개의 계산기저(computational basis) 상태 **전부에 걸친 선형결합**(중첩, superposition)이며, 이를 정확히 기술하려면 $2^n$개의 복소 진폭(계수)이 필요하다.
- 이 차이(1개의 이산 상태 vs. $2^n$개 복소수)가 바로 아래 2절의 "고전 컴퓨터로 양자계를 시뮬레이션하기 어렵다"는 문제의 근원이다. 큐비트 하나 늘 때마다 고전 컴퓨터가 그 상태를 그대로 저장하는 데 필요한 메모리가 2배로 늘어난다(지수적 증가).

여기서 아직 안 다루는 것(다음 챕터 몫): 이 복소 진폭이 실제로 뭘 뜻하는지(측정 확률), 왜 그게 "이용 가능한 계산 자원"이 되는지(간섭을 통한 진폭 증폭/상쇄), entanglement가 왜 "부분의 합보다 큰" 정보를 만드는지. 이번 챕터는 정의와 동기까지만.

## 2. 기원 — Feynman 1981과 시뮬레이션 문제

슬라이드가 인용한 Feynman의 말(1981):

> "Nature isn't classical, dammit, and if you want to make a simulation of nature, you'd better make it quantum mechanical, and by golly it's a wonderful problem because it doesn't look so easy."

이는 1981년 MIT에서 열린 첫 "Physics of Computation" 학회 기조강연에서 나온 말로, 이후 논문으로 정리됐다(Feynman, "Simulating Physics with Computers," *International Journal of Theoretical Physics* 21, 1982, pp. 467–488).

**문제의 정확한 형태**: $n$개의 상호작용하는 양자 입자(예: 분자 속 전자들)로 이뤄진 계의 상태를 고전 컴퓨터로 정확히 표현하려면, 위 1절에서 본 것처럼 $2^n$개의 복소 진폭을 저장해야 한다. 입자 수가 늘어날수록 필요한 메모리가 지수적으로 폭발한다 — $n=50$짜리 계만 돼도 이미 현존하는 어떤 슈퍼컴퓨터의 메모리로도 부족하다. 이것이 "고전 컴퓨터로 양자역학적 시스템을 시뮬레이션하는 데 본질적인 어려움이 있다"(슬라이드 표현)는 것의 구체적 내용이다.

**Feynman의 제안(핵심 아이디어)**: 이 어려움을 우회하는 방법은, 시뮬레이션하는 컴퓨터 자체를 양자역학 원리로 만드는 것이다. 그러면 $n$개의 물리적 큐비트로 $n$개 입자계의 상태를 (지수적 메모리 없이) 자연스럽게 표현할 수 있다 — 큐비트 자체가 이미 $2^n$차원 공간에 사는 대상이기 때문. 이것이 "양자컴퓨터"라는 아이디어의 최초 동기다.

## 3. 자연 현상 시뮬레이션 — 기대되는 응용

슬라이드가 나열하는 응용 후보:

- **입자 충돌**(particle collision) — 고에너지 물리학의 격자 QCD(lattice QCD) 계산 등
- **분자 화학**(molecular chemistry) — 분자의 전자 구조 계산. 촉매·신약 설계에서 가장 자주 언급되는 근시일 응용 후보
- **얽힌 전자계**(entangled electrons) — 강상관계 전자계(strongly correlated electron systems), 응집물질물리
- **초전도체**(superconductors) — 특히 고온 초전도의 메커니즘은 현재도 고전적으로 완전히 풀리지 않은 문제
- **블랙홀**, **초기 우주** — 양자중력·고에너지 우주론 시뮬레이션

**슬라이드가 명시하는 단서**: "It is the expectation (**not proven yet**) that quantum computers will be able to efficiently simulate any processes that occur in nature." 즉 이건 증명된 정리가 아니라 기대(expectation)다. 실제로 "양자컴퓨터가 자연의 모든 과정을 효율적으로 시뮬레이션할 수 있다"는 주장은 형식적으로 증명되어 있지 않다 — 이 챕터 수준에서는 "왜 그럴듯한 기대인지"(2절의 논증)와 "왜 아직 증명이 아닌지"를 구분해서 알아두면 된다.

## 4. "There's plenty of room at the bottom" — 원자 스케일의 새로운 설계 공간

슬라이드가 함께 인용하는 또 다른 Feynman 발언(1959, 별도의 유명한 강연 — "There's Plenty of Room at the Bottom," Caltech, 나노기술의 개념적 기원으로 흔히 인용됨):

> "When we get to the very, very small world... we have a lot of new things that would happen that represent completely new opportunities for design. Atoms on a small scale behave like nothing on a large scale, for they satisfy the laws of quantum mechanics..."

요지: 원자 스케일에서는 거시 세계의 직관(뉴턴역학적 직관)이 통하지 않고 양자역학 법칙이 지배한다. 1981년 발언(2절)이 "그러니 계산도 양자역학적으로 하자"는 논증이라면, 1959년 발언은 그보다 20여 년 앞서 "작은 스케일은 완전히 다른 설계 공간"이라는, 같은 통찰의 더 이른 형태다. 두 인용을 나란히 놓은 건 이 아이디어가 하루아침에 나온 게 아니라 Feynman 안에서 수십 년에 걸쳐 이어진 사고였다는 맥락을 보여주기 위함으로 보인다.

## 5. 최근 타임라인 — 이론에서 실증으로

슬라이드에 "A Brief Quantum Computing Timeline"이 있고, 그중 가장 최근 항목이 2025년 QEC(quantum error correction) 성과를 가리킨다. **주의**: PDF에서 이 부분 텍스트가 깨져서 추출됐다("2025 QEC proof of concept by Googe's Wiow QPU") — 오타·OCR 손상으로 보이며, 정확한 문구·수치는 실제 강의 슬라이드 이미지나 강의 중 설명으로 확인이 필요하다. 참고로 실제 강의 전 알아두면 좋을 배경(슬라이드 밖 일반 지식, 강의 확인 전까지는 잠정 정보로 취급):

- Google의 초전도 큐비트 칩 "Willow"는 2024년 말 발표되어, **QEC의 "below-threshold" 스케일링**(논리 큐비트를 구성하는 물리 큐비트 수를 늘릴수록 논리 오류율이 지수적으로 감소하는 것)을 처음으로 실증했다고 보고됐다. 이는 QEC 이론이 실제로 스케일링 방향대로 작동함을 보인 이정표로 널리 인용된다.
- 이 챕터에서는 이 항목을 "확정 사실"이 아니라 "확인이 필요한 슬라이드 항목"으로만 표시해둔다 — 강의 후 `delta.md`에서 정확한 문구로 정정할 것.

## 6. 양자컴퓨터를 만드는 물리적 기술들

슬라이드는 양자컴퓨터를 물리적으로 구현하는 여러 기술을 개괄한다(출처: Popkin, *Science*, 2016). 주요 후보와 트레이드오프:

| 기술 | 대표 진영 | 강점 | 약점 |
|---|---|---|---|
| 초전도 큐비트(superconducting) | Google, IBM | 게이트 속도 빠름(수십 ns), 반도체 공정과 유사한 제작 방식 | 결맞음 시간(coherence time) 짧음(~수십–수백 μs), 극저온 냉동기(밀리켈빈) 필수 |
| Trapped ion | IonQ, Quantinuum | 게이트 충실도(fidelity) 매우 높음, 결맞음 시간 김 | 게이트 속도 느림, 이온 간 연결성 확장이 어려움 |
| Photonic | Xanadu, PsiQuantum | 상온 동작 가능, 양자통신과 자연스럽게 연결 | 결정론적 다중 큐비트 게이트 구현이 어려움(측정 기반 확률적 게이트) |
| **Neutral atom**(슬라이드가 "최근 추가"로 명시) | QuEra, Pasqal | trapped ion과 개념적으로 유사하나 **전하가 없는(neutral)** 원자를 광학 집게(optical tweezers)로 전자기장(optical lattice)에 가둬 조작. 결맞음 시간 양호, 재배치 가능한 배열로 확장성 좋음 | 개별 원자를 정밀 제어하는 것은 여전히 어려움 |

슬라이드 원문 각주: "Recent addition: neutral atoms; similar in concept to trapped ions but using neutral (uncharged) atoms suspended in electromagnetic fields (optical lattices) and manipulated with lasers (called tweezers). Decent coherence times and scalability, but controlling individual atoms still difficult."

## Common misconceptions

- **"양자컴퓨터는 모든 문제를 지수적으로 빠르게 푼다"** — 오개념. 알려진 speedup은 특정 구조를 가진 문제(정수 인수분해, 비정렬 탐색, 특정 시뮬레이션 등)에 국한되며, 일반 계산 문제 전반에 대한 만능 가속기가 아니다. 3절의 "자연 시뮬레이션" 기대조차 슬라이드 스스로 "증명되지 않았다"고 명시한다.
- **"큐비트는 그냥 상태가 더 많은 비트다(0, 1, 2, 3...)"** — 오개념. 큐비트는 이산적인 다치 논리가 아니라 연속적인 복소 진폭들의 중첩이며, 측정 시 확률적으로 계산기저 중 하나로 붕괴한다(1절 참고, 다음 챕터에서 formal하게 다룰 부분).
- **"양자컴퓨터가 고전 컴퓨터를 완전히 대체한다"** — 오개념. 현재도, 예견 가능한 미래에도 양자컴퓨터는 고전 컴퓨터와 결합된 하이브리드 구조로 동작한다(고전 컴퓨터가 호스트, 양자 프로세서는 특정 서브루틴만 담당). 이 과목이 다룰 QKD·teleportation·Deutsch 알고리즘 등도 전부 이런 하이브리드 맥락에서 실행된다.

## Glossary

- **Quantum computing (paradigm)**: a computing model that exploits quantum-mechanical properties (superposition, entanglement, interference) of matter to perform computation, as opposed to manipulating discrete classical bits.
- **Superposition**: a quantum state expressed as a linear combination of basis states, with complex-valued coefficients (amplitudes).
- **Entanglement**: a correlation between qubits such that the joint state cannot be factored into independent per-qubit states.
- **Interference (quantum)**: the phenomenon by which probability amplitudes add constructively or destructively, used algorithmically to amplify correct outcomes and cancel incorrect ones.
- **Quantum error correction (QEC)**: techniques that encode one logical qubit into many physical qubits so that errors can be detected and corrected without directly measuring (and thus collapsing) the encoded quantum information.
- **Coherence time**: the timescale over which a qubit retains its quantum state before decohering due to interaction with its environment.
- **Below-threshold scaling**: a QEC regime in which adding more physical qubits per logical qubit *decreases* the logical error rate, confirming that error correction overhead is worthwhile.

## References

- R. P. Feynman, "Simulating Physics with Computers," *International Journal of Theoretical Physics* 21 (1982): 467–488 (1981년 MIT, First Conference on the Physics of Computation 강연을 논문화).
- R. P. Feynman, "There's Plenty of Room at the Bottom" (1959년 Caltech 강연).
- Gabriel Popkin, "Scientists are close to building a quantum computer that can beat a conventional one," *Science*, Dec. 2016. (슬라이드가 기술 비교표의 출처로 직접 인용)
- 강의 슬라이드: `ch01_qcp.pdf`, Bernd Burgstaller, *Quantum Computing: Overview, History & Recent Trends*, CAS3140-01 Quantum Computer Programming, Fall 2026, Yonsei University.
- (미확인, 강의 중 확인 필요) Google Quantum AI의 Willow 칩 QEC 결과 — 슬라이드 원문 텍스트 손상으로 정확한 인용 불가, 5절 참고.
