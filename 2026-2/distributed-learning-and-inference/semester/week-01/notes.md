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

---

## Day 4 (2026-09-11) — Batch Normalization, CNN, Issues in Centralized Training

> 소스: 2026-09-11 강의 녹음 STT 2건(같은 시간대에 이어진 녹음, 시간순) + 슬라이드. 첫 번째 파일은 지난 시간 예고대로 `week1-02-dl-basics.pdf` 덱의 남은 부분(batch normalization, CNN)을 마무리한다. t=2163부터 교수가 "이 강의 노트의 제목은 Issues in Centralized Training"이라고 명시적으로 선언하며 완전히 새로운 덱으로 전환한다 — **이 새 덱은 이번 한 번의 수업에서 도입부부터 결론(다음 주 예고)까지 전부 다뤄졌다.**

### 18. Batch Normalization — 동기 (Motivation)

- 지난 시간까지 배운 것 요약 복습: loss function 정의 → gradient descent → backpropagation으로 gradient 계산 → overfitting 완화(regularization, dropout). 오늘은 여기에 batch normalization을 하나 더 추가.
- **동기를 예시로 도출**: 집값 예측 문제(입력: house size, number of rooms).
  - (1) **한 mini-batch 안에서** 서로 다른 입력 feature가 서로 다른 스케일·범위를 가질 수 있다 — 스케일이 큰 feature가 학습을 지배(dominate)할 위험. 정규화하면 두 feature가 비슷한 비중으로 학습에 기여하게 만들 수 있다.
  - (2) **mini-batch 간에도** 스케일이 다를 수 있다(예: 첫 mini-batch 값들은 크고 두 번째는 작음) — 정규화하지 않으면 스케일이 큰 mini-batch가 학습을 지배해 훈련이 불안정해진다.
  - (3) 신경망의 **layer마다도** 값의 범위가 달라질 수 있어 특정 뉴런·layer가 지배적이 될 수 있다.
- 이 세 가지 관찰이 "각 hidden layer의 입력을 (mini-batch 단위로) 정규화하자"는 batch normalization의 동기.
- **주의**: 원 논문도 "왜 되는지"에 대한 명확한 이론적 설명을 주지 않으며, 최근 논문들도 여전히 설명을 시도하는 중 — 보편적으로 합의된 이론은 없다. 위 동기는 어디까지나 직관적인 설명일 뿐.

### 19. Batch Normalization — 메커니즘 ($\mu$, $\sigma$, $\gamma$, $\beta$)

- 정규화가 없을 때 뉴런 하나의 계산: 입력 $x_k$ → 가중치 곱+합산 → $z_k$ → 비선형 activation. Batch norm은 **$z_k$를 계산하는 방식은 그대로 두고**, $z_k$가 비선형 activation을 통과하기 전에 정규화 층을 하나 끼워 넣는다.
- **정규화 방법**: 하나의 mini-batch($B$개 샘플, $k=1,\dots,B$)에 대해 $z_k$를 전부 계산 → 그 mini-batch 기준 평균 $\mu$, 분산 $\sigma^2$ 계산 → $\hat z_k = (z_k - \mu)/\sigma$. 이렇게 하면 통계적으로 모든 값이 비슷한 범위를 갖게 된다.
- **여기서 끝나지 않는다 — $\gamma, \beta$ 도입**: 정규화된 $\hat z_k$를 그대로 activation에 넣는 대신, **scale($\gamma$)·shift($\beta$)한 값** $\gamma \hat z_k + \beta$를 activation에 넣는다. $\gamma, \beta$는 뉴런마다 존재하는 **학습 가능한(trainable) 파라미터**로, 기존 모델 파라미터 $W$에 더해 batch norm을 쓰면 추가로 학습해야 할 파라미터가 생기는 것.
- **왜 굳이 scale/shift를 하는가**: 정규화 범위를 고정값(평균 0, 분산 1)으로 강제하는 게 항상 최적이라는 보장이 없다는 직관. $\gamma, \beta$를 학습 가능하게 열어두면 뉴런별로 최적의 정규화 범위를 훈련을 통해 자동으로 찾을 여지가 생긴다 — 더 많은 유연성·개선 여지.
- $\gamma, \beta$도 **backpropagation으로 업데이트**된다(단, $W$에 대한 backprop 식과는 형태가 다르며 이번 수업에서 유도까지는 다루지 않음). 핵심은 구현이 쉽다는 것 — 원리를 완전히 이해하지 못해도 이 층을 추가하고 그대로 backprop을 돌리면 $\gamma, \beta$가 알아서 학습된다.

### 20. Batch Normalization — Training vs. Inference

- **문제**: 학습이 끝나면 $\gamma, \beta$는 확정되지만, inference 시점의 $\mu, \sigma$는 어떻게 정하는가? Test 샘플은 보통 1개씩 들어오므로 "mini-batch 통계"를 그 자리에서 계산할 방법이 없다(여러 test 샘플을 동시에 넣지 않는 한).
- **해법**: 학습 중에 각 mini-batch마다 계산됐던 $\mu, \sigma$ 값들의 **이동평균(moving average)** 을 구해서 고정시켜두고, inference 때는 이 고정된 $\mu, \sigma$와 학습된 $\gamma, \beta$를 그대로 사용한다.
- **효과**: batch normalization을 적용하면 훈련이 훨씬 안정적이고 빨라진다(강의 그래프에서 파란 곡선=batch norm 적용, 주황 곡선=미적용 — 파란 쪽이 확연히 안정적). 단점·한계도 존재하며, 이를 mini-batch에 의존하지 않는 방식으로 개선한 **group normalization, layer normalization**도 언급(세부 내용은 다루지 않음 — batch norm 원리를 이해하면 유추 가능하다고만 언급).

### 21. CNN — Convolution 연산

