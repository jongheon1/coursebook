# Quantum Computing: Overview, History & Recent Trends / Quantum Information Science / First Glimpse Into the Microscopic World

> 소스: 강의 슬라이드(`ch01_qcp_v2.pdf`, Bernd Burgstaller, CAS3140-01 Quantum Computer Programming, Fall 2026, Yonsei University, 총 74장). 이 챕터는 강의 전 슬라이드만으로 준비한 예습 자료다 — 실제 강의(강의 녹음 확보 시) 내용은 `semester/week-NN/`에 정리하고, 이 챕터와 대조해 강조점·정정 사항을 `delta.md`로 남길 것. **이 버전은 이전에 받은 12장짜리 초안(Part 1만 포함)을 대체한다** — 실제 강의안은 Part 1(개요·역사), Part 2(양자정보과학), Part 3(미시세계 첫 관찰) 세 파트, 74장 분량이다. 분량상 하루 강의로 끝나지 않고 여러 차시에 걸쳐 다뤄질 가능성이 높다. 이 과목은 coursebook에 처음 등록되는 과목이라 전체 학기 로드맵(`00-roadmap.md`)이 아직 없다.

## Learning goals

- **(Part 1)** 양자컴퓨팅을 계산 패러다임으로 정의하고, Feynman의 1981년 문제 제기를 상태 공간 크기로 설명할 수 있다.
- **(Part 1)** 물리적 큐비트 수와 논리적(오류정정된) 큐비트 수의 격차, 초전도/trapped ion/neutral atom 세 기술 진영의 큐비트 스케일링 로드맵을 비교할 수 있다.
- **(Part 2)** 양자컴퓨팅이 "강력하다"고 믿어지는 근거(인수분해, 복잡도 이론, 지수적 고전 시뮬레이션 비용)와 그 근거가 **아직 증명되지 않은 추측**이라는 한계를 구분할 수 있다.
- **(Part 2)** decoherence·NISQ·quantum error correction(QEC)이 서로 어떻게 연결되는지, QEC의 물리:논리 큐비트 오버헤드가 왜 그렇게 큰지 설명할 수 있다.
- **(Part 2)** 양자회로 모델의 제약(무루프, no fan-in/fan-out, no-cloning 예고)이 왜 생기는지, 결정론적/확률론적 양자 알고리즘의 차이를 설명할 수 있다.
- **(Part 3)** 이중슬릿 실험에서 관찰자 효과(which-path measurement)가 간섭무늬를 없애는 이유를 decoherence로 설명할 수 있다.
- **(Part 3)** 확률 진폭(complex amplitude)과 Born rule로 두 경로의 간섭(보강/상쇄)을 직접 손으로 계산할 수 있다 — 편광판 3장 퍼즐, 이중슬릿 진폭 계산 두 worked example로 연습.
- **(Part 3)** 큐비트가 왜 "상태가 3개 이상인 비트"가 아닌지, 동일하게 준비된 큐비트 100개를 측정해도 왜 같은 결과가 안 나오는지 설명할 수 있다.

## Why this matters

이 자료는 이 과목의 첫 실질 강의(행정 안내 다음 시간) 내용이며, 74장이라는 분량에서 보이듯 여러 차시에 걸쳐 다뤄질 것으로 보인다. 구조상 이 챕터는 큐비트의 선형대수적 정의(Hilbert space, 게이트 행렬)를 배우기 전의 **"왜"**에 해당한다: (Part 1) 왜 양자역학을 계산에 끌어오려 하는지, (Part 2) 그게 이론적으로 왜 강력하면서도 왜 만들기 어려운지, (Part 3) 애초에 "중첩·간섭"이라는 말이 어떤 물리 현상에서 나왔는지를 순서대로 다룬다. Part 3의 이중슬릿·편광판 예제는 이후 챕터에 나올 큐비트 상태 $\alpha|0\rangle+\beta|1\rangle$와 측정 확률 $|\alpha|^2$이 어디서 왔는지 미리 손으로 계산해보는 부분이라 특히 중요하다 — 여기서 계산 연습을 해두면 다음 챕터에서 형식(formalism)만 새로 익히면 된다.

---

## Part 1 — Quantum Computing: Overview, History & Recent Trends

### 1.1 양자컴퓨팅이란 무엇인가

슬라이드의 정의: **양자컴퓨팅은 물질의 양자역학적 성질(superposition, entanglement, interference 등)을 계산에 이용하는 계산 패러다임이다.** (슬라이드는 이걸 요즘 **"quantum advantage"**라는 말로도 부른다고 언급한다.)

고전 계산과 대비하면 왜 근본적으로 다른 패러다임인지 보인다.

- 고전 비트 $n$개는 항상 $2^n$개의 이산 상태(bitstring) 중 **정확히 하나**에 있다 — 기술에 필요한 정보량은 $n$비트.
- 큐비트 $n$개의 상태는 $2^n$차원 복소 벡터공간(Hilbert space)의 벡터다. 일반적인 상태는 $2^n$개의 계산기저 상태 **전부에 걸친 선형결합**(중첩)이며, 정확히 기술하려면 $2^n$개의 복소 진폭이 필요하다.
- 이 차이(1개의 이산 상태 vs. $2^n$개 복소수)가 바로 다음 절의 "고전 컴퓨터로 양자계를 시뮬레이션하기 어렵다"는 문제의 근원이다.

여기서 아직 안 다루는 것(다음 챕터 몫): 복소 진폭이 뭘 뜻하는지(측정 확률, → Part 3에서 미리 손으로 계산), 왜 그게 계산 자원이 되는지(간섭을 통한 증폭/상쇄), entanglement가 왜 "부분의 합보다 큰" 정보를 만드는지.

### 1.2 기원 — Feynman 1981과 시뮬레이션 문제

슬라이드가 인용한 Feynman의 말(1981, MIT 첫 "Physics of Computation" 학회 기조강연, 이후 논문화: Feynman, "Simulating Physics with Computers," *International Journal of Theoretical Physics* 21, 1982, pp. 467–488):

> "Nature isn't classical, ..., and if you want to make a simulation of nature, you'd better make it quantum mechanical, and ... it's a wonderful problem because it doesn't look so easy."

**문제의 정확한 형태**: $n$개의 상호작용하는 양자 입자로 이뤄진 계의 상태를 고전 컴퓨터로 정확히 표현하려면 $2^n$개의 복소 진폭을 저장해야 한다(1.1절). 입자 수가 늘어날수록 필요한 메모리가 지수적으로 폭발한다.

**Feynman의 제안**: 시뮬레이션하는 컴퓨터 자체를 양자역학 원리로 만들면, $n$개의 물리적 큐비트로 $n$개 입자계의 상태를 지수적 메모리 없이 자연스럽게 표현할 수 있다 — 큐비트 자체가 이미 $2^n$차원 공간에 사는 대상이기 때문.

### 1.3 자연 현상 시뮬레이션 — 기대되는 응용

슬라이드가 나열하는 응용 후보: **입자 충돌**(particle collision, 격자 QCD 등), **분자 화학**(molecular chemistry, 근시일 응용 후보로 가장 자주 언급됨), **얽힌 전자계**(entangled electrons, 강상관계 전자계), **초전도체**(고온 초전도 메커니즘은 지금도 고전적으로 완전히 안 풀림), **블랙홀**, **초기 우주**(양자중력·고에너지 우주론).

**슬라이드가 명시하는 단서**: "It is the expectation (**not proven yet**) that quantum computers will be able to efficiently simulate any processes that occur in nature." — 증명된 정리가 아니라 기대(expectation)다.

### 1.4 "There's plenty of room at the bottom"

슬라이드가 함께 인용하는 또 다른 Feynman 발언(1959, Caltech 강연 — 나노기술의 개념적 기원으로 흔히 인용됨):

> "When we get to the very, very small world... we have a lot of new things that would happen that represent completely new opportunities for design. Atoms on a small scale behave like nothing on a large scale, for they satisfy the laws of quantum mechanics..."

1981년 발언(1.2절)이 "그러니 계산도 양자역학적으로 하자"는 논증이라면, 1959년 발언은 20여 년 앞서 "작은 스케일은 완전히 다른 설계 공간"이라는, 같은 통찰의 더 이른 형태다.

### 1.5 최근 타임라인과 물리적 구현 기술

슬라이드의 "A Brief Quantum Computing Timeline"에 가장 최근 항목으로 2025년 QEC 성과가 있는데, **PDF에서 이 부분 텍스트가 v1·v2 모두 동일하게 깨져 나온다**("2025 QEC proof of concept by Googe's Wiow QPU") — 두 버전에서 재현되는 걸 보면 원본 슬라이드 파일 자체의 폰트/인코딩 문제로 보인다. 강의 중 정확한 문구·수치를 확인해서 정정할 것 (참고로 일반적으로 알려진 배경: Google의 초전도 큐비트 칩 "Willow"가 2024년 말 QEC의 "below-threshold" 스케일링을 처음 실증했다고 보고됨 — 확정 전까지는 잠정 정보로 취급).

**양자컴퓨터를 만드는 물리적 기술들**(출처: Popkin, *Science*, 2016 [Gab16]):

| 기술 | 강점 | 약점 |
|---|---|---|
| 초전도 큐비트(superconducting) | 게이트 속도 빠름 | 결맞음 시간 짧음, 극저온 필수 |
| Trapped ion | 게이트 충실도 매우 높음, 결맞음 시간 김 | 게이트 속도 느림, 연결성 확장 어려움 |
| Photonic | 상온 동작 가능 | 결정론적 다중 큐비트 게이트 구현이 어려움 |
| **Neutral atom**(슬라이드가 "최근 추가"로 명시) | 결맞음 시간 양호, 재배치 가능한 배열로 확장성 좋음 | 개별 원자 정밀 제어가 여전히 어려움 |

**초전도 큐비트 프로세서 상세**(예: IBM 2016, 5큐비트): 큐비트 자체는 **Josephson junction**(거의 무손실) 기반이고, **마이크로파 공진기**(microwave resonator)가 (1) 큐비트 상태 판독, (2) 다중 큐비트 버스, (3) 노이즈 필터 역할을 겸한다. 양자 연산은 공진기에 4–8 GHz 대역 마이크로파 펄스를 보내서 수행한다. Trapped-ion 쪽도 별도 개략도(Blatt & Wineland 2008 [BW08])로 소개된다.

### 1.6 물리적 큐비트 수 대 "논리적" 큐비트 수 — 왜 격차가 큰가

지난 25년간 단일 양자컴퓨트 노드의 **물리적** 큐비트 수는 꾸준히 늘어왔다(pre-fault-tolerance 시대). 반면 "논리적"(오류정정을 거친) 큐비트 로드맵을 보면 IBM·Google·IonQ·Quantinuum·QuEra 등이 수천~수백만 개의 **물리** 큐비트로 수만~수십만 개의 **논리** 큐비트를 목표로 잡고 있다 — 물리:논리 비율이 왜 이렇게 큰지는 Part 2.6(QEC 오버헤드)에서 설명한다.

---

## Part 2 — Quantum Information Science

### 2.1 정의와 6개 하위분야

$$\text{quantum theory} + \text{computer science} + \text{information theory} = \text{quantum information science (QIS)}$$

QIS의 6개 분야: (1) **quantum computing** — 어려운 문제의 해법 가속, (2) **quantum cryptography** — 양자물리 법칙에 기반한 프라이버시, (3) **quantum networking** — 양자성(quantumness)을 전 세계로 분배, (4) **quantum information concepts** — entanglement·error correction·complexity, (5) **quantum sensing** — 감도·공간분해능 향상, (6) **quantum simulation** — 양자 다체계 현상 연구.

### 2.2 두 가지 근본 원리

1. **Quantum complexity** — 양자컴퓨팅이 왜 강력하다고 여겨지는가.
2. **Quantum error correction** — 양자컴퓨팅이 왜 대규모로 확장 가능하다고 여겨지는가.

### 2.3 왜 양자컴퓨팅이 강력하다고 믿어지는가 — 그리고 그 한계

1. 고전적으로는 어렵다고 믿어지지만 양자컴퓨터에는 쉬운 문제가 있다(예: 인수분해).
2. 복잡도 이론적 논거들은 양자컴퓨터를 고전적으로 시뮬레이션하기 어렵다는 걸 시사한다.
3. 양자컴퓨터를 고전 컴퓨터로 효율적으로 시뮬레이션하는 방법을 아직 모른다 — 알려진 최선의 시뮬레이션 알고리즘 비용은 큐비트 수에 지수적으로 증가한다. **이것도 아직 증명 안 된(다만 널리 믿어지는) 추측이다.**
4. 하지만 양자컴퓨터의 힘에는 한계가 있다 — 양자컴퓨터가 NP-hard 최적화 문제(예: 외판원 문제)의 최악 사례(worst-case)를 풀 수 있다고는 믿어지지 않는다. **이 역시 추측이다.**

즉 "정확히 어떤 문제가 quantumly easy인가"는 아직 열린 연구 질문이다.

### 2.4 왜 양자컴퓨팅이 어려운가

요구사항이 서로 모순적이다: **큐비트끼리는 강하게 상호작용해야 하지만**, **환경과는 상호작용하면 안 된다** — 우리가 제어하거나 측정할 때만 예외.

**Decoherence**: 실험실의 미시계에서 관찰되는 양자 현상이 왜 일상의 거시계에서는 안 보이는지를 설명하는 개념. 양자컴퓨터를 decoherence와 다른 오류원으로부터 보호하려면, 계산 중 환경이 양자컴퓨터의 상태에 대해 "알게 되는 것"(정보 유출)을 막아야 한다. → **이 절은 Part 3.1의 이중슬릿 which-path 실험과 정확히 같은 이야기다**: 슬릿을 지나간 경로 정보가 환경으로 새어나가는 순간 간섭이 사라진다.

### 2.5 NISQ 시대 (Preskill 2018 [Pre18])

- (노이즈 있는) 50–100 큐비트 양자컴퓨터가 이미 존재한다 — **N**oisy **I**ntermediate-**S**cale **Q**uantum (NISQ).
- NISQ 장치는 현존 최강 슈퍼컴퓨터로도 brute-force 시뮬레이션이 안 된다.
- 노이즈가 NISQ 시대 기술의 계산 능력을 제한한다.
- NISQ는 물리 탐구에 흥미로운 도구가 될 것이고, 다른 유용한 응용도 있을 수 있다(미정).
- **NISQ 자체가 세상을 바꾸지는 않는다** — 미래의 더 강력한 양자 기술로 가는 디딤돌로 여겨진다.
- 확장 가능한(scalable) 양자컴퓨터는 여전히 수십 년 남았을 수 있다(얼마나 걸릴지 확실치 않음).

### 2.6 스케일 업의 가파른 경사 — QEC 오버헤드

- NISQ 시대 장치는 QEC로 보호되지 않는다 — 노이즈가 정확히 실행 가능한 계산 규모를 제한한다.
- 어려운 문제를 풀려면 QEC가 필수적이지만, **QEC는 큐비트·게이트 수에서 큰 오버헤드 비용**을 수반한다.
- 비용은 하드웨어 품질과 알고리즘 복잡도 둘 다에 좌우된다.
- 현재 하드웨어 기준, 보호된 논리 큐비트 1개당 물리 큐비트 **수백~수천 개**가 필요할 수 있다.
- **2025년 추정치**: 2048비트 RSA 정수를 1주일 이내에 인수분해하려면 약 **898,000개**의 물리 큐비트가 필요.
- IBM: quantum low-density parity-check(qLDPC) 코드로 **12:1** 비율을 projected. 오버헤드까지 포함하면 논리 큐비트 200개에 물리 큐비트 1만 개(**50:1**).
- 완전한 fault-tolerant 양자컴퓨터가 오려면 게이트 충실도, 시스템 엔지니어링, 알고리즘 설계, 오류정정 프로토콜 전반의 발전이 필요하다.

(1.6절의 "물리:논리 큐비트 격차"가 왜 그렇게 큰지가 여기서 설명된다.)

### 2.7 NISQ 시대의 양자 speedup

- Quantum advantage 실증들은 양자 세계가 제공하는 인상적인 계산 자원을 확인해준다.
- NISQ 시대엔 **heuristic 양자 알고리즘**(왜 잘 작동하는지 초기엔 이론적 증명이 없는 알고리즘)을 활용할 수 있다 — 고전 예: simplex 알고리즘, 딥러닝.
- 진짜 확장 가능한 양자컴퓨팅에는 QEC가 필요한데, 오버헤드 비용이 커서 근시일 내엔 실현이 어려울 수 있다.
- 게이트 오류율을 낮추면 QEC 오버헤드도 줄고, QEC 없이 쓰는 알고리즘의 도달 범위도 넓어진다.
- NISQ가 그 자체로 세상을 바꾸지는 않는다. 현실적 목표는 미래 장치로 더 큰 성과를 내기 위한 길을 닦는 것 — fault-tolerant QC를 향한 진전이 계속 최우선 과제여야 한다.

### 2.8 양자계산 모델들 — 전부 동치

여러 양자계산 모델(모두 계산 능력이 동치): **quantum Turing machines**, **quantum circuits**, **measurement-based quantum computing (MBQC)**, **adiabatic quantum computing**.

고전 튜링머신 대비 계산 능력 비교는 여전히 논쟁적인 경계다([NC11], p. 6). Strong Church-Turing thesis의 수정판:

> "Any algorithmic process can be simulated efficiently using a **probabilistic** Turing machine."

("probabilistic"이 추가된 이유는 무작위 알고리즘 때문 — 다만 튜링머신 자체는 결정론적이다.) **Shor's algorithm**은 양자컴퓨터(QC)에서는 효율적으로 되지만 튜링머신(TM)에서는 안 되는 계산이 존재한다는 강력한 정황 증거다. TM이 QC를 시뮬레이션하는 효율성 문제 자체도 또 다른 정황 증거.

### 2.9 양자 회로의 형식적 제약

- 양자회로는 기본 게이트 집합 $\{U_1, U_2, \dots, U_n\}$을 쓴다. 각 게이트는 유한 개 큐비트에 작용하는 **unitary 변환**이며, 임의의 unitary 변환은 이 게이트들로 구성할 수 있다.
- 회로는 왼쪽에서 오른쪽으로 읽는다. 입력은 관습적으로 전부 $|0\rangle$인 계산기저 상태.
- 양자회로는 **순수 데이터 흐름**만 가진다(제어 흐름 없음).
  - **fan-in 불가**: 가능하면 비가역적인 고전 OR 같은 게이트를 허용하게 됨.
  - **fan-out 불가**: 큐비트를 복제해야 하는데, 이는 **no-cloning theorem**(다음 챕터에서 소개)에 위배됨.
  - 결과적으로 **양자회로는 루프를 가질 수 없다**.
- 회로 구성 자체는 고전 컴퓨터가 지휘한다.
- 계산 끝에 결과는 기저 $\{|0\rangle, |1\rangle\}$로의 projection을 통해 읽어낸다.

### 2.10 양자 프로그래밍 언어들

QASM, **Qiskit**(IBM), **Cirq**(Google), Forest/pyQuil(Rigetti), Q#(Microsoft), Ocean(D-Wave) — 대부분 양자회로를 명세하기 위한 것들이다. (week-01 정리노트에 이미 기록된 대로, 이 과목은 Qiskit + IBM Quantum Platform으로 실습한다.)

### 2.11 컴퓨터과학의 문 앞에 선 양자컴퓨팅

양자컴퓨팅은 **암호**, **화학 시뮬레이션**, **최적화**, **머신러닝**에서의 강력한 잠재력 때문에 컴퓨팅 혁명을 촉발할 수 있다. 컴퓨터과학자들은 대규모 fault-tolerant 양자컴퓨팅 시스템 설계를 주도하도록 요청받고 있다 — 이 분야는 아직 신흥 분야이고, 소프트웨어부터 하드웨어까지 최신 기술 수준이 상당히 미성숙하다. (양자컴퓨팅 기술 스택은 여러 계층에 걸쳐 있고 계층 간 최적화 기회가 많다 — Prof. Yufei Ding 슬라이드 인용.)

### 2.12 양자 컴퓨터과학의 두 얼굴

1. **회로 설계(Circuit Design)** — 개별 부품(게이트)은 알고 있으니, 이를 조립해 효율적인 전체 회로를 만드는 이해와 숙련이 필요하다.
2. **알고리즘 설계(Algorithm Design)** — 양자역학은 본질적으로 확률적이라, 회로가 항상 바로 답을 주지는 않는다. 어떤 알고리즘은 그렇지만, 다른 알고리즘은 같은 입력을 같은 회로에 여러 번 넣어 확률 법칙이 작동하도록 해야 한다. 알고리즘이 적절한 오차 허용도로 답에 수렴할 가능성이 있는지 수학적으로 분석해야 한다.

### 2.13 Worked example — 고전 AND 게이트 vs. 양자 Hadamard$^{\otimes2}$ 게이트

**고전(CAS1100에서 배운 AND 게이트)**: 진리표 하나면 끝. "문제될 게 없었다"(슬라이드 표현).

**양자**: 2큐비트 상태를 진리표가 아니라 **행렬**로 다뤄야 한다. 2큐비트 상태를

$$|\psi\rangle_2 = \begin{pmatrix}\alpha\\\beta\\\gamma\\\delta\end{pmatrix}$$

로 놓고 $H^{\otimes 2}$ (Hadamard 게이트의 2큐비트 텐서곱) 게이트를 통과시키면($|\psi\rangle_2 \to H^{\otimes2} \to H^{\otimes2}|\psi\rangle_2$, 즉 큐비트 $|\psi\rangle_2$가 들어가고 다른 큐비트 $H^{\otimes2}|\psi\rangle_2$가 나온다는 뜻):

$$H^{\otimes 2}|\psi\rangle_2 = \frac12\begin{pmatrix}1&1&1&1\\1&-1&1&-1\\1&1&-1&-1\\1&-1&-1&1\end{pmatrix}\begin{pmatrix}\alpha\\\beta\\\gamma\\\delta\end{pmatrix} = \frac12\begin{pmatrix}\alpha+\beta+\gamma+\delta\\\alpha-\beta+\gamma-\delta\\\alpha+\beta-\gamma-\delta\\\alpha-\beta-\gamma+\delta\end{pmatrix}$$

슬라이드는 이 부분을 "나중에 자세히 다룬다"고 명시한다 — 지금 단계의 포인트는 계산 결과 자체가 아니라, **왜 트루스테이블이 아니라 행렬 곱이 필요한가**(중첩 상태는 이산값이 아니라 연속적인 복소 진폭들의 벡터이므로)이다.

### 2.14 결정론적 vs. 확률론적 양자 알고리즘

슬라이드가 예고편으로 제시하는 회로 구조: $|0\rangle^n \to H^{\otimes n} \to U_f \to H^{\otimes n} \to$ 측정(자세한 설명은 이후 강의).

- **결정론적 알고리즘**: 회로를 **한 번만** 돌리고 측정하면 즉시 답이 나온다. 예: 0이 나오면 함수가 constant, 0이 아닌 값이 나오면 balanced (자세한 알고리즘 이름과 증명은 이후 강의 — 여기서 추측하지 않는다). 여러 번 평가해야 하는 전형적 고전 알고리즘과 대비된다.
- **확률론적 알고리즘**: 가끔 틀린 답을 줄 수 있다. $n+T$ 회 시도(pass, 한 pass = 회로 1회 실행) 후 끝나도 답을 못 찾으면 실패. 성공하면 오류확률 $<1/2^T$, 시간복잡도 $O(n^3)$(다항시간)로 문제를 풀었다고 본다.
- 결정론적이든 확률론적이든 목표는 같다: 고전보다 빠른 회로 설계.

### 2.15 Perspective & Outlook

양자컴퓨팅은 고전컴퓨팅을 대체하는 게 아니라 **한 단계 업그레이드**다. Superposition·entanglement·interference를 활용하지만, 모든 걸 고전보다 잘한다고 예견되지는 않는다 — **대부분의 처리 요구는 여전히 고전 비트 기반 로직이 더 효율적으로 처리할 것이다.** 목표는 현재 못 푸는 문제를 위한 새 도구를 만드는 것이지, 안 고장난 걸 고치는 게 아니다.

---

## Part 3 — First Glimpse Into the Microscopic World

### 3.1 고전물리를 놀라게 한 실험들

#### Stern–Gerlach 실험

은 원자를 불균일한 자기장을 통과시키면, 스핀에 따라 위/아래로 휘어진다. 이는 이산적인(discrete) 양자 상태 간의 분리를 직접 관측할 수 있게 해준다 — $z$-spin 같은 관측량이 이산적인 "양자"(quanta)로 나타나는 것이 바로 **"quantum mechanics"라는 이름의 유래**다. 실험 구성: (1) 노(furnace), (2) 은 원자 빔, (3) 불균일 자기장, (4) 고전적으로 기대되는 결과(연속 분포), (5) 실제 관측 결과(이산 분리).

#### 이중슬릿 실험 — "양자역학의 심장"(Feynman)

빛과 물질은 고전적으로 정의된 파동과 입자 양쪽의 특성을 모두 보인다 — 양자역학적 현상의 근본적인 확률적 본성을 보여준다. 광자를 (한 번에 하나씩) 두 개의 좁은 슬릿이 있는 벽으로 쏜다(전자를 쓴 변형 실험도 있고, 최근에는 최대 2000개 원자로 이뤄진 분자로도 재현됨). 각 광자가 뒤쪽 스크린 어디에 도달할지는 확률적이다.

어떤 위치는 확률이 높고, 어떤 위치는 낮다. 뒤쪽 스크린의 어떤 구간에 대해:
- $P$ = 두 슬릿 다 열었을 때 그 구간에 도달할 확률
- $P_1$ = 슬릿 1만 열었을 때 그 구간에 도달할 확률
- $P_2$ = 슬릿 2만 열었을 때 그 구간에 도달할 확률

고전적 기대: $P = P_1 + P_2$. **하지만 실제론 그렇지 않다** — 두 슬릿을 다 열었을 때 전혀 안 맞는 자리(dark spot)가, 한쪽 슬릿만 열면 오히려 잘 맞는 경우가 있다. 단일슬릿 패턴에는 없던 어두운 지점들이 이중슬릿 패턴에서 나타난다.

#### which-path 측정과 decoherence — 관찰하면 무늬가 사라진다

각 슬릿에 "광자가 어느 슬릿으로 지나갔는지" 측정하는 장치를 달면, 측정 결과가 달라진다: 간섭무늬 대신 슬릿마다 하나씩, **두 개의 밝은 띠**만 남는다 — 마치 전자가 고전적인 확률론을 따르는 것처럼 보인다. **이유**: 측정 장치 때문에, 어느 슬릿으로 지나갔는지에 대한 정보가 바깥 환경으로 새어나가기(leak) 때문이다. 계가 환경과 결합했을 때 고전적 확률론으로 되돌아가는 이 현상을 **decoherence**라고 부른다(전자가 더 이상 중첩 상태에 있지 않은 것).

> **Part 2.4와 정확히 같은 이야기다**: "환경과 상호작용하면 안 된다"는 요구사항이 실제로 깨지는 순간이 바로 이 which-path 측정이다.

#### Decoherence, 그리고 Schrödinger의 고양이

Decoherence는 일상생활에서 왜 통상적인 확률 법칙이 잘 작동하는 것처럼 보이는지를 설명한다. 양자 중첩은 입자(또는 입자 집합)가 환경으로부터 **고립**돼 있을 때 일어나는 조건이다 — 그리고 이 고립의 필요성이 바로 양자컴퓨터를 만들기가 그렇게 어려운 이유다.

Schrödinger의 고양이는 **실제로는 중첩 상태에 들어간 적이 없다**: 상자 속 고양이는 살아있음/죽어있음의 중첩이 아니다. 왜냐하면 고양이는 끊임없이 자신의 환경과 상호작용하고, 그 상호작용이 "고양이 시스템"에 대한 정보를 계속 흘려보내기 때문이다(사고실험이 실제로 짚는 포인트는 "중첩이 실제로 일어난다"가 아니라 "거시계는 이런 이유로 중첩에 못 들어간다"는 것).

1900–1926년 사이 물리학자들은 이중슬릿 같은, 통상적인 역학·확률 법칙과 안 맞는 현상들을 계속 발견했고 그때마다 임시방편적(ad-hoc) 설명을 붙였다. 이게 정식화된 건 Max Planck, Niels Bohr, Werner Heisenberg, Wolfgang Pauli, Erwin Schrödinger 등이 양자역학의 일반 규칙을 만들면서다(1925–1927년경, 1930년 코펜하겐 회의 사진이 슬라이드에 등장).

#### 확률에서 진폭으로

당시 관측을 설명하려면 확률 계산법 자체를 바꿔야 했다: $P \in [0,1]$인 확률 대신 **복소 진폭** $\alpha \in \mathbb{C}$을 쓰기 시작했다(양수/음수, 실수부·허수부를 가진 임의의 복소수). 양자역학의 핵심 성질: 고립계의 상태를 완전히 기술하려면, 측정 시 나올 수 있는 **가능한 결과마다 진폭 하나씩**이 필요하다. (예고: 측정하면 큐비트는 0 또는 1로 붕괴하므로, 큐비트 하나를 나타내려면 진폭 2개가 필요하다 — 다음 챕터에서 확장.)

**Born rule**: 특정 결과가 나올 확률은 그 진폭의 절댓값 제곱이다.

$$P = |\alpha|^2 = \mathrm{Re}(\alpha)^2 + \mathrm{Im}(\alpha)^2$$

#### Worked example — 이중슬릿 간섭을 진폭으로 계산하기

뒤쪽 스크린의 한 구간에 대해, 두 슬릿 다 열었을 때 진폭을 $\alpha$, 슬릿 1만 열었을 때 진폭을 $\alpha_1$, 슬릿 2만 열었을 때 진폭을 $\alpha_2$라 하면 (고전적 확률 덧셈 규칙의 아날로그, 다만 이번엔 복소수):

$$\alpha = \alpha_1 + \alpha_2$$

Born rule을 적용하면(두 슬릿 다 열렸을 때):

$$P = |\alpha|^2 = |\alpha_1+\alpha_2|^2 = (\alpha_1+\alpha_2)(\alpha_1+\alpha_2)^* = |\alpha_1|^2 + |\alpha_2|^2 + \alpha_1\alpha_2^* + \alpha_1^*\alpha_2$$

여기서 $\alpha_1\alpha_2^* + \alpha_1^*\alpha_2$ 항이 바로 **간섭**(interference) 항이다 — 고전적 확률 덧셈($P_1+P_2$)에는 없는 교차항.

**숫자를 넣어보면**: $\alpha_1 = 1/2,\ \alpha_2 = -1/2$라 하자.
- 슬릿 하나만 열면: $P = |1/2|^2 = |-1/2|^2 = 1/4$ (양쪽 다 동일).
- 둘 다 열면: $P = |1/2|^2 + |-1/2|^2 + (1/2)(-1/2) + (1/2)(-1/2) = 1/4+1/4-1/4-1/4 = 0$.

**완전한 상쇄간섭**이다 — 각 슬릿을 따로 열면 $1/4$씩 도달 확률이 있는 자리인데, 둘 다 열면 그 자리엔 아예 아무것도 안 온다. 핵심은 **광자/전자 "하나"가 자기 자신과 간섭한다**는 것이지, 여러 입자끼리 서로 부딪히는 게 아니다.

#### Waves 배경지식

물리·수학에서 **파동(wave)**은 하나 이상의 물리량이 평형 상태에서 벗어나 전파되는 동적 교란이다(물 자체와 물결 파동은 다른 것이라는 점에 유의). **회절(diffraction)**은 파동이 장애물 모서리를 돌아가거나 구멍을 통과해 기하학적 그림자 영역까지 번지는 간섭 현상이다.

**간섭(interference)**: 두 파동이 모든 시공간 점에서 변위를 더해 합쳐지면서, 진폭이 더 크거나 작거나 같은 결과 파동을 만드는 현상.
- **보강간섭**(constructive): 두 파동의 위상차가 $\pi$(180°)의 **짝수배**일 때.
- **상쇄간섭**(destructive): 위상차가 $\pi$의 **홀수배**일 때.
- 그 외에는 두 파동의 합이 최소값과 최대값 사이 어딘가가 된다.

#### 파동-입자 이중성 (wave-particle duality)

양자역학에서 모든 입자·양자적 실체는 입자 또는 파동, 둘 중 하나로 기술될 수 있다는 개념 — 고전적인 "입자"나 "파동" 개념 각각으로는 양자 규모 객체의 행동을 완전히 설명할 수 없음을 나타낸다. Einstein의 말:

> "It seems as though we must use sometimes the one theory and sometimes the other, while at times we may use either. We are faced with a new kind of difficulty. We have two contradictory pictures of reality; separately neither of them fully explains the phenomena of light, but together they do."

이중슬릿 실험에서 빛의 파동성이 슬릿을 통과하는 광자(들)를 간섭시켜 스크린의 명암 띠를 만들지만(고전 입자, 예를 들어 테니스공에게서는 기대할 수 없는 현상), 광자는 스크린에서 항상 **개별 입자로서 이산적인 점**에 흡수된 채로 관측된다(파동이 아니라). 간섭무늬는 이 입자 타격들의 밀도 분포로 나타난다 — 밝은 띠는 광자가 그 위치에 착지할 확률이 높다는 뜻, 어두운 부분은 확률이 낮다는 뜻이다.

#### Worked example — 편광판 세 장 퍼즐: 필터를 더 끼우면 왜 빛이 더 통과하는가

**설정**: 광원과 스크린 사이에 필터 A를 놓으면 빛의 세기가 절반이 된다. 필터 A와 직교하는 필터 C를 (A 뒤에) 넣으면 출력이 0이 된다. 그런데 **A와 C 사이에 45° 기울어진 필터 B를 끼워 넣으면**, 직관과 반대로 빛의 **$1/8$이 스크린에 도달한다**(YouTube 실증 영상: `https://www.youtube.com/watch?v=5SIxEiL8ujA`).

**설명 (측정 공준 + 기저 변환)**:
1. 광자의 편광 상태는 적절한 방향을 가리키는 단위벡터로 모델링된다. 임의의 편광은 $|\psi\rangle = \alpha|{\uparrow}\rangle + \beta|{\to}\rangle$로 쓴다($|{\to}\rangle$은 수평 편광 기저벡터, $|{\uparrow}\rangle$은 수직 편광 기저벡터, $\alpha,\beta\in\mathbb C,\ |\alpha|^2+|\beta|^2=1$).
2. 측정 공준: 2차원계를 측정하는 장치는 그 측정이 이뤄지는 기준의 정규직교기저를 갖는다. 측정은 중첩 상태를 두 기저벡터 중 하나로 붕괴시킨다.
3. **필터 A**를 통과한 광자는 전부 $0|{\uparrow}\rangle + 1|{\to}\rangle$ 상태(순수 수평 편광)가 된다 — 세기가 절반이 되는 이유.
4. **필터 C**는 $|{\uparrow}\rangle$ 기저로 측정한다 — 수평 편광 광자는 수직 방향 성분이 0이므로, **하나도 통과 못 한다**(A 다음 바로 C면 출력 0).
5. **필터 B**를 끼우면, B는 대각선 기저 $\{|{\nearrow}\rangle, |{\nwarrow}\rangle\} = \left\{\tfrac1{\sqrt2}(|{\uparrow}\rangle+|{\to}\rangle),\ \tfrac1{\sqrt2}(|{\uparrow}\rangle-|{\to}\rangle)\right\}$로 측정한다. 필터 A를 나온 수평 편광 광자는 이 기저로 재표현하면 $|{\nearrow}\rangle$로 측정될 확률이 **0.5**다(그 절반은 B를 통과).
6. B를 통과해 $|{\nearrow}\rangle$ 상태가 된 광자를 다시 $\{|{\uparrow}\rangle,|{\to}\rangle\}$ 기저로 측정하는 필터 C를 통과할 확률도 **0.5**다($|{\nearrow}\rangle = \tfrac1{\sqrt2}(|{\uparrow}\rangle+|{\to}\rangle)$이므로 $|{\uparrow}\rangle$ 성분의 확률이 $|1/\sqrt2|^2=0.5$).
7. 전체: $\underbrace{1/2}_{\text{A}} \times \underbrace{1/2}_{\text{A}\to\text{B}} \times \underbrace{1/2}_{\text{B}\to\text{C}} = 1/8$.

**포인트**: 매 측정(필터)이 상태를 그 측정 기저로 **붕괴**시키기 때문에, 중간에 다른 기저로 측정하는 필터를 추가하면 오히려 최종 통과 확률이 올라갈 수 있다 — 순수하게 편광을 "걸러내는" 고전적 직관과 반대되는 현상이다.

### 3.2 Bits vs. Qubits

고전 컴퓨팅은 0 또는 1, 그게 전부인 **비트**를 쓴다. 양자컴퓨팅은 **큐비트**의 세계에서 일어난다. 큐비트 $|\psi\rangle$는 측정되기 전까지는 0도 1도 아닌 상태 — 둘의 **중첩**으로, 형식적으로는

$$|\psi\rangle = \alpha|0\rangle + \beta|1\rangle$$

기호 $|0\rangle$은 고전 "0"에, $|1\rangle$은 고전 "1"에 대응한다. $\alpha,\beta$는 큐비트에 "0"과 "1"이 각각 얼마나 들어있는지를 나타내는 수다(슬라이드 비유: 티스푼만큼의 "0"과 테이블스푼만큼의 "1"). 이런 계를 **이상태계(two-state system)**라 부른다 — 가능한 모든 상태를 오직 두 상태의 중첩으로 표현할 수 있다는 뜻.

큐비트는 (아)원자 수준(광자, 전자의 스핀 상태, 원자의 바닥상태+들뜬상태 등)에 존재한다. 반면 고전 비트는 보통 수백만 개의 원자를 필요로 한다(실험실에서는 12개까지 줄인 사례가 있다고 언급).

**고전 실험**: 동일한 값 $x$로 초기화된 100개의 고전 1비트 저장 위치가 있다고 하자(전부 0이거나 전부 1). 첫 번째 위치를 측정해 1이 나오면, 나머지 99개도 전부 1이라는 걸 즉시 안다 — 실제로 측정해도 확인될 뿐이다.

**양자 실험**: 동일하게 준비된 큐비트 $|\psi\rangle$ 값으로 채워진 100개의 큐비트 메모리 위치가 있다고 하자. 첫 번째 위치를 측정하면 (고전과 마찬가지로) "0" 또는 "1"이 나온다 — "1"이 나왔다고 하자. **나머지 99개는 어떨까? 전혀 예측할 수 없다** — 어떤 건 1, 어떤 건 0이 나올 수 있다, 100개 모두 애초에 동일한 큐비트 값으로 준비됐음에도. 게다가 이 측정은 준비했던 원래 상태를 **영구적으로 파괴**한다(결과는 고전적인 "0" 또는 "1"로 남는다).

**얽힘(entanglement) 예고**: 슬라이드는 "특정 상황에서는(추후 논의), 이 큐비트들 중 하나를 측정하는 것이 배선도, 전파도, 시간도 없이 다른 컴퓨터/방/국가에 있는 큐비트를 변화시킬 수 있다"고 언급한다. **주의**: 이 문장만 읽으면 "즉각적인 정보 전송(빛보다 빠른 통신)"으로 오해하기 쉽다 — 아래 Common misconceptions에서 바로 정정한다.

**Worked example**: 큐비트가 $\alpha=1/2,\ \beta=\sqrt3/2$인 상태 $|\psi\rangle=\alpha|0\rangle+\beta|1\rangle$라면,

$$P(0) = |\alpha|^2 = (1/2)^2 = 1/4 = 25\%, \qquad P(1) = |\beta|^2 = (\sqrt3/2)^2 = 3/4 = 75\%$$

## Common misconceptions

