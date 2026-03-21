---
name: zero-trust-assessment
description: >-
  Zero trust architecture maturity assessment with five-pillar scoring rubric.
  Evaluates identity, device, network, application, and data pillars against
  a five-level maturity model grounded in NIST SP 800-207 ZTA tenets. Produces
  a posture score, gap analysis, and prioritized remediation roadmap.
license: Apache-2.0
metadata:
  safety: read-only
  author: network-security-skills-suite
  version: "1.0.0"
  openclaw: '{"emoji":"📋","safetyTier":"read-only","requires":{"bins":["ssh"],"env":[]},"tags":["zero-trust","nist","segmentation"],"mcpDependencies":[],"egressEndpoints":[]}'
---

# Zero Trust Architecture Maturity Assessment

Architecture-level posture assessment that scores an organization's zero trust
maturity across five pillars: Identity, Device, Network, Application, and Data.
This is not a device-specific configuration audit — it evaluates how well the
overall architecture implements zero trust principles from NIST SP 800-207.

Each pillar is scored from Level 1 (Traditional perimeter-centric) to Level 5
(Adaptive, fully automated). The overall maturity equals the lowest individual
pillar score because zero trust is only as strong as its weakest pillar.

Consult `references/maturity-model.md` for full pillar definitions, scoring
criteria per level, and calculation methodology. Use `references/cli-reference.md`
for platform-specific validation commands organized by ZT control category.

## When to Use

- Initial zero trust posture baseline — establishing where the organization
  stands before beginning a ZT transformation program
- Annual or semi-annual ZT maturity reassessment to measure progress against
  roadmap milestones
- Pre-migration assessment — evaluating ZT readiness before moving workloads
  to cloud, hybrid, or multi-cloud architectures
- Merger/acquisition due diligence — assessing acquired infrastructure against
  organizational ZT maturity targets
- Compliance mapping — demonstrating ZT posture for frameworks that reference
  zero trust (NIST CSF 2.0, DoD ZTRA, CISA ZT Maturity Model)
- Board or executive reporting — translating security posture into a scored
  maturity model with clear improvement trajectory

## Prerequisites

- Read-only access to network infrastructure devices (firewalls, switches,
  routers, NAC appliances) via SSH, console, or management API
- Read-only access to identity infrastructure (IdP, RADIUS/TACACS+ servers,
  MFA platform, certificate authority) for configuration verification
- Network architecture diagrams showing segmentation boundaries, trust zones,
  and traffic flow paths
- Inventory of authentication methods deployed (password-only, MFA, certificate,
  SSO) and coverage percentage across user populations
- Understanding of data classification scheme (if any) and where sensitive data
  resides in the network
- Documented security policies covering access control, encryption requirements,
  and monitoring standards

## Procedure

Follow this six-step maturity assessment flow. Each step scores one or more
pillars against the maturity criteria in Threshold Tables below.

### Step 1: Define Assessment Scope

Establish the boundaries of the assessment before scoring any pillar.

**Identify the assessment perimeter:**
- Enterprise campus, data center, cloud, remote access, or full organization
- Which sites, business units, or network segments are included
- Regulatory or compliance drivers that set minimum maturity targets

**Document current architecture baseline:**
- Number and type of network segments (VLANs, VRFs, security zones)
- Identity infrastructure components (IdP, directory, MFA, NAC)
- Data classification maturity (none, informal, formal with labeling)
- Monitoring and logging coverage (SIEM, flow analysis, endpoint telemetry)

**Set target maturity level:**
Determine the organization's target maturity for each pillar based on risk
appetite, regulatory requirements, and business objectives. Most organizations
target Level 3 (Advanced) as an initial milestone with Level 4 (Optimal) as a
two-to-three-year goal.

### Step 2: Identity Pillar Assessment

Evaluate authentication and authorization maturity across all access points.

**Authentication method inventory:**
Identify what authentication mechanisms are deployed and where. Check
centralized identity provider integration, MFA deployment coverage, and
certificate-based authentication availability.

Key evidence to collect:
- Percentage of users with MFA enabled (privileged vs. all users)
- Authentication method for network device management (local, RADIUS, TACACS+)
- Service account management — are machine identities inventoried with
  credential rotation policies?
- Conditional access policies — does authentication strength vary based on
  risk signals (location, device, behavior)?

**Authorization model:**
Evaluate how access decisions are made. Check for role-based access control,
just-in-time privilege elevation, and separation of duties enforcement.

Score the Identity pillar against the Threshold Tables maturity criteria.
Record evidence for each level criterion that is or is not met.

