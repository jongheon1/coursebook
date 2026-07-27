# Week 4 — Active Recall Quiz

먼저 답을 소리 내어 말한 뒤 펼쳐서 확인한다. 답의 핵심 용어는 영어를 유지한다.

---

**Q1.** Git object 의 id 는 어떻게 계산되는가? 정확한 공식과, 이 방식의 이름은?

<details><summary>답</summary>
$\text{oid} = \text{SHA-1}(\texttt{"<type> <size>\0"} \Vert \text{content})$ — header(타입, 바이트 크기, NUL) 뒤에 내용을 붙여 해싱. content-addressable storage: 주소가 내용의 함수이므로 object 는 불변이고 자동 중복 제거된다.
</details>

**Q2.** Git 의 4가지 object type 과 각각이 담는 것은?

<details><summary>답</summary>
blob = 파일 내용 (이름·경로·시각 없음); tree = 디렉토리 1개 (mode, type, oid, name 엔트리 목록); commit = root tree + parent(들) + author/committer + 메시지; annotated tag = 대상 object + 타입 + tag 이름 + tagger + 메시지 (서명 가능).
</details>

**Q3.** Git 히스토리가 Merkle DAG 라는 것의 의미와, 따라오는 무결성 속성은?

<details><summary>답</summary>
tree id 는 자식 id 들을, commit id 는 tree id 와 parent id 를 포함해 계산되므로 tip id 하나가 도달 가능한 전체 히스토리를 재귀적으로 요약한다. 과거 1바이트만 바뀌어도 그 위 모든 id 가 연쇄 변경 → 변조 증거; 두 레포의 tip 이 같으면 히스토리 전체가 같음 (동기화 판정 O(1)).
</details>

**Q4.** Git 이 SHA-1 에서 SHA-256 으로 전환하는 이유와, 전환이 유독 어려운 이유는?

<details><summary>답</summary>
2017 SHAttered 가 실제 SHA-1 collision 을 보임 (~$2^{63}$ 연산) — "id 같으면 내용 같다" 논증이 깨질 수 있음. 임시로 hardened SHA-1(sha1dc, 2.13+) 로 공격 패턴을 탐지하고, `git init --object-format=sha256` (2.29 실험, 2.42 정식) 제공. 어려운 이유: 해시 함수가 곧 모든 object 의 이름이라 전환하면 전체 oid 가 바뀜 — 두 형식 간 변환 테이블·프로토콜·생태계 지원이 전부 필요.
</details>

**Q5.** branch, HEAD, detached HEAD 의 파일 수준 실체는?

<details><summary>답</summary>
branch = `.git/refs/heads/<name>` 의 41바이트 파일 (40-hex oid + 개행) — 생성이 파일 하나 쓰기라 O(1). HEAD = `.git/HEAD`, 보통 symbolic ref (`ref: refs/heads/main`). detached HEAD = HEAD 에 branch 이름 대신 commit oid 가 직접 든 상태 — 여기서 만든 commit 은 branch 가 안 가리키므로 이탈 시 reflog 로만 도달 가능.
</details>

**Q6.** index (staging area) 는 무엇이고, blob 은 `git add` 와 `git commit` 중 언제 object DB 에 쓰이는가?

<details><summary>답</summary>
`.git/index` 바이너리 파일 — "다음 commit 이 될 tree 의 평면 목록" (경로별 mode, blob oid, stage 번호 + stat 캐시). blob 은 **`git add` 시점에 즉시** object DB 에 기록되고, commit 은 index 를 tree 로 굳혀 commit object 를 만들고 ref 를 옮길 뿐이다.
</details>

**Q7.** two-way merge 로는 왜 안 되고, three-way merge 에서 conflict 의 형식적 정의는?

<details><summary>답</summary>
two-way 불가: ours 에 있고 theirs 에 없는 줄이 "theirs 가 지운 것"(지워야 함)인지 "ours 가 추가한 것"(남겨야 함)인지 구분 불가 — 정반대 결과를 요구하는 두 경우가 같은 관측을 만든다. base 가 있어야 누가 무엇을 바꿨는지 판정 가능. conflict 정의: 같은 영역에 대해 ours ≠ base ∧ theirs ≠ base ∧ ours ≠ theirs. 한쪽만 변경=그쪽 채택, 동일 변경=채택. 단 "다른 영역" 판정에는 변경 사이 무변경 줄이 최소 한 줄 필요 — 인접한 변경은 한 영역으로 합쳐져 conflict.
</details>

**Q8.** merge base 는 무엇이고, criss-cross 히스토리에서 recursive/ort 전략이 하는 일은?

