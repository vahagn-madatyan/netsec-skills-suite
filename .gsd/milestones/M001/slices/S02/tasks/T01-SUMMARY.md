---
id: T01
parent: S02
milestone: M001
provides:
  - Production Cisco IOS-XE/NX-OS dual-platform device health check skill
  - CLI reference with side-by-side IOS-XE and NX-OS commands by subsystem
  - Platform-specific threshold tables with 4 severity tiers
key_files:
  - skills/cisco-device-health/SKILL.md
  - skills/cisco-device-health/references/cli-reference.md
  - skills/cisco-device-health/references/threshold-tables.md
key_decisions:
  - Shared procedure steps with platform-labeled code blocks — not separate IOS-XE and NX-OS procedure sections. Keeps the skill scannable while preserving platform-specific depth.
  - NX-OS CPU/memory thresholds offset 5–10% higher than IOS-XE to reflect Linux kernel baseline overhead. Thresholds are in separate tables in references/ rather than merged.
  - vPC health added as NX-OS-specific routing check and threshold table — vPC peer-link state is critical DC health signal absent from IOS-XE.
  - QFP drops/sec added as IOS-XE-only threshold — data plane health indicator with no NX-OS equivalent.
patterns_established:
  - Dual-platform skill structure: shared H3 procedure steps with **[IOS-XE]** and **[NX-OS]** labeled code blocks where commands diverge. Reusable for any future multi-platform skills.
  - Platform-specific threshold tables in references/ with separate sections per platform where baselines differ.
  - CLI reference uses side-by-side columns (IOS-XE Command | NX-OS Command) per subsystem.
observability_surfaces:
  - none
duration: 1 task step
verification_result: passed
completed_at: 2026-03-15
blocker_discovered: false
---

# T01: Write Cisco IOS-XE/NX-OS device health check skill

**Created production dual-platform Cisco health check skill with IOS-XE QFP/RP and NX-OS VDC-aware triage procedures, 1708-word body (well under 2700 budget).**

## What Happened

Built the Cisco device health check skill covering both IOS-XE and NX-OS platforms in a single SKILL.md. The procedure uses shared H3 steps (Baseline, CPU, Memory, Interfaces, Routing, Environment) with platform-labeled code blocks where commands diverge.

Key platform-specific depth:
- IOS-XE: RP vs QFP split triage in decision trees — high QFP drops with normal RP means data plane overload, not a restart situation. QFP drops/sec has its own threshold table.
- NX-OS: VDC context check is step 1, `show system resources` replaces `show processes cpu sorted`, vPC peer-link state added as critical routing health signal, module health check via `show module`.
- Thresholds: NX-OS CPU normal baseline is 0–50% vs IOS-XE 0–40%. NX-OS memory normal is >30% free vs IOS-XE <70% used. Separate tables in references/.

CLI reference uses side-by-side IOS-XE/NX-OS columns per subsystem with interpretation notes that explain _why_ commands differ (architecture, not just syntax).

Body word count: 1708 words — 63% of the 2700 budget. This confirms the token budget pattern works for dual-platform skills; single-platform skills (Juniper T02, Arista T03) will fit easily.

## Verification

- `agentskills validate skills/cisco-device-health` → "Valid skill" (exit 0) ✓
- `bash scripts/validate.sh` → cisco-device-health all OK, 0 errors ✓
- Body word count: 1708 (≤ 2700 target) ✓
- IOS-XE appears 12 times in Procedure section ✓
- NX-OS appears 14 times in Procedure section ✓
- All 6 frontmatter keys present with `name: cisco-device-health` and `metadata.safety: read-only` ✓
- All 7 H2 sections present ✓
- references/ directory contains cli-reference.md and threshold-tables.md ✓

### Slice-level verification status (T01 of 3 tasks):
- `agentskills validate skills/cisco-device-health` → PASS ✓
- `agentskills validate skills/juniper-device-health` → not yet created (T02)
- `agentskills validate skills/arista-device-health` → not yet created (T03)
- `bash scripts/validate.sh` → PASS (2 skills: example + cisco) ✓
- Cisco body ≤ 2700 words → PASS ✓
- README catalog update → pending (likely T03 or later)

## Diagnostics

None — read-only skill files with no runtime behavior. Validate with `agentskills validate skills/cisco-device-health` and `bash scripts/validate.sh`.

## Deviations

None.

## Known Issues

None.

## Files Created/Modified

- `skills/cisco-device-health/SKILL.md` — Production dual-platform Cisco health check skill (1708 words body)
- `skills/cisco-device-health/references/cli-reference.md` — IOS-XE and NX-OS commands by subsystem with side-by-side columns
- `skills/cisco-device-health/references/threshold-tables.md` — Platform-specific thresholds with 4 severity tiers, separate NX-OS sections where baselines differ
