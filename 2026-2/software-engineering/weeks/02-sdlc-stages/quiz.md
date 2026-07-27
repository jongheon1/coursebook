# Week 2 — Active Recall Quiz: SDLC Stages

먼저 답을 소리 내어 말한 뒤 펼쳐서 확인할 것. `/quiz` 스킬로 구술 세션 가능.

### Q1. Functional / non-functional requirement 의 정의와 경계가 흐려지는 대표 사례는? NFR 의 출처 기준 3분류는?

<details><summary>답</summary>
FR: 시스템이 제공해야 할 서비스 — 특정 입력·상황에 대한 반응의 서술 (하지 말아야 할 것 포함 가능). NFR: 서비스·기능에 걸리는 제약 (timing, 표준, 프로세스) — 시스템 전체에 걸리는 경우가 많음. 경계 사례: "권한 있는 사용자만 접근" 은 NFR (security constraint) 처럼 보이지만 상세화하면 인증 기능이라는 FR 들을 생성한다 — 요구사항은 서로 독립이 아니다. NFR 3분류: product (시스템 자체의 행동 제약 — performance, availability, security), organizational (개발 조직의 정책·표준), external (규제, 법률, 윤리).
</details>

### Q2. "The system should be easy to use" 가 requirement 로 실격인 이유와 처방은?

<details><summary>답</summary>
검증 불가능한 goal 이기 때문 — 충족 여부를 판정할 객관적 테스트를 쓸 수 없어 납품 후 분쟁의 원천이 된다. 처방: 측정 가능한 형태로 재작성 — 예: "2시간 교육 후 전 기능 사용 가능, 이후 시간당 조작 오류 ≤ 2회" (metric: training time, error rate).
</details>

### Q3. Availability 를 MTTF/MTTR 로 나타내는 식은? 이 식의 실무적 함의는?

<details><summary>답</summary>
$A = MTTF/(MTTF+MTTR)$. MTTR 이 분모에 있으므로 가용성은 "안 죽는 것" 뿐 아니라 "죽었을 때 빨리 복구하는 것" 으로도 올릴 수 있다.
</details>

### Q4. Requirements elicitation 이 어려운 이유 5가지는? 그중 interview 가 못 잡고 ethnography 가 잡는 요구 두 종류는?

<details><summary>답</summary>
(1) stakeholder 는 원하는 것을 막연하게만 알고 비현실적 요구를 함, (2) 자기 용어와 tacit knowledge 위에서 말함, (3) stakeholder 간 요구가 다양하고 충돌함, (4) 정치적·조직적 요인이 요구를 왜곡함, (5) 분석 중에도 환경이 변해 요구·우선순위·stakeholder 가 바뀜. Ethnography 가 잡는 것: (a) 공식 프로세스가 아니라 실제 일하는 방식에서 나오는 요구 (규정상 켜야 하는 경보를 꺼버리는 관제사), (b) 협업·상호 인지 (awareness) 에서 나오는 요구 (옆 섹터 부하를 보고 전략을 조정 → 인접 가시성 필요). tacit knowledge 는 "너무 당연해서 말하지 않는" 지식이라 인터뷰에서 안 나온다.
</details>

### Q5. User story 의 템플릿과 핵심 철학, INVEST 는?

<details><summary>답</summary>
"As a &lt;role&gt;, I want &lt;capability&gt;, so that &lt;benefit&gt;". 철학: 완결된 명세가 아니라 **대화의 placeholder** — 상세는 구현 직전 대화로 채우고 acceptance criteria 로 판정. INVEST: Independent, Negotiable, Valuable, Estimable, Small, Testable.
</details>

### Q6. Requirements validation 의 5가지 check 는?

<details><summary>답</summary>
Validity (진짜 필요 반영), consistency (내부 무충돌), completeness (의도한 전부 포함), realism (예산·기술 내 구현 가능), verifiability (요구별 판정 테스트 작성 가능). 기법: reviews, prototyping, test-case generation.
</details>

### Q7. Traceability 가 없으면 requirements change 에서 무엇이 불가능해지나?

<details><summary>답</summary>
Change analysis and costing — "이 요구를 바꾸면 어떤 설계·코드·테스트가 영향받는가" 의 파급 범위·비용 산정. 변경 수용 여부를 근거 있게 결정할 수 없게 된다.
</details>