- 배경: 지금까지는 fully-connected layer 기준으로 backprop을 다뤘지만, CNN·attention/transformer 같은 잘 알려진 다른 아키텍처도 존재한다. 이번 강의에서는 CNN만 개략적으로 다루고 넘어감(CNN 자체의 이해가 이 과목의 핵심은 아니지만, 이후 예시에 등장할 수 있어 배경으로 소개).
- **기본 아이디어**: 이미지에 필터(filter/kernel)를 대고, 필터가 이미지 전체를 스캔하며 어떤 정보가 담겨 있는지 뽑아낸다. 필터(커널)가 CNN의 **모델 파라미터**.
- **2D convolution 연산**: 필터를 이미지의 한 위치에 대고 element-wise 곱 후 합산(weighted sum)해서 출력값 하나를 얻는다 → 필터를 옆으로 이동시키며 같은 연산을 반복 → 출력 feature map 전체를 채운다.
- **필터 여러 개 사용**: fully-connected layer에서 뉴런을 여러 개 두는 것과 같은 논리로, 필터를 여러 개(예: blue filter + red filter) 두면 각 필터가 독립적으로 이미지를 스캔해 각각의 출력을 만들고, 이를 쌓아 depth가 있는 출력을 만든다. **출력 depth = 필터 개수**(fully-connected에서 뉴런 수가 늘면 출력 차원이 느는 것과 동일한 논리). 이후 fully-connected와 마찬가지로 비선형 activation을 거친다.
- **입력이 다채널(RGB 등)일 때**: 실제 이미지는 보통 RGB 3채널 → 입력 depth = 3. 이 경우 **필터의 depth도 반드시 입력 depth와 일치**해야 한다(예: depth 3). 필터 depth가 3이어도 필터는 "1개"로 취급되며(R·G·B 각 채널에 대해 conv 연산을 한 뒤 셋을 합산해서 값 하나를 얻음), **출력 depth는 필터의 depth가 아니라 필터의 개수로 결정**된다.
- **일반적인 경우(다채널 입력 + 다중 필터)**: 입력 depth가 3이면 각 필터의 depth도 3이어야 하지만, 필터를 2개 쓰면 각 필터가 만드는 결과가 하나씩(filter 1 결과, filter 2 결과) 쌓여 최종 출력 depth = 2가 된다. 즉 **필터 depth는 입력 depth와 맞추고, 출력 depth는 필터 개수가 결정**한다는 원칙이 핵심.

### 22. CNN — 전체 아키텍처, Pooling, 학습

- 전체 그림: (convolution + 비선형 activation) 블록을 여러 층 쌓고(fully-connected에서 layer를 쌓는 것과 동일한 논리), 마지막에 fully-connected layer를 붙여 classification 등 최종 예측을 수행한다.
- **Max pooling**: CNN에만 있는 별도 연산으로, 정보를 압축(compression)하는 과정 — 특정 영역에서 값을 고르거나(max) 평균을 취하는 식의 마스크(mask) 연산. 목적: (a) 연산 부담을 줄이고, (b) 작은 회전·국소적 왜곡(local distortion)에 모델을 어느 정도 불변(invariant)하게 만든다 — 경험적으로 자리 잡은 휴리스틱. Convolution+비선형+pooling 블록이 여러 번 반복되는 구조.
- **왜 "국소적(local)"으로 보는 게 말이 되는가**: 이미지 속 각 물체는 특정 영역에 국한(localized)돼 있어서, 서로 멀리 떨어진 픽셀끼리보다 가까운 픽셀끼리 상관관계가 높다 — 그래서 필터가 인접 픽셀만 묶어서 처리하는 게 합리적이라는 설명.
- **학습 방식은 fully-connected와 완전히 동일**: forward propagation → loss 계산 → backpropagation으로 gradient 계산 → mini-batch SGD/momentum/RMSProp/Adam 등으로 업데이트. Backprop의 구체적 수식은 아키텍처(conv 연산)에 맞게 달라지지만 절차 자체는 바뀌지 않는다 — **바뀌는 건 아키텍처뿐**. Overfitting 대응(dropout, weight decay)이나 batch normalization도 CNN에 동일하게 적용 가능.
- 이것으로 "딥러닝 기초" 파트(DNN 구조, loss function, optimizer, backpropagation, overfitting 대응, batch normalization, 대표 아키텍처 CNN)를 마무리. Transformer는 필요할 때마다 배경 설명을 추가하는 방식으로 다룰 예정이라고 언급.

---

**(여기서부터 새 덱: "Issues in Centralized Training" — t=2163)**

### 23. Issues in Centralized Training — 정의와 문제의 동기

- 지금까지 쌓은 딥러닝 배경지식은 바로 이 문제(그리고 다음 주부터 다룰 분산 학습)를 기술적으로 이해하기 위한 준비였다는 점을 강조하며 새 강의노트를 시작.
- **Centralized training의 정의(이 과목 기준)**: 모델과 데이터셋이 **하나의 GPU·하나의 머신**에 모두 있는 상태로 학습하는 것.
- **문제의 동기**: 모델 크기가 GPU 메모리보다 빠르게 커지고 있어 단일 머신에서 매우 큰 모델을 학습하는 게 어렵거나 아예 불가능해진다(out-of-memory). 데이터셋 크기가 클 경우에도 메모리뿐 아니라 연산량·지연(delay) 부담이 커진다.
- **On-device 학습 예시**: Qualcomm·Apple 같은 모바일 AI 하드웨어는 서버용 고가 GPU보다 메모리가 훨씬 작아, 모델 크기와 메모리 간 격차가 더 크다 → on-device 학습은 특히 더 어려운 문제.
- 결론: 큰 모델 + 큰 데이터셋이 centralized training의 근본 이슈이고, **분산 학습(distributed training)은 이 격차를 메우기 위한 한 방향**(여러 머신을 도입해 협력적으로 학습).

### 24. 핵심 지표 세 가지: Memory, Computation, Delay

- 학생 질문에 대한 답으로 명시: centralized training의 이슈를 볼 때 봐야 할 핵심 지표는 **memory, computation(연산량), delay(지연)** 세 가지.
- Memory는 다시 두 가지로 나뉜다: **parameter memory**와 **activation memory** — 이후 순서대로 설명.

