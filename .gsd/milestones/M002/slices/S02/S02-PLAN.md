# S02: Rule Analysis & Compliance Skills

**Goal:** Deliver 3 skills — `acl-rule-analysis` (R021), `cis-benchmark-audit` (R022), `nist-compliance-assessment` (R023) — each with `metadata.safety: read-only`, 7 required H2 sections, `references/` with exactly 2 files, and ≤2700 body words. Retire the CIS copyright-safe reference approach (D026 key risk).
**Demo:** `bash scripts/validate.sh` passes 19 skills (16 existing + 3 new) with 0 errors. ACL rule analysis skill detects shadowed/overly permissive rules with multi-vendor inline labels. CIS benchmark skill references actual control IDs in `references/control-reference.md` without reproducing copyrighted text. NIST skill maps network security to CSF Protect/Detect functions with 800-53 control families.

## Must-Haves

- `acl-rule-analysis` SKILL.md with shadowed rule detection, overly permissive rule flagging, unused rule detection, rule ordering optimization — vendor-agnostic patterns with `[Cisco]`/`[JunOS]`/`[EOS]`/`[PAN-OS]`/`[FortiGate]`/`[CheckPoint]` inline labels
- `cis-benchmark-audit` SKILL.md with compliance assessment procedure covering Management Plane, Control Plane, Data Plane for Cisco IOS, PAN-OS, JunOS, Check Point
- `cis-benchmark-audit/references/control-reference.md` citing CIS control IDs + categories only — NO reproduced benchmark text, remediation steps, or rationale (D026 constraint)
- `nist-compliance-assessment` SKILL.md mapping 6 NIST 800-53 control families (AC, AU, CM, IA, SC, SI) to network device audit checks with CSF function mapping (PR/DE focus)
- All 3 skills: frontmatter with `metadata.safety: read-only`, body ≤2700 words, `references/` with exactly 2 files
- All 3 skills pass `bash scripts/validate.sh` (7 required H2 sections validated)
- README catalog updated with 3 new rows under existing "Security Skills" separator
- Zero regression on existing 16 skills

## Verification

```bash
# Full validation — 19 skills, 0 errors
bash scripts/validate.sh
# Expected: "Skills checked: 19" and "Result: PASS (0 errors)"

# Word counts ≤2700 for all 3 new skills
for s in acl-rule-analysis cis-benchmark-audit nist-compliance-assessment; do
  echo "$s: $(awk 'BEGIN{c=0} /^---$/{c++; if(c==2){found=1; next}} found{print}' skills/$s/SKILL.md | wc -w) words"
done

# Reference file counts (exactly 2 per skill)
for s in acl-rule-analysis cis-benchmark-audit nist-compliance-assessment; do
  echo "$s: $(ls skills/$s/references/ | wc -l) ref files"
done

# README has 3 new rows
grep -c 'rule-analysis\|benchmark-audit\|compliance-assessment' README.md  # must be 3

# CIS copyright-safe check — control IDs present, no benchmark text reproduced
grep -c '\.[0-9]' skills/cis-benchmark-audit/references/control-reference.md  # many control IDs

# Content depth checks
grep -l 'shadowed' skills/acl-rule-analysis/SKILL.md        # ACL rule analysis depth
grep -l 'CIS' skills/cis-benchmark-audit/SKILL.md           # CIS references
grep -l 'NIST\|800-53\|CSF' skills/nist-compliance-assessment/SKILL.md  # NIST mapping

# No regression — 0 errors total
bash scripts/validate.sh 2>&1 | grep -c 'ERROR:'  # must be 0

# Failure-path / diagnostic checks
# 1. Verify validate.sh detects a broken skill (missing required section)
mkdir -p /tmp/nss-diag-test/skills/broken-test-skill/references
echo -e "---\nname: broken-test-skill\ncategory: test\ndifficulty: beginner\nestimated_time: 5 minutes\nmetadata:\n  safety: read-only\n---\n# Only one section\nNo real content." > /tmp/nss-diag-test/skills/broken-test-skill/SKILL.md
# Running validate.sh against a skill missing 6 of 7 required H2 sections must produce ERROR lines
bash scripts/validate.sh /tmp/nss-diag-test/skills/broken-test-skill 2>&1 | grep -c 'ERROR:'  # must be >0 (confirms failure detection works)
rm -rf /tmp/nss-diag-test

# 2. Verify structured error output is parseable — each ERROR line includes skill name and check
bash scripts/validate.sh 2>&1 | grep -E '(OK|ERROR):' | head -5  # confirm structured per-check output

# 3. Verify validate.sh exits non-zero on failure (regression guard)
bash scripts/validate.sh 2>&1 > /dev/null; echo "exit: $?"  # must be 0 for passing suite

# 4. Diagnostic: isolate per-skill failures for targeted debugging
bash scripts/validate.sh 2>&1 | grep 'ERROR:' | awk -F: '{print $2}' | sort -u  # list failing skill names (empty = all pass)
```

