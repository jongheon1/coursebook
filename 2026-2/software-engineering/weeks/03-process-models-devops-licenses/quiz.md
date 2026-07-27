# Week 3 — Active Recall Quiz

먼저 답을 소리 내어 말한 뒤 펼쳐서 확인한다. 답의 핵심 용어는 영어를 유지한다.

---

**Q1.** Software process 의 4개 근본 activity 는? Process model 은 무엇의 표현인가?

<details><summary>답</summary>
Specification, development, validation, evolution. Process model 은 이 activity 들의 배열과 인터페이스에 대한 추상적 표현 — plan-driven vs agile 은 산출물을 언제 동결하는가의 스펙트럼이다.
</details>

**Q2.** Royce (1970) 가 순차 모델에 대해 실제로 한 말은? 그가 제안한 보완 중 두 가지는?

<details><summary>답</summary>
"I believe in this concept, but the implementation described above is risky and invites failure" — 테스트가 마지막이라 설계 결함이 최대 비용 시점에 드러나기 때문. 보완: "do it twice" (버리는 pilot = prototype 의 원형), 고객의 공식 개입 (on-site customer 의 원형), preliminary design 우선, 테스트 계획·통제, 문서화. waterfall 이라는 이름은 후대의 것.
</details>

**Q3.** Waterfall 이 여전히 적합한 세 가지 상황 (Sommerville) 은?

<details><summary>답</summary>
(1) Embedded systems — 하드웨어 인터페이스가 비유연하므로 spec 동결이 현실적. (2) Critical systems — spec·설계 문서에 대한 안전성 분석이 인증 요건이라 안정된 spec 이 전제. (3) 여러 회사가 나눠 만드는 대형 시스템 — 동결된 인터페이스 spec 이 조직 간 조정 계약.
</details>

**Q4.** Incremental development 의 두 가지 실패 모드는?

<details><summary>답</summary>
(1) Process 비가시성 — 단계 산출물(문서)이 없어 진행도 측정이 어렵고, 증분마다 문서를 만들면 속도 이점이 죽는다. (2) Architecture erosion — 새 증분을 기존 구조에 우겨넣는 것이 국소적으로 항상 싸서 구조가 열화; 정기적 refactoring 투자 없이는 변경 비용이 누적 상승.
</details>

**Q5.** Spiral model 의 4 사분면과 "risk-driven" 의 의미는?

<details><summary>답</summary>
① determine objectives/alternatives/constraints ② evaluate alternatives; identify & resolve risks ③ develop & verify next-level product ④ plan next phases. Risk-driven = 다음에 수행할 activity (prototype? 벤치마크? 그냥 진행?) 를 단계 순서가 아니라 현재 지배적 리스크가 결정한다 — waterfall·prototyping 을 특수 케이스로 포함하는 process generator (Boehm 1988).
</details>

**Q6.** Risk exposure 와 risk reduction leverage 의 식은?

<details><summary>답</summary>
$RE = P(UO) \times L(UO)$ — 불만족 결과의 확률 × 손실. $RRL = (RE_{before} - RE_{after}) / \text{cost of reduction}$ — 1 보다 크면 리스크 완화 activity (prototype 등) 투자가 정당화된다 (Boehm 1991).
</details>

**Q7.** Agile Manifesto 4 values 를 원문으로. 마지막 단서 문장은 왜 중요한가?

<details><summary>답</summary>
Individuals and interactions over processes and tools / Working software over comprehensive documentation / Customer collaboration over contract negotiation / Responding to change over following a plan. 단서: "while there is value in the items on the right, we value the items on the left more" — agile 은 문서·계획의 폐지가 아니라 우선순위 재배열.
</details>

**Q8.** XP practices 를 5개 이상 나열하고, cherry-picking 이 왜 위험한지 예를 들라.

<details><summary>답</summary>
Small releases, test-first development (TDD), refactoring, pair programming, collective ownership, continuous integration, simple design, sustainable pace, on-site customer, incremental planning. 상호 지지 구조라서: small releases 만 도입하고 TDD·CI 를 빼면 릴리스마다 수동 회귀 검증이 병목이 되어 품질 붕괴; refactoring 없이 증분만 쌓으면 architecture erosion; 테스트 없는 collective ownership 은 혼란.
</details>

