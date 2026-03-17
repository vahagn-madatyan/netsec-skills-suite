# S02: Rule Analysis & Compliance Skills — Research

**Date:** 2026-03-16
**Researcher:** auto

## Summary

S02 delivers 3 skills — `acl-rule-analysis` (R021), `cis-benchmark-audit` (R022), and `nist-compliance-assessment` (R023). All three follow the proven SKILL.md template with `metadata.safety: read-only`, 7 required H2 sections, `references/` with exactly 2 files, and ≤2700 body words. The infrastructure is stable — S01 proved the word budget, the references/ offload strategy, and validate.sh requires zero changes.

The main deliverable risk is the CIS copyright-safe reference approach (D026). The skill must cite CIS control IDs and section categories without reproducing benchmark text — describing audit checks independently. This was identified as M002's #2 key risk and is retired by this slice. The NIST skill is lower risk since NIST SP 800-53 and CSF are public-domain US government publications.

The ACL rule analysis skill introduces no new risk — it reuses the "policy audit" procedure shape from S01 with vendor-agnostic rule pattern analysis instead of vendor-specific policy evaluation. CIS and NIST introduce the "compliance assessment" procedure shape (D028) — mapping device config to framework controls.

## Recommendation

Build in this order: **ACL rule analysis → CIS benchmark → NIST compliance.**

1. **ACL rule analysis first** — it's the simplest of the three (vendor-agnostic patterns, no copyright concern) and directly extends S01's policy audit procedure shape. It proves the multi-vendor inline labeling style works for a security audit skill (same `[Cisco]`/`[JunOS]`/`[EOS]`/`[PAN-OS]`/`[FortiGate]` labeling as M001 network skills).

2. **CIS benchmark second** — this is the slice's key risk. The `references/control-reference.md` file must demonstrate the copyright-safe approach: cite control IDs + section categories, describe what config to check, but never reproduce CIS benchmark text. Building CIS before NIST proves the compliance assessment procedure shape.

3. **NIST compliance third** — builds on the compliance assessment pattern from CIS. NIST CSF and SP 800-53 are public-domain US government publications (no copyright constraint). The skill focuses on Protect (PR) and Detect (DE) functions with concrete network device audit mappings, per the research notes.

After all three skills are built, update the README catalog table by inserting 3 new rows under the existing "Security Skills" bold separator (after the 4 firewall audit rows added by S01).

## Implementation Landscape

### Key Files

**New files to create (9 SKILL.md/reference files + README update):**

- `skills/acl-rule-analysis/SKILL.md` — Vendor-agnostic ACL/rule analysis skill. Uses `[Cisco]`/`[JunOS]`/`[EOS]`/`[PAN-OS]`/`[FortiGate]`/`[CheckPoint]` inline labels for CLI commands. Procedure: collect rulebase → identify shadowed rules → flag overly permissive rules → detect unused rules → recommend consolidation. Uses "policy audit" procedure shape.
- `skills/acl-rule-analysis/references/cli-reference.md` — Multi-vendor CLI commands for retrieving ACLs, rulebases, and hit counts. Covers Cisco IOS/ASA, JunOS, EOS, PAN-OS, FortiOS, Check Point.
- `skills/acl-rule-analysis/references/rule-patterns.md` — Rule analysis pattern definitions: shadowed rules, redundant rules, overly permissive rules, unused rules, rule ordering optimization, conflict detection algorithms.

- `skills/cis-benchmark-audit/SKILL.md` — CIS benchmark compliance assessment. Multi-vendor (Cisco IOS, Palo Alto, Juniper, Check Point — the four platforms CIS publishes benchmarks for). Procedure: identify device platform → select CIS benchmark → audit management plane → audit control plane → audit data plane → generate compliance report. Uses "compliance assessment" procedure shape.
- `skills/cis-benchmark-audit/references/control-reference.md` — **Copyright-safe CIS control reference.** Table mapping CIS section numbers to categories (Management Plane, Control Plane, Data Plane), the config area to check, and the CLI command to audit that control. References control IDs only (e.g., "1.1.1") without reproducing CIS benchmark text. Target 30–40 high-impact controls across Cisco IOS, PAN-OS, JunOS, Check Point.
- `skills/cis-benchmark-audit/references/cli-reference.md` — Read-only CLI commands organized by CIS benchmark category for each covered platform.

- `skills/nist-compliance-assessment/SKILL.md` — NIST CSF and 800-53 mapping for network security posture. Vendor-agnostic. Focuses on Protect (PR) and Detect (DE) functions. Procedure: scope assessment → map access controls (AC) → audit logging (AU) → validate config management (CM) → check identification/auth (IA) → assess communications protection (SC) → verify system integrity (SI). Uses "compliance assessment" procedure shape.
- `skills/nist-compliance-assessment/references/control-reference.md` — NIST 800-53 control families (AC, AU, CM, IA, SC, SI) mapped to network device audit checks with specific CLI commands. CSF function mapping (ID/PR/DE/RS/RC) for each control family.
- `skills/nist-compliance-assessment/references/cli-reference.md` — CLI commands organized by NIST control family for Cisco IOS, JunOS, EOS, PAN-OS.