### Q8. Sommerville 의 design process 4 활동은?

<details><summary>답</summary>
Architectural design (전체 구조·주요 component·관계), database design, interface design (component 간 계약 — 합의되면 병렬 독립 개발 가능), component selection and design (재사용 탐색 + 상세 설계).
</details>

### Q9. 왜 architecture 결정은 조기에, 신중히 해야 하나? (agile 에서도)

<details><summary>답</summary>
변경 비용의 비대칭: component refactoring 은 비교적 싸지만 architecture refactoring 은 대부분의 component 를 함께 수정해야 해서 비싸다. 그래서 agile 에서도 초기 up-front architecture 설계가 일반적으로 받아들여지고, architecture 의 incremental 개발은 대개 실패한다 (Sommerville ch6).
</details>

### Q10. Coupling 6종과 cohesion 7종을 각각 나쁜 것부터 나열하면?

<details><summary>답</summary>
Coupling: content (남의 내부에 직접 손댐) > common (전역 mutable 공유) > external (외부 형식·장치 상세를 여럿이 공유) > control (flag 로 내부 분기 지시) > stamp (필요 이상의 복합 구조 전달) > data (필요한 원소 데이터만 전달). Cohesion: coincidental (무관) < logical (같은 범주, flag 선택) < temporal (같은 시점 실행) < procedural (실행 순서) < communicational (같은 데이터) < sequential (출력→입력 사슬) < functional (단일 작업에 전원 기여).
</details>

### Q11. Logical cohesion 이 낮은 등급인 이유를 coupling 과 연결해 설명하면?

<details><summary>답</summary>
같은 "범주" 의 일을 flag 로 선택하게 묶으면, 호출자가 flag 로 피호출자의 내부 분기를 지시해야 한다 — 즉 caller 측에 control coupling 을 강제한다. 낮은 cohesion 과 나쁜 coupling 은 동전의 양면.
</details>

### Q12. Parnas (1972) 의 module 분해 기준을 한 문장으로? 그가 반대한 기준과, KWIC 예제에서 차이가 드러나는 변경 시나리오 하나는?

<details><summary>답</summary>
"어렵거나 변할 가능성이 높은 design decision 의 목록에서 시작해, 각 decision 을 다른 module 들로부터 숨기는 것 (secret) 을 module 로 삼아라." 반대한 기준: flowchart 의 처리 단계 하나하나를 module 로 만드는 것. KWIC 시나리오 예: 줄 저장 방식 변경 (메모리 → 보조기억, 문자 packing) — flowchart 분해에서는 공유 데이터 구조를 모든 module 이 알므로 거의 전부 수정, information hiding 분해에서는 Line Storage module 하나만 수정. (circular shift 표현 변경 → Circular Shifter 만, 정렬 시점 변경 → Alphabetizer 만도 정답.)
</details>

### Q13. Information hiding 과 encapsulation 의 관계는?

<details><summary>답</summary>
Information hiding 은 "무엇을 비밀로 할 것인가" 라는 설계 결정 (분해 기준), encapsulation 은 그 비밀에 대한 접근을 언어 기능 (private 등) 으로 막는 구현 수단. 수단과 목적의 관계이지 동의어가 아니다.
</details>

### Q14. Architectural erosion 과 drift 의 구분 (Perry & Wolf 1992) 은? Emergency fix 가 이 부패를 만드는 경로는?

<details><summary>답</summary>
Erosion: architecture 를 **위반**하는 변경의 누적 (금지된 의존, layer 건너뛰기). Drift: 위반은 아니지만 architecture 에 **무관심한** 변경의 누적 — 설계 의도가 불명료해지고 erosion 의 길을 닦는다. Emergency fix 경로: 운영 장애 → 문서·설계 갱신 없이 코드만 급히 수정 ("빨리 되는" 해법 선택) → 갱신은 다음 긴급 수정에 밀려 영구 누락 → 요구·설계·코드 불일치 고착 + software ageing 가속. 처방: 수정 후 refactoring 으로 구조 복원, 설계 규칙의 기계 검사.
</details>

### Q15. Configuration management 의 4가지 활동은?