**Q9.** Scrum 의 3 accountabilities 와 각자의 배타적 권한, 5 events 와 timebox, 3 artifacts 와 commitments 는?

<details><summary>답</summary>
Accountabilities: Product Owner — Product Backlog 의 내용·순서 단독 결정 (what). Scrum Master — Scrum process 의 효과에 책임, 지휘 권한 없이 팀과 조직에 봉사하는 "true leader who serves" (2020판이 2017판의 servant-leader 를 대체한 표현). Developers — 어떻게 만들지 단독 결정 (self-managing), Sprint 마다 usable Increment 책임. Events: the Sprint (≤1개월), Sprint Planning (≤8h), Daily Scrum (15분), Sprint Review (≤4h), Sprint Retrospective (≤3h). Artifacts↔commitments: Product Backlog↔Product Goal, Sprint Backlog↔Sprint Goal, Increment↔Definition of Done.
</details>

**Q10.** Velocity 란 무엇이고 어디에 쓰면 안 되는가?

<details><summary>답</summary>
Sprint 당 완료한 추정 단위(story point)의 이동 평균 — 자기 팀의 capacity 예측용 (다음 Sprint 용량, backlog 소진 예측). 팀 간 비교·성과 평가에 쓰면 point 인플레이션으로 지표가 오염된다 (Goodhart's law). Scrum Guide 에는 없는 보조 practice.
</details>

**Q11.** Boehm & Turner 의 plan-driven vs agile 5 factors 는?

<details><summary>답</summary>
Size (대규모→plan), criticality (인명·거액→plan), dynamism (요구 변경률 높음→agile), personnel (시니어 비율 높음→agile), culture (자율 선호→agile / 절차 선호→plan). 결론은 이분법이 아니라 시스템 부위별 혼합의 위치 선정.
</details>

**Q12.** Dev 와 ops 의 incentive 충돌 구조와 DevOps 의 해법 논리는?

<details><summary>답</summary>
Dev 성과 = 변경(기능 출시), ops 성과 = 무변경(안정) — 그런데 장애 최대 원인이 변경이라 ops 는 관문을 쌓고, dev 는 변경을 크게 묶고, 큰 배치는 더 자주 실패하는 악순환 ("wall of confusion"). DevOps: 만든 사람이 운영까지 책임 ("you build it, you run it"), 전면 자동화, 작은 배치·잦은 배포 — 배치 크기가 줄면 1회당 실패 확률·격리 비용·복구 시간이 모두 준다.
</details>

**Q13.** CI 의 정의는? "CI 서버가 있다 ≠ CI 를 한다" 인 이유는?

<details><summary>답</summary>
전원이 최소 하루 1회 mainline 에 통합하고, 모든 통합이 자동화된 self-testing build 로 검증되는 **행동** (Fowler). 장수 feature branch 에서 작업하면 서버가 있어도 통합 주기는 branch 수명이므로 CI 위반. 부속 규율: 깨진 빌드 즉시 수리 최우선, 빌드 10분 이내.
</details>

**Q14.** Deployment pipeline 4단계와 각 단계 실패의 의미는?

<details><summary>답</summary>
Commit stage (compile·unit test·lint, ~10분) 실패 = 코드 단위 논리·규약 오류. Acceptance stage (integration·acceptance test) 실패 = 조립이 틀림 — 컴포넌트 간 계약 위반. Staging (prod 유사 환경) 실패 = 환경 가정이 틀림 (데이터 규모, 의존 서비스). Production 실패 = 현실이 모든 가정과 다름 — 소거 불가하므로 blast radius (canary) 와 복구 시간 (rollback) 을 설계 (Humble & Farley).
</details>

**Q15.** Continuous delivery 와 continuous deployment 의 차이는?

<details><summary>답</summary>
Delivery = 모든 변경이 파이프라인을 통과해 언제든 배포 가능한 상태 유지, 실제 배포는 사람의 결정. Deployment = 통과한 변경이 자동으로 production 까지 나감. Deployment ⊃ delivery.
</details>

**Q16.** Blue-green vs canary vs feature flag — 각각 무엇을 분리/제한하는가?

<details><summary>답</summary>
Blue-green: 환경 2벌 + 라우터 전환 — 롤백을 초 단위로 (비용: 인프라 2배 + DB schema 는 2벌이 아니라 expand–contract 마이그레이션 필요). Canary: 트래픽 1%→점진 확대 + 지표 비교 — 실패의 blast radius 제한. Feature flag: deploy (코드가 prod 에) 와 release (사용자가 겪음) 의 분리 — dark launch 가능, 비용은 flag 조합 테스트 공간과 죽은 flag 부채.
</details>

**Q17.** DORA 4 key metrics 를 throughput/stability 로 나눠 정의하라. Accelerate 의 핵심 발견은?

<details><summary>답</summary>
Throughput: deployment frequency (배포 빈도), lead time for changes (commit→production 시간). Stability: change failure rate (배포 중 장애 유발 비율), time to restore service (장애→복구). 발견: 4개는 trade-off 가 아니라 co-vary — 2017 조사에서 high performer 는 배포 46배, lead time 440배, MTTR 170배, CFR 1/5. 메커니즘은 작은 배치 크기.
</details>

**Q18.** IaC 의 3 원리 (declarative/idempotent, snowflake 제거, drift 방어) 를 설명하라.

<details><summary>답</summary>
(1) 목표 상태를 선언하면 도구가 차이만 적용, 재실행해도 결과 동일 (idempotence) — 실패 후 재시도 안전. (2) 수동 패치 누적으로 재현 불가능한 snowflake server 를 재생성 가능한 산출물로 대체 — 고치지 말고 갈아 끼움 (phoenix, pets→cattle). (3) 정의 파일이 유일한 진실이므로 수동 변경에 의한 configuration drift 를 탐지·수렴 가능.
</details>

**Q19.** NIST 의 cloud 5 essential characteristics, 3 service models, 4 deployment models 은?

<details><summary>답</summary>
5: on-demand self-service, broad network access, resource pooling, rapid elasticity, measured service. 3: IaaS/PaaS/SaaS. 4: public/private/community/hybrid (SP 800-145). IaaS 는 OS 부터 사용자 책임, PaaS 는 앱+데이터만, FaaS (NIST 이후 등장) 는 함수 코드만, SaaS 는 데이터·접근 설정만.
</details>

**Q20.** Serverless (FaaS) 가 지불하는 비용 4가지는?

<details><summary>답</summary>
(1) Cold start — 샌드박스+런타임+코드 초기화가 p99 직격; provisioned concurrency 로 막으면 상시 비용 부활. (2) Stateless 강제 + 실행 시간 상한 (Lambda 15분) — 상태·함수 간 데이터가 스토리지/네트워크 경유. (3) Vendor lock-in — 이벤트 소스·권한 배선이 provider 전용. (4) 비용 교차 — 평탄한 고부하에선 예약 VM 보다 비쌈; serverless 는 "항상 싸다"가 아니라 "유휴에 과금 안 한다".
</details>

**Q21.** 12-factor 의 config, build/release/run, processes 원칙은?

<details><summary>답</summary>
III Config: 설정은 환경 변수로 — "코드베이스를 통째로 공개해도 credential 유출이 없는가" 리트머스. V Build/release/run: 불변 artifact (build) + config = release (append-only, 롤백 = 이전 release 재실행); 환경마다 재빌드하면 테스트한 것 ≠ 배포한 것. VI Processes: stateless·share-nothing — sticky session 은 위반, 상태는 backing service 로 (W5 horizontal scaling 의 전제).
</details>

**Q22.** Copyleft 의 trigger 는 무엇이고 trigger 가 **아닌** 것 4가지는? GPLv3 와 AGPLv3 는 여기에 무엇을 추가했나?

<details><summary>답</summary>
Trigger = conveying (배포 — 타인이 복제본을 받을 수 있게 하는 것). Trigger 아님: 실행/사용 (프로그램 출력물도 라이선스 밖), 조직 내부 사용, 수정 후 비공개 사용, SaaS 제공 (ASP loophole). GPLv3 가 v2 에 추가: 명시적 patent grant (§11), anti-tivoization (User Product 에는 수정판을 설치·실행할 Installation Information 제공 — TiVo 의 서명 잠금 대응), Apache-2.0 호환 (§7 additional permissions). AGPLv3 §13: 수정한 버전을 네트워크 서버로 제공하면 그 사용자들에게 수정판 소스 제공 의무 — "배포" 에 "네트워크 서비스" trigger 추가 (ASP loophole 봉쇄, 무수정 사용은 미발동). Google 은 사내 AGPL 사용을 금지.
</details>

**Q23.** MIT 와 Apache-2.0 의 실질적 차이는? 라이선스 호환성의 방향 규칙과 대표 함정 두 개는?

<details><summary>답</summary>
Apache-2.0 은 명시적 patent grant (§3: contributor 의 기여가 읽는 특허의 무상 실시권) + 특허 보복 조항 (특허 소송 제기 시 실시권 소멸) + NOTICE·변경 표시 의무. MIT 는 특허 무언급 (묵시 논쟁만) — 특허 리스크가 있는 도메인에선 Apache-2.0. 호환성: 약한 조건 → 강한 조건으로만 결합 가능하고 결과물은 강한 쪽을 따른다 (MIT→Apache-2.0→GPLv3→AGPLv3). 함정: (1) Apache-2.0 은 GPLv3 와 호환이지만 GPLv2-only 와는 비호환 (특허 보복 조항이 v2 의 "추가 제한" 금지에 저촉). (2) GPLv2-only ↮ GPLv3 상호 비호환 — "or later" 표기만 상향 가능 (Linux kernel 이 GPLv2-only 라 GPLv3 코드 수용 불가).
</details>

**Q24.** LGPL 이 proprietary 앱에 허용하는 것과 요구하는 두 조건은?

<details><summary>답</summary>
LGPL 라이브러리에 링크하는 앱은 proprietary 로 남을 수 있다. 조건: (1) 라이브러리 자체의 수정분은 LGPL 로 공개, (2) 사용자가 라이브러리를 교체(relink)할 수 있게 보장 — 동적 링크를 쓰거나 object 파일 제공 (glibc 위의 proprietary 소프트웨어가 성립하는 이유).
</details>

**Q25.** SPDX expression `MIT OR Apache-2.0` 과 `GPL-2.0-only WITH Classpath-exception-2.0` 의 의미는?

<details><summary>답</summary>
OR = 수취인이 둘 중 하나를 선택 (disjunctive). WITH = 본 라이선스에 예외 결합 — Classpath exception 은 이 라이브러리에 "링크만 하는" 프로그램을 GPL 의무에서 제외 (OpenJDK: 모든 Java 앱이 GPL 이 되는 것을 방지). SPDX 는 Linux Foundation 의 라이선스 식별자·식 표준 (ISO/IEC 5962) 이며 SBOM 포맷이기도 하다.
</details>

---

## Anki TSV

```tsv
Software process 의 4개 근본 activity 는?	Specification, development, validation, evolution — process model 은 이들의 배열·인터페이스의 추상적 표현
Royce 1970 이 순차 모델에 대해 실제로 한 말은?	"the implementation described above is risky and invites failure" — 보완으로 do it twice(prototype), 고객 개입 등을 제안. waterfall 창시자가 아니라 최초의 비판자
Waterfall 이 적합한 3 상황 (Sommerville)?	Embedded systems (HW 비유연), critical systems (spec 안전성 분석·인증), 다자간 대형 개발 (동결 spec 이 조정 계약)
Incremental development 의 2 실패 모드?	Process 비가시성 (문서 산출물 부재), architecture erosion (refactoring 투자 없이는 구조 열화로 변경 비용 상승)
Spiral model 의 4 사분면?	① objectives/alternatives/constraints ② risk 식별·해소 ③ develop & verify ④ plan next phases — risk-driven process generator (Boehm 1988)
Risk exposure 와 risk reduction leverage 식은?	RE = P(UO) × L(UO); RRL = (RE_before − RE_after) / cost — RRL > 1 이면 완화 투자 정당화
Agile Manifesto 4 values?	Individuals and interactions over processes and tools / Working software over comprehensive documentation / Customer collaboration over contract negotiation / Responding to change over following a plan — 오른쪽도 가치 있음 (폐지 아님)
Working software is the primary measure of progress 는 어디 출처?	Agile Manifesto 12 principles (P7)
XP practices 5개 이상?	Small releases, TDD, refactoring, pair programming, collective ownership, CI, simple design, sustainable pace, on-site customer — 상호 지지 구조라 cherry-picking 위험
Scrum 3 accountabilities 와 배타 권한?	PO: backlog 내용·순서 단독 (what) / Scrum Master: process 책임, 지휘권 없음 / Developers: how 단독 결정, usable Increment 책임
Scrum 5 events 와 timebox?	Sprint(≤1개월), Sprint Planning(≤8h), Daily Scrum(15분), Sprint Review(≤4h), Sprint Retrospective(≤3h)
Scrum 3 artifacts 와 commitments?	Product Backlog↔Product Goal, Sprint Backlog↔Sprint Goal, Increment↔Definition of Done (2020 Scrum Guide)
Velocity 의 용도와 금기?	팀 자체 capacity 예측용 이동 평균 (story point/sprint). 팀 간 비교·성과 평가에 쓰면 Goodhart's law 로 오염. Scrum Guide 에는 없음
Boehm & Turner 5 factors?	Size, criticality, dynamism, personnel, culture — 클수록/치명적일수록/안정적일수록/주니어일수록/절차 선호일수록 plan-driven
Dev vs ops 갈등 구조는?	Dev 성과=변경, ops 성과=안정인데 장애 원인 1위가 변경 → 관문↑ → 배치 크기↑ → 실패율↑ 악순환 (wall of confusion). DevOps: 작은 배치 + you build it, you run it
CI 의 정의는?	전원이 최소 매일 mainline 에 통합 + 모든 통합을 자동 self-testing build 로 검증하는 행동 (Fowler). CI 서버 보유 ≠ CI
Deployment pipeline 4단계 실패의 의미?	Commit=코드 논리·규약 오류 / Acceptance=조립(계약) 위반 / Staging=환경 가정 오류 / Production=현실≠가정 → blast radius·복구 설계
Continuous delivery vs deployment?	Delivery=언제든 배포 가능 상태 유지(버튼은 사람), deployment=통과한 변경 자동 배포. deployment ⊃ delivery
Blue-green 의 함정은?	환경은 2벌이지만 DB schema 는 1벌 — 양쪽 버전과 호환되는 expand–contract 마이그레이션 필요. 롤백=라우터 전환
DORA 4 key metrics?	Throughput: deployment frequency, lead time for changes(commit→prod) / Stability: change failure rate, time to restore service
Accelerate 의 핵심 발견은?	Speed 와 stability 는 co-vary (trade-off 아님) — high performer: 배포 46×, lead time 440×, MTTR 170×, CFR 1/5 (2017). 메커니즘은 작은 배치
IaC 의 idempotence 가 주는 것은?	같은 정의를 반복 적용해도 결과 동일 → 실패 후 재실행 안전. 선언형 정의가 유일한 진실 → configuration drift 탐지·수렴
Snowflake vs phoenix server?	Snowflake: 수동 패치 누적으로 재현 불가 — 복구 불능·환경 불일치 원천. Phoenix: 정의에서 재생성 — 고치지 말고 갈아 끼운다 (pets→cattle)
NIST cloud 5 characteristics?	On-demand self-service, broad network access, resource pooling, rapid elasticity, measured service (SP 800-145)
NIST 4 deployment models?	Public, private (단일 조직 전용), community, hybrid (2+ 조합, cloud bursting)
IaaS/PaaS/FaaS/SaaS 사용자 책임 범위?	IaaS: OS 부터 위 전부(패치 포함) / PaaS: 앱+데이터 / FaaS: 함수 코드만 / SaaS: 데이터·접근 설정만
FaaS cold start 란?	유휴 후 첫 호출이 샌드박스 생성+런타임 초기화+코드 초기화를 겪는 지연 — p99 직격, provisioned concurrency 로 막으면 상시 비용 부활
Serverless 비용 구조의 본질은?	유휴에 과금하지 않음 — 스파이크/저트래픽에 유리, 평탄한 고부하에선 예약 VM 이 저렴 (교차점 존재)
12-factor Config 의 리트머스 테스트는?	지금 코드베이스를 통째로 오픈소스로 공개해도 credential 이 유출되지 않는가 — 설정은 환경 변수로
12-factor build/release/run 이 파이프라인에 주는 규칙은?	불변 build artifact + config = release (append-only). 환경마다 재빌드 금지 — 테스트한 것과 배포한 것의 동일성 보장
라이선스 없는 공개 코드의 법적 상태는?	All rights reserved — 저작권은 작성 즉시 자동 발생 (Berne), 복제·수정·배포는 배타적 권리라 명시 허락 없이는 사용 불가
Copyleft 의 trigger 는?	Conveying(배포). 실행·내부 사용·비공개 수정·SaaS 는 trigger 아님 — SaaS 를 잡는 건 AGPL §13 (수정 버전 조건)
MIT 대비 Apache-2.0 의 추가 사항?	명시적 patent grant(§3) + 특허 보복 조항(소송 시 실시권 소멸) + NOTICE·변경 표시. GPLv2 와는 비호환, GPLv3 와는 호환
LGPL 의 relink 조건이란?	Proprietary 앱이 LGPL 라이브러리를 쓰려면 사용자가 라이브러리를 교체할 수 있어야 함 (동적 링크 or object 파일 제공) + 라이브러리 수정분은 LGPL 공개
Static vs dynamic linking 논쟁의 현주소는?	Static=결합 저작물 이견 없음. Dynamic=FSF 는 결합으로 봄, 반론 존재, 정면 판례 없음 — 실무는 보수적으로 FSF 해석. LGPL 의 존재가 방증
별도 프로세스 실행(GPL FAQ)의 판단 기준은?	별도 주소 공간 + arm's length 통신(pipe/socket)이면 별개 저작물(aggregation), 내부 자료구조 공유하는 긴밀한 IPC 면 결합 — 기준은 통신의 친밀도
Classpath exception 이 하는 일은?	GPL-2.0 라이브러리에 링크만 하는 프로그램을 GPL 의무에서 제외 — OpenJDK 의 GPL-2.0-only WITH Classpath-exception-2.0, proprietary Java 앱 성립 근거
GPLv3 의 anti-tivoization 조항은?	User Product 로 배포 시 수정판을 설치·실행할 Installation Information 제공 의무 (§6) — 소스는 주되 서명 잠금으로 실행을 막는 것 금지
AGPL §13 의 정확한 trigger 는?	프로그램을 수정한 버전을 네트워크로 서비스하면, 원격 상호작용하는 사용자에게 수정판의 Corresponding Source 제공 의무 — 무수정 사용은 §13 미발동
GPLv2-only 와 GPLv3 를 한 저작물로 결합할 수 있는가?	불가 — 각자 자기 라이선스로만 배포를 요구해 동시 충족 불능. "GPL-2.0-or-later" 만 v3 로 상향 결합 가능 (Linux kernel 은 v2-only)
라이선스 호환성의 방향 규칙은?	약한 조건 → 강한 조건으로만 (MIT→Apache-2.0→GPLv3→AGPLv3), 결합물은 강한 쪽 라이선스를 따름. 역방향은 배포 불가 또는 전체가 강한 쪽으로
SSPL 사변 (MongoDB/Elastic/Redis) 의 교훈은?	SaaS 는 conveying 이 아니라 클라우드 벤더를 못 막음 → SSPL 전환 → OSI 불인정 + fork (OpenSearch, Valkey). 라이선스 변경은 이후 버전에만 적용 — 기존 permissive 사본으로 fork 가능
Dual licensing 의 전제 조건은?	저작권 전부 보유 (CLA 로 기여자 권리 집적) — 같은 코드를 copyleft 무료판 + 상용판으로 병행 판매 (Qt, MySQL, Ghostscript/Artifex)
미국 최초의 GPL 소송은?	Andersen v. Monsoon Multimedia (2007, BusyBox 펌웨어 소스 미제공) — 합의. 독일은 Welte v. D-Link (2006) 가 GPL 구속력 인정
Artifex v. Hancom (2017) 의 의의는?	GPL(AGPL) 위반을 저작권 침해에 더해 계약 위반으로도 다툴 수 있다고 판단 — dual licensing 모델의 법적 실효성 입증 (Ghostscript)
SPDX 란?	Linux Foundation 의 라이선스 식별자·expression 표준 (MIT OR Apache-2.0, X WITH exception; -only vs -or-later 구분). SPDX-License-Identifier 헤더, SBOM 포맷 (ISO/IEC 5962)
SBOM 이란?	Software Bill of Materials — 구성 컴포넌트·버전·라이선스의 기계 가독 인벤토리. 미 행정명령 14028 이후 조달 요건화
```
