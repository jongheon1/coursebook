# Week 01 강의 노트 — Course Overview & Introduction

> 소스: 2026-09-02(수) 강의 녹음 STT + 강의 슬라이드(`week1-01-course-overview.pdf`, 38 slides). 담당 교수 한동준(Dong-Jun Han). 원본은 `_private/` 에만 있다.

## 1. 운영 정보 (logistics)

- **담당교수**: 한동준 (Dong-Jun Han) — 컴퓨터과학과. Edge AI Lab 운영.
  - 학력·경력: KAIST 수학·전기전자공학 학사(2016) → KAIST 전기전자공학 석·박사(2022) → Postdoc @ KAIST(2022.03–2022.12) → Postdoc @ Purdue(2023.01–2024.08) → Assistant Professor @ Yonsei(2024.09–현재)
  - 연구분야: distributed/federated learning, trustworthy & robust AI(personalization, OOD generalization), resource/data-efficient learning(parameter-efficient fine-tuning, model compression) — 이 과목의 관심사와 직결된다. 강의에서 반복적으로 나오는 "personalization", "edge-cloud collaboration" 프레이밍이 본인 연구 주제에서 나온 것.
  - 이메일: djh@yonsei.ac.kr · 방: 공학관4 D720호
- **TA**: 최용희(Yonghee Choi, 2025321337@yonsei.ac.kr), 신성현(Sunghyun Shin, sunghyun.shin@yonsei.ac.kr)
- **강의실**: D408 (교수가 강의 중 "E408"이라 발음했으나 슬라이드 기준 D408이 맞음 — STT 오인식 정정)
- **시간**: 수 11:00–11:50, 금 11:00–12:50(공식 시간표상 10분 휴식 포함). 교수는 금요일 휴식 없이 12:40 종료 예정이라고 언급(점심시간 확보 목적) — 공식 시간표와 다르게 운영될 수 있음.
- **오피스 아워**: 정해진 시간 없음, 이메일로 약속 후 온/오프라인 진행.

### 성적 평가

| 항목 | 비중 | 비고 |
|---|---|---|
| 출석 | 10% | 아래 지각/결석 규정 참고 |
| 과제 | 30% | 미니과제 1(15%) + 미니과제 2(15%), 템플릿 제공 예정 |
| 중간고사 | 30% | 슬라이드 표기: 2025-10-24(금) 11:00–12:50 |
| 기말고사 | 30% | 슬라이드 표기: 2025-12-19(금) 11:00–12:50 |

- **주의**: 슬라이드의 시험 날짜 연도가 "2025"로 되어 있다. 이 강의는 2026-2학기 진행이므로 슬라이드가 작년 템플릿을 재사용했을 가능성이 높다 — **실제 2026년 날짜는 LearnUs 공지로 재확인 필요** (`delta.md` 참고).
- 시험 일정은 확정이며 변경 불가 — 교수가 "다른 과목과 겹치더라도 조정 안 해준다"는 취지로 제주도 항공권 등 개인 사정으로 시험을 옮겨달라는 요청을 받아온 경험을 언급(이번 강의 자체에는 해당 일화가 나오지 않았고, W1 강의에서는 "일정은 고정이니 다른 과목과 안 겹치는지 미리 확인하라"는 언급만 있었음).
- **지각/결석 규정**: 지각 3회 = 결석 1회. 결석 2회(=지각 6회+결석 1회+지각 3회 조합까지)는 무감점. 결석 2회 초과부터 결석 1회당 -1점.
- **과제 지연 제출 페널티**: 0–6시간 지연 90% 인정 / 6–12시간 70% / 12–24시간 50% / 24시간 초과 0%.
- 세부 사항(과제, 시험, 강의노트)은 LearnUs에 업로드 예정.

### 강의 방식

- 교재 없음 — 분야가 아직 emerging이라 마땅한 교과서가 없음. 최근 논문 기반 자료를 교수가 직접 슬라이드로 재구성해서 쉽게 설명.
- 필요시 참고 링크 제공, 일부 주차는 Google Colab 실습 코드 업로드, 문제 세트(problem sets)로 중간/기말 대비 지원.
- 선수지식: 머신러닝/딥러닝, 선형대수, Python/PyTorch 기본 이해. "새로운 걸 배우려는 태도가 더 중요하다"고 강조.

## 2. 과목 제목 풀어보기: Learning, Inference, Distributed

교수는 "왜 이 과목을 듣는가"를 과목 제목("Distributed Learning and Inference")의 세 키워드를 하나씩 풀어서 설명하는 방식으로 시작했다.

### Learning (training)이란

- 모델 + 데이터 + 알고리즘 + 하드웨어의 조합. "모델을 최적화하고 싶고, 그 모델이 배우길 바라는 데이터가 있으면, 특정 과제를 풀 수 있는 모델을 얻는다"는 넓은 정의. AlphaGo 예시: 과거 대국 기록(데이터) → 모델에 입력 → 이기는 법 학습.
- 지도/비지도/강화학습이라는 전통적 분류보다, "데이터를 이용해 모델을 바꾸는 모든 과정"이라는 넓은 정의를 강조 — 이 과목에서 쓸 작업 정의.
- **알고리즘**과 **하드웨어**를 훈련의 두 축으로 명시. 특히 하드웨어(GPU 메모리·연산 제약)를 "많은 공학 수업이 무시하지만 이 과목은 다룬다"고 못박음 — 이 과목의 정체성 발언.

### Inference (serving/deployment)란

