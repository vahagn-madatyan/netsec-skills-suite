# S01: Vendor-Specific Firewall Audit Skills — UAT

**Milestone:** M002
**Written:** 2026-03-16

## UAT Type

- UAT mode: artifact-driven
- Why this mode is sufficient: Skills are static SKILL.md files with no runtime component. Validation is structural (validate.sh, word count, vendor-specific content checks). No server, API, or live device interaction required.

## Preconditions

- Repository cloned at `/Users/djbeatbug/RoadToMillion/network-security-skills-suite`
- Node.js available (for `npx skills add . --list`)
- `bash` available (for `scripts/validate.sh`)
- All 12 M001 skills present and unmodified

## Smoke Test

Run `bash scripts/validate.sh` — expect output containing "Skills checked: 16" and "Result: PASS (0 errors)".

## Test Cases

### 1. Full suite validation passes with 16 skills

1. Run `bash scripts/validate.sh`
2. **Expected:** Exit code 0. Output contains "Skills checked: 16" and "Result: PASS (0 errors)". No lines containing "ERROR:" in output.

### 2. All 4 firewall audit skills are within 2700-word body budget

1. Run for each skill:
   ```bash
   for skill in palo-alto-firewall-audit fortigate-firewall-audit checkpoint-firewall-audit cisco-firewall-audit; do
     body_words=$(awk 'BEGIN{c=0} /^---$/{c++; if(c==2){found=1; next}} found{print}' "skills/$skill/SKILL.md" | wc -w | tr -d ' ')
     echo "$skill: $body_words"
   done
   ```
2. **Expected:** All 4 skills report ≤2700 words. Expected values: palo-alto ~1941, fortigate ~2692, checkpoint ~2537, cisco ~2694.

### 3. Each firewall skill has exactly 2 reference files

1. Run `ls skills/palo-alto-firewall-audit/references/`
2. Run `ls skills/fortigate-firewall-audit/references/`
3. Run `ls skills/checkpoint-firewall-audit/references/`
4. Run `ls skills/cisco-firewall-audit/references/`
5. **Expected:** Each directory contains exactly `cli-reference.md` and `policy-model.md`.

### 4. PAN-OS skill encodes vendor-specific content (not generic firewall advice)

1. Run `grep -c 'App-ID' skills/palo-alto-firewall-audit/SKILL.md`
2. Run `grep -c 'Content-ID' skills/palo-alto-firewall-audit/SKILL.md`
3. Run `grep -c 'Security Profile Group' skills/palo-alto-firewall-audit/SKILL.md`
4. Run `grep -c 'Zone Protection' skills/palo-alto-firewall-audit/SKILL.md`
5. **Expected:** All counts ≥1. Skill discusses PAN-OS zone-based architecture, App-ID identification chain, Security Profile Group validation — not generic "check firewall rules" advice.

### 5. FortiGate skill encodes VDOM/UTM vendor-specific content

1. Run `grep -c 'VDOM' skills/fortigate-firewall-audit/SKILL.md`
2. Run `grep -c 'UTM' skills/fortigate-firewall-audit/SKILL.md`
3. Run `grep -c 'FortiGuard' skills/fortigate-firewall-audit/SKILL.md`
4. Run `grep -c 'SD-WAN' skills/fortigate-firewall-audit/SKILL.md`
5. **Expected:** All counts ≥1. Skill encodes FortiOS VDOM segmentation, UTM profile binding, FortiGuard service validation, and SD-WAN security assessment.

### 6. Check Point skill encodes rulebase layer and blade content

1. Run `grep -c 'rulebase layer\|ordered layer\|inline layer' skills/checkpoint-firewall-audit/SKILL.md`
2. Run `grep -c 'blade' skills/checkpoint-firewall-audit/SKILL.md`
3. Run `grep -c 'SmartConsole' skills/checkpoint-firewall-audit/SKILL.md`
4. Run `grep -c 'SIC' skills/checkpoint-firewall-audit/SKILL.md`
5. **Expected:** All counts ≥1. Skill encodes R80+ management architecture, Unified Policy layer model, blade activation audit, and SIC trust verification.

### 7. Cisco skill encodes dual-platform ASA/FTD content

1. Run `grep -c '\[ASA\]' skills/cisco-firewall-audit/SKILL.md`
2. Run `grep -c '\[FTD\]' skills/cisco-firewall-audit/SKILL.md`
3. Run `grep -c 'security.level' skills/cisco-firewall-audit/SKILL.md`
4. Run `grep -c 'Access Control Policy\|ACP' skills/cisco-firewall-audit/SKILL.md`
5. Run `grep -c 'Snort' skills/cisco-firewall-audit/SKILL.md`
6. **Expected:** All counts ≥1. Skill covers both ASA (security levels, ACL, MPF) and FTD (ACP evaluation chain, Snort IPS) with platform-specific labels.