<details><summary>답</summary>
Version management (버전 추적·동시 수정 조정), system building/integration (버전 조합 정의 + 자동 빌드), problem tracking (이슈 보고·상태 추적), release management (릴리스 기능 계획·배포). 재현 가능한 빌드가 CI/CD 의 전제.
</details>

### Q16. Verification vs validation — Boehm 의 두 질문과, 따로 필요한 이유는?

<details><summary>답</summary>
Verification: "are we building the product right?" (스펙 대비). Validation: "are we building the right product?" (실제 필요 대비). 따로 필요한 이유: requirements 문서 자체가 고객의 진짜 필요를 반영한다는 보장이 없으므로 (elicitation 의 어려움) — 스펙 100% 부합해도 잘못된 제품일 수 있다.
</details>

### Q17. Inspection 이 testing 대비 갖는 강점 2개와 원리적 한계는?

<details><summary>답</summary>
강점: (1) 실행 불가능한 산출물 (요구 문서, 설계, 미완성 코드) 에도 적용 가능, (2) 한 번에 여러 결함 발견 (한 오류가 다른 오류를 가리는 간섭 없음). 한계: 실행하지 않으므로 성능 등 NFR 결함과 예기치 못한 상호작용에서 오는 결함은 못 찾는다 — testing 만 가능.
</details>

### Q18. V-model 의 대응 관계 (왼쪽 산출물 ↔ 오른쪽 test level) 는?

<details><summary>답</summary>
User requirements ↔ acceptance test (validation 성격), system requirements ↔ system test, architectural design (interface 정의 포함) ↔ integration test, detailed design ↔ unit test. Coding 은 V 의 꼭짓점 — 짝이 되는 test level 이 따로 없고, code 는 detailed design 과 함께 unit test 의 basis 에 들어간다. 핵심은 각 산출물이 대응 level 의 **test basis** 라는 것 — 산출물이 생기는 즉시 그 기준의 테스트를 설계할 수 있다. 한계: validation 이 사슬의 맨 끝.
</details>

### Q19. Rolling / blue-green / canary 를 rollback 속도와 전제 조건으로 비교하면? Blue-green 의 DB schema 함정과 안전 절차는?

<details><summary>답</summary>
Rolling: 순차 교체, 추가 인프라 최소, rollback 은 역방향 roll (느림), 구·신 동시 서빙 → N-1 호환 필수. Blue-green: 환경 2벌 + 라우터 절체, rollback 즉시, 인프라 2배. Canary: 소량 트래픽으로 실측 검증 후 확대, blast radius 상한을 c 로 캡, metric 파이프라인·자동 판정 없으면 무의미. Blue-green 함정: 환경은 2벌이지만 **DB 는 1벌** — 절체·rollback 순간에 구버전이 신 schema 를 (또는 그 역을) 읽게 된다. 안전 절차: expand/contract (parallel change) — (1) expand: 새 컬럼 추가 + dual-write/backfill, (2) 읽기를 릴리스에 걸쳐 이전, (3) contract: 아무 버전도 안 쓰게 된 뒤 구 컬럼 제거. 각 단계가 개별적으로 하위 호환.
</details>

### Q20. Canary 비율 c 를 줄이면 좋아지는 것과 나빠지는 것은? (식으로)

<details><summary>답</summary>
좋아지는 것: worst-case 피해 상한 $cRTf$ 가 c 에 비례해 감소. 나빠지는 것: 판정에 필요한 표본 $N$ 을 모으는 시간 $t_{detect} = N/(cR)$ 이 $1/c$ 로 증가. 표본 검출형 결함의 기대 피해는 $N \cdot f$ 로 c 와 무관 — canary 의 가치는 평균이 아니라 worst case 의 캡.
</details>

### Q21. 유지보수 4분류와 Sommerville 의 대응 명칭, 실측 비중은?

<details><summary>답</summary>
Corrective (fault repair, ~24%), adaptive (environmental adaptation, ~19%), perfective (functionality addition/modification, ~58%), preventive (선제 구조 개선 — ISO 14764 가 추가). 비중 출처: Sommerville Fig 9.12 (Davidsen & Krogstie 2010), 30년간 거의 불변. 요점: 유지보수의 3/4 은 진화.
</details>

### Q22. 유지보수 중 기능 추가가 개발 중보다 비싼 3가지 이유는?

