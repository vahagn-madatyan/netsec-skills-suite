# Requirements

This file is the explicit capability and coverage contract for the project.

## Active

### R001 — Monorepo scaffold with skills/ convention
- Class: core-capability
- Status: validated
- Description: pnpm workspace monorepo with `skills/<name>/SKILL.md` directory convention, package.json, and .gitignore
- Why it matters: Foundation for all skill distribution — without this, nothing is installable
- Source: user
- Primary owning slice: M001/S01
- Supporting slices: none
- Validation: `npx skills add . --list` discovers skills; `scripts/validate.sh` enforces directory convention
- Notes: Must match skills.sh discovery expectations (recursive SKILL.md scan)

### R002 — SKILL.md template with safety tier metadata
- Class: core-capability
- Status: validated
- Description: Standardized SKILL.md template with safety tier in frontmatter metadata, section structure for procedures/thresholds/decision trees/report templates
- Why it matters: Consistency across 40+ skills, safety classification for every skill
- Source: user
- Primary owning slice: M001/S01
- Supporting slices: none
- Validation: Skeleton skill passes `agentskills validate` and `scripts/validate.sh`; mutation tests confirm invalid safety values and missing sections are caught
- Notes: Safety tiers are advisory metadata tags (safety: read-only | read-write)

### R003 — GitHub Actions validation CI pipeline
- Class: quality-attribute
- Status: validated
- Description: CI that validates all SKILL.md files on push — checks frontmatter schema, name matching, description length, required sections
- Why it matters: Prevents broken skills from being published, ensures consistency at scale
- Source: user
- Primary owning slice: M001/S01
- Supporting slices: none
- Validation: `actionlint` confirms workflow syntax (exit 0); two-layer validation wired as separate named steps. Pending first real GitHub Actions run.
- Notes: Use skills-ref Python library or custom validation script

### R004 — README with npx skills add install instructions
- Class: launchability
- Status: validated
- Description: Professional README with install commands, skill catalog table, usage examples, badges
- Why it matters: First thing users see — must clearly communicate value and installation
- Source: research
- Primary owning slice: M001/S01
- Supporting slices: M001/S02, M001/S03, M001/S04
- Validation: README contains `npx skills add` command, catalog table with Safety Tier column, usage example. Will be updated as skills are added in S02-S04.
- Notes: Update as skills are added

### R005 — CONTRIBUTING guide for skill authors
- Class: operability
- Status: validated
- Description: Guide covering SKILL.md format, safety tier conventions, reference file patterns, validation, PR process
- Why it matters: Enables community contributions, maintains quality standards
- Source: research
- Primary owning slice: M001/S01
- Supporting slices: none
- Validation: CONTRIBUTING contains frontmatter schema (6 keys), all 7 body sections, safety tier convention, two-layer validation instructions, PR checklist
- Notes: none

### R006 — Cisco IOS-XE/NX-OS device health check skill
- Class: core-capability
- Status: validated
- Description: Deep procedural skill for Cisco device triage — CPU/memory/interface/routing thresholds, decision trees, structured report output
- Why it matters: Cisco is the most deployed network vendor — table stakes for the suite
- Source: user
- Primary owning slice: M001/S02
- Supporting slices: none
- Validation: S02: `agentskills validate` exit 0, `scripts/validate.sh` PASS, body 1708 words ≤ 2700, dual-platform IOS-XE/NX-OS coverage confirmed
- Notes: Covers both IOS-XE and NX-OS with platform-specific thresholds

### R007 — Juniper JunOS device health check skill
- Class: core-capability
- Status: validated
- Description: Deep procedural skill for Juniper device triage — RE/PFE health, routing engine failover, alarm analysis
- Why it matters: Second most common enterprise vendor — needed for multi-vendor credibility
- Source: user
- Primary owning slice: M001/S02
- Supporting slices: none
- Validation: S02: `agentskills validate` exit 0, `scripts/validate.sh` PASS, body 2326 words ≤ 2700, RE/PFE separation and alarm-first triage confirmed
- Notes: none

### R008 — Arista EOS device health check skill
- Class: core-capability
- Status: validated
- Description: Deep procedural skill for Arista device triage — MLAG, VXLAN/EVPN health, hardware monitoring
- Why it matters: Dominant in modern data center networks
- Source: user
- Primary owning slice: M001/S02
- Supporting slices: none
- Validation: S02: `agentskills validate` exit 0, `scripts/validate.sh` PASS, body 2643 words ≤ 2700, MLAG/VXLAN/agent health confirmed
- Notes: none

