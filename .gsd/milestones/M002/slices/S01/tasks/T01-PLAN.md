---
estimated_steps: 5
estimated_files: 3
---

# T01: Author PAN-OS firewall audit skill with policy-model and CLI references

**Slice:** S01 — Vendor-Specific Firewall Audit Skills
**Milestone:** M002

## Description

Create the Palo Alto Networks PAN-OS firewall audit skill — the most complex vendor policy model in the slice. This is the risk-retirement task: if PAN-OS fits within ~2700 body words with vendor detail offloaded to `references/`, the remaining three vendors will too.

The skill must encode real PAN-OS expertise: zone-based security architecture, the App-ID → Content-ID → URL-ID identification chain, Security Profile Groups, and the policy evaluation order. It must NOT be a generic firewall best practices checklist.

Follow the "policy audit" procedure shape (Decision D028): systematic rule-by-rule analysis against best practices.

**Reference implementation:** Study `skills/bgp-analysis/SKILL.md` for the exact template format (frontmatter schema, 7 required H2 sections, multi-vendor CLI labeling style). Study `skills/bgp-analysis/references/cli-reference.md` and `skills/bgp-analysis/references/state-machine.md` for reference file patterns.

## Steps

1. **Create directory structure:** `mkdir -p skills/palo-alto-firewall-audit/references/`

2. **Author `SKILL.md`** with:
   - **Frontmatter:** `name: palo-alto-firewall-audit`, description mentioning PAN-OS zone-based policy audit with App-ID/Content-ID analysis, `license: Apache-2.0`, `metadata.safety: read-only`, author and version fields matching M001 pattern
   - **Opening paragraph** (before H2 sections): Explain what this skill does — policy-audit-driven analysis of PAN-OS security policies. Distinguish from generic firewall checklists. Note this covers PAN-OS 10.x+ on PA-series and VM-series.
   - **When to Use:** Security policy review after changes, annual audit, post-incident rule assessment, zone segmentation validation, Security Profile Group gap analysis, App-ID adoption assessment
   - **Prerequisites:** Read-only admin access to PAN-OS (or XML API), understanding of zone topology, knowledge of expected application allowlists and Security Profile Group assignments
   - **Procedure:** Use "policy audit" shape — systematic analysis flow:
     - Step 1: Zone architecture inventory — collect zones, zone protection profiles, inter-zone policy count
     - Step 2: Security policy rule-by-rule analysis — evaluate each rule for: overly permissive application matching (any vs specific App-ID), missing Security Profile Groups, disabled rules still in rulebase, shadowed rules, source/destination zone coverage
     - Step 3: App-ID coverage assessment — identify rules using `application any` vs specific App-IDs, check App-ID signature update status
     - Step 4: Security Profile Group validation — verify AV, Anti-Spyware, Vulnerability Protection, URL Filtering, File Blocking, WildFire profiles are bound to traffic-allowing rules
     - Step 5: Zone Protection Profile audit — validate flood protection (SYN/UDP/ICMP/Other), reconnaissance protection, packet-based attack protection settings per zone
     - Step 6: Decryption policy review — check SSL/TLS decryption rule coverage, certificate status, excluded categories
   - **Threshold Tables:** Policy rule severity thresholds (e.g., rules with `application any` + `action allow` = Critical, missing Security Profiles on allow rules = High, disabled rules in production = Medium)
   - **Decision Trees:** Rule remediation triage: overly permissive → App-ID migration path; missing profiles → profile group binding; shadowed rules → consolidation
   - **Report Template:** Structured findings with severity, rule name, zone pair, issue description, recommended remediation
   - **Troubleshooting:** Common audit obstacles — large rulebases (>500 rules), shared vs device-group policies in Panorama, dynamic address groups complicating analysis
   - **Body word count target:** ≤2700 words. Move detailed CLI syntax and policy model diagrams to reference files.

3. **Author `references/policy-model.md`:** Document PAN-OS security policy evaluation chain:
   - Packet flow: ingress zone → security policy lookup → App-ID (L4 session → app shift → content inspection) → Security Profiles (AV → AS → VP → URL → FB → WF → DP) → egress zone
   - Zone types: L3, L2, V-Wire, Tap, Tunnel
   - Policy rule matching: top-down first-match, intrazone default, interzone default, universal rules
   - Security Profile Group components and what each inspects
   - Panorama device group hierarchy: shared → device-group → pre-rules → local rules → post-rules

