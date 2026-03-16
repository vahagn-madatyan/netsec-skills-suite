# S02: Multi-Vendor Device Health Checks

**Goal:** Deliver 3 production device health check skills (Cisco IOS-XE/NX-OS, Juniper JunOS, Arista EOS) with vendor-specific procedural depth, threshold tables, decision trees, and structured report templates. Establish the token budget pattern for all future skills.
**Demo:** `bash scripts/validate.sh` passes with 4 skills (including S01's example). Each new SKILL.md encodes platform-specific triage procedures — not shallow command substitution. Cisco skill body is measured under ~5000 tokens.

## Must-Haves

- Cisco skill covers both IOS-XE and NX-OS with platform-specific callouts, not conflated commands (R006)
- Juniper skill reflects RE/PFE health model with mastership checks and alarm analysis as first-class steps (R007)
- Arista skill includes MLAG state validation and VXLAN/EVPN health as DC-specific extensions beyond core health (R008)
- Every SKILL.md has all 6 frontmatter keys and all 7 required H2 sections matching exact names in validate.sh
- Every skill has `references/` with cli-reference.md and threshold-tables.md
- SKILL.md body stays under ~5000 tokens (~2700 words max) per skill
- All 3 new skills pass `agentskills validate` and `scripts/validate.sh`
- README catalog table updated with 3 new rows (R004 supporting)
- `metadata.safety: read-only` on all three (show commands only)

## Verification

- `agentskills validate skills/cisco-device-health` → exit 0
- `agentskills validate skills/juniper-device-health` → exit 0
- `agentskills validate skills/arista-device-health` → exit 0
- `bash scripts/validate.sh` → all checks PASS across all 4 skill directories
- Cisco SKILL.md body word count ≤ 2700 (proxy for ~5000 token budget)
- README.md catalog table contains rows for cisco-device-health, juniper-device-health, arista-device-health

## Tasks

- [x] **T01: Write Cisco IOS-XE/NX-OS device health check skill** `est:45m`
  - Why: R006 — Cisco is the most deployed vendor and the dual-platform (IOS-XE + NX-OS) skill is the most complex. Serves as the token budget proof point.
  - Files: `skills/cisco-device-health/SKILL.md`, `skills/cisco-device-health/references/cli-reference.md`, `skills/cisco-device-health/references/threshold-tables.md`
  - Do: Write SKILL.md with dual-platform procedure using H3 subsections or labeled code blocks where IOS-XE and NX-OS diverge. Decision trees must account for NX-OS VDC architecture and different process model. Thresholds must be platform-aware (NX-OS `show system resources` vs IOS-XE `show processes cpu sorted`). Offload detailed per-subsystem CLI tables and expanded thresholds to references/. Measure body word count to confirm token budget.
  - Verify: `agentskills validate skills/cisco-device-health` exit 0; `bash scripts/validate.sh` passes for this skill; body word count ≤ 2700
  - Done when: Cisco skill passes both validators and body stays within token budget

- [x] **T02: Write Juniper JunOS and Arista EOS skills, update README catalog** `est:45m`
  - Why: R007, R008, R004 — Completes the three vendor health check skills and updates the public catalog. Juniper and Arista are each single-platform and follow the pattern established in T01.
  - Files: `skills/juniper-device-health/SKILL.md`, `skills/juniper-device-health/references/cli-reference.md`, `skills/juniper-device-health/references/threshold-tables.md`, `skills/arista-device-health/SKILL.md`, `skills/arista-device-health/references/cli-reference.md`, `skills/arista-device-health/references/threshold-tables.md`, `README.md`
  - Do: Write Juniper SKILL.md with RE/PFE separation, mastership check as mandatory first step, alarm analysis as first-class procedure step, PFE health distinct from RE health. Write Arista SKILL.md with core health first, then MLAG state validation and VXLAN/EVPN as DC-specific extension steps, agent/daemon health via `show agent`. Each gets references/ with cli-reference.md and threshold-tables.md. Add 3 new rows to README catalog table.
  - Verify: `agentskills validate` exit 0 for both new skills; `bash scripts/validate.sh` PASS across all 4 skills; README contains all 3 new catalog entries
  - Done when: All 3 new skills pass validation, README catalog is complete, slice verification commands all pass

## Files Likely Touched

- `skills/cisco-device-health/SKILL.md`
- `skills/cisco-device-health/references/cli-reference.md`
- `skills/cisco-device-health/references/threshold-tables.md`
- `skills/juniper-device-health/SKILL.md`
- `skills/juniper-device-health/references/cli-reference.md`
- `skills/juniper-device-health/references/threshold-tables.md`
- `skills/arista-device-health/SKILL.md`
- `skills/arista-device-health/references/cli-reference.md`
- `skills/arista-device-health/references/threshold-tables.md`
- `README.md`