### 25. Parameter Memory

- 문제 제기: GPU가 96GB인데 모델이 120GB면 당연히 OOM. 그런데 **모델이 80GB로 GPU(96GB)보다 작아도 학습이 안 되는 경우**가 많다 — 그 이유 중 하나가 parameter memory.
- **SGD**: 모델 파라미터 수를 $m$이라 하면, gradient도 원소 수가 $m$개(전체 파라미터를 업데이트한다고 가정) → 모델 + gradient = 약 $2m$ 필요.
- **SGD with Momentum**: 모델 + gradient + momentum buffer(동일 차원) → 약 $3m$.
- **Adam**: momentum류 항 + RMSProp의 $v_t$ 항 + 모델 + gradient를 전부 동시에 유지 → 약 $4m$(momentum, $v_t$, weights, gradient가 모두 같은 차원이라고 가정).
- **파라미터 수 세는 법**: linear layer는 (입력 차원 $c_i$) × (출력 차원 $c_o$); conv layer는 (필터 개수 $c_o$) × $c_i \times k_h \times k_w$($c_i$=입력 채널, $k_h, k_w$=필터 높이·너비).
- **모델 크기 = 파라미터 개수 × bit width**. 워크드 예시(Q&A 포함): 파라미터 6,100만 개(61M)를 32-bit float로 저장하면 모델 크기 ≈ 244MB(61M × 4byte). 이 경우 optimizer별 필요 메모리는 **SGD 244×2, SGD+Momentum 244×3, Adam 244×4 (MB)** 로 커진다. 8-bit 등으로 quantize하면 저장량은 줄어들지만 여전히 파라미터 개수에 비례한다.
- **핵심 메시지 두 가지**: (1) GPU 메모리가 모델 크기보다 크다고 해서 학습이 보장되지 않는다 — gradient·optimizer state 때문. (2) optimizer가 복잡할수록(SGD < Momentum < Adam) 필요 메모리가 커진다 — 그래서 Adam으로는 OOM이 나던 모델이 SGD로 바꾸면 돌아가는 경우가 실제로 있다.
- Parameter memory는 **모델 크기에 비례**하고, **mini-batch 크기·데이터셋 크기와는 무관**하다는 점이 다음 섹션(activation memory)과의 핵심 차이.

### 26. Activation Memory

- Parameter memory보다 **직관적이지 않은** 개념이며, 이를 이해하려면 backpropagation의 구조를 다시 봐야 한다.
- **activation 개수 정의**: 샘플 1개를 입력하면 각 layer의 activation 개수 = 그 layer의 출력 뉴런 수(예: 입력 5 → layer1 출력 4개 → layer2 출력 3개 → layer3 출력 2개). **Mini-batch SGD처럼 $n$개 샘플을 텐서로 묶어 동시에 처리**하면, 각 layer의 activation 개수가 뉴런 수 × $n$으로 늘어난다(예: 4n, 3n, 2n). Conv layer도 동일 논리: 샘플 1개당 activation 개수는 $c_o \times h_o \times w_o$이고, 배치가 $n$이면 여기에 $n$이 곱해진다.
- **왜 activation을 저장해야 하는가 (backprop과의 관계)**: forward propagation에서 layer $L$의 계산은 $a^{(L-1)}$(이전 layer의 activation, "입력 차원 × 배치 크기"의 행렬)이 가중치 $W$를 거쳐 $z$ → 비선형 activation → $a^{(L)}$이 되는 과정이다. **Backpropagation으로 그 layer의 가중치에 대한 gradient를 계산하려면 chain rule 상 $a^{(L-1)}$(그 layer의 입력 activation)이 반드시 필요**하다.
- **Inference만 할 때는 문제없음**: 추론(forward propagation만 수행)에서는 $a^{(L-1)}$을 이용해 $a^{(L)}$을 구하고 나면 $a^{(L-1)}$은 즉시 버려도 된다(다음 계산에 필요 없음) — 최종 출력까지 이 과정을 반복하며 이전 activation들을 순차적으로 폐기할 수 있다.
- **Training 시에는 즉시 버릴 수 없음**: backpropagation 때 각 layer의 gradient를 계산하려면 forward pass 때 만들어진 그 layer의 입력 activation이 필요하므로, **forward propagation이 끝날 때까지(정확히는 해당 layer의 backward가 끝날 때까지) 모든 중간 activation $a^{(L-2)}, a^{(L-1)}, a^{(L)}, \dots$을 계속 들고 있어야** 한다. Backward pass는 뒤(출력쪽)에서 앞쪽으로 진행되며, 각 layer의 gradient 계산이 끝날 때마다 그 layer가 썼던 activation을 순서대로(출력에 가까운 것부터) 버릴 수 있다.
- **왜 병목(bottleneck)인가**: 모델의 layer 수가 많거나 layer당 뉴런 수가 많을수록 저장해야 할 activation 총량이 커진다(→ **모델 크기에 비례하는 성분**). 동시에 각 layer의 activation 차원은 **mini-batch 크기에 비례**해서 커진다 — 예: mini-batch 1,000이면 샘플 1개일 때보다 activation 차원이 1,000배.
- **결론**: activation memory는 모델 크기와 mini-batch 크기 양쪽에 동시에 비례한다(전체 layer에 대해 합산). 이 때문에 **training 메모리가 inference 메모리보다 훨씬 크다** — parameter memory뿐 아니라 activation memory까지 추가로 필요하기 때문. 실전 경험과 연결: 같은 모델이 mini-batch 크기 112 등에서는 OOM이 나다가 8이나 16처럼 작은 배치로 줄이면 학습이 되는 경우가 흔한 이유가 바로 이것.
- **완화 전략(언급만, 세부는 다루지 않음)**: 모든 activation을 들고 있는 대신 일부만 저장하고 필요할 때 다시 계산하는 **recomputation(activation checkpointing)** — 메모리와 연산량을 맞바꾸는 트레이드오프.
- Parameter memory와 activation memory가 정확히 산술적으로 더해지는 관계는 아니고(다른 메모리 요소들도 존재), 이 두 가지가 가장 핵심적으로 줄이려고 시도하는 병목. 이후 분산 학습 기법들을 배울 때, 각 기법이 parameter memory를 줄이는지 activation memory를 줄이는지로 구분해서 설명할 예정이라고 예고(예: 모델을 여러 조각으로 나눠 여러 머신에 분산하면 머신당 parameter memory도 activation memory도 줄어든다; 데이터셋만 여러 GPU에 나누면 parameter memory는 그대로지만 activation memory는 줄어든다).

