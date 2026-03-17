---
estimated_steps: 5
estimated_files: 3
---

# T02: Author FortiGate firewall audit skill with VDOM/UTM model and CLI references

**Slice:** S01 — Vendor-Specific Firewall Audit Skills
**Milestone:** M002

## Description

Create the FortiGate (FortiOS) firewall audit skill — the second vendor skill confirming the pattern established by T01. FortiGate has a fundamentally different architecture from PAN-OS: Virtual Domains (VDOMs) for multi-tenant segmentation, Unified Threat Management (UTM) profile binding, FortiGuard service dependencies, and SD-WAN SLA-based traffic steering.

The skill must encode real FortiOS expertise. Follow the "policy audit" procedure shape (D028).

**Reference implementation:** Use T01's PAN-OS skill (`skills/palo-alto-firewall-audit/SKILL.md`) as the structural pattern — match its frontmatter schema, section ordering, and depth level. Also reference the M001 template at `skills/bgp-analysis/SKILL.md`.

## Steps

1. **Create directory structure:** `mkdir -p skills/fortigate-firewall-audit/references/`

2. **Author `SKILL.md`** with:
   - **Frontmatter:** `name: fortigate-firewall-audit`, description mentioning FortiOS VDOM segmentation, UTM profile validation, and SD-WAN security assessment, `license: Apache-2.0`, `metadata.safety: read-only`
   - **Opening paragraph:** Policy-audit-driven analysis of FortiGate/FortiOS firewall policies. Covers FortiOS 7.x+ on FortiGate appliances and VMs.
   - **When to Use:** Post-change policy review, VDOM segmentation audit, UTM profile coverage assessment, SD-WAN security evaluation, FortiGuard license/connectivity validation, HA cluster security posture check
   - **Prerequisites:** Read-only admin access (or `diagnose` privilege), understanding of VDOM topology, knowledge of expected UTM profile assignments
   - **Procedure** (policy audit shape):
     - Step 1: VDOM architecture inventory — list VDOMs, inter-VDOM links, management VDOM identification, VDOM resource limits
     - Step 2: Firewall policy rule-by-rule analysis — per-VDOM policy table, interface-pair policy lookup, policy ordering (by sequence number), implicit deny, schedule-based rules, disabled policies
     - Step 3: UTM profile binding audit — for each allow policy, verify antivirus, web-filter, application-control, IPS, email-filter, DLP sensor profiles are bound; identify policies with no UTM inspection
     - Step 4: FortiGuard service validation — license status, update connectivity, signature freshness (AV, IPS, web filter, application control databases)
     - Step 5: SD-WAN SLA and rule security — SLA target monitoring, traffic steering rules, health-check status, fail-open behavior, implications of SLA violations on security policy enforcement
     - Step 6: HA and session sync audit — HA mode (active-passive/active-active), session sync configuration, firmware version parity, config sync status
   - **Threshold Tables:** UTM coverage thresholds (allow policies with no UTM profiles = Critical, FortiGuard signatures >7 days old = High, disabled policies in production VDOM = Medium)
   - **Decision Trees:** UTM gap remediation, VDOM consolidation assessment, SD-WAN fail-open risk evaluation
   - **Report Template:** Structured findings per VDOM with severity, policy ID, interfaces, issue, remediation
   - **Troubleshooting:** Large multi-VDOM deployments, shared policy packages in FortiManager, UTM performance impact analysis
   - **Body word count target:** ≤2700 words

3. **Author `references/policy-model.md`:** Document FortiOS policy evaluation:
   - VDOM architecture: root VDOM, per-VDOM routing/policy isolation, inter-VDOM links as virtual interfaces
   - Policy lookup: ingress interface + egress interface → policy table (top-down by sequence number) → first match → UTM inspection chain → action
   - UTM inspection order: flow-based vs proxy-based modes, profile types and what each inspects
   - FortiGuard integration: cloud queries, local cache, fail-open/fail-close behavior
   - Central NAT vs per-policy NAT

4. **Author `references/cli-reference.md`:** Read-only FortiOS CLI commands:
   - Table format organized by audit category
   - Categories: VDOM/System, Firewall policy, UTM profiles, FortiGuard status, SD-WAN, HA, Session/Traffic
   - Commands: `get system status`, `config vdom` / `edit <vdom>`, `show firewall policy`, `diagnose sys session list`, `get webfilter status`, `diagnose firewall proute list`, `get system ha status`, etc.
   - Note `get` (running config summary) vs `show` (full config) vs `diagnose` (runtime state) distinction

5. **Validate:** Run `bash scripts/validate.sh` and verify new skill passes. Check word count ≤2700.

## Must-Haves

- [ ] `skills/fortigate-firewall-audit/SKILL.md` exists with valid frontmatter (`name: fortigate-firewall-audit`, `metadata.safety: read-only`)
- [ ] SKILL.md body contains all 7 required H2 sections
- [ ] SKILL.md body ≤2700 words
- [ ] `references/policy-model.md` documents FortiOS VDOM architecture and UTM inspection chain
- [ ] `references/cli-reference.md` contains read-only FortiOS commands in table format
- [ ] Procedure encodes FortiOS-specific audit (VDOMs, UTM profiles, FortiGuard, SD-WAN) — not generic firewall advice
- [ ] `bash scripts/validate.sh` passes including this skill

## Verification

- `bash scripts/validate.sh` exits 0 and counts this skill
- `sed '1,/^---$/d' skills/fortigate-firewall-audit/SKILL.md | sed '1,/^---$/d' | wc -w` ≤ 2700
- `grep -l 'VDOM\|UTM' skills/fortigate-firewall-audit/SKILL.md` returns the file
- `grep -l 'FortiGuard\|SD-WAN' skills/fortigate-firewall-audit/SKILL.md` returns the file
- `ls skills/fortigate-firewall-audit/references/` shows `policy-model.md` and `cli-reference.md`

## Inputs

- `skills/palo-alto-firewall-audit/SKILL.md` — T01 output, proven pattern to follow for structure and depth
- `skills/bgp-analysis/SKILL.md` — M001 reference implementation for template format
- `scripts/validate.sh` — validation script that must pass
- Decision D025, D027, D028 — one skill per vendor, read-only, policy audit shape

## Expected Output

- `skills/fortigate-firewall-audit/SKILL.md` — complete FortiGate firewall audit skill with FortiOS-specific content
- `skills/fortigate-firewall-audit/references/policy-model.md` — FortiOS VDOM/UTM policy evaluation documentation
- `skills/fortigate-firewall-audit/references/cli-reference.md` — read-only FortiOS CLI commands in tabular format