<details><summary>답</summary>
DAG 상 두 tip 의 best common ancestor (`git merge-base`). criss-cross 면 best common ancestor 가 복수 존재 — recursive/ort 는 그 조상들끼리 먼저 (재귀적으로) merge 한 virtual base 를 만들어 기준으로 쓴다. ort 는 recursive 재작성으로 Git 2.34 부터 기본.
</details>

**Q9.** conflict 상태에서 index 에는 무엇이 들어 있는가?

<details><summary>답</summary>
해당 경로에 대해 stage 1 = base, stage 2 = ours, stage 3 = theirs 세 버전이 동시에 존재 (`git ls-files -u`, `git cat-file -p :2:path`). 해결 후 `git add` 하면 stage 0 하나로 접힌다. 3-pane merge 도구가 가능한 이유.
</details>

**Q10.** rebase 가 commit 을 "옮기지" 못하고 새로 만드는 이유, merge vs rebase 의 트레이드오프, 공유 브랜치 rebase 금지의 유도는?

<details><summary>답</summary>
commit id 는 parent id 를 포함한 해시라 parent 가 바뀌면 id 가 바뀜 — object 불변성의 귀결. 트레이드오프 — merge: 실제 병렬 작업 토폴로지 보존(+), merge commit 으로 log 가 얽힘(−); rebase: 선형 히스토리로 log/bisect 단순(+), 중간 commit 들이 그 조합으로 테스트된 적 없는 상태(−). 금지의 유도: 이미 push 된 commit C 를 rebase 하면 나는 C′, 동료는 C 를 가짐 → Git 에게 둘은 무관한 commit → 동료의 pull/merge 가 같은 변경 두 벌인 히스토리를 만든다. 그래서 rebase 는 나만 아는 commit 에만; 정당한 재작성 push 는 `--force-with-lease`.
</details>

**Q11.** reflog 의 정의, 한계 2가지, 기본 만료 기간은?

<details><summary>답</summary>
각 ref 와 HEAD 가 이 로컬 레포에서 가리켜 온 값들의 append-only 저널 — reset --hard/rebase 로 잃은 commit 복구 경로 (`git reset --hard 'HEAD@{1}'`). 한계: (1) 로컬 전용 — push/clone 안 됨, (2) 만료: 도달 가능 90일, 도달 불가 30일 (gc.reflogExpire / gc.reflogExpireUnreachable) 후 gc 가 prune 가능.
</details>

**Q12.** "Git 은 diff 를 저장하는가 스냅샷을 저장하는가"의 정확한 답은?

<details><summary>답</summary>
논리 모델은 commit 마다 전체 스냅샷 (root tree). 물리 계층에서만 packfile 이 비슷한 object 를 delta 로 압축 (gc·push/fetch 시). "논리적으로 스냅샷, 물리적으로 pack 안에서 스냅샷+delta".
</details>

**Q13.** git-flow 의 branch 구조와, 어떤 제품에 맞고 어떤 제품에 안 맞는가?

<details><summary>답</summary>
영구 branch: main(릴리스만, tag) + develop(통합); 보조: feature(develop↔), release(develop→안정화→main·develop 양쪽), hotfix(main→양쪽). 맞는 곳: 버전드 릴리스 — 설치형, 앱 심사, 다중 버전 지원. 안 맞는 곳: continuous deployment 웹 서비스 — Driessen 본인이 2020년에 그런 경우 GitHub flow 를 권한다고 노트를 달았다.
</details>

**Q14.** trunk-based development 의 정의와, 그것을 가능하게 하는 기법 2가지, DORA 의 근거는?

<details><summary>답</summary>
모든 개발자가 trunk 하나에 최소 하루 1회 통합 (branch 수명 하루 이내 또는 직접 commit). 기법: feature flag (배포와 릴리스 분리 — 미완성 코드를 꺼둔 채 배포), branch by abstraction, 높은 신뢰도의 CI. Accelerate ch4: 활성 branch ≤3, 수명 <1일, 매일 통합이 높은 전달 성능과 상관.
</details>

**Q15.** protected branch 로 강제할 수 있는 불변식 4가지.

<details><summary>답</summary>
(1) PR 없이는 merge 불가 + approving review N개 (dismiss stale 로 새 push 시 approval 무효화), (2) required status checks — CI green 이어야 merge, (3) force-push·삭제 금지 — 히스토리 append-only, (4) CODEOWNERS 경로별 리뷰어 강제 / linear history 요구 (squash·rebase 만 허용).
</details>