### 27. Computation 지표 — MAC, FLOPs

- **MAC(Multiply-Accumulate) 연산**: 신경망 forward propagation에서 흔히 일어나는 연산 — 곱셈(multiply) 하나 + 누적합(accumulate) 하나가 한 세트. Fully-connected layer의 forward propagation에서 입력 차원 $c_i$, 출력 차원 $c_o$, mini-batch 크기 $N$이면 필요한 MAC 연산 수는 $N \times c_i \times c_o$ 형태로 표현된다. CNN처럼 더 복잡한 구조는 MAC 수가 더 늘어나지만 세부 유도는 다루지 않는다.
- **FLOPs(Floating Point Operations)**: 더 일반적이고 직관적인 지표 — 덧셈·뺄셈·곱셈·나눗셈 등 모든 산술 연산을 동일하게(1회 연산 = 1 FLOP) 취급한다. 곱셈 1회 = 1 FLOP, 덧셈 1회 = 1 FLOP이므로, MAC 하나(곱셈+누적합) = 2 FLOPs.
- Backpropagation의 연산량(FLOPs)은 forward propagation의 대략 2배 정도로 알려져 있다(강의에서 참고 링크로 소개, 세부 유도는 다루지 않음).
- **FLOPs가 논문에서 표준적으로 쓰이는 이유**: 특정 하드웨어에 의존하지 않고 알고리즘·모델 자체의 연산 부담을 나타내는 **형식적(formal)** 지표이기 때문 — 그래서 연구 논문들이 연산 효율을 주장할 때 대개 FLOPs 기준으로 설명한다(다만 학습 중 FLOPs를 정확히 세는 건 추론보다 더 어렵다는 언급도 있었다).

### 28. Delay(Latency) 지표

- 연산 부담을 측정하는 또 다른 방법은 **특정 하드웨어에서 실제 지연(delay)을 측정**하는 것 — 같은 GPU에서 알고리즘 A와 B의 지연을 각각 재서, 더 적게 걸리는 쪽을 "더 계산 효율적"이라고 주장하는 방식. FLOPs보다 측정은 쉽지만, **하드웨어에 의존적**이라는 한계가 있다 — 느린 머신에서는 두 알고리즘의 격차가 커 보이고, 빠른 머신에서는 격차가 거의 안 보일 수도 있다. 그래서 FLOPs 쪽이 더 형식적인(formal) 지표로 취급된다.
- Latency는 (a) **알고리즘/모델 쪽 요인** — 모델 크기, 출력 activation 크기, 어떤 optimizer를 쓰는지 — 과 (b) **하드웨어 쪽 요인** — 프로세서가 초당 처리 가능한 연산 수, 메모리 대역폭(memory bandwidth) — 양쪽에 의해 결정된다. 이 지연을 정확히 수식으로 모델링하는 건 늘 어렵고, 이 수업에서 굳이 formal하게 모델링할 필요는 없다고 언급 — 목표는 (단일·복수 머신으로) 학습을 실제로 빠르게 만드는 것. 하드웨어와 알고리즘을 함께 최적화(co-optimization)하려는 하드웨어 연구자들도 있다고 언급.
- Memory 이슈와 마찬가지로, **모델이 크거나 데이터셋·mini-batch 크기가 클수록 computation(FLOPs/MAC)과 latency 모두 증가**한다.

### 29. Q&A — 모델 크기, 트레이드오프, "정답 없음"

- **Q: 모델 크기는 얼마나 커야 이상적인가?** A: 타겟 애플리케이션에 따라 다르다. OpenAI 같은 강력한 범용 foundation model을 지향하면 모델을 가능한 한 계속 키우려 하지만, 어느 순간부터 성능이 더 이상 오르지 않는 구간에 도달할 수 있다 — 데이터가 계속 생성되고 있어도 모델 크기를 무한정 키우면 overfitting 등으로 오히려 성능이 나빠질 위험이 있기 때문에 데이터 양과 모델 크기를 맞춰가야 한다(OpenAI가 사용자로부터 데이터를 계속 수집해 모델을 더 키워나가는 이유로 언급됨 — 정확히 어떻게 쓰이는지는 알 수 없지만 모델 개선에 활용될 것이라는 추정). 반대로 OpenAI 수준만큼 복잡하지 않은 특정 target task라면 무한히 큰 모델이 필요하지 않고, 경험적으로 적정 크기를 찾아야 한다. 또한 **모델 크기보다 아키텍처 선택이 더 중요할 때도 있다** — 예: Transformer 기반 아키텍처가 성능 향상에 크게 기여.
- **Q: 학습이 되려면 모델 크기 대비 메모리가 얼마나 더 필요한가?** A: 보편적인 정답은 없다 — mini-batch 크기와 optimizer 선택에 따라 달라진다(강의 사례: 랩에서 20GB나 10GB급 모델로도 OOM을 겪는 경우가 있었다고 언급). 실무적으로는 시행착오(try-and-see)로 접근하되, 배운 원리에 기반해 **선택지를 좁힐 수 있다**: mini-batch 크기를 줄이거나, 모델 크기를 줄이거나, 더 단순한 optimizer(예: Adam 대신 SGD)를 쓰는 식. **모델 크기 유지가 중요한 태스크라면** optimizer를 단순화하고 mini-batch를 줄이는 쪽으로, **mini-batch 크기 유지가 중요하다면** optimizer를 단순화하고 모델 크기를 줄이는 쪽으로 트레이드오프한다.
- **일반화된 코멘트**: 머신러닝의 많은 부분(왜 batch normalization이 되는지, 왜 Adam이 잘 되는지 등)은 여전히 **정답이 없고 경험·휴리스틱에 의존**하며 활발한 이론 연구 대상이라는 점을 재차 강조(수학+ML 관련 과목을 들으면 이런 이론적 배경을 더 깊이 이해할 수 있다고 언급).

