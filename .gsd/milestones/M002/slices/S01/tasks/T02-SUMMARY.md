---
id: T02
parent: S01
milestone: M002
provides:
  - FortiGate (FortiOS) firewall audit skill with VDOM/UTM model and CLI references
key_files:
  - skills/fortigate-firewall-audit/SKILL.md
  - skills/fortigate-firewall-audit/references/policy-model.md
  - skills/fortigate-firewall-audit/references/cli-reference.md
key_decisions:
  - FortiGate body at 2692 words — within 2700 budget, confirming references/ offload strategy works for second vendor
patterns_established:
  - Interface-based policy matching (FortiOS srcintf/dstintf) vs zone-based matching (PAN-OS) is a key structural difference that shapes how audit procedures are written per vendor
  - UTM profile binding audit (FortiOS) is analogous to Security Profile Group audit (PAN-OS) — same concept, vendor-specific implementation
observability_surfaces:
  - "Validate: bash scripts/validate.sh — includes fortigate-firewall-audit in 14-skill count"
  - "Word count: awk 'BEGIN{c=0} /^---$/{c++; if(c==2){found=1; next}} found{print}' skills/fortigate-firewall-audit/SKILL.md | wc -w"
  - "Vendor specificity: grep -l 'VDOM\\|UTM' skills/fortigate-firewall-audit/SKILL.md"
duration: ~15 minutes
verification_result: passed
completed_at: 2026-03-16
blocker_discovered: false
---

# T02: Author FortiGate firewall audit skill with VDOM/UTM model and CLI references

**Authored complete FortiGate/FortiOS firewall audit skill with VDOM segmentation, UTM profile binding validation, FortiGuard service health, SD-WAN security, and HA posture — 2692 body words, confirming pattern portability from T01.**

## What Happened

Created the FortiGate firewall audit skill as the second vendor in S01, following the structural pattern established by T01's PAN-OS skill. The skill encodes FortiOS-specific expertise:

1. **SKILL.md** — 6-step policy audit procedure covering VDOM architecture inventory, per-VDOM rule-by-rule analysis, UTM profile binding audit, FortiGuard service validation, SD-WAN SLA/rule security, and HA session sync. Includes severity threshold tables (15 findings), UTM coverage maturity table, three decision trees (UTM gap remediation, VDOM consolidation, SD-WAN fail-open risk), per-VDOM report template, and five troubleshooting scenarios.

2. **references/policy-model.md** — Documents FortiOS VDOM architecture (types, inter-VDOM links, resource limits), full packet processing pipeline (VDOM context → DoS → session lookup → policy → NAT → SSL inspection → UTM chain → egress), flow-based vs proxy-based inspection modes, FortiGuard fail-open/fail-close behavior, central NAT vs per-policy NAT, and VIP DNAT ordering.

3. **references/cli-reference.md** — Read-only FortiOS CLI commands in table format across 8 categories (VDOM/System, Firewall Policy, UTM Profiles, FortiGuard Status, SD-WAN, HA, Session/Traffic, Logging). Documents the `get` vs `show` vs `diagnose` command distinction with per-section notes.

Initial body was 2820 words; trimmed Troubleshooting section by compressing verbose paragraphs to meet the 2700-word budget.

## Verification

- `bash scripts/validate.sh` → PASS, 0 errors, 14 skills checked
- Body word count: 2692 (≤2700 budget)
- `grep -l 'VDOM\|UTM'` → returns file (vendor specificity confirmed)
- `grep -l 'FortiGuard\|SD-WAN'` → returns file (vendor specificity confirmed)
- `ls skills/fortigate-firewall-audit/references/` → `cli-reference.md`, `policy-model.md`
- All 7 required H2 sections present
- Frontmatter: `name: fortigate-firewall-audit`, `metadata.safety: read-only`

Slice-level checks (2 of 4 firewall skills complete):
- validate.sh PASS with 14 skills (target: 16 at slice completion)
- palo-alto-firewall-audit: 1941 words ✓
- fortigate-firewall-audit: 2692 words ✓
- checkpoint-firewall-audit: not yet created (T03)
- cisco-firewall-audit: not yet created (T04)

## Diagnostics

- Inspect skill: `cat skills/fortigate-firewall-audit/SKILL.md`
- Word count: `awk 'BEGIN{c=0} /^---$/{c++; if(c==2){found=1; next}} found{print}' skills/fortigate-firewall-audit/SKILL.md | wc -w`
- Validate: `bash scripts/validate.sh 2>&1 | grep fortigate`
- References: `ls skills/fortigate-firewall-audit/references/`

## Deviations

- Initial body was 2820 words (120 over budget). Compressed Troubleshooting section to bring under 2700. No content was removed — only prose density improved.

## Known Issues

None.

## Files Created/Modified

- `skills/fortigate-firewall-audit/SKILL.md` — Complete FortiGate firewall audit skill (2692 body words)
- `skills/fortigate-firewall-audit/references/policy-model.md` — FortiOS VDOM architecture and UTM inspection chain documentation
- `skills/fortigate-firewall-audit/references/cli-reference.md` — Read-only FortiOS CLI commands in tabular format (8 categories)
- `.gsd/milestones/M002/slices/S01/tasks/T02-PLAN.md` — Added Observability Impact section (pre-flight fix)
