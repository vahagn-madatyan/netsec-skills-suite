---
id: S01
parent: M002
milestone: M002
provides:
  - 4 vendor-specific firewall audit skills (PAN-OS, FortiGate, Check Point, Cisco ASA/FTD)
  - Proven pattern — vendor-specific security audit skills fit within 2700-word budget using references/ offload
  - "Policy audit" procedure shape — systematic rule-by-rule analysis against vendor best practices
  - README catalog with "Security Skills" section header and 4 new rows
requires:
  - slice: M001/S01
    provides: SKILL.md template, scripts/validate.sh, CI pipeline, references/ subdirectory convention
affects:
  - S02 (reuses policy audit procedure shape, vendor CLI reference pattern, proven word budget)
  - S03 (firewall vendor context for incident response and SIEM log correlation skills)
  - S04 (security audit skill pattern reusable by VPN, zero-trust, wireless skills)
key_files:
  - skills/palo-alto-firewall-audit/SKILL.md
  - skills/palo-alto-firewall-audit/references/policy-model.md
  - skills/palo-alto-firewall-audit/references/cli-reference.md
  - skills/fortigate-firewall-audit/SKILL.md
  - skills/fortigate-firewall-audit/references/policy-model.md
  - skills/fortigate-firewall-audit/references/cli-reference.md
  - skills/checkpoint-firewall-audit/SKILL.md
  - skills/checkpoint-firewall-audit/references/policy-model.md
  - skills/checkpoint-firewall-audit/references/cli-reference.md
  - skills/cisco-firewall-audit/SKILL.md
  - skills/cisco-firewall-audit/references/policy-model.md
  - skills/cisco-firewall-audit/references/cli-reference.md
  - README.md
key_decisions:
  - D025 — One skill per vendor (not multi-vendor inline labels) because firewall policy models are fundamentally different across vendors
  - D027 — All M002 skills are read-only; no firewall modification guidance
  - D028 — "Policy audit" is a new procedure shape: systematic rule-by-rule analysis against vendor best practices
  - Cisco dual-platform labeling ([ASA]/[FTD]) works well for same-vendor products with divergent architectures
  - 2700-word budget confirmed viable for all 4 vendors — PAN-OS (most complex) only used 1941 words
patterns_established:
  - Firewall audit skills use "policy audit" procedure shape — zone/VDOM/layer inventory → rule-by-rule analysis → profile coverage → protection assessment
  - Vendor-specific policy evaluation chains go in references/policy-model.md (analogous to routing protocol state-machine.md)
  - CLI/API commands go in references/cli-reference.md in table format organized by audit category
  - README catalog uses bold-text separator rows to group skills by category (e.g., "Security Skills")
  - Dual-platform skills use [ASA]/[FTD] inline labels for platform-specific commands within shared procedure steps
observability_surfaces:
  - "bash scripts/validate.sh" — reports 16 skills, 0 errors
  - "awk 'BEGIN{c=0} /^---$/{c++; if(c==2){found=1; next}} found{print}' skills/SKILL/SKILL.md | wc -w" — body word count per skill
  - "grep -l 'VENDOR_TERM' skills/SKILLNAME/SKILL.md" — confirms vendor specificity
  - "grep -c 'firewall-audit' README.md" — returns 4, confirms catalog completeness
drill_down_paths:
  - .gsd/milestones/M002/slices/S01/tasks/T01-SUMMARY.md
  - .gsd/milestones/M002/slices/S01/tasks/T02-SUMMARY.md
  - .gsd/milestones/M002/slices/S01/tasks/T03-SUMMARY.md
  - .gsd/milestones/M002/slices/S01/tasks/T04-SUMMARY.md
duration: ~75min across 4 tasks
verification_result: passed
completed_at: 2026-03-16
---

# S01: Vendor-Specific Firewall Audit Skills

**Delivered 4 vendor-specific firewall audit skills (PAN-OS, FortiGate, Check Point, Cisco ASA/FTD) with 12 reference files, proving the 2700-word budget and references/ offload strategy for security audit skills. Retired the milestone's key risk.**

## What Happened

Built the four most important enterprise firewall audit skills, each encoding real vendor expertise rather than generic firewall checklists. The key risk for M002 — whether PAN-OS (the most complex vendor policy model) could fit within ~2700 words with overflow to `references/` — was retired in T01 when the PAN-OS skill came in at only 1941 body words.

