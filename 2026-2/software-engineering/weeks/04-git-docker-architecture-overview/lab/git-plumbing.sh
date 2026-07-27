#!/usr/bin/env bash
# Lab 1 — Git plumbing: object model, refs, three-way merge, reflog recovery
#
# Creates a throwaway repo in a temp dir and walks through Git's storage layer
# with plumbing commands (hash-object, cat-file, ls-tree, ls-files, merge-base).
# Every claim in the chapter's §1 is asserted here — the script exits non-zero
# if any assertion fails.
#
# Usage: bash git-plumbing.sh
# Requires: git >= 2.23 (uses `git switch`), shasum or sha1sum.

set -euo pipefail

# ---------- helpers ----------
PASS=0
step() { printf '\n\033[1;34m== %s ==\033[0m\n' "$*"; }
say()  { printf '%s\n' "$*"; }
assert_eq() { # assert_eq <label> <expected> <actual>
  if [ "$2" = "$3" ]; then
    PASS=$((PASS+1)); printf '  \033[32mOK\033[0m  %s\n' "$1"
  else
    printf '  \033[31mFAIL\033[0m %s\n    expected: %s\n    actual:   %s\n' "$1" "$2" "$3"
    exit 1
  fi
}
sha1() { if command -v shasum >/dev/null; then shasum | cut -d' ' -f1; else sha1sum | cut -d' ' -f1; fi; }

LAB_DIR=$(mktemp -d "${TMPDIR:-/tmp}/git-lab.XXXXXX")
trap 'rm -rf "$LAB_DIR"' EXIT
cd "$LAB_DIR"

git -c init.defaultBranch=main init -q repo
cd repo
git config user.name  "Lab Student"
git config user.email "lab@example.invalid"
git config commit.gpgsign false

# =====================================================================
step "A1. A blob's name is SHA-1 of 'blob <size>\\0' + content"
# ---------------------------------------------------------------------
CONTENT='hello, git'                       # git will see "hello, git\n" (11 bytes)
GIT_HASH=$(printf '%s\n' "$CONTENT" | git hash-object --stdin)
MANUAL_HASH=$(printf 'blob 11\0%s\n' "$CONTENT" | sha1)
say "  git hash-object : $GIT_HASH"
say "  manual sha1     : $MANUAL_HASH"
assert_eq "blob id == sha1(header + content)" "$GIT_HASH" "$MANUAL_HASH"

# =====================================================================
step "A2. -w stores the object under .git/objects/<2>/<38>, zlib-deflated"
# ---------------------------------------------------------------------
printf '%s\n' "$CONTENT" > greeting.txt
BLOB=$(git hash-object -w greeting.txt)
OBJ_PATH=".git/objects/${BLOB:0:2}/${BLOB:2}"
say "  object file: $OBJ_PATH ($(wc -c < "$OBJ_PATH" | tr -d ' ') bytes on disk, content is 11 bytes)"
assert_eq "loose object file exists"        "yes"  "$([ -f "$OBJ_PATH" ] && echo yes)"
assert_eq "cat-file -t sees a blob"         "blob" "$(git cat-file -t "$BLOB")"
assert_eq "cat-file -s sees logical size"   "11"   "$(git cat-file -s "$BLOB")"
say "  cat-file -p: $(git cat-file -p "$BLOB")"

# =====================================================================
step "A3. git add = hash-object -w + index entry (no tree/commit yet)"
# ---------------------------------------------------------------------
git add greeting.txt
say "  index (git ls-files --stage):"
git ls-files --stage | sed 's/^/    /'
INDEX_BLOB=$(git ls-files --stage | awk '{print $2}')
assert_eq "index points at the same blob" "$BLOB" "$INDEX_BLOB"
assert_eq "object DB has no tree/commit yet" "1" "$(git cat-file --batch-all-objects --batch-check='%(objecttype)' | sort -u | wc -l | tr -d ' ')"