### 30. 결론 및 다음 주 예고

- 오늘 다룬 centralized training의 이슈 정리: **memory 이슈**(parameter memory + activation memory), **computation 이슈**(MAC/FLOPs), **delay 이슈** — 모두 "모델이 크고 데이터셋이 크지만 단일 머신의 메모리·연산·시간은 제한적"이라는 근본 문제에서 비롯된다.
- **다음 주 예고**: 이 문제들을 완화하기 위한 분산 학습(distributed training) 기법으로 바로 진입. 다음 주에는 **data parallelism**(모델은 나누지 않고 데이터에 대해서만 병렬 연산)을, **4주차에는 모델을 여러 머신에 나누는 전략(model parallelism 계열)**을 다룰 예정. 구체적 사례로 **DeepSeek** 모델이 언급됨 — DeepSeek 학습 시 data parallelism과 여러 model parallelism 전략을 함께 활용해 메모리 이슈를 줄이고 학습 속도를 높였다고 예고.
- 쉬는 시간 없이 진행된 강의를 여기서 마무리.

---

## Day 5 (2026-09-16) — Data Parallelism: Parameter Server와 Gradient Synchronization

> 소스: 2026-09-16(수) 강의 녹음 STT + 슬라이드(신규 덱 "Week 3 — Data Parallelism", 49 slides). t=0~419는 지난 금요일(Day 4) 강의 내용에 대한 Q&A 후속 복습이고, t=419부터 교수가 "오늘 강의 제목은 Data Parallelism"이라 선언하며 새 덱으로 전환한다. **이 새 덱은 이번 시간에 도입부부터 시작했지만 "Comparison with Centralized Training" 절 초반, t=2772(11시)에 시간이 다 되어 끝나지 못했다 — 그 절의 결론, 그리고 outline상 남은 항목(memory·delay 분석, 다른 optimizer로의 확장, fully decentralized 설정)은 전부 금요일로 명시적으로 이월되었다.**

### 31. 복습: 지난주 Q&A 후속 (Activation Memory, Computation/Delay, GPU OOM)

- **Activation memory가 언제 최대가 되는가**: forward propagation이 끝난 시점에 activation memory가 **최댓값**을 찍고, 이후 backpropagation이 진행되면서 점점 줄어든다. 구체적으로, $W_{L+1}$에 대한 gradient 계산이 끝나야 그때 쓰인 $A_L$을 버릴 수 있고, $W_L$에 대한 gradient 계산이 끝나야 $A_{L-1}$을 버릴 수 있다 — 즉 **출력에 가까운 activation부터 순서대로 해제**된다(Day 4의 "역순으로 버려진다"는 설명을 한 단계 더 구체화한 것).
- Activation memory 차원은 (재확인) **모델 크기(레이어 수·레이어당 뉴런 수)와 mini-batch 크기 둘 다에 비례**한다. 예: 레이어의 뉴런 수를 늘리면 $D_{in}$이 커져 activation memory 증가; 레이어 수를 늘리면 저장해야 할 activation들이 그만큼 늘어나 총합(=전체 레이어 activation의 합)이 커진다.
- **Q: delay가 왜 $T_{computation} + T_{memory}$로 근사되는가?** A: 메모리 접근(읽기)과 연산이 병렬로 진행될 수 있다는 가정 때문 — 정확히는 최대 지연이 두 값의 합이지만, 병렬 처리가 가능하면 "이미 읽어온 데이터에 대해서는 연산을 할 수 있다"는 가정 하에서 근사적으로 성립한다. **이 과목에서 깊이 다룰 내용은 아니라고 명시적으로 언급.**
- **Q: GPU에서 OOM이 나는 이유, CPU로 offload가 가능한가?** A: 가능하다 — 예를 들어 momentum 같은 **optimizer state를 CPU로 offload**하는 연구도 실제로 존재. 하지만 별도로 설정하지 않는 한 **기본적으로는 아무것도 offload되지 않는다**: CPU는 모델·데이터셋을 불러와 mini-batch를 구성하는 역할만 하고, gradient 계산·backpropagation·optimizer step은 전부 GPU에서 수행된다. 이것이 GPU에서 OOM을 일으키는 실질적 병목이며, offload를 하지 않는 한 **parameter memory + activation memory가 GPU VRAM을 넘으면 곧바로 OOM**으로 이어진다.

### 32. Data Parallelism 도입 — 이번 주 동기와 목표

- 지난주 복습을 마치며 "이제 분산 학습 전략(distributed training strategy)을 이야기할 준비가 됐다"고 선언, **오늘 강의 제목: Data Parallelism**. "Parallelism"이라는 용어가 앞으로 강의 내내 반복해서 등장할 핵심 키워드이며, 병렬화 방법에는 여러 종류가 있음을 예고.
- **지난주 내용 재요약(이번 주 논의의 출발점)**: centralized training = 특정 데이터셋으로 **단일 머신**에서 모델을 학습시키는 것. 대규모 데이터셋·대규모 모델 때문에 memory·computation·delay 문제 발생. 그중 **대규모 모델**은 parameter memory와 activation memory 둘 다에 영향을 주고 계산 지연도 키운다. **대규모 데이터셋**은 한 epoch을 끝내는 데 걸리는 지연을 키운다. **더 큰 mini-batch 크기**를 쓰면 activation memory도 커진다.
- **이번 주의 범위 한정**: data parallelism은 주로 **대규모 데이터셋/mini-batch 크기 문제**를 완화하기 위한 기법이며, 대규모 모델 문제를 다루는 기법이 아니다(모델 문제는 이후 model parallelism 계열에서 다룸).
- **Full-batch gradient descent 복습(동기 부여용)**: 극단적인 경우로 전체 데이터셋을 다 써서 gradient를 계산·업데이트하는 full-batch gradient descent를 고려하면, **batch size = dataset size**가 된다. 이 경우 mini-batch 크기가 곧 dataset 크기이므로, **activation memory가 dataset 크기에도 좌우**된다(작은 값으로 고정된 mini-batch를 쓰면 activation memory가 dataset 크기와 무관할 수 있는 것과 대비).
- **이번 주를 여는 두 가지 핵심 질문**: (1) 원하는 mini-batch/dataset 크기가 GPU의 한정된 VRAM 때문에 **메모리 문제**를 일으키면 어떻게 하는가? (2) 원하는 mini-batch/dataset 크기가 GPU의 한정된 연산 성능 때문에 **지연 문제**를 일으키면 어떻게 하는가? → **Data parallelism이 이 두 문제(메모리·지연)를 완화하는 해법**으로 제시된다.

### 33. 산업 사례: DeepSeek의 병렬화 조합

- DeepSeek의 기술 보고서(DeepSeek-V3, 약 1년 6개월 전 공개, 매우 많이 인용됨)를 예로 들어, 오늘 배울 data parallelism이 실제 산업에서 쓰이고 있음을 보여줌.
- **학습(training) 프레임워크**: DeepSeek-V3는 **16-way pipeline parallelism**(다음 주 강의 주제), **64-way expert parallelism**(중간고사 전 강의 주제), 그리고 **data parallelism**(이번 주 주제)을 함께 사용.
- **추론(inference)·배포(deployment) 전략**: **tensor parallelism**(앞으로 3주 내에 다룰 주제), data parallelism, expert parallelism을 함께 사용.
- **핵심 메시지**: 서로 다른 병렬화 기법들은 **독립적인 대안이 아니라 함께 결합해서 쓰인다.** 연구 단계에서는 개별 기법(DP 또는 pipeline parallelism 등)만 따로 연구하는 경우가 많지만, 실제로 좋은 성능의 모델을 학습시키려면 **여러 병렬화 기법을 동시에 결합**하는 것이 일반적이다. 최근 DeepSeek 모델들도 data parallelism을 채택했는데, 이는 data parallelism이 갖는 여러 장점 때문(장점은 이번 주와 앞으로 계속 다룰 예정이라고 예고).

### 34. Data Parallelism 개요(Outline)

이번 주(및 금요일까지)에 다룰 순서:
1. **작동 방식(how it works)** — 학습 과정이 어떻게 생겼는지(mini-batch/full-batch gradient descent를 알면 이해하기 쉬움).
2. **Centralized training과의 비교** — 정말 같은 결과로 수렴하는가?
3. **Memory와 delay** 분석.
4. **다른 optimizer로의 확장** — 단순 SGD는 느릴 수 있으므로, SGD with Momentum이나 Adam과 data parallelism을 어떻게 통합하는지.
5. **(금요일)** **Fully decentralized 설정** — 중앙 parameter server 없이 data parallelism을 적용하는 방식(이번 시간엔 아직 배경 개념이 없어 이름만 예고됨).

이번 노트(Day 5)에서는 위 중 **1(작동 방식)** 과 **2(centralized training과의 비교, 도입부만)** 를 다룬다 — 나머지는 시간 부족으로 금요일로 이월(§40 참고).

### 35. Data Parallelism 설정 — 데이터셋 분할과 모델 복제

- **기본 설정은 centralized training과 동일**: 특정 모델 + 특정 목표 데이터셋. 차이는 이제 **여러 머신**을 쓸 수 있다는 것 — 단일 머신에 국한될 필요가 없음.
- **핵심 아이디어 — 데이터셋 분할**: 데이터셋을 여러 머신에 나눠 분배한다. 예시(슬라이드): 데이터 샘플 3,000개가 있으면 처음 1,000개는 GPU 1에, 다음 1,000개는 GPU 2에, … 이런 식으로 할당 → **각 GPU는 데이터셋의 특정 부분(shard)만 담당**.
- **할당은 학습 내내 고정**: 한 번 GPU 1에 파란색 데이터 뭉치, GPU 2에 초록색 데이터 뭉치가 할당되면, 학습이 끝날 때까지 그 배정은 바뀌지 않는다.
- **모델은 나누지 않는다(pure data parallelism)**: 원본 모델을 **그대로 복사**해서 모든 GPU에 배치한다. 즉 데이터셋은 여러 GPU에 분산되지만, **모든 GPU가 학습 내내 동일한 모델을 공유**한다.
- **왜 모델을 나누지 않는가**: (1) 데이터와 모델을 동시에 나누면 너무 복잡해지므로, data parallelism과 model parallelism을 **따로 연구**하는 것이 일반적. (2) (§33에서 봤듯) 실제 기업들은 data parallelism을 다른 model parallelism 전략과 **결합**해서 쓰기 때문에, "모델을 절대 안 나눈다"는 게 필수 조건은 아니다 — 단, **기본(basic) data parallelism**에서는 모델을 나누지 않는 것이 정의.
- **미리 짚어둘 함의**: 모델을 그대로 복제하므로, data parallelism은 **parameter memory를 줄여주지 않을 수도 있다**(모델 자체 크기는 안 바뀌므로). 이 부분의 실제 내용(어떤 조건에서 줄어드는지)은 이후 다른 optimizer들을 다룰 때(금요일 이후) 자세히 설명 예정.
- **"data" parallelism이라는 이름의 이유**: 각 GPU는 자신에게 할당된 데이터로 gradient를 계산하고, **여러 GPU가 같은 시간대(time step)에 서로 다른 데이터 샘플을 동시에 처리**한다 — 즉 데이터에 대한 연산을 여러 GPU로 병렬화하는 것.

