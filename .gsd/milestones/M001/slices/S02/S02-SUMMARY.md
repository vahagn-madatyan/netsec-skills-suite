---
id: S02
parent: M001
milestone: M001
provides:
  - 3 production device health check skills (Cisco IOS-XE/NX-OS, Juniper JunOS, Arista EOS) with vendor-specific procedural depth
  - Proven token budget pattern — dual-platform Cisco at 1708 words, single-platform at 2326–2643, all under 2700 word / ~5000 token limit
  - Vendor-specific threshold tables with 4 severity tiers and platform-aware baselines
  - Decision tree format encoding platform-specific triage logic (RP vs QFP, RE vs PFE, agent-level health)
  - Updated README catalog with 3 new skill rows
requires:
  - slice: S01
    provides: SKILL.md template structure, safety tier convention, references/ subdirectory convention, CI validation pipeline
affects:
  - S04
key_files:
  - skills/cisco-device-health/SKILL.md
  - skills/cisco-device-health/references/cli-reference.md
  - skills/cisco-device-health/references/threshold-tables.md
  - skills/juniper-device-health/SKILL.md
  - skills/juniper-device-health/references/cli-reference.md
  - skills/juniper-device-health/references/threshold-tables.md
  - skills/arista-device-health/SKILL.md
  - skills/arista-device-health/references/cli-reference.md
  - skills/arista-device-health/references/threshold-tables.md
  - README.md
key_decisions:
  - "D015: Dual-platform skills use shared H3 procedure steps with **[IOS-XE]** / **[NX-OS]** labeled code blocks — keeps skill scannable without duplicating procedure sections"
  - "D016: JunOS alarm-first triage — RE mastership (Step 1) then alarm analysis (Step 2) before resource checks, because JunOS alarms often identify the problem directly"
  - "D017: DC-extension steps (MLAG, VXLAN/EVPN) as opt-in procedure sections with explicit skip guidance — keeps Arista skill usable for non-DC deployments"
  - "D018: Agent/daemon health as dedicated EOS procedure step — per-agent architecture means subsystem failures invisible in aggregate metrics"
patterns_established:
  - "Dual-platform skill structure: shared H3 procedure steps with platform-labeled code blocks. Reusable for any future multi-platform skills."
  - "Single-platform skill structure follows identical 7 H2 sections with vendor-specific depth in Procedure and Decision Trees. No structural divergence from dual-platform pattern."
  - "DC-specific extension steps as opt-in procedure sections with explicit skip guidance. Reusable for any skill with feature-specific extensions."
  - "Alarm-first triage for platforms where alarms are first-class (JunOS). Applicable to future vendor skills with prominent alarm systems."
  - "Platform-specific threshold tables in references/ with separate sections per platform where baselines differ."
  - "CLI reference uses side-by-side columns per subsystem with interpretation notes explaining architectural differences."
observability_surfaces:
  - none
drill_down_paths:
  - .gsd/milestones/M001/slices/S02/tasks/T01-SUMMARY.md
  - .gsd/milestones/M001/slices/S02/tasks/T02-SUMMARY.md
duration: 2 tasks
verification_result: passed
completed_at: 2026-03-15
---

# S02: Multi-Vendor Device Health Checks

**Delivered 3 production device health check skills (Cisco, Juniper, Arista) with genuine vendor-specific triage logic, proving the token budget pattern at 63–98% of the 2700-word limit.**

## What Happened

Built three device health check skills that encode genuinely different vendor health models — not command substitution across platforms.

**Cisco IOS-XE/NX-OS (T01):** Dual-platform skill using shared H3 procedure steps with platform-labeled code blocks where commands diverge. Key platform-specific depth: IOS-XE RP vs QFP split triage in decision trees (high QFP drops with normal RP = data plane overload, not restart), NX-OS VDC context as mandatory first check, vPC peer-link as critical routing health signal, `show system resources` replacing `show processes cpu sorted`. NX-OS thresholds offset 5–10% higher to reflect Linux kernel baseline overhead. Body: 1708 words (63% of budget). This was the token budget proof point — dual-platform skills fit comfortably.

**Juniper JunOS (T02):** RE/PFE architecture encoded as separate procedure steps and decision tree branches. Mastership verification is mandatory Step 1 (data from wrong RE is invalid on dual-RE systems). Alarm analysis is Step 2 as a triage gate before resource checks — Major alarms take priority over everything. Threshold tables account for RE CPU commit spikes being normal behavior. Body: 2326 words.

**Arista EOS (T02):** Core health (Steps 1–5) plus DC extensions (Steps 6–7 for MLAG/VXLAN). Agent/daemon health is a dedicated Step 3 because EOS runs subsystems as independent processes — a crashed Bgp agent means BGP is down even when system CPU shows 10%. MLAG state validation and VXLAN/EVPN health are explicitly skippable DC extensions. Linux-native commands documented as valid supplements. Body: 2643 words (98% of budget — single-platform with DC extensions pushes close to the limit).