**Existing file to modify:**

- `README.md` — Add 3 new rows to the catalog table under the "Security Skills" separator (after line 45, after the 4 firewall rows). No new separator row needed — S01 already created the "Security Skills" header.

**Files that do NOT change:**

- `scripts/validate.sh` — no changes needed
- `.github/workflows/validate.yml` — no changes needed
- `CONTRIBUTING.md` — no changes needed
- All 16 existing skills — no modifications

### Existing Patterns to Follow

1. **SKILL.md template** — frontmatter with `name`, `description`, `license: Apache-2.0`, `metadata.safety: read-only`, `metadata.author: network-security-skills-suite`, `metadata.version: "1.0.0"`. Body has 7 required H2 sections: When to Use, Prerequisites, Procedure, Threshold Tables, Decision Trees, Report Template, Troubleshooting.

2. **Multi-vendor inline labeling** — ACL rule analysis and NIST use `[Cisco]`/`[JunOS]`/`[EOS]` labels like `bgp-analysis` (see `skills/bgp-analysis/SKILL.md`). ACL rule analysis also adds `[PAN-OS]`/`[FortiGate]`/`[CheckPoint]` since it covers firewall platforms too. CIS benchmark uses per-vendor sections within steps since CIS publishes separate benchmarks per vendor.

3. **"Threshold Tables" section for severity classification** — S01 firewall skills use this section for "Policy Rule Severity Classification" and "IPS/Inspection Maturity" tables (not threshold metrics). S02 should follow this pattern:
   - ACL rule analysis: "Rule Risk Severity" (any/any = Critical, unused = Low, etc.)
   - CIS benchmark: "Compliance Violation Severity" (scored by CIS control level)
   - NIST compliance: "Control Gap Severity" (by 800-53 impact level)

4. **References file structure** — Tables organized by category. See `skills/palo-alto-firewall-audit/references/cli-reference.md` for the table format: `| Function | CLI Command |` with section headers per audit category and prose notes after tables.

5. **Report Template section** — Fenced code block with markdown template. See any S01 skill for the pattern — structured report with sections for executive summary, findings by category, severity distribution, and recommendations.

6. **Word count verification** — Use `awk 'BEGIN{c=0} /^---$/{c++; if(c==2){found=1; next}} found{print}' skills/SKILLNAME/SKILL.md | wc -w` (K001 — not `sed`).

### Procedure Shape Details

**ACL rule analysis — "policy audit" shape (proven in S01):**
- Step 1: Collect rulebases from target device (multi-vendor CLI)
- Step 2: Identify shadowed rules (rule A precedes rule B, A's match criteria is a superset of B's)
- Step 3: Detect overly permissive rules (any/any source-dest, permit ip any any, broad service objects)
- Step 4: Find unused rules (zero hit count over extended period)
- Step 5: Identify redundant/duplicate rules (overlapping match criteria with same action)
- Step 6: Rule ordering optimization (most-hit rules should be near top for performance)
- Step 7: Generate consolidated rule recommendations

**CIS benchmark — "compliance assessment" shape (new):**
- Step 1: Platform identification and CIS benchmark selection
- Step 2: Management Plane audit (SSH, AAA, NTP, logging, SNMP, banner)
- Step 3: Control Plane audit (routing protocol authentication, CoPP, ICMP controls)
- Step 4: Data Plane audit (ACLs, uRPF, storm control, port security, encryption)
- Step 5: Compliance scoring and gap analysis
- Step 6: Priority-ranked remediation plan

**NIST compliance — "compliance assessment" shape:**
- Step 1: Assessment scope and NIST framework selection (CSF vs 800-53)
- Step 2: Access Control (AC) family assessment
- Step 3: Audit and Accountability (AU) assessment
- Step 4: Configuration Management (CM) assessment
- Step 5: Identification and Authentication (IA) assessment
- Step 6: System and Communications Protection (SC) assessment
- Step 7: System and Information Integrity (SI) assessment

### Build Order

1. **Task 1: `acl-rule-analysis` skill** — Create SKILL.md + 2 reference files. Proves multi-vendor security audit skill with inline labels. Verify: `agentskills validate`, `bash scripts/validate.sh` (17 skills), word count ≤2700.

2. **Task 2: `cis-benchmark-audit` skill** — Create SKILL.md + 2 reference files. **Key risk retirement: copyright-safe CIS reference.** The `references/control-reference.md` must cite control IDs + categories only, describe audit checks independently, and NOT reproduce CIS text. Verify: validate.sh (18 skills), word count ≤2700, control-reference.md contains CIS control IDs without benchmark text.

3. **Task 3: `nist-compliance-assessment` skill** — Create SKILL.md + 2 reference files. Builds on CIS compliance pattern. NIST is public domain — no copyright constraint. Verify: validate.sh (19 skills), word count ≤2700.

4. **Task 4: README catalog update + full slice verification** — Add 3 rows to README catalog table. Run full validation: `bash scripts/validate.sh` (19 skills, 0 errors), verify word counts for all 3 new skills, confirm no M001 regression, verify README has 3 new rows.