## Observability / Diagnostics

- **Validation surface:** `bash scripts/validate.sh` — single command reports skill count, per-skill section/frontmatter/reference checks, and total error count. Output is structured (OK/ERROR per check) for agent parsing.
- **Word budget inspection:** `awk 'BEGIN{c=0} /^---$/{c++; if(c==2){found=1; next}} found{print}' skills/<name>/SKILL.md | wc -w` — per-skill body word count. Exceeding 2700 is a hard fail.
- **Reference file count:** `ls skills/<name>/references/ | wc -l` — must be exactly 2 per skill. Missing or extra files indicate incomplete or over-scoped delivery.
- **Content depth grep:** `grep -l '<keyword>' skills/<name>/SKILL.md` — quick check that key concepts (shadowed, CIS, NIST) are present in the right skills.
- **Failure visibility:** validate.sh prints `ERROR:` lines to stderr for each failing check with the skill name and specific check that failed. `grep -c 'ERROR:' <(bash scripts/validate.sh 2>&1)` gives a scalar failure count.
- **Regression detection:** validate.sh checks ALL skills (not just new ones), so any regression in existing M001 skills surfaces immediately as an error count increase.
- **Failure-path verification:** To confirm validate.sh correctly detects broken skills, create a minimal broken skill (`mkdir -p /tmp/nss-diag-test/skills/broken-test-skill/references && echo '---\nname: broken-test-skill\n---\n# Only intro' > /tmp/nss-diag-test/skills/broken-test-skill/SKILL.md`) and run `bash scripts/validate.sh /tmp/nss-diag-test/skills/broken-test-skill 2>&1 | grep -c 'ERROR:'` — must return >0. Structured output is parseable via `grep -E '(OK|ERROR):' | head -5`. Exit code is 0 only for passing suites (`bash scripts/validate.sh 2>&1 > /dev/null; echo "exit: $?"`).

## Tasks

- [x] **T01: Build vendor-agnostic ACL rule analysis skill with multi-vendor inline labels** `est:30m`
  - Why: Delivers R021. Extends S01's "policy audit" procedure shape to vendor-agnostic rule pattern analysis (shadowed rules, overly permissive rules, unused rules, rule ordering). Proves multi-vendor inline labeling works for security audit skills with 6 vendor labels.
  - Files: `skills/acl-rule-analysis/SKILL.md`, `skills/acl-rule-analysis/references/cli-reference.md`, `skills/acl-rule-analysis/references/rule-patterns.md`
  - Do: Create SKILL.md with frontmatter (`name: acl-rule-analysis`, `metadata.safety: read-only`), 7 required H2 sections. Procedure: collect rulebase → identify shadowed rules → detect overly permissive rules → find unused rules → identify redundant/duplicate rules → rule ordering optimization → generate recommendations. Use `[Cisco]`/`[JunOS]`/`[EOS]`/`[PAN-OS]`/`[FortiGate]`/`[CheckPoint]` inline labels for vendor-specific CLI commands. Threshold Tables: "Rule Risk Severity" classification. References: `cli-reference.md` (multi-vendor ACL retrieval commands in table format), `rule-patterns.md` (rule analysis pattern definitions with detection algorithms). Body ≤2700 words.
  - Verify: `bash scripts/validate.sh` (17 skills, 0 errors), `awk 'BEGIN{c=0} /^---$/{c++; if(c==2){found=1; next}} found{print}' skills/acl-rule-analysis/SKILL.md | wc -w` ≤2700, `ls skills/acl-rule-analysis/references/ | wc -l` = 2
  - Done when: validate.sh reports 17 skills with 0 errors, body ≤2700 words, 2 reference files exist, skill contains "shadowed" and multi-vendor inline labels

