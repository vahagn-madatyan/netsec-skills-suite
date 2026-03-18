# S02: Rule Analysis & Compliance Skills — UAT

**Milestone:** M002
**Written:** 2026-03-17

## UAT Type

- UAT mode: artifact-driven
- Why this mode is sufficient: All deliverables are static SKILL.md content files and README catalog entries — no runtime, no APIs, no UI. Verification is structural (validation script, word counts, grep checks) and content-depth (specific terms, control IDs, vendor labels).

## Preconditions

- Working directory is the `network-security-skills-suite` repository root
- `bash` available (macOS or Linux)
- `awk`, `grep`, `wc` available (standard Unix tools)
- All 19 skill directories exist under `skills/`
- `scripts/validate.sh` is executable

## Smoke Test

```bash
bash scripts/validate.sh 2>&1 | tail -2
# Expected: "Skills checked: 19" and "Result: PASS (0 errors)"
```

## Test Cases

### 1. Full Suite Validation — 19 Skills, 0 Errors

1. Run `bash scripts/validate.sh`
2. Check output for skill count and error count
3. **Expected:** "Skills checked: 19" and "Result: PASS (0 errors)" with exit code 0

### 2. ACL Rule Analysis — Word Budget and Content Depth

1. Run `awk 'BEGIN{c=0} /^---$/{c++; if(c==2){found=1; next}} found{print}' skills/acl-rule-analysis/SKILL.md | wc -w`
2. Run `ls skills/acl-rule-analysis/references/ | wc -l`
3. Run `grep -l 'shadowed' skills/acl-rule-analysis/SKILL.md`
4. Run `grep -c '\[Cisco\]\|\[JunOS\]\|\[EOS\]\|\[PAN-OS\]\|\[FortiGate\]\|\[CheckPoint\]' skills/acl-rule-analysis/SKILL.md`
5. **Expected:** Word count ≤2700, exactly 2 reference files, "shadowed" found, vendor label count ≥30

### 3. ACL Rule Analysis — Four Analysis Categories Present

1. Run `grep -c 'shadowed' skills/acl-rule-analysis/SKILL.md`
2. Run `grep -c 'permissive' skills/acl-rule-analysis/SKILL.md`
3. Run `grep -c 'unused' skills/acl-rule-analysis/SKILL.md`
4. Run `grep -c 'redundant' skills/acl-rule-analysis/SKILL.md`
5. **Expected:** All four return ≥1 — all four rule analysis categories are covered

### 4. CIS Benchmark Audit — Word Budget and Content Depth

1. Run `awk 'BEGIN{c=0} /^---$/{c++; if(c==2){found=1; next}} found{print}' skills/cis-benchmark-audit/SKILL.md | wc -w`
2. Run `ls skills/cis-benchmark-audit/references/ | wc -l`
3. Run `grep -l 'CIS' skills/cis-benchmark-audit/SKILL.md`
4. **Expected:** Word count ≤2700, exactly 2 reference files, "CIS" found

### 5. CIS Copyright Safety — No Reproduced Benchmark Text

1. Run `grep -c '\.[0-9]' skills/cis-benchmark-audit/references/control-reference.md`
2. Run `grep -c 'Remediation:' skills/cis-benchmark-audit/references/control-reference.md`
3. Run `grep -c 'Rationale:' skills/cis-benchmark-audit/references/control-reference.md`
4. **Expected:** Control ID count ≥40 (many CIS section IDs present). Remediation: returns 0. Rationale: returns 0. No copyrighted CIS benchmark text is reproduced.

### 6. CIS Platform Coverage — 4 Vendors

1. Run `grep -c 'Cisco IOS\|PAN-OS\|JunOS\|Check Point' skills/cis-benchmark-audit/SKILL.md`
2. **Expected:** ≥4 — all four CIS benchmark platforms are referenced

### 7. NIST Compliance Assessment — Word Budget and Content Depth

1. Run `awk 'BEGIN{c=0} /^---$/{c++; if(c==2){found=1; next}} found{print}' skills/nist-compliance-assessment/SKILL.md | wc -w`
2. Run `ls skills/nist-compliance-assessment/references/ | wc -l`
3. Run `grep -l 'NIST\|800-53\|CSF' skills/nist-compliance-assessment/SKILL.md`
4. **Expected:** Word count ≤2700, exactly 2 reference files, NIST/800-53/CSF found

### 8. NIST Control Family Coverage — 6 Families

1. Run `grep -c 'AC-\|AU-\|CM-\|IA-\|SC-\|SI-' skills/nist-compliance-assessment/SKILL.md`
2. Run `grep -c 'AC-\|AU-\|CM-\|IA-\|SC-\|SI-' skills/nist-compliance-assessment/references/control-reference.md`
3. **Expected:** Both return ≥6 — all 6 control families (Access Control, Audit, Configuration Management, Identification/Authentication, System/Communications Protection, System/Information Integrity) present in both SKILL.md and control-reference.md