## Verification

All slice-level verification checks passed:

- `agentskills validate skills/cisco-device-health` → "Valid skill" (exit 0) ✓
- `agentskills validate skills/juniper-device-health` → "Valid skill" (exit 0) ✓
- `agentskills validate skills/arista-device-health` → "Valid skill" (exit 0) ✓
- `bash scripts/validate.sh` → 4 skills checked, 0 errors ✓
- Cisco body: 1708 words ≤ 2700 ✓
- Juniper body: 2326 words ≤ 2700 ✓
- Arista body: 2643 words ≤ 2700 ✓
- README.md catalog: 3 new rows (cisco-device-health, juniper-device-health, arista-device-health) ✓
- All SKILL.md files: 6 frontmatter keys, 7 H2 sections, `metadata.safety: read-only` ✓
- All skills: references/ directory with cli-reference.md and threshold-tables.md ✓

## Requirements Advanced

- R006 (Cisco IOS-XE/NX-OS health check) — Delivered with dual-platform depth: IOS-XE QFP/RP triage, NX-OS VDC/vPC awareness, platform-specific thresholds
- R007 (Juniper JunOS health check) — Delivered with RE/PFE separation, alarm-first triage, dual-RE failover detection
- R008 (Arista EOS health check) — Delivered with agent monitoring, MLAG state validation, VXLAN/EVPN DC extensions

## Requirements Validated

- R006 — `agentskills validate` exit 0, `scripts/validate.sh` PASS, body 1708 words ≤ 2700, dual-platform coverage confirmed (IOS-XE 12 refs, NX-OS 14 refs in Procedure)
- R007 — `agentskills validate` exit 0, `scripts/validate.sh` PASS, body 2326 words ≤ 2700, mastership/alarm-first triage confirmed
- R008 — `agentskills validate` exit 0, `scripts/validate.sh` PASS, body 2643 words ≤ 2700, MLAG/VXLAN/agent health confirmed

## New Requirements Surfaced

- none

## Requirements Invalidated or Re-scoped

- none

## Deviations

None.

## Known Limitations

- Arista skill at 2643 words is 98% of the 2700 budget — future skills with similar DC-extension depth may need to offload more aggressively to references/
- Token budget metric is word count as proxy (~1.8 tokens/word) — actual token count varies by model tokenizer

## Follow-ups

- none

## Files Created/Modified

- `skills/cisco-device-health/SKILL.md` — Dual-platform Cisco health check skill (1708 words)
- `skills/cisco-device-health/references/cli-reference.md` — IOS-XE/NX-OS side-by-side CLI tables
- `skills/cisco-device-health/references/threshold-tables.md` — Platform-specific thresholds with 4 severity tiers
- `skills/juniper-device-health/SKILL.md` — JunOS health check skill with RE/PFE separation (2326 words)
- `skills/juniper-device-health/references/cli-reference.md` — JunOS CLI tables by RE/PFE/Alarm subsystems
- `skills/juniper-device-health/references/threshold-tables.md` — JunOS thresholds with commit spike norms
- `skills/arista-device-health/SKILL.md` — EOS health check skill with agent monitoring and DC extensions (2643 words)
- `skills/arista-device-health/references/cli-reference.md` — EOS CLI tables including agent/MLAG/VXLAN subsystems
- `skills/arista-device-health/references/threshold-tables.md` — EOS thresholds including MLAG state and agent health
- `README.md` — Added 3 new rows to skill catalog table

## Forward Intelligence

### What the next slice should know
- Token budget is proven: dual-platform at 1708 words (63%), single-platform at 2326–2643 (86–98%). Skills with multiple optional extension sections (like Arista's MLAG+VXLAN) push close to the limit. Routing protocol skills (S03) should plan for offloading vendor CLI reference tables to references/ early.
- The `[IOS-XE]` / `[NX-OS]` labeled code block pattern works well for dual-platform procedure steps. S03's multi-vendor routing skills (BGP, OSPF, IS-IS) will need a similar approach but across 3 vendors — consider whether 3-way labeled blocks remain scannable or need a different structure.

### What's fragile
- Arista body word count at 2643/2700 — adding any new DC extension section would breach the budget. If S04's interface-health skill reuses this pattern with vendor-specific sections, measure early.

### Authoritative diagnostics
- `bash scripts/validate.sh` — validates all skills in one pass, reports per-skill per-check results with error count. This is the single slice-level verification command.
- `agentskills validate skills/<name>` — spec-level validation per skill. Must be invoked per-directory, not on parent.

### What assumptions changed
- Original concern that ~5000 tokens might not fit deep procedural content — confirmed it fits comfortably. Even the most complex skill (Arista with DC extensions) used only 98% of the budget.
