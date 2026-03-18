---
id: T01
parent: S03
milestone: M002
provides:
  - vulnerability-assessment skill with CVE mapping, CVSS v3.1 scoring, and 5-vendor version retrieval
key_files:
  - skills/vulnerability-assessment/SKILL.md
  - skills/vulnerability-assessment/references/cli-reference.md
  - skills/vulnerability-assessment/references/vulnerability-reference.md
key_decisions:
  - Used threshold-comparison procedure shape per D028 (CVSS scores as thresholds mapping to severity tiers and remediation SLAs)
patterns_established:
  - CVE assessment skill follows 6-step procedure: version inventory → CPE mapping → NVD/vendor query → CVSS scoring → combined risk classification → remediation plan
observability_surfaces:
  - bash scripts/validate.sh — reports 20 skills, 0 errors (was 19)
  - grep -c 'CVE|CVSS|NVD' skills/vulnerability-assessment/SKILL.md — returns 79
  - awk word count method (K001) — body is 2446 words (≤2700 limit)
duration: 15m
verification_result: passed
completed_at: 2026-03-17
blocker_discovered: false
---

# T01: Build vulnerability-assessment skill with CVE mapping and CVSS scoring

**Created vulnerability-assessment skill with 5-vendor CVE-to-version mapping, CVSS v3.1 scoring, and SLA-driven remediation prioritization**

## What Happened

Built the vulnerability-assessment skill covering R024 (CVE assessment for network devices). The skill follows the proven threshold-comparison pattern from M001 device health skills, where CVSS scores map to severity tiers and remediation SLAs.

Created three files:
1. `references/cli-reference.md` — Version, patch, hardware model, and uptime retrieval commands for all 5 vendors (`[Cisco]`/`[JunOS]`/`[EOS]`/`[PAN-OS]`/`[FortiGate]`), including CPE construction examples and version parsing notes.
2. `references/vulnerability-reference.md` — Complete CVSS v3.1 metric breakdown (Base/Temporal/Environmental groups), NVD API query methods (by CPE, keyword, CVE ID), severity-to-SLA mapping table, CISA KEV catalog integration, and all 5 vendor advisory portal URLs.
3. `SKILL.md` — Full skill with frontmatter (`metadata.safety: read-only`), all 7 required H2 sections, and a 6-step procedure: inventory versions → map to CPE → query NVD/vendor advisories → score with CVSS v3.1 → classify by combined risk (severity × exposure × exploitability) → generate prioritized remediation plan.

Also applied pre-flight observability fixes: added `## Observability / Diagnostics` section and failure-path verification step to S03-PLAN.md, and added `## Observability Impact` section to T01-PLAN.md.

## Verification

All must-haves confirmed:
- `metadata.safety: read-only` present in YAML frontmatter ✅
- All 7 required H2 sections present ✅
- Body word count: 2446 (≤2700 limit) ✅
- `references/cli-reference.md` exists with 5-vendor commands ✅
- `references/vulnerability-reference.md` exists with CVSS scoring and vendor advisory sources ✅
- `grep -c 'CVE|CVSS|NVD'` returns 79 (≥5 requirement) ✅
- `bash scripts/validate.sh` reports 20 skills, 0 errors ✅
- All 19 prior skills still pass (0 regression errors) ✅

## Verification Evidence

| # | Command | Exit Code | Verdict | Duration |
|---|---------|-----------|---------|----------|
| 1 | `bash scripts/validate.sh` | 0 | ✅ pass — 20 skills, 0 errors | 3.6s |
| 2 | `awk ... \| wc -w` (body word count) | 0 | ✅ pass — 2446 words (≤2700) | <1s |
| 3 | `ls skills/vulnerability-assessment/references/` | 0 | ✅ pass — 2 files | <1s |
| 4 | `grep -c 'CVE\|CVSS\|NVD' SKILL.md` | 0 | ✅ pass — 79 matches (≥5) | <1s |
| 5 | `bash scripts/validate.sh 2>&1 \| grep -c 'ERROR:'` | 0 | ✅ pass — 0 errors | 3.6s |
| 6 | `grep -c 'vulnerability-assessment\|...' README.md` | 0 | ⏳ expected 0 — T04 adds catalog | <1s |

## Diagnostics

- `bash scripts/validate.sh 2>&1 | grep vulnerability-assessment` — shows per-skill validation result
- `awk 'BEGIN{c=0} /^---$/{c++; if(c==2){found=1; next}} found{print}' skills/vulnerability-assessment/SKILL.md | wc -w` — body word count
- `grep 'safety' skills/vulnerability-assessment/SKILL.md` — confirms read-only safety tier
- `ls skills/vulnerability-assessment/references/` — confirms 2 reference files

## Deviations

None. All steps executed as planned.

## Known Issues

None.

## Files Created/Modified

- `skills/vulnerability-assessment/SKILL.md` — Complete CVE assessment skill (2446 body words) with 5-vendor version mapping, CVSS scoring, remediation prioritization
- `skills/vulnerability-assessment/references/cli-reference.md` — Version/patch retrieval CLI commands for Cisco, JunOS, EOS, PAN-OS, FortiGate with CPE construction examples
- `skills/vulnerability-assessment/references/vulnerability-reference.md` — CVSS v3.1 breakdown, NVD API query methods, severity-to-SLA mapping, vendor advisory sources, CISA KEV integration
- `.gsd/milestones/M002/slices/S03/S03-PLAN.md` — Added Observability / Diagnostics section and failure-path verification step
- `.gsd/milestones/M002/slices/S03/tasks/T01-PLAN.md` — Added Observability Impact section
