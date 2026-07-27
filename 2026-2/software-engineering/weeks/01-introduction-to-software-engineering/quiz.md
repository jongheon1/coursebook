# Week 1 — Active Recall Quiz

먼저 답을 소리 내어 말한 뒤 펼쳐서 확인한다. 답의 핵심 용어는 영어를 유지한다.

---

**Q1.** Software engineering 의 Sommerville 정의와 IEEE 610.12 정의를 각각 말하라.

<details><summary>답</summary>
Sommerville: "an engineering discipline concerned with **all aspects of software production**, from early system specification to maintenance after it goes into use." IEEE 610.12: "the application of a **systematic, disciplined, quantifiable** approach to the development, operation, and maintenance of software."
</details>

**Q2.** "Software crisis" 는 언제 어디서 명명됐고, 무엇을 가리키는가?

<details><summary>답</summary>
1968년 NATO Science Committee 의 Garmisch **Software Engineering Conference**. 하드웨어 성능 성장 대비 소프트웨어가 예산 초과·일정 지연·낮은 신뢰성으로 만성 실패하던 상태. 일회성 사건이 아니라 복잡도가 방법을 앞지를 때마다 재발하는 구조적 조건.
</details>

**Q3.** Software ≠ program 인 이유는? 소프트웨어에 포함되는 것 두 가지 이상.

<details><summary>답</summary>
Software = programs + 그것을 유용하게 만드는 모든 것: **documentation**, 설치·구성용 **configuration data**, 라이브러리 등. 배포·설정·수정 방법을 아무도 모르면 program 은 있어도 software product 는 없는 것.
</details>

**Q4.** Brooks 의 3×3 프레임: 두 축의 이름과 각 축이 추가하는 비용을 말하라. 최종 배수는?

<details><summary>답</summary>
Program → **Programming Product** (×3): generalization, 철저한 testing, documentation, 유지보수 가능성. Program → **Programming System** (×3): 정의된 interface 준수, 자원 예산 준수, 통합 테스트. 둘 다 = **Programming Systems Product, ~×9**. 코딩은 소프트웨어 비용의 소수 지분.
</details>

**Q5.** Brooks's law 를 말하고, 그 세 가지 근거를 대라.

<details><summary>답</summary>
"**Adding manpower to a late software project makes it later.**" 근거: (1) 통신 경로 $n(n-1)/2$ 의 초선형 증가, (2) 신규 인원 ramp-up 이 기존 인원 생산성을 잠식, (3) 분할 불가능한 (직렬) 작업엔 인력 추가가 무효.
</details>

**Q6.** 10명 팀에 5명을 추가하면 통신 경로는 몇 개에서 몇 개가 되는가?

<details><summary>답</summary>
$10 \cdot 9/2 = 45$ → $15 \cdot 14/2 = 105$. 능력 1.5배에 통신 경로 **2.3배**.
</details>

**Q7.** Essential complexity 와 accidental complexity 를 정의하라.

<details><summary>답</summary>
**Essential**: 소프트웨어의 개념 구조 자체 (상호 맞물린 data sets·관계·알고리즘) 를 지정·설계·검증하는 데 내재한 어려움 — 표현 도구로 제거 불가. **Accidental**: 그 구조를 특정 기술로 표현하는 과정의 어려움 (언어, 빌드, 도구) — 원리상 제거 가능.
</details>

**Q8.** Brooks 의 essence 4속성을 나열하고 각각 한 줄로 설명하라.

<details><summary>답</summary>
**Complexity** (같은 부분이 없어 크기 대비 최고 복잡도, 상호작용이 초선형 증가) · **Conformity** (자연법칙이 아닌 인간 제도·기존 인터페이스에 맞춰야 함) · **Changeability** (무한히 가변적이라 인식되어 끊임없는 변경 압력 — 성공할수록 더) · **Invisibility** (기하학적 표현 없음 — 겹치는 여러 그래프로만 표현됨).
</details>

**Q9.** "No Silver Bullet" 의 핵심 논증을 9/10 산수로 재구성하라.

<details><summary>답</summary>
과거의 10배급 도약 (HLL, time-sharing, 환경) 은 전부 accidental 제거였다. accidental 비중이 전체의 9/10 미만이면, accidental 을 **전부 0으로 만들어도** 총 개선은 10배 미만. 남는 essence 를 지수적으로 공략하는 단일 기법은 없다 → 은탄환 없음.
</details>

**Q10.** Brooks 가 제시한 essence 공략법 (promising attacks) 4가지는?