**T01 — PAN-OS firewall audit** (1941 words): Zone-based architecture, security policy evaluation order (intrazone → interzone → universal), App-ID identification chain (L4 session → App-ID → Content-ID → URL-ID), Security Profile Groups (AV, AS, VP, URL, FB, WF, DP), Zone Protection Profiles, DoS protection, and decryption policy review. Policy model reference documents the complete PAN-OS packet processing pipeline. CLI reference covers 8 audit categories using read-only `show`/`test` commands plus XML API queries.

**T02 — FortiGate firewall audit** (2692 words): VDOM architecture (root/management VDOMs, inter-VDOM links), interface-based policy lookup with policy ID ordering, UTM profile binding audit (antivirus, web-filter, application-control, IPS, email-filter, DLP), FortiGuard service validation, SD-WAN SLA monitoring security implications, and HA session sync review. Initial draft was 2820 words — trimmed to fit budget by compressing Troubleshooting section prose.

**T03 — Check Point firewall audit** (2537 words): R80+/R81.x management architecture (SmartConsole → Management Server → Security Gateway), SIC trust verification, Unified Policy with ordered/inline layers (all-must-accept evaluation model), Software Blade activation audit (Firewall, IPS, App Control, URL Filtering, Anti-Bot, AV, Threat Emulation, Content Awareness, HTTPS Inspection), NAT policy review (automatic vs manual), identity awareness assessment.

**T03 — Cisco ASA/FTD firewall audit** (2694 words): Dual-platform coverage using [ASA]/[FTD] inline labels. ASA side encodes security levels (0–100), interface-bound ACLs, Modular Policy Framework (class-map → policy-map → service-policy). FTD side encodes Access Control Policy evaluation chain (Prefilter → SSL → Access → Intrusion → File/Malware → Default Action) with Snort IPS integration. Initial draft was 2987 words — trimmed by compressing report template and troubleshooting sections.

**T04 — README catalog update**: Added "Security Skills" bold separator row to the catalog table and inserted 4 vendor-specific firewall audit skill rows with descriptions citing vendor-specific capabilities. Ran full 16-skill validation confirming zero regressions on M001 skills.

## Verification

All slice-level verification checks from the plan passed:

- `bash scripts/validate.sh` → exits 0, "Skills checked: 16", "Result: PASS (0 errors)" ✅
- Word counts: PAN-OS 1941, FortiGate 2692, Check Point 2537, Cisco 2694 — all ≤2700 ✅
- `grep -c 'firewall-audit' README.md` → 4 ✅
- `grep 'Security Skills' README.md` → found section header ✅
- `bash scripts/validate.sh 2>&1 | grep -c 'ERROR:'` → 0 ✅
- Vendor specificity confirmed via grep for all 4 skills:
  - PAN-OS: App-ID, Content-ID, zone ✅
  - FortiGate: VDOM, UTM ✅
  - Check Point: rulebase layer, blade ✅
  - Cisco: security-level, Access Control Policy, FTD ✅
- All 12 M001 skills pass validation unchanged (no regression) ✅
- Each skill has `references/` directory with exactly 2 files (policy-model.md, cli-reference.md) ✅
- All 4 skills have `metadata.safety: read-only` in frontmatter ✅

## Requirements Advanced

- R017 — PAN-OS skill delivered with zone-based architecture, App-ID chain, Security Profile Groups, Zone Protection Profiles
- R018 — FortiGate skill delivered with VDOM segmentation, UTM profile binding, SD-WAN SLA, FortiGuard service validation
- R019 — Check Point skill delivered with rulebase layers, blade activation audit, SmartConsole management validation
- R020 — Cisco ASA/FTD skill delivered with dual-platform coverage: ASA security levels/ACL/MPF + FTD ACP/Snort

## Requirements Validated

- R017 — validate.sh passes, vendor-specific grep confirms PAN-OS content, 1941 body words, 2 reference files
- R018 — validate.sh passes, vendor-specific grep confirms FortiOS content, 2692 body words, 2 reference files
- R019 — validate.sh passes, vendor-specific grep confirms Check Point content, 2537 body words, 2 reference files
- R020 — validate.sh passes, vendor-specific grep confirms Cisco ASA/FTD content, 2694 body words, 2 reference files

## New Requirements Surfaced

- none

## Requirements Invalidated or Re-scoped

- none

## Deviations

- macOS BSD `sed` double-strip word count command from the plan (`sed '1,/^---$/d' | sed '1,/^---$/d' | wc -w`) does not work correctly — returns 0 for all skills. Replaced with `awk` approach across all tasks: `awk 'BEGIN{c=0} /^---$/{c++; if(c==2){found=1; next}} found{print}' SKILL.md | wc -w`. Documented as K001 in KNOWLEDGE.md.
- FortiGate initial draft was 2820 words (120 over budget) — compressed Troubleshooting prose to reach 2692.
- Cisco initial draft was 2987 words (287 over budget) — compressed report template and troubleshooting sections to reach 2694.

