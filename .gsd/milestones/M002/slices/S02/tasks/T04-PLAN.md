---
estimated_steps: 4
estimated_files: 1
---

# T04: Update README catalog and run full slice verification

**Slice:** S02 — Rule Analysis & Compliance Skills
**Milestone:** M002

## Description

Add 3 new rows to the README catalog table for the skills created in T01–T03, then run the full slice-level verification battery confirming all 19 skills pass, no M001 regression, word budgets met, CIS copyright safety validated, and content depth checks pass.

The new rows go under the existing "Security Skills" bold separator row (line 41 of README.md), after the 4 firewall audit rows (lines 42–45). No new separator row is needed — S01 already created the "Security Skills" header.

## Steps

1. Edit `README.md` to add 3 new rows after line 45 (after the `cisco-firewall-audit` row). The rows should be:
   ```
   | [acl-rule-analysis](skills/acl-rule-analysis/SKILL.md) | Vendor-agnostic ACL/firewall rule analysis — shadowed rule detection, overly permissive rule flagging, unused rule cleanup, rule ordering optimization | `read-only` |
   | [cis-benchmark-audit](skills/cis-benchmark-audit/SKILL.md) | CIS benchmark compliance assessment — Management/Control/Data Plane audit for Cisco IOS, PAN-OS, JunOS, Check Point with copyright-safe control references | `read-only` |
   | [nist-compliance-assessment](skills/nist-compliance-assessment/SKILL.md) | NIST CSF and 800-53 compliance mapping — AC, AU, CM, IA, SC, SI control family assessment for network device security posture | `read-only` |
   ```

2. Run full validation:
   ```bash
   bash scripts/validate.sh
   # Expected: "Skills checked: 19" and "Result: PASS (0 errors)"
   ```

3. Run all word count checks:
   ```bash
   for s in acl-rule-analysis cis-benchmark-audit nist-compliance-assessment; do
     echo "$s: $(awk 'BEGIN{c=0} /^---$/{c++; if(c==2){found=1; next}} found{print}' skills/$s/SKILL.md | wc -w) words"
   done
   # All must be ≤2700
   ```

4. Run all content and structure checks:
   ```bash
   # README has 3 new rows
   grep -c 'rule-analysis\|benchmark-audit\|compliance-assessment' README.md  # must be 3

   # Reference file counts
   for s in acl-rule-analysis cis-benchmark-audit nist-compliance-assessment; do
     echo "$s: $(ls skills/$s/references/ | wc -l) ref files"
   done
   # All must be 2

   # CIS copyright check
   grep -c '\.[0-9]' skills/cis-benchmark-audit/references/control-reference.md  # many control IDs

   # Content depth
   grep -l 'shadowed' skills/acl-rule-analysis/SKILL.md
   grep -l 'CIS' skills/cis-benchmark-audit/SKILL.md
   grep -l 'NIST\|800-53\|CSF' skills/nist-compliance-assessment/SKILL.md

   # No regression
   bash scripts/validate.sh 2>&1 | grep -c 'ERROR:'  # must be 0
   ```

## Must-Haves

- [ ] README.md has 3 new catalog rows under "Security Skills" separator for acl-rule-analysis, cis-benchmark-audit, nist-compliance-assessment
- [ ] `bash scripts/validate.sh` reports 19 skills, 0 errors
- [ ] All 3 new skills have body ≤2700 words
- [ ] All 3 new skills have exactly 2 reference files
- [ ] No M001 skill regression (0 errors)

## Verification

- `bash scripts/validate.sh` exits 0 with "Skills checked: 19" and "Result: PASS (0 errors)"
- `grep -c 'rule-analysis\|benchmark-audit\|compliance-assessment' README.md` = 3
- All 3 word counts ≤2700
- `bash scripts/validate.sh 2>&1 | grep -c 'ERROR:'` = 0

## Inputs

- `README.md` — current catalog table with 16 skill rows (12 M001 + 4 S01 firewall) and "Security Skills" separator at line 41
- T01/T02/T03 completed skills in `skills/acl-rule-analysis/`, `skills/cis-benchmark-audit/`, `skills/nist-compliance-assessment/`
- K001 in KNOWLEDGE.md — use `awk` (not `sed`) for body word count on macOS

## Expected Output

- `README.md` — updated with 3 new catalog rows (total 19 skill rows including separator), all slice verification checks passing
