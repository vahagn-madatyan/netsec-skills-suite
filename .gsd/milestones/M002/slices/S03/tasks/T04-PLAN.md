---
estimated_steps: 4
estimated_files: 1
---

# T04: Update README catalog and run full-suite validation

**Slice:** S03 — Security Operations Skills
**Milestone:** M002

## Description

Complete S03 by adding the 3 new security operations skills to the README catalog table and running the full verification battery. The 3 new rows go after line 48 (nist-compliance-assessment — the current last security skill row) under the existing "Security Skills" separator. After this task, the README will show 22 skill rows and all slice-level verification checks will pass.

## Steps

1. **Add 3 new rows to README.md catalog table** — Insert after the nist-compliance-assessment row (line 48). The 3 new rows:
   ```
   | [vulnerability-assessment](skills/vulnerability-assessment/SKILL.md) | CVE assessment for network devices — version-to-CVE mapping, CVSS scoring, remediation prioritization across Cisco, JunOS, EOS, PAN-OS, FortiGate | `read-only` |
   | [siem-log-analysis](skills/siem-log-analysis/SKILL.md) | Network security SIEM analysis — syslog parsing, event correlation, alert triage with Splunk SPL, ELK KQL, and QRadar AQL query patterns | `read-only` |
   | [incident-response-network](skills/incident-response-network/SKILL.md) | Network forensics during incident response — packet capture, flow analysis, lateral movement detection, evidence preservation (Cisco/JunOS/EOS) | `read-only` |
   ```

2. **Run the full validation battery** — Execute all verification commands from the S03 slice plan:
   - `bash scripts/validate.sh` → expect "Skills checked: 22", "Result: PASS (0 errors)"
   - Word counts for all 3 new skills (each ≤2700 via K001 `awk` method)
   - Reference file counts (exactly 2 per skill)
   - SIEM vendor labels: `grep -c '\[Splunk\]\|\[ELK\]\|\[QRadar\]' skills/siem-log-analysis/SKILL.md` → ≥10
   - Content specificity checks for vulnerability-assessment and incident-response-network
   - README catalog: `grep -c 'vulnerability-assessment\|siem-log-analysis\|incident-response-network' README.md` → 3
   - No regression: `bash scripts/validate.sh 2>&1 | grep -c 'ERROR:'` → 0

3. **Verify M001 skills are unaffected** — Confirm the 12 M001 skills pass validation unchanged by checking the validate.sh output shows 0 errors across all skills.

4. **Fix any issues found** — If README formatting is broken (table alignment), fix the markdown. If any validation errors appear, investigate and resolve.

## Must-Haves

- [ ] README.md has 3 new catalog rows for vulnerability-assessment, siem-log-analysis, incident-response-network
- [ ] New rows are under the "Security Skills" separator, after nist-compliance-assessment
- [ ] All rows have correct links, descriptions, and `read-only` safety tier
- [ ] `bash scripts/validate.sh` reports 22 skills, 0 errors
- [ ] All 3 new skills have body ≤2700 words
- [ ] All 3 new skills have exactly 2 reference files each
- [ ] SIEM skill has ≥10 vendor labels
- [ ] No M001/S01/S02 regression (0 errors across all prior skills)

## Verification

- `bash scripts/validate.sh` exits 0, reports "Skills checked: 22" and "Result: PASS (0 errors)"
- `grep -c 'vulnerability-assessment\|siem-log-analysis\|incident-response-network' README.md` returns 3
- All word counts ≤2700 (K001 `awk` method)
- `grep -c '\[Splunk\]\|\[ELK\]\|\[QRadar\]' skills/siem-log-analysis/SKILL.md` returns ≥10
- `grep -c 'CVE\|CVSS\|NVD' skills/vulnerability-assessment/SKILL.md` returns ≥5
- `grep -ci 'lateral movement\|packet capture\|netflow\|evidence' skills/incident-response-network/SKILL.md` returns ≥5
- `bash scripts/validate.sh 2>&1 | grep -c 'ERROR:'` returns 0

## Inputs

- T01, T02, T03 completed: all 3 skills are created and individually validated (22 skills total)
- Current README.md with nist-compliance-assessment as the last security skill row (line 48)
- S03 slice plan Verification section — the definitive list of checks to run

## Expected Output

- `README.md` — Updated with 3 new catalog rows under "Security Skills" section
- Full verification battery passing with all expected values
- S03 slice complete and ready for summary
