---
id: T01
parent: S04
milestone: M001
provides:
  - interface-health skill with error counters, optical thresholds, and discard analysis
key_files:
  - skills/interface-health/SKILL.md
  - skills/interface-health/references/cli-reference.md
  - skills/interface-health/references/threshold-tables.md
key_decisions: []
patterns_established:
  - Optical power thresholds organized by SFP type (1G-SX, 10G-SR, 10G-LR, 25G-SR, 100G-SR4) with per-lane breakdown for multi-lane optics
  - Error thresholds use per-5-minute-interval rates rather than absolute counters or per-hour rates
observability_surfaces:
  - "agentskills validate skills/interface-health → exit 0"
  - "bash scripts/validate.sh → interface-health checked, 0 errors"
  - "awk word count on SKILL.md body → 2176 words (limit 2700)"
duration: 15m
verification_result: passed
completed_at: 2026-03-16
blocker_discovered: false
---

# T01: Create interface-health skill with error counters, optical thresholds, and discard analysis

**Created complete interface-health skill with 6-step procedure, 3-vendor coverage, optical power tables for 5 SFP types, and decision trees for errors/discards/optics.**

## What Happened

Created `skills/interface-health/` directory with SKILL.md and two reference files. The SKILL.md follows the established 7-section template with `[Cisco]`/`[JunOS]`/`[EOS]` vendor labeling throughout the procedure.

The procedure covers 6 diagnostic steps: interface status overview, error counter analysis (CRC, frame, input/output errors, runts, giants), discard analysis (input/output discards, queue drops), interface reset/flap detection, optical power monitoring (Tx/Rx power, laser bias, temperature), and utilization assessment.

`references/threshold-tables.md` provides detailed 4-severity-tier tables for error rates (per 5-minute intervals), discard rates, reset/flap rates, optical power for 5 common SFP types (1G-SX, 10G-SR, 10G-LR, 25G-SR, 100G-SR4), utilization percentages, and error-rate-as-percentage-of-traffic for high-throughput links.

`references/cli-reference.md` provides multi-vendor command tables organized by diagnostic category (status, errors, discards, resets, optical, utilization) with 4 columns (IOS-XE, NX-OS, JunOS, EOS) and interpretation notes for format differences.

Also fixed observability gaps in S04-PLAN.md (added `## Observability / Diagnostics` section) and T01-PLAN.md (added `## Observability Impact` section).

## Verification

- `agentskills validate skills/interface-health` → exit 0 ("Valid skill")
- `bash scripts/validate.sh` → 9 skills checked, 0 errors, PASS (interface-health included)
- Word count: 2176 words (well within 2700 limit)
- Frontmatter: 6 keys present, `metadata.safety: read-only`
- H2 sections: all 7 required sections present
- References: exactly 2 files (`cli-reference.md`, `threshold-tables.md`)
- Vendor labels: 20 `[Cisco]`/`[JunOS]`/`[EOS]` labels used in SKILL.md

**Slice-level checks (partial — T01 of 5):**
- ✅ `agentskills validate skills/interface-health` → exit 0
- ✅ `bash scripts/validate.sh` → 9 skills, 0 errors, PASS
- ✅ Word count ≤ 2700
- ✅ 6 frontmatter keys, correct safety value
- ✅ 7 required H2 sections
- ✅ references/ has exactly 2 files
- ⏳ README catalog update (T05)
- ⏳ `npx skills add . --list` (T05)

## Diagnostics

- Run `agentskills validate skills/interface-health` to verify structural validity
- Run `bash scripts/validate.sh` to verify as part of full suite
- Check body word count: `awk 'BEGIN{c=0}/^---$/{c++;if(c==2){f=1;next}}f{print}' skills/interface-health/SKILL.md | wc -w`
- List references: `ls skills/interface-health/references/`

## Deviations

- `cli-reference.md` uses 4 columns (IOS-XE, NX-OS, JunOS, EOS) instead of the plan's 3-column format (Cisco, JunOS, EOS). This provides better coverage since IOS-XE and NX-OS have non-trivial command differences (e.g., `show interfaces` vs `show interface` singular).

## Known Issues

None.

## Files Created/Modified

- `skills/interface-health/SKILL.md` — Complete interface health skill with 6-step procedure, 3 decision trees, threshold summary, report template
- `skills/interface-health/references/cli-reference.md` — Multi-vendor CLI reference with 6 diagnostic categories, 4 vendor columns
- `skills/interface-health/references/threshold-tables.md` — Detailed threshold tables for error rates, discards, resets, optical power (5 SFP types), utilization
- `.gsd/milestones/M001/slices/S04/S04-PLAN.md` — Added Observability / Diagnostics section
- `.gsd/milestones/M001/slices/S04/tasks/T01-PLAN.md` — Added Observability Impact section
