# Lab — 한 기능의 SDLC 미니 사이클

킥보드 요금 계산기 하나로 SDLC 를 축소해서 한 바퀴 돈다:

```
SRS-lite 작성 → 테스트 먼저 작성 (spec 기반) → 두 가지 설계로 구현
→ change request (CR-1) 수용 → 변경 비용을 diff 로 실측
```

챕터 본문의 주장 — "coupling 이 낮고 pricing 결정이 한 module 에 숨겨진 설계는 변경이 국소화된다 (Parnas)" — 를 **측정으로** 확인하는 것이 목표다.

## 구조

```
lab/
├── srs-lite.md            # 요구사항 v1.0 + Change Request CR-1 (→ v2.0)
├── v1/                    # v1.0 구현 2종
│   ├── fare_tangled.py    #   tangled: 모든 지식이 한 덩어리 + 지식 중복
│   └── fare_modular/      #   modular: pricing 결정을 policy.py 에 은닉
│       ├── model.py       #     Ride + validation (FR-5)
│       ├── policy.py      #     pricing 의 'secret' 전부 (FR-1..4)
│       ├── calculator.py  #     합산만 — 가격을 모름
│       ├── receipt.py     #     렌더링만 — 가격 규칙을 모름 (FR-6)
│       └── __init__.py    #     facade: quote(), total_fare()
├── v2/                    # CR-1 반영 후 (v1 을 복사해 최소 수정)
├── tests/
│   ├── test_v1.py         # v1.0 spec 테스트 — 두 구현 모두에 실행
│   └── test_v2.py         # v2.0 spec 테스트 — 두 구현 모두에 실행
└── measure_change_cost.py # v1→v2 diff 를 파일별 집계
```

의존성: **python3 표준 라이브러리만** (NFR-1). 별도 설치 없음.

## 실행법

`lab/` 디렉토리에서:

```bash
python3 tests/test_v1.py        # v1 spec: 8 tests, 두 구현 모두 OK
python3 tests/test_v2.py        # v2 spec: 8 tests, 두 구현 모두 OK
python3 measure_change_cost.py  # CR-1 의 변경 비용 실측
```

## 순서대로 할 것

1. **`srs-lite.md` 를 읽는다.** 각 요구가 ID (FR-n) 를 갖고 verifiable 하게 쓰인 것, acceptance example 이 붙은 것을 확인 (챕터 §1.2, §1.5).
2. **테스트를 먼저 읽는다** (`tests/test_v1.py`). 모든 테스트가 구현이 아니라 **SRS 의 ID 를** 참조한다 — requirements validation 기법 중 test-case generation 의 축소판.
3. **두 구현을 비교하며 읽는다.**
   - `fare_tangled.py`: 상수가 계산과 ops report 용 `total_fare()` 두 곳에 존재 (지식 중복), validation·계산·할증·포맷팅이 한 함수에 교차 (procedural cohesion), 할증이 총액 계산 중간에 inline.
   - `fare_modular/`: pricing 지식은 `policy.py` 에만 있다. `calculator` 는 항목 합산만, `receipt` 는 `(label, amount)` 리스트 렌더링만 안다 — Parnas 의 "module = design decision 을 숨기는 단위".
4. **CR-1 을 읽고** (`srs-lite.md` 하단) v1 → v2 diff 를 눈으로 따라간다: `diff -ru v1 v2`.
5. **측정한다**: `python3 measure_change_cost.py`.

## 실측 결과 (이 레포의 구현 기준)

```
== tangled ==
  fare_tangled.py              +32  -10  hunks 10 <- pricing owner
  files touched: 1, changed lines: 42, edit locations (hunks): 10, changed lines outside pricing owner: 0

== modular ==
  fare_modular/__init__.py     +4   -4   hunks 4
  fare_modular/calculator.py   +0   -0   hunks 0
  fare_modular/model.py        +5   -0   hunks 3
  fare_modular/policy.py       +14  -8   hunks 3 <- pricing owner
  fare_modular/receipt.py      +0   -0   hunks 0
  files touched: 3, changed lines: 35, edit locations (hunks): 10, changed lines outside pricing owner: 13

== verdict ==
tangled : 42 lines / 10 edit locations in 1 file(s); the whole module IS the pricing owner — every edit sits next to validation and formatting code, and the surcharge rule had to be changed in TWO places (quote and total_fare)
modular : 35 lines / 10 edit locations in 3 file(s); 22 lines in policy.py, 13 interface ripple (model/facade); calculator.py and receipt.py provably untouched
```

