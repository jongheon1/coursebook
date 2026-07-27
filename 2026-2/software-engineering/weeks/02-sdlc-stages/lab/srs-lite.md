# SRS-lite — Scooter Fare Calculator

작은 기능 하나를 SRS 형식으로 고정한다. 각 요구는 ID 를 갖고 (traceability), verifiable 하게 쓴다. 모든 테스트는 이 문서의 ID 를 주석으로 참조한다.

## v1.0 (baseline)

### Scope

공유 킥보드 1회 주행의 요금 (KRW, 정수) 을 계산하고 영수증 텍스트를 생성한다. 입력: 주행 시간 (초), 주행 시작 시각의 시 (0–23).

### Functional requirements

- **FR-1 (billing minutes)**: 청구 분은 `ceil(duration_seconds / 60)` 로 계산한다. (61초 → 2분)
- **FR-2 (base fare)**: 요금 = unlock fee **1,000** + 청구 분 × 분당 요금 **180**.
- **FR-3 (night surcharge)**: 시작 시각이 00시 이상 06시 미만이면 **요금 총액에 20% 할증**을 더한다.
- **FR-4 (rounding)**: 최종 요금은 **10원 단위 내림** (floor to 10).
- **FR-5 (validation)**: `duration_seconds <= 0` 또는 `start_hour ∉ [0, 23]` 이면 `ValueError`.
- **FR-6 (receipt)**: 영수증은 다음 줄들로 구성된 텍스트다 — 항목 줄들 (`<label>` 과 `<amount>`), 구분선, `TOTAL <final fare>` 줄. 항목: `unlock`, `ride <n> min`, 할증 시 `night +20%`. 항목 줄의 금액 합계에 FR-4 를 적용한 것이 TOTAL 과 일치해야 한다.

### Non-functional requirements (발췌)

- **NFR-1 (portability/testability)**: 구현은 python3 표준 라이브러리만 사용한다. 검증: import 검사.
- **NFR-2 (determinism)**: 같은 입력에 대해 항상 같은 출력 (시계·난수 사용 금지). 검증: 반복 실행 테스트.

## Change Request CR-1 → v2.0

운영 6개월 후 멤버십 도입 결정 + 할증 규칙에 대한 분쟁 (validation 단계에서 못 잡은 모호성) 정정.

- **FR-7 (membership, 신규)**: 요청에 `membership ∈ {NONE, BASIC, PLUS}` 가 추가된다 (기본 NONE).
  - `BASIC`: **시간 요금 (ride 항목) 10% 할인**.
  - `PLUS`: **unlock fee 면제 + 시간 요금 30% 할인**.
  - 할인 금액은 항목별로 정수 내림 계산. 영수증에 할인 항목 (`basic -10%` / `plus -30%`, 음수 금액) 을 표시한다.
- **FR-3′ (night surcharge, 변경)**: 할증의 적용 대상을 "요금 총액" 에서 **"할인 적용 후 시간 요금"** 으로 정정한다. unlock fee 에는 할증이 붙지 않는다. (원 조항의 "요금 총액" 이 stakeholder 간 다르게 해석됨 — requirements validation 실패의 전형)
- FR-1, FR-2, FR-4, FR-5, FR-6, NFR 은 불변.

### CR-1 의 성격

- FR-7 은 **perfective** 변경 (새 요구), FR-3′ 은 requirements defect 의 **corrective** 변경이다.
- pricing 규칙 (금액, 할인, 할증 대상) 이라는 **하나의 design decision 군**만 변한다. Parnas 기준으로 설계했다면 파급은 pricing 을 소유한 module 에 갇혀야 한다.

## Acceptance examples (양 버전 공통 형식)

| duration_s | start_hour | membership | v1 total | v2 total |
|---|---|---|---|---|
| 600 (10 min) | 14 | NONE | 1000+1800=2800 | 2800 |
| 600 | 3 | NONE | floor10(2800×1.2)=3360 | 1000+1800+360=3160 |
| 610 (11 min) | 14 | BASIC | — | 1000+(1980−198)=2782 → floor10=2780 |
| 610 | 3 | PLUS | — | 0+(1980−594)+277=1663 → floor10=1660 |

(v2 night: surcharge = floor(discounted_ride × 0.2); PLUS 예: ride=11×180=1980, 할인 594, 할인 후 1386, 할증 277, 합 1663 → 1660.)
