# Zero Trust Maturity Model Reference

Framework for scoring zero-trust architecture maturity across five pillars.
Based on NIST SP 800-207 zero trust architecture tenets and the CISA Zero
Trust Maturity Model structure.

## NIST SP 800-207 ZTA Tenets

The assessment is grounded in the following zero trust tenets from NIST
SP 800-207:

1. All data sources and computing services are considered resources
2. All communication is secured regardless of network location
3. Access to individual enterprise resources is granted on a per-session basis
4. Access is determined by dynamic policy — including client identity,
   application/service, and requesting asset state
5. The enterprise monitors and measures the integrity and security posture
   of all owned and associated assets
6. All resource authentication and authorization are dynamic and strictly
   enforced before access is allowed
7. The enterprise collects as much information as possible about the current
   state of assets, network infrastructure, and communications and uses it
   to improve its security posture

## Five ZT Pillars

### Identity

Authentication and authorization of all human and machine identities before
granting access. Covers user authentication (MFA, certificate-based, SSO),
service accounts, API keys, and machine-to-machine identity.

**Scope:** AAA infrastructure, identity providers, MFA deployment, privilege
management, service identity, conditional access policies.

### Device

Validation of device health, compliance, and trustworthiness before granting
access. Covers endpoint detection, device certificates, posture assessment,
and asset inventory completeness.

**Scope:** Endpoint management (MDM/UEM), device certificates, posture
assessment agents, asset inventory, compliance checks (OS patch level,
encryption status, AV presence).

### Network

Micro-segmentation, encrypted transport, and dynamic access control at the
network layer. Moves beyond perimeter-based trust to per-flow enforcement.

**Scope:** Micro-segmentation (SGT/TrustSec, VRF-lite, security zones),
encrypted east-west traffic, software-defined perimeter, network access
control (802.1X/NAC), DNS security.

### Application

Application-level access control, workload identity, and runtime protection.
Covers API security, workload segmentation, and application-aware policies.

**Scope:** Application-aware firewalling, API gateway enforcement, workload
identity, container/service mesh security, WAF, application access brokers.

### Data

Data classification, encryption, access control, and loss prevention.
Protects data at rest, in transit, and in use with granular access policies.

**Scope:** Data classification and labeling, encryption (at rest and in
transit), DLP controls, access logging and monitoring, data access governance,
rights management.

## Five Maturity Levels

### Level 1 — Traditional

Perimeter-centric security model. Static network segmentation via VLANs.
Limited identity verification — single-factor authentication, flat network
trust. No continuous monitoring of device or user posture.

**Characteristics:** Firewall-only segmentation, password-only auth,
implicit trust for internal traffic, manual access provisioning, limited
visibility into east-west traffic.

### Level 2 — Initial

Beginning ZT adoption. MFA deployed for privileged access. Some network
segmentation beyond VLANs. Basic device inventory exists but is not enforced
as an access condition.

**Characteristics:** MFA for admin accounts, VLAN + ACL segmentation, partial
asset inventory, centralized logging exists but not correlated, initial
identity provider integration.

### Level 3 — Advanced

ZT principles applied across most pillars. MFA required for all users. Micro-
segmentation deployed in critical zones. Device posture checked before access.
Centralized policy engine makes access decisions.

**Characteristics:** Universal MFA, SGT/TrustSec or zone-based segmentation,
device compliance checks enforced, centralized SIEM with correlation, identity-
aware firewall rules, automated provisioning/deprovisioning.

### Level 4 — Optimal

Comprehensive ZT architecture. Dynamic, risk-based access decisions across
all pillars. Continuous verification — sessions are re-evaluated based on
behavior and posture changes. Data-centric security controls applied.

**Characteristics:** Risk-adaptive authentication, continuous posture
monitoring, encrypted east-west traffic, data classification enforced at
access points, automated incident response, least-privilege verified by
analytics, SDP or ZTNA for remote access.

### Level 5 — Adaptive

Fully automated, self-healing ZT architecture. Real-time policy adaptation
based on threat intelligence and behavioral analytics. All five pillars
operate with continuous verification and automated response.

**Characteristics:** AI/ML-driven anomaly detection triggering policy changes,
automated micro-segmentation updates, real-time data access governance,
predictive posture assessment, zero standing privileges, full telemetry
across all pillars feeding closed-loop policy engine.

## Scoring Criteria Matrix

### Identity Pillar Scoring

| Level | Criteria |
|-------|----------|
| 1 | Password-only authentication; local accounts on devices; no centralized IdP |
| 2 | MFA for privileged users; centralized IdP (RADIUS/TACACS+) for network devices; basic password policies |
| 3 | MFA for all users; certificate-based authentication available; automated account lifecycle; conditional access policies |
| 4 | Risk-adaptive MFA; continuous session evaluation; just-in-time privilege elevation; passwordless options deployed |
| 5 | Zero standing privileges; behavioral biometrics; real-time identity risk scoring; fully automated access governance |

