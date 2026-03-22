---
name: wireless-security-audit
description: >-
  Wireless network security audit covering SSID policy, 802.1X/EAP validation,
  WPA3 encryption assessment, rogue AP detection, and RF security posture across
  Cisco WLC, Aruba, and Meraki wireless controllers. Systematic audit from SSID
  inventory through authentication, rogue AP, and RF assessment to final report.
license: Apache-2.0
metadata:
  safety: read-only
  author: network-security-skills-suite
  version: "1.0.0"
  openclaw: '{"emoji":"🛡️","safetyTier":"read-only","requires":{"bins":[],"env":[]},"tags":["wireless","802.1x","wpa3"],"mcpDependencies":["juniper-mist-mcp"],"egressEndpoints":["api.mist.com:443","api.eu.mist.com:443"]}'
---

# Wireless Security Audit

Policy-audit-driven analysis of wireless network security posture across
enterprise wireless controllers. Evaluates SSID configuration policies,
authentication and encryption strength, 802.1X/RADIUS validation, rogue AP
exposure, and RF security — the five domains that determine wireless
network risk.

Uses inline vendor labels for platform-specific commands:
- **[Cisco WLC]** — Cisco AireOS-based wireless LAN controllers
- **[Aruba]** — Aruba Mobility Controllers (AOS)
- **[Meraki]** — Cisco Meraki cloud-managed wireless (API-only, no CLI)

Consult `references/security-standards.md` for 802.1X/EAP state machine,
WPA3 requirements, and rogue AP classification tiers. Consult
`references/cli-reference.md` for read-only commands and API endpoints
organized by audit category.

## When to Use

- Annual wireless security audit as part of infrastructure security review
- Post-deployment validation of new SSID policies or controller upgrades
- Incident response when rogue AP or unauthorized access is suspected
- Compliance assessment requiring wireless security evidence (PCI DSS 4.0 §11.2, HIPAA)
- Pre-migration assessment before WPA2 → WPA3 upgrade across the wireless fleet
- After RF redesign, office relocation, or new building buildout
- Periodic rogue AP sweep to validate WIDS/WIPS detection effectiveness
- Guest network isolation verification following network segmentation changes

## Prerequisites

- Read-only access to wireless controller CLI, management GUI, or API:
  [Cisco WLC] SSH or HTTPS; [Aruba] SSH; [Meraki] Dashboard API key with
  read-only organization scope
- Inventory of expected SSIDs: which SSIDs should exist, their intended
  purpose (corporate, guest, IoT), and required security policy per SSID
- RADIUS server addresses, expected EAP methods, and certificate chain
  documentation for 802.1X-secured SSIDs
- RF design documentation or site survey data (channel plan, AP placement,
  expected coverage boundaries)
- Understanding of VLAN-to-SSID mapping and inter-VLAN firewall rules
- WIDS/WIPS policy documentation: containment enabled or monitoring-only,
  approved neighboring AP list (if maintained)

## Procedure

Follow this audit flow sequentially. Each step builds on findings from the
prior step. The procedure adapts the policy audit shape for wireless:
SSID inventory → authentication/encryption → 802.1X → rogue AP → RF → report.

### Step 1: SSID Policy Inventory

Collect all configured SSIDs and their security posture.

[Cisco WLC] `show wlan summary`
[Aruba] `show wlan ssid-profile`
[Meraki] `GET /networks/{networkId}/wireless/ssids`

For each SSID, record:
- **Name and status** — enabled or disabled (disabled SSIDs still consume
  configuration but may indicate decommissioned services)
- **Security mode** — Open, WPA2-Personal, WPA2-Enterprise, WPA3-Personal,
  WPA3-Enterprise, WPA3-Transition
- **Authentication method** — PSK, 802.1X, MAC-auth, captive portal, open
- **VLAN assignment** — which VLAN clients are placed on post-authentication
- **Broadcast status** — hidden SSIDs provide negligible security benefit
  (SSIDs are disclosed in probe responses and association frames)

Flag immediately:
- Open (no encryption) SSIDs — Critical unless explicitly designated guest
  with captive portal and isolation
- WPA2-Personal (PSK) SSIDs in enterprise environments — PSK shared across
  all clients enables credential sharing and offline dictionary attacks
- SSIDs with no VLAN assignment — clients may land on a default VLAN with
  unintended access

### Step 2: Authentication and Encryption Audit

Evaluate each SSID's encryption and authentication configuration against
the Threshold Tables severity tiers.

[Cisco WLC] `show wlan <id>` — check Security Policies section
[Aruba] `show wlan ssid-profile <name>` — check WPA, Key Management
[Meraki] `GET /networks/{networkId}/wireless/ssids/{number}` — check
`encryptionMode` and `authMode` fields