### Verification Approach

**Per-task (after each skill):**
```bash
# Validate single skill
agentskills validate skills/<skill-name>

# Convention check — should show increasing skill count and 0 errors
bash scripts/validate.sh

# Word count (K001 — use awk, not sed)
awk 'BEGIN{c=0} /^---$/{c++; if(c==2){found=1; next}} found{print}' skills/<skill-name>/SKILL.md | wc -w

# Reference file count
ls skills/<skill-name>/references/ | wc -l  # must be 2
```

**Slice-level (after all 4 tasks):**
```bash
# Full validation — 19 skills, 0 errors
bash scripts/validate.sh

# All 3 word counts ≤2700
for s in acl-rule-analysis cis-benchmark-audit nist-compliance-assessment; do
  echo "$s: $(awk 'BEGIN{c=0} /^---$/{c++; if(c==2){found=1; next}} found{print}' skills/$s/SKILL.md | wc -w) words"
done

# README has 3 new skill rows
grep -c 'rule-analysis\|benchmark-audit\|compliance-assessment' README.md  # should be 3

# CIS copyright check — control-reference.md has control IDs, no benchmark text
grep -c '\.[0-9]' skills/cis-benchmark-audit/references/control-reference.md  # should have many control IDs

# No M001 regression — first 12 skills still pass
bash scripts/validate.sh 2>&1 | grep -c 'ERROR:'  # must be 0

# Content verification
grep -l 'shadowed' skills/acl-rule-analysis/SKILL.md  # confirms rule analysis depth
grep -l 'CIS' skills/cis-benchmark-audit/SKILL.md     # confirms CIS references
grep -l 'NIST\|800-53\|CSF' skills/nist-compliance-assessment/SKILL.md  # confirms NIST mapping
```

## Constraints

- **CIS copyright (D026):** Reference CIS control IDs and section categories only. Describe audit checks independently. Do not reproduce benchmark remediation text, rationale, or exact configuration commands from CIS benchmark documents.
- **NIST is public domain:** NIST SP 800-53 and CSF are US government publications — no copyright restriction on referencing control text. However, keep references concise to fit word budget.
- **≤2700 word body budget:** S01 proved this is viable. ACL rule analysis (vendor-agnostic, less procedure depth per vendor) and NIST (abstract framework) should fit easily. CIS benchmark is the tightest — multi-vendor coverage across 4 platforms within 2700 words requires heavy offload to `references/control-reference.md`.
- **All 3 skills are safety: read-only (D027).** No remediation commands. Skills describe what to audit, not how to fix.
- **7 required H2 sections.** "Threshold Tables" used for severity classification tables (proven in S01 firewall skills). "Decision Trees" used for remediation priority flowcharts.
- **README catalog rows go under existing "Security Skills" separator** at line 41 of README.md, after the 4 firewall audit rows (lines 42–45). No new separator row needed.

## Common Pitfalls

- **ACL rule analysis duplicating S01 firewall skills** — S01 skills already cover vendor-specific rule analysis (e.g., PAN-OS Step 2 does rule-by-rule analysis). The ACL skill must focus on **vendor-agnostic patterns**: shadowed rule detection algorithms, redundant rule identification, unused rule cleanup, and rule ordering optimization. The vendor-specific "how to retrieve rules" goes in the CLI commands; the "what constitutes a bad rule" is universal.
- **CIS control-reference.md becoming a CIS benchmark reproduction** — The reference file must NOT list CIS remediation steps, rationale text, or exact benchmark configuration commands. It should list: control ID → category → what config area to check → which CLI command to use. The skill procedure independently describes the audit methodology.
- **NIST skill being too abstract** — NIST CSF categories (Identify, Protect, Detect, Respond, Recover) are broad. The skill must map to **specific network device config elements** — not describe the NIST framework in the abstract. Focus on PR (Protect) and DE (Detect) functions with concrete audit checks. AC, AU, CM, IA, SC, SI control families have direct network device relevance.
- **Word budget pressure on CIS benchmark** — CIS publishes benchmarks for 4 network platforms (Cisco IOS, PAN-OS, JunOS, Check Point). Covering all 4 in-line will strain the 2700-word budget. Offload per-vendor control mappings to `references/control-reference.md` and keep the SKILL.md procedure vendor-agnostic (audit methodology) with per-vendor CLI examples only where essential.

## Open Risks

- **CIS control selection depth** — CIS benchmarks contain 60–200+ controls per vendor. The `control-reference.md` must select the ~30–40 most impactful controls per vendor. If the planner/executor includes too many, the reference file becomes unwieldy; too few, and the skill lacks coverage. Group by CIS benchmark section (Management Plane, Control Plane, Data Plane) and select the controls most commonly failed in real audits.
- **NIST 800-53 revision scope** — NIST 800-53 Rev 5 has 20 control families. The skill covers 6 families (AC, AU, CM, IA, SC, SI) — the ones with direct network device relevance. Omitting the other 14 families is intentional but should be explicitly stated in the skill's scope section.
