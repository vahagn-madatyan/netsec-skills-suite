---
estimated_steps: 8
estimated_files: 6
---

# T03: Author Check Point and Cisco ASA/FTD firewall audit skills

**Slice:** S01 — Vendor-Specific Firewall Audit Skills
**Milestone:** M002

## Description

Create the final two vendor firewall audit skills: Check Point (R80+ rulebase layers, blade activation, SmartConsole management plane) and Cisco ASA/FTD (dual-platform: ASA classic security levels + FTD Access Control Policy with Snort IPS). Both follow the proven pattern from T01–T02.

These are combined in one task because the pattern is now established — the executor has two proven examples to reference. Each skill still gets its own SKILL.md + 2 reference files (6 files total). Covers R019 and R020.

**Reference implementation:** Use T01's PAN-OS and T02's FortiGate skills as structural patterns. Match frontmatter schema, section ordering, depth level, and reference file format.

## Steps

### Check Point skill

1. **Create directory structure:** `mkdir -p skills/checkpoint-firewall-audit/references/`

2. **Author `skills/checkpoint-firewall-audit/SKILL.md`** with:
   - **Frontmatter:** `name: checkpoint-firewall-audit`, description mentioning R80+ rulebase layer analysis, blade activation audit, and SmartConsole management validation, `license: Apache-2.0`, `metadata.safety: read-only`
   - **Opening paragraph:** Policy-audit-driven analysis of Check Point Security Gateway policies. Covers R80.x/R81.x managed via SmartConsole/Management Server.
   - **Procedure** (policy audit shape):
     - Step 1: Management architecture inventory — Management Server, Log Server, Security Gateway mapping; domain separation in Multi-Domain (MDS) deployments; SIC trust status
     - Step 2: Rulebase layer analysis — ordered vs inline layers, rule ordering within each layer, implicit rules (Cleanup, Stealth), disabled rules, rule hit counts for unused rule identification
     - Step 3: Blade activation audit — which blades are enabled per gateway (Firewall, IPS, Application Control, URL Filtering, Anti-Bot, Threat Emulation, Content Awareness, HTTPS Inspection), license entitlement vs activation status
     - Step 4: NAT policy review — automatic NAT (per object) vs manual NAT rules, NAT rule ordering, hide vs static NAT, NAT traversal implications
     - Step 5: Identity awareness and access role assessment — identity sources (AD, RADIUS), access roles in security rules, identity agent deployment coverage
     - Step 6: Log and compliance verification — SmartEvent correlation policy, log server connectivity, log completeness, compliance blade status
   - **Threshold/Decision/Report/Troubleshooting sections** following the pattern from T01–T02
   - Body ≤2700 words

3. **Author Check Point reference files:**
   - `references/policy-model.md`: R80+ architecture (SmartConsole → Management Server → Security Gateway), Unified Policy (ordered layers, inline layers), blade activation model, NAT policy types, policy installation process
   - `references/cli-reference.md`: Read-only commands using `fw`, `cpstat`, `cpview`, `clish`, and `mgmt_cli` (API). Categories: System/SIC, Policy/Rulebase, Blade status, NAT, Sessions, Logs. Table format.

### Cisco ASA/FTD skill

4. **Create directory structure:** `mkdir -p skills/cisco-firewall-audit/references/`

