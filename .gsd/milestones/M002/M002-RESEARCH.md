# M002: Security Skills — Research

**Date:** 2026-03-16
**Researcher:** auto

## Summary

M002 delivers 13 security-focused skills across four slices, building on a mature foundation from M001. The codebase is stable — 12 skills pass validation, the SKILL.md template, CI pipeline, and reference file conventions are proven. M002's primary challenge isn't infrastructure; it's **domain knowledge encoding**. Each firewall vendor has a fundamentally different security policy model, compliance frameworks are copyrighted reference material requiring careful attribution, and security operations skills introduce new procedure shapes (policy audit, compliance assessment, forensic timeline, maturity scoring) beyond M001's threshold-comparison and state-machine patterns.

The key strategic decisions are: (1) firewall skills are **vendor-specific** (one skill per vendor, not multi-vendor inline labels like M001's routing skills), (2) compliance reference files must cite CIS/NIST **control IDs and categories only** without reproducing copyrighted benchmark text, and (3) VPN/IPSec troubleshooting reuses M001's FSM reference pattern for IKE negotiation state machines. The existing validate.sh, CI pipeline, and CONTRIBUTING conventions require zero changes — M002 is purely additive content.

Risk concentrates in S01 (firewall vendor skills) — four skills with four completely different policy models — and S02 (compliance) — proving the CIS copyright-safe reference approach. S03 (security ops) and S04 (additional security) are lower risk with familiar procedure shapes.

## Recommendation

**Order slices by risk: S01 (firewall) → S02 (compliance) → S03 (security ops) → S04 (additional security).** S01 proves the vendor-specific firewall audit pattern and is the most content-intensive slice (4 skills × vendor-specific policy models). S02 proves the compliance reference file approach — the CIS copyright constraint is the single biggest unknown. S03 and S04 build on proven patterns and carry less risk.

Within S01, build the **Palo Alto skill first** — it's the #1 enterprise firewall vendor (R017 says "biggest gap vs NetClaw") and its zone-based security model with security profiles is the most complex policy model to encode. If PAN-OS fits the template and word budget, the other three vendors will too.

Within S02, build the **CIS benchmark skill first** to prove the compliance reference pattern before NIST. CIS is more prescriptive (specific controls per device) while NIST is more abstract (framework categories) — proving the harder case first de-risks the easier one.

All 13 skills are safety: **read-only** (audit/analysis only). No skill in M002 modifies device state. This simplifies the pattern — no ⚠️ WRITE markers needed, no safety notes about write operations.

## Implementation Landscape

### Key Files

- `skills/<skill-name>/SKILL.md` — Each new skill follows the template established by M001. 7 required H2 sections, frontmatter with `metadata.safety: read-only`, ≤2700 word body.
- `skills/<skill-name>/references/cli-reference.md` — Vendor-specific CLI commands for each skill. For single-vendor firewall skills, this is the platform's show/debug commands.
- `skills/<skill-name>/references/<domain-file>.md` — Second reference file, domain-specific. New naming conventions for M002:
  - Firewall skills: `policy-model.md` (vendor-specific policy object hierarchy and evaluation flow)
  - Compliance skills: `control-reference.md` (CIS control IDs or NIST categories with network device mappings)
  - VPN/IPSec: `state-machine.md` (IKE phase 1/2 negotiation FSM — reuses M001 convention)
  - SIEM: `query-reference.md` (vendor-agnostic query patterns for Splunk/ELK/QRadar)
  - Incident response: `forensics-workflow.md` (evidence collection and timeline methodology)
  - Zero-trust: `maturity-model.md` (assessment rubric and scoring framework)
  - Wireless: `security-standards.md` (802.1X state machine, WPA3 requirements, RF security)
- `scripts/validate.sh` — **No changes needed.** Checks safety tier, 7 H2 sections, and references/ directory. All M002 skills conform to the same convention.
- `.github/workflows/validate.yml` — **No changes needed.** Runs `agentskills validate skills/` and `bash scripts/validate.sh` across all skills.
- `README.md` — Update skill catalog table with 13 new rows (total 25). Add a "Security Skills" section header within the catalog.
- `CONTRIBUTING.md` — **No changes needed.** The existing format reference covers M002 skill patterns.

### New Skill Inventory

| # | Skill Name | Slice | Requirement | Vendor Scope | Safety |
|---|-----------|-------|-------------|-------------|--------|
| 1 | `palo-alto-firewall-audit` | S01 | R017 | PAN-OS only | read-only |
| 2 | `fortigate-firewall-audit` | S01 | R018 | FortiOS only | read-only |
| 3 | `checkpoint-firewall-audit` | S01 | R019 | Gaia/R8x only | read-only |
| 4 | `cisco-firewall-audit` | S01 | R020 | ASA + FTD | read-only |
| 5 | `acl-rule-analysis` | S02 | R021 | Multi-vendor | read-only |
| 6 | `cis-benchmark-audit` | S02 | R022 | Multi-vendor | read-only |
| 7 | `nist-compliance-assessment` | S02 | R023 | Vendor-agnostic | read-only |
| 8 | `vulnerability-assessment` | S03 | R024 | Multi-vendor | read-only |
| 9 | `siem-log-analysis` | S03 | R025 | Vendor-agnostic | read-only |
| 10 | `incident-response-network` | S03 | R026 | Multi-vendor | read-only |
| 11 | `vpn-ipsec-troubleshooting` | S04 | R027 | Multi-vendor | read-only |
| 12 | `zero-trust-assessment` | S04 | R028 | Vendor-agnostic | read-only |
| 13 | `wireless-security-audit` | S04 | R029 | Multi-vendor | read-only |

### New Procedure Shapes for M002

M001 established four procedure shapes. M002 introduces four new ones:

| Shape | M001 Precedent | M002 Skills | Key Pattern |
|-------|---------------|-------------|-------------|
| Threshold-comparison | cisco-device-health | — | Compare metric to threshold table |
| Protocol FSM | bgp-analysis | vpn-ipsec-troubleshooting | State machine diagnosis |
| Iterative seed expansion | network-topology-discovery | — | Expand discovery set iteratively |
| Event-driven lifecycle | change-verification | incident-response-network | Before→during→after phases |
| **Policy audit** *(new)* | — | 4 firewall skills, acl-rule-analysis | Systematic rule-by-rule analysis against best practices |
| **Compliance assessment** *(new)* | config-management (Step 6) | cis-benchmark-audit, nist-compliance-assessment | Map device config to framework controls |
| **Forensic timeline** *(new)* | — | siem-log-analysis, incident-response-network | Evidence-driven chronological reconstruction |
| **Maturity scoring** *(new)* | — | zero-trust-assessment, wireless-security-audit | Rubric-based posture assessment with scoring |

### Build Order

**Phase 1 — S01: Vendor-Specific Firewall Audit Skills (4 skills, highest risk)**

Build Palo Alto first — it proves the policy audit procedure shape and the vendor-specific skill pattern for M002. Its zone-based architecture, security profile chain (AV → AS → WF → vulnerability → file blocking → data filtering), and rule shadowing logic are the most complex firewall policy model. If it fits within ~2700 words with overflow to `references/policy-model.md`, the other vendors will too.

Build order within S01: Palo Alto → FortiGate → Check Point → Cisco ASA/FTD.

FortiGate second because it's the next most complex (VDOM, UTM profiles, SD-WAN security). Check Point third (rulebase layers, blade architecture). Cisco ASA/FTD last because it's closest to M001 Cisco patterns and has the most prior art.

**Phase 2 — S02: Rule Analysis & Compliance (3 skills, medium risk)**

ACL rule analysis first — vendor-agnostic, can cross-reference the firewall skills from S01. CIS benchmark second — proves the copyright-safe reference pattern. NIST assessment third — builds on the compliance reference pattern from CIS.

**Phase 3 — S03: Security Operations (3 skills, medium risk)**

Vulnerability assessment first — most structured (CVE lookup → CVSS scoring → prioritization). SIEM log analysis second — vendor-agnostic query patterns. Incident response last — event-driven lifecycle (reuses change-verification pattern).

**Phase 4 — S04: Additional Security (3 skills, lowest risk)**

VPN/IPSec first — reuses FSM pattern from M001. Zero-trust second — maturity assessment is a new pattern but structurally simple. Wireless last — combines audit and assessment patterns.

### Verification Approach

Each slice verified identically to M001:

1. **Per-skill:** `agentskills validate skills/<skill-name>` exit 0
2. **Convention:** `bash scripts/validate.sh` — 0 errors (checks safety tier, 7 H2 sections, references/ directory)
3. **Word count:** `wc -w` on body content ≤ 2700 words per skill
4. **Discovery:** `npx skills add . --list` — discovers all 25 skills (12 M001 + 13 M002)
5. **README:** Catalog table updated with all 13 new rows
6. **No regression:** M001 skills continue to pass validation unchanged

## Constraints

- **CIS benchmark text is copyrighted.** Skills must reference control IDs (e.g., "CIS Cisco IOS 16 Benchmark v1.1.0 — Control 1.1.1") and categories ("Management Plane Hardening") without reproducing the actual benchmark text. The `control-reference.md` file lists control IDs, titles, and which config section to check — not the benchmark's remediation steps or rationale text.
- **≤2700 word body budget** per SKILL.md (proven in M001). Security skills with vendor-specific CLI and multiple decision trees may push this limit. Firewall audit skills must offload the policy object hierarchy and evaluation flow to `references/policy-model.md`.
- **All M002 skills are safety: read-only.** No skill modifies firewall rules, device config, or operational state. Skills analyze/audit existing state only. This is a deliberate constraint from the context document — firewall audit skills are analysis only.
- **scripts/validate.sh checks for exactly the 7 H2 sections** established in M001. M002 skills must include all 7 even when some are a slightly awkward fit (e.g., "Threshold Tables" for a zero-trust assessment). Use the section for scoring rubrics or severity classifications.
- **Each skill requires a `references/` subdirectory with ≥1 file.** M001 established a convention of exactly 2 reference files. M002 should maintain this convention.
- **Single-vendor firewall skills break the multi-vendor labeling pattern.** Firewall skills do NOT use `[Cisco]`/`[JunOS]`/`[EOS]` labels. Instead, each skill is dedicated to one vendor platform. This is intentional — firewall policy models are too different for inline multi-vendor labeling.
- **Cisco ASA/FTD skill covers two platforms** (like M001's Cisco device health covering IOS-XE/NX-OS). Use `[ASA]`/`[FTD]` dual-platform labeling within a single skill, following D015's pattern.

## Common Pitfalls

- **Generic checklists instead of vendor-specific expertise** — The acceptance criteria explicitly state "Firewall audit skills cover vendor-specific policy analysis, not generic checklists." Each firewall skill must encode the vendor's specific policy evaluation order, object hierarchy, and common misconfigurations. A PAN-OS skill that doesn't mention security profile groups, decryption policies, or zone-based segmentation is not deep enough.
- **Reproducing CIS benchmark text** — CIS benchmarks are commercially licensed. Reference control IDs and categories, describe what to check and how, but do not reproduce the benchmark's remediation guidance, rationale, or exact configuration commands from the benchmark. The skill's procedure should independently describe how to audit — referencing CIS controls as the standard, not copying them.
- **SIEM vendor lock-in** — R025 says "Vendor-agnostic (Splunk, ELK, QRadar patterns)." The SIEM skill must present query patterns with vendor-specific syntax examples but the diagnostic reasoning should be platform-independent. Use a labeling convention like `[Splunk]`/`[ELK]`/`[QRadar]` similar to M001's multi-vendor labels.
- **Incident response scope creep** — R026 covers "network forensics during incident response" not general incident response. Keep the skill focused on network evidence (packet captures, flow data, log correlation, lateral movement detection) — not endpoint forensics, malware analysis, or full NIST 800-61 IR lifecycle.
- **"Threshold Tables" section misuse** — Security skills often don't have threshold-based metrics like device health skills do. Use this section for severity classification tables (e.g., firewall rule risk scoring, CVE severity tiers, compliance violation severity). M001 already demonstrated flexibility here — config-management used "Drift Severity by Config Section" and "Unsaved Change Age" tables.
- **VPN/IPSec skill trying to cover SSL VPN** — R027 specifically says "IPSec/IKE troubleshooting." SSL/TLS VPN is a different technology. Keep focused on IKEv1/IKEv2 negotiation, SA management, and crypto parameter mismatch diagnosis.

## Open Risks

- **CIS control ID coverage depth** — CIS publishes benchmarks for Cisco IOS, Palo Alto, Juniper, and Check Point, but control counts vary (60-200+ per benchmark). The skill must select the most impactful controls for the `references/control-reference.md` file, not attempt exhaustive coverage. Propose covering the top 30-40 controls per vendor grouped by category.
- **Firewall vendor CLI access patterns** — PAN-OS uses `show running security-policy` and XML API; FortiGate uses `diagnose` and `get` commands; Check Point uses `fw stat`, SmartConsole CLI, and `cpstat`; ASA uses `show access-list` and `show run`. These are all substantially different from Cisco IOS/JunOS/EOS patterns in M001. Each skill needs its own cli-reference.md from scratch.
- **13 skills is a large batch** — M001 delivered 12 skills across 4 slices, but 1 was a skeleton example. M002 delivers 13 real skills. Consider whether any skill can be deferred or merged if word budget pressures emerge. The most deferrable candidate is R021 (ACL rule analysis) since the vendor-specific firewall skills already cover rule analysis within their vendor context.
- **NIST framework abstraction level** — NIST CSF and 800-53 are abstract frameworks. A skill that maps network device config to NIST controls risks being too vague to be actionable. The skill should focus on the Protect (PR) and Detect (DE) functions with specific network security mappings, not attempt to cover all 5 CSF functions.

## Skills Discovered

No directly relevant professional skills found in the skills.sh ecosystem for M002's domain:

| Technology | Skill | Status |
|------------|-------|--------|
| Firewall audit (PAN-OS, FortiGate) | chaterm/terminal-skills@firewall | Available — generic, not deep enough to be useful |
| Security compliance (CIS/NIST) | davila7/claude-code-templates@security-compliance | Available — application security focused, not network device compliance |
| Incident response / SIEM | groeimetai/snow-flow@security-operations | Available — ServiceNow focused, not network forensics |

None of the discovered skills are relevant enough to install — they target different domains (application security, cloud security, ServiceNow). This confirms the ecosystem gap M002 fills.

## Vendor-Specific Firewall Architecture Notes

### Palo Alto (PAN-OS) — R017

- **Policy model:** Zone-based. Traffic must cross zones to be evaluated. Intrazone traffic has implicit allow (configurable). Security policy rules are processed top-down, first match wins.
- **Key concepts:** Security profiles (antivirus, anti-spyware, vulnerability protection, URL filtering, file blocking, data filtering), security profile groups, decryption policies, App-ID (application identification), User-ID (user-to-IP mapping), zone protection profiles.
- **Common misconfigs:** Overly broad "any/any" rules, security profiles not applied to allow rules, decryption policy gaps leaving encrypted traffic uninspected, App-ID dependency on decryption, interzone default deny not accounting for implied rules.
- **Audit CLI:** `show running security-policy`, `show running nat-policy`, `show running security-profile-group`, `show system info`, `debug dataplane show log-setting`.
- **Reference files:** `cli-reference.md` (PAN-OS show/debug commands), `policy-model.md` (zone-based evaluation flow, security profile chain, rule shadowing detection logic).

### FortiGate (FortiOS) — R018

- **Policy model:** Interface/zone-based with implicit deny. Policies reference source/destination interfaces or zones, addresses, services, and UTM profiles. Processed top-down, first match.
- **Key concepts:** VDOMs (virtual domains for multi-tenancy), UTM profiles (antivirus, web filter, application control, IPS, DNS filter, email filter), SD-WAN security integration, SSL inspection profiles, session helpers, virtual IPs (DNAT).
- **Common misconfigs:** "all/all" policies with no UTM, VDOM misconfiguration leaking traffic between domains, SSL inspection bypasses, SD-WAN health-check security gaps, overly permissive central SNAT rules.
- **Audit CLI:** `get firewall policy`, `diagnose firewall policy list`, `get system status`, `diagnose sys session list`, `get vpn ipsec tunnel summary`.
- **Reference files:** `cli-reference.md` (FortiOS get/diagnose commands), `policy-model.md` (VDOM architecture, UTM profile chain, SD-WAN security integration).

### Check Point (Gaia/R8x) — R019

- **Policy model:** Layer-based rulebase with blade architecture. Security policy organized in layers (ordered and inline). Blades (Firewall, IPS, Application Control, URL Filtering, Anti-Bot, Anti-Virus, Threat Emulation) are independently enabled.
- **Key concepts:** Rulebase layers (ordered vs inline), blade architecture, SmartConsole vs CLI (clish/expert), NAT rules (automatic vs manual), identity awareness (AD integration), HTTPS inspection, threat prevention profiles.
- **Common misconfigs:** Disabled blades with security implications, overly broad rules in ordered layers that shadow inline layer rules, cleanup rule missing at bottom of layer, implied rules conflicting with explicit policy, unoptimized rulebase causing performance issues.
- **Audit CLI:** `fw stat`, `cpstat fw`, `fw tab -s -t connections`, `fwaccel stat`, `show security-policy`, SmartConsole API via `mgmt_cli`.
- **Reference files:** `cli-reference.md` (Gaia/clish/expert commands), `policy-model.md` (layer-based evaluation, blade architecture, implied rules).

### Cisco ASA/FTD — R020

- **Policy model:** Two platforms — legacy ASA (ACL-based, security levels) and modern FTD (Firepower, application-aware). ASA uses ordered ACLs per interface with security level implicit trust. FTD uses Firepower Management Center with access control policies, intrusion policies, and malware/file policies.
- **Key concepts:** ASA security levels, ACL per interface, NAT (auto-NAT vs manual NAT), Firepower IPS (Snort-based), Access Control Policy (ACP) evaluation (prefilter → ACP → default action → intrusion policy), SSL/TLS decryption policies, URL/application filtering.
- **Common misconfigs:** ASA overly permissive same-security-traffic, FTD ACP with broad "allow" rules and no intrusion inspection, NAT rule ordering conflicts, Firepower inline pair vs routed mode confusion, IPS policy set to "balanced" when "maximum detection" needed for sensitive segments.
- **Audit CLI:** ASA — `show access-list`, `show running-config access-list`, `show nat`, `show conn count`. FTD — `show access-control-config`, `show snort statistics`, `system support diagnostic-cli` (drops to ASA CLI).
- **Reference files:** `cli-reference.md` (ASA + FTD commands), `policy-model.md` (ASA security levels vs FTD ACP evaluation, dual-platform `[ASA]`/`[FTD]` labeling).

## Compliance Reference File Strategy

### CIS Benchmark Approach

The `cis-benchmark-audit` skill references CIS Benchmark controls by:
- **Control ID** (e.g., `1.1.1`, `2.3.4`) — unambiguous, versionless reference
- **Section category** (e.g., "Management Plane", "Control Plane", "Data Plane") — structural grouping
- **What to check** — described independently in the skill's procedure (not copied from CIS)
- **Config pattern to grep** — skill describes what CLI output to examine, not the benchmark's remediation

The `references/control-reference.md` file contains a table mapping CIS section numbers to categories, network device config sections, and the CLI commands to audit that control. Target 30-40 high-impact controls per covered vendor (Cisco IOS, Palo Alto, Juniper, Check Point).

### NIST Approach

The `nist-compliance-assessment` skill maps network security posture to NIST CSF core functions and 800-53 control families:
- **CSF functions:** Identify (ID), Protect (PR), Detect (DE) — focus on PR and DE for network devices
- **800-53 families:** AC (Access Control), AU (Audit), CM (Configuration Management), IA (Identification/Authentication), SC (System/Communications Protection), SI (System/Information Integrity)
- **Mapping approach:** For each control family, describe what network device config elements map to that control, not reproducing NIST text

The `references/control-reference.md` file maps NIST control families to network device audit checks with specific CLI commands.

## Requirements Analysis

### Table Stakes (must deliver, well-scoped)

- R017-R020 (firewall vendor skills) — core differentiator, well-defined vendor boundaries
- R021 (ACL rule analysis) — fundamental security hygiene, vendor-agnostic complements vendor-specific S01 skills
- R027 (VPN/IPSec) — common troubleshooting need, reuses proven FSM pattern

### Well-Scoped but Need Careful Framing

- R022 (CIS benchmark) — copyright constraint requires careful reference approach; control ID + category referencing is the right strategy
- R023 (NIST compliance) — abstract framework needs concrete network-specific mappings to be actionable; focus on PR and DE functions
- R025 (SIEM log analysis) — vendor fragmentation managed via multi-vendor labeling; query patterns must be genuinely useful, not generic log-reading advice
- R026 (incident response) — scope is "network forensics," not general IR; keep focused on network evidence

### Lower Risk, Straightforward

- R024 (vulnerability assessment) — CVE/CVSS triage is well-documented; NVD references are public domain
- R028 (zero-trust assessment) — maturity model is a new procedure shape but structurally simple
- R029 (wireless security) — well-defined audit domain (802.1X, WPA3, rogue AP)

### Candidate Requirement Observations

- **No cross-reference requirement between CIS and NIST.** CIS controls often map to NIST 800-53 families. Consider whether the NIST skill should include a CIS cross-reference mapping in its reference file. This would add value for organizations using both frameworks. **Advisory only — not proposing a new requirement.**
- **R021 (ACL rule analysis) overlaps with R017-R020.** Each vendor-specific firewall skill will include rule analysis in its procedure. R021 should focus on vendor-agnostic patterns (shadowed rules, unused rules, overly permissive rules) that apply to any ACL/rulebase — complementing, not duplicating, the vendor skills. **This boundary should be made explicit during planning.**
- **R026 scope boundary with R038 (M003).** R026 is "network forensics during incident response" (M002). R038 is "structured incident response — triage, escalation, communication templates, RCA framework" (M003). These are complementary, not overlapping. R026 focuses on network evidence collection; R038 focuses on the organizational IR process. **The boundary is clean as stated.**

## Sources

- M001 codebase — all patterns, conventions, and decisions directly observed from existing skills, validate.sh, CI pipeline, README, CONTRIBUTING, and M001-SUMMARY.md
- M002-CONTEXT.md — scope definition, requirements mapping, risks, and constraints
- skills.sh ecosystem search — confirmed no existing deep firewall audit, CIS/NIST compliance, or network SIEM/IR skills in the marketplace
- Vendor documentation knowledge — PAN-OS, FortiOS, Check Point Gaia, Cisco ASA/FTD policy models and CLI patterns (domain expertise, not external docs fetched)