### Step 3: Device Pillar Assessment

Evaluate device trust and compliance verification maturity.

**Asset inventory completeness:**
Determine whether all devices connecting to the network are inventoried,
classified, and tracked. Check network access control enforcement — are
unknown devices blocked or quarantined?

Key evidence to collect:
- 802.1X or NAC deployment coverage (percentage of access ports enforcing
  device authentication)
- Device posture checks enforced at connection time (patch level, encryption
  status, endpoint protection)
- IoT and unmanaged device handling — profiled, segmented, or unrestricted?
- Device certificate issuance and lifecycle management

**Continuous compliance monitoring:**
Assess whether device posture is checked only at connection time or monitored
continuously. Check for automated quarantine of devices that fall out of
compliance during an active session.

Score the Device pillar against the Threshold Tables maturity criteria.

### Step 4: Network Pillar Assessment

Evaluate segmentation, encryption, and network-layer access control maturity.

**Segmentation analysis:**
Assess the granularity of network segmentation beyond basic VLANs. Check for
micro-segmentation technologies that enforce identity-aware or tag-based
policies between workloads in the same zone.

Key evidence to collect:
- Segmentation technology in use (VLAN-only, ACL-based, group-based policy,
  zone-based, software-defined)
- East-west traffic inspection — is lateral movement between segments
  inspected and controlled?
- Encryption of internal traffic — MACsec for LAN, IPsec for WAN,
  TLS for application transport
- Dynamic segmentation — does the network segment change based on identity
  or posture signals?

**Access control model:**
Evaluate firewall and ACL rule architecture. Check for default-deny posture,
explicit allow rules with logging, and regular rule review cadence. Assess
rule permissiveness — overly broad rules (any-any, /8 source ranges) indicate
low maturity.

Score the Network pillar against the Threshold Tables maturity criteria.

### Step 5: Application and Data Pillar Assessment

Evaluate application-layer controls and data protection maturity together
because they are closely coupled in ZT architectures.

**Application access controls:**
Assess whether applications enforce their own access controls independent of
network location. Check for application-aware proxies, ZTNA brokers, or
service mesh with mutual TLS.

Key evidence to collect:
- Application access method (direct network access, VPN, ZTNA/SDP, reverse proxy)
- API security — authentication and authorization enforcement at API gateway
- Workload segmentation in data center or cloud (container network policies,
  service mesh, security groups)
- Application vulnerability management integration with access decisions

**Data protection controls:**
Assess data classification, encryption enforcement, and access governance.

Key evidence to collect:
- Data classification scheme (does one exist, is it enforced, is it automated?)
- Encryption by classification level — is sensitive data encrypted at rest
  and in transit regardless of network location?
- Data loss prevention coverage — egress inspection, email DLP, endpoint DLP
- Data access logging — are accesses to sensitive data stores logged and
  monitored?

Score both the Application and Data pillars against the Threshold Tables.

### Step 6: Calculate Maturity Score and Report

Compile pillar scores into an overall maturity assessment.

**Calculate overall maturity:**
Use the lowest-pillar method (recommended) — overall maturity equals the
lowest individual pillar score. Optionally calculate the weighted average
for progress tracking (see `references/maturity-model.md` for default
weights).

**Gap analysis:**
For each pillar, identify the specific criteria not met between the current
level and the target level. Classify each gap as a quick win (0–30 days,
configuration change), project (1–6 months, new tooling), or strategic
initiative (6+ months, organizational change).

**Generate remediation roadmap:**
Prioritize the lowest-scoring pillar first. Within each pillar, order
remediation actions by impact — quick wins that raise the pillar score
first, then projects that close remaining gaps. Set re-assessment dates
to measure progress.

## Threshold Tables

### Maturity Level Scoring — Identity Pillar

| Level | Maturity | Criteria |
|-------|----------|----------|
| 1 | Traditional | Password-only authentication; local accounts on devices; no centralized identity provider |
| 2 | Initial | MFA for privileged users; centralized IdP (RADIUS/TACACS+) for infrastructure; basic password policies enforced |
| 3 | Advanced | MFA for all users; certificate-based auth available; automated account lifecycle; conditional access policies active |
| 4 | Optimal | Risk-adaptive MFA; continuous session evaluation; just-in-time privilege elevation; passwordless options deployed |
| 5 | Adaptive | Zero standing privileges; behavioral biometrics; real-time identity risk scoring; fully automated access governance |

### Maturity Level Scoring — Device Pillar

