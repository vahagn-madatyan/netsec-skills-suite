---
id: T02
parent: S04
milestone: M002
provides:
  - Zero-trust architecture maturity assessment skill with 5-pillar scoring rubric (R028)
  - Maturity scoring procedure shape (D028/D031) — reusable for any rubric-based posture assessment
key_files:
  - skills/zero-trust-assessment/SKILL.md
  - skills/zero-trust-assessment/references/maturity-model.md
  - skills/zero-trust-assessment/references/cli-reference.md
key_decisions:
  - "D031: Maturity scoring procedure shape — scope → pillar assessments → scoring → report, Threshold Tables hold pillar × level rubric"
patterns_established:
  - "Maturity scoring procedure shape generalizes to any rubric-based posture assessment (compliance maturity, cloud readiness, etc.)"
  - "Lowest-pillar scoring methodology ensures maturity cannot be inflated by strong pillars masking weak ones"
observability_surfaces:
  - "bash scripts/validate.sh 2>&1 | grep zero-trust — per-skill validation pass/fail"
  - "grep -c 'maturity|pillar|score|Level' skills/zero-trust-assessment/SKILL.md — content density ≥10"
  - "grep -ci '[Cisco]|[JunOS]|[PAN-OS]|[FortiGate]' skills/zero-trust-assessment/SKILL.md — must be 0 (vendor-agnostic guard)"
duration: 12m
verification_result: passed
completed_at: 2026-03-17
blocker_discovered: false
---

# T02: Build zero-trust assessment skill with maturity scoring rubric

**Created zero-trust assessment skill with 5-pillar × 5-level maturity scoring rubric, vendor-agnostic body, NIST SP 800-207 foundation, and multi-vendor CLI reference — 2667 words, 24 skills PASS.**

## What Happened

Built the zero-trust assessment skill introducing the "maturity scoring" procedure shape (D031). The skill assesses architecture-level ZT posture across five pillars (Identity, Device, Network, Application, Data) scored at five maturity levels (Traditional → Adaptive).

Key structural decisions:
- **Threshold Tables section** maps directly to pillar × level maturity scoring — each of the 5 pillars has a table with Level 1–5 criteria, following the same section-purpose pattern as CIS benchmark's severity tiers but applied to maturity rubrics.
- **Procedure follows maturity scoring shape:** Define Scope → Identity Assessment → Device Assessment → Network Assessment → Application & Data Assessment → Calculate Score and Report. This mirrors the BGP FSM / IKE FSM 6-step pattern adapted for posture assessment.
- **Vendor-agnostic body:** SKILL.md contains zero vendor labels. All platform-specific commands live in references/cli-reference.md with [Cisco]/[JunOS]/[PAN-OS]/[FortiGate] labels.
- **Lowest-pillar scoring methodology** recommended as primary (overall = MIN of all pillars), with weighted average as an alternative for tracking incremental progress.

Reference files:
- `maturity-model.md` — 5 pillar definitions, 5 maturity levels, scoring criteria matrix (5×5), calculation methodology (lowest-pillar + weighted average), assessment methodology phases.
- `cli-reference.md` — 7 ZT control categories (802.1X/NAC, AAA, MFA/cert, micro-segmentation, encryption, policy enforcement, monitoring) with 4-vendor command tables.

## Verification

- validate.sh: 24 skills, PASS (0 errors)
- Word count: 2667 ≤ 2700
- Content density: 89 matches for maturity/pillar/score/Level (≥10 required)
- NIST references: 4 matches (≥1 required)
- Vendor-agnostic guard: 0 vendor labels in SKILL.md body
- Reference file count: 2

## Verification Evidence

| # | Command | Exit Code | Verdict | Duration |
|---|---------|-----------|---------|----------|
| 1 | `bash scripts/validate.sh 2>&1 \| grep 'Skills checked'` | 0 | ✅ pass — "Skills checked: 24" | <1s |
| 2 | `bash scripts/validate.sh 2>&1 \| grep 'Result'` | 0 | ✅ pass — "Result: PASS (0 errors)" | <1s |
| 3 | `awk '...' skills/zero-trust-assessment/SKILL.md \| wc -w` | 0 | ✅ pass — 2667 ≤ 2700 | <1s |
| 4 | `ls skills/zero-trust-assessment/references/ \| wc -l` | 0 | ✅ pass — 2 files | <1s |
| 5 | `grep -c 'maturity\|pillar\|score\|Level' skills/zero-trust-assessment/SKILL.md` | 0 | ✅ pass — 89 ≥ 10 | <1s |
| 6 | `grep -c 'NIST\|800-207' skills/zero-trust-assessment/SKILL.md` | 0 | ✅ pass — 4 ≥ 1 | <1s |
| 7 | `grep -ci '\[Cisco\]\|\[JunOS\]...' skills/zero-trust-assessment/SKILL.md` | 1 | ✅ pass — 0 (vendor-agnostic) | <1s |

### Slice-Level Checks (partial — T03/T04 pending)

| # | Check | Result |
|---|-------|--------|
| 1 | VPN word count ≤2700 | ✅ 2506 |
| 2 | ZT word count ≤2700 | ✅ 2667 |
| 3 | VPN ref files = 2 | ✅ |
| 4 | ZT ref files = 2 | ✅ |
| 5 | VPN IKE density ≥10 | ✅ 74 |
| 6 | ZT maturity density ≥10 | ✅ 89 |
| 7 | Wireless checks | ⏳ pending T03 |
| 8 | README catalog rows = 3 | ⏳ pending T04 |
| 9 | validate.sh 25 skills | ⏳ pending T03 |

## Diagnostics

- **Validation:** `bash scripts/validate.sh 2>&1 | grep zero-trust` — shows pass/fail for this skill
- **Word count:** `awk 'BEGIN{c=0} /^---$/{c++; if(c==2){found=1; next}} found{print}' skills/zero-trust-assessment/SKILL.md | wc -w`
- **Content density:** `grep -c 'maturity\|pillar\|score\|Level' skills/zero-trust-assessment/SKILL.md` — should be ≥10
- **Vendor guard:** `grep -ci '\[Cisco\]\|\[JunOS\]\|\[PAN-OS\]\|\[FortiGate\]' skills/zero-trust-assessment/SKILL.md` — must be 0

## Deviations

None.

## Known Issues

None.

## Files Created/Modified

- `skills/zero-trust-assessment/SKILL.md` — ZT maturity assessment skill with 5-pillar scoring rubric, vendor-agnostic body, 2667 words
- `skills/zero-trust-assessment/references/maturity-model.md` — ZT maturity framework: 5 pillars × 5 levels with scoring criteria matrix and calculation methodology
- `skills/zero-trust-assessment/references/cli-reference.md` — Multi-vendor ZT control validation commands across 7 control categories
- `.gsd/milestones/M002/slices/S04/tasks/T02-PLAN.md` — Added Observability Impact section (pre-flight fix)