### R009 — BGP analysis skill (multi-vendor)
- Class: core-capability
- Status: active
- Description: Protocol state machine reasoning for BGP — peer state diagnosis, path selection analysis, route filtering validation, convergence assessment
- Why it matters: BGP is the internet's routing protocol — most complex and most needed
- Source: user
- Primary owning slice: M001/S03
- Supporting slices: none
- Validation: unmapped
- Notes: Must cover Cisco, Juniper, Arista CLI variations

### R010 — OSPF analysis skill (multi-vendor)
- Class: core-capability
- Status: active
- Description: OSPF state machine reasoning — adjacency diagnosis (stuck states), area design validation, LSA analysis, SPF convergence
- Why it matters: Most common IGP in enterprise networks
- Source: user
- Primary owning slice: M001/S03
- Supporting slices: none
- Validation: unmapped
- Notes: Cover OSPF states: Down → Init → 2-Way → ExStart → Exchange → Loading → Full

### R011 — EIGRP analysis skill (Cisco)
- Class: core-capability
- Status: active
- Description: EIGRP DUAL state machine reasoning — successor/feasible successor analysis, stuck-in-active diagnosis, K-value validation
- Why it matters: Still widely deployed in Cisco-only environments
- Source: user
- Primary owning slice: M001/S03
- Supporting slices: none
- Validation: unmapped
- Notes: Cisco-only protocol

### R012 — IS-IS analysis skill (multi-vendor)
- Class: core-capability
- Status: active
- Description: IS-IS adjacency and LSPDB analysis — level 1/2 routing, NET address validation, TLV analysis
- Why it matters: Used in large SP and DC networks, increasingly common
- Source: user
- Primary owning slice: M001/S03
- Supporting slices: none
- Validation: unmapped
- Notes: Cover Cisco, Juniper, Arista

### R013 — Network topology discovery skill
- Class: core-capability
- Status: active
- Description: Guide agent through topology discovery using CDP/LLDP, routing tables, ARP/MAC tables to build network maps
- Why it matters: Understanding topology is prerequisite to most network troubleshooting
- Source: user
- Primary owning slice: M001/S04
- Supporting slices: none
- Validation: unmapped
- Notes: Tool-agnostic — agent uses whatever access method is available

### R014 — Config management & drift detection skill
- Class: core-capability
- Status: active
- Description: Procedural skill for config backup, comparison, drift detection, golden config validation
- Why it matters: Config drift is the #1 cause of network outages
- Source: user
- Primary owning slice: M001/S04
- Supporting slices: none
- Validation: unmapped
- Notes: safety: read-write (involves config operations)

### R015 — Interface/link health monitoring skill
- Class: core-capability
- Status: active
- Description: Interface error analysis — CRC, input/output errors, discards, resets, optical power levels, threshold tables
- Why it matters: Physical layer issues are the most common and most misdiagnosed problems
- Source: user
- Primary owning slice: M001/S04
- Supporting slices: none
- Validation: unmapped
- Notes: Includes optical transceiver thresholds

### R016 — Network change pre/post verification skill
- Class: core-capability
- Status: active
- Description: Structured pre-change baseline capture, change execution guidance, post-change verification with diff analysis
- Why it matters: Change management discipline prevents outages — this is the safety net
- Source: research
- Primary owning slice: M001/S04
- Supporting slices: none
- Validation: unmapped
- Notes: safety: read-write

### R017 — Palo Alto PAN-OS firewall audit skill
- Class: core-capability
- Status: active
- Description: PAN-OS security policy audit — rule analysis, zone segmentation, threat prevention profile validation, best practice assessment
- Why it matters: Palo Alto is the #1 enterprise firewall vendor — biggest gap vs NetClaw
- Source: user
- Primary owning slice: M002/S01
- Supporting slices: none
- Validation: unmapped
- Notes: none

### R018 — Fortinet FortiGate firewall audit skill
- Class: core-capability
- Status: active
- Description: FortiGate policy audit — rule optimization, VDOM analysis, UTM profile validation, SD-WAN security assessment
- Why it matters: Second largest firewall market share — enterprise staple
- Source: user
- Primary owning slice: M002/S01
- Supporting slices: none
- Validation: unmapped
- Notes: none

