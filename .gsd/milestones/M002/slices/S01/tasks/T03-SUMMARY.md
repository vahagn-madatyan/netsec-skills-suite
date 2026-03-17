---
id: T03
parent: S01
milestone: M002
provides:
  - Check Point (R80+/R81.x) firewall audit skill with rulebase layer analysis, blade activation audit, SmartConsole management validation
  - Cisco ASA/FTD dual-platform firewall audit skill with ACL/ACP analysis, NAT policy validation, Snort IPS assessment
key_files:
  - skills/checkpoint-firewall-audit/SKILL.md
  - skills/checkpoint-firewall-audit/references/policy-model.md
  - skills/checkpoint-firewall-audit/references/cli-reference.md
  - skills/cisco-firewall-audit/SKILL.md
  - skills/cisco-firewall-audit/references/policy-model.md
  - skills/cisco-firewall-audit/references/cli-reference.md
key_decisions:
  - Check Point body at 2537 words, Cisco at 2694 words — both within 2700 budget, confirming references/ offload strategy works for all 4 vendors
  - Cisco skill uses [ASA]/[FTD] labels for dual-platform coverage following M001 multi-vendor labeling convention
patterns_established:
  - All 4 vendor firewall audit skills now proven to fit within 2700-word budget using references/ offload — pattern is fully validated
  - R80+ rulebase layer model (ordered layers, inline layers, all-must-accept) is a unique Check Point concept not present in other vendors
  - Dual-platform labeling ([ASA]/[FTD]) works well for same-vendor products with divergent architectures
observability_surfaces:
  - "bash scripts/validate.sh" reports 16 skills, 0 errors
  - "awk word-count approach" returns ≤2700 for both new skills
  - "grep vendor-specific terms" confirms vendor specificity (rulebase layer, blade, security-level, Access Control Policy, FTD, Snort)
duration: 25m
verification_result: passed
completed_at: 2026-03-16
blocker_discovered: false
---

# T03: Author Check Point and Cisco ASA/FTD firewall audit skills

**Authored complete Check Point and Cisco ASA/FTD firewall audit skills — 6 files total — completing all 4 vendor-specific firewall skills for S01.**

## What Happened

Created the final two vendor firewall audit skills following the proven pattern from T01 (PAN-OS) and T02 (FortiGate).

**Check Point skill** encodes: R80+/R81.x management architecture (SmartConsole → Management Server → Security Gateway), SIC trust verification, Unified Policy with ordered/inline layers (all-must-accept evaluation), Software Blade activation audit (Firewall, IPS, App Control, URL Filtering, Anti-Bot, AV, Threat Emulation, Content Awareness, HTTPS Inspection), NAT policy review (automatic vs manual), identity awareness assessment (AD integration, access roles), and log/compliance verification. CLI reference covers `fw`, `cpstat`, `cpview`, `clish`, and `mgmt_cli` commands. Policy model documents the R80+ layer architecture, blade activation model, and policy installation process.

**Cisco ASA/FTD skill** encodes dual-platform coverage using **[ASA]**/**[FTD]** labels: ASA security levels (0–100) with interface-bound ACLs and Modular Policy Framework (class-map → policy-map → service-policy), plus FTD Access Control Policy evaluation chain (Prefilter → SSL → Access → Intrusion → File/Malware → Default Action) with Snort IPS integration. NAT audit covers the three-section model (Manual → Auto → After-auto) on both platforms. VPN and remote access audit covers IKEv1/v2, crypto algorithms, AnyConnect. CLI reference has dual-platform commands with [ASA]/[FTD] labels plus FMC REST API endpoints.

Initial Cisco draft was 2987 words — trimmed report template and troubleshooting sections to reach 2694 (under budget).

## Verification

- `bash scripts/validate.sh` → exits 0, "Skills checked: 16", "Result: PASS (0 errors)"
- Word counts: checkpoint-firewall-audit: 2537, cisco-firewall-audit: 2694 — both ≤2700
- `grep -l 'rulebase layer\|blade' skills/checkpoint-firewall-audit/SKILL.md` → match found
- `grep -l 'SmartConsole\|Management Server' skills/checkpoint-firewall-audit/SKILL.md` → match found
- `grep -l 'security-level\|security level' skills/cisco-firewall-audit/SKILL.md` → match found
- `grep -l 'Access Control Policy\|Snort\|FTD' skills/cisco-firewall-audit/SKILL.md` → match found
- All 7 H2 sections present in both skills (confirmed by validate.sh)
- Both skills have `references/` directory with 2 files each

### Slice-level verification (partial — T04 remaining):
- ✅ `bash scripts/validate.sh` exits 0 and reports "Skills checked: 16"
- ✅ All 4 firewall skills within word budget (1941, 2692, 2537, 2694)
- ❌ `grep -c 'firewall-audit' README.md` → returns 0 (T04 will update README)
- ✅ Vendor specificity grep checks pass for all 4 skills
- ✅ `bash scripts/validate.sh 2>&1 | grep -c 'ERROR:'` → returns 0

## Diagnostics

- Inspect Check Point skill: `cat skills/checkpoint-firewall-audit/SKILL.md`
- Inspect Cisco skill: `cat skills/cisco-firewall-audit/SKILL.md`
- Word count: `awk 'BEGIN{c=0} /^---$/{c++; if(c==2){found=1; next}} found{print}' skills/checkpoint-firewall-audit/SKILL.md | wc -w`
- Word count: `awk 'BEGIN{c=0} /^---$/{c++; if(c==2){found=1; next}} found{print}' skills/cisco-firewall-audit/SKILL.md | wc -w`
- Validate: `bash scripts/validate.sh 2>&1 | grep -E 'checkpoint|cisco'`
- References: `ls skills/checkpoint-firewall-audit/references/ skills/cisco-firewall-audit/references/`
- Note: Use `awk` approach for word count on macOS, not `sed` (see T01 summary for rationale)

## Deviations

- Cisco SKILL.md initially came in at 2987 words (287 over budget). Trimmed the report template from expanded multi-line format to condensed single-line format, shortened troubleshooting subsections, and reduced some verbose descriptions. Final: 2694 words.

## Known Issues

None.

## Files Created/Modified

- `skills/checkpoint-firewall-audit/SKILL.md` — Check Point R80+ firewall security policy audit skill (2537 body words)
- `skills/checkpoint-firewall-audit/references/policy-model.md` — R80+ architecture, Unified Policy layers, blade model, NAT types
- `skills/checkpoint-firewall-audit/references/cli-reference.md` — fw, cpstat, cpview, clish, mgmt_cli audit commands
- `skills/cisco-firewall-audit/SKILL.md` — Cisco ASA/FTD dual-platform firewall audit skill (2694 body words)
- `skills/cisco-firewall-audit/references/policy-model.md` — ASA security-level model, MPF, FTD ACP evaluation chain
- `skills/cisco-firewall-audit/references/cli-reference.md` — Dual-platform ASA/FTD commands + FMC REST API
- `.gsd/milestones/M002/slices/S01/tasks/T03-PLAN.md` — Added Observability Impact section (pre-flight fix)
