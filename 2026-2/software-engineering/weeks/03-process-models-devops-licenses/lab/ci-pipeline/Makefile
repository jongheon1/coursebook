# Mini CI pipeline: lint -> unit test -> build, with per-stage failure semantics.
#
#   make ci          run the whole pipeline (incremental: green stages are skipped)
#   make break-test  inject a logic fault  -> pipeline must go red at stage 2
#   make break-lint  inject style faults   -> pipeline must go red at stage 1
#   make fix         restore the good source
#   make clean       remove stamps and artifacts
#
# Stage results are recorded as stamp files under .ci/ — make's dependency
# graph is the pipeline: a stage only runs if its inputs changed or an
# earlier stage was re-run. That is exactly how real CI caches stages.

PY      := python3
SRC     := $(wildcard src/*.py)
TESTS   := $(wildcard tests/*.py)
STAMPS  := .ci
DIST    := dist
BACKUP  := $(STAMPS)/semver.py.orig

.PHONY: ci clean break-test break-lint fix

ci: $(STAMPS)/build.ok
	@echo "=================================================="
	@echo "CI GREEN — release candidate: $(DIST)/app.tar.gz"
	@cat $(DIST)/SHA256SUMS

$(STAMPS):
	@mkdir -p $(STAMPS)

# ---- Stage 1: commit-stage lint -----------------------------------------
# Failure meaning: code-local convention/syntax defect. The committer can
# fix it immediately; nothing further runs (fast feedback is the point).
$(STAMPS)/lint.ok: $(SRC) tools/lint.py | $(STAMPS)
	@echo "[stage 1/3] lint"
	@$(PY) tools/lint.py src || { \
	  echo "[stage 1/3] FAILED — meaning: code-local convention/syntax defect."; \
	  echo "            Fix and re-run; later stages did not run."; exit 1; }
	@touch $@
	@echo "[stage 1/3] OK"

# ---- Stage 2: unit tests -------------------------------------------------
# Failure meaning: a unit's logic is wrong. Lint cannot see this class of
# defect; the self-testing build (Fowler) is what catches it.
$(STAMPS)/test.ok: $(STAMPS)/lint.ok $(TESTS)
	@echo "[stage 2/3] unit tests"
	@$(PY) -m unittest discover -s tests -t . || { \
	  echo "[stage 2/3] FAILED — meaning: unit logic defect (lint was green)."; \
	  echo "            The build is broken; fixing it outranks new work."; exit 1; }
	@touch $@
	@echo "[stage 2/3] OK"

# ---- Stage 3: build the release artifact --------------------------------
# Only reached when stages 1-2 are green. Produces the single immutable
# artifact later stages would reuse (12-factor V: build/release/run).
$(STAMPS)/build.ok: $(STAMPS)/test.ok
	@echo "[stage 3/3] build"
	@mkdir -p $(DIST)
	@tar -czf $(DIST)/app.tar.gz src
	@$(PY) -c "import hashlib,pathlib; p=pathlib.Path('$(DIST)/app.tar.gz'); \
	  print(hashlib.sha256(p.read_bytes()).hexdigest(), ' ', p.name)" > $(DIST)/SHA256SUMS
	@touch $@
	@echo "[stage 3/3] OK — artifact + checksum written"

# ---- Fault injection -----------------------------------------------------
break-test: fix | $(STAMPS)
	@cp src/semver.py $(BACKUP)
	@cp faults/semver_buggy.py src/semver.py
	@rm -f $(STAMPS)/*.ok
	@echo "Injected LOGIC fault into src/semver.py — run 'make ci' (expect stage 2 to fail)"

break-lint: fix | $(STAMPS)
	@cp src/semver.py $(BACKUP)
	@cp faults/semver_lint.py src/semver.py
	@rm -f $(STAMPS)/*.ok
	@echo "Injected LINT faults into src/semver.py — run 'make ci' (expect stage 1 to fail)"

fix:
	@if [ -f $(BACKUP) ]; then \
	  mv $(BACKUP) src/semver.py; \
	  rm -f $(STAMPS)/*.ok; \
	  echo "Restored good src/semver.py"; \
	fi

clean:
	@rm -rf $(STAMPS) $(DIST)
	@find . -name __pycache__ -type d -exec rm -rf {} + 2>/dev/null || true
	@echo "cleaned"