### R019 — Check Point firewall audit skill
- Class: core-capability
- Status: active
- Description: Check Point policy audit — rulebase analysis, blade activation, SmartConsole management validation
- Why it matters: Third major firewall vendor — completes the big three
- Source: user
- Primary owning slice: M002/S01
- Supporting slices: none
- Validation: unmapped
- Notes: none

### R020 — Cisco ASA/FTD firewall audit skill
- Class: core-capability
- Status: active
- Description: ASA/FTD security audit — ACL analysis, NAT policy validation, Firepower IPS assessment
- Why it matters: Still heavily deployed in Cisco shops
- Source: user
- Primary owning slice: M002/S01
- Supporting slices: none
- Validation: unmapped
- Notes: none

### R021 — ACL/firewall rule analysis & optimization skill
- Class: core-capability
- Status: active
- Description: Vendor-agnostic ACL/rule analysis — shadowed rules, overly permissive rules, rule ordering optimization, unused rule detection
- Why it matters: Rule bloat is universal across all firewall vendors
- Source: research
- Primary owning slice: M002/S02
- Supporting slices: none
- Validation: unmapped
- Notes: none

### R022 — CIS benchmark compliance assessment skill
- Class: compliance/security
- Status: active
- Description: CIS benchmark assessment for network devices — maps device config against CIS controls, generates compliance report
- Why it matters: CIS benchmarks are the industry standard for device hardening
- Source: user
- Primary owning slice: M002/S02
- Supporting slices: none
- Validation: unmapped
- Notes: CIS covers Cisco, Palo Alto, Juniper, Check Point

### R023 — NIST framework compliance mapping skill
- Class: compliance/security
- Status: active
- Description: NIST CSF and 800-53 control mapping — maps network/security posture to NIST framework categories
- Why it matters: Required for government and many enterprise compliance programs
- Source: user
- Primary owning slice: M002/S02
- Supporting slices: none
- Validation: unmapped
- Notes: none

### R024 — Vulnerability management & CVE triage skill
- Class: core-capability
- Status: active
- Description: CVE assessment for network devices — version-to-CVE mapping, CVSS scoring, remediation prioritization, patch guidance
- Why it matters: Unpatched network devices are a top attack vector
- Source: user
- Primary owning slice: M002/S03
- Supporting slices: none
- Validation: unmapped
- Notes: References NVD database

### R025 — SIEM log analysis skill (vendor-agnostic)
- Class: core-capability
- Status: active
- Description: SIEM log analysis — syslog parsing, event correlation, alert triage, threat hunting queries
- Why it matters: SIEM is the center of security operations
- Source: user
- Primary owning slice: M002/S03
- Supporting slices: none
- Validation: unmapped
- Notes: Vendor-agnostic (Splunk, ELK, QRadar patterns)

### R026 — Incident response network forensics skill
- Class: core-capability
- Status: active
- Description: Network forensics during incident response — traffic analysis, lateral movement detection, containment procedures, evidence preservation
- Why it matters: Network evidence is critical during security incidents
- Source: research
- Primary owning slice: M002/S03
- Supporting slices: none
- Validation: unmapped
- Notes: none

### R027 — VPN/IPSec tunnel analysis skill
- Class: core-capability
- Status: active
- Description: IPSec/IKE troubleshooting — phase 1/2 negotiation analysis, SA lifetime management, crypto mismatch diagnosis
- Why it matters: VPN issues are frequent, complex, and poorly understood
- Source: research
- Primary owning slice: M002/S04
- Supporting slices: none
- Validation: unmapped
- Notes: Multi-vendor coverage

### R028 — Zero-trust assessment skill
- Class: core-capability
- Status: active
- Description: Zero-trust maturity assessment — identity verification, micro-segmentation validation, least privilege analysis
- Why it matters: Zero-trust is the dominant security architecture direction
- Source: user
- Primary owning slice: M002/S04
- Supporting slices: none
- Validation: unmapped
- Notes: none

### R029 — Wireless security audit skill
- Class: core-capability
- Status: active
- Description: Wireless security assessment — SSID policy audit, 802.1X validation, rogue AP detection guidance, RF security
- Why it matters: Wireless is a common attack surface often overlooked
- Source: research
- Primary owning slice: M002/S04
- Supporting slices: none
- Validation: unmapped
- Notes: none

### R030 — AWS VPC/TGW networking skill
- Class: core-capability
- Status: active
- Description: AWS networking — VPC design analysis, Transit Gateway routing, security group/NACL audit, VPC flow log analysis
- Why it matters: AWS is the dominant cloud platform
- Source: user
- Primary owning slice: M003/S01
- Supporting slices: none
- Validation: unmapped
- Notes: none