<details><summary>답</summary>
(1) **Buy vs build** (아예 안 만들기 — 기성품·재사용), (2) **requirements refinement & rapid prototyping**, (3) **grow, don't build** (incremental development), (4) **great designers** 양성.
</details>

**Q11.** Ariane 5 사고의 proximate cause 를 변수명·변환·시점까지 말하라.

<details><summary>답</summary>
SRI 의 alignment function 이 계산하는 **horizontal bias (BH)** (수평 속도에 비례) 를 **64-bit float → 16-bit signed int 로 변환**하는 미보호 코드에서, Ariane 5 의 큰 수평 속도로 값이 32767 을 초과 → **H0+36.7초** (리프트오프 후 약 30초) 에 Ada **Operand Error** → 예외 정책에 따라 프로세서 셧다운 → 진단 비트 패턴이 비행 데이터로 해석돼 노즐 full deflection → H0+39s 분해·자폭.
</details>

**Q12.** Ariane 5 에서 backup SRI 가 무력했던 이유와 그 현상의 이름은?

<details><summary>답</summary>
Backup 과 active 가 **동일 소프트웨어**라 같은 입력에 같은 방식으로 실패 — backup 이 72ms **먼저** 죽어 전환 대상이 없었다. **Common-mode failure**: 이중화는 독립적 무작위 고장만 방어하고 design fault 는 못 막는다.
</details>

**Q13.** Ariane 5 의 미보호 변환이 "실수"가 아니었던 이유는?

<details><summary>답</summary>
"Ariane 4 에서는 물리적으로 제한되거나 여유가 충분하다"는 reasoning (Lions 보고서: 궤적 데이터로 분석한 증거는 없음) + CPU 부하 80% 이하 요구 → 위험 변수 7개 중 4개만 보호하기로 파트너들이 **공동 합의한 의도적 결정**. 단 그 정당화는 소스에도 spec 에도 문서화되지 않아 외부 리뷰에서 가려졌다. 실패는 코딩이 아니라 그 **환경 가정을 spec 에 명시하지 않고 Ariane 5 에서 재검증하지 않은 것** (재사용의 함정).
</details>

**Q14.** Therac-25 race condition 의 메커니즘과 발현 조건은?

<details><summary>답</summary>
Bending magnet 설정에 **~8초** 소요. 그 안에 오퍼레이터가 모드/에너지를 수정하면, 공유 변수 + 한 번만 검사되는 완료 플래그 구조 때문에 수정이 미반영 → **X-ray 용 고전류 빔 (~100배) + 타깃 제거** 상태로 조사. 빠른 (숙련된) 오퍼레이터에게만 발현 — 재현 극난.
</details>

**Q15.** Therac-20 에는 같은 버그가 있었는데 왜 사고가 없었나? 여기서 나오는 원칙은?

<details><summary>답</summary>
**하드웨어 인터록**이 위험 조합을 물리적으로 차단 — 소프트웨어가 틀려도 퓨즈만 나감. Therac-25 는 인터록을 제거하고 안전을 소프트웨어에 전담시켰다. 원칙: **defense in depth** — safety 는 소프트웨어가 아니라 **시스템의 속성**이다 (Leveson & Turner).
</details>

**Q16.** Knight Capital 사고의 4단계 인과 사슬을 순서대로 말하라.

<details><summary>답</summary>
(1) **Power Peg dead code** 를 2003년 은퇴 후에도 미삭제 → (2) 2005년 리팩토링으로 체결 카운터가 이동해 종료 조건이 **조용히 파손** → (3) 신기능 RLP 가 **옛 활성화 플래그를 재사용** → (4) 8대 중 1대 **수동 배포 누락** → 그 서버가 플래그를 옛 의미로 해석, 체결량 무시하고 주문 무한 발사. 45분, 체결 400만+, ~$460M 손실.
</details>

**Q17.** Knight 의 롤백이 사태를 악화시킨 이유는?

<details><summary>답</summary>
정상이던 7대에서 신코드를 제거하자 그 서버들도 **이전 코드 = 플래그를 Power Peg 로 해석**하는 상태로 복귀 → 폭주가 1대에서 **8대 전부**로 확대. 교훈: 롤백도 배포다 — 검증 없는 롤백은 복구가 아니라 재배포.
</details>

**Q18.** 좋은 소프트웨어의 4 essential attributes 를 정의와 함께 나열하라.

<details><summary>답</summary>
**Maintainability** (변화하는 요구에 맞춰 진화 가능하게), **dependability & security** (reliability + safety + security — 실패가 물리·경제적 피해로 이어지지 않고 악의적 접근 차단), **efficiency** (자원 낭비 없음 — responsiveness·처리시간·메모리), **acceptability** (대상 사용자에게 이해·사용 가능, 타 시스템과 호환).
</details>

**Q19.** Generic product 와 custom (bespoke) system 을 가르는 결정적 기준은?

<details><summary>답</summary>
**Specification 의 소유권.** Generic 은 개발 조직이 spec 과 변경을 결정 (시장 판매), custom 은 발주 고객이 spec 을 소유·통제. ERP 구성·확장 같은 하이브리드에선 주도권이 분할되어 요구공학이 더 어려워진다.
</details>

**Q20.** 소프트웨어 프로세스에 공통인 4 fundamental activities 는?

<details><summary>답</summary>
**Specification** (무엇을 만들지와 운영 제약 정의), **development** (설계·프로그래밍), **validation** (고객이 원하는 것과 일치하는지 확인), **evolution** (변화하는 요구 반영 수정). 배열 방식이 process model (W3).
</details>

**Q21.** Custom software 의 비용 구조에서 시험에 나올 두 가지 수치/관계는?

<details><summary>답</summary>
대략 **development 60% / testing 40%**, 그리고 custom 시스템에서 **evolution 비용 > development 비용** (Sommerville ch1 FAQ) — maintainability 가 첫 번째 essential attribute 인 이유.
</details>

**Q22.** Sommerville 의 직업 윤리 4대 이슈는?

<details><summary>답</summary>
**Confidentiality** (계약 없어도 기밀 존중), **competence** (능력 허위 표현 금지, 능력 밖 수임 금지), **intellectual property rights** (특허·저작권 존중), **computer misuse** (타인 컴퓨터 오용 금지).
</details>

**Q23.** ACM/IEEE Code of Ethics 8원칙을 나열하고, 원칙 충돌 시 규칙을 말하라.

<details><summary>답</summary>
**Public, Client and Employer, Product, Judgment, Management, Profession, Colleagues, Self.** 충돌 시 **public interest (건강·안전·복리) 가 최우선** — 고용주 이익 (2) 은 공공 이익 (1) 과 일치하는 범위에서만. "시켜서 했다"는 면책이 아니다.
</details>

**Q24.** 세 사고 (Ariane, Therac, Knight) 를 관통하는 공통 패턴 한 가지는?

<details><summary>답</summary>
**검증된 것의 경계 밖 재사용**: Ariane — 다른 로켓 (환경 가정 이식 실패), Therac — 다른 기계 (인터록 없는 환경으로 SW 이식), Knight — 다른 의미로 플래그 재사용. 검증은 그 전제 가정과 함께 이식되지 않는 한 이식되지 않는다.
</details>

**Q25.** 일회성 스크립트·제품·safety-critical 시스템에서 공학적 엄격성을 결정하는 두 변수는?

<details><summary>답</summary>
**실패 비용** (재실행 분 vs 매출 손실 vs 인명) 과 **기대 수명** (1회 vs 수년 vs 수십 년). 판단 순서는 실패 비용 평가 → 프로세스 선택. 과잉 엄격성은 돈을 잃고 과소 엄격성은 사람을 잃는다 — 보편적 SE 방법은 없다 (Sommerville).
</details>

---

## Anki import (TSV)

```tsv
Software engineering 의 Sommerville / IEEE 610.12 정의는?	Sommerville: engineering discipline concerned with all aspects of software production, specification 부터 maintenance 까지. IEEE 610.12: systematic, disciplined, quantifiable approach to development, operation, maintenance of software.
Software crisis 는 언제 어디서 명명? 무엇?	1968 NATO Garmisch Software Engineering Conference. 예산 초과·지연·저신뢰의 만성 실패 상태 — 복잡도가 방법을 앞지를 때마다 재발하는 구조적 조건.
Software ≠ program 인 이유는?	Software = programs + documentation + configuration data 등 유용하게 만드는 전부. 배포·설정·수정법을 모르면 product 가 아님.
Brooks 3×3 프레임의 두 축과 최종 배수는?	Product 축 ×3 (generalization·testing·documentation), System 축 ×3 (interface·자원 예산·통합 테스트) → programming systems product ~×9. 코딩은 비용의 소수 지분.
Brooks's law 와 세 근거는?	Adding manpower to a late software project makes it later. 통신 경로 n(n-1)/2, ramp-up 이 기존 인원 잠식, 분할 불가 작업.
10명 팀 → 15명이면 통신 경로는?	45 → 105 (n(n-1)/2). 능력 1.5배, 통신 경로 2.3배.
Essential vs accidental complexity 정의는?	Essential: 문제의 개념 구조 자체의 어려움 — 도구로 제거 불가. Accidental: 표현 기술 (언어·빌드·도구) 에서 오는 어려움 — 원리상 제거 가능.
Brooks essence 의 4속성은?	Complexity (같은 부분 없음, 초선형 상호작용) · conformity (인간 제도에 맞춤) · changeability (끊임없는 변경 압력) · invisibility (기하학적 표현 없음).
No Silver Bullet 의 9/10 논증은?	과거 도약은 전부 accidental 제거. accidental 비중이 9/10 미만이면 전부 없애도 10배 미만. essence 공략에 지수적 기법 없음 → 단일 기법 10배 개선 불가.
Brooks 의 essence 공략법 4가지는?	Buy vs build, requirements refinement & rapid prototyping, grow don't build (incremental), great designers.
Ariane 5 proximate cause 는?	SRI alignment function 의 horizontal bias (BH) 를 64-bit float → 16-bit signed int 변환 (미보호), Ariane 5 의 큰 수평 속도로 H0+36.7s (리프트오프 후 ~30s) 에 overflow → Operand Error → 프로세서 셧다운 → 진단 패턴을 비행 데이터로 해석 → 자폭.
Ariane 5 backup SRI 가 무력했던 이유는?	동일 소프트웨어 → 같은 입력에 같은 실패 (backup 이 72ms 먼저 사망). Common-mode failure — 이중화는 design fault 를 못 막는다.
Ariane 5 미보호 변환이 실수가 아닌 이유는?	Ariane 4 에선 물리적으로 제한된다는 reasoning (궤적 데이터 분석 증거 없음) + CPU 80% 요구로 7개 중 4개만 보호한, 파트너들이 공동 합의한 의도적 결정 — 단 정당화는 소스·spec 에 미문서화. 실패는 환경 가정의 미명세 + 새 환경 재검증 부재 (재사용의 함정).
Therac-25 race condition 메커니즘은?	Magnet 설정 ~8초 내 오퍼레이터가 모드 수정 → 공유 변수·1회 검사 플래그 탓에 미반영 → 고전류 (~100배) 빔 + 타깃 제거 = 과조사. 빠른 오퍼레이터에게만 발현.
Therac-20 에 같은 버그가 있었는데 무사고인 이유와 원칙은?	하드웨어 인터록이 위험 조합을 물리 차단 (퓨즈만 소손). Defense in depth — safety 는 시스템 속성, 소프트웨어 단일 계층에 안전을 전담시키지 말 것.
Knight Capital 4단계 인과 사슬은?	Dead code 방치 (2003) → 리팩토링으로 종료 조건 파손 (2005) → RLP 가 옛 플래그 재사용 → 8대 중 1대 배포 누락 → 폭주. 45분, ~$460M.
Knight 의 롤백이 악화시킨 이유는?	7대의 이전 코드도 플래그 = Power Peg 해석 → 폭주가 1대에서 8대로 확대. 롤백도 배포다 — 검증 없는 롤백은 재배포.
좋은 소프트웨어 4 essential attributes 는?	Maintainability (진화 가능), dependability & security (reliability+safety+security), efficiency (자원 낭비 없음), acceptability (이해·사용 가능·호환).
Generic vs custom system 구분 기준은?	Specification 소유권. Generic = 개발자가 spec·변경 결정 (시장), custom = 고객이 소유·통제. 하이브리드 (ERP 구성) 는 주도권 분할.
SE 의 4 fundamental activities 는?	Specification (무엇+제약 정의), development (설계·프로그래밍), validation (고객 요구와 일치 확인), evolution (변경 반영). 배열 = process model.
SE 비용 구조의 시험용 수치 둘은?	Development ~60% / testing ~40%; custom 은 evolution 비용 > development 비용.
Sommerville 윤리 4대 이슈는?	Confidentiality, competence, intellectual property rights, computer misuse.
ACM/IEEE 8원칙과 충돌 시 규칙은?	Public, Client and Employer, Product, Judgment, Management, Profession, Colleagues, Self. 충돌 시 public interest 최우선 — 고용주 이익은 공공 이익과 일치 범위 내.
세 사고의 공통 패턴은?	검증된 것의 경계 밖 재사용 — 다른 로켓 / 다른 기계 / 다른 의미의 플래그. 검증은 가정과 함께가 아니면 이식되지 않는다.
공학적 엄격성을 결정하는 두 변수는?	실패 비용과 기대 수명. 실패 비용 평가 → 프로세스 선택. 과잉 엄격성 = 돈 손실, 과소 엄격성 = 인명 손실.
```
