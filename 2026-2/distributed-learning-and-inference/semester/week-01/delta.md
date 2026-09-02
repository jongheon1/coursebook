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
