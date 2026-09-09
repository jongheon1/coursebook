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
- 시험 일정은 확정이며 변경 불가 — "다른 과목과 안 겹치는지 미리 확인하라"고 안내.
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

---

# Day 2 (2026-09-04, 금) — Deep Learning 기초 (Week 1 & 2)

> 소스: 2026-09-04(금) 강의 녹음 STT(whisper-1 verbose_json, 세그먼트별 실타임스탬프) + 슬라이드 `week1-02-dl-basics.pdf` ("Week 1 & 2 — Basics of Deep Learning"). **슬라이드 제목은 Week 1&2 전체를 포괄하지만, 이번 강의에서 실제로 다룬 내용은 슬라이드의 "This Week's Goal" 목록 중 정의(DNN)·loss function·mini-batch SGD까지이며, backpropagation·overfitting·batch normalization·CNN/attention 응용은 슬라이드에 있지만 이번 시간에는 다루지 않았다(교수가 명시적으로 다음 수요일로 미룸)** — 아래 노트는 이번 강의에서 실제로 다룬 범위까지만 정리한다.

## 7. 운영 공지

- 출석은 다음 시간(금)부터 Y-Attend 앱 코드 입력 방식으로 체크하되, 교수 본인은 과거 강의에서 "출석 체크한 학생 수"와 "실제로 앉아 있던 학생 수" 사이에 큰 괴리가 있었다는 걸 알고 있어서, 구두로 자주 확인하지는 않겠다고 명시. "그런 식으로 편법 쓰는 건 장기적으로 자기 자신한테 도움이 안 된다"고 언급. 앱상 출석은 다 찍혔는데 실제로 학생이 적어 보이면 가끔 구두로 확인할 수 있음.
- 파이토치·머신러닝에 익숙하지 않은 학생을 위해 PyTorch 기초 자료를 LearnUs/Colab에 추가로 업로드해둠.
- 오늘(그리고 아마 다음 주까지)은 딥러닝 기초 복습이라 출석을 체크하지 않겠다고 재차 언급. 이미 아는 학생은 나가도 되고, 모르는 학생은 "암기보다 원리 이해가 우선"이라는 태도로 들으라고 당부.

## 8. Deep Neural Network 정의

- 요즘 대부분의 머신러닝 모델은 deep neural network(DNN)다. 구조: 입력 데이터(이미지 또는 문장) → DNN → 예측(다음 단어 예측, 이미지 분류, object detection, 수학 문제 풀이 등). 예시로 쓰인 건 이미지 분류 — 개 이미지를 입력하면 "개"라는 결정이 나오는 것.
- **뉴런 하나의 구조** (생물학적 뉴런에서 영감을 받음): 입력 $x_0, x_1, x_2$ (이미지 패치의 RGB 값이나 단어 임베딩처럼 실수값으로 변환된 것들) 각각에 가중치 $w_0, w_1, w_2$를 곱하고 합산(weighted sum) → bias $b$를 더함 → 비선형 activation function을 거쳐 뉴런의 출력이 됨. $w$들과 $b$가 모델 파라미터이고, 학습의 목표는 이것들을 태스크에 맞게 최적화하는 것.
- 이 출력이 다음 layer 뉴런의 입력이 되어 같은 과정(곱셈→합산→bias→비선형 활성화)이 반복됨. 이 뉴런을 세로·가로로 쌓은 것이 deep neural network.

## 9. 왜 layer를 쌓는가, 왜 비선형 activation이 필요한가

