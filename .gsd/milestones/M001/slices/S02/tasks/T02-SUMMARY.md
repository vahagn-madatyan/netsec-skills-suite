---
id: T02
parent: S02
milestone: M001
provides:
  - Production Juniper JunOS device health check skill with RE/PFE separation, alarm-first triage, and dual-RE failover detection
  - Production Arista EOS device health check skill with agent monitoring, MLAG state validation, and VXLAN/EVPN DC extensions
  - Updated README catalog with all 3 new vendor skills
key_files:
  - skills/juniper-device-health/SKILL.md
  - skills/juniper-device-health/references/cli-reference.md
  - skills/juniper-device-health/references/threshold-tables.md
  - skills/arista-device-health/SKILL.md
  - skills/arista-device-health/references/cli-reference.md
  - skills/arista-device-health/references/threshold-tables.md
  - README.md
key_decisions:
  - Juniper procedure opens with RE mastership verification as mandatory Step 1 — wrong RE yields wrong data on dual-RE systems. Alarms are Step 2, before any resource checks, because JunOS alarms often identify the problem directly.
  - Arista procedure splits into core health (Steps 1-5) and DC extensions (Steps 6-7 for MLAG/VXLAN). DC steps are explicitly skippable when not configured, avoiding the skill being DC-only.
  - Agent/daemon health is a dedicated Step 3 in Arista — EOS's per-agent architecture means a single crashed agent can silently break a subsystem even when aggregate metrics look normal.
patterns_established:
  - Single-platform skill structure follows the same 7 H2 sections with vendor-specific depth in Procedure and Decision Trees. No structural divergence from the dual-platform Cisco pattern.
  - DC-specific extension steps (MLAG, VXLAN/EVPN) as opt-in procedure steps with explicit skip guidance. Reusable pattern for future skills with feature-specific extensions.
  - Alarm-first triage for platforms where alarms are first-class (JunOS). Other platforms may adopt this if alarm systems are prominent.
observability_surfaces:
  - none
duration: ~25m
verification_result: passed
completed_at: 2026-03-15
blocker_discovered: false
---

# T02: Write Juniper JunOS and Arista EOS skills, update README catalog

**Created Juniper JunOS and Arista EOS device health check skills with vendor-specific procedural depth, plus updated README catalog with all 3 new vendor skill rows.**

## What Happened

Built both skills following the pattern from T01's Cisco skill but with genuinely different vendor health models — not command substitution.

Juniper skill encodes JunOS's RE/PFE architecture: mastership verification is mandatory first step (data from wrong RE is invalid), alarm analysis is Step 2 as a first-class triage gate (Major alarms take priority over everything), RE health and PFE health are separate procedure steps and separate decision tree branches. Threshold tables account for RE CPU commit spikes being normal behavior. References include RE/PFE/alarm-organized CLI tables.

Arista skill encodes EOS's Linux-native and agent-based architecture: core health (Steps 1-5) covers CPU, memory, agent/daemon health, interfaces, and environment. Agent health is a dedicated step because EOS runs each subsystem as an independent process — a crashed Bgp agent means BGP is down even if system CPU is 10%. MLAG (Step 6) and VXLAN/EVPN (Step 7) are DC extensions with explicit skip guidance. Decision trees include MLAG state triage as its own subtree. Linux-native commands (`bash top`, `bash free -m`) documented as valid supplements to EOS show commands.

Updated README catalog table with cisco-device-health, juniper-device-health, and arista-device-health rows.

Word counts: Juniper body 2326 words, Arista body 2643 words — both well within the ~2700 word budget.

## Verification

All slice-level verification checks pass:

- `agentskills validate skills/juniper-device-health` → exit 0 ✓
- `agentskills validate skills/arista-device-health` → exit 0 ✓
- `agentskills validate skills/cisco-device-health` → exit 0 ✓ (prior, confirmed still passes)
- `bash scripts/validate.sh` → PASS, 4 skills checked, 0 errors ✓
- README.md contains rows for cisco-device-health, juniper-device-health, arista-device-health (3 matches) ✓
- Grep confirms "mastership" in Juniper SKILL.md Procedure section ✓
- Grep confirms "MLAG" in Arista SKILL.md Procedure section ✓
- Grep confirms "show agent" in Arista SKILL.md Procedure section ✓
- Juniper body: 2326 words ≤ 2700 ✓
- Arista body: 2643 words ≤ 2700 ✓

## Diagnostics

None — read-only skill files with no runtime behavior. Validate with `agentskills validate skills/juniper-device-health`, `agentskills validate skills/arista-device-health`, and `bash scripts/validate.sh`.

## Deviations

None.

## Known Issues

None.

## Files Created/Modified

- `skills/juniper-device-health/SKILL.md` — JunOS health check skill with RE/PFE separation, alarm-first triage, dual-RE failover
- `skills/juniper-device-health/references/cli-reference.md` — JunOS CLI tables organized by RE, PFE, Alarms, System, Interfaces, Routing, Environment
- `skills/juniper-device-health/references/threshold-tables.md` — JunOS thresholds including commit spike norms and per-FPC PFE thresholds
- `skills/arista-device-health/SKILL.md` — EOS health check skill with agent monitoring, MLAG/VXLAN DC extensions
- `skills/arista-device-health/references/cli-reference.md` — EOS CLI tables organized by System, Agent, Interfaces, MLAG, VXLAN/EVPN, Environment
- `skills/arista-device-health/references/threshold-tables.md` — EOS thresholds including agent health, MLAG state, VXLAN/EVPN peer health
- `README.md` — Added 3 new skill rows to catalog table (cisco-device-health, juniper-device-health, arista-device-health)
