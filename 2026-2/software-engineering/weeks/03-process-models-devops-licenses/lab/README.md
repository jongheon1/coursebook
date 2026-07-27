# Week 3 Lab — Mini CI Pipeline & License Audit

챕터의 두 축을 손으로 만져본다: (1) deployment pipeline 의 **단계별 실패 의미** (§8.3) 를 make 기반 미니 CI 로, (2) copyleft 의 **전염 trigger 판정** (§10) 을 의존성 라이선스 감사 스크립트로.

요구사항: `python3` (3.10+), `make`. 외부 패키지 없음 (표준 라이브러리만).

전체 자동 검증 (두 랩의 성공 경로 + **의도된 실패 경로**를 전부 assert):

```bash
cd lab
make verify
# ...
# ALL LAB ASSERTIONS PASSED
```

---

## Lab 1 — `ci-pipeline/`: make 로 만드는 3-stage CI

### 구조

```
ci-pipeline/
├── Makefile            # 파이프라인 정의: lint → unit test → build
├── src/semver.py       # 대상 코드: SemVer 2.0.0 파서/비교기
├── tests/test_semver.py
├── tools/lint.py       # 의존성 없는 미니 린터 (commit-stage 검사)
└── faults/             # 주입용 결함 변형 2종
    ├── semver_buggy.py # 논리 결함 (spec 11.4.1 위반) — stage 2 가 잡는다
    └── semver_lint.py  # 스타일 결함 (debug 출력 등) — stage 1 이 잡는다
```

설계 포인트: **make 의 dependency graph 가 곧 파이프라인이다.** 각 stage 는 성공 시 `.ci/<stage>.ok` stamp 를 남기고, 다음 stage 는 이전 stamp 에 의존한다. 소스가 안 바뀌면 green stage 는 재실행되지 않는다 — 실제 CI 의 stage cache 와 같은 원리. stage 순서는 "싸고 빠른 검사 먼저" (commit stage ~10분 원칙): lint 가 깨지면 테스트는 돌지도 않는다.

### 실행

```bash
cd ci-pipeline
make ci            # green: 3 stage 통과, dist/app.tar.gz + SHA256SUMS 생성
make ci            # 재실행: 전부 캐시 — 아무 stage 도 다시 돌지 않음

make break-test    # 논리 결함 주입 (prerelease 숫자 식별자를 문자열 비교)
make ci            # stage 1 green → stage 2 FAILED: "unit logic defect"
                   #   → lint 는 이 부류를 구조적으로 못 잡는다

make break-lint    # 스타일 결함 주입 (debug 출력, 긴 줄, trailing whitespace)
make ci            # stage 1 FAILED: "code-local convention defect"
                   #   → 기능은 멀쩡하다 (테스트는 통과했을 코드) — stage 별로 잡는 결함 부류가 다르다

make fix           # 원본 복원
make ci            # 다시 green
```

### 예상 출력 (green 경로)

```
[stage 1/3] lint
[stage 1/3] OK
[stage 2/3] unit tests
Ran 14 tests ... OK
[stage 2/3] OK
[stage 3/3] build
[stage 3/3] OK — artifact + checksum written
CI GREEN — release candidate: dist/app.tar.gz
```

### 챕터 연결

- 실패 메시지가 곧 §8.3 표의 "실패의 의미"다: stage 1 = 코드 규약/문법 (커밋한 사람이 즉시 수정), stage 2 = 단위 논리 (self-testing build 만 잡는다), stage 3 = artifact 생성. 이후 stage (acceptance/staging) 는 이 **동일한 artifact** 를 재사용해야 한다 (12-factor V).
- `faults/semver_buggy.py` 는 lint 를 통과하고 테스트에 죽고, `faults/semver_lint.py` 는 테스트를 통과할 코드지만 lint 에 죽는다 — 두 stage 는 대체 관계가 아니라 서로 다른 결함 부류의 필터다.

---

## Lab 2 — `license-audit/`: 의존성 라이선스 감사

### 구조

```
license-audit/
├── audit.py                    # SPDX expression 분류 + copyleft 판정 엔진
├── test_audit.py               # 분류/판정 로직 unit tests (18개)
├── licenses.json               # 패키지 → SPDX expression DB
├── requirements-sample.txt     # 감사 대상 (챕터 Worked example 3 과 동일 구성)
├── requirements-unknown.txt    # 라이선스 미상 의존성
└── scenario-*.json             # 배포 시나리오 4종 (internal/saas/saas-modified/binary)
```

판정 모델 (단순화한 교육용 — 법률 자문 아님):

- copyleft trigger = **conveying** (`distribution: "binary"`). internal/saas 는 conveying 이 아니다.
- AGPL §13: **수정된** 버전의 네트워크 서비스가 추가 trigger. 무수정 + 별도 프로세스(arm's length)면 미발동. in-process 결합 + SaaS 는 보수적 (FSF) 해석으로 VIOLATION 처리.
- LGPL: dynamic linking + relink 보장이면 proprietary 유지 가능, static 은 object 파일 제공 조건 (WARN).
- `X WITH Classpath-exception-2.0` 은 linking 목적상 weak 으로 강등 (예외의 존재 이유).
- SPDX expression: `OR` = 수취인 선택 → 가장 약한 branch, `AND` = 전부 적용 → 가장 강한 part, `WITH` 최우선 결합. 괄호 미지원.

### 실행

```bash
cd license-audit
make test              # 판정 로직 unit tests
make audit-internal    # exit 0 — conveying 없음, 전부 OK
make audit-saas        # exit 0 — GPL import 는 latent WARN, AGPL 무수정 process 는 OK
make audit-saas-mod    # exit 1 — AGPL 을 패치했다: §13 발동, VIOLATION
make audit-binary      # exit 1 — GPL import 를 conveying: 결합 저작물 VIOLATION
make audit-unknown     # exit 1 — 라이선스 미상은 무조건 차단
make demo              # 위 다섯을 순서대로 (예상 실패 포함)
```

### 예상 출력 (binary 시나리오 요약부)

```
chartkit       GPL-3.0-only        strong-copyleft   import   VIOLATION
               -> conveying a combined work with copyleft code — release the whole work ...
pdfengine      AGPL-3.0-only       network-copyleft  process  WARN
               -> separate program at arm's length: aggregation is allowed, ...
summary: OK=5, VIOLATION=1, WARN=1
AUDIT FAILED: 1 blocking finding(s)
```

### 챕터 연결

- **같은 requirements, 같은 licenses.json 인데 시나리오 (배포 모드) 만 바꾸면 판정이 뒤집힌다** — Worked example 3 의 "배포 방식이 적법을 위반으로 만든다"를 exit code 로 확인하는 것이 이 랩의 요점이다.
- exit code 로 CI 게이트가 된다: 이 스크립트를 Lab 1 파이프라인의 stage 로 끼우면 §10.8 의 "위반은 모르는 채 쌓인 의존성에서 온다"에 대한 process 수준 방어가 완성된다.

### 확장 아이디어 (선택)

1. Lab 1 의 Makefile 에 `audit` stage 를 추가해 4-stage 파이프라인으로 (`.ci/audit.ok`).
2. `licenses.json` 을 실제 PyPI 메타데이터 (`pip show`, `importlib.metadata`) 에서 자동 생성.
3. SPDX 괄호 expression 파서 (재귀 하강) 로 `(MIT OR GPL-3.0-only) AND Apache-2.0` 지원.
