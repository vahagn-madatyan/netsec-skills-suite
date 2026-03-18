# S03: Security Operations Skills — UAT

**Milestone:** M002
**Written:** 2026-03-17

## UAT Type

- UAT mode: artifact-driven
- Why this mode is sufficient: All deliverables are static SKILL.md files and reference documents. No runtime, no API calls, no UI. Verification is structural (validate.sh), quantitative (word counts, term density), and content-quality (domain-specific terms present, correct vendor labels).

## Preconditions

- Repository cloned at `/Users/djbeatbug/RoadToMillion/network-security-skills-suite`
- Node.js available (for `npx skills add . --list` if testing discovery)
- `bash` available for `scripts/validate.sh`
- All 19 prior skills (M001 + S01 + S02) already passing validation

## Smoke Test

```bash
bash scripts/validate.sh 2>&1 | tail -3
# Expected: "Skills checked: 22" and "Result: PASS (0 errors)"
```

## Test Cases

### 1. Full suite validation — 22 skills, 0 errors

1. Run `bash scripts/validate.sh`
2. **Expected:** Output ends with `Skills checked: 22` and `Result: PASS (0 errors)`. Exit code 0.
3. Run `bash scripts/validate.sh 2>&1 | grep -c 'ERROR:'`
4. **Expected:** Returns `0`

### 2. Vulnerability-assessment skill structure

1. Run `grep 'safety' skills/vulnerability-assessment/SKILL.md`
2. **Expected:** Contains `read-only`
3. Run `grep '^## ' skills/vulnerability-assessment/SKILL.md`
4. **Expected:** 7 H2 sections: When to Use, Prerequisites, Procedure, Threshold Tables, Decision Trees, Report Template, Troubleshooting
5. Run `awk 'BEGIN{c=0} /^---$/{c++; if(c==2){found=1; next}} found{print}' skills/vulnerability-assessment/SKILL.md | wc -w`
6. **Expected:** ≤2700 (actual: 2446)
7. Run `ls skills/vulnerability-assessment/references/`
8. **Expected:** `cli-reference.md` and `vulnerability-reference.md` (exactly 2 files)

### 3. Vulnerability-assessment content specificity

1. Run `grep -c 'CVE\|CVSS\|NVD' skills/vulnerability-assessment/SKILL.md`
2. **Expected:** ≥5 (actual: 79)
3. Run `grep -c '\[Cisco\]\|\[JunOS\]\|\[EOS\]\|\[PAN-OS\]\|\[FortiGate\]' skills/vulnerability-assessment/SKILL.md`
4. **Expected:** ≥5 — confirms 5-vendor coverage
5. Open `skills/vulnerability-assessment/SKILL.md` and scan the Procedure section
6. **Expected:** 6-step procedure covering version inventory → CPE mapping → NVD query → CVSS scoring → risk classification → remediation plan
7. Open `skills/vulnerability-assessment/references/vulnerability-reference.md`
8. **Expected:** CVSS v3.1 metric breakdown (Base/Temporal/Environmental), severity-to-SLA mapping table, vendor advisory portal URLs for all 5 vendors

### 4. SIEM log analysis skill structure

1. Run `grep 'safety' skills/siem-log-analysis/SKILL.md`
2. **Expected:** Contains `read-only`
3. Run `grep '^## ' skills/siem-log-analysis/SKILL.md`
4. **Expected:** 7 H2 sections present
5. Run `awk 'BEGIN{c=0} /^---$/{c++; if(c==2){found=1; next}} found{print}' skills/siem-log-analysis/SKILL.md | wc -w`
6. **Expected:** ≤2700 (actual: 2682)
7. Run `ls skills/siem-log-analysis/references/`
8. **Expected:** `cli-reference.md` and `query-reference.md` (exactly 2 files)

### 5. SIEM vendor label density — key risk retirement

1. Run `grep -c '\[Splunk\]\|\[ELK\]\|\[QRadar\]' skills/siem-log-analysis/SKILL.md`
2. **Expected:** ≥10 (actual: 24) — confirms M002 SIEM vendor fragmentation risk retired
3. Open `skills/siem-log-analysis/SKILL.md` and verify that all three platforms appear within the Procedure section
4. **Expected:** [Splunk], [ELK], and [QRadar] each appear with platform-specific query syntax (SPL, KQL/Lucene, AQL)
5. Open `skills/siem-log-analysis/references/query-reference.md`
6. **Expected:** Side-by-side query patterns for ≥5 network-security use cases (auth failures, config changes, firewall denies, interface events, VPN tunnels, anomalous traffic, lateral movement)

### 6. SIEM content is network-security-specific, not generic

1. Open `skills/siem-log-analysis/SKILL.md` and read the Procedure section
2. **Expected:** All use cases relate to network security (firewall denies, auth failures, config changes, lateral movement) — NOT generic SIEM administration, log management, or data onboarding
3. Open `skills/siem-log-analysis/references/cli-reference.md`
4. **Expected:** Contains BOTH SIEM platform access commands (Splunk, ELK, QRadar) AND network device syslog verification commands for 5 vendors ([Cisco]/[JunOS]/[EOS]/[PAN-OS]/[FortiGate])

### 7. Incident response network skill structure

