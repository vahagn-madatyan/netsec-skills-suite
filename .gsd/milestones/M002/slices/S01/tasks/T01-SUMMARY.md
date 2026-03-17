---
id: T01
parent: S01
milestone: M002
provides:
  - PAN-OS firewall audit skill (SKILL.md + 2 reference files)
  - Proven pattern: vendor-specific firewall policy audit fits within 2700-word budget with references/ offload
key_files:
  - skills/palo-alto-firewall-audit/SKILL.md
  - skills/palo-alto-firewall-audit/references/policy-model.md
  - skills/palo-alto-firewall-audit/references/cli-reference.md
key_decisions:
  - PAN-OS body at 1941 words — well within 2700 budget, confirming references/ offload strategy works for complex vendors
patterns_established:
  - Firewall audit skills use "policy audit" procedure shape: zone inventory → rule-by-rule analysis → App-ID/profile coverage → zone protection → decryption review
  - Vendor-specific policy evaluation chains go in references/policy-model.md (analogous to BGP state-machine.md)
  - CLI/API commands go in references/cli-reference.md in table format, organized by audit category
observability_surfaces:
  - "bash scripts/validate.sh" discovers and validates the skill (per-check OK/ERROR output)
  - "awk frontmatter strip | wc -w" for body word count verification (1941 words)
  - "grep -l 'App-ID|Content-ID|zone'" confirms vendor specificity
duration: ~25min
verification_result: passed
completed_at: 2026-03-16
blocker_discovered: false
---

# T01: Author PAN-OS firewall audit skill with policy-model and CLI references

**Authored complete PAN-OS firewall security policy audit skill with zone-based architecture, App-ID/Content-ID chain, Security Profile Group validation, and zone protection assessment — 1941 body words, proving the 2700-word budget is achievable for the most complex vendor.**

## What Happened

Created `skills/palo-alto-firewall-audit/` with three files:

1. **SKILL.md** (1941 body words): Full policy-audit-shaped procedure covering 6 steps — zone architecture inventory, security policy rule-by-rule analysis, App-ID coverage assessment, Security Profile Group validation, zone protection profile audit, and decryption policy review. Includes PAN-OS-specific threshold tables (rule severity classification, App-ID adoption maturity), decision trees (overly permissive rule remediation, missing SPG remediation), structured report template, and troubleshooting for real audit obstacles (large rulebases, Panorama hierarchy, DAGs, GlobalProtect zones, content update failures).

2. **references/policy-model.md**: Documents the complete PAN-OS packet processing pipeline from ingress zone through zone protection → session lookup → NAT → security policy → App-ID chain (L4→App-ID→Content-ID→URL-ID) → Security Profiles (AV→AS→VP→URL→FB→WF→DP) → egress. Covers zone types, policy rule matching (top-down first-match, rule types, implicit defaults, app shift re-evaluation), Security Profile Group components, Panorama device group hierarchy, and decryption policy types.

3. **references/cli-reference.md**: Read-only PAN-OS CLI and XML/REST API commands in table format organized by 8 audit categories: zone/interface inventory, security policy, App-ID status, security profiles, zone protection, decryption, session/traffic, system status. Includes XML API query examples for programmatic audit of large environments.

Key risk retired: PAN-OS is the most complex vendor model in S01, and it fits comfortably at 1941 words (759 words under budget). The remaining three vendors (FortiGate, Check Point, Cisco ASA/FTD) will fit easily.

## Verification

- `bash scripts/validate.sh` → PASS, 0 errors, Skills checked: 13 (12 M001 + 1 new)
- Body word count: 1941 (≤2700 ✓) — verified via `awk` frontmatter strip
- `grep -l 'App-ID\|Content-ID'` → returns file ✓
- `grep -l 'zone'` → returns file ✓
- `ls skills/palo-alto-firewall-audit/references/` → `cli-reference.md policy-model.md` ✓
- Frontmatter has `name: palo-alto-firewall-audit`, `metadata.safety: read-only` ✓
- All 7 required H2 sections present ✓
- Procedure encodes PAN-OS-specific content (zone pairs, App-ID identification chain, Security Profile Groups, Zone Protection Profiles, Panorama hierarchy) — not generic firewall advice ✓

### Slice-Level Verification (partial — T01 of 4)
- `bash scripts/validate.sh` → Skills checked: 13 (target: 16 after T04) — partial ✓
- `grep -c 'firewall-audit' README.md` → 0 (target: 4 after T04) — expected
- PAN-OS vendor specificity: `grep -l 'App-ID\|Content-ID\|zone'` → ✓

## Diagnostics

- Inspect skill: `cat skills/palo-alto-firewall-audit/SKILL.md`
- Check word count: `awk 'BEGIN{c=0} /^---$/{c++; if(c==2){found=1; next}} found{print}' skills/palo-alto-firewall-audit/SKILL.md | wc -w`
- Validate: `bash scripts/validate.sh 2>&1 | grep palo-alto`
- Note: The task plan's `sed '1,/^---$/d' | sed '1,/^---$/d'` word count approach returns 0 on macOS BSD sed due to range matching behavior. Use the `awk` approach instead.

## Deviations

- Task plan's verification command `sed '1,/^---$/d' | sed '1,/^---$/d' | wc -w` does not work correctly on macOS BSD sed — it returns 0 for all skills including the reference implementation (bgp-analysis). Used `awk` frontmatter stripping instead, which correctly returns 1941 words. This is a tooling quirk, not a content issue.

## Known Issues

- The `sed` double-strip word count command in the task and slice plans is broken on macOS BSD sed. Future tasks (T02, T03) should use the `awk` approach: `awk 'BEGIN{c=0} /^---$/{c++; if(c==2){found=1; next}} found{print}' SKILL.md | wc -w`

## Files Created/Modified

- `skills/palo-alto-firewall-audit/SKILL.md` — PAN-OS firewall security policy audit skill (1941 body words)
- `skills/palo-alto-firewall-audit/references/policy-model.md` — PAN-OS packet processing pipeline, zone model, policy matching, SPG components, Panorama hierarchy
- `skills/palo-alto-firewall-audit/references/cli-reference.md` — Read-only PAN-OS CLI/API commands in table format (8 categories)
- `.gsd/milestones/M002/slices/S01/S01-PLAN.md` — Added Observability/Diagnostics section, diagnostic verification step; marked T01 done
- `.gsd/milestones/M002/slices/S01/tasks/T01-PLAN.md` — Added Observability Impact section