- [x] **T02: Build CIS benchmark audit skill with copyright-safe control reference** `est:40m`
  - Why: Delivers R022. Retires M002's #2 key risk (D026 — CIS copyright-safe reference strategy). Must prove that citing control IDs + categories without reproducing benchmark text produces actionable audit guidance. Introduces "compliance assessment" procedure shape (D028).
  - Files: `skills/cis-benchmark-audit/SKILL.md`, `skills/cis-benchmark-audit/references/control-reference.md`, `skills/cis-benchmark-audit/references/cli-reference.md`
  - Do: Create SKILL.md with frontmatter (`name: cis-benchmark-audit`, `metadata.safety: read-only`), 7 required H2 sections. Procedure (compliance assessment shape): platform identification → Management Plane audit (SSH, AAA, NTP, logging, SNMP, banner) → Control Plane audit (routing protocol auth, CoPP, ICMP) → Data Plane audit (ACLs, uRPF, storm control, port security, encryption) → compliance scoring → priority remediation plan. Cover Cisco IOS, PAN-OS, JunOS, Check Point per-vendor sections. Threshold Tables: "Compliance Violation Severity" scored by CIS control level. References: `control-reference.md` — **COPYRIGHT-SAFE**: table mapping CIS section IDs to categories and config areas to check, WITHOUT reproducing benchmark text/remediation/rationale. Target ~30-40 high-impact controls. `cli-reference.md` — read-only audit commands by CIS category per platform. Body ≤2700 words.
  - Verify: `bash scripts/validate.sh` (18 skills, 0 errors), body ≤2700 words, 2 reference files, `grep -c '\.[0-9]' skills/cis-benchmark-audit/references/control-reference.md` shows many control IDs, manual scan confirms no reproduced CIS benchmark text
  - Done when: validate.sh reports 18 skills with 0 errors, body ≤2700 words, control-reference.md contains CIS control IDs without reproducing benchmark text, "CIS" appears in SKILL.md

- [x] **T03: Build NIST compliance assessment skill with 800-53 control family mapping** `est:30m`
  - Why: Delivers R023. Builds on compliance assessment procedure shape proven in T02. NIST SP 800-53 and CSF are public-domain US government publications — no copyright constraint. Maps 6 control families (AC, AU, CM, IA, SC, SI) to concrete network device audit checks.
  - Files: `skills/nist-compliance-assessment/SKILL.md`, `skills/nist-compliance-assessment/references/control-reference.md`, `skills/nist-compliance-assessment/references/cli-reference.md`
  - Do: Create SKILL.md with frontmatter (`name: nist-compliance-assessment`, `metadata.safety: read-only`), 7 required H2 sections. Procedure (compliance assessment shape): scope assessment and framework selection (CSF vs 800-53) → Access Control (AC) assessment → Audit and Accountability (AU) → Configuration Management (CM) → Identification and Authentication (IA) → System and Communications Protection (SC) → System and Information Integrity (SI). Focus on CSF Protect (PR) and Detect (DE) functions. Vendor-agnostic with `[Cisco]`/`[JunOS]`/`[EOS]`/`[PAN-OS]` inline labels. Threshold Tables: "Control Gap Severity" by 800-53 impact level. Explicitly state scope is limited to 6 of 20 800-53 families (the ones with direct network device relevance). References: `control-reference.md` — NIST 800-53 control families mapped to network device audit checks with CSF function mapping. `cli-reference.md` — CLI commands organized by NIST control family per vendor. Body ≤2700 words.
  - Verify: `bash scripts/validate.sh` (19 skills, 0 errors), body ≤2700 words, 2 reference files, `grep -l 'NIST\|800-53\|CSF' skills/nist-compliance-assessment/SKILL.md` succeeds
  - Done when: validate.sh reports 19 skills with 0 errors, body ≤2700 words, SKILL.md references NIST 800-53 and CSF with concrete network audit mappings

- [x] **T04: Update README catalog and run full slice verification** `est:15m`
  - Why: Integrates 3 new skills into the README catalog table and runs comprehensive slice-level verification confirming all 19 skills pass, no M001 regression, word budgets met, CIS copyright safety validated, and content depth checks pass.
  - Files: `README.md`
  - Do: Add 3 new rows to README catalog table after line 45 (after the 4 firewall audit rows, under existing "Security Skills" separator). Row format matches existing table: `| [skill-name](skills/skill-name/SKILL.md) | Description | \`read-only\` |`. Descriptions should cite specific capabilities (e.g., "shadowed rule detection" not "rule analysis"). Run all slice-level verification checks from the Verification section above.
  - Verify: Full verification battery — `bash scripts/validate.sh` (19 skills, 0 errors), all 3 word counts ≤2700, all 3 have 2 reference files, `grep -c 'rule-analysis\|benchmark-audit\|compliance-assessment' README.md` = 3, `bash scripts/validate.sh 2>&1 | grep -c 'ERROR:'` = 0
  - Done when: README has 3 new catalog rows, validate.sh shows 19 skills with 0 errors, all slice verification checks pass

## Files Likely Touched

- `skills/acl-rule-analysis/SKILL.md`
- `skills/acl-rule-analysis/references/cli-reference.md`
- `skills/acl-rule-analysis/references/rule-patterns.md`
- `skills/cis-benchmark-audit/SKILL.md`
- `skills/cis-benchmark-audit/references/control-reference.md`
- `skills/cis-benchmark-audit/references/cli-reference.md`
- `skills/nist-compliance-assessment/SKILL.md`
- `skills/nist-compliance-assessment/references/control-reference.md`
- `skills/nist-compliance-assessment/references/cli-reference.md`
- `README.md`
