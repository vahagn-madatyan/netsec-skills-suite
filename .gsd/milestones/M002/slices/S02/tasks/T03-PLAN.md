---
estimated_steps: 5
estimated_files: 3
---

# T03: Build NIST compliance assessment skill with 800-53 control family mapping

**Slice:** S02 — Rule Analysis & Compliance Skills
**Milestone:** M002

## Description

Create the `nist-compliance-assessment` skill (R023) — a NIST CSF and SP 800-53 compliance mapping skill for network security posture. Builds on the "compliance assessment" procedure shape proven in T02 (CIS benchmark). NIST SP 800-53 and CSF are public-domain US government publications — no copyright constraint applies.

The skill maps 6 NIST 800-53 control families with direct network device relevance (AC, AU, CM, IA, SC, SI) to concrete device audit checks. It explicitly states that the remaining 14 of 20 families are out of scope. Focuses on CSF Protect (PR) and Detect (DE) functions per the roadmap requirement.

Uses vendor-agnostic approach with `[Cisco]`/`[JunOS]`/`[EOS]`/`[PAN-OS]` inline labels for platform-specific CLI examples.

Three files are created: SKILL.md + `references/control-reference.md` + `references/cli-reference.md`.

## Steps

1. Create directory `skills/nist-compliance-assessment/references/` (mkdir -p).

2. Create `skills/nist-compliance-assessment/SKILL.md` with:
   - **Frontmatter:** `name: nist-compliance-assessment`, `description` mentioning NIST CSF, 800-53, control family mapping, network security posture assessment, `license: Apache-2.0`, `metadata.safety: read-only`, `metadata.author: network-security-skills-suite`, `metadata.version: "1.0.0"`.
   - **Intro paragraph:** NIST Cybersecurity Framework (CSF) and SP 800-53 compliance assessment for network infrastructure. Maps network device configuration and operational state against 6 NIST 800-53 Rev 5 control families with direct network device relevance: Access Control (AC), Audit and Accountability (AU), Configuration Management (CM), Identification and Authentication (IA), System and Communications Protection (SC), and System and Information Integrity (SI). The remaining 14 control families (e.g., AT, CA, CP, IR, MA, MP, PE, PL, PM, PS, PT, RA, SA, SR) are outside the scope of network device assessment. Focuses on CSF Protect (PR) and Detect (DE) functions. Reference the two reference files.
   - **7 required H2 sections:**
     - `## When to Use` — federal compliance (FISMA), government contractor assessments, enterprise NIST adoption, security posture baselining, audit preparation for NIST-referenced frameworks (FedRAMP, CMMC)
     - `## Prerequisites` — read-only access to network devices, knowledge of system categorization (FIPS 199 — Low/Moderate/High impact), NIST 800-53 Rev 5 or CSF 2.0 document available, network architecture diagrams
     - `## Procedure` — 7 steps following "compliance assessment" shape:
       1. Assessment scope and framework selection — determine if mapping to CSF functions (Identify/Protect/Detect/Respond/Recover) or 800-53 control families; define system boundary and impact level (Low/Moderate/High)
       2. Access Control (AC) — account management (AC-2), access enforcement (AC-3), least privilege (AC-6), session controls (AC-12), remote access (AC-17). Check: local accounts, privilege levels, VTY/console ACLs, idle timeouts, SSH restrictions
       3. Audit and Accountability (AU) — audit events (AU-2), content of records (AU-3), audit storage (AU-4), audit review/analysis (AU-6), timestamps (AU-8). Check: syslog configuration, log destinations, NTP sync, buffer sizes, log retention
       4. Configuration Management (CM) — baseline config (CM-2), config change control (CM-3), least functionality (CM-7), config settings (CM-6). Check: running vs startup config diff, unused services disabled, config archive/rollback capability, secure boot
       5. Identification and Authentication (IA) — user identification (IA-2), authenticator management (IA-5), device identification (IA-3). Check: AAA server integration, password complexity, SSH key management, SNMP v3 credentials, 802.1X
       6. System and Communications Protection (SC) — boundary protection (SC-7), transmission confidentiality (SC-8), cryptographic protection (SC-13), network disconnect (SC-10). Check: ACL filtering at boundaries, encryption in transit (SSH/TLS/IPsec/MACsec), crypto algorithms (no DES/3DES/MD5), session timeouts
       7. System and Information Integrity (SI) — flaw remediation (SI-2), security alerts (SI-5), software integrity (SI-7), information handling (SI-4). Check: OS patch level, vulnerability status, image integrity verification, IDS/IPS configuration, file integrity monitoring
     - Use `[Cisco]`/`[JunOS]`/`[EOS]`/`[PAN-OS]` inline labels for CLI commands within steps.
     - `## Threshold Tables` — "Control Gap Severity" table classified by NIST 800-53 impact level and control baseline: Critical (High-impact baseline control gap — AC-2, SC-7 failures on boundary devices), High (Moderate-impact baseline gap — AU-2 logging absent, IA-2 no MFA for privileged access), Medium (Low-impact baseline gap — CM-7 unnecessary services, AU-8 NTP not authenticated), Low (Enhancement gap — advanced controls beyond required baseline)
     - `## Decision Trees` — control gap remediation flowchart: What is the system impact level? → Is this a baseline control? → Is there a compensating control? → Priority ranking
     - `## Report Template` — fenced markdown template: NIST Compliance Assessment Summary, System Categorization, Control Family Compliance Summary (AC/AU/CM/IA/SC/SI), CSF Function Mapping (PR/DE focus), Gap Analysis, POA&M (Plan of Action & Milestones)
     - `## Troubleshooting` — common issues: mapping CSF subcategories to 800-53 controls, handling inherited controls vs device-specific controls, multi-device scope aggregation, dealing with Rev 4 vs Rev 5 differences