| Level | Maturity | Criteria |
|-------|----------|----------|
| 1 | Traditional | No device inventory; no posture checks; any device connects freely |
| 2 | Initial | Basic asset inventory; 802.1X on some access ports; endpoint protection required but not enforced at network level |
| 3 | Advanced | NAC enforces posture checks at connection; device certificates issued; 802.1X on all wired access ports |
| 4 | Optimal | Continuous posture monitoring; non-compliant devices quarantined automatically; IoT profiled and segmented |
| 5 | Adaptive | Real-time device risk scoring; automated remediation; predictive compliance; hardware attestation |

### Maturity Level Scoring — Network Pillar

| Level | Maturity | Criteria |
|-------|----------|----------|
| 1 | Traditional | Flat network or VLAN-only segmentation; implicit trust for internal traffic; no east-west inspection |
| 2 | Initial | ACL-based segmentation between zones; VRF-lite for management isolation; perimeter IDS/IPS only |
| 3 | Advanced | Micro-segmentation (group-based policy or zone-based); identity-aware firewall rules; encrypted management plane |
| 4 | Optimal | Encrypted east-west traffic; software-defined perimeter; dynamic segmentation based on posture and identity |
| 5 | Adaptive | Fully automated micro-segmentation; real-time policy adaptation; per-flow encryption; closed-loop enforcement |

### Maturity Level Scoring — Application Pillar

| Level | Maturity | Criteria |
|-------|----------|----------|
| 1 | Traditional | No application-layer access control; network access implies application access; no API security |
| 2 | Initial | Basic WAF deployed; application-aware firewall rules for critical apps; initial API gateway |
| 3 | Advanced | All external apps behind ZTNA/application proxy; API auth enforced; workload segmentation in data center |
| 4 | Optimal | Service mesh with mTLS; runtime protection (RASP); automated vulnerability scanning in CI/CD pipeline |
| 5 | Adaptive | Real-time application behavior analytics; automated policy generation from traffic analysis; zero-trust service mesh |

### Maturity Level Scoring — Data Pillar

| Level | Maturity | Criteria |
|-------|----------|----------|
| 1 | Traditional | No data classification; encryption only on external links; no DLP; access based on network location |
| 2 | Initial | Basic classification (public/internal/confidential); encryption at rest for databases; email DLP |
| 3 | Advanced | Automated classification and labeling; DLP across egress points; access logging for sensitive data stores |
| 4 | Optimal | Data access governance with analytics; rights management enforced; encryption enforced by classification level |
| 5 | Adaptive | Real-time data access risk scoring; automated DLP; predictive data movement analysis; full lineage tracking |

### Overall Maturity Posture

| Score | Posture | Guidance |
|-------|---------|----------|
| Level 4–5 | Strong | Maintain continuous improvement; focus on automation and adaptive controls |
| Level 3 | Moderate | Solid foundation; prioritize pillar-specific gaps to reach Level 4 |
| Level 2 | Developing | ZT journey underway; accelerate foundational controls (identity, network) |
| Level 1 | Traditional | Significant transformation needed; begin with identity and network pillars |

## Decision Trees

### ZT Pillar Prioritization

```
Assess all five pillar scores
├── Identity Pillar is lowest?
│   ├── Yes → PRIORITY 1: Identity
│   │   ├── Is MFA deployed for any users?
│   │   │   ├── No → Quick win: deploy MFA for privileged accounts first
│   │   │   └── Yes but partial → Expand MFA to all users
│   │   └── Is there a centralized IdP?
│   │       ├── No → Project: deploy RADIUS/TACACS+ integration
│   │       └── Yes → Advance to conditional access policies
│   └── No → Check next pillar
│
├── Network Pillar is lowest?
│   ├── Yes → PRIORITY 1: Network
│   │   ├── Segmentation beyond VLANs?
│   │   │   ├── No → Project: deploy micro-segmentation technology
│   │   │   └── Yes but limited → Expand to cover critical workloads
│   │   └── East-west encryption?
│   │       ├── No → Project: evaluate MACsec/IPsec for internal traffic
│   │       └── Partial → Extend to remaining segments
│   └── No → Check next pillar
│
├── Device Pillar is lowest?
│   ├── Yes → PRIORITY 1: Device
│   │   ├── 802.1X/NAC deployed?
│   │   │   ├── No → Project: deploy NAC on access layer
│   │   │   └── Yes but partial → Extend to all wired access ports
│   │   └── Posture checks enforced?
│   │       ├── No → Quick win: enable posture policy on existing NAC
│   │       └── At connection only → Advance to continuous monitoring
│   └── No → Check next pillar
│
├── Application or Data Pillar is lowest?
│   └── Yes → Address after Identity/Device/Network foundation is Level 3+
│       ├── Application: start with ZTNA/app proxy for external access
│       └── Data: start with classification scheme and encryption policy
│
└── All pillars at same level?
    └── Advance Identity and Network first (foundational pillars)
```