For enterprise SSIDs, verify:
- **WPA3-Enterprise** preferred; WPA2-Enterprise (AES/CCMP) minimum
- **PMF (Protected Management Frames)** enabled — prevents deauthentication
  attacks that force client disconnection and credential re-entry
- **TKIP disabled** — TKIP has known cryptographic weaknesses; CCMP or
  GCMP-256 only
- **Key management** — SAE for WPA3-Personal; 802.1X with FT (Fast
  Transition / 802.11r) for enterprise roaming

For WPA3-Transition mode SSIDs, document:
- Transition mode is a temporary migration step — it allows WPA2 clients
  that cannot support WPA3. WPA2 clients in transition mode do not benefit
  from SAE or PMF protections
- Set a target date for transition mode removal based on client fleet
  WPA3 adoption rate

### Step 3: 802.1X / RADIUS Validation

Validate the 802.1X authentication chain: supplicant → authenticator → RADIUS.

[Cisco WLC] `show radius summary` — verify server IP, port, status
[Aruba] `show aaa authentication-server all` — check reachability, state
[Meraki] SSID endpoint → `radiusServers` array — verify configured servers

Verify each component:

**RADIUS server reachability:**
- Primary and secondary RADIUS servers configured for redundancy
- RADIUS server state shows active/responding (not timeout/unreachable)
- Shared secret matches between controller and RADIUS server
- Ports correct: UDP 1812 (authentication), UDP 1813 (accounting)

**EAP method validation:**
- EAP-TLS (mutual certificate) for highest security — requires PKI
- PEAP (MSCHAPv2) as acceptable alternative — server certificate required
- LEAP deprecated — flag as Critical if still in use
- Verify server certificate validity: expiration date, trusted CA chain

**Dynamic VLAN assignment:**
- RADIUS should return Tunnel-Private-Group-ID attribute for VLAN placement
- Verify that the returned VLAN exists on the controller and maps to the
  correct network segment
- Test with sample authentications if possible — a valid 802.1X exchange
  that lands a client on the wrong VLAN is a segmentation failure

**RADIUS accounting:**
- Accounting enabled (needed for session tracking and compliance evidence)
- Accounting server reachable and receiving records

### Step 4: Rogue AP Assessment

Evaluate rogue AP detection, classification, and response posture.

[Cisco WLC] `show rogue ap summary`
[Aruba] `show wids-event`
[Meraki] `GET /networks/{networkId}/wireless/airMarshal`

Assess:

**Detection coverage:**
- All managed APs scanning for rogues (on-channel or dedicated monitors)
- Detection covers both 2.4 GHz and 5 GHz bands
- If 6 GHz (Wi-Fi 6E) APs deployed, verify 6 GHz rogue detection capability

**Classification accuracy:**
- Review rogue AP list for misclassifications — neighboring APs classified
  as rogues create alert fatigue; actual rogues classified as neighbors
  create blind spots
- Verify wired-side correlation: controller checks switch MAC tables to
  determine if a rogue AP is connected to the corporate LAN
- Wired-connected rogues are Critical — they bridge the wireless and wired
  networks, bypassing perimeter controls

**Containment policy:**
- Is WIPS containment enabled (active deauthentication of rogue clients)?
- If enabled, containment limited to wired-connected rogues only (to avoid
  interfering with legitimate neighboring APs)
- Legal review of active containment approved for the operating jurisdiction

**Rogue AP metrics:**
- Total rogues detected, classified, and unclassified
- Rogues with clients associated — higher priority than idle rogues
- Rogues on the same channels as managed SSIDs — higher interference risk
- Time from detection to classification — delays increase exposure window

### Step 5: RF Security Posture Review

Assess radio frequency configuration for security implications.

[Cisco WLC] `show 802.11a` / `show 802.11b`
[Aruba] `show ap radio-database`
[Meraki] `GET /networks/{networkId}/wireless/rfProfiles`

Evaluate:

**Channel and power configuration:**
- Non-overlapping channels used (2.4 GHz: 1, 6, 11 only)
- Transmit power appropriate for coverage cell design — over-powered APs
  leak signal beyond physical boundaries
- Auto-channel and auto-power enabled for dynamic adjustment (preferred
  for most deployments)

**Coverage security:**
- APs near building perimeter use directional antennas or reduced power
  to minimize external signal leakage
- No coverage holes where clients could be forced to rogue APs
- Band steering encourages 5/6 GHz — reduces 2.4 GHz range-based exposure

**Channel utilization:**
- High utilization (>80%) indicates congestion — degrades performance and
  may push clients to weaker/rogue APs
- DFS channel events tracked — frequent radar detections cause channel
  changes that disrupt service

**Guest network RF isolation:**
- Guest SSID on same AP hardware as corporate is acceptable if VLAN
  isolation verified (Step 1)