<details><summary>답</summary>
(1) 새 팀의 program understanding 비용 (설계 결정의 배경까지 이해해야 안전하게 변경), (2) 개발·유지보수 계약 분리 → 개발팀이 유지보수성에 투자할 유인 없음, (3) 유지보수 업무의 낮은 인기 → 숙련 인력 배치 어려움.
</details>

### Q23. Lehman 의 E-type 정의와, laws 가 E-type 에만 적용되는 이유는?

<details><summary>답</summary>
E-type: 현실 세계에 embed 되어 그 세계와 상호작용하는 프로그램 (S-type: 형식 스펙으로 완전 정의, P-type: 현실 문제의 근사 해). 이유: E-type 은 설치 자체가 환경을 바꾸고 바뀐 환경이 새 요구를 낳는 feedback loop 안에 있다 — 진화 압력의 원천. 스펙이 고정된 S-type 엔 이 loop 가 없다.
</details>

### Q24. Lehman law 1 (continuing change) 과 2 (increasing complexity) 의 조합이 만드는 긴장과 그 해소는?

<details><summary>답</summary>
변하지 않으면 점점 무용해지고 (1), 변하면 구조가 퇴화한다 (2). 해소: 복잡도를 줄이는 작업을 명시적으로 투입 — preventive maintenance (refactoring) 는 사치가 아니라 law 2 에 대한 상쇄 작업이다.
</details>

### Q25. Cunningham 의 technical debt 은유에서 debt / interest / repayment 는? Fowler quadrant 에서 이 은유의 위치는?

<details><summary>답</summary>
Debt: 현재의 불완전한 이해를 담은 코드로 일단 출시하는 것 (학습을 앞당김). Interest: not-quite-right 코드 위에서 이후 모든 작업이 조금씩 느려지는 비용 — "every minute spent on not-quite-right code counts as interest". Repayment: 배운 것을 반영한 신속한 rewrite. 위험은 부채가 아니라 미상환. Quadrant (deliberate/inadvertent × prudent/reckless) 에서: "지금 출시한다" 는 결정은 prudent-deliberate 지만, Fowler 자신은 Ward 가 말한 debt — 출시해 봐야 드러나는 not-quite-rightness — 를 **prudent-inadvertent** ("now we know how we should have done it") 에 놓는다. "설계할 시간 없어" 는 reckless-deliberate — 은유가 정당화해주지 않는 부실.
</details>

---

## Anki TSV

