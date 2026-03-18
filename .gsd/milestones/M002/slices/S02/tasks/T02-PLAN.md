---
estimated_steps: 5
estimated_files: 3
---

# T02: Build CIS benchmark audit skill with copyright-safe control reference

**Slice:** S02 — Rule Analysis & Compliance Skills
**Milestone:** M002

## Description

Create the `cis-benchmark-audit` skill (R022) — a CIS benchmark compliance assessment skill for network devices. This is the **key risk retirement for M002** (D026): the `references/control-reference.md` must demonstrate the copyright-safe approach — cite CIS control IDs and section categories WITHOUT reproducing CIS benchmark text, remediation steps, or rationale.

This skill introduces the "compliance assessment" procedure shape (D028): map device config to framework controls. Covers 4 platforms that CIS publishes benchmarks for: Cisco IOS, PAN-OS, JunOS, Check Point.

**COPYRIGHT CONSTRAINT (D026):** CIS benchmarks are commercially licensed. The skill must:
- ✅ Reference CIS control IDs (e.g., "1.1.1", "2.3.2")
- ✅ Reference CIS section category names (e.g., "Management Plane Hardening")
- ✅ Independently describe what config area to audit and which CLI commands to use
- ❌ NOT reproduce CIS benchmark remediation text, rationale, or exact configuration commands from CIS
- ❌ NOT copy CIS scoring methodology text or audit procedure descriptions

Three files are created: SKILL.md + `references/control-reference.md` + `references/cli-reference.md`.

## Steps

1. Create directory `skills/cis-benchmark-audit/references/` (mkdir -p).

2. Create `skills/cis-benchmark-audit/SKILL.md` with:
   - **Frontmatter:** `name: cis-benchmark-audit`, `description` mentioning CIS benchmark compliance, multi-vendor, management/control/data plane audit, `license: Apache-2.0`, `metadata.safety: read-only`, `metadata.author: network-security-skills-suite`, `metadata.version: "1.0.0"`.
   - **Intro paragraph:** CIS benchmark compliance assessment for network infrastructure devices. Maps device configuration against CIS benchmark controls organized by Management Plane, Control Plane, and Data Plane categories. Covers Cisco IOS, PAN-OS, JunOS, and Check Point (the four platforms CIS publishes network device benchmarks for). References control IDs for traceability without reproducing copyrighted benchmark content (see D026). Reference the two reference files.
   - **7 required H2 sections:**
     - `## When to Use` — annual/quarterly compliance audit, pre-audit preparation, new device commissioning baseline, post-upgrade verification
     - `## Prerequisites` — read-only access to target device, CIS benchmark document for the specific platform/version (referenced by ID only — the operator must obtain their own copy), understanding of platform management architecture
     - `## Procedure` — 6 steps following "compliance assessment" shape:
       1. Platform identification and CIS benchmark selection (identify device type, OS version, select matching CIS benchmark by ID — e.g., "CIS Cisco IOS 16 Benchmark v1.1.0")
       2. Management Plane audit — SSH configuration, AAA/TACACS+/RADIUS, NTP authentication, logging (syslog/SNMP traps), SNMP v3 hardening, login banners. Use per-vendor CLI commands with vendor labels or short vendor subsections.
       3. Control Plane audit — routing protocol authentication (OSPF/BGP MD5/SHA, IS-IS auth), Control Plane Policing/Protection (CoPP), ICMP rate limiting, ARP inspection, DHCP snooping
       4. Data Plane audit — ACL baseline (explicit deny logging), uRPF (unicast reverse path forwarding), storm control, port security/802.1X, encryption (MACsec, IPsec for management)
       5. Compliance scoring and gap analysis — count pass/fail/not-applicable per section, calculate compliance percentage per plane, identify critical gaps
       6. Priority-ranked remediation plan — order findings by CIS control level (Level 1 = essential, Level 2 = defense-in-depth), group by effort, note dependencies
     - `## Threshold Tables` — "Compliance Violation Severity" table: Critical (Level 1 control fail — management access without AAA, SNMP v1/v2c exposed, no logging), High (Level 1 control fail — partial NTP auth, weak encryption, missing banner), Medium (Level 2 control fail — missing CoPP, no uRPF, storm control disabled), Low (Level 2 control — cosmetic banners, optional hardening not applied)
     - `## Decision Trees` — compliance remediation priority: Is it a Level 1 control? → Is the device internet-facing? → Is there a compensating control? → Priority ranking
     - `## Report Template` — fenced markdown template: CIS Benchmark Assessment Summary, Device Info, Benchmark Reference (ID only), Compliance Score by Plane, Critical Findings, Remediation Plan
     - `## Troubleshooting` — common issues: benchmark version mismatch, platform-specific config location differences, controls that don't apply to all deployment models
   - Keep body under 2700 words — heavy offload of per-vendor control mappings to `references/control-reference.md`.

3. Create `skills/cis-benchmark-audit/references/control-reference.md`:
   - **This file retires the D026 copyright risk.**
   - Table format mapping CIS control IDs to audit checks. Columns: `| CIS Section | Category | Config Area to Check | Audit CLI |`
   - Organized by plane: Management Plane, Control Plane, Data Plane
   - Cover 4 platforms with labeled subsections or multi-row entries: Cisco IOS, PAN-OS, JunOS, Check Point
   - Target ~30-40 high-impact controls across all vendors (8-10 per vendor)
   - **COPYRIGHT RULES for this file:**
     - USE CIS control IDs (e.g., "1.1.1", "2.3.1.1") — these are factual references
     - USE CIS section category names (e.g., "Management Plane", "Control Plane") — these are generic descriptors
     - WRITE ORIGINAL descriptions of what config area to check — do NOT copy from CIS
     - LIST the CLI command an operator would run to audit that control — these are vendor documentation, not CIS content
     - Do NOT include CIS remediation text, CIS rationale text, or CIS scoring methodology

