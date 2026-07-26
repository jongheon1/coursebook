# coursebook

수강 과목마다 전용 교과서를 만든다. 방학에 강의계획서만으로 전 주차를 한 바퀴 도는 예습 교재를 생성하고, 학기 중에는 강의 녹취·강의안을 소화해 복습 자료로 재정리한다. 전부 Claude Code 로 만든다.

## Courses

### 2026-2

| 과목 | 코드 | 한 줄 | 교재 |
|---|---|---|---|
| [분산학습및추론](2026-2/distributed-learning-and-inference/) | CAS4401 | Distributed/federated training & efficient inference — parallelism, communication, non-IID, inference optimization | [roadmap](2026-2/distributed-learning-and-inference/00-roadmap.md) |
| [시스템프로그래밍](2026-2/system-programming/) | CAS3107 | Linux kernel programming — process, interrupt, synchronization, memory management, file system | [roadmap](2026-2/system-programming/00-roadmap.md) |
| [소프트웨어공학](2026-2/software-engineering/) | CAS3106 | SDLC, large-scale system design, OOP/SOLID/design patterns, testing (Sommerville 10e) | [roadmap](2026-2/software-engineering/00-roadmap.md) |

## 구조

과목마다:

- `syllabus.md` — 계획서 요약 (주차표·평가·선수과목)
- `00-roadmap.md` — 주차→토픽→정본 소스 매핑. 깊이 벤치마크 (탑티어 CS 강의·원 논문·공식 문서)
- `weeks/NN-topic/` — 주차별 챕터: 본문(`README.md`) + 시험 스타일 연습문제(`exercises.md`) + active recall 퀴즈(`quiz.md`, Anki TSV 포함) + 실행 가능한 실습(`lab/`)
- `semester/week-NN/` — 학기 중: 강의 노트(`notes.md`) + 예습 교재와의 delta(`delta.md`, 시험 신호)

## 방법론

검증된 학습 방법의 조합:

1. **Source-grounded 교재 생성** — 모든 내용은 지정 교재·원 논문·공식 문서·실제 소스 코드에 근거, 출처 명시
2. **Active recall + spaced repetition** — 챕터마다 퀴즈 은행, Anki 임포트 지원
3. **Directness** — 매주 손으로 돌려보는 lab
4. **Lecture-delta 복습** — 학기 중 실제 강의와 예습 교재의 차이를 추출. "교수가 강조했는데 교재에 없던 것" = 시험 신호

## Skills

| 스킬 | 용도 |
|---|---|
| `/build-week <course> <week>` | 주차 챕터 풀 생성 (방학 예습) |
| `/ingest-lecture <course> <week>` | 녹음·강의안 → 강의 노트 + delta (학기 중 복습) |
| `/quiz <course> [week]` | active recall 구술 세션 |
| `/exam-prep <course> <midterm\|final>` | 시험 대비 통합 정리 (delta 가중) |
