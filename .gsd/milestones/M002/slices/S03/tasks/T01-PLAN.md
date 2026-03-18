---
estimated_steps: 5
estimated_files: 3
---

# T01: Build vulnerability-assessment skill with CVE mapping and CVSS scoring

**Slice:** S03 — Security Operations Skills
**Milestone:** M002

## Description

Create the vulnerability-assessment skill covering R024 (CVE assessment for network devices). This is the most structured of the three S03 skills — it follows the proven threshold-comparison pattern where CVSS scores map to severity tiers and remediation SLAs, similar to how M001 device health skills map resource utilization to severity thresholds.

The skill guides agents through: identifying device software versions → querying CVE databases → scoring with CVSS v3.1 → classifying by severity × exposure × exploitability → prioritizing remediation timelines. Uses 5-vendor inline labels (`[Cisco]`/`[JunOS]`/`[EOS]`/`[PAN-OS]`/`[FortiGate]`) for version retrieval commands.

NVD/CVE data is public domain — no copyright concerns (unlike S02's CIS benchmark skill).

## Steps

1. **Create `skills/vulnerability-assessment/references/cli-reference.md`** — Version and patch information retrieval commands organized by vendor. Include commands for: current software version, installed patches/hotfixes, hardware model identification, running vs startup config version, and NTP/uptime (for last-patched estimation). Cover all 5 vendors in table format. Each vendor needs: show version equivalent, show installed packages/patches, show hardware inventory. Approximate ~15 commands total across vendors.

2. **Create `skills/vulnerability-assessment/references/vulnerability-reference.md`** — CVSS v3.1 scoring breakdown (Base/Temporal/Environmental metric groups, Attack Vector/Complexity/Privileges/User Interaction/Scope/Impact classifications), NVD API query approach (search by CPE, by keyword, by CVE ID), severity-to-SLA mapping table (Critical 0-9.9→10.0 CVSS → 24hr/72hr/7d/30d/90d remediation windows), vendor-specific advisory sources with URLs: Cisco PSIRT (sec.cloudapps.cisco.com), Palo Alto Security Advisories (security.paloaltonetworks.com), Juniper JSA (supportportal.juniper.net), Fortinet PSIRT (fortiguard.com), Arista Security Advisories (arista.com/en/support/advisories-notices).

3. **Create `skills/vulnerability-assessment/SKILL.md`** — Full skill file with:
   - YAML frontmatter: name, description (CVE assessment focus), license Apache-2.0, metadata.safety: read-only
   - Intro paragraph explaining the skill assesses network device vulnerability posture via CVE mapping and CVSS scoring — not generic patch management
   - **When to Use**: vulnerability assessment requests, audit findings, post-advisory triage, compliance-driven patching cycles
   - **Prerequisites**: device CLI/API access, NVD/vendor advisory access, device inventory
   - **Procedure**: 6-step flow: (1) Inventory device versions using vendor-specific commands with `[Vendor]` labels, (2) Map versions to CPE identifiers, (3) Query NVD/vendor advisories for matching CVEs, (4) Score each CVE using CVSS v3.1 base metrics, (5) Classify by combined risk (CVSS severity × network exposure × exploit availability), (6) Generate prioritized remediation plan with SLA mapping
   - **Threshold Tables**: CVSS severity tiers (Critical ≥9.0, High 7.0-8.9, Medium 4.0-6.9, Low 0.1-3.9), remediation SLA table, exposure multiplier table (internet-facing vs internal vs management-only)
   - **Decision Trees**: Patch-now vs schedule vs accept-risk decision flow based on CVSS + exploit availability + exposure + compensating controls
   - **Report Template**: structured output with executive summary, critical CVE table, device-by-device findings, remediation timeline
   - **Troubleshooting**: version parsing issues, CPE matching failures, advisory source unavailability, false positives from EOL version detection
   - Target ≤2700 words. Reference cli-reference.md and vulnerability-reference.md for detailed commands and scoring tables.

4. **Verify the skill passes validation** — Run `bash scripts/validate.sh` and confirm it reports 20 skills checked with 0 errors. Run `awk 'BEGIN{c=0} /^---$/{c++; if(c==2){found=1; next}} found{print}' skills/vulnerability-assessment/SKILL.md | wc -w` and confirm ≤2700. Verify `ls skills/vulnerability-assessment/references/` shows exactly 2 files. Run `grep -c 'CVE\|CVSS\|NVD' skills/vulnerability-assessment/SKILL.md` and confirm ≥5.

5. **Fix any issues** — If word count exceeds 2700, compress Troubleshooting or Report Template prose (proven trim targets from S01). If validation fails, check frontmatter format and H2 section names against the 7 required sections.

## Must-Haves

- [ ] SKILL.md has `metadata.safety: read-only` in YAML frontmatter
- [ ] All 7 required H2 sections present: When to Use, Prerequisites, Procedure, Threshold Tables, Decision Trees, Report Template, Troubleshooting
- [ ] Body word count ≤2700 (use K001 `awk` method, not BSD `sed`)
- [ ] `references/cli-reference.md` exists with 5-vendor version retrieval commands
- [ ] `references/vulnerability-reference.md` exists with CVSS scoring and vendor advisory sources
- [ ] `grep -c 'CVE\|CVSS\|NVD' SKILL.md` returns ≥5
- [ ] `bash scripts/validate.sh` reports 20 skills, 0 errors

## Verification

- `bash scripts/validate.sh` exits 0, reports "Skills checked: 20" and "Result: PASS (0 errors)"
- `awk 'BEGIN{c=0} /^---$/{c++; if(c==2){found=1; next}} found{print}' skills/vulnerability-assessment/SKILL.md | wc -w` returns ≤2700
- `ls skills/vulnerability-assessment/references/` shows exactly `cli-reference.md` and `vulnerability-reference.md`
- `grep -c 'CVE\|CVSS\|NVD' skills/vulnerability-assessment/SKILL.md` returns ≥5
- All 19 prior skills still pass validation (0 errors total)

## Inputs

- Existing S01/S02 skills for structural reference (frontmatter format, H2 sections, vendor label convention, references/ pattern)
- Example frontmatter from `skills/palo-alto-firewall-audit/SKILL.md` — use same YAML structure
- K001 in KNOWLEDGE.md — use `awk` word count, not BSD `sed`
- D027 — all M002 skills are read-only
- D028 — this skill uses threshold-comparison procedure shape (CVSS scores as thresholds)

## Expected Output

- `skills/vulnerability-assessment/SKILL.md` — Complete CVE assessment skill (~2200-2600 body words) with 5-vendor version mapping, CVSS scoring, remediation prioritization
- `skills/vulnerability-assessment/references/cli-reference.md` — Version/patch retrieval CLI commands for Cisco, JunOS, EOS, PAN-OS, FortiGate
- `skills/vulnerability-assessment/references/vulnerability-reference.md` — CVSS v3.1 breakdown, NVD query approach, severity-to-SLA mapping, vendor advisory sources
- `bash scripts/validate.sh` reporting 20 skills, 0 errors