### 36. 두 핵심 구성요소: Worker Node와 Parameter Server

- **Worker node**: data parallelism 과정에 존재하는 여러 노드 중 하나로, **GPU로 볼 수 있다.** 여러 GPU에 데이터 샘플을 나눠주고, 각 worker node의 역할은 **자신에게 할당된 데이터셋을 기반으로 gradient를 계산하는 것.**
- **왜 worker node만으로는 부족한가**: 학습의 핵심은 "gradient 계산 → 모델 업데이트"인데, 여러 노드가 각각 **자신만의 gradient**를 만들어내므로, 서로 다른 GPU들이 만든 gradient들을 반영해 **하나의 모델**을 어떻게 업데이트할지가 문제가 된다.
- **Parameter server**: 여러 노드/GPU에서 계산된 gradient들을 **취합(aggregate)**하는 중앙 구성요소. 역할: worker node들로부터 gradient를 받아서, 취합된 결과(업데이트된 모델)를 다시 돌려보낸다.
- **Parameter server로 무엇을 쓸 수 있나**: 데이터센터 환경에서 worker node로 GPU들을 쓰고, parameter server로는 별도의 노드(CPU든 다른 GPU든) 아무거나 쓸 수 있다 — 하드웨어 종류 자체는 중요하지 않다. 다만 **parameter server가 GPU들로부터 지리적으로 너무 멀면 통신 지연(communication delay)이 발생**하므로 너무 멀리 두면 안 된다. 실무적으로는 가용한 노드들 중 하나를 parameter server로, 나머지를 worker node로 지정하는 식으로 구성한다.

### 37. 동기식(synchronous) 학습 과정 — Parameter Server 기반 훈련 루프

전체 데이터셋 $D$를 worker node 수만큼(예시에서는 4개 노드) 나눈 $D_1, D_2, D_3, D_4$가 각각 worker 1~4에 배정되어 있다고 하자. **$D_1 \cup D_2 \cup D_3 \cup D_4 = D$(합집합이 전체 데이터셋)이고 서로 겹치지 않는다(no overlap)**. 이 배정은 학습 내내 고정된다.

1. **모델 초기화 + 다운로드**: centralized training과 마찬가지로 첫 단계는 모델을 무작위 분포에 따라 초기화($W_0$)하는 것. 여기서는 이 무작위 초기화된 모델을 **모든 worker 머신에 전송(download)**해야 한다는 추가 과정이 붙는다 — centralized training 대비 **통신(communication)**이 추가되는 첫 지점.
2. **각 worker의 gradient 계산**: 모든 머신이 (일단은) **full-batch gradient descent**를 쓴다고 가정 — 즉 자신에게 할당된 데이터 전체를 사용해 gradient 하나를 계산한다. Worker 1은 자신의 데이터 $D_1$으로 $G_1$을, worker 2는 $D_2$로 $G_2$를 계산하는 식으로 **worker 1~4가 각각 $G_1, G_2, G_3, G_4$를 계산**(정의 자체는 일반적인 gradient 정의와 동일). **핵심**: 모든 worker가 사용하는 데이터는 서로 다르지만, **모델은 전부 동일**(parameter server로부터 똑같이 받은 모델)해야 한다 — 하나의 모델을 모든 데이터에 대해 잘 동작하도록 최적화하는 것이 목표이므로, 애초에 받은 모델이 서로 다르면 말이 안 됨.
3. **Gradient 업로드 + 취합(aggregation)**: 각 worker가 계산한 gradient를 parameter server로 업로드하면, server가 이를 취합한다. **워크드 예시(기호 단계)**: 4개 데이터셋이 모두 **동일한 샘플 개수**를 갖는다고 가정하면, 취합된 gradient는
   $$G = \frac{G_1+G_2+G_3+G_4}{4}$$
   (4개 gradient의 평균)이다. 이 $G$는 4개 데이터셋 전부를 반영하는 방향, 즉 "이 4개 데이터셋 모두에서 잘 동작하도록 모델을 최적화하는 방향"으로 해석된다. *(강의에서 실제 숫자 값은 제시되지 않았고 $G_1$–$G_4$는 기호로만 다뤄졌다 — 평균을 취하는 절차 자체가 핵심.)*
   - **통신 비용 노트**: gradient의 크기는 (전체 파라미터를 업데이트한다고 가정하면) **모델 크기와 동일**하므로 이 업로드 단계의 통신 비용이 상당히 클 수 있다. *(강의 원문은 "모델 크기가 매우 커지면 이 통신 부담이 매우 낮아진다"고 말했는데, 직전 문맥("통신 비용이 매우 크다")과 앞뒤가 맞지 않는다 — 모델이 커질수록 통신 부담이 커진다는 취지의 구두 실수(mis-speak)로 보이나, 원문 그대로 기록해둔다.)*
4. **모델 업데이트**: parameter server가 취합된 gradient $G$로 모델을 업데이트한다. Full-batch gradient descent를 쓴다면 $W_1 = W_0 - \eta G$ 형태로 업데이트(단순 gradient descent 업데이트 식에 취합된 gradient를 대입). SGD with Momentum, Adam 등 다른 optimizer와의 통합은 **금요일에 상세히 다룰 예정** — 오늘은 단순 full-batch GD만 가정.
5. **업데이트된 모델을 다시 broadcast**: parameter server가 $W_1$을 모든 worker node에 다시 전송한다.
6. **반복**: 2~5단계(gradient 계산 → 업로드/취합 → 모델 업데이트 → broadcast)를 만족스러운 성능을 얻을 때까지 여러 **training round**에 걸쳐 반복 — centralized training에서 여러 epoch에 걸쳐 반복하는 것과 같은 철학. 예: 3라운드를 하기로 하면 $W_0 \to W_1 \to W_2 \to W_T$ 순으로 모델을 얻는다.