**Q16.** container 와 VM 의 근본 차이 한 문장 + 그로부터 나오는 트레이드오프 2개.

<details><summary>답</summary>
container 는 guest kernel 이 없다 — host kernel 을 공유하고 userland 만 격리한 보통의 Linux 프로세스들. 트레이드오프: 시작 ms 단위·고밀도·MB 이미지 (+) vs 격리가 syscall 경계라 kernel 취약점이 공유 리스크이고 이종 OS 불가 (−).
</details>

**Q17.** namespace 8종 중 6종 이상과 각각의 격리 대상은?

<details><summary>답</summary>
mnt(mount 테이블 — 자기만의 /), pid(PID 공간 — container 첫 프로세스가 PID 1), net(네트워크 스택 — 독립 port 공간), uts(hostname), ipc(SysV IPC/mqueue), user(UID/GID 매핑), cgroup(cgroup root), time(boot/monotonic clock). Docker 기본은 user·time 미사용.
</details>

**Q18.** namespaces 와 cgroups 의 분업을 한 문장으로. 그리고 memory 제한과 cpu 제한의 초과 시 동작 차이는?

<details><summary>답</summary>
namespaces = 무엇이 보이는가(가시성 격리), cgroups = 얼마나 쓸 수 있는가(자원 계량·제한). memory.max 초과 = cgroup 범위 OOM kill (exit 137, 죽는다); cpu.max 초과 = throttling — quota 소진 시 period 끝까지 정지 (죽지 않고 p99 spike 로 느려진다).
</details>

**Q19.** OverlayFS 의 lowerdir/upperdir/merged 역할과, 쓰기·삭제가 각각 어떻게 구현되는가?

<details><summary>답</summary>
lowerdir = image layer 들 (읽기 전용 스택), upperdir = container writable layer, merged = 통합 뷰 (같은 경로는 위가 이김). 쓰기 = copy-up: 파일 전체를 upper 로 복사 후 수정 (파일 단위 CoW — 1GB 파일 1바이트 수정에 1GB 복사). 삭제 = whiteout: upper 에 0/0 character device 를 만들어 lower 파일을 가림 (lower 는 불변).
</details>

**Q20.** Dockerfile 에서 지운 secret 이 왜 복구 가능한가? 크기와 secret 각각의 올바른 해법은?

<details><summary>답</summary>
layer 는 append-only — 뒤 layer 의 rm 은 whiteout 으로 가릴 뿐 앞 layer 의 바이트는 `docker save` 로 추출 가능. 크기·toolchain 제거 = multi-stage build (builder stage 의 layer 는 최종 image 에 미포함), build 시 secret = BuildKit secret mount (layer 에 기록 안 됨).
</details>

**Q21.** Docker build cache 의 무효화 규칙 (RUN vs COPY) 과, 그로부터 나오는 Dockerfile 작성 원칙은?

<details><summary>답</summary>
step 의 cache key = 부모 layer + 명령. RUN 은 명령 문자열만 (결과 무관 — `apt-get update` 단독 layer 가 낡는 함정 → update && install 한 RUN 에), COPY/ADD 는 파일 내용 checksum. 한 step miss 면 이후 전부 재실행 (cascade). 원칙: 변동성 낮은 것부터 — deps manifest 복사·설치를 소스 복사보다 앞에 (lab 실측: 소스만 변경 시 3791ms vs 649ms).
</details>

**Q22.** compose 의 `depends_on` 함정과 tag vs digest 의 차이는?

<details><summary>답</summary>
depends_on 은 시작 순서만 보장, 준비 완료(readiness)는 안 기다림 — healthcheck + condition: service_healthy 필요. tag 는 mutable 포인터 (`:latest` 는 옮겨 다님), digest (`@sha256:...`) 는 immutable content address — 재현 가능한 배포는 digest 고정. Git 의 ref vs object 관계와 동형.
</details>

**Q23.** 아키텍처 결정이 조기·고비용인 세 가지 논거는?

<details><summary>답</summary>
(1) quality attribute (performance, availability, security...) 는 컴포넌트 코드가 아니라 컴포넌트 배치·상호작용 구조에서 창발 — 코드 리팩토링으로 안 고쳐짐. (2) 아키텍처 = 경계들의 집합이라 변경이 국소화되지 않고 전 시스템 파급 — 그런데 결정은 정보가 가장 적은 초기에 내려야 함. (3) 경계가 팀·API 계약·배포 단위로 얼어붙음 (Conway 의 관찰).
</details>

**Q24.** 4+1 view 각각이 답하는 질문과 주 이해관계자는? Scenarios 가 "+1" 인 이유는?