- 훈련이 끝난 뒤 모델을 unseen data에 적용해 서비스를 제공/제공받는 단계. Training과 Inference를 이 과목에서는 명확히 구분해서 다룬다고 강조.
- ChatGPT를 예시로: "훈련이 어떻게 됐는지는 모르지만 어떻게든 훈련됐고, 그 모델이 서비스로 제공된다" — inference = test/service/deployment 단계.

### Foundation model

- 정의(Bommasani et al. 2022 인용, 슬라이드 그대로): "넓은 데이터로 학습되어 다양한 downstream task에 적용(파인튜닝)될 수 있는 모델".
- **Pre-training**(파운데이션 모델 자체를 만드는 단계, 주로 산업계 — OpenAI/DeepSeek/Meta 예시)과 **fine-tuning**(특정 task로 개인화, 산업계+학계 모두 가능)을 구분. Pre-training이 fine-tuning보다 훨씬 많은 하드웨어·시간·데이터를 요구한다고 명시.
- 이 과목은 pre-training/fine-tuning 알고리즘 자체를 깊이 다루지 않는다고 명확히 선을 그음. **다룰 것은 그 과정에서 생기는 GPU 메모리/연산/지연(delay) 문제** — 원인은 (1) 대규모 데이터셋, (2) 대규모 모델.

### Distributed — 이 과목의 핵심 질문

> "대규모 데이터셋으로 대규모 모델을 어떻게 효율적으로 훈련시키고, 훈련된 모델을 어떻게 효율적으로 배포·서빙할 것인가?"

- 앞부분(효율적 훈련) → training 측, 뒷부분(효율적 배포) → inference 측. 이 두 문제를 "분산"이라는 도구로 푸는 것이 과목명의 유래.

## 3. 분산 학습의 두 유형 (Type 1 / Type 2)

교수가 직접 "Type 1", "Type 2"라는 용어로 분산 학습을 두 갈래로 나눴다 — **예습 챕터(`weeks/01-course-overview/README.md`)의 분류 체계 표(§7.1: data/pipeline/tensor/sequence/hybrid)와는 다른 상위 레벨 분류**이므로 주의. 예습 챕터의 축들은 전부 Type 1 안에 속한다.

- **Type 1 — 단일 그룹(서버/데이터센터/랩) 안에서 여러 GPU로 훈련 효율화**
  - Centralized training(단일 머신, 모델+데이터 전부 한 곳)의 memory/compute 한계에서 출발.
  - 해결책: 여러 머신 도입 → **data parallelism**(데이터를 나눔) 또는 **model parallelism**(모델을 나눔, layer 단위 분할이 한 예 — tensor/pipeline parallelism도 모델 병렬화의 하위 유형으로 언급, 상세는 이후 주차).
  - GPU가 클라우드 서버든 데이터센터든 랩 서버든 위치는 상관없고, "여러 device로 나눈다"는 개념 자체가 Type 1.
- **Type 2 — multi-user collaboration (federated learning)**
  - 데이터가 이미 여러 사용자에게 자연스럽게 분산되어 있는 상황(예: 병원마다 다른 질병 데이터). Type 1처럼 "의도적으로" 나누는 게 아니라 애초에 나뉘어 있음.
  - 목표: 여러 사용자가 데이터를 옮기지 않고 협력해서 하나(또는 여러) 모델을 학습.

## 4. 분산 추론 (distributed inference)

훈련뿐 아니라 **추론(inference)에도 분산이 필요하다**는 것이 이번 강의에서 교수가 명시적으로 던진 질문이자 답. 근거로 ChatGPT를 다시 예시로 듦: 수십억 사용자가 동시에 OpenAI에 요청 → 단일 GPU로는 처리 불가.

- **Type 1과 유사한 방식**: 모델을 여러 GPU에 쪼개거나(추론 속도 향상), 모델 복사본을 여러 개 두어(동시 사용자 처리) 대응.
- **Edge-cloud collaboration**: 로컬(사용자 기기)에 자체 모델을, 클라우드 서버에도 모델을 두고 "예측을 어디서 할 것인가"를 선택하는 문제. 로컬 추론 vs. 서버로 요청 전송 후 결과 수신 — 사용자가 많아질수록 서버 부담 증가가 트레이드오프.
- 이 edge-cloud 프레이밍은 교수 본인의 연구분야(Edge AI Lab)에서 직접 나온 관점으로 보인다.

## 5. 과목 아젠다 (구두로 설명된 순서)

1. Background studies (딥러닝 기초, W1–2) — 이미 아는 사람은 복습, 모르면 이번에 학습.
2. Centralized training의 이슈들 → Distributed training: data parallelism, 여러 model parallelism 유형.
3. 분산 훈련의 근본 문제 — 통신(communication)과 지연(delay)은 피할 수 없고, 일부 device가 악의적/고장일 때의 안전성·견고성(robustness)도 다룸.
4. Type 2(multi-user, federated learning).
5. Inference strategies (멀티 GPU 서빙, edge-cloud 협업).
6. 스터디 위크 → 기말고사.

전체 구조는 상황에 따라 조금 바뀔 수 있지만 큰 틀은 고정이라고 언급.

## 6. 마무리

첫 강의의 목적을 스스로 요약: "이 과목이 무엇에 관한 것이고, 왜 배울 만큼 중요한지 설명하는 것." 대규모 데이터·모델 문제 때문에 분산 훈련·추론 기법이 실무에서 실제로 필요하다는 점을 강조하며 마무리. 다음 수업(금요일)부터 딥러닝 기초 warm-up, 그다음 주부터 centralized training의 memory/compute/delay 문제로 진입 예정.
