---
id: T03
parent: S03
milestone: M002
provides:
  - incident-response-network skill with 6-step evidence-driven lifecycle, 3-vendor forensic commands, lateral movement detection, and read-only containment verification
key_files:
  - skills/incident-response-network/SKILL.md
  - skills/incident-response-network/references/cli-reference.md
  - skills/incident-response-network/references/forensics-workflow.md
key_decisions:
  - Scoped containment verification as strictly read-only (check ACL counters, routing state, VLAN isolation) per D027 — no write operations
  - Offloaded chain-of-custody templates, evidence volatility ordering, and timeline reconstruction methodology to forensics-workflow.md to keep SKILL.md body at 2698 words
patterns_established:
  - Evidence-driven lifecycle procedure (preserve → triage → detect → verify → reconstruct → document) adapts D028 event-driven lifecycle to forensic phases
  - Forensic reference file pattern — forensics-workflow.md contains methodology reusable by future IR-adjacent skills
observability_surfaces:
  - bash scripts/validate.sh — 22 skills, 0 errors
  - awk body word count — 2698 (≤2700 threshold)
  - grep -c vendor labels — 21 [Cisco]/[JunOS]/[EOS] instances
  - grep -ci forensic terms — 61 matches for lateral movement/packet capture/netflow/evidence
duration: 20m
verification_result: passed
completed_at: 2026-03-17
blocker_discovered: false
---

# T03: Build incident-response-network skill for network forensics

**Created incident-response-network skill with 6-step forensic evidence lifecycle, 3-vendor packet capture and flow commands, lateral movement detection via flow/ARP/MAC analysis, and read-only containment verification across Cisco/JunOS/EOS**

## What Happened

Built the incident-response-network skill covering R026 (network forensics during incident response). The skill uses a 6-step evidence-driven procedure: (1) evidence preservation ordered by volatility (ARP/MAC → packet captures → routing state → flow data → configs), (2) initial triage to scope affected devices/IPs/time window, (3) lateral movement detection via flow records and ARP/MAC table changes, (4) read-only containment verification (ACL hit counters, null route presence, VLAN isolation checks), (5) timeline reconstruction merging syslog/flow/routing/ARP evidence, and (6) post-incident documentation with evidence inventory.

Created two reference files: cli-reference.md (149 lines) with forensic data collection commands organized by evidence type (packet capture, flow export, ARP/MAC/CAM, routing snapshots, ACL hit counts, SNMP/syslog verification) across 3 vendors, and forensics-workflow.md (213 lines) with evidence volatility ordering, artifact type descriptions, chain-of-custody documentation template, and 5-step timeline reconstruction methodology.

Initial body word count was 2707 (7 over limit). Trimmed the last Troubleshooting workaround paragraph to bring it to 2698 — proven trim target from prior tasks.

Also fixed two pre-flight observability gaps: added failure-path diagnostic check to S03-PLAN.md verification section and added `## Observability Impact` section to T03-PLAN.md.

## Verification

All must-haves verified:
- `bash scripts/validate.sh` — 22 skills, 0 errors, EXIT_CODE=0
- Body word count: 2698 (≤2700)
- `[Cisco]`/`[JunOS]`/`[EOS]` vendor labels: 21 instances (≥5)
- Forensic keywords (lateral movement/packet capture/netflow/evidence): 61 matches (≥5)
- `metadata.safety: read-only` confirmed in frontmatter
- All 7 H2 sections present (When to Use, Prerequisites, Procedure, Threshold Tables, Decision Trees, Report Template, Troubleshooting)
- `references/` directory contains exactly cli-reference.md and forensics-workflow.md
- No endpoint forensics, malware analysis, or general IR content — scope is network artifacts only
- Containment verification is read-only (check counters/state, not execute changes)
- All 21 prior skills pass validation (0 errors total, no regression)

Slice-level checks (partial — T04 pending for README catalog):
- ✅ Full validation: 22 skills, 0 errors
- ✅ All 3 S03 skill word counts ≤2700 (2446, 2682, 2698)
- ✅ Reference files: exactly 2 per skill
- ✅ SIEM vendor labels: 24 (≥10)
- ✅ CVE/CVSS/NVD terms: 79 (≥5)
- ✅ IR forensic terms: 61 (≥5)
- ⬜ README catalog completeness: 0 (T04 will add 3 rows)

## Verification Evidence

| # | Command | Exit Code | Verdict | Duration |
|---|---------|-----------|---------|----------|
| 1 | `bash scripts/validate.sh` | 0 | ✅ pass | 1s |
| 2 | `awk ... \| wc -w` (body word count) | 0 | ✅ pass (2698) | <1s |
| 3 | `grep -ci 'lateral movement\|packet capture\|netflow\|evidence'` | 0 | ✅ pass (61) | <1s |
| 4 | `grep -c '\[Cisco\]\|\[JunOS\]\|\[EOS\]'` | 0 | ✅ pass (21) | <1s |
| 5 | `ls skills/incident-response-network/references/` | 0 | ✅ pass (2 files) | <1s |
| 6 | `grep 'safety' skills/incident-response-network/SKILL.md` | 0 | ✅ pass (read-only) | <1s |
| 7 | `grep '^## ' skills/incident-response-network/SKILL.md` | 0 | ✅ pass (7 sections) | <1s |
| 8 | `bash scripts/validate.sh 2>&1 \| grep -c 'ERROR:'` | 0 | ✅ pass (0) | 1s |

## Diagnostics

- `bash scripts/validate.sh 2>&1 | grep -A1 'incident-response-network'` — shows per-check pass/fail for this skill
- `awk 'BEGIN{c=0} /^---$/{c++; if(c==2){found=1; next}} found{print}' skills/incident-response-network/SKILL.md | wc -w` — body word count (2698)
- `grep -c '\[Cisco\]\|\[JunOS\]\|\[EOS\]' skills/incident-response-network/SKILL.md` — vendor label density (21)
- `wc -l skills/incident-response-network/references/*.md` — reference file sizes (149 + 213 = 362 lines)
- `grep '^## ' skills/incident-response-network/SKILL.md` — structural completeness (7 H2 sections)

## Deviations

None. Body word count required minor trimming (2707 → 2698) using the proven Troubleshooting trim approach, as anticipated in Step 5 of the task plan.

## Known Issues

None.

## Files Created/Modified

- `skills/incident-response-network/SKILL.md` — Main skill file with 6-step forensic evidence lifecycle, threshold tables, decision trees, report template
- `skills/incident-response-network/references/cli-reference.md` — Forensic data collection commands across 6 evidence types for Cisco/JunOS/EOS
- `skills/incident-response-network/references/forensics-workflow.md` — Evidence methodology, chain-of-custody template, artifact types, timeline reconstruction
- `.gsd/milestones/M002/slices/S03/S03-PLAN.md` — Marked T03 as done; added failure-path diagnostic check to verification
- `.gsd/milestones/M002/slices/S03/tasks/T03-PLAN.md` — Added Observability Impact section
