# Week 01 Delta — 실제 강의 vs 예습 챕터(`weeks/01-course-overview/README.md`)

> 예습 챕터는 방학 중에 syllabus만으로 미리 써둔 것으로, scaling laws·memory wall·roofline·Amdahl's law·MFU 등 상당히 기술적인 내용까지 다룬다. 실제 Week 1 강의는 **오리엔테이션 성격이 강한 개론 강의**였고, 예습 챕터의 §1–6(정량적 내용)은 전혀 다루지 않았다. 그래서 이번 delta는 "정정"보다 "예습 챕터에 없던 운영/맥락 정보"와 "다음 주차 작성 시 참고할 프레이밍 차이"가 중심이다.

## Emphasized (교수가 강조했는데 예습 챕터에서 비중이 작았던 것)

- **"우리는 특정 알고리즘을 깊이 다루지 않고, 그 뒤의 공학적 이슈(GPU 메모리/연산/지연)를 다룬다"** — 이 과목의 정체성을 교수가 직접, 여러 번 강조. 예습 챕터의 `Why this matters` 섹션이 이미 이 톤(시스템/트레이드오프 중심)으로 쓰여 있어서 방향 자체는 맞았지만, "우리는 pre-training/fine-tuning 알고리즘 자체는 안 가르친다"는 명시적 선긋기는 챕터에 없다 — 이후 주차 챕터를 쓸 때도 "알고리즘 나열이 아니라 왜 이런 시스템 문제가 생기는가"에 계속 방점을 둘 근거로 인용 가능.
- **하드웨어(메모리 제약)를 다루는 것 자체가 이 과목의 차별점**이라는 언급 — "많은 공학 수업이 효율성/하드웨어를 무시하지만 우리는 다룬다". 예습 챕터 §4(하드웨어 기초)·§3(memory wall)이 정확히 이 위치에 있으므로 그대로 유지하되, 이번 강의의 이 발언을 §"Why this matters"나 도입부에 한 줄 인용으로 추가하면 좋음(★ 시험 신호라기보다 챕터의 자기정당화 근거).

## New (교재에 없던 내용 — 교수 자체 자료·운영 정보)

1. **Type 1 / Type 2 분산 학습이라는 상위 분류 용어.** 예습 챕터 §7.1은 data/pipeline/tensor/sequence/hybrid라는 "무엇을 쪼개는가" 축으로 분류하는데, 이는 전부 교수가 말한 **Type 1**(단일 조직 내 여러 GPU로 훈련 효율화)에 속한다. **Type 2**(federated learning, multi-user collaboration)는 별도 상위 카테고리로 W10-11에 대응. 이 Type 1/Type 2 용어 자체가 교수의 강의 전체를 관통하는 어휘이므로, W1 챕터 §7(과목 지도)이나 각 주차 도입부에서 "이 주차는 Type 1/Type 2 중 어디에 속하는가"를 명시하면 학생이 좌표를 잡기 쉬워짐. **W1 챕터 개정 시 반영 권장.**
2. **Edge-cloud collaboration을 inference의 한 축으로 명시.** 교수는 추론 분산을 (a) 멀티 GPU 서빙 + (b) local model vs. server model(edge-cloud 협업, 예측을 어디서 할지) 두 가지로 설명했다. 그런데 `00-roadmap.md`의 W12–13 서브토픽(quantization/pruning/distillation, KV cache/FlashAttention/PagedAttention/continuous batching/speculative decoding)에는 **edge-cloud collaboration이나 on-device inference 관련 항목이 전혀 없다.** 교수 본인이 Edge AI Lab을 운영하고 있어 이 주제를 실제로 다룰 가능성이 높다 — **로드맵 W12/W13 서브토픽에 on-device/edge-cloud 협업 추론(예: split computing, early-exit, cloud offloading)을 추가할지 검토 필요.** (지금은 추정이므로 실제 W12-13 강의에서 확인 후 로드맵 갱신 권장.)
3. **운영 정보 전반**: 교수 연락처(djh@yonsei.ac.kr, 공학관4 D720), TA 2명 이름·이메일, 강의실 D408, 요일/시간, 오피스아워 방식(이메일 약속), 출석/지각 환산 규정(지각3=결석1, 결석2까지 무감점, 초과시 결석당 -1점), 과제 지연 제출 페널티 구간(6/12/24시간), 과제 30%가 미니과제 1·2(각 15%)로 구성. → `syllabus.md`에 반영함(아래 "syllabus.md 갱신" 참고).
4. **시험 날짜가 슬라이드에 명시**: 중간 2025-10-24(금), 기말 2025-12-19(금), 각 11:00–12:50. **연도가 2025로 되어 있어 작년 슬라이드를 재사용했을 가능성이 있다.** `syllabus.md`에는 "확인 필요" 주석과 함께 넣었다 — LearnUs 공지로 실제 2026년 날짜 확인 후 정정 요망.
5. **교수 배경**: KAIST 수학·전자공학 학사, KAIST 석·박사, Purdue/KAIST 포닥, 2024.09부터 연세대 조교수, Edge AI Lab 운영. 연구분야(distributed/federated learning, trustworthy AI, personalization, resource-efficient learning)가 이 과목 프레이밍(특히 personalization, edge-cloud)과 직접 연결됨 — W10-11(federated), W12-13(inference) 챕터의 "왜 이 문제가 중요한가" 서술에 교수 본인 연구 맥락을 참고할 수 있음.