5. **Author `skills/cisco-firewall-audit/SKILL.md`** with:
   - **Frontmatter:** `name: cisco-firewall-audit`, description mentioning dual-platform ASA/FTD coverage with ACL analysis, NAT policy validation, and Firepower IPS assessment, `license: Apache-2.0`, `metadata.safety: read-only`
   - **Opening paragraph:** Policy-audit-driven analysis covering both Cisco ASA (classic) and Firepower Threat Defense (FTD). Uses **[ASA]** and **[FTD]** labels where platforms diverge (following M001's multi-vendor labeling convention for same-vendor dual-platform).
   - **Procedure** (policy audit shape):
     - Step 1: Platform identification and architecture inventory — ASA (security levels, interfaces, contexts) vs FTD (managed by FMC or FDM), HA/failover status, multi-context mode for ASA
     - Step 2: Access policy analysis — **[ASA]** ACL evaluation (interface-bound, top-down, implicit deny), global ACL, EtherType ACLs; **[FTD]** Access Control Policy evaluation order (Prefilter → SSL → Access Rules → Intrusion → File/Malware), rule ordering within ACP
     - Step 3: NAT policy audit — **[ASA]** NAT order of operations (Section 1: manual/twice, Section 2: auto, Section 3: after-auto), NAT rule conflicts; **[FTD]** NAT rule types (manual, auto, twice) in FMC
     - Step 4: Inspection and IPS assessment — **[ASA]** Modular Policy Framework (class-map → policy-map → service-policy), default inspection rules; **[FTD]** Snort IPS policies, network analysis policies, file/malware policies, intrusion rule sets
     - Step 5: VPN and remote access audit — site-to-site tunnel groups, crypto map / IKEv2 profiles, AnyConnect configuration security, certificate validation
     - Step 6: Logging and monitoring — syslog severity levels, SNMP, **[FTD]** eStreamer / Security Analytics, connection event logging completeness
   - Body ≤2700 words

6. **Author Cisco reference files:**
   - `references/policy-model.md`: ASA security-level model (higher-to-lower implicit allow, same-security-traffic), MPF hierarchy, multi-context architecture; FTD ACP evaluation chain (Prefilter → SSL → Access → Intrusion → File/Malware → Default Action), Snort deployment modes (inline/passive), FMC management model
   - `references/cli-reference.md`: Dual-platform commands with **[ASA]** and **[FTD]** labels. ASA: `show access-list`, `show nat`, `show service-policy`, `show conn`, `show failover`. FTD: `system support diagnostic-cli`, `show access-control-config`, FMC REST API endpoints. Table format.

7. **Run `bash scripts/validate.sh`** — verify both new skills pass (expect 14+ skills counting at this point, or 16 if running after T01–T02 are complete)

8. **Word count check** on both skills to confirm ≤2700 body words each.

## Must-Haves

- [ ] `skills/checkpoint-firewall-audit/SKILL.md` exists with valid frontmatter and all 7 H2 sections
- [ ] Check Point SKILL.md body ≤2700 words
- [ ] Check Point `references/policy-model.md` documents R80+ architecture, layers, blades
- [ ] Check Point `references/cli-reference.md` contains `fw`, `cpstat`, `clish` commands
- [ ] `skills/cisco-firewall-audit/SKILL.md` exists with valid frontmatter and all 7 H2 sections
- [ ] Cisco SKILL.md body ≤2700 words and uses **[ASA]** / **[FTD]** labels for platform-specific content
- [ ] Cisco `references/policy-model.md` documents both ASA security-level model AND FTD ACP evaluation chain
- [ ] Cisco `references/cli-reference.md` covers both ASA `show` commands and FTD diagnostics
- [ ] `bash scripts/validate.sh` passes including both new skills

## Verification

- `bash scripts/validate.sh` exits 0 counting both new skills
- Word count ≤2700 for both:
  - `sed '1,/^---$/d' skills/checkpoint-firewall-audit/SKILL.md | sed '1,/^---$/d' | wc -w`
  - `sed '1,/^---$/d' skills/cisco-firewall-audit/SKILL.md | sed '1,/^---$/d' | wc -w`
- `grep -l 'rulebase layer\|blade' skills/checkpoint-firewall-audit/SKILL.md` returns the file
- `grep -l 'SmartConsole\|Management Server' skills/checkpoint-firewall-audit/SKILL.md` returns the file
- `grep -l 'security-level\|security level' skills/cisco-firewall-audit/SKILL.md` returns the file
- `grep -l 'Access Control Policy\|Snort\|FTD' skills/cisco-firewall-audit/SKILL.md` returns the file

## Inputs

- `skills/palo-alto-firewall-audit/SKILL.md` — T01 output, proven pattern
- `skills/fortigate-firewall-audit/SKILL.md` — T02 output, confirmed pattern
- `skills/bgp-analysis/SKILL.md` — M01 reference for template format
- `scripts/validate.sh` — validation script
- Decision D025, D027, D028

## Expected Output

- `skills/checkpoint-firewall-audit/SKILL.md` — complete Check Point firewall audit skill
- `skills/checkpoint-firewall-audit/references/policy-model.md` — R80+ policy architecture
- `skills/checkpoint-firewall-audit/references/cli-reference.md` — Check Point CLI commands
- `skills/cisco-firewall-audit/SKILL.md` — complete Cisco ASA/FTD dual-platform audit skill
- `skills/cisco-firewall-audit/references/policy-model.md` — ASA + FTD policy models
- `skills/cisco-firewall-audit/references/cli-reference.md` — dual-platform CLI commands

## Observability Impact

- **Validation surface:** `bash scripts/validate.sh` gains two new skills in its pass/fail output — `checkpoint-firewall-audit` and `cisco-firewall-audit`. Skill count increases from 14 to 16 (or 12→14 if run before T01/T02).
- **Word budget inspection:** `awk 'BEGIN{c=0} /^---$/{c++; if(c==2){found=1; next}} found{print}' skills/checkpoint-firewall-audit/SKILL.md | wc -w` and same for `cisco-firewall-audit` — must return ≤2700.
- **Vendor specificity signals:** `grep -l 'rulebase layer\|blade' skills/checkpoint-firewall-audit/SKILL.md` and `grep -l 'security-level\|Access Control Policy\|FTD' skills/cisco-firewall-audit/SKILL.md` — confirm vendor-specific content, not generic boilerplate.
- **Failure state:** validate.sh prints `ERROR: <reason>` lines to stderr for each failed check. A missing H2 section or absent references/ directory produces a named error.