# =====================================================================
step "A4. commit = tree (+ nested tree per directory) + metadata"
# ---------------------------------------------------------------------
mkdir src
printf 'fn main() {}\n' > src/main.rs
git add src/main.rs
git commit -qm "C0: initial"
say "  commit object (git cat-file -p HEAD):"
git cat-file -p HEAD | sed 's/^/    /'
say "  root tree (git cat-file -p HEAD^{tree}):"
git cat-file -p 'HEAD^{tree}' | sed 's/^/    /'
say "  recursive listing (git ls-tree -r HEAD):"
git ls-tree -r HEAD | sed 's/^/    /'
SUBTREE_TYPE=$(git cat-file -p 'HEAD^{tree}' | awk '$4=="src"{print $2}')
assert_eq "directory 'src' is a nested tree object" "tree" "$SUBTREE_TYPE"
assert_eq "tree references the exact blob from A2" "$BLOB" "$(git ls-tree HEAD -- greeting.txt | awk '{print $3}')"

# =====================================================================
step "A5. Content addressing deduplicates: same content => same blob"
# ---------------------------------------------------------------------
cp greeting.txt copy-of-greeting.txt
git add copy-of-greeting.txt
git commit -qm "C1: duplicate content"
assert_eq "two paths, one blob" "$BLOB" "$(git ls-tree HEAD -- copy-of-greeting.txt | awk '{print $3}')"
say "  (the object DB stores 'hello, git\\n' exactly once, whatever the path or commit)"

# =====================================================================
step "A6. Refs and HEAD are tiny files; a branch costs ~41 bytes"
# ---------------------------------------------------------------------
say "  .git/HEAD            : $(cat .git/HEAD)"
say "  .git/refs/heads/main : $(cat .git/refs/heads/main)"
BRANCH_BYTES=$(wc -c < .git/refs/heads/main | tr -d ' ')
say "  branch file size     : $BRANCH_BYTES bytes"
assert_eq "branch = 40-hex SHA-1 + newline" "41" "$BRANCH_BYTES"
git branch topic
assert_eq "new branch = new 41-byte file, same commit" "$(git rev-parse main)" "$(git rev-parse topic)"

# =====================================================================
step "A7. Annotated tag is a 4th object type pointing at a commit"
# ---------------------------------------------------------------------
git tag -a v0.1 -m "first release"
assert_eq "tag ref points at a 'tag' object" "tag" "$(git cat-file -t v0.1)"
say "  tag object payload:"
git cat-file -p v0.1 | sed 's/^/    /'
assert_eq "lightweight tag would point at 'commit' instead" "commit" "$(git cat-file -t 'v0.1^{commit}')"

# =====================================================================
step "A8. Detached HEAD = HEAD holds a raw commit id, not a symref"
# ---------------------------------------------------------------------
git checkout -q --detach HEAD
say "  .git/HEAD now: $(cat .git/HEAD)"
assert_eq "HEAD no longer says 'ref: ...'" "" "$(grep '^ref:' .git/HEAD || true)"
git switch -q main

# =====================================================================
step "B1. Three-way merge, non-overlapping edits: auto-merge"
# ---------------------------------------------------------------------
# Base file: 9 numbered lines. 'left' edits line 1, 'right' edits line 9.
seq -f 'line %g' 1 9 > poem.txt
git add poem.txt && git commit -qm "C2: base for merge"
BASE_COMMIT=$(git rev-parse HEAD)

git switch -qc left
sed -i.bak 's/^line 1$/line 1 (edited on left)/' poem.txt && rm poem.txt.bak
git commit -qam "L: edit line 1"

git switch -q main && git switch -qc right
sed -i.bak 's/^line 9$/line 9 (edited on right)/' poem.txt && rm poem.txt.bak
git commit -qam "R: edit line 9"

MB=$(git merge-base left right)
say "  merge-base(left, right) = $MB"
assert_eq "merge base is the fork-point commit C2" "$BASE_COMMIT" "$MB"