## Corrected (교재 서술과 다르거나 더 정확한 서술)

- 없음. 강의가 개론 수준이라 예습 챕터의 구체적 수치·정의(scaling laws exponent, memory wall 성장률, MFU 등)와 직접 충돌하는 지점이 없었다.
- 사소한 정정 1건(교재 아님, STT 오인식): 교수가 강의실을 "E408"이라 발음했으나 슬라이드 기준 정답은 **D408**. `notes.md`에 반영.

## syllabus.md 갱신

`syllabus.md`에 아래를 반영함 (이 파일은 커밋 대상):
- 담당교수 연락처·방·오피스아워, TA 2명
- 강의실/시간 (D408, 수 11:00–11:50 / 금 11:00–12:50)
- 평가 비중 세분화: 과제 30% = 미니과제 1(15%)+2(15%)
- 지각/결석 환산 규정, 과제 지연 제출 페널티
- 중간/기말고사 날짜 — **연도 확인 필요 주석 포함**

## 다음 액션 아이템

- [ ] LearnUs에서 2026-2학기 실제 중간/기말고사 날짜 확인 → `syllabus.md`의 "확인 필요" 주석 제거하고 정정.
- [ ] W12-13 로드맵에 edge-cloud/on-device inference 서브토픽 추가 여부, 실제 W12-13 강의 내용 확인 후 결정.
- [ ] W1 챕터(`weeks/01-course-overview/README.md`)에 Type 1/Type 2 상위 분류 용어를 §7 어딘가에 한 단락으로 추가할지 검토 (선택 사항 — 예습 챕터 자체 품질에는 문제 없음, 교수 어휘와의 정합성 목적).

---

# Day 2 Delta (2026-09-04) — 실제 강의 vs 예습 챕터(`weeks/02-memory-issues/README.md`)

> 비교 대상은 `weeks/02-memory-issues/README.md`("Recap of AI/ML & Memory Issues in Deep Learning") — 제목상 이번 강의와 가장 가까운 예습 챕터다. 다만 그 챕터는 **supervised learning의 ERM 정식화에서 바로 시작해서 computational graph·training memory anatomy(16 bytes/param)·activation memory 공식까지 대학원 입문 수준으로 깊이 들어가는 반면**, 실제 Day 2 강의는 뉴런 정의·비선형성이 왜 필요한지·forward propagation의 차원 계산·gradient descent의 1차원 직관 같은 **훨씬 더 기초적인 온보딩 수준**이었고 backpropagation 직전에서 멈췄다. 그래서 이번 delta도 "정정"보다는 "예습 챕터가 전제하고 건너뛴 기초를 실제 강의가 어떻게 채우는지"와 "두 문서의 깊이·범위 차이"가 중심이다.

## Emphasized (교수가 강조했는데 예습 챕터에서 비중이 작았던 것)

- **"기본 원리를 이해하지 않고 옵티마이저를 그냥 쓰는 습관은 장기적으로 도움이 안 된다"** — momentum, RMSProp, Adam을 설명할 때마다 반복적으로 나온 메시지(§15). 예습 챕터는 이미 그 수준을 전제하고 수식으로 바로 들어가므로 이 페다고지적 강조가 챕터에는 없다. W1 delta에서 이미 확인된 "이 교수는 원리 이해를 강조한다"는 성향과 일관됨 — 이후 주차 노트를 쓸 때도 참고할 만한 프레이밍.
- **optimizer별 GPU 메모리 요구량 차이(§16)** — SGD 2배, momentum 3배, Adam 그 이상이라는 강의의 직관적 설명은, 예습 챕터 §5.3("fp16 mixed-precision Adam의 파라미터당 16 bytes = weights 2 + grads 2 + opt states 12")의 훨씬 더 정밀한 바이트 단위 회계를 향한 첫 디딤돌이다. 강의는 "왜 optimizer 선택이 단일 GPU의 OOM 여부를 가르는가"를 정성적으로만 짚었을 뿐, 예습 챕터의 $16\Psi$ 유도·GPT-2 XL 24GB 계산까지는 가지 않았다. **후속 강의(들)에서 이 정성적 설명이 §5.3의 정량적 회계와 정확히 연결되는지 확인 필요.**

