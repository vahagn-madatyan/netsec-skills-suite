---
estimated_steps: 4
estimated_files: 1
---

# T04: Update README catalog with 4 firewall audit skills and run full 16-skill validation

**Slice:** S01 — Vendor-Specific Firewall Audit Skills
**Milestone:** M002

## Description

Close the slice by updating the README.md skill catalog table with 4 new firewall audit rows under a "Security Skills" section header, then run comprehensive validation across all 16 skills to confirm zero regressions and full compliance.

## Steps

1. **Add "Security Skills" section to README catalog table.** After the last M001 skill row (network-topology-discovery), add a section separator row and 4 new skill rows. The section header should visually separate Network Device Skills from Security Skills. Each description must mention vendor-specific capabilities — not generic "firewall audit" text. Format:

   ```
   | **Security Skills** | | |
   | [palo-alto-firewall-audit](skills/palo-alto-firewall-audit/SKILL.md) | PAN-OS zone-based security policy audit — App-ID/Content-ID analysis, Security Profile Group validation, zone protection assessment | `read-only` |
   | [fortigate-firewall-audit](skills/fortigate-firewall-audit/SKILL.md) | FortiGate/FortiOS policy audit — VDOM segmentation analysis, UTM profile binding validation, SD-WAN security assessment | `read-only` |
   | [checkpoint-firewall-audit](skills/checkpoint-firewall-audit/SKILL.md) | Check Point R80+ security policy audit — rulebase layer analysis, blade activation audit, SmartConsole management validation | `read-only` |
   | [cisco-firewall-audit](skills/cisco-firewall-audit/SKILL.md) | Cisco ASA/FTD dual-platform audit — ASA ACL/security-level analysis, FTD Access Control Policy and Snort IPS assessment | `read-only` |
   ```

2. **Run full validation:** `bash scripts/validate.sh` — expect output: "Skills checked: 16" and "Result: PASS (0 errors)"

3. **Run word count verification on all 4 new skills:**
   ```bash
   for skill in palo-alto-firewall-audit fortigate-firewall-audit checkpoint-firewall-audit cisco-firewall-audit; do
     body_words=$(sed '1,/^---$/d' "skills/$skill/SKILL.md" | sed '1,/^---$/d' | wc -w)
     echo "$skill: $body_words words"
     if [ "$body_words" -gt 2700 ]; then echo "FAIL: $skill over 2700 word budget"; fi
   done
   ```

4. **Verify no M001 regression:** Confirm validate.sh output shows all 12 original M001 skills still passing (no errors for any skill). Check `grep -c 'firewall-audit' README.md` returns 4.

## Must-Haves

- [ ] README catalog table has 16 rows (12 M001 + 4 M002 firewall)
- [ ] "Security Skills" section header visible in README table
- [ ] Each firewall skill description mentions vendor-specific capabilities
- [ ] All 4 new skills show `read-only` safety tier
- [ ] `bash scripts/validate.sh` passes all 16 skills with 0 errors
- [ ] All 4 new skills ≤2700 body words
- [ ] All 12 M001 skills still pass (no regression)

## Verification

- `bash scripts/validate.sh` reports "Skills checked: 16" and "Result: PASS (0 errors)"
- `grep -c 'firewall-audit' README.md` returns 4
- `grep 'Security Skills' README.md` finds the section header
- Word count check passes for all 4 new skills (all ≤2700)

## Observability Impact

- **Validation surface:** `bash scripts/validate.sh` now reports "Skills checked: 16" (up from 12). Any missing or malformed skill row in README will cause the count to differ from the expected 16.
- **Catalog inspection:** `grep -c 'firewall-audit' README.md` returns 4 — confirms all 4 firewall skills are cataloged. `grep 'Security Skills' README.md` confirms the section header exists.
- **Regression detection:** validate.sh output lists each skill with pass/fail. Any M001 skill regression appears as an `ERROR:` line in output. `bash scripts/validate.sh 2>&1 | grep -c 'ERROR:'` returns 0 for clean state.
- **Failure state:** If a firewall skill row is missing from README or has incorrect formatting, validate.sh will not count it. If the Security Skills header is absent, `grep 'Security Skills' README.md` returns nothing.

## Inputs

- `skills/palo-alto-firewall-audit/SKILL.md` — T01 output
- `skills/fortigate-firewall-audit/SKILL.md` — T02 output
- `skills/checkpoint-firewall-audit/SKILL.md` — T03 output
- `skills/cisco-firewall-audit/SKILL.md` — T03 output
- `README.md` — current README with 12-skill catalog table
- `scripts/validate.sh` — validation script

## Expected Output

- `README.md` — updated with 16-row catalog table including "Security Skills" section and 4 firewall audit skill rows with vendor-specific descriptions