1. Run `grep 'safety' skills/incident-response-network/SKILL.md`
2. **Expected:** Contains `read-only`
3. Run `grep '^## ' skills/incident-response-network/SKILL.md`
4. **Expected:** 7 H2 sections present
5. Run `awk 'BEGIN{c=0} /^---$/{c++; if(c==2){found=1; next}} found{print}' skills/incident-response-network/SKILL.md | wc -w`
6. **Expected:** ≤2700 (actual: 2698)
7. Run `ls skills/incident-response-network/references/`
8. **Expected:** `cli-reference.md` and `forensics-workflow.md` (exactly 2 files)

### 8. Incident response content specificity and scope

1. Run `grep -ci 'lateral movement\|packet capture\|netflow\|evidence' skills/incident-response-network/SKILL.md`
2. **Expected:** ≥5 (actual: 61)
3. Open `skills/incident-response-network/SKILL.md` and read the Procedure section
4. **Expected:** 6-step evidence-driven lifecycle: evidence preservation → initial triage → lateral movement detection → containment verification → timeline reconstruction → post-incident documentation
5. Verify containment verification is read-only: search for "ACL" or "containment" in the Procedure
6. **Expected:** Containment verification checks ACL hit counters, null route presence, VLAN isolation — it does NOT execute ACL applications, routing changes, or port shutdowns
7. Search for "endpoint", "malware", or "EDR" in the skill body
8. **Expected:** These terms do NOT appear (or appear only in explicit scope-exclusion context). The skill is scoped to network forensics only.

### 9. Incident response evidence volatility ordering

1. Open `skills/incident-response-network/SKILL.md` and find the evidence preservation step
2. **Expected:** Evidence collected in volatility order: ARP/MAC tables first (most volatile), then packet captures, then routing state, then flow data, then configurations (least volatile)
3. Open `skills/incident-response-network/references/forensics-workflow.md`
4. **Expected:** Contains evidence volatility ordering, artifact type descriptions, chain-of-custody documentation template, and timeline reconstruction methodology

### 10. README catalog completeness

1. Run `grep -c 'vulnerability-assessment\|siem-log-analysis\|incident-response-network' README.md`
2. **Expected:** Returns `3`
3. Open `README.md` and locate the 3 new rows
4. **Expected:** Each row has a link to the skill directory, a one-line description, and `read-only` safety tier. Rows appear under the Security Skills section, after nist-compliance-assessment.

### 11. No M001/S01/S02 regression

1. Run `bash scripts/validate.sh 2>&1 | grep -E 'ERROR:|WARNING:' | wc -l`
2. **Expected:** Returns `0`
3. Run `bash scripts/validate.sh 2>&1 | grep -c 'OK:'`
4. **Expected:** Returns ≥180 (9 checks × ≥20 skills) — confirms all prior skills still pass all checks

## Edge Cases

### Word count boundary — siem-log-analysis at 2682/2700

1. Run `awk 'BEGIN{c=0} /^---$/{c++; if(c==2){found=1; next}} found{print}' skills/siem-log-analysis/SKILL.md | wc -w`
2. **Expected:** 2682 — exactly 18 words under the 2700 limit. Verify this hasn't drifted.

### Word count boundary — incident-response-network at 2698/2700

1. Run `awk 'BEGIN{c=0} /^---$/{c++; if(c==2){found=1; next}} found{print}' skills/incident-response-network/SKILL.md | wc -w`
2. **Expected:** 2698 — only 2 words under the 2700 limit. Any edit to this file must recount.

### Validate.sh exit code on clean suite

1. Run `bash scripts/validate.sh; echo "EXIT_CODE=$?"`
2. **Expected:** `EXIT_CODE=0`

## Failure Signals

- `validate.sh` reports any ERROR line → structural defect in a skill file
- Word count >2700 for any skill → body needs trimming
- SIEM vendor label count <10 → insufficient platform coverage, risk not retired
- CVE/CVSS/NVD grep <5 → vulnerability skill lacks domain specificity
- IR forensic term grep <5 → incident response skill is too generic
- README grep ≠ 3 → missing catalog rows
- Any "endpoint", "malware", "EDR" content in IR skill → scope violation (should be network-only)
- Containment steps that execute changes (apply ACL, shut interface) → safety tier violation (should be read-only)

## Requirements Proved By This UAT

- R024 — Test cases 2–3 prove CVE assessment with 5-vendor version mapping, CVSS scoring, and SLA-driven remediation
- R025 — Test cases 4–6 prove SIEM log analysis with [Splunk]/[ELK]/[QRadar] labels and network-security-specific use cases
- R026 — Test cases 7–9 prove network forensics IR with evidence lifecycle, lateral movement detection, and read-only containment

## Not Proven By This UAT

- Runtime agent execution — these are static skill files; actual agent behavior when consuming the skill depends on the agent platform
- SIEM query correctness — SPL/KQL/AQL syntax is representative but not validated against live SIEM instances
- NVD API integration — the skill describes how to query NVD; actual API responses depend on NVD availability
- Cross-skill interaction — whether an agent correctly chains vulnerability-assessment → siem-log-analysis → incident-response-network in a real investigation workflow

## Notes for Tester

- The word count check uses the K001 awk method (not sed) due to BSD sed incompatibility on macOS. Always use: `awk 'BEGIN{c=0} /^---$/{c++; if(c==2){found=1; next}} found{print}' SKILL.md | wc -w`
- incident-response-network is 2 words under the 2700 limit — be aware that even trivial edits could push it over
- The SIEM skill's cli-reference.md is intentionally dual-purpose (SIEM platform + network device syslog) — this is a design choice, not an error
- All three skills are read-only (D027) — if you see any suggestion to execute changes in the procedure, that's a defect
