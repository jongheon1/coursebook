#!/usr/bin/env bash
# Lab 2 — Dockerfile layer cache: instruction order decides what survives a change
#
# Protocol:
#   1. Cold-build Dockerfile.bad and Dockerfile.good with --no-cache.
#   2. Edit ONLY src/main.py (a source-only change).
#   3. Rebuild both WITH cache and compare: which build re-runs the
#      3-second "install" step, and which gets CACHED?
#   4. Edit deps.txt and rebuild good: show that a manifest change
#      invalidates the install step and everything after it (cascade).
#
# Usage: bash run-experiment.sh          (from this directory)
# Requires: docker with BuildKit (any modern Docker Desktop / Engine).
# Cleans up its images and file edits on exit; the alpine base image is kept.

set -euo pipefail
cd "$(dirname "$0")"

command -v docker >/dev/null || { echo "docker not found — see lab/README.md for the no-docker walkthrough"; exit 1; }
docker info >/dev/null 2>&1   || { echo "docker daemon not reachable — start it and retry"; exit 1; }

BAD_IMG=se-w4-cache-bad
GOOD_IMG=se-w4-cache-good
LOG_DIR=$(mktemp -d "${TMPDIR:-/tmp}/docker-lab.XXXXXX")

now_ms() { perl -MTime::HiRes=time -e 'printf "%d", time()*1000'; }

cleanup() {
  git checkout -q -- src/main.py deps.txt 2>/dev/null \
    || { sed -i.bak '/# touched by experiment/d' src/main.py 2>/dev/null; rm -f src/main.py.bak
         sed -i.bak '/^leftpad==/d' deps.txt 2>/dev/null; rm -f deps.txt.bak; }
  docker rmi -f "$BAD_IMG" "$GOOD_IMG" >/dev/null 2>&1 || true
  rm -rf "$LOG_DIR"
}
trap cleanup EXIT

build() { # build <dockerfile> <tag> <logfile>  -> echoes elapsed ms
  local t0 t1
  t0=$(now_ms)
  docker build --progress=plain -f "$1" -t "$2" . >"$LOG_DIR/$3" 2>&1
  t1=$(now_ms)
  echo $((t1 - t0))
}

# Was the RUN install step served from cache in this build log?
# BuildKit prints steps as "#N [k/m] RUN ..." and, if cached, "#N CACHED".
install_cached() { # install_cached <logfile>
  local n
  n=$(grep -Eo '^#[0-9]+ \[[0-9]+/[0-9]+\] RUN' "$LOG_DIR/$1" | head -1 | grep -Eo '^#[0-9]+' || true)
  [ -n "$n" ] && grep -q "^$n CACHED" "$LOG_DIR/$1" && echo yes || echo no
}

echo "== 1. Cold builds (--no-cache) =="
docker build --no-cache -q -f Dockerfile.bad  -t "$BAD_IMG"  . >/dev/null
docker build --no-cache -q -f Dockerfile.good -t "$GOOD_IMG" . >/dev/null
echo "   both images built cold (install step ran in both, ~3 s each)"

echo
echo "== 2. Source-only change: edit src/main.py =="
printf '# touched by experiment %s\n' "$(date +%s)" >> src/main.py

BAD_MS=$( build Dockerfile.bad  "$BAD_IMG"  rebuild-bad.log)
GOOD_MS=$(build Dockerfile.good "$GOOD_IMG" rebuild-good.log)
BAD_CACHED=$(install_cached rebuild-bad.log)
GOOD_CACHED=$(install_cached rebuild-good.log)

echo
printf '   %-18s %-14s %s\n' "rebuild" "install step" "wall time"
printf '   %-18s %-14s %s\n' "------------------" "------------" "---------"
printf '   %-18s %-14s %s ms\n' "Dockerfile.bad"  "$([ "$BAD_CACHED"  = yes ] && echo CACHED || echo re-ran)" "$BAD_MS"
printf '   %-18s %-14s %s ms\n' "Dockerfile.good" "$([ "$GOOD_CACHED" = yes ] && echo CACHED || echo re-ran)" "$GOOD_MS"

echo
echo "   BuildKit log for the good rebuild (RUN step is CACHED):"
grep -E '^#[0-9]+ (\[[0-9]+/[0-9]+\] (COPY|RUN)|CACHED)' "$LOG_DIR/rebuild-good.log" | sed 's/^/     /'

FAIL=0
[ "$BAD_CACHED"  = no  ] || { echo "ASSERT FAIL: bad build should have re-run the install"; FAIL=1; }
[ "$GOOD_CACHED" = yes ] || { echo "ASSERT FAIL: good build should have CACHED the install"; FAIL=1; }
[ "$GOOD_MS" -lt "$BAD_MS" ] || { echo "ASSERT FAIL: good rebuild should be faster"; FAIL=1; }

echo
echo "== 3. Manifest change: edit deps.txt =="
# Unique per run: BuildKit's build cache survives across runs (docker rmi does
# not clear it), so a deterministic line would content-match a previous run's
# layer and come back CACHED.
printf 'leftpad==1.0.%s\n' "$(date +%s)" >> deps.txt
GOOD2_MS=$(build Dockerfile.good "$GOOD_IMG" rebuild-good-deps.log)
GOOD2_CACHED=$(install_cached rebuild-good-deps.log)
printf '   Dockerfile.good after deps.txt change: install %s, %s ms\n' \
  "$([ "$GOOD2_CACHED" = yes ] && echo CACHED || echo re-ran)" "$GOOD2_MS"
echo "   -> COPY deps.txt got a new content checksum; that step and every later step re-ran (cascade)."
[ "$GOOD2_CACHED" = no ] || { echo "ASSERT FAIL: deps change must invalidate the install"; FAIL=1; }

echo
echo "== 4. Layers are the image: docker history $GOOD_IMG =="
docker history --format 'table {{.CreatedBy}}\t{{.Size}}' "$GOOD_IMG" | head -8 | sed 's/^/   /'

echo
if [ "$FAIL" -eq 0 ]; then
  echo "All assertions passed."
else
  echo "Some assertions FAILED."; exit 1
fi