## Known Limitations

- Word budget is tight for FortiGate (2692/2700) and Cisco (2694/2700). Any future additions to these skills must be offset by equivalent trimming or offloaded to references/.
- Skills encode vendor expertise as static procedural guidance — no runtime validation of actual firewall configs. Agents must have appropriate access to execute the CLI/API commands referenced.
- CIS benchmark integration (mapping firewall configs to CIS controls) is deferred to S02 compliance skills.

## Follow-ups

- S02 can reuse the "policy audit" procedure shape for ACL rule analysis skills, and cross-reference the vendor CLI reference patterns established here.
- S03 incident response and SIEM skills should reference firewall vendor context (policy models, CLI patterns) when discussing firewall log analysis and security event correlation.
- S04 VPN/IPSec, zero-trust, and wireless audit skills can adapt the security audit skill pattern (read-only analysis with structured findings).

## Files Created/Modified

- `skills/palo-alto-firewall-audit/SKILL.md` — PAN-OS firewall security policy audit skill (1941 body words)
- `skills/palo-alto-firewall-audit/references/policy-model.md` — PAN-OS packet processing pipeline, zone model, policy matching, SPG components, Panorama hierarchy
- `skills/palo-alto-firewall-audit/references/cli-reference.md` — Read-only PAN-OS CLI/API commands (8 categories)
- `skills/fortigate-firewall-audit/SKILL.md` — FortiGate/FortiOS firewall audit skill (2692 body words)
- `skills/fortigate-firewall-audit/references/policy-model.md` — FortiOS VDOM architecture and UTM inspection chain
- `skills/fortigate-firewall-audit/references/cli-reference.md` — Read-only FortiOS CLI commands (8 categories)
- `skills/checkpoint-firewall-audit/SKILL.md` — Check Point R80+ firewall audit skill (2537 body words)
- `skills/checkpoint-firewall-audit/references/policy-model.md` — R80+ architecture, Unified Policy layers, blade model
- `skills/checkpoint-firewall-audit/references/cli-reference.md` — fw, cpstat, cpview, clish, mgmt_cli commands
- `skills/cisco-firewall-audit/SKILL.md` — Cisco ASA/FTD dual-platform firewall audit skill (2694 body words)
- `skills/cisco-firewall-audit/references/policy-model.md` — ASA security-level model, MPF, FTD ACP evaluation chain
- `skills/cisco-firewall-audit/references/cli-reference.md` — Dual-platform ASA/FTD commands + FMC REST API
- `README.md` — Added "Security Skills" section header + 4 firewall audit skill rows

## Forward Intelligence

### What the next slice should know
- The "policy audit" procedure shape works: zone/VDOM/layer inventory → rule-by-rule analysis → profile coverage → protection assessment. S02 ACL rule analysis and compliance skills can follow this same flow with different evaluation criteria.
- The references/ offload strategy is proven — even the most complex vendor (PAN-OS) only needed 1941 of 2700 words. Security audit skills have enough room for depth.
- The `awk` word count approach (not `sed`) must be used on macOS. See K001 in KNOWLEDGE.md.
- README catalog table now uses bold-text separator rows for skill categories. S02/S03/S04 should add their skills under the existing "Security Skills" header, not create new section rows.

### What's fragile
- FortiGate (2692 words) and Cisco (2694 words) are within 8 words of the 2700-word budget — any additions require compensating cuts or offload to references/.
- The `validate.sh` script checks for `references/` directory existence and file count but does not validate reference file content or naming. A skill could pass validation with empty or misnamed reference files.

### Authoritative diagnostics
- `bash scripts/validate.sh` — the single source of truth for skill validity. Reports per-skill OK/ERROR with named reasons. "Skills checked: 16" confirms discovery.
- `awk 'BEGIN{c=0} /^---$/{c++; if(c==2){found=1; next}} found{print}' skills/SKILLNAME/SKILL.md | wc -w` — reliable body word count on macOS.

### What assumptions changed
- Original assumption: PAN-OS would be the hardest to fit in 2700 words. Actual: PAN-OS was the easiest (1941 words). FortiGate and Cisco were tighter due to more complex troubleshooting scenarios and dual-platform coverage respectively.
- Original T03 plan allocated Cisco to T04 as a separate task. Actual: T03 combined Check Point + Cisco (both followed the proven pattern), and T04 focused solely on README + validation. This was more efficient.