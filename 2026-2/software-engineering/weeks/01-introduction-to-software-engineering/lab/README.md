# Lab — 두 건의 사고를 코드로 재현하기

두 실습 모두 **Python 표준 라이브러리만** 사용한다. 가상환경·의존성 설치 불필요, 난수 없음 (완전 결정적):

```bash
python3 ariane501.py
python3 knight_capital.py
```

선택 과제 (C 컴파일러 필요):

```bash
cc -O2 -o ariane_overflow ariane_overflow.c && ./ariane_overflow
```

두 시뮬레이션 모두 **사고의 인과 구조** (Lions report / SEC order 에 기록된) 를 재현하는 것이 목표이고, 물리 상수·손실 단가는 실제 수치가 아니라 사고의 시각·규모가 재현되도록 조정한 교육용 값이다 (각 스크립트 docstring 에 명시).

---

## Lab 1 — `ariane501.py`: 64-bit float → 16-bit int 변환 사고

**목표**: (1) 같은 코드가 환경 (궤적) 만 바뀌어 실패함을 재현하고, (2) 동일 소프트웨어 이중화가 common-mode failure 에 무력함을 보이고, (3) out-of-range 값에 대한 5가지 정책 (Ada 예외 / C wraparound / saturation / range-check fallback / dead code 제거) 의 실패 모드를 비교한다.

**구현 포인트**

- Ada 의 checked conversion 은 `OperandError` 예외로, C 의 (사실상) unchecked 변환은 two's-complement wraparound 로 모델링. 실제 SRI 의 예외 정책 "진단 기록 후 프로세서 셧다운"을 그대로 구현 — 예외 자체가 아니라 **예외 정책**이 임무를 죽였음을 보이기 위해.
- 궤적 상수는 실제 사고처럼 **t≈36.7s 에 BH 가 32767 을 넘도록** 조정한 교육용 값 (실제 텔레메트리 아님). t 는 Lions report 의 시각 표기처럼 **H0 기준** (H0+36.7s ≈ 리프트오프 후 30초) 으로 읽는다.
- alignment function 은 flight mode 후 ~50초까지 동작 (Ariane 4 레거시 요구사항의 재현).

**실제 실행 출력**

```
=== Part 1: same code, two rockets ===
  Ariane 4: OK  (max BH =   6600, fits int16)
  Ariane 5: OPERAND ERROR at t=36.7s (BH = 32769 > 32767) -> PROCESSOR SHUTDOWN
  -> the code did not change; the ENVIRONMENT did. 'Proven on Ariane 4' was a claim about Ariane 4's trajectory, not the code.

=== Part 2: redundancy vs common-mode failure (Ariane 5) ===
  [identical software (actual design)]
    SRI1 (backup) shut down at t=36.7s
    SRI2 (active) shut down at t=36.7s
    no surviving channel within one cycle -> OBC reads the diagnostic bit pattern as flight data -> loss of mission
  [diverse conversion policy]
    SRI1 (backup) shut down at t=36.7s
    surviving channel(s): SRI2 (active) -> OBC still has attitude data, mission continues
  -> two copies of the same design fault fail on the same input;
     redundancy only protects against INDEPENDENT failures.

=== Part 3: defense comparison on the Ariane 5 trajectory ===
  policy                 first anomaly  detected  outcome
  ------------------------------------------------------------------------
  unprotected-ada        t=36.7s        yes       PROCESSOR SHUTDOWN
  wraparound-c           t=36.7s        NO        GARBAGE DATA (undetected) (BH reported as -32767)
  saturate               t=36.7s        yes       degraded, flagged, kept flying
  range-check-fallback   t=36.7s        yes       degraded, flagged, kept flying
  disable-after-liftoff  -              NO        nominal
```

**읽는 법**

- **Part 1**: 코드는 한 줄도 안 바뀌었다. "Ariane 4 에서 검증됨"은 코드에 대한 진술이 아니라 **Ariane 4 궤적이라는 환경 가정에 대한 진술**이었고, 그 가정은 spec 에 명시되지 않은 채 이식됐다.
- **Part 2**: 동일 소프트웨어 두 채널은 같은 입력에 같은 사이클에서 함께 죽는다 — 이중화가 design fault 앞에서 0 의 가치. 변환 정책만 다르게 한 diverse 채널은 살아남는다 (N-version programming 의 기본 아이디어 — 단, 비용과 "다양성도 상관될 수 있다"는 한계는 별론).
- **Part 3** 이 이 lab 의 본론이다:
  - `unprotected-ada` — **시끄럽게** 실패하지만, 셧다운 정책이 "무용한 계산의 overflow"를 "기체 상실"로 증폭.
  - `wraparound-c` — crash 없음, 그러나 자세 데이터가 쓰레기인데 **아무 신호도 없다**. Silent wrong data 는 loud failure 보다 나쁘다.
  - `saturate` / `range-check-fallback` — 값을 유계로 막고 **명시적 flag** 를 올린 채 비행 지속. 실제 Lions 보고서의 권고 방향 (예외 시 최선 추정값으로 지속하는 것도 설계 선택지).
  - `disable-after-liftoff` — 진짜 정답. 이 함수는 Ariane 5 에서 liftoff 후 **아무 목적이 없었다**. 실행되지 않는 코드는 실패할 수 없다 — 죽은 요구사항을 제거하는 것이 최고의 방어다 (Knight 의 dead code 교훈과 동일).

**C 보충 (`ariane_overflow.c`)**: C 에서 범위 밖 float→int16 변환은 wraparound 조차 보장되지 않는 **undefined behavior** (C11 6.3.1.4) 다. 실측 (arm64 Apple clang 17): **같은 컴파일러·같은 CPU 에서도** `-O0` 은 `-32767` (런타임 `fcvtzs` 변환 후 16-bit truncation), `-O2` 는 `-32768` (컴파일러가 out-of-range 변환을 poison 으로 접어 printf 인자 자체를 생략 — 찍힌 값은 스택 잔여물이다) 을 출력한다. 결과가 CPU·컴파일러·**최적화 수준** 어느 것에든 의존할 수 있다는 비결정성 자체가 교훈이다. 유일한 이식 가능한 방법은 명시적 range check. 아래는 문서화된 `cc -O2` 빌드의 출력:

```
BH (64-bit double)        : 32769.7
int16 range               : [-32768, 32767]
direct cast  (UB in C)    : -32768   <- silent garbage, no error signal
checked conversion        : REJECTED - out of range, handle explicitly (ok=0)
```

---

## Lab 2 — `knight_capital.py`: flag 재사용 + 부분 배포의 상태 머신

**목표**: (1) "코드는 옳은데 배포가 틀린" 상태 — 8대 중 1대만 구버전 — 가 어떻게 폭주를 만드는지 상태 머신으로 재현하고, (2) 검증 없는 롤백이 사태를 8배로 키우는 것을 보고, (3) 세 가지 방어 (배포 검증 / dead code 제거 / kill switch) 의 효과와 성격 차이를 비교한다.

**구현 포인트**

- Parent order 상태 머신: `NEW → WORKING → FILLED` (신코드: 체결 추적, 10 child 후 완료) vs `NEW → RUNAWAY` (구코드: Power Peg 가 체결 카운터를 못 보므로 종료 조건이 영원히 거짓 — 분당 1,000 child 발사) vs `NEW → REJECTED` (dead code 제거 시: 미지의 flag 는 hard reject).
- 라우팅은 round-robin — 8대 중 1대가 구버전이면 **정확히 1/8 의 주문**이 폭주로 변한다. 코드가 아니라 fleet 의 버전 상태가 리스크의 소재임을 보이는 장치.
- 실제 사건의 "08:01 에 'Power Peg disabled' 참조 이메일 97통 발송, 무시됨"도 재현 (legacy 서버가 있으면 pre-open 경고 발생).
- 손실 단가 ($115/child) 는 실제 사고의 자릿수 (~$460M, 체결 400만+) 에 맞춘 교육용 값.

**실제 실행 출력** (요약 테이블)

```
scenario              filled  runaway  rejected  child orders            loss  note
----------------------------------------------------------------------------------------------------
full-deploy              225        0         0         2,250              $0  correct deployment: new code on all 8 servers
incident                 197       28         0       600,970     $68,885,000  actual bug: 1 of 8 servers still runs legacy code [97 pre-open warning e-mails ignored]
incident+rollback         88      137         0     1,910,880    $219,650,000  + minute 20: new code rolled back off the 7 good servers [97 pre-open warning e-mails ignored]
deploy-verification        0        0         0             0              $0  version mismatch across servers -> deployment aborted before open, zero orders at risk
dead-code-removed        197        0        28         1,970              $0  defense 2: Power Peg deleted; unknown flag -> reject
kill-switch               40        5         0        19,400      $2,185,000  defense 3: automated $2M loss limit halts trading (halted at minute 8) [97 pre-open warning e-mails ignored]
```

타임라인 (`incident+rollback`) 은 minute 20 의 롤백에서 runaway 생성률이 8배로 꺾이는 것을 보여준다:

```
minute  runaway parents  child orders       cum. loss
    15               10        68,700      $7,820,000
    19               12       110,880     $12,650,000
    20               17       122,880     $14,030,000  <- rollback: ALL 8 servers now defective
    25               42       257,880     $29,555,000
    44              137     1,910,880    $219,650,000
```

**읽는 법**

- `full-deploy` vs `incident`: **같은 코드, 같은 주문 흐름** — 다른 것은 배포 상태뿐이다. 신코드에는 버그가 없다. 사고의 "버그"는 코드가 아니라 **fleet 이 혼합 버전이라는 상태 + 그 상태에서 flag 의 의미가 서버마다 다르다는 사실**이다.
- `incident+rollback`: 원인을 모른 채 "릴리스를 되돌리자"는 직관이 유일하게 옳던 7대의 해석을 제거해 폭주를 8배로 키운다. **롤백도 배포다** — 리허설·검증 없는 롤백은 복구가 아니라 재배포.
- 세 방어의 성격 차이에 주목:
  - `deploy-verification` (**예방**, 가장 저렴): 위험 상태 (버전 skew) 자체를 개장 전에 소거. DevOps 의 자동화된 배포 파이프라인이 사는 것이 정확히 이것 (→ W3).
  - `dead-code-removed` (**설계적 소거**): 위험한 상태로 가는 경로 자체가 없다. 비용은 소수의 reject 된 주문 — 유계·가시적·복구 가능한 실패로의 전환.
  - `kill-switch` (**피해 유계화**): fault 를 막지 못하지만 손실 상한을 계약한다 ($460M → ~$2M). SEC 가 Rule 15c3-5 로 요구한 것이 바로 이 통제였다.
- 방어는 택일이 아니라 **계층** (defense in depth — Therac-25 의 교훈과 동일 구조) 이다: 예방이 뚫려도 소거가, 소거가 뚫려도 유계화가 받친다.

---

## 확장 과제 (선택)

1. `ariane501.py` 의 diverse redundancy 에서, 두 채널이 **같은 잘못된 spec** (예: 둘 다 wraparound) 을 공유하면 어떻게 되는지 실험하라 — diversity 가 구현 수준이 아니라 spec 수준의 결함에는 왜 무력한가.
2. `knight_capital.py` 에 canary deployment 시나리오를 추가하라: 신코드를 1대에만 먼저 배포하고 N분 관찰 후 전체 배포. 이 사고에서는 canary 가 잡았을까? (힌트: 결함은 신코드가 아니라 **배포되지 않은 서버**에 있다 — canary 가 검출하는 것과 못 하는 것을 구분하라.)
3. kill switch 의 loss limit 을 $100k / $1M / $10M 로 바꿔가며 "false trip (정상 변동에 오작동) 리스크 vs 손실 상한" 트레이드오프를 논하라.