### Device Pillar Scoring

| Level | Criteria |
|-------|----------|
| 1 | No device inventory; no posture checks; any device connects freely to network |
| 2 | Basic asset inventory; 802.1X on some access ports; antivirus required but not enforced at network layer |
| 3 | NAC enforces posture checks (patch level, AV, encryption); device certificates issued; 802.1X on all wired access ports |
| 4 | Continuous posture monitoring; non-compliant devices quarantined automatically; IoT device profiling and segmentation |
| 5 | Real-time device risk scoring; automated remediation; predictive compliance; hardware-rooted identity attestation |

### Network Pillar Scoring

| Level | Criteria |
|-------|----------|
| 1 | Flat network or VLAN-only segmentation; implicit trust for internal traffic; no east-west inspection |
| 2 | ACL-based segmentation between zones; VRF-lite for management traffic isolation; basic IDS/IPS at perimeter |
| 3 | Micro-segmentation (SGT/TrustSec, security zones); identity-aware firewall rules; encrypted management plane |
| 4 | Encrypted east-west traffic (MACsec/IPsec); software-defined perimeter; dynamic segmentation based on posture/identity |
| 5 | Fully automated micro-segmentation; real-time policy adaptation; per-flow encryption; network-wide telemetry with closed-loop enforcement |

### Application Pillar Scoring

| Level | Criteria |
|-------|----------|
| 1 | No application-layer access control; network access implies application access; no API security |
| 2 | Basic WAF; application-aware firewall rules for critical apps; initial API gateway deployment |
| 3 | All external apps behind application proxy/ZTNA; API authentication enforced; workload segmentation in data center |
| 4 | Service mesh with mTLS; runtime application self-protection (RASP); automated vulnerability scanning in CI/CD |
| 5 | Real-time application behavior analytics; automated policy generation; zero-trust service mesh across all workloads |

### Data Pillar Scoring

| Level | Criteria |
|-------|----------|
| 1 | No data classification; encryption only on external links; no DLP; access based on network location |
| 2 | Basic data classification (public/internal/confidential); encryption at rest for databases; initial DLP on email |
| 3 | Automated classification and labeling; DLP across network egress points; access logging for sensitive data stores |
| 4 | Data access governance with analytics; rights management enforced; encryption enforced by classification level |
| 5 | Real-time data access risk scoring; automated data loss prevention; predictive data movement analysis; full lineage tracking |

## Overall Maturity Calculation

### Method: Lowest-Pillar Approach (Recommended)

The overall maturity level equals the **lowest individual pillar score**.
Rationale: zero trust is only as strong as its weakest pillar — a Level 4
network with Level 1 identity provides a false sense of security.

```
Overall Maturity = MIN(Identity, Device, Network, Application, Data)
```

### Method: Weighted Average (Alternative)

When organizations need a more granular score for tracking incremental
progress, use weighted averages. Default weights reflect that identity and
network are foundational:

| Pillar | Default Weight |
|--------|---------------|
| Identity | 25% |
| Device | 20% |
| Network | 25% |
| Application | 15% |
| Data | 15% |

```
Weighted Score = (Identity × 0.25) + (Device × 0.20) + (Network × 0.25) +
                 (Application × 0.15) + (Data × 0.15)
```

Report both the weighted average and the lowest-pillar score. The weighted
average shows progress trajectory; the lowest-pillar score shows true
maturity posture.

## Assessment Methodology

### Phase 1: Evidence Collection

Gather configuration artifacts, policy documents, and operational data for
each pillar. Use platform-specific commands from `cli-reference.md` to verify
technical controls. Document what exists vs. what is claimed.

### Phase 2: Pillar Scoring

Score each pillar independently against the criteria matrix above. Assign
the highest level for which **all** criteria are satisfied. Partial
implementation of a level's criteria does not earn that level — score at
the highest fully-met level.

### Phase 3: Gap Analysis

For each pillar, identify the delta between current level and target level.
Map specific capability gaps to remediation actions. Classify gaps as:
- **Quick wins:** Achievable in 0–30 days with configuration changes
- **Projects:** Require 1–6 months, new tooling, or infrastructure changes
- **Strategic:** Require 6+ months, organizational change, or major investment

### Phase 4: Roadmap Generation

Build a prioritized roadmap that addresses the lowest-scoring pillar first.
Sequence actions so that foundational capabilities (identity, network) are
established before dependent capabilities (application, data). Include
milestones, resource estimates, and re-assessment dates.