**수업 중 Q&A(이 훈련 루프에 대한 질문들)**:
- **Q: gradient를 평균 내서 업데이트하는 것만으로 모든 머신의 데이터를 "정확히" 반영하기에 충분한가?** A: **그렇다** — 단, (a) parameter server에서 모델이 업데이트되고, (b) 모든 머신이 **동일한 개수의 데이터 샘플**을 갖는다는 가정 하에서. 이것이 centralized training의 학습 과정과 정확히 같은지는 다음 절(§40)에서 다루기 시작하지만, **이번 시간에는 결론까지 가지 못했다.**
- **Q: 모델을 여러 머신에 전송(broadcast)할 때, 머신 개수가 지연에 영향을 주는가?** A: **유선(wireline) 통신 기반 데이터센터**에서는 정확히 비례하지는 않아도 머신이 많아질수록 지연이 **늘어난다**(통신을 완전히 병렬로 할 수 없기 때문) — 머신 개수를 무시할 수 없다. 반면 **무선(wireless) 통신**(많은 실제 사례에 해당)에서는 정보를 방송(broadcast)하면 모든 머신이 동시에 수신할 수 있으므로 **머신 개수에 크게 의존하지 않는다.**
- **Q: 모델 크기 자체가 매우 커지는 문제는 data parallelism이 해결하는가?** A: **아니다** — data parallelism은 대규모 모델 문제를 다루지 못한다. 그래서 실무에서는 data parallelism을 **pipeline parallelism이나 expert parallelism과 결합**해서 두 문제를 동시에 해결한다(data parallelism의 목표는 어디까지나 데이터셋 문제이지 모델 크기 문제가 아니라는 점의 재확인).
- **Q: 여러 머신의 계산이 항상 동시에 끝난다고 보장할 수 있는가?** A: **아니다** — 머신마다 계산 능력이 다르거나 동시에 다른 작업을 하고 있을 수 있어 완료 시간(completion time)에 큰 차이가 날 수 있다. 이 이슈는 강의 노트의 **delay 절**에서 다룰 예정이며, **synchronous distributed learning**과 **asynchronous distributed learning**을 구분해서 고려해야 하는 이유이기도 하다 — 대략 **10주차 전후**(일정은 바뀔 수 있음)에, 첫 강의에서 이미 보여준 course overview 상의 예고된 주제로 다시 등장할 예정.

### 38. "A Simpler Illustration" — 같은 과정의 재정리

- 위 §37과 동일한 과정을 더 단순한 그림으로 다시 요약: 전체 학습 데이터셋을 가진 **중앙 parameter server**에서 시작 → 데이터셋을 여러 머신에 분산 → 현재 모델을 모든 노드에 전송(모델 다운로드) → 각 노드가 자신에게 할당된 데이터로 gradient 계산(서로 다른 데이터셋 → 서로 다른 gradient) → 각 gradient를 parameter server로 전송 → server가 취합해서 모델 업데이트 → 좋은 성능을 얻을 때까지 반복.
- 이 시점(강의 진행 기준)까지 **아직 다루지 않은 것**: (1) 이 학습 과정이 centralized training과 **정확히 같은 결과**를 내는지, (2) **memory·delay** 분석, (3) 이 과정을 **다른 optimizer**로 확장하는 방법 — 모두 이후 강의(주로 금요일)로 이월.

### 39. 통신 병목과 Fully Decentralized 설정 예고

- 오늘 나온 질문들과 연결지어: 머신 수가 많아지면 **모델 전송(broadcast)** 부담과 **gradient 업로드** 통신 부담이 둘 다 커지고, 이는 결국 **parameter server 자체에서 심각한 병목(bottleneck)**을 일으킨다.
- 이를 완화하기 위해 연구된 것이 **fully decentralized 설정** — 중앙 parameter server 없이 data parallelism을 적용하는 방식(모든 머신에 연결된 중앙 서버가 존재하지 않음). **금요일에 다룰 예정.**
- 오늘 나온 질문들(머신 수·통신 지연, 완료 시간 불일치 등)은 대부분 **앞으로 이어질 강의들에서** 다뤄질 것이라고 명시적으로 언급되었다.

### 40. Comparison with Centralized Training — 도입부만 진행, 다음 시간(금요일)으로 이월

- 이 절이 답하려는 질문: **data parallelism의 학습 과정이 뭔가를 보장하는가?** — 임의의(arbitrary) 모델로 수렴하는 것인지, 아니면 실제로 centralized training과 **동일한 학습 과정**을 따르는 것인지.
- 비교의 기준점으로 "Deep Learning Basics" 강의 노트 **26페이지**에 있던 centralized training의 학습 과정을 다시 가져옴: $W_0$를 무작위 초기화한 뒤, 여러 epoch/iteration에 걸쳐 학습 — **매 iteration마다 데이터셋 $D$ 전체를 사용해 gradient를 계산**하고 모델을 업데이트하는 과정을 반복($T$ = iteration index). 여기서는 **full-batch gradient descent**를 가정하므로 표기에 $N$(worker 수)이 등장하지 않는다.
- Data parallelism 쪽에서는 이 위에 **추가적인 과정**이 붙는다고 언급하며 새 파라미터 **$N$(worker node 개수)**을 도입: 모든 worker node가 parameter server로부터 **동일한 모델**을 받았기 때문에, 이후 **모든 worker가 병렬로 gradient를 계산하는 과정**이 추가된다는 점까지만 언급되었다.
- **여기서 시간 종료(t=2772, 11시)**: 교수가 "이 슬라이드부터는 금요일에 이야기하겠다"고 명시적으로 말하며 강의를 마쳤다. 즉 **centralized training과의 실제 비교(수렴 결과가 같은지에 대한 증명/설명)는 이번 시간에 완료되지 않았고, 다음 시간(금요일)으로 명시적으로 이월**되었다. 마찬가지로 §34 outline 중 memory/delay 분석, 다른 optimizer로의 확장, fully decentralized 설정도 전부 금요일 이후 몫으로 남았다.
