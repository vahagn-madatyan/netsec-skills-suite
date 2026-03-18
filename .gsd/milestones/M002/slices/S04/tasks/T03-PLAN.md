---
estimated_steps: 5
estimated_files: 3
---

# T03: Build wireless security audit skill with multi-controller coverage

**Slice:** S04 — Additional Security Skills & Suite Finalization
**Milestone:** M002

## Description

Create the wireless security audit skill (R029) combining the policy audit procedure shape (from S01 firewall skills) with security assessment patterns. Uses new vendor labels: [Cisco WLC]/[Aruba]/[Meraki] — these are wireless controller platforms, not the network device vendors from M001.

Note: Meraki is API/dashboard-only for automation (no traditional CLI). The cli-reference.md should include Meraki Dashboard API endpoints alongside Cisco WLC and Aruba CLI commands.

Safety: read-only (D027). Body must be ≤2700 words.

## Steps

1. Create `skills/wireless-security-audit/references/security-standards.md` documenting wireless security standards:
   - 802.1X/EAP authentication state machine: Supplicant ↔ Authenticator ↔ RADIUS server interaction, EAP method types (EAP-TLS, PEAP, EAP-TTLS)
   - WPA3-Enterprise (192-bit mode, SAE, PMF — Protected Management Frames) vs WPA3-Personal requirements
   - WPA2 → WPA3 transition considerations (transition mode, backward compatibility)
   - Rogue AP classification: legitimate/managed, neighboring/interfering, malicious/rogue
   - WIDS/WIPS capabilities: detection, classification, containment mechanisms
   - RF security best practices: channel isolation, power level management, coverage design
   - Guest network isolation requirements: VLAN separation, bandwidth limits, captive portal

2. Create `skills/wireless-security-audit/references/cli-reference.md` with wireless controller commands:
   - [Cisco WLC]: `show wlan summary`, `show wlan <id>`, `show client summary`, `show rogue ap summary`, `show 802.11a/b`, `show radius summary`
   - [Aruba]: `show wlan ssid-profile`, `show ap database`, `show aaa authentication-server`, `show wids-event`, `show ap radio-database`
   - [Meraki]: Dashboard API endpoints — `GET /networks/{id}/wireless/ssids`, `GET /organizations/{id}/networks`, `GET /networks/{id}/wireless/clients`, `GET /networks/{id}/wireless/airMarshal` (Meraki has no CLI — API only for automation)
   - Table format organized by audit category: SSID config, authentication, rogue AP, RF, client

3. Create `skills/wireless-security-audit/SKILL.md` with:
   - Frontmatter: name, description, license: Apache-2.0, metadata.safety: read-only, metadata.author: network-security-skills-suite, metadata.version: "1.0.0"
   - Intro explaining wireless security audit approach with [Cisco WLC]/[Aruba]/[Meraki] vendor labels
   - 7 required H2 sections: When to Use, Prerequisites, Procedure, Threshold Tables, Decision Trees, Report Template, Troubleshooting
   - Procedure follows policy audit shape adapted for wireless: (1) SSID Policy Inventory → (2) Authentication & Encryption Audit → (3) 802.1X / RADIUS Validation → (4) Rogue AP Assessment → (5) RF Security Posture Review → (6) Report
   - Threshold Tables: encryption strength tiers (WPA3 > WPA2-Enterprise > WPA2-Personal > Open), rogue AP severity classification, RF signal thresholds
   - Decision Trees: SSID security triage — which SSIDs need immediate remediation, auth method upgrade paths
   - Key content: SSID security policy (encryption mode, auth method, VLAN assignment), 802.1X validation (RADIUS reachability, EAP method, cert chain), rogue AP detection methodology, RF assessment (channel utilization, power, containment), guest isolation (captive portal, bandwidth limits, VLAN separation)

4. Verify word count: `awk 'BEGIN{c=0} /^---$/{c++; if(c==2){found=1; next}} found{print}' skills/wireless-security-audit/SKILL.md | wc -w` → must be ≤2700. If over budget, compress Troubleshooting section.

5. Run validation: `bash scripts/validate.sh 2>&1 | grep -E 'Skills checked|Result'` → must show 25 skills, PASS.

## Must-Haves

- [ ] SKILL.md has valid frontmatter with `metadata.safety: read-only`
- [ ] All 7 required H2 sections present
- [ ] Procedure follows policy audit shape adapted for wireless: SSID inventory → auth/encryption → 802.1X → rogue AP → RF → report
- [ ] 3-vendor inline labels: [Cisco WLC], [Aruba], [Meraki]
- [ ] Meraki uses Dashboard API endpoints (not CLI commands) in references
- [ ] references/security-standards.md covers 802.1X/EAP, WPA3, rogue AP classification, RF security
- [ ] references/cli-reference.md has commands/endpoints for all 3 vendors
- [ ] Body ≤2700 words (awk K001 method)
- [ ] `bash scripts/validate.sh` passes with 25 skills

## Verification

- `bash scripts/validate.sh 2>&1 | grep 'Skills checked'` → "Skills checked: 25"
- `bash scripts/validate.sh 2>&1 | grep 'Result'` → "Result: PASS (0 errors)"
- `awk 'BEGIN{c=0} /^---$/{c++; if(c==2){found=1; next}} found{print}' skills/wireless-security-audit/SKILL.md | wc -w` → ≤2700
- `ls skills/wireless-security-audit/references/ | wc -l` → 2
- `grep -c '802.1X\|WPA3\|rogue\|SSID' skills/wireless-security-audit/SKILL.md` → ≥5
- `grep -c 'Meraki' skills/wireless-security-audit/SKILL.md` → ≥1

## Inputs

- `skills/palo-alto-firewall-audit/SKILL.md` — Policy audit procedure shape precedent (inventory → analysis → profile → assessment)
- `skills/cis-benchmark-audit/SKILL.md` — Threshold Tables scoring pattern for severity classification
- `scripts/validate.sh` — Convention validator
- T01, T02 completed: validate.sh passes 24 skills

## Expected Output

- `skills/wireless-security-audit/SKILL.md` — Wireless security audit skill with SSID/802.1X/rogue AP coverage, 3-vendor labels, ≤2700 words
- `skills/wireless-security-audit/references/security-standards.md` — 802.1X/EAP state machine, WPA3 requirements, rogue AP classification, RF security
- `skills/wireless-security-audit/references/cli-reference.md` — Wireless controller commands for Cisco WLC, Aruba, and Meraki API endpoints