- Guest bandwidth limits configured to prevent WAN saturation
- Client isolation (peer-to-peer blocking) enabled on guest SSIDs

### Step 6: Report

Compile findings into the report template. Prioritize by severity:
Critical findings require immediate remediation, High findings within
30 days, Medium within 90 days. Include specific SSIDs, VLAN IDs, and
controller hostnames in each finding for actionable remediation.

## Threshold Tables

### Encryption Strength Tiers

| Configuration | Tier | Severity if Used | Notes |
|---------------|------|------------------|-------|
| WPA3-Enterprise (192-bit) | Tier 1 | — | CNSA-grade; SAE + GCMP-256 + PMF mandatory |
| WPA3-Enterprise | Tier 1 | — | SAE + CCMP-128/GCMP-256 + PMF mandatory |
| WPA2-Enterprise (AES/CCMP) | Tier 2 | — | Acceptable baseline for enterprise |
| WPA3-Personal (SAE) | Tier 2 | — | Acceptable for non-802.1X SSIDs |
| WPA3-Transition | Tier 3 | Medium | Temporary; WPA2 clients lose PMF/SAE protection |
| WPA2-Personal (AES) | Tier 3 | Medium | PSK shared — offline dictionary attack risk |
| WPA2 (TKIP) | Tier 4 | High | TKIP deprecated; known cryptographic weaknesses |
| WEP | Tier 5 | Critical | Broken — trivially cracked in minutes |
| Open (no encryption) | Tier 5 | Critical | No confidentiality; acceptable only with captive portal + isolation |

### Rogue AP Severity Classification

| Condition | Severity | Response Time |
|-----------|----------|---------------|
| Wired-connected rogue AP (on corporate LAN) | Critical | Immediate — contain and physically locate |
| Evil twin (spoofing managed SSID) | Critical | Immediate — contain; SOC alert; incident response |
| Rogue AP with associated clients | High | 24 hours — classify and contain or approve |
| Unclassified rogue AP (no wired correlation) | Medium | 72 hours — classify as neighboring or rogue |
| Known neighboring AP (from adjacent tenant) | Low | Document; no action unless interference |

### RF Signal Thresholds

| Metric | Good | Acceptable | Poor |
|--------|------|------------|------|
| SNR (voice) | ≥30 dB | 25–30 dB | <25 dB |
| SNR (data) | ≥25 dB | 20–25 dB | <20 dB |
| Channel utilization | <40% | 40–70% | >70% |
| Noise floor | < -90 dBm | -90 to -85 dBm | > -85 dBm |
| Co-channel interference | 0 overlapping APs | 1 overlapping | >1 overlapping |

## Decision Trees

### SSID Security Triage

```
SSID encryption mode?
├── Open (no encryption)
│   ├── Guest SSID with captive portal + VLAN isolation?
│   │   ├── Yes → MEDIUM: Acceptable if isolation verified
│   │   │   └── Verify: VLAN separation, bandwidth limits, client isolation
│   │   └── No → CRITICAL: Unencrypted with network access
│   │       └── Immediate: Enable WPA2-Enterprise minimum or disable SSID
│   └── IoT SSID?
│       └── CRITICAL regardless: IoT must use WPA2-PSK minimum + dedicated VLAN
│
├── WPA2-Personal (PSK)
│   ├── Enterprise environment?
│   │   ├── Yes → HIGH: Migrate to WPA2-Enterprise (802.1X)
│   │   └── No (small office) → MEDIUM: Acceptable with strong PSK + rotation policy
│   └── PSK shared with >20 users?
│       └── HIGH: PSK compromise risk — migrate to 802.1X
│
├── WPA2-Enterprise (AES)
│   ├── PMF enabled?
│   │   ├── No → MEDIUM: Enable PMF (required for deauth attack protection)
│   │   └── Yes → Baseline acceptable; evaluate WPA3 upgrade timeline
│   └── 802.1X auth validated? → Proceed to Step 3
│
├── WPA3-Transition
│   └── Transition timeline defined?
│       ├── Yes → LOW: Monitor WPA2 client percentage; sunset when <5%
│       └── No → MEDIUM: Define sunset date; transition mode is temporary
│
└── WPA3-Enterprise
    └── 192-bit mode?
        ├── Yes → Optimal: CNSA-grade compliance
        └── No → Strong: Standard WPA3-Enterprise is sufficient for most
```

### Authentication Method Upgrade Path