### Quick Win vs Strategic Investment

```
Identified gap between current and target maturity
├── Can it be closed with a configuration change?
│   ├── Yes → Quick win (0–30 days)
│   │   ├── MFA enablement on existing IdP
│   │   ├── ACL tightening on existing firewalls
│   │   ├── Enable logging/monitoring already licensed
│   │   └── 802.1X on ports with existing NAC infrastructure
│   └── No → Requires new tooling or infrastructure?
│       ├── Yes → Project (1–6 months)
│       │   ├── NAC platform deployment
│       │   ├── Micro-segmentation technology rollout
│       │   ├── ZTNA/SDP implementation
│       │   └── Data classification tooling
│       └── Requires organizational change?
│           └── Strategic initiative (6+ months)
│               ├── Zero standing privileges program
│               ├── Full data governance framework
│               └── Automated closed-loop policy engine
```

## Report Template

```
ZERO TRUST MATURITY ASSESSMENT
======================================
Organization: [name]
Assessment Scope: [campus / data center / full enterprise]
Assessment Date: [timestamp]
Assessed By: [operator/team]
Framework Reference: NIST SP 800-207

PILLAR MATURITY SCORES:
  Identity:    Level [1-5] — [Traditional/Initial/Advanced/Optimal/Adaptive]
  Device:      Level [1-5] — [Traditional/Initial/Advanced/Optimal/Adaptive]
  Network:     Level [1-5] — [Traditional/Initial/Advanced/Optimal/Adaptive]
  Application: Level [1-5] — [Traditional/Initial/Advanced/Optimal/Adaptive]
  Data:        Level [1-5] — [Traditional/Initial/Advanced/Optimal/Adaptive]

OVERALL MATURITY:
  Lowest-Pillar Score: Level [n] — [label]
  Weighted Average:    [n.n]
  Target Maturity:     Level [n] — [label]

PILLAR DETAIL — [Pillar Name]:
  Current Level: [n]
  Target Level:  [n]
  Evidence Summary:
    - [criteria met]
    - [criteria met]
  Gaps to Target:
    - [criteria not met] — Classification: [quick win / project / strategic]
  (Repeat for each pillar)

GAP ANALYSIS SUMMARY:
  Quick Wins (0–30 days):
    - [action] — [pillar] — [expected level improvement]

  Projects (1–6 months):
    - [action] — [pillar] — [expected level improvement]

  Strategic Initiatives (6+ months):
    - [action] — [pillar] — [expected level improvement]

REMEDIATION ROADMAP:
  Phase 1 (0–90 days):  [lowest-scoring pillar quick wins]
  Phase 2 (3–6 months): [foundational pillar projects]
  Phase 3 (6–12 months): [advanced maturity initiatives]

NEXT ASSESSMENT: [date — typically 6 months for active transformation, 12 months for maintenance]
```

## Troubleshooting

### Pillar Scoring Disagreements

When evidence supports arguments for two adjacent maturity levels, score at
the lower level. A pillar earns a level only when all criteria for that level
are fully met. Partial implementation does not count — document the specific
gaps preventing the higher score.

### Scope Boundary Ambiguity

If the assessment scope is unclear (e.g., which cloud environments are
included, whether partner network connections count), resolve scope questions
before beginning pillar assessments. Unclear scope leads to inconsistent
scoring and non-comparable results across assessment cycles.

### Missing Evidence

When technical evidence cannot be collected for a pillar (e.g., no read-only
access to the identity provider, cloud environment not in scope), document
the gap and score based on available evidence only. Flag the pillar as
"partial assessment" in the report and schedule follow-up evidence collection.

### Legacy Infrastructure

Legacy devices that cannot support modern ZT controls (e.g., switches without
802.1X, devices without SNMPv3) should be scored at their actual capability
level, not excluded. Their presence lowers the pillar score, which correctly
reflects the risk. Document compensating controls if legacy devices are
isolated into restricted segments.

### Multi-Site Consistency

When assessing organizations with multiple sites, score each site independently
first, then roll up to an overall score. A headquarters at Level 3 with branch
offices at Level 1 results in an overall Level 1 — the weakest site determines
organizational posture. This prevents overestimating maturity based on flagship
site capabilities alone.