- **layer를 쌓는 이유**: neural network는 결국 하나의 함수(function)다. layer(= 파라미터)가 많을수록 표현할 수 있는 함수가 더 복잡·다양해진다. 즉 neural network를 설계한다는 건 태스크를 잘 푸는 복잡한 함수를 설계하는 것과 같고, 이게 사람들이 layer를 계속 늘리려는 이유다.
- **비선형 activation function이 필요한 이유 (직접 유도)**: 교수가 학생들에게 "비선형 activation function이 정말 필요한가?"를 직접 물어봄. 만약 비선형 활성화 함수를 전부 제거하면 neural network는 단순한 행렬곱의 연쇄가 된다. 입력 $x$, 1층 가중치 $W_1$(예: 5×4 행렬)이라 하면 1층 출력은 $W_1x$. 비선형성이 없으면 이게 그대로 2층, 3층으로 들어가서 최종 출력은 $W_3 W_2 W_1 x$가 되는데, 이 세 행렬의 곱은 항상 하나의 행렬 $W'$로 합쳐질 수 있다. **즉 비선형 activation 없이는 3층이든 100층이든 항상 단일 layer 신경망으로 다시 쓸 수 있다 — layer를 쌓아도 표현력이 늘지 않는다.** 그래서 비선형 activation function은 신경망의 표현력을 실제로 늘려주는 필수 요소다.
- 어떤 activation function이 가장 좋은지는 애플리케이션·데이터셋·모델 아키텍처에 따라 다르며 "무조건 최고"인 함수는 없다 — 다만 비선형성 자체는 필수. 예시: ReLU($z>0$이면 $z$, 아니면 0 — 가장 직관적인 형태), 그 외 Leaky ReLU, sigmoid, tanh(하이퍼볼릭 탄젠트) 언급.

## 10. Softmax layer

- 신경망 출력은 보통 확률(probability)이어야 하는데, 출력을 그대로 두면 0~1 사이라는 보장이 없다. softmax layer는 모델 출력을 확률값으로 바꿔준다.
- 방법: 각 값에 지수함수(exponential)를 취한 뒤, 그 합으로 나누어 정규화(단순 합으로 정규화하는 것도 대안이지만 이 방식은 아님). 지수를 취하기 때문에 값들 사이의 상대적 격차가 확률로 변환된 후 더 커진다 — 예: softmax 전에는 3~4배 차이였던 것이 softmax 후에는 40배 정도 차이가 될 수 있다.
- 단순 분류 task에서는 확률이 가장 높은 클래스를 선택하고, LLM의 next-word prediction에서는 확률이 가장 높은 다음 단어를 선택한다. 신경망 전체는 흔히 "가중치+activation의 스택"이라고 부르고, 이런 구조를 multi-layer perceptron(MLP) 또는 그냥 deep neural network라고 부른다.

## 11. Forward Propagation

- forward propagation = 이미지나 단어를 신경망에 입력해서 출력을 계산하는 과정 전체.
- **차원 walkthrough (칠판 예시)**: 데이터 샘플 $x$의 입력 크기가 784인 벡터($x_1,\dots,x_{784}$)라 하면, 1층 가중치 $W_1$의 열(column) 수는 반드시 784(입력 차원과 일치), 행(row) 수는 다음 layer의 뉴런 개수와 같다. $W_1 x$를 계산하고 bias를 더한 뒤 원소별(element-wise) 비선형 활성화를 적용하면 $a_1$을 얻는다($a_1$의 길이 = 그 layer의 뉴런 수). 같은 과정을 $W_2$에 대해 반복하는데(예시에서 출력 클래스 수 10이면 $W_2$의 행 수는 10), 마지막에 softmax를 거쳐 확률 $y$를 얻는다. 이 전체 계산 과정이 forward propagation.
- forward propagation을 알면 새로운 test 샘플에 대해 모델 성능을 평가할 수 있다(입력→계산→예측 확인). 하지만 아직 모델을 **어떻게 학습(training)시키는지는 다루지 않았다** — 학습은 모든 $W, b$ 파라미터를 태스크에 맞게 최적화하는 것인데, 하나의 파라미터를 바꾸면 이후 전체 출력에 연쇄적으로 영향을 주기 때문에 손으로 풀 수 있는 문제가 아니다.

## 12. Loss Function — Cross-Entropy

