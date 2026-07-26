---
name: exam-prep
description: 중간/기말 범위의 챕터·강의 노트·delta 를 통합해 시험 대비 자료를 생성한다. delta(교수 강조점)를 가중한다.
---

# exam-prep

인자: `<course-slug> <midterm|final>`

범위: midterm = 1주~중간시험 전 주차, final = 중간시험 다음 주차~기말 전 주차 (syllabus.md 의 주차표 기준).

## 절차

1. 범위 내 모든 `weeks/NN-*/README.md`, `semester/week-NN/notes.md`, `semester/week-NN/delta.md`, `semester/quiz-log.md` 를 읽는다.
2. `<course-dir>/exam/<midterm|final>.md` 생성:
   - **출제 예상 토픽 랭킹** — 근거 명시: delta 의 Emphasized(★★), 계획서 수업목표 비중, 챕터 분량, quiz-log 의 오답 빈도
   - **토픽별 압축 정리** — 챕터 재요약이 아니라 시험장에서 꺼내 쓸 형태: 정의 한 줄(영어), 핵심 유도/알고리즘 단계, 비교표, 함정
   - **예상 문제 세트** — 영어, 실제 배점 스타일, 서술·계산·설계 혼합 10~15문항, `<details>` 모범답안. 기출·과제가 `_private/` 에 있으면 스타일을 맞춘다
   - **막판 체크리스트** — 시험 전날 30분용 한 페이지
3. 사용자의 약점(quiz-log 오답)이 있는 토픽은 정리·예상문제에서 비중을 올린다.
4. 커밋: `<course-slug>: add <midterm|final> exam prep`.
