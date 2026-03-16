# S02: Multi-Vendor Device Health Checks — UAT

**Milestone:** M001
**Written:** 2026-03-15

## UAT Type

- UAT mode: artifact-driven
- Why this mode is sufficient: Skills are static markdown files with no runtime behavior. Validation is structural (frontmatter schema, section presence, naming) and content-based (word count, vendor-specific content checks). No live runtime to exercise.

## Preconditions

- Repository cloned locally
- Python `agentskills` CLI installed (`pip install agentskills`)
- `bash` available for `scripts/validate.sh`

## Smoke Test

Run `bash scripts/validate.sh` — should report 4 skills checked, 0 errors.

## Test Cases

### 1. All skills pass spec-level validation

1. Run `agentskills validate skills/cisco-device-health`
2. Run `agentskills validate skills/juniper-device-health`
3. Run `agentskills validate skills/arista-device-health`
4. **Expected:** Each prints "Valid skill: skills/<name>" and exits 0

### 2. All skills pass convention-level validation

1. Run `bash scripts/validate.sh`
2. **Expected:** 4 skills checked (example + 3 vendor), all checks OK, 0 errors

### 3. Token budget compliance

1. For each vendor skill, count body words (content after second `---` frontmatter delimiter)
2. **Expected:** Cisco ≤ 2700, Juniper ≤ 2700, Arista ≤ 2700

### 4. Cisco skill covers both platforms

1. Open `skills/cisco-device-health/SKILL.md`
2. Search Procedure section for "IOS-XE" and "NX-OS" references
3. **Expected:** Both platforms referenced with platform-labeled code blocks; NX-OS VDC context check present; IOS-XE QFP health referenced

### 5. Juniper skill has RE/PFE separation and alarm-first triage

1. Open `skills/juniper-device-health/SKILL.md`
2. Check procedure step ordering
3. **Expected:** Step 1 is RE mastership verification, Step 2 is alarm analysis, RE health and PFE health are separate procedure steps

### 6. Arista skill has DC extensions and agent health

1. Open `skills/arista-device-health/SKILL.md`
2. Check for MLAG, VXLAN/EVPN, and agent health content
3. **Expected:** Agent/daemon health is a dedicated procedure step; MLAG and VXLAN/EVPN are separate extension steps with skip guidance; `show agent` referenced

### 7. README catalog updated

1. Open `README.md`
2. Search for catalog table rows
3. **Expected:** Rows exist for cisco-device-health, juniper-device-health, arista-device-health with descriptions and safety tier

### 8. Reference files present and substantive

1. Check each skill has `references/cli-reference.md` and `references/threshold-tables.md`
2. Open each reference file
3. **Expected:** CLI references have vendor-specific commands organized by subsystem; threshold tables have severity tiers (Normal/Warning/Critical/Emergency or equivalent)

## Edge Cases

### Arista skill without DC features

1. Read Steps 6–7 of Arista SKILL.md Procedure section
2. **Expected:** Explicit skip guidance when MLAG/VXLAN not configured — skill should remain useful for non-DC Arista deployments

### NX-OS vs IOS-XE threshold divergence

1. Compare NX-OS and IOS-XE threshold tables in `skills/cisco-device-health/references/threshold-tables.md`
2. **Expected:** NX-OS CPU/memory baselines are offset higher than IOS-XE (reflecting Linux kernel overhead); tables are separate, not merged

## Failure Signals

- `agentskills validate` exits non-zero for any skill
- `scripts/validate.sh` reports any errors
- Body word count exceeds 2700 for any skill
- Missing `references/` directory or reference files in any skill
- IOS-XE or NX-OS not referenced in Cisco SKILL.md Procedure
- No mastership/alarm content in Juniper SKILL.md Procedure
- No MLAG/VXLAN/agent content in Arista SKILL.md Procedure
- Missing catalog rows in README.md

## Requirements Proved By This UAT

- R006 — Cisco IOS-XE/NX-OS device health check skill with dual-platform depth
- R007 — Juniper JunOS device health check skill with RE/PFE separation and alarm-first triage
- R008 — Arista EOS device health check skill with agent monitoring and DC extensions
- R004 (supporting) — README catalog updated with 3 new skill rows

## Not Proven By This UAT

- Runtime agent interaction quality — no test of loading a skill into a live agent session and measuring guidance quality (human judgment needed)
- `npx skills add` discovery of the new skills from this repo — infrastructure tested in S01, not re-tested here
- GitHub Actions CI execution — workflow syntax validated in S01, pending first real GHA run

## Notes for Tester

- All skills are `safety: read-only` — they guide show/display commands only, no configuration changes
- The Arista skill body (2643 words) is close to the 2700 limit — this is expected and documented as a known limitation for skills with DC-extension sections
- Reference files are designed for progressive disclosure — agents should load SKILL.md first and only fetch references/ when deeper detail is needed