- 학습을 하려면 먼저 "무엇을 최적화할 것인가"를 정의하는 objective/loss function이 있어야 한다. 신경망 학습의 목표: loss function을 최소화하는 최선의 $W^*$(모든 모델 파라미터)를 찾는 것.
- 학습은 training data 기반: 예를 들어 AlphaGo면 과거 대국 기록, 이미지 분류면 라벨이 붙은 이미지들(이 이미지는 "개", 저 이미지는 "말", "자동차" 등). **전체 loss function은 보통 각 개별 샘플의 loss를 평균낸 것**: $n$개 샘플 중 $k$번째 샘플의 loss를 $L_k(w)$라 하면, 샘플이 맞게 예측되면 값이 작고 틀리면 값이 크도록 정의되어야 한다.
- **cross-entropy loss 정의 (5-class 예시로 도출)**: $C$는 클래스 개수, $t_i$는 one-hot 인코딩된 ground truth($i$가 정답 클래스면 1, 아니면 0), $y_i$는 신경망의 softmax 출력, $q_k$는 $k$번째 샘플의 정답 클래스. Cross-entropy loss $L_k(w) = -\sum_i t_i \log y_i$인데, $t_i$가 정답 클래스에서만 1이고 나머지는 0이므로 이 합은 결국 $-\log y_{q_k}$ 하나로 줄어든다. 슬라이드 예시(softmax 출력이 [0.2, 0.1, 0.4, 0.15, 0.15]이고 첫 값이 정답인 경우)로는 $-\log(0.2)$가 됨.
  - (STT 정정) 강의 음성만으로는 "minus log 0.02"처럼 들리지만, 실제 슬라이드 수치는 0.2이며 계산도 $-\log(0.2)$가 맞다 — 슬라이드를 정본으로 정정.
- cross-entropy를 최소화한다는 건 $y$가 ground truth $t$를 따라가게 만드는 것 — 정답 클래스 확률은 1에, 나머지는 0에 가깝게. 대안으로 두 벡터의 차이를 직접 재는 mean squared error(MSE)도 언급되지만 실무에서는 cross-entropy가 더 흔히 쓰임.
- 최종 loss = 전체 training data에 대한 cross-entropy의 평균. "모델이 잘 학습됐다" = 최대한 많은 샘플을 정확히 예측하도록 이 평균 loss를 최소화했다는 뜻.

## 13. Gradient Descent

- 목표(loss function)는 정했지만, 이걸 어떻게 최적화하는지는 아직 모른다. 파라미터가 수백만 개 이상인 매우 고차원의(non-convex) 문제라 손으로 풀 수 없다.
- **1차원 직관**: $L(w)$를 $w$에 대해 그렸을 때, 기울기(slope)가 음수면 오른쪽으로, 양수면 왼쪽으로 이동($w_{new} = w_{prev} \mp \Delta$), 기울기가 0이면 정지 — 공을 굴리는 것과 같은 비유. 기울기의 **크기(magnitude)**도 중요: 최소점에서 멀수록 크고, 가까울수록 0에 수렴 → 크기가 클수록 더 과감하게, 작을수록 더 정밀하게 이동. 이걸 반영한 업데이트 규칙: $w_{new} = w_{prev} - \eta \cdot \text{slope}$ ($\eta$ = step size/learning rate).
- gradient의 정의는 loss를 $w$에 대해 미분한 도함수. loss가 샘플별 loss의 평균이므로, gradient도 마찬가지로 샘플별 gradient의 평균으로 쓸 수 있다.
- **전체 알고리즘**: $w_0$를 무작위 초기화 → 전체 training data로 gradient 계산 → 업데이트해서 $w_1$ 획득 → 다시 전체 데이터로 gradient 계산 → $w_2$ → ... 이걸 수백 번 반복. **1 epoch = training dataset 전체를 한 번 다 훑는 것**(이 기본형 GD에서는 gradient 한 번 계산할 때마다 전체 데이터를 다 쓰므로, 1회 업데이트 = 1 epoch).
- **장단점**: 매 스텝 전체 데이터를 쓰므로 안정적이지만 계산 비용이 크고, local minima에 갇히기 쉽다(실제 DNN loss landscape는 단순한 그릇 모양이 아니라 고차원의 복잡한 non-convex 함수이며, global minimum 외에 여러 local minima가 존재).

## 14. Mini-batch SGD