```
Current auth method?
├── Open / MAC auth only
│   └── Upgrade to WPA2-Enterprise + 802.1X (Priority: CRITICAL)
│       └── If no RADIUS infrastructure: Deploy RADIUS first
│
├── WPA2-Personal (PSK)
│   └── Upgrade path depends on scale:
│       ├── <10 devices → WPA3-Personal (SAE) acceptable
│       └── ≥10 devices → WPA2-Enterprise + 802.1X
│           └── Deploy RADIUS, enable 802.1X on SSID, push supplicant config
│
├── WPA2-Enterprise (PEAP/MSCHAPv2)
│   └── Current: Acceptable baseline
│       └── Next upgrade: EAP-TLS (mutual cert) for passwordless auth
│           └── Requires: PKI infrastructure, client cert deployment (MDM/GPO)
│
├── WPA2-Enterprise (EAP-TLS)
│   └── Current: Strong
│       └── Next upgrade: WPA3-Enterprise with PMF
│           └── Verify client fleet WPA3 support before transition
│
└── LEAP
    └── CRITICAL: Deprecated — vulnerable to offline dictionary attacks
        └── Immediate: Replace with PEAP or EAP-TLS
```

## Report Template

```
WIRELESS SECURITY AUDIT REPORT
=================================
Controller: [hostname / org name]
Platform: [Cisco WLC version / Aruba AOS version / Meraki Dashboard]
Sites Audited: [count / names]
Audit Date: [timestamp]
Performed By: [operator/agent]

SSID INVENTORY:
- Total SSIDs configured: [count]
- Enabled SSIDs: [count]
- Encryption breakdown:
  - WPA3-Enterprise: [n]
  - WPA2-Enterprise: [n]
  - WPA2-Personal: [n]
  - Open: [n]
  - Other: [n]

AUTHENTICATION SUMMARY:
- SSIDs using 802.1X: [n] / [total enabled]
- RADIUS servers: [count] — Primary: [IP] Secondary: [IP]
- RADIUS server status: [all reachable / issues]
- EAP method: [EAP-TLS / PEAP / other]
- Certificate expiration: [date]

ROGUE AP SUMMARY:
- Rogues detected: [total]
- Classification: [n] rogue, [n] interfering, [n] neighboring, [n] unclassified
- Wired-connected rogues: [n] — CRITICAL if >0
- Containment status: [enabled/disabled] — rogues contained: [n]

RF POSTURE:
- APs audited: [count]
- Channel utilization average: [%]
- APs with SNR <20 dB: [n]
- Perimeter APs with high external leakage: [n]

GUEST NETWORK:
- Guest SSIDs: [count]
- VLAN isolation verified: [yes/no]
- Bandwidth limits configured: [yes/no]
- Client isolation enabled: [yes/no]
- Captive portal: [yes/no] — HTTPS redirect: [yes/no]

FINDINGS:
1. [Severity] [Category] — [Description]
   SSID: [name]
   Current Config: [encryption/auth/VLAN]
   Issue: [specific problem]
   Recommendation: [specific remediation]

RECOMMENDATIONS:
- [Prioritized action list by severity]

NEXT AUDIT: [CRITICAL findings: 30d, HIGH: 90d, clean: 180d]
```

## Troubleshooting

### Large Multi-Site Deployments

Auditing multi-site wireless environments (>50 APs across multiple
controllers) manually is impractical. For [Cisco WLC], use the XML or
SNMP interface to bulk-export WLAN and rogue AP data. For [Aruba], use
the Aruba Central API or AOS REST API for programmatic data collection.
For [Meraki], the Dashboard API is the only automation method — paginate
large result sets and respect the 10-request-per-second rate limit.
Aggregate per-site findings into a single report with site-level
severity summaries.

### Mixed-Mode Controller Environments

Enterprises running multiple wireless platforms (e.g., Cisco WLC at HQ,
Meraki at branch offices) require separate data collection per platform
but unified reporting. Normalize findings to a common severity scale
using the Threshold Tables in this skill. SSID naming conventions may
differ across platforms even when representing the same logical network.

### WPA3 Client Compatibility

WPA3-Enterprise requires client driver and supplicant support. Before
mandating WPA3-only, survey the client fleet: older Windows 10 builds,
legacy IoT sensors, and some medical devices do not support WPA3 or SAE.
Use WPA3-Transition mode as a bridge, but set a firm sunset date.
Monitor the percentage of WPA2-only clients using controller client
reports — when below 5%, transition to WPA3-only.

### RADIUS Certificate Expiration

RADIUS server certificates expiring during the audit window (or within
90 days) should be flagged as High. An expired RADIUS certificate causes
all 802.1X authentication to fail — total wireless outage for enterprise
SSIDs. Check certificate expiration on both the RADIUS server and any
intermediate CAs in the chain.

### Air Marshal / WIDS False Positives

High false-positive rates in rogue AP detection cause alert fatigue and
reduce the effectiveness of the wireless security program. Maintain an
approved neighboring AP list where possible. Regularly review and
reclassify rogue alerts — a sustained false-positive rate >30% indicates
the classification policy needs tuning.
