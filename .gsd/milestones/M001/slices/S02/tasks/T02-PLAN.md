---
estimated_steps: 5
estimated_files: 7
---

# T02: Write Juniper JunOS and Arista EOS skills, update README catalog

**Slice:** S02 — Multi-Vendor Device Health Checks
**Milestone:** M001

## Description

Create the Juniper JunOS and Arista EOS device health check skills, then update the README catalog with all three new skills. These follow the pattern proven in T01 but each encodes genuinely different vendor health models — JunOS's RE/PFE separation with alarm-first triage, and EOS's Linux-native architecture with MLAG/VXLAN DC extensions.

## Steps

1. Create `skills/juniper-device-health/SKILL.md` with all 6 frontmatter keys (`name: juniper-device-health`, `metadata.safety: read-only`). Write all 7 H2 sections:
   - **Procedure** starts with RE mastership check as mandatory first step (wrong RE = wrong data). Then RE health, PFE health (separate from RE), alarm analysis as a first-class step, system resources, environment.
   - **Decision Trees** reflect JunOS-specific patterns: alarm severity triage (Major/Minor), RE failover detection, PFE vs RE health distinction.
   - JunOS alarms are first-class — `show chassis alarms` and `show system alarms` get dedicated procedure attention.
2. Create Juniper references/: `cli-reference.md` (organized by RE, PFE, Alarms, System, Environment subsystems) and `threshold-tables.md` (JunOS-specific thresholds including RE CPU spike norms during commit).
3. Create `skills/arista-device-health/SKILL.md` with all 6 frontmatter keys (`name: arista-device-health`, `metadata.safety: read-only`). Write all 7 H2 sections:
   - **Procedure** covers core device health first (CPU, memory, interfaces, environment), then MLAG state validation and VXLAN/EVPN health as DC-specific extension steps. Include EOS agent/daemon health via `show agent`.
   - **Decision Trees** include MLAG state triage (often the single most important DC assessment) and agent health diagnosis.
   - Linux-native commands (`bash top`, etc.) noted as valid troubleshooting options.
4. Create Arista references/: `cli-reference.md` (organized by System, Interfaces, MLAG, VXLAN/EVPN, Environment subsystems) and `threshold-tables.md` (EOS-specific thresholds including MLAG health indicators).
5. Update `README.md` catalog table: add rows for cisco-device-health, juniper-device-health, arista-device-health. Run full validation suite.

## Must-Haves

- [ ] Juniper SKILL.md has RE mastership check as mandatory first procedure step
- [ ] Juniper skill treats alarm analysis as a first-class procedure step, not an afterthought
- [ ] Juniper skill separates RE health from PFE health in procedure and decision trees
- [ ] Arista skill covers core health first, then MLAG/VXLAN as DC-specific extensions
- [ ] Arista skill includes agent/daemon health check (`show agent`)
- [ ] Both skills have all 6 frontmatter keys and all 7 required H2 sections
- [ ] Both skills have references/ with cli-reference.md and threshold-tables.md
- [ ] README catalog table has rows for all 3 new skills
- [ ] All 4 skills (including example) pass `agentskills validate` and `scripts/validate.sh`

## Verification

- `agentskills validate skills/juniper-device-health` → exit 0
- `agentskills validate skills/arista-device-health` → exit 0
- `bash scripts/validate.sh` → all checks PASS across all 4 skill directories
- README contains "cisco-device-health", "juniper-device-health", "arista-device-health" in catalog table
- Grep confirms "mastership" in Juniper SKILL.md Procedure section
- Grep confirms "MLAG" in Arista SKILL.md Procedure section

## Inputs

- `skills/cisco-device-health/SKILL.md` — T01 output, pattern to follow for structure and depth
- `skills/example-device-health/SKILL.md` — reference implementation for frontmatter and section format
- S02-RESEARCH.md — JunOS RE/PFE architecture, EOS MLAG/VXLAN details, threshold guidance

## Expected Output

- `skills/juniper-device-health/SKILL.md` — JunOS health check skill with RE/PFE and alarm focus
- `skills/juniper-device-health/references/cli-reference.md` — JunOS command tables
- `skills/juniper-device-health/references/threshold-tables.md` — JunOS-specific thresholds
- `skills/arista-device-health/SKILL.md` — EOS health check skill with MLAG/VXLAN extensions
- `skills/arista-device-health/references/cli-reference.md` — EOS command tables
- `skills/arista-device-health/references/threshold-tables.md` — EOS-specific thresholds
- `README.md` — updated catalog table with 3 new skill rows