```tsv
FR vs NFR definition?	FR: statement of a service/reaction the system shall provide. NFR: constraint on services or functions (timing, standards, process), often system-wide.
Three NFR source categories?	Product (behavioral constraints: performance, availability, security), organizational (developer's policies/standards), external (regulation, law, ethics).
Why is "easy to use" not a requirement?	It is an unverifiable goal — no objective test can decide it. Rewrite measurably, e.g., "all functions usable after 2h training, ≤2 errors/hour thereafter".
Availability formula?	A = MTTF / (MTTF + MTTR) — availability improves by failing less AND recovering faster.
Five reasons elicitation is hard?	Stakeholders don't know what they want; tacit knowledge and own terms; conflicting stakeholders; political factors; environment changes during analysis.
What does ethnography capture that interviews miss?	Requirements from actual (not formal) work practice and from cooperation/awareness between workers; tacit knowledge too obvious to be mentioned.
User story template and philosophy?	"As a <role>, I want <capability>, so that <benefit>" — a placeholder for a conversation, negotiable, judged by acceptance criteria; not a contract.
INVEST criteria for stories?	Independent, Negotiable, Valuable, Estimable, Small, Testable.
Five requirements validation checks?	Validity, consistency, completeness, realism, verifiability. Techniques: reviews, prototyping, test-case generation.
What breaks without traceability?	Change analysis and costing — you cannot determine which design/code/tests a requirements change affects.
Sommerville's four design activities?	Architectural design, database design, interface design, component selection and design.
Why decide architecture early?	Cost asymmetry: refactoring a component is cheap; refactoring the architecture forces modifying most components. Incremental architecture development usually fails.
Coupling grades worst to best?	Content > common > external > control > stamp > data.
Cohesion grades worst to best?	Coincidental < logical < temporal < procedural < communicational < sequential < functional.
Why is logical cohesion bad?	Flag-selected "same category" grouping forces control coupling on callers — low cohesion and bad coupling are two sides of one coin.
Parnas's decomposition criterion?	Start from difficult or likely-to-change design decisions; each module hides one such decision (its secret) behind an interface. Not flowchart steps.
KWIC: line storage format changes — impact in each decomposition?	Flowchart: nearly every module (shared data structure known to all). Information hiding: only the Line Storage module.
Parnas's three benefits of information hiding?	Independent development (managerial), changeability (product flexibility), comprehensibility. Contingent on predicting which decisions actually change.
Information hiding vs encapsulation?	Hiding = the design decision of what to make secret; encapsulation = the language mechanism enforcing access. Means vs end, not synonyms.
Erosion vs drift (Perry & Wolf)?	Erosion: accumulated violations of the architecture. Drift: accumulated insensitivity to it — intent obscured, paving the way to erosion.
Emergency fix failure path?	Urgent fix without doc/design update → realignment postponed forever → requirements, design, code permanently inconsistent; quick fixes accelerate ageing.
Four configuration management activities?	Version management, system building/integration, problem tracking, release management.
Verification vs validation?	Verification: "building the product right" (conforms to spec). Validation: "building the right product" (meets real needs). Spec itself may be wrong, so both can fail independently.
Inspection strengths and limit?	Works on non-executable artifacts, finds many defects per pass without masking; but cannot find NFR (performance) defects or unexpected-interaction defects — those need execution.
V-model pairing?	User requirements↔acceptance, system requirements↔system test, architectural design↔integration, detailed design↔unit; coding sits unpaired at the vertex (code joins detailed design as unit-test basis). Each artifact is the test basis for its level. Weakness: validation comes last.
Rolling deployment requirement?	Old and new versions serve traffic concurrently → N-1 compatibility of API, schema, and message formats; rollback is a slow reverse roll.
Blue-green key property and trap?	Instant router-switch cutover/rollback; but the DB is single — schema must stay compatible with both versions (expand/contract), else rollback is illusory.
Canary: what does shrinking c buy and cost?	Buys a lower worst-case cap cRTf; costs detection latency t=N/(cR) growing as 1/c. Expected harm of sample-detected defects is N·f regardless of c.
Expand/contract (parallel change)?	1 expand: add new column, dual-write/backfill; 2 migrate readers over releases; 3 contract: drop old column when unused. Every step backward-compatible.
Four maintenance categories (ISO 14764)?	Corrective (fault repair), adaptive (environmental adaptation), perfective (functionality addition), preventive (restructuring to cut future cost).
Maintenance effort distribution (Sommerville Fig 9.12)?	~24% fault repair, ~19% environmental adaptation, ~58% functionality addition/modification — maintenance is mostly evolution, not bug fixing.
Why is maintenance-time feature addition costlier?	New team must understand the program first; contract separation removes maintainability incentives; maintenance work is unpopular/less skilled.
Lehman E-type vs S-type?	E-type: embedded in the real world, feedback loop (installation changes environment → new requirements) — laws apply. S-type: fully defined by a fixed formal spec — no loop, laws don't apply.
Lehman laws 1 and 2?	1 Continuing change: evolve or become progressively less useful. 2 Increasing complexity: structure degrades unless explicit work is done to reduce complexity.
Lehman laws 4 and 5?	4 Conservation of organizational stability: average activity roughly invariant to resources. 5 Conservation of familiarity: per-release change bounded by what the organization can absorb.
Cunningham's technical debt metaphor?	Debt: shipping not-quite-right code embodying current understanding to learn sooner. Interest: every minute working on that code. Repayment: prompt rewrite with the improved understanding.
Fowler's debt quadrant and Cunningham's position?	Deliberate/inadvertent × prudent/reckless. The decision to ship is prudent-deliberate, but Fowler places Ward's debt — the not-quite-rightness revealed only by shipping — in prudent-inadvertent ("now we know how we should have done it"). "No time for design" = reckless-deliberate.
Boehm & Basili defect cost claim?	Finding/fixing a problem after delivery is often 100x the cost of fixing it during requirements/design (large systems; factor much smaller for small systems).
```