4. **Author `references/cli-reference.md`:** Read-only PAN-OS CLI and API commands organized by audit category:
   - Use table format like `skills/bgp-analysis/references/cli-reference.md`
   - Categories: Zone/Interface inventory, Security policy, App-ID status, Security Profiles, Zone Protection, Decryption, Session/Traffic, System status
   - Commands: `show running security-policy`, `show running zone`, `show running profile-group`, `test security-policy-match`, `show system info`, `show session all filter`, etc.
   - Note CLI vs XML API vs REST API access methods

5. **Validate:** Run `bash scripts/validate.sh` and verify the new skill passes. Check word count: `sed '1,/^---$/d' skills/palo-alto-firewall-audit/SKILL.md | sed '1,/^---$/d' | wc -w` must be ≤2700.

## Must-Haves

- [ ] `skills/palo-alto-firewall-audit/SKILL.md` exists with valid frontmatter (`name: palo-alto-firewall-audit`, `metadata.safety: read-only`)
- [ ] SKILL.md body contains all 7 required H2 sections
- [ ] SKILL.md body ≤2700 words
- [ ] `references/policy-model.md` documents PAN-OS evaluation chain (App-ID, Content-ID, zone model)
- [ ] `references/cli-reference.md` contains read-only PAN-OS commands in table format
- [ ] Procedure encodes PAN-OS-specific policy audit (zone pairs, App-ID, Security Profile Groups) — not generic firewall advice
- [ ] `bash scripts/validate.sh` passes including this skill

## Verification

- `bash scripts/validate.sh` exits 0 and counts this skill
- `sed '1,/^---$/d' skills/palo-alto-firewall-audit/SKILL.md | sed '1,/^---$/d' | wc -w` ≤ 2700
- `grep -l 'App-ID\|Content-ID' skills/palo-alto-firewall-audit/SKILL.md` returns the file
- `grep -l 'zone' skills/palo-alto-firewall-audit/SKILL.md` returns the file
- `ls skills/palo-alto-firewall-audit/references/` shows `policy-model.md` and `cli-reference.md`

## Inputs

- `skills/bgp-analysis/SKILL.md` — reference implementation for SKILL.md template format (frontmatter schema, 7 H2 sections, opening paragraph style)
- `skills/bgp-analysis/references/cli-reference.md` — reference implementation for CLI reference table format
- `skills/bgp-analysis/references/state-machine.md` — reference for how to structure a `policy-model.md` (analogous to protocol state machine)
- `scripts/validate.sh` — validation script that must pass
- Decision D025: one skill per vendor (not multi-vendor inline labels)
- Decision D027: all M002 skills are safety: read-only
- Decision D028: "policy audit" procedure shape — systematic rule-by-rule analysis

## Observability Impact

- **New validation surface:** `bash scripts/validate.sh` now discovers and validates `skills/palo-alto-firewall-audit/`. Output includes per-check OK/ERROR lines for this skill's frontmatter safety, 7 H2 sections, and references/ directory.
- **Word budget signal:** `sed '1,/^---$/d' skills/palo-alto-firewall-audit/SKILL.md | sed '1,/^---$/d' | wc -w` — body word count must remain ≤2700. Future edits can re-run to verify budget.
- **Vendor specificity signal:** `grep -l 'App-ID\|Content-ID\|zone' skills/palo-alto-firewall-audit/SKILL.md` — confirms PAN-OS-specific content hasn't been diluted into generic firewall advice.
- **Failure artifact:** If validate.sh fails for this skill, stderr contains named errors (e.g., "Missing required section: ## Procedure") for immediate diagnosis.

## Expected Output

- `skills/palo-alto-firewall-audit/SKILL.md` — complete PAN-OS firewall audit skill with vendor-specific content
- `skills/palo-alto-firewall-audit/references/policy-model.md` — PAN-OS security policy evaluation chain documentation
- `skills/palo-alto-firewall-audit/references/cli-reference.md` — read-only PAN-OS CLI commands in tabular format
