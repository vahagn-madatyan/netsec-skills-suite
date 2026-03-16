---
estimated_steps: 5
estimated_files: 3
---

# T01: Write Cisco IOS-XE/NX-OS device health check skill

**Slice:** S02 — Multi-Vendor Device Health Checks
**Milestone:** M001

## Description

Create the production Cisco device health check skill covering both IOS-XE and NX-OS platforms. This is the most complex S02 skill (dual-platform) and serves as the token budget proof point — if this fits within ~5000 tokens body, all other skills will too.

The key challenge is encoding genuine platform-specific triage knowledge, not shallow command substitution. IOS-XE separates RP/QFP for control/data plane health. NX-OS uses `show system resources` (not `show processes cpu sorted`), has VDC isolation, and a different process model. The skill must reflect these architectural differences in its procedure, decision trees, and thresholds.

## Steps

1. Create `skills/cisco-device-health/SKILL.md` with all 6 frontmatter keys (`name: cisco-device-health`, `metadata.safety: read-only`). Write the 7 required H2 sections with real procedural depth:
   - **Procedure** uses H3 subsections per triage area (CPU, memory, interfaces, environment, routing). Each step includes both IOS-XE and NX-OS commands in labeled code blocks where they diverge.
   - **Threshold Tables** in-body are summary-level with platform callouts. Detailed tables go to references/.
   - **Decision Trees** encode triage logic that accounts for NX-OS VDC architecture and IOS-XE QFP/RP split.
   - **Report Template** has structured output format.
2. Create `skills/cisco-device-health/references/cli-reference.md` — organized by subsystem (CPU, Memory, Interface, Environment, Routing), with IOS-XE and NX-OS command columns side by side and interpretation notes.
3. Create `skills/cisco-device-health/references/threshold-tables.md` — Normal/Warning/Critical/Emergency 4-tier format with platform-specific threshold values where they differ (e.g., NX-OS control plane CPU norms differ from IOS-XE RP CPU).
4. Measure body word count: `wc -w` on SKILL.md body (excluding frontmatter). Target ≤ 2700 words. If over, move detail to references/.
5. Run validators: `agentskills validate skills/cisco-device-health` and `bash scripts/validate.sh`.

## Must-Haves

- [ ] SKILL.md has all 6 frontmatter keys with `name: cisco-device-health` and `metadata.safety: read-only`
- [ ] All 7 H2 sections present with exact names matching validate.sh expectations
- [ ] Procedure covers both IOS-XE and NX-OS with platform-specific commands, not conflated
- [ ] Decision trees account for NX-OS VDC architecture and IOS-XE QFP/RP split
- [ ] Thresholds are platform-aware — NX-OS and IOS-XE have different normal baselines
- [ ] references/ contains cli-reference.md and threshold-tables.md
- [ ] SKILL.md body ≤ 2700 words (~5000 tokens)
- [ ] Passes `agentskills validate` and `scripts/validate.sh`

## Verification

- `agentskills validate skills/cisco-device-health` → "Valid skill" (exit 0)
- `bash scripts/validate.sh` → cisco-device-health checks all OK
- `wc -w` on SKILL.md body (after frontmatter) ≤ 2700
- Grep confirms both "IOS-XE" and "NX-OS" appear in the Procedure section

## Inputs

- `skills/example-device-health/SKILL.md` — reference implementation for structure, frontmatter schema, section names
- `skills/example-device-health/references/` — format reference for cli-reference.md and threshold-tables.md
- S02-RESEARCH.md — vendor-specific CLI commands, architecture notes, threshold guidance, token budget analysis

## Expected Output

- `skills/cisco-device-health/SKILL.md` — Production dual-platform Cisco health check skill
- `skills/cisco-device-health/references/cli-reference.md` — IOS-XE and NX-OS command tables by subsystem
- `skills/cisco-device-health/references/threshold-tables.md` — Platform-specific threshold tables with 4 severity tiers