<details><summary>답</summary>
Logical: 기능의 객체 분해 — end-user (class diagram). Process: 런타임 동시성·통신, 성능 분석 — 통합자 (sequence). Development: 모듈·패키지 조직, 팀 분담 — 개발자 (package/component). Physical: 하드웨어 배치 — 인프라 엔지니어 (deployment). Scenarios(+1): 새 정보가 아니라 (의도적으로 redundant) use case 로 4개 view 를 관통·검증하고 잇는 역할.
</details>

**Q25.** performance 와 maintainability 의 구조적 처방이 충돌하는 지점은? (Sommerville)

<details><summary>답</summary>
performance: critical 연산을 소수의 큰 컴포넌트에 국소화 (통신 최소화). maintainability: fine-grain 교체 가능한 컴포넌트. 같은 설계 변수(granularity)를 반대로 당김 — 한 구조에서 동시 최대화 불가. 아키텍트의 산출물은 정답이 아니라 우선순위가 명시된 트레이드오프 결정 (ADR 로 기록).
</details>

---

## Anki TSV

```tsv
Git object id 계산 공식은?	SHA-1("<type> <size>\0" ‖ content) — header 뒤 내용을 해싱. content-addressable: 주소가 내용의 함수, object 불변, 자동 dedup.
Git 4가지 object type 과 내용은?	blob=파일 내용; tree=디렉토리(mode,type,oid,name 목록); commit=root tree+parent(들)+author/committer+메시지; annotated tag=대상 oid+타입+이름+tagger+메시지.
Git 히스토리가 Merkle DAG 인 이유와 속성은?	commit id 가 tree·parent id 를 재귀 포함 → tip 하나가 전체 히스토리 요약. 과거 변조 시 상위 id 연쇄 변경(변조 증거), tip 동일 = 히스토리 동일.
Git SHA-256 전환의 이유와 어려움은?	SHAttered(2017) SHA-1 collision. 임시: sha1dc(2.13+). 정식: --object-format=sha256 (2.29 실험→2.42 정식). 어려움: 해시가 모든 object 의 이름이라 전체 oid 변경 — 변환 테이블·생태계 필요.
Git branch 의 실체와 생성 비용은?	.git/refs/heads/<name> 의 41바이트 파일(40-hex+개행). 생성 = 파일 하나 쓰기 = O(1).
HEAD 와 detached HEAD 의 실체는?	HEAD=.git/HEAD 의 symbolic ref("ref: refs/heads/main"). detached=oid 직접 보유 — 여기서 만든 commit 은 이탈 시 reflog 로만 도달.
git add 와 commit 중 blob 이 저장되는 시점은?	add 시점에 blob 이 object DB 에 즉시 기록 + index 갱신. commit 은 index→tree 동결, commit object 생성, ref 전진만.
three-way merge 의 conflict 정의는?	같은 영역에서 ours≠base ∧ theirs≠base ∧ ours≠theirs. 한쪽만 변경=그쪽 채택, 동일 변경=채택. 단 영역 분리에는 변경 사이 무변경 줄 최소 1줄 필요 — 인접 변경은 한 영역으로 합쳐져 conflict.
two-way merge 가 불가능한 이유는?	ours 에만 있는 줄이 "theirs 의 삭제"인지 "ours 의 추가"인지 구분 불가 — 반대 결과를 요구하는 두 경우가 같은 관측. base 필요.
merge base 정의와 criss-cross 처리?	DAG 의 best common ancestor. 복수면 recursive/ort 가 조상끼리 먼저 merge 한 virtual base 사용. ort 는 2.34+ 기본.
conflict 시 index 상태는?	stage 1=base, 2=ours, 3=theirs 세 버전 공존(git ls-files -u). 해결 후 add 로 stage 0 에 접힘.
공유 브랜치 rebase 금지의 메커니즘 근거는?	rebase 는 parent 변경→새 oid(C′). 동료는 C 보유 → pull/merge 시 같은 변경 두 벌 히스토리. content addressing 의 귀결.
merge vs rebase 트레이드오프?	merge: 토폴로지 진실 보존 / log 얽힘. rebase: 선형·bisect 용이 / 중간 commit 미검증 상태 + force-push 위험.
reflog 정의·한계·만료는?	ref/HEAD 의 로컬 append-only 저널. 한계: 로컬 전용(push 안 됨). 만료: 도달 가능 90일, 불가 30일 후 gc prune 가능.
Git 은 diff 저장인가 스냅샷 저장인가?	논리: commit 마다 전체 스냅샷(root tree). 물리: packfile 에서만 유사 object 간 delta 압축.
git-flow 구조와 적합/부적합은?	main+develop 영구, feature/release/hotfix 보조. 적합: 버전드 릴리스(설치형·앱심사·다중버전). 부적합: continuous deployment (Driessen 2020 노트).
trunk-based development 정의와 enabler 는?	전원이 trunk 에 최소 매일 통합, branch 수명 <1일. enabler: feature flag(배포≠릴리스), branch by abstraction, 강한 CI. DORA: 높은 전달 성능과 상관.
protected branch 불변식 4가지?	PR+review N개(+stale dismiss), required status checks(CI green), force-push·삭제 금지, CODEOWNERS/linear history.
container vs VM 한 문장?	container 는 guest kernel 없음 — host kernel 공유, namespace 로 시야·cgroup 으로 예산만 제한한 보통 프로세스. 밀도·속도 ↔ syscall 경계 격리·kernel 공유 리스크.
Linux namespace 8종은?	mnt, pid, net, uts, ipc, user, cgroup, time — 각각 mount 테이블/PID 공간/네트워크 스택/hostname/IPC/UID 매핑/cgroup root/clock 격리.
Docker 기본 설정과 user namespace 관계는?	기본 미사용(userns-remap/rootless 는 opt-in) — container 의 root = host uid 0. capability 축소+seccomp 가 보완. "container 안 root 는 안전" 은 거짓.
namespaces vs cgroups 분업은?	namespaces=무엇이 보이는가(가시성), cgroups=얼마나 쓰는가(계량·제한: cpu, memory, io, pids).
cgroup memory 초과 vs cpu 초과 동작?	memory.max 초과=cgroup 범위 OOM kill(exit 137). cpu.max 초과=throttling(period 끝까지 정지, p99 spike). 죽는다 vs 느려진다.
OverlayFS 구조와 쓰기/삭제 구현?	lowerdir(image, RO 스택)+upperdir(writable)+merged(위가 이김). 쓰기=copy-up(파일 전체 복사 후 수정). 삭제=whiteout(0/0 char device 로 가림).
image 에서 지운 secret 이 복구되는 이유와 해법?	layer 는 append-only — rm 은 whiteout 일 뿐, docker save 로 앞 layer 추출 가능. 해법: multi-stage(빌드 layer 미포함), BuildKit secret mount.
Docker build cache 무효화 규칙은?	key=부모 layer+명령. RUN=명령 문자열만(apt-get update 단독 함정→update&&install 한 RUN). COPY/ADD=내용 checksum. miss 시 이후 전부 재실행(cascade).
Dockerfile 순서 원칙과 근거는?	변동성 낮은 것부터: base→시스템 패키지→deps manifest+설치→소스. 소스만 바뀌는 일상 빌드에서 설치 step 이 항상 CACHED (lab: 3791ms vs 649ms).
multi-stage build 의 3가지 효과는?	최종 image 에 toolchain·소스·중간 layer 미포함 → 크기 축소, 공격 표면 축소, builder stage 의 secret/파일 잔존 차단.
compose depends_on 의 함정은?	시작 순서만 보장, readiness 는 안 기다림 — healthcheck + condition: service_healthy 필요.
tag vs digest?	tag=mutable 포인터(:latest 이동), digest=@sha256 immutable content address. 재현 배포는 digest 고정. Git 의 ref vs object 와 동형.
아키텍처 결정이 조기·고비용인 3가지 논거?	(1) quality attribute 는 구조에서 창발(코드로 못 고침), (2) 경계 변경은 광역 파급인데 결정은 정보 최소 시점, (3) 경계가 팀·계약·배포 단위로 동결(Conway).
4+1 view 각각의 질문·이해관계자는?	Logical=기능 분해/end-user, Process=동시성·통신·성능/통합자, Development=모듈·팀/개발자, Physical=배치/인프라, Scenarios=use case 로 관통·검증(+1, 의도적 redundant).
performance vs maintainability 의 구조 충돌은?	performance=소수 대형 컴포넌트(통신 최소화) vs maintainability=fine-grain 교체 가능 — 같은 granularity 변수를 반대로 당김. 산출물은 정답이 아니라 명시적 트레이드오프 결정(ADR).
semantic conflict 란?	텍스트 merge 는 성공하지만 의미가 깨지는 충돌 — 예: 한쪽 함수 rename, 다른 쪽 옛 이름 호출 추가. merge 후 CI 필수 근거.
fast-forward merge 란?	theirs 가 ours 의 자손(merge-base=ours)이면 새 commit 없이 ref 만 전진. 묶음 보존 원하면 --no-ff.
```