- 철학은 GD와 동일(반복적으로 gradient를 계산하고 업데이트)하되, **매 업데이트마다 전체 데이터가 아닌 일부(mini-batch)만 사용**. 예: 전체 데이터를 3개의 mini-batch로 나누고, 첫 mini-batch로 gradient 계산+업데이트 → 다음 mini-batch로 다시 계산+업데이트 → ...
- **왜 덜 안정적인가**: 전체 데이터의 분포와 특정 mini-batch의 분포가 다를 수 있어서, mini-batch 기준 "최적" gradient 방향이 전체 데이터 기준과 다를 수 있음 — 결과적으로 목표 지점으로 바로 가지 않고 더 노이즈가 낀 경로를 그림. 다만 이 노이즈가 오히려 local minima를 탈출하는 데 도움이 될 수 있다는 게 장점.
- **epoch과 셔플**: mini-batch가 3개면 1 epoch = 3번의 mini-batch 업데이트. 한 epoch이 끝나면 데이터셋을 다시 셔플한 뒤 새로 mini-batch를 나눠야 함 — 같은 mini-batch 구성을 계속 재사용하면 모델이 그 구성에 편향되어 성능이 떨어짐.
- **GD vs mini-batch SGD vs SGD(batch size=1)**: 셋 다 같은 업데이트 규칙($w_{t+1} = w_t - \eta g_t$)을 공유하고, $g_t$를 계산할 때 쓰는 샘플 수만 다르다(전체 / mini-batch / 1개). "stochastic"이라는 이름은 mini-batch를 무작위로 뽑는 데서 온 것.

## 15. SGD with Momentum, RMSProp, Adam

이 알고리즘들은 전부 위 gradient descent 업데이트 규칙(강의에서 "27페이지 5번째 줄"이라 지칭)의 업데이트 식만 바꿔 끼우는 형태다.

- **SGD with Momentum**: 현재 gradient $g_t$뿐 아니라 이전 업데이트 방향(momentum)도 함께 고려 — 자동차 운전에 비유: 핸들을 꺾어도 차가 즉시 그 방향으로 가지 못하고 그 사이 어딘가로 가는 것과 같다. $m_t = \alpha \cdot m_{t-1} + g_t$로 momentum을 계산하고, $w_{t+1} = w_t - \eta \cdot m_t$로 업데이트. $\alpha=0$이면 $m_t = g_t$가 되어 momentum 없는 기본 GD로 정확히 환원. 장점: 더 빠른 수렴, local minima 탈출 용이. 단점: momentum이 너무 커지면 global minimum이나 다른 좋은 local minima까지 지나쳐버릴 수 있음.
- **RMSProp**: 방향은 그대로 두고 **step size(learning rate)만** 최근 gradient 크기에 따라 조절. $v_t$ = gradient 제곱값들의 지수이동평균(element-wise, 예: 벡터 [1,2,3]의 제곱은 [1,4,9]) — 최근 gradient 크기가 크면 $v_t$가 커지고, 그러면 유효 learning rate($\eta / \sqrt{v_t}$ 형태)가 작아진다(정밀 탐색). 반대로 최근 gradient 크기가 작으면 learning rate가 커진다(빨리 벗어나기). 이렇게 하는 이유: 기울기가 가파른(=최근 gradient가 큰) 영역은 좋은 minimum 근처일 가능성이 높으니 정밀하게, 평평한(=최근 gradient가 작은) 영역은 좋은 minimum이 없을 가능성이 높으니 빨리 지나가려는 것 — momentum이 좋은 minimum을 지나쳐버리는 문제에 대한 대응.
- **Adam**: momentum(SGD-momentum의 $m_t$)과 RMSProp(적응적 learning rate)을 결합한 것. bias correction 항도 있지만 강의에서는 "지금은 그렇게 중요하지 않다"고 언급하고 넘어감. 실전에서 가장 널리 쓰이는 optimizer이며, 플롯상 대부분의 최신 optimizer(RMSProp, Adam 등)가 전통적 SGD보다 우수한 성능을 보인다. **다만 "Adam이 항상 최고"라는 보장은 없음** — 모델 아키텍처·데이터셋·데이터 양에 따라 다른 optimizer가 더 잘 맞을 수 있다.

## 16. Optimizer별 메모리 요구량 (이 과목의 관심사와 연결)