### 8. README catalog shows 4 firewall audit skills under Security Skills section

1. Run `grep -c 'firewall-audit' README.md`
2. Run `grep 'Security Skills' README.md`
3. Visually inspect that the 4 firewall rows appear under the "Security Skills" separator, not mixed with M001 network skills.
4. **Expected:** Count is 4. "Security Skills" header row exists. Each row has a vendor-specific description (not generic) and `read-only` safety tier.

### 9. All 4 skills have correct frontmatter

1. For each skill, verify frontmatter contains `metadata.safety: read-only`:
   ```bash
   for skill in palo-alto-firewall-audit fortigate-firewall-audit checkpoint-firewall-audit cisco-firewall-audit; do
     grep -A2 'metadata:' "skills/$skill/SKILL.md" | grep 'safety:'
   done
   ```
2. **Expected:** All 4 return `safety: read-only`.

### 10. No M001 skill regression

1. Run `bash scripts/validate.sh 2>&1 | grep -E 'bgp-analysis|ospf-analysis|eigrp-analysis|isis-analysis|cisco-device-health|juniper-device-health|arista-device-health|interface-health|network-topology-discovery|config-management|change-verification|example-device-health' | grep -c 'OK'`
2. **Expected:** All 12 M001 skills still validate. No ERROR lines for any M001 skill.

## Edge Cases

### Empty reference files would pass validate.sh

1. Run `wc -l skills/palo-alto-firewall-audit/references/policy-model.md skills/palo-alto-firewall-audit/references/cli-reference.md`
2. **Expected:** Both files have substantial content (>50 lines each). validate.sh checks file existence but not content — manual verification confirms reference files contain real vendor documentation, not empty stubs.

### Word count near budget boundary

1. Verify FortiGate (2692) and Cisco (2694) word counts are stable:
   ```bash
   awk 'BEGIN{c=0} /^---$/{c++; if(c==2){found=1; next}} found{print}' skills/fortigate-firewall-audit/SKILL.md | wc -w
   awk 'BEGIN{c=0} /^---$/{c++; if(c==2){found=1; next}} found{print}' skills/cisco-firewall-audit/SKILL.md | wc -w
   ```
2. **Expected:** Both ≤2700. These are the tightest skills — any future edits must preserve the budget.

### Procedure uses "policy audit" shape, not generic checklist

1. Open each SKILL.md `## Procedure` section.
2. **Expected:** Procedure follows systematic rule-by-rule analysis pattern (inventory → individual rule analysis → profile coverage → protection assessment), NOT a generic checklist of "check X, check Y" items. Each step references vendor-specific constructs.

## Failure Signals

- `bash scripts/validate.sh` exits non-zero or reports fewer than 16 skills
- Any skill body exceeds 2700 words
- Vendor-specific grep checks return 0 matches (skill contains generic content)
- README has fewer than 4 `firewall-audit` entries
- Missing `references/` directory or fewer than 2 files in any firewall skill
- Any M001 skill that previously passed now fails validation

## Requirements Proved By This UAT

- R017 — PAN-OS security policy audit with zone segmentation, App-ID, threat prevention profiles
- R018 — FortiGate policy audit with VDOM analysis, UTM validation, SD-WAN assessment
- R019 — Check Point policy audit with rulebase layers, blade activation, SmartConsole management
- R020 — ASA/FTD security audit with ACL analysis, NAT validation, Firepower IPS assessment

## Not Proven By This UAT

- Runtime correctness of CLI commands against actual firewall devices — skills are static procedural guidance
- Agent consumption quality — whether an AI agent can effectively follow the procedure end-to-end on a real device
- Integration with S02 compliance skills, S03 SIEM/incident response, S04 VPN/zero-trust (these slices are not yet built)
- `npx skills add . --list` discovering exactly 16 skills (not tested in this UAT since it depends on registry state)

## Notes for Tester

- Use the `awk` word count approach, NOT the `sed` double-strip approach from older plan documents. The `sed` approach returns 0 on macOS BSD sed. See K001 in `.gsd/KNOWLEDGE.md`.
- FortiGate (2692/2700) and Cisco (2694/2700) are near the word budget ceiling. If you spot-check and find they're over 2700, the `wc -w` result may vary slightly by locale — verify with `LANG=C wc -w`.
- The "Security Skills" section header is a bold-text row in the markdown table (`| **Security Skills** | | |`), not a markdown heading. Look for it within the table, not above it.
- Vendor specificity spot-check: pick any one skill and read the Procedure section. You should immediately recognize vendor-specific constructs (e.g., PAN-OS "App-ID shift re-evaluation", FortiOS "VDOM inter-link traffic inspection", Check Point "ordered layer all-must-accept", Cisco "Prefilter → SSL → Access → Intrusion"). If the procedure reads like generic "check your firewall rules" advice, that's a failure.
