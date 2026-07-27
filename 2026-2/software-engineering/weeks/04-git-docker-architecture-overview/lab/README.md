# Week 4 Lab — Git Plumbing & Docker Layer Cache

챕터 §1 (Git internals) 과 §3.5 (layer cache) 의 모든 정량적 주장을 직접 재현한다. 두 실험 모두 자기 검증형이다 — 스크립트 안의 assert 가 실패하면 non-zero 로 종료한다.

## Lab 1 — Git plumbing: object model, merge, reflog (`git-plumbing.sh`)

### 목표

- blob id 가 정확히 `SHA-1("blob <size>\0" + content)` 임을 손으로 재현한다.
- `git add` 시점에 blob 이 object DB 에 기록되는 것, commit/tree/tag object 의 실제 내용, branch 가 41바이트 파일임을 확인한다.
- non-overlapping 편집의 자동 병합과 same-region 편집의 conflict 를 만들고, `git merge-base` 가 fork 지점을 돌려주는 것과 conflict 중 index 의 stage 1/2/3 을 관찰한다.
- `reset --hard` 로 "잃은" commit 을 reflog 로 복구한다.

### 실행

```bash
bash git-plumbing.sh
```

- 의존성: git ≥ 2.23, `shasum` 또는 `sha1sum`. 임시 디렉토리에 일회용 레포를 만들고 종료 시 삭제한다 — 현재 레포는 건드리지 않는다.
- 참고: SHA-256 레포 (`git init --object-format=sha256`) 에서는 header 규칙은 같고 해시 함수·oid 길이만 다르다.

### 예상 출력 (요지)

```
== A1. A blob's name is SHA-1 of 'blob <size>\0' + content ==
  git hash-object : 94bab17c85ac96c4dd0cfcb7a16f22f6862733eb
  manual sha1     : 94bab17c85ac96c4dd0cfcb7a16f22f6862733eb
  OK  blob id == sha1(header + content)
...
== B2. Conflict = both sides changed the SAME region differently vs base ==
  index now holds THREE stages for poem.txt (git ls-files -u):
    100644 451d5e5d... 1  poem.txt      ← stage 1 = base
    100644 13a8b2c0... 2  poem.txt      ← stage 2 = ours
    100644 7511a865... 3  poem.txt      ← stage 3 = theirs
...
All 26 assertions passed.
```

섹션 구성: A1–A8 (object store, refs, tag, detached HEAD) → B1–B4 (auto-merge, conflict, fast-forward, reflog 복구). 26개 assertion 전부 통과가 성공 기준이다.

## Lab 2 — Dockerfile layer cache (`docker-layer-cache/run-experiment.sh`)

### 목표

명령 순서만 다른 두 Dockerfile 로 cache 무효화 규칙을 실측한다:

- `Dockerfile.bad`: `COPY . .` → install (소스 변경이 install 을 무효화)
- `Dockerfile.good`: `COPY deps.txt` → install → `COPY src/` (소스 변경이 install cache 를 보존)

install 은 `sleep 3` 으로 비용을 흉내 낸 step 이다 (네트워크 의존 없음).

### 실행

```bash
cd docker-layer-cache
bash run-experiment.sh
```

- 의존성: Docker (BuildKit — 최신 Docker Desktop/Engine 이면 기본), `alpine:3.20` pull 가능한 네트워크 1회.
- 스크립트는 종료 시 자기 image (`se-w4-cache-*`) 와 파일 수정을 원상 복구한다. base image 는 남긴다.
- 주의: **BuildKit build cache 는 실행 간에 살아남는다** — `docker rmi` 는 image 만 지우고 build cache 는 지우지 않는다. 그래서 스크립트의 파일 편집 두 곳 모두 timestamp 를 넣어 매 실행이 새 content checksum 을 만들게 되어 있다 (재실행해도 assert 가 통과하는 이유). cache 를 진짜 비우고 싶으면 `docker builder prune`.

### 예상 출력 (2026-07 macOS/Docker 27.4 실측)

```
== 2. Source-only change: edit src/main.py ==
   rebuild            install step   wall time
   Dockerfile.bad     re-ran         3791 ms
   Dockerfile.good    CACHED         649 ms
== 3. Manifest change: edit deps.txt ==
   Dockerfile.good after deps.txt change: install re-ran, 3817 ms
   -> cascade: COPY deps.txt 의 checksum 변경이 이후 전 step 을 무효화
All assertions passed.
```

수치는 머신마다 다르지만 부등호는 항상 같아야 한다: bad ≥ 3초 (install 재실행), good ≪ bad (install CACHED), deps 변경 시 good 도 ≥ 3초 (cascade).

### Docker 를 쓸 수 없는 경우 (절차 문서화)

daemon 없이도 같은 결론을 종이 위에서 검증할 수 있다:

1. 두 Dockerfile 의 step 목록을 세로로 나란히 적는다.
2. 각 step 의 cache key 를 적는다 — `FROM`/`WORKDIR`: 문자열, `COPY`: 대상 파일 내용 checksum, `RUN`: 명령 문자열. 모든 key 는 **부모 layer 의 key 를 누적 포함**한다.
3. "src/main.py 1줄 수정" 이벤트에 대해: bad 는 `COPY . .` 의 checksum 이 바뀌므로 그 step 부터 전부 miss; good 은 `COPY deps.txt` 가 hit 이므로 install 까지 hit, `COPY src/` 부터만 miss — 를 key 비교로 표시한다.
4. "deps.txt 수정" 이벤트에 대해 같은 표를 만들어 good 도 install 부터 miss 임을 확인한다.

이 표가 곧 `docker build --progress=plain` 출력의 `CACHED` 마크와 일대일 대응한다.

## 파일 목록

```
lab/
├── README.md                      # 이 문서
├── git-plumbing.sh                # Lab 1 (self-verifying, 26 asserts)
└── docker-layer-cache/
    ├── run-experiment.sh          # Lab 2 (self-verifying)
    ├── Dockerfile.bad             # COPY . . 먼저 — 잘못된 순서
    ├── Dockerfile.good            # deps 먼저 — 올바른 순서
    ├── deps.txt                   # 가짜 dependency manifest
    ├── src/main.py                # 실험이 수정했다 복구하는 소스
    └── .dockerignore
```