교수가 이 강의 노트 안에서 유일하게 이 과목의 시스템/메모리 관점과 직접 연결한 대목: optimizer마다 학습에 필요한 GPU 메모리가 다르다.
- 전통적 SGD: 모델(weights) + gradient만 저장하면 됨 — 모델 크기의 약 2배.
- SGD with Momentum: 여기에 momentum 버퍼까지 저장 — 약 3배.
- Adam: momentum류 항 + 추가 항(RMSProp의 $v_t$) + weights + gradient를 전부 동시에 유지 — 더 많은 메모리 필요.
→ 단일 GPU에서 SGD로는 돌아가는 모델이 Adam으로는 메모리 부족(OOM)이 날 수 있다는 실무적 예시를 듦. "이런 optimizer가 정확히 뭘 저장하는지 이해하는 게 중요한 이유"로 제시.

## 17. 다음 시간 예고 및 이번 강의에서 다루지 않은 것

- 남은 질문으로 명시: "이 모든 optimizer가 쓰는 gradient $g_t$ 자체는 어떻게 계산하는가?" — 이 답이 backpropagation이며, 다음 수요일 강의에서 다룰 예정이라고 명시적으로 예고.
- 강의는 쉬는 시간 없이 진행되었고, 다음 수요일부터 backpropagation과 이어서 centralized training의 이슈들(메모리/연산/지연 — Week 2 챕터 내용)로 넘어간다고 마무리.
- **슬라이드에는 있었지만 이번 강의에서 다루지 않은 것** (추측 금지 원칙에 따라 이 노트에도 아직 넣지 않음): backpropagation 자체의 상세 유도, overfitting과 그 방지책(data augmentation, L2 regularization/weight decay, dropout/dropconnect), batch normalization, CNN/attention 등 다른 아키텍처로의 응용. 이들은 실제로 다뤄지는 다음 강의(들)에서 delta.md와 함께 갱신 예정.

---

## Day 3 (2026-09-09) — Backpropagation, Overfitting과 정규화

> 소스: 같은 덱(`week1-02-dl-basics.pdf`), 이전 시간 예고대로 backpropagation부터 이어감. 강의 초반에 지난 시간 내용(gradient descent, optimizer들)을 짧게 복습.

- **Backpropagation 유도 마무리**: chain rule을 층(layer)마다 적용해서, 최종 출력 $y$에 대한 손실로부터 시작해 각 층의 가중치에 대한 gradient를 뒤에서 앞으로 전파하는 과정을 구체적인 표기($a^{(L-1)}$ 등)로 끝까지 전개. "이 값을 이미 안다고 가정하면, 이 값은 chain rule로 바로 계산된다"는 식으로 앞 층 gradient가 뒷 층에서 계산된 값을 재사용한다는 게 핵심(그래서 "back"propagation).
- **왜 train/test를 나누는가**: 학습에 쓴 데이터로 성능을 재는 건 의미가 없으므로(모델이 그 데이터를 이미 맞추도록 최적화됐기 때문), 학습에 안 쓴 validation/test 데이터로 성능을 측정해야 한다는 것.
- **Overfitting vs. Underfitting**: **CIFAR-10 데이터셋**을 예로 들어 cross-entropy loss를 계산해보고, 모델이 너무 복잡(overfitting, training error는 계속 낮아지는데 validation error는 어느 순간부터 다시 올라감)하거나 너무 단순(underfitting)한 경우를 그래프로 설명.
- **Overfitting 완화 전략**:
  - **데이터를 더 모은다** — 가장 직접적이지만 항상 쉬운 건 아님.
  - **Data augmentation** — 있는 데이터를 변형해서 늘림.
  - **L2 정규화(weight decay)** — 기존 손실함수에 가중치 크기에 대한 페널티 항을 더함. 직관: 모델이 특정 가중치에 과도하게 의존하지 못하게 막는 것. 트레이드오프: 정규화를 너무 세게 걸면 모델이 충분히 복잡한 패턴을 못 배움.
  - **Dropout** — 학습 중 뉴런 일부를 무작위로 꺼버림. 왜 도움이 되는지: 특정 뉴런 조합에 과도하게 의존하는 "이상한" 최적화 경로를 막아준다는 설명, 학습 시와 추론 시 동작 차이(및 그 실제 성능 비교)도 언급.
- **마무리 공지**: PyTorch 관련 자료 LearnUs 업로드 예정. **금요일 강의 예고**: batch normalization, CNN, 그리고 분산 학습(distributed training)이 왜 필요한지에 대한 동기 부여. 다음 주부터는 예고된 대로 분산 학습 본론으로 들어갈 예정.
