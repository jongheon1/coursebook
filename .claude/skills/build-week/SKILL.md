---
name: build-week
description: 과목의 특정 주차 교과서 챕터(본문·연습문제·퀴즈·lab)를 풀 퀄리티로 생성한다. 방학 예습 단계의 핵심 스킬.
---

# build-week

인자: `<course-slug 또는 과목명> <주차 번호 또는 토픽>` (예: `system-programming 5`, `분산 data-parallelism`)

## 절차

1. 루트 `CLAUDE.md` 와 해당 과목의 `00-roadmap.md`, `syllabus.md` 를 읽는다. 챕터의 언어·깊이·템플릿 규칙은 전부 거기에 있다.
2. roadmap 에서 해당 주차의 토픽 범위와 정본 소스 목록을 확인한다. roadmap 에 없는 주차면 먼저 roadmap 에 추가하고 사용자에게 알린다.
3. 이미 그 주차 디렉토리가 있으면 덮어쓰지 말고 무엇을 갱신할지 사용자에게 확인한다.
4. `weeks/NN-topic-slug/` 에 챕터 템플릿 4종을 생성한다: `README.md`, `exercises.md`, `quiz.md`, `lab/`.
   - 분량 가이드: 본문은 해당 주차 강의 3시간 분량을 자습으로 대체할 수 있는 밀도. 보통 README 300~600줄.
   - 인접 주차 챕터가 이미 있으면 읽고 중복 없이 연결되게 쓴다 (앞 주차 개념은 링크로 참조).
5. lab 코드는 반드시 실행해서 검증한다. Python 이면 `.venv` 만들어 의존성 설치 후 실행, 커널 모듈이면 VM 셋업 문서 기준으로 빌드까지 (VM 없으면 빌드 절차 문서화 + 검증 불가 표시).
6. 검증 결과와 함께 커밋한다: `<course-slug>: add week NN <topic>`.

## 품질 기준

- roadmap 의 벤치마크 강의(탑티어 CS) 수준. 개괄·나열 금지, 메커니즘과 트레이드오프 중심.
- 모든 사실은 References 의 소스로 뒷받침. 소스 없이 쓴 문장은 지운다.
- exercises 는 실제 시험처럼: 영어, 배점, 계산/설계 문제 포함, `<details>` 모범답안.
