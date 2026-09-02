# 분산학습및추론 (Distributed Learning and Inference)

- **학정번호**: CAS4401-01 · 첨단컴퓨팅학부 · 3학점
- **담당**: 한동준 (컴퓨터과학과) · djh@yonsei.ac.kr · 공학관4 D720 · 오피스아워는 정해진 시간 없이 이메일로 약속(온/오프라인)
- **TA**: 최용희 (2025321337@yonsei.ac.kr) · 신성현 (sunghyun.shin@yonsei.ac.kr)
- **강의실/시간**: D408 · 수 11:00–11:50, 금 11:00–12:50
- **진행**: 영어 강의 · 절대평가 · 강의 100% · 교재 없음(분야가 emerging이라 논문 기반 자료를 슬라이드로 재구성)
- **평가**: 중간 30% / 기말 30% / 개인과제 30%(미니과제 1: 15% + 미니과제 2: 15%) / 출석 10%
  - 중간고사: 10/24(금) 11:00–12:50 · 기말고사: 12/19(금) 11:00–12:50 — ⚠️ 강의 슬라이드 표기 연도가 2025로 되어 있어 작년 템플릿 재사용 가능성 있음. **LearnUs 공지로 2026-2학기 실제 날짜 확인 필요.**
  - 출석: 지각 3회 = 결석 1회. 결석 2회(=지각 6회 포함)까지 무감점, 초과 시 결석 1회당 -1점.
  - 과제 지연 제출: 0–6h 90% 인정 / 6–12h 70% / 12–24h 50% / 24h~ 0%.
- **선수 추천**: Machine Learning, Deep Learning, Python/PyTorch, 선형대수 (교수 언급: "새로운 것을 배우려는 태도가 지식보다 중요")

## 개요

분산·연합 학습(distributed & federated learning)의 연산·통신·메모리 효율성, non-IID 데이터, 보안·프라이버시, 개인화 문제를 다루고, 학습된 모델의 효율적 추론(inference) 방법론까지 다룬다. 이론 + 구현 과제.

## 주차별 계획

| 주차 | 내용 | 비고 |
|---|---|---|
| 1 | Course Overview & Introduction | |
| 2 | Recap of AI/ML & Memory Issues in Deep Learning | |
| 3 | Data Parallelism | |
| 4 | Pipeline/Tensor/Sequence Parallelism | |
| 5 | Hybrid Parallelism | |
| 6 | Communication Efficiency in Distributed Training | |
| 7 | Synchronous and Asynchronous Updates | |
| 8 | **Midterm Exam** | |
| 9 | Robustness and Fault Tolerance in Distributed Training | |
| 10 | Multi-User Training | federated learning |
| 11 | Multi-User Training | federated learning |
| 12 | Inference Optimization | |
| 13 | Inference Optimization | |
| 14 | Applications to Recent Topics | |
| 15 | Study Week | |
| 16 | **Final Exam** | |
