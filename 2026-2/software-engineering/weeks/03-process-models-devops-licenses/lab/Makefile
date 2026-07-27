# Top-level driver for both labs.
#
#   make verify   run the full self-check of both labs, asserting expected
#                 successes AND expected failures. Exits 0 only if every
#                 assertion holds.

.PHONY: verify clean

verify:
	@echo "### Lab 1: CI pipeline — green path"
	@$(MAKE) --no-print-directory -C ci-pipeline clean ci >/dev/null 2>&1
	@echo "ok: pipeline green"
	@echo "### Lab 1: logic fault must fail at stage 2"
	@$(MAKE) --no-print-directory -C ci-pipeline break-test >/dev/null
	@! $(MAKE) --no-print-directory -C ci-pipeline ci >/dev/null 2>&1
	@echo "ok: pipeline red on logic fault"
	@echo "### Lab 1: lint fault must fail at stage 1"
	@$(MAKE) --no-print-directory -C ci-pipeline break-lint >/dev/null
	@! $(MAKE) --no-print-directory -C ci-pipeline ci >/dev/null 2>&1
	@echo "ok: pipeline red on lint fault"
	@$(MAKE) --no-print-directory -C ci-pipeline fix >/dev/null
	@$(MAKE) --no-print-directory -C ci-pipeline ci >/dev/null 2>&1
	@echo "ok: pipeline green again after fix"
	@echo "### Lab 2: audit unit tests"
	@$(MAKE) --no-print-directory -C license-audit test >/dev/null 2>&1
	@echo "ok: audit tests pass"
	@echo "### Lab 2: scenario outcomes"
	@$(MAKE) --no-print-directory -C license-audit audit-internal >/dev/null
	@$(MAKE) --no-print-directory -C license-audit audit-saas >/dev/null
	@! $(MAKE) --no-print-directory -C license-audit audit-saas-mod >/dev/null 2>&1
	@! $(MAKE) --no-print-directory -C license-audit audit-binary >/dev/null 2>&1
	@! $(MAKE) --no-print-directory -C license-audit audit-unknown >/dev/null 2>&1
	@echo "ok: internal/saas pass; saas-modified/binary/unknown blocked"
	@echo "=================================================="
	@echo "ALL LAB ASSERTIONS PASSED"

clean:
	@$(MAKE) --no-print-directory -C ci-pipeline clean
	@$(MAKE) --no-print-directory -C license-audit clean