4. Create `skills/cis-benchmark-audit/references/cli-reference.md`:
   - Read-only CLI commands organized by CIS benchmark category (Management Plane / Control Plane / Data Plane)
   - Covers Cisco IOS, PAN-OS, JunOS, Check Point
   - Table format: `| Function | CLI Command |` with per-vendor sections
   - Focus on audit/verification commands — not remediation commands (read-only per D027)

5. Verify:
   - `bash scripts/validate.sh` — should show 18 skills, 0 errors
   - `awk 'BEGIN{c=0} /^---$/{c++; if(c==2){found=1; next}} found{print}' skills/cis-benchmark-audit/SKILL.md | wc -w` — must be ≤2700
   - `ls skills/cis-benchmark-audit/references/ | wc -l` — must be 2
   - `grep -c '\.[0-9]' skills/cis-benchmark-audit/references/control-reference.md` — should return many matches (control IDs)
   - `grep -l 'CIS' skills/cis-benchmark-audit/SKILL.md` — confirms CIS references
   - Scan `references/control-reference.md` to confirm NO reproduced benchmark text (no "Remediation:", no "Rationale:", no copied configuration commands from CIS)

## Must-Haves

- [ ] Frontmatter has `name: cis-benchmark-audit`, `metadata.safety: read-only`, `license: Apache-2.0`
- [ ] Body has all 7 required H2 sections: When to Use, Prerequisites, Procedure, Threshold Tables, Decision Trees, Report Template, Troubleshooting
- [ ] Procedure covers: platform ID, Management Plane, Control Plane, Data Plane, compliance scoring, remediation plan
- [ ] `references/control-reference.md` cites CIS control IDs + categories only — NO reproduced benchmark text (D026)
- [ ] Body ≤2700 words (use K001 awk method for word count)
- [ ] `references/` directory has exactly 2 files: `control-reference.md` and `cli-reference.md`
- [ ] `bash scripts/validate.sh` passes with 18 skills and 0 errors

## Verification

- `bash scripts/validate.sh` exits 0 with "Skills checked: 18" and "Result: PASS (0 errors)"
- `awk 'BEGIN{c=0} /^---$/{c++; if(c==2){found=1; next}} found{print}' skills/cis-benchmark-audit/SKILL.md | wc -w` ≤ 2700
- `ls skills/cis-benchmark-audit/references/ | wc -l` = 2
- `grep -c '\.[0-9]' skills/cis-benchmark-audit/references/control-reference.md` returns many matches
- `grep -l 'CIS' skills/cis-benchmark-audit/SKILL.md` returns the file path
- Manual scan of `control-reference.md` confirms no "Remediation:", "Rationale:", or reproduced CIS benchmark text

## Inputs

- `skills/palo-alto-firewall-audit/SKILL.md` — reference for SKILL.md structure, frontmatter format, 7 H2 sections, Threshold Tables as severity classification, Report Template as fenced markdown block
- `skills/palo-alto-firewall-audit/references/cli-reference.md` — reference for CLI reference table format
- D026 decision — copyright-safe CIS reference strategy: control IDs + categories only, independently written audit descriptions
- D027 decision — all M002 skills are read-only
- D028 decision — "compliance assessment" procedure shape: map device config to framework controls
- K001 in KNOWLEDGE.md — use `awk` (not `sed`) for body word count on macOS

## Observability Impact

- **New validation surface:** `bash scripts/validate.sh` skill count increases from 17 to 18. The new `cis-benchmark-audit` skill is checked for all 7 H2 sections, frontmatter fields, and reference file count.
- **Copyright safety inspection:** `grep -c 'Remediation:\|Rationale:' skills/cis-benchmark-audit/references/control-reference.md` must return 0 — confirms no reproduced CIS benchmark text. `grep -c '\.[0-9]' skills/cis-benchmark-audit/references/control-reference.md` must return >20 — confirms CIS control IDs are present.
- **Word budget signal:** `awk 'BEGIN{c=0} /^---$/{c++; if(c==2){found=1; next}} found{print}' skills/cis-benchmark-audit/SKILL.md | wc -w` — body word count. Must be ≤2700.
- **Future agent inspection:** To verify this task's output, run `bash scripts/validate.sh 2>&1 | grep cis-benchmark-audit` to see per-check status. `ls skills/cis-benchmark-audit/references/` confirms 2 reference files exist.
- **Failure state:** If SKILL.md is missing a required H2 section, validate.sh emits `ERROR: cis-benchmark-audit — missing section: <name>`. If body exceeds 2700 words, it's detectable via the awk word count command above.

## Expected Output

- `skills/cis-benchmark-audit/SKILL.md` — CIS benchmark compliance assessment skill with Management/Control/Data Plane audit procedure
- `skills/cis-benchmark-audit/references/control-reference.md` — copyright-safe CIS control reference with control IDs, categories, and independently-written audit descriptions (NO reproduced benchmark text)
- `skills/cis-benchmark-audit/references/cli-reference.md` — read-only CLI commands organized by CIS benchmark category per platform