### R031 — Azure VNet/NSG networking skill
- Class: core-capability
- Status: active
- Description: Azure networking — VNet peering analysis, NSG rule audit, Azure Firewall policy, ExpressRoute/VPN gateway health
- Why it matters: Azure is #2 cloud and dominant in enterprise
- Source: user
- Primary owning slice: M003/S01
- Supporting slices: none
- Validation: unmapped
- Notes: none

### R032 — GCP VPC/firewall networking skill
- Class: core-capability
- Status: active
- Description: GCP networking — VPC network analysis, firewall rule audit, Cloud NAT, Cloud Interconnect health
- Why it matters: Completes the big three cloud providers
- Source: user
- Primary owning slice: M003/S01
- Supporting slices: none
- Validation: unmapped
- Notes: none

### R033 — Cloud security posture assessment skill
- Class: compliance/security
- Status: active
- Description: Cross-cloud security posture — IAM analysis, encryption audit, public exposure detection, compliance mapping
- Why it matters: Misconfigured cloud is the #1 cause of breaches
- Source: user
- Primary owning slice: M003/S02
- Supporting slices: none
- Validation: unmapped
- Notes: none

### R034 — NetBox/Nautobot SOT integration skill
- Class: core-capability
- Status: active
- Description: Source-of-truth integration — inventory reconciliation, data quality audit, intent vs reality comparison
- Why it matters: SOT is the foundation of network automation maturity
- Source: user
- Primary owning slice: M003/S03
- Supporting slices: none
- Validation: unmapped
- Notes: none

### R035 — IPAM/DNS management skill
- Class: core-capability
- Status: active
- Description: IPAM/DNS operations — subnet utilization analysis, DNS record audit, IP conflict detection
- Why it matters: IP and DNS issues cause cascading failures
- Source: user
- Primary owning slice: M003/S03
- Supporting slices: none
- Validation: unmapped
- Notes: none

### R036 — Grafana/Prometheus monitoring skill
- Class: core-capability
- Status: active
- Description: Monitoring — Grafana dashboard analysis, PromQL query building, alert rule validation, SLA reporting
- Why it matters: Observability is essential for proactive network management
- Source: user
- Primary owning slice: M003/S04
- Supporting slices: none
- Validation: unmapped
- Notes: none

### R037 — Log analysis & correlation skill
- Class: core-capability
- Status: active
- Description: Network log analysis — syslog pattern recognition, event correlation, anomaly detection, timeline reconstruction
- Why it matters: Logs are the primary diagnostic data source
- Source: user
- Primary owning slice: M003/S04
- Supporting slices: none
- Validation: unmapped
- Notes: none

### R038 — Network incident response workflow skill
- Class: core-capability
- Status: active
- Description: Structured incident response — triage, escalation, communication templates, RCA framework, post-mortem guidance
- Why it matters: Structured IR reduces MTTR and prevents panic-driven mistakes
- Source: research
- Primary owning slice: M003/S04
- Supporting slices: none
- Validation: unmapped
- Notes: none

## Deferred

### R039 — MCP server wrappers for tool backends
- Class: integration
- Status: deferred
- Description: Lightweight MCP server wrappers that connect skills to specific tool backends
- Why it matters: Would make skills executable out of the box, but adds maintenance burden
- Source: user (explicitly deferred)
- Primary owning slice: none
- Supporting slices: none
- Validation: unmapped
- Notes: User decided skills-only approach — agent decides how to execute

### R040 — Automated skill generation from vendor docs
- Class: operability
- Status: deferred
- Description: Pipeline to generate SKILL.md drafts from vendor documentation
- Why it matters: Could accelerate skill creation at scale
- Source: research
- Primary owning slice: none
- Supporting slices: none
- Validation: unmapped
- Notes: Interesting but premature — need to establish quality bar first

### R041 — Skill versioning and changelog tracking
- Class: operability
- Status: deferred
- Description: Version metadata in SKILL.md frontmatter with changelog tracking
- Why it matters: Users need to know when skills are updated
- Source: research
- Primary owning slice: none
- Supporting slices: none
- Validation: unmapped
- Notes: Can add metadata.version later without breaking changes

## Out of Scope

