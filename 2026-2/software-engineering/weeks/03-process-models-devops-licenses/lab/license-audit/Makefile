# License audit lab.
#
#   make test           unit tests for classification and verdict logic
#   make audit-internal expected: PASS (exit 0) — no conveying
#   make audit-saas     expected: PASS (exit 0) — GPL dep is only a latent WARN
#   make audit-saas-mod expected: FAIL (exit 1) — modified AGPL, s13 triggers
#   make audit-binary   expected: FAIL (exit 1) — conveying a GPL combined work
#   make audit-unknown  expected: FAIL (exit 1) — unresolved license blocks
#   make demo           run all five in order (continues past expected failures)

PY := python3
AUDIT := $(PY) audit.py --requirements requirements-sample.txt --db licenses.json

.PHONY: test audit-internal audit-saas audit-saas-mod audit-binary audit-unknown demo clean

test:
	@$(PY) -m unittest -v test_audit

audit-internal:
	@$(AUDIT) --scenario scenario-internal.json

audit-saas:
	@$(AUDIT) --scenario scenario-saas.json

audit-saas-mod:
	@$(AUDIT) --scenario scenario-saas-modified.json

audit-binary:
	@$(AUDIT) --scenario scenario-binary.json

audit-unknown:
	@$(PY) audit.py --requirements requirements-unknown.txt --db licenses.json \
	  --scenario scenario-internal.json

demo:
	@$(MAKE) --no-print-directory audit-internal; echo "exit=$$?"; echo
	@$(MAKE) --no-print-directory audit-saas; echo "exit=$$?"; echo
	@-$(MAKE) --no-print-directory audit-saas-mod; echo "exit=$$?"; echo
	@-$(MAKE) --no-print-directory audit-binary; echo "exit=$$?"; echo
	@-$(MAKE) --no-print-directory audit-unknown; echo "exit=$$?"

clean:
	@find . -name __pycache__ -type d -exec rm -rf {} + 2>/dev/null || true
	@echo "cleaned"