주: tangled 의 "outside pricing owner: 0" 은 좋다는 뜻이 아니다 — 파일이 하나뿐이라 **모든 것이 pricing owner** 로 집계될 뿐이다. modular 의 13줄이 무엇인지는 아래 3번 참고.

### 숫자를 정직하게 읽기

**총 변경 줄 수는 42 vs 35 로 큰 차이가 아니다.** 이 크기의 장난감 문제에서 총량 차이는 원래 작다 — 순진하게 "줄 수" 만 보면 결론을 놓친다. 진짜 차이는 세 가지다:

1. **지식 중복의 세금.** tangled 에서는 FR-3′ (할증 규칙 변경) 을 `quote()` 와 `total_fare()` **두 곳에서** 고쳐야 했다. 한 곳을 잊으면? 실험해 봤다 — `total_fare()` 를 v1 상태로 되돌리면 `test_ops_report_agrees_with_quote` 가 즉시 실패한다 (`3570 != 3370`). 이 consistency 테스트가 없었다면 ops report 는 **조용히 틀린 값을 내는** 채로 배포된다 — 챕터 §3.1 의 drift 가 정확히 이렇게 시작된다.
2. **변경의 blast zone.** tangled 의 10개 hunk 는 validation·포맷팅 코드와 **한 함수 안에서 교차**한다 — 모든 편집이 영수증 포맷을 깨뜨릴 수 있는 위치에서 일어나고, 리뷰 범위는 module 전체다. modular 의 변경 중 policy.py 밖의 13줄은 전부 **interface plumbing** (새 필드 + facade 인자 전달) 이고, `calculator.py` 와 `receipt.py` 는 **diff 0 줄** — 가격 규칙을 모르게 설계됐으므로 가격 규칙 변경에 재검토조차 필요 없다는 것이 기계적으로 증명된다.
3. **interface 변경은 좋은 설계도 지불한다.** modular 의 13줄 ripple 은 CR-1 이 순수한 규칙 변경이 아니라 **입력 (membership) 의 추가** — 즉 interface 변경 — 를 포함하기 때문이다. Parnas 의 은닉이 공짜로 만들어 주는 것은 "숨긴 결정" 의 변경이지 인터페이스의 변경이 아니다. FR-3′ 만 왔다면 (할증 대상 정정) modular 의 diff 는 policy.py 몇 줄이 전부였을 것이다.

## 확장 실험 (선택)

- **Stale duplicate 재현**: `v2/fare_tangled.py` 의 `total_fare()` 를 v1 버전으로 되돌리고 `python3 tests/test_v2.py` → 어떤 테스트가 어떻게 실패하는지 확인. 테스트가 못 잡는 조합 (day ride, NONE) 이 존재함도 확인해 볼 것 — coverage 의 한계 (W14 예고).
- **다음 change request 를 스스로 설계**: "주말 요금제" (FR-8) 를 정의하고 양쪽에 적용, 측정을 반복. pricing 외의 결정 (영수증 다국어화) 을 바꾸면 어느 설계가 유리한지도 실험 — 은닉의 이득은 **어떤 변경이 오는가에 대한 예측**에 걸려 있다 (챕터 §2.3).
- **coupling 분류 연습**: `fare_tangled.py` 에서 content/common/control/stamp/data coupling 과 cohesion 등급의 실물 예를 찾아 라벨링.

## 검증 환경

macOS, python3 (3.9+ 면 충분; f-string·dataclass·difflib 만 사용). 전체 테스트 16개 + 측정 스크립트 실행 확인 완료.