### R042 — Agent runtime / orchestration framework
- Class: anti-feature
- Status: out-of-scope
- Description: No agent runtime, no orchestration layer, no OpenClaw/LangChain dependency
- Why it matters: Prevents scope creep — we are a skill library, not an agent framework
- Source: inferred
- Primary owning slice: none
- Supporting slices: none
- Validation: n/a
- Notes: Skills are consumed by existing agent platforms

### R043 — Vendor-specific MCP server implementations
- Class: anti-feature
- Status: out-of-scope
- Description: We do not build or maintain MCP servers for connecting to network devices
- Why it matters: MCP servers are a separate concern — skills describe reasoning, not transport
- Source: user (skills only)
- Primary owning slice: none
- Supporting slices: none
- Validation: n/a
- Notes: Users bring their own tool backends

## Traceability

| ID | Class | Status | Primary owner | Supporting | Proof |
|---|---|---|---|---|---|
| R001 | core-capability | validated | M001/S01 | none | S01: `npx skills add . --list` discovers skills, validate.sh enforces convention |
| R002 | core-capability | validated | M001/S01 | none | S01: passes `agentskills validate` + `scripts/validate.sh`; mutation tests catch violations |
| R003 | quality-attribute | validated | M001/S01 | none | S01: `actionlint` passes; two-layer CI wired. Pending first GHA run. |
| R004 | launchability | validated | M001/S01 | M001/S02-S04 | S01: README has install cmd, catalog table, usage example |
| R005 | operability | validated | M001/S01 | none | S01: CONTRIBUTING has format ref, safety tiers, validation, PR checklist |
| R006 | core-capability | validated | M001/S02 | none | S02: dual-platform Cisco skill, `agentskills validate` + `scripts/validate.sh` PASS |
| R007 | core-capability | validated | M001/S02 | none | S02: JunOS RE/PFE skill, `agentskills validate` + `scripts/validate.sh` PASS |
| R008 | core-capability | validated | M001/S02 | none | S02: EOS agent+DC skill, `agentskills validate` + `scripts/validate.sh` PASS |
| R009 | core-capability | active | M001/S03 | none | unmapped |
| R010 | core-capability | active | M001/S03 | none | unmapped |
| R011 | core-capability | active | M001/S03 | none | unmapped |
| R012 | core-capability | active | M001/S03 | none | unmapped |
| R013 | core-capability | active | M001/S04 | none | unmapped |
| R014 | core-capability | active | M001/S04 | none | unmapped |
| R015 | core-capability | active | M001/S04 | none | unmapped |
| R016 | core-capability | active | M001/S04 | none | unmapped |
| R017 | core-capability | active | M002/S01 | none | unmapped |
| R018 | core-capability | active | M002/S01 | none | unmapped |
| R019 | core-capability | active | M002/S01 | none | unmapped |
| R020 | core-capability | active | M002/S01 | none | unmapped |
| R021 | core-capability | active | M002/S02 | none | unmapped |
| R022 | compliance/security | active | M002/S02 | none | unmapped |
| R023 | compliance/security | active | M002/S02 | none | unmapped |
| R024 | core-capability | active | M002/S03 | none | unmapped |
| R025 | core-capability | active | M002/S03 | none | unmapped |
| R026 | core-capability | active | M002/S03 | none | unmapped |
| R027 | core-capability | active | M002/S04 | none | unmapped |
| R028 | core-capability | active | M002/S04 | none | unmapped |
| R029 | core-capability | active | M002/S04 | none | unmapped |
| R030 | core-capability | active | M003/S01 | none | unmapped |
| R031 | core-capability | active | M003/S01 | none | unmapped |
| R032 | core-capability | active | M003/S01 | none | unmapped |
| R033 | compliance/security | active | M003/S02 | none | unmapped |
| R034 | core-capability | active | M003/S03 | none | unmapped |
| R035 | core-capability | active | M003/S03 | none | unmapped |
| R036 | core-capability | active | M003/S04 | none | unmapped |
| R037 | core-capability | active | M003/S04 | none | unmapped |
| R038 | core-capability | active | M003/S04 | none | unmapped |
| R039 | integration | deferred | none | none | unmapped |
| R040 | operability | deferred | none | none | unmapped |
| R041 | operability | deferred | none | none | unmapped |
| R042 | anti-feature | out-of-scope | none | none | n/a |
| R043 | anti-feature | out-of-scope | none | none | n/a |

## Coverage Summary

- Active requirements: 30
- Mapped to slices: 30
- Validated: 8 (R001–R008)
- Unmapped active requirements: 0