git merge -q --no-edit left
assert_eq "left's change survived"  "line 1 (edited on left)"  "$(sed -n 1p poem.txt)"
assert_eq "right's change survived" "line 9 (edited on right)" "$(sed -n 9p poem.txt)"
NPARENTS=$(git cat-file -p HEAD | grep -c '^parent')
assert_eq "merge commit has 2 parents" "2" "$NPARENTS"
say "  each side changed a different region relative to base => both taken, no conflict"

# =====================================================================
step "B2. Conflict = both sides changed the SAME region differently vs base"
# ---------------------------------------------------------------------
git switch -q main
git merge -q --no-edit right 2>/dev/null   # fast-forward-ish catch-up of main
BASE2=$(git rev-parse HEAD)

git switch -qc ours
sed -i.bak 's/^line 5$/line 5 says OURS/' poem.txt && rm poem.txt.bak
git commit -qam "O: line 5 -> OURS"

git switch -q main && git switch -qc theirs
sed -i.bak 's/^line 5$/line 5 says THEIRS/' poem.txt && rm poem.txt.bak
git commit -qam "T: line 5 -> THEIRS"

git switch -q ours
assert_eq "merge base is where ours/theirs forked" "$BASE2" "$(git merge-base ours theirs)"

if git merge --no-edit theirs 2>/dev/null; then
  say "  UNEXPECTED: merge succeeded"; exit 1
else
  say "  merge stopped with a conflict, as expected"
fi

say "  index now holds THREE stages for poem.txt (git ls-files -u):"
git ls-files -u | sed 's/^/    /'
NSTAGES=$(git ls-files -u | awk '{print $3}' | sort -u | tr '\n' ' ')
assert_eq "stages present are 1(base) 2(ours) 3(theirs)" "1 2 3 " "$NSTAGES"
say "  stage 1 (base)  line 5: $(git cat-file -p :1:poem.txt | sed -n 5p)"
say "  stage 2 (ours)  line 5: $(git cat-file -p :2:poem.txt | sed -n 5p)"
say "  stage 3 (theirs)line 5: $(git cat-file -p :3:poem.txt | sed -n 5p)"
say "  working tree got conflict markers:"
grep -n -A2 '^<<<<<<<' poem.txt | sed 's/^/    /'

# resolve: pick ours' line, keep going
sed -i.bak '/^<<<<<<</d; /^=======/,/^>>>>>>>/d' poem.txt && rm poem.txt.bak
git add poem.txt
git commit -qm "M: resolve line 5 in favor of OURS"
assert_eq "resolution recorded; index back to 1 stage" "" "$(git ls-files -u)"

# =====================================================================
step "B3. Fast-forward: no new commit when target is a descendant"
# ---------------------------------------------------------------------
git switch -q main
BEFORE=$(git rev-parse HEAD)
git switch -qc ff-topic
printf 'note\n' > note.txt && git add note.txt && git commit -qm "F: add note"
TOPIC_TIP=$(git rev-parse HEAD)
git switch -q main
git merge -q --ff-only ff-topic
assert_eq "main moved to the topic tip (no merge commit)" "$TOPIC_TIP" "$(git rev-parse HEAD)"
assert_eq "merge-base(main@before, topic) was main itself" "$BEFORE" "$(git merge-base "$BEFORE" ff-topic)"

# =====================================================================
step "B4. Reflog: 'destroyed' commits are recoverable"
# ---------------------------------------------------------------------
printf 'precious work\n' > precious.txt
git add precious.txt && git commit -qm "P: precious commit"
LOST=$(git rev-parse HEAD)
git reset -q --hard HEAD~1                 # "oops"
assert_eq "commit is gone from the branch" "" "$(git log --oneline | grep -o 'P: precious commit' || true)"
say "  reflog still remembers where HEAD was:"
git reflog -3 | sed 's/^/    /'
git reset -q --hard 'HEAD@{1}'
assert_eq "recovered the exact commit object" "$LOST" "$(git rev-parse HEAD)"
assert_eq "file is back" "precious work" "$(cat precious.txt)"

# =====================================================================
printf '\n\033[1;32mAll %d assertions passed.\033[0m\n' "$PASS"
say "Temp repo was created in $LAB_DIR (removed on exit)."