- **"양자컴퓨터는 모든 문제를 지수적으로 빠르게 푼다"** — 오개념. 알려진 speedup은 특정 구조를 가진 문제(인수분해, 특정 시뮬레이션 등)에 국한된다. 양자컴퓨터가 NP-hard 문제의 worst-case를 풀 수 있다는 것조차 믿어지지 않으며(2.3절), "고전 시뮬레이션이 지수적으로 어렵다"는 것 자체도 아직 증명 안 된 추측이다.
- **"큐비트는 그냥 상태가 더 많은 비트다(0,1,2,3...)"** — 오개념. 큐비트는 이산적 다치 논리가 아니라 연속적인 복소 진폭들의 중첩이며, 측정 시 확률적으로 계산기저 중 하나로 붕괴한다(3.2절).
- **"양자컴퓨터가 고전 컴퓨터를 완전히 대체한다"** — 오개념. 대부분의 처리 요구는 여전히 고전 비트 기반 로직이 더 효율적으로 처리한다(2.15절). 양자컴퓨터는 고전 컴퓨터가 지휘하는 하이브리드 구조로 동작한다(2.9절: 회로 구성은 고전 컴퓨터가 지휘).
- **"얽힘을 이용하면 빛보다 빠른 통신이 가능하다"** — 오개념. 3.2절의 "배선도 전파도 시간도 없이 변화시킨다"는 표현은 오해를 부르기 쉽다. 실제로는 각 측정 결과 자체가 무작위(Born rule)이고, 측정하는 쪽이 그 결과를 원하는 대로 조작할 방법이 없으므로, 이 상관관계만으로는 정보를 전송할 수 없다(no-signaling theorem) — 다음 챕터에서 정식으로 다룰 주제.
- **"이중슬릿에서 간섭이 사라지는 건 측정 장치가 광자를 물리적으로 건드려서(교란)다"** — 오개념. 원인은 (아무리 정교해도) 측정 자체가 "어느 슬릿을 지나갔는가"라는 정보를 환경으로 새어나가게(decoherence) 만든다는 것이지, 고전적인 의미의 물리적 충돌·교란이 아니다(3.1절).
- **"필터(측정)를 하나 더 추가하면 통과하는 빛의 양은 늘거나 그대로다, 절대 줄지 않는다"** — 오개념. 편광판 퍼즐(3.1절)은 정반대를 보여준다: 필터 B를 추가하면 (없을 때 0이던) 통과율이 오히려 $1/8$로 **늘어난다** — 각 측정이 그 측정 기저로 상태를 다시 투영(projection)하기 때문.

## Glossary

- **Quantum computing (paradigm)**: a computing model that exploits quantum-mechanical properties (superposition, entanglement, interference) of matter to perform computation.
- **Superposition**: a quantum state expressed as a linear combination of basis states with complex-valued amplitudes.
- **Entanglement**: a correlation between qubits such that the joint state cannot be factored into independent per-qubit states.
- **Interference (quantum)**: constructive/destructive combination of probability amplitudes, arising from cross terms in $|\alpha_1+\alpha_2|^2$.
- **Decoherence**: the loss of quantum superposition due to information about the system's state leaking into the environment.
- **NISQ (Noisy Intermediate-Scale Quantum)**: the current era of 50–100-qubit quantum devices that are not protected by quantum error correction.
- **Quantum error correction (QEC)**: encoding one logical qubit into many physical qubits so errors can be detected/corrected without collapsing the encoded information.
- **qLDPC code**: a class of quantum low-density parity-check codes studied as a lower-overhead alternative for QEC.
- **Fault tolerance**: the property of a quantum computation that remains correct despite a bounded rate of physical errors, typically achieved via QEC.
- **Quantum Turing machine / quantum circuit / MBQC / adiabatic QC**: four computationally-equivalent models of quantum computation.
- **Unitary transformation**: a norm-preserving linear transformation; the mathematical form every quantum gate takes.
- **No-cloning theorem**: an arbitrary unknown quantum state cannot be copied exactly (previewed here as the reason quantum circuits forbid fan-out).
- **Born rule**: the postulate that the probability of a measurement outcome equals the squared modulus of its amplitude, $P=|\alpha|^2$.
- **Amplitude**: a complex number $\alpha \in \mathbb C$ assigned to each possible measurement outcome of a quantum state.
- **Wave–particle duality**: the fact that light and matter each display both wave-like and particle-like behavior depending on how they are observed.
- **Stern–Gerlach experiment**: an experiment demonstrating that a measured quantity (e.g., spin) takes discrete ("quantized") values.
- **Double-slit experiment**: an experiment demonstrating single-particle self-interference and the probabilistic nature of quantum mechanics.
- **Qubit**: the quantum analogue of a bit, a two-state quantum system whose general state is $\alpha|0\rangle+\beta|1\rangle$.

## References

- R. P. Feynman, "Simulating Physics with Computers," *International Journal of Theoretical Physics* 21 (1982): 467–488 (1981년 MIT 강연을 논문화).
- R. P. Feynman, "There's Plenty of Room at the Bottom" (1959년 Caltech 강연).
- Gabriel Popkin, "Scientists are close to building a quantum computer that can beat a conventional one," *Science*, Dec. 2016. [Gab16]
- Rainer Blatt and David Wineland, "Entangled states of trapped atomic ions," *Nature* 453.7198 (2008): 1008–1015. [BW08]
- Michael A. Nielsen and Isaac L. Chuang, *Quantum Computation and Quantum Information: 10th Anniversary Edition*, Cambridge University Press, 2011. [NC11]
- John Preskill, "Quantum Computing in the NISQ era and beyond," *Quantum* 2 (2018): 79, doi:10.22331/q-2018-08-06-79. [Pre18]
- Jochen Rau, "Why quantum technology is hot," YouTube, Feb. 2021. [Rau21]
- Walter Riess (IBM Research Zürich), "Scalable Quantum Computing with Superconducting Qubits," Sept. 2017. [Wal17]
- Eleanor Rieffel and Wolfgang Polak, "An introduction to quantum computing for non-physicists," *ACM Comput. Surv.* 32.3 (2000): 300–335. [RP00]
- Eleanor Rieffel and Wolfgang Polak, *Quantum Computing: A Gentle Introduction*, MIT Press, 2011. [RP11]
- J. von Neumann, "Various techniques used in connection with random digits," in *The Monte Carlo Method*, National Bureau of Standards, 1951, pp. 36–38. [von51]
- 강의 슬라이드: `ch01_qcp_v2.pdf`, Bernd Burgstaller, CAS3140-01 Quantum Computer Programming, Fall 2026, Yonsei University (74장).