### 9. NIST Out-of-Scope Families Documented

1. Run `grep -c 'AT, CA, CP, IR' skills/nist-compliance-assessment/SKILL.md`
2. **Expected:** ≥1 — the 14 out-of-scope families are explicitly listed

### 10. README Catalog — 3 New Rows

1. Run `grep -c 'rule-analysis\|benchmark-audit\|compliance-assessment' README.md`
2. Run `grep 'acl-rule-analysis' README.md`
3. Run `grep 'cis-benchmark-audit' README.md`
4. Run `grep 'nist-compliance-assessment' README.md`
5. **Expected:** Count returns 3. Each grep returns a table row with skill name, description, and `read-only` safety tier.

### 11. Safety Tier — All 3 Skills Read-Only

1. Run `grep -A5 'name: acl-rule-analysis' skills/acl-rule-analysis/SKILL.md | grep 'safety'`
2. Run `grep -A5 'name: cis-benchmark-audit' skills/cis-benchmark-audit/SKILL.md | grep 'safety'`
3. Run `grep -A5 'name: nist-compliance-assessment' skills/nist-compliance-assessment/SKILL.md | grep 'safety'`
4. **Expected:** All three return `safety: read-only`

### 12. M001 Regression — No Existing Skills Broken

1. Run `bash scripts/validate.sh 2>&1 | grep 'ERROR:'`
2. **Expected:** No output (0 ERROR lines). All 12 M001 skills and 4 S01 skills continue to pass.

## Edge Cases

### Failure-Path Detection — Validate.sh Catches Broken Skills

1. Run:
   ```bash
   mkdir -p /tmp/nss-diag-test/skills/broken-test-skill/references
   echo -e "---\nname: broken-test-skill\ncategory: test\ndifficulty: beginner\nestimated_time: 5 minutes\nmetadata:\n  safety: read-only\n---\n# Only one section\nNo real content." > /tmp/nss-diag-test/skills/broken-test-skill/SKILL.md
   bash scripts/validate.sh /tmp/nss-diag-test/skills/broken-test-skill 2>&1 | grep -c 'ERROR:'
   rm -rf /tmp/nss-diag-test
   ```
2. **Expected:** Error count ≥6 (missing 6 of 7 required H2 sections). Confirms validate.sh correctly detects broken skills.

### Word Budget Boundary — NIST Skill Near Limit

1. Run `awk 'BEGIN{c=0} /^---$/{c++; if(c==2){found=1; next}} found{print}' skills/nist-compliance-assessment/SKILL.md | wc -w`
2. **Expected:** Result is ≤2700 but ≥2600 (currently 2664). This skill is near the word budget boundary — confirms the budget is being used effectively, not wastefully padded.

### Structured Output Parseable

1. Run `bash scripts/validate.sh 2>&1 | grep -E '(OK|ERROR):' | head -5`
2. **Expected:** Lines matching `OK:` or `ERROR:` pattern — confirms output is machine-parseable for agent consumption.

## Failure Signals

- `bash scripts/validate.sh` reports any `ERROR:` lines or exits non-zero
- Any skill body exceeds 2700 words
- Any skill has ≠ 2 reference files
- `grep -c 'Remediation:\|Rationale:' skills/cis-benchmark-audit/references/control-reference.md` returns >0 (copyright violation)
- README.md does not contain all 3 new skill rows
- Any M001 or S01 skill that previously passed now fails (regression)

## Requirements Proved By This UAT

- R021 — ACL rule analysis skill with shadowed/permissive/unused/redundant rule detection across 6 vendors (Tests 2, 3)
- R022 — CIS benchmark audit with copyright-safe control reference, 4-platform coverage (Tests 4, 5, 6)
- R023 — NIST 800-53 compliance assessment with 6 control families and CSF mapping (Tests 7, 8, 9)

## Not Proven By This UAT

- Runtime execution of skills by an actual AI agent (these are static content files)
- Quality of agent-generated compliance reports when using these skills (requires live agent + device access)
- Completeness of CIS control coverage beyond the ~40 high-impact controls selected
- NIST assessment accuracy for the 14 control families explicitly excluded from scope

## Notes for Tester

- The `nist-compliance-assessment` skill is at 2664 words — only 36 words under the 2700-word limit. If you spot-check this file, note that it's intentionally dense.
- The CIS copyright safety check (Test 5) is the D026 risk retirement gate. The `grep` for `Remediation:` and `Rationale:` must return 0 — these are hallmarks of reproduced CIS benchmark text.
- All three skills use `metadata.safety: read-only` — they analyze existing configurations without modifying device state.
- The ACL rule analysis skill uses 6 vendor labels (including FortiGate and CheckPoint), which is more than the 4-vendor pattern used in compliance skills. This is intentional — ACL analysis applies to both traditional ACL platforms and NGFW rulebases.
