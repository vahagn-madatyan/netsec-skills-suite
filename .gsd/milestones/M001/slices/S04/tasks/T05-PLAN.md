---
estimated_steps: 4
estimated_files: 1
---

# T05: Update README catalog and run final M001 end-to-end validation

**Slice:** S04 — Network Operations & Change Management
**Milestone:** M001

## Description

Add 4 new skill rows to the README catalog table and run comprehensive end-to-end validation across all M001 skills. This is the M001 completion gate — confirming that all 12 real skills pass validation, safety tiers are correct, the README is complete, and `npx skills add` discovers the full set.

## Steps

1. **Update the README.md skill catalog table.** Add 4 new rows after the existing routing protocol rows, maintaining alphabetical order within each category grouping. The new rows are:
   - `change-verification` — Pre/post change verification with baseline capture, diff analysis, and rollback guidance (Cisco/JunOS/EOS) — `read-write`
   - `config-management` — Config backup, drift detection, and golden config validation with compliance checking (Cisco/JunOS/EOS) — `read-write`
   - `interface-health` — Interface error analysis — CRC, discards, resets, optical power monitoring with threshold tables (Cisco/JunOS/EOS) — `read-only`
   - `network-topology-discovery` — Network topology discovery via CDP/LLDP, ARP/MAC tables, and routing table analysis (Cisco/JunOS/EOS) — `read-only`

   Each row follows the existing format: `| [skill-name](skills/skill-name/SKILL.md) | Description | \`safety-tier\` |`

2. **Run full validation across all skills:**
   - `bash scripts/validate.sh` → must show 12+ skills checked (excluding example or including it — either way 0 errors), PASS
   - Confirm each new skill is included in the validation output

3. **Verify safety tier correctness across the whole repo:**
   - `grep -l 'safety: read-write' skills/*/SKILL.md` → should return exactly `config-management` and `change-verification`
   - All other skills should have `safety: read-only`

4. **Run discovery check:**
   - `npx skills add . --list` → should discover all skills
   - Verify total count matches expected (12 real + 1 example = 13 discoverable skills)

## Must-Haves

- [ ] README catalog has 13 total rows (1 example + 8 existing real + 4 new)
- [ ] New rows have correct descriptions and safety tiers
- [ ] `bash scripts/validate.sh` passes with 0 errors across all skills
- [ ] Only config-management and change-verification have `read-write` safety tier
- [ ] `npx skills add . --list` discovers all skills

## Verification

- `bash scripts/validate.sh` → 0 errors, PASS
- `grep -c '|' README.md | ...` or manually confirm 13 skill rows in catalog
- `grep -l 'safety: read-write' skills/*/SKILL.md` → exactly 2 files (config-management, change-verification)
- `npx skills add . --list` → discovers all 13 skills

## Inputs

- T01 output: `skills/interface-health/` with SKILL.md + 2 reference files
- T02 output: `skills/network-topology-discovery/` with SKILL.md + 2 reference files
- T03 output: `skills/config-management/` with SKILL.md + 2 reference files
- T04 output: `skills/change-verification/` with SKILL.md + 2 reference files
- `README.md` — existing file with 8 real skill rows + 1 example row
- `scripts/validate.sh` — validation script

## Expected Output

- `README.md` — Updated with 4 new catalog rows (13 total), complete M001 skill catalog