3. Create `skills/nist-compliance-assessment/references/control-reference.md`:
   - NIST 800-53 Rev 5 control families mapped to network device audit checks
   - Table format: `| Control ID | Control Name | CSF Function | Network Device Audit Check | Baseline (L/M/H) |`
   - Organized by control family: AC, AU, CM, IA, SC, SI
   - Map each control to CSF functions (ID, PR, DE, RS, RC) — focus on PR and DE
   - Include baseline applicability (which controls apply at Low, Moderate, High impact levels)
   - Cover ~30-40 controls across the 6 families (5-7 per family)
   - NIST is public domain — control descriptions can be referenced directly

4. Create `skills/nist-compliance-assessment/references/cli-reference.md`:
   - CLI commands organized by NIST control family (AC, AU, CM, IA, SC, SI)
   - Covers Cisco IOS, JunOS, EOS, PAN-OS
   - Table format: `| Control Area | [Cisco] | [JunOS] | [EOS] | [PAN-OS] |` or per-vendor sections
   - Focus on read-only verification commands per D027

5. Verify:
   - `bash scripts/validate.sh` — should show 19 skills, 0 errors
   - `awk 'BEGIN{c=0} /^---$/{c++; if(c==2){found=1; next}} found{print}' skills/nist-compliance-assessment/SKILL.md | wc -w` — must be ≤2700
   - `ls skills/nist-compliance-assessment/references/ | wc -l` — must be 2
   - `grep -l 'NIST\|800-53\|CSF' skills/nist-compliance-assessment/SKILL.md` — confirms NIST content
   - `grep -l 'AC-2\|SC-7\|AU-2' skills/nist-compliance-assessment/SKILL.md` — confirms specific control IDs

## Must-Haves

- [ ] Frontmatter has `name: nist-compliance-assessment`, `metadata.safety: read-only`, `license: Apache-2.0`
- [ ] Body has all 7 required H2 sections: When to Use, Prerequisites, Procedure, Threshold Tables, Decision Trees, Report Template, Troubleshooting
- [ ] Procedure covers 6 NIST 800-53 control families: AC, AU, CM, IA, SC, SI
- [ ] Explicitly states 14 of 20 control families are out of scope
- [ ] Maps controls to CSF functions with PR/DE focus
- [ ] Uses `[Cisco]`/`[JunOS]`/`[EOS]`/`[PAN-OS]` inline labels
- [ ] Body ≤2700 words (use K001 awk method for word count)
- [ ] `references/` directory has exactly 2 files: `control-reference.md` and `cli-reference.md`
- [ ] `bash scripts/validate.sh` passes with 19 skills and 0 errors

## Verification

- `bash scripts/validate.sh` exits 0 with "Skills checked: 19" and "Result: PASS (0 errors)"
- `awk 'BEGIN{c=0} /^---$/{c++; if(c==2){found=1; next}} found{print}' skills/nist-compliance-assessment/SKILL.md | wc -w` ≤ 2700
- `ls skills/nist-compliance-assessment/references/ | wc -l` = 2
- `grep -l 'NIST\|800-53\|CSF' skills/nist-compliance-assessment/SKILL.md` returns the file path
- `grep -l 'AC-2\|SC-7' skills/nist-compliance-assessment/references/control-reference.md` confirms specific control IDs

## Inputs

- `skills/palo-alto-firewall-audit/SKILL.md` — reference for SKILL.md structure, frontmatter format, 7 H2 sections
- `skills/palo-alto-firewall-audit/references/cli-reference.md` — reference for CLI reference table format
- T02 output (CIS benchmark skill) — reference for "compliance assessment" procedure shape and compliance severity classification in Threshold Tables
- D027 decision — all M002 skills are read-only
- D028 decision — "compliance assessment" procedure shape
- K001 in KNOWLEDGE.md — use `awk` (not `sed`) for body word count on macOS

## Expected Output

- `skills/nist-compliance-assessment/SKILL.md` — NIST CSF and 800-53 compliance assessment skill mapping 6 control families to network device audit checks
- `skills/nist-compliance-assessment/references/control-reference.md` — NIST 800-53 control families with CSF mapping and network device audit checks
- `skills/nist-compliance-assessment/references/cli-reference.md` — CLI commands organized by NIST control family per vendor