## New (예습 챕터에 아예 없던 내용 — 더 기초적인 온보딩)

이 항목들은 "정정"이 아니라, 예습 챕터가 전제 지식으로 건너뛴 것들이 실제 강의에서 어떻게 도출되는지를 보여준다.

1. **비선형 activation function이 필요한 이유의 직접 증명** (§9) — 비선형성을 제거하면 $W_3W_2W_1x$가 단일 행렬 $W'x$로 붕괴한다는 것을 직접 유도. 예습 챕터는 신경망 구조 자체를 아예 다루지 않고 바로 supervised learning 정식화로 들어가므로 이 내용이 전혀 없다 — DNN 챕터가 신설된다면 반드시 포함할 것.
2. **Forward propagation의 구체적 차원 계산 walkthrough** (§11) — $x \in \mathbb{R}^{784}$부터 시작해 $W_1$의 행/열 수를 뉴런 개수로 결정하는 손 계산. 예습 챕터 §2(backpropagation)는 이미 $\mathbf{a}^{[l]}, \mathbf{W}^{[l]}, \mathbf{z}^{[l]}$ 표기를 전제로 시작하므로, 그 표기 자체의 유래를 보여주는 이 walkthrough는 예습 챕터를 읽기 전 온보딩 자료로 유용.
3. **Cross-entropy loss의 5-class 예시 도출과 softmax의 "상대 격차 증폭" 설명** (§10, §12) — softmax가 지수함수를 쓰기 때문에(단순 정규화가 아니라) 확률로 변환된 뒤 클래스 간 격차가 커진다는 직관, 그리고 $L_k(w)=-\sum t_i\log y_i$가 one-hot 때문에 $-\log y_{q_k}$ 하나로 붕괴하는 유도. 예습 챕터는 loss를 "$\ell(f_w(x),y)$"로 추상화만 하고 cross-entropy의 구체적 형태·유도는 다루지 않는다.
4. **Gradient descent의 1차원 시각적 직관(공 굴리기 비유) + 기울기 크기가 step size에 반영되는 이유** (§13) — 예습 챕터 §1.1은 곧바로 $w_{t+1}=w_t-\eta\nabla L(w_t)$ 수식과 발산 조건($\eta<2/\lambda$)으로 들어가는데, 이 강의는 그 수식이 나오게 된 직관(기울기 부호로 방향, 기울기 크기로 보폭)을 먼저 손으로 짚었다. 온보딩용으로 참고 가능.
5. **RMSProp의 상세 설명** (§15) — 예습 챕터는 momentum과 Adam($m_t, v_t$)만 다루고 RMSProp 자체는 별도로 설명하지 않는다. 강의는 "왜 momentum만으로는 부족한가(global minimum까지 지나칠 수 있음) → RMSProp이 어떻게 이를 보완하는가(방향은 그대로, step size만 최근 gradient 크기에 따라 조절) → Adam이 왜 이 둘을 합친 것인가"라는 계보를 명확히 짚었다. 예습 챕터를 개정할 기회가 있다면 이 계보 설명(momentum → RMSProp → Adam)을 §3.2 도입부에 한 문단 추가할 가치가 있음.

## Corrected (교재 서술과 다르거나 더 정확한 서술)

- 없음 — 두 문서가 실제로 겹치는 지점(Adam의 $m_t, v_t$, bias correction)에서 서술이 상충하지 않는다. 강의는 그 지점을 훨씬 얕게(bias correction은 "지금은 안 중요하다"고 생략) 다뤘을 뿐이다.
- 사소한 정정 1건(교재 아님, STT 오인식): cross-entropy 예시에서 음성만으로는 "$-\log(0.02)$"처럼 들리지만, 슬라이드의 실제 softmax 출력값은 0.2이며 정답 계산은 $-\log(0.2)$다. `notes.md`/`notes.en.md`에 정정 반영함.

## 다음 액션 아이템 (Day 2)

- [ ] 다음 강의(예정: 수요일)에서 backpropagation·overfitting·batch normalization·CNN/attention 응용을 다루면, `notes.md`/`notes.en.md`에 이어서 추가하고 이 delta도 갱신할 것 — 특히 backpropagation 파트는 예습 챕터 §2("Backpropagation: computational graph와 chain rule")와 직접 비교 가능하므로 Corrected 항목이 나올 가능성이 있음.
- [ ] optimizer별 메모리 요구량에 대한 강의의 정성적 설명(§16)이 후속 강의에서 예습 챕터 §5.3의 $16\Psi$ 바이트 회계로 이어지는지 확인.
