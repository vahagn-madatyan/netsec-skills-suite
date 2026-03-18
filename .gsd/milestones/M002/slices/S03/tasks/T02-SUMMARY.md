---
id: T02
parent: S03
milestone: M002
provides:
  - siem-log-analysis skill with [Splunk]/[ELK]/[QRadar] labeled query patterns and platform-independent diagnostic reasoning
  - Network-security-specific SIEM analysis covering 7 use cases (auth failures, config changes, firewall denies, interface events, VPN tunnels, anomalous traffic, lateral movement)
key_files:
  - skills/siem-log-analysis/SKILL.md
  - skills/siem-log-analysis/references/cli-reference.md
  - skills/siem-log-analysis/references/query-reference.md
key_decisions:
  - Used [Splunk]/[ELK]/[QRadar] inline labels mirroring the [Cisco]/[JunOS]/[EOS] pattern from device skills — diagnostic reasoning stays platform-independent, only query syntax diverges
  - Offloaded full side-by-side query patterns to references/query-reference.md to keep SKILL.md body under 2700 words while maintaining ≥10 SIEM vendor labels in the main file
patterns_established:
  - SIEM skill uses forensic timeline procedure shape (D028) with 6 steps — verify sources, normalize, correlate, build timeline, detect anomalies, triage
  - cli-reference.md covers both SIEM platform access commands and network device syslog verification (5-vendor coverage) since syslog forwarding is a prerequisite for SIEM analysis
observability_surfaces:
  - bash scripts/validate.sh — reports 21 skills, 0 errors (siem-log-analysis appears in per-skill OK lines)
  - grep -c '[Splunk]|[ELK]|[QRadar]' skills/siem-log-analysis/SKILL.md — returns 24 (≥10 required)
  - awk K001 word count — returns 2682 (≤2700 limit)
duration: 18m
verification_result: passed
completed_at: 2026-03-17
blocker_discovered: false
---

# T02: Build siem-log-analysis skill with multi-platform query patterns

**Created siem-log-analysis skill with 24 SIEM vendor labels, 7 network-security use cases, and side-by-side SPL/KQL/AQL query patterns — retires M002 SIEM vendor fragmentation risk**

## What Happened

Built three files for the siem-log-analysis skill following the plan's specification exactly:

1. `references/cli-reference.md` — SIEM platform access commands for Splunk (SPL search commands), ELK (Kibana/Dev Tools), and QRadar (AQL/Log Activity). Network device syslog verification commands for 5 vendors ([Cisco], [JunOS], [EOS], [PAN-OS], [FortiGate]) with table format. Includes RFC 5424 severity/facility mapping and vendor default facility codes.

2. `references/query-reference.md` — Side-by-side SPL/KQL/AQL query patterns for 7 network security use cases: authentication failures, configuration changes, firewall/ACL denies, interface state changes, VPN tunnel events, anomalous traffic patterns, and lateral movement indicators. Each use case has 3 platform-specific queries plus a brief explanation.

3. `SKILL.md` — Full skill file with all 7 required H2 sections. Procedure follows the forensic timeline shape (D028): verify syslog sources → normalize events → correlate across sources → build timeline → identify anomalies → triage and classify. Threshold Tables include alert severity classification, event volume anomaly thresholds (σ-based), and correlation confidence scoring. Decision tree covers the complete alert triage flow with true positive/false positive/informational branches.

Word count came in at 2721 initially — trimmed Troubleshooting section by tightening two subsections (Missing Log Sources, Log Parsing Failures) to reach 2682.

## Verification

All must-haves confirmed:
- `metadata.safety: read-only` in YAML frontmatter ✓
- All 7 required H2 sections present ✓
- Body word count 2682 (≤2700) ✓
- 24 SIEM vendor label instances (≥10) ✓
- All queries are network-security-specific (firewall denies, auth failures, lateral movement — not generic SIEM admin) ✓
- `references/cli-reference.md` exists with SIEM access + 5-vendor syslog commands ✓
- `references/query-reference.md` exists with side-by-side SPL/KQL/AQL ✓
- `bash scripts/validate.sh` reports 21 skills, 0 errors ✓

## Verification Evidence

| # | Command | Exit Code | Verdict | Duration |
|---|---------|-----------|---------|----------|
| 1 | `bash scripts/validate.sh` | 0 | ✅ pass — 21 skills, 0 errors | 1s |
| 2 | `awk K001 word count` | 0 | ✅ pass — 2682 words (≤2700) | <1s |
| 3 | `grep -c '[Splunk]\|[ELK]\|[QRadar]' SKILL.md` | 0 | ✅ pass — 24 labels (≥10) | <1s |
| 4 | `ls references/` | 0 | ✅ pass — cli-reference.md, query-reference.md | <1s |
| 5 | `grep 'safety' SKILL.md` | 0 | ✅ pass — read-only | <1s |
| 6 | `grep '^## ' SKILL.md` | 0 | ✅ pass — 7 H2 sections | <1s |
| 7 | Slice check: vulnerability-assessment word count | 0 | ✅ pass — 2446 | <1s |
| 8 | Slice check: README catalog | 1 | ⏳ expected — T04 adds README entries | <1s |
| 9 | Slice check: validate.sh error count | 0 | ✅ pass — 0 errors | 1s |

## Diagnostics

- `bash scripts/validate.sh 2>&1 | grep siem-log-analysis` — per-skill validation output
- `grep -c '\[Splunk\]\|\[ELK\]\|\[QRadar\]' skills/siem-log-analysis/SKILL.md` — SIEM label density (24)
- `awk 'BEGIN{c=0} /^---$/{c++; if(c==2){found=1; next}} found{print}' skills/siem-log-analysis/SKILL.md | wc -w` — body word count (2682)
- `wc -l skills/siem-log-analysis/references/*.md` — reference file sizes (non-trivial content)
- `grep '^## ' skills/siem-log-analysis/SKILL.md` — structural completeness (7 H2 sections)

## Deviations

None. Initial word count was 2721 (21 words over limit) — trimmed two Troubleshooting subsections to reach 2682. This was anticipated by Step 5 of the plan.

## Known Issues

None.

## Files Created/Modified

- `skills/siem-log-analysis/SKILL.md` — Main skill file (2682 body words, 24 SIEM vendor labels, 7 H2 sections)
- `skills/siem-log-analysis/references/cli-reference.md` — SIEM platform access + 5-vendor syslog verification commands
- `skills/siem-log-analysis/references/query-reference.md` — Side-by-side SPL/KQL/AQL patterns for 7 network security use cases
- `.gsd/milestones/M002/slices/S03/S03-PLAN.md` — Added diagnostic failure-path verification step (pre-flight fix)
- `.gsd/milestones/M002/slices/S03/tasks/T02-PLAN.md` — Added Observability Impact section (pre-flight fix)
