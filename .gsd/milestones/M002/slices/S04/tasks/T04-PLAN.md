---
estimated_steps: 4
estimated_files: 1
---

# T04: Update README catalog and run full suite verification

**Slice:** S04 — Additional Security Skills & Suite Finalization
**Milestone:** M002

## Description

Add the final 3 skill rows to the README catalog table and run the full M002 milestone verification battery. This task closes the milestone's final integration check: `npx skills add . --list` must discover all 25 skills.

The 3 new rows go under the existing "Security Skills" bold separator row in the catalog table. Do NOT create a new section header (per S01 Forward Intelligence).

## Steps

1. Add 3 rows to the README catalog table, immediately after the last existing security skill row (`incident-response-network`). The rows go under the existing `| **Security Skills** | | |` separator — do NOT add another separator or section header. New rows:
   ```
   | [vpn-ipsec-troubleshooting](skills/vpn-ipsec-troubleshooting/SKILL.md) | IPSec/IKE troubleshooting — IKE SA state machine diagnosis, crypto mismatch analysis, NAT-T detection, DPD tuning (Cisco/JunOS/PAN-OS/FortiGate) | `read-only` |
   | [zero-trust-assessment](skills/zero-trust-assessment/SKILL.md) | Zero-trust maturity assessment — 5-pillar scoring rubric (identity, device, network, application, data), NIST 800-207 alignment, micro-segmentation validation | `read-only` |
   | [wireless-security-audit](skills/wireless-security-audit/SKILL.md) | Wireless security audit — SSID policy analysis, 802.1X/EAP validation, rogue AP detection, WPA3 assessment (Cisco WLC/Aruba/Meraki) | `read-only` |
   ```

2. Run full suite validation:
   - `bash scripts/validate.sh` → must show "Skills checked: 25", "Result: PASS (0 errors)"
   - Verify zero regression: all 22 pre-existing skills still pass (validate.sh covers this — it checks every skill in skills/)

3. Run skills discovery:
   - `npx skills add . --list` → must report "Found 25 skills"
   - If it reports fewer, check that all 3 new skill directories have proper SKILL.md files

4. Final verification battery:
   - `grep -c 'vpn-ipsec\|zero-trust\|wireless-security' README.md` → 3
   - Word counts for all 3 new skills ≤2700 (awk K001 method)
   - All 3 new skills have references/ with exactly 2 files each
   - All 3 new skills have metadata.safety: read-only

## Must-Haves

- [ ] README catalog has 3 new rows under existing "Security Skills" header
- [ ] No new section separator rows added
- [ ] `bash scripts/validate.sh` → 25 skills, 0 errors
- [ ] `npx skills add . --list` → Found 25 skills
- [ ] Zero regression on all 22 pre-existing skills

## Verification

- `bash scripts/validate.sh 2>&1 | grep 'Skills checked'` → "Skills checked: 25"
- `bash scripts/validate.sh 2>&1 | grep 'Result'` → "Result: PASS (0 errors)"
- `npx skills add . --list 2>&1 | grep -i 'found'` → "Found 25 skills"
- `grep -c 'vpn-ipsec\|zero-trust\|wireless-security' README.md` → 3
- Count catalog table rows (excluding header and separator): `grep -c '^\| \[' README.md` → 25

## Inputs

- T01, T02, T03 completed: all 3 new skills created with SKILL.md + 2 reference files each
- `README.md` — current catalog has 22 skill rows plus "Security Skills" separator
- `scripts/validate.sh` — convention validator
- All 25 skill directories in `skills/`

## Expected Output

- `README.md` — Updated catalog with 25 skill rows total (12 M001 + 13 M002), complete "Security Skills" section with all 13 security skills
