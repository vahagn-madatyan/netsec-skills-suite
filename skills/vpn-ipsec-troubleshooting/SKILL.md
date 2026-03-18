---
name: vpn-ipsec-troubleshooting
description: >-
  IPSec/IKE VPN troubleshooting with IKE state machine diagnosis, crypto
  parameter verification, and tunnel health assessment. Multi-vendor coverage
  for Cisco IOS-XE, Juniper JunOS, Palo Alto PAN-OS, and FortiGate FortiOS
  with FSM-driven diagnostic reasoning.
license: Apache-2.0
metadata:
  safety: read-only
  author: network-security-skills-suite
  version: "1.0.0"
---

# IPSec/IKE VPN Troubleshooting

State-machine-driven troubleshooting skill for IPSec VPN tunnels using IKE
negotiation diagnosis. IKE is a protocol state machine — IKEv1 Main Mode
progresses through defined states (MM_NO_STATE → MM_SA_SETUP → MM_KEY_EXCH →
MM_KEY_AUTH → QM_IDLE), and IKEv2 uses SA_INIT/SA_AUTH exchanges. Reading the
current SA state and mapping it to the negotiation phase isolates the failure
domain without guesswork.

Commands are labeled **[Cisco]**, **[JunOS]**, **[PAN-OS]**, or **[FortiGate]**
where syntax diverges. Unlabeled statements apply to all four vendors. Reference
`references/state-machine.md` for full IKE FSM detail and
`references/cli-reference.md` for complete command tables.

## When to Use

- VPN tunnel reported down or not passing traffic
- IKE SA stuck in a non-established state (MM_NO_STATE, AG_INIT_EXCH, SA_INIT_SENT)
- Phase 1 establishes but Phase 2 / Child SA fails to negotiate
- Tunnel is established but traffic is not flowing (encap/decap counters not incrementing)
- After configuration changes to crypto proposals, peer addresses, or PSK/certificates
- Intermittent tunnel flapping or unexpected SA rekey failures
- NAT-related VPN issues (NAT-T not activating, keepalive failures)
- Dead Peer Detection declaring a peer dead prematurely
- Crypto mismatch diagnosis after multi-vendor interop changes

## Prerequisites

- SSH or console access to the VPN gateway (read-only privilege sufficient)
- At least one IPSec VPN tunnel configured on the device
- Knowledge of expected tunnel topology: peer IP addresses, protected networks (proxy IDs / traffic selectors), and intended crypto parameters
- Awareness of configured IKE version (IKEv1 vs IKEv2) per tunnel
- For route-based VPN: knowledge of tunnel interface assignments and routing
- For policy-based VPN: knowledge of crypto map or security policy bindings

## Procedure

Follow this diagnostic flow sequentially. Each step builds on data from prior
steps. The procedure moves from SA state inventory through targeted failure
diagnosis to tunnel health verification.

### Step 1: Check IKE SA State

Collect all IKE SAs and compare against expected tunnel topology.

**[Cisco]**
```
show crypto isakmp sa
show crypto ikev2 sa
```

**[JunOS]**
```
show security ike security-associations
```

**[PAN-OS]**
```
show vpn ike-sa
```

**[FortiGate]**
```
diagnose vpn ike gateway list
```

Record each SA: peer address, IKE version, state, role (initiator/responder),
lifetime remaining. Compare against expected topology — every configured tunnel
peer should have an IKE SA. Missing SAs mean the tunnel was never initiated or
was cleared. Any SA not showing an established state requires Step 2 diagnosis.

For IKEv1, map the Cisco state name to the negotiation phase:
- **MM_NO_STATE** → no exchange started or failed at SA proposal
- **MM_SA_SETUP** → SA proposal accepted, DH exchange next
- **MM_KEY_EXCH** → DH complete, authentication next
- **MM_KEY_AUTH** → authenticated, completing
- **QM_IDLE** → Phase 1 complete, ready for Phase 2

### Step 2: Diagnose Stuck or Failed State

For any SA not in established state, the IKE state reveals the failure domain.

**IKEv1 Main Mode failure isolation:**
- **Stuck at MM_NO_STATE:** No response from peer. Check: peer reachable on UDP 500, firewall permits IKE, peer has matching crypto map, peer IKE process running.
- **Stuck at MM_SA_SETUP:** Proposal mismatch. The peers agreed on an SA but the DH key exchange failed. Check: DH group mismatch between proposals.
- **Stuck at MM_KEY_EXCH:** Authentication failure. DH succeeded but identity verification failed. Check: PSK mismatch, certificate chain invalid, peer ID type mismatch (IP vs FQDN).
- **QM_IDLE with no Phase 2:** Phase 1 established but no IPSec SA created. Check: no interesting traffic triggering the tunnel, proxy ID mismatch, transform set mismatch.

**IKEv2 failure isolation:**
- **No SA_INIT response:** Peer unreachable on UDP 500/4500 or no matching IKE proposal.
- **NO_PROPOSAL_CHOSEN notify:** No overlapping crypto suite. Compare encryption, PRF, integrity, and DH group on both sides.
- **INVALID_KE_PAYLOAD notify:** DH group mismatch. The responder returns its preferred group; initiator should retry automatically.
- **AUTHENTICATION_FAILED notify:** PSK mismatch or certificate validation failure.
- **TS_UNACCEPTABLE notify:** Traffic selector (proxy ID) mismatch between peers.

Check SA detail for error messages and last failure reason:

**[Cisco]**
```
show crypto isakmp sa detail
show crypto ikev2 sa detail
```

**[JunOS]**
```
show security ike security-associations detail
```

**[PAN-OS]**
```
show vpn ike-sa gateway <name>
```

**[FortiGate]**
```
diagnose vpn ike gateway list name <name>
```

### Step 3: Verify Crypto Parameter Alignment

For proposal mismatches, compare configured crypto parameters across both peers.

**Phase 1 / IKE parameters to verify:**

| Parameter | Must Match? | Notes |
|-----------|-------------|-------|
| Encryption algorithm | Yes | AES-128, AES-256, 3DES — must be identical |
| Hash / integrity | Yes | SHA-256, SHA-384, SHA-512 — must be identical |
| DH group | Yes | Group 14 (2048-bit), 19 (256-bit ECP), 20 (384-bit ECP) |
| Authentication method | Yes | PSK, RSA-sig, ECDSA — must agree |
| SA lifetime | Negotiable | Shorter value wins; large discrepancies cause rekey issues |
| IKE version | Yes | Both peers must use the same version |

**[Cisco]**
```
show crypto isakmp policy
show crypto ikev2 proposal
```

**[JunOS]**
```
show security ike proposal
```

**[PAN-OS]**
```
show vpn ike crypto-profiles
```

**[FortiGate]**
```
diagnose vpn ike config list
```

Verify Phase 2 / IPSec parameters similarly: encryption, hash, PFS DH group,
and SA lifetime must align. Proxy IDs (traffic selectors) must match or overlap.

### Step 4: Validate Phase 2 / Child SA

With Phase 1 established, verify IPSec SAs are created and functional.

**[Cisco]**
```
show crypto ipsec sa
```

**[JunOS]**
```
show security ipsec security-associations
```

**[PAN-OS]**
```
show vpn ipsec-sa
```

**[FortiGate]**
```
diagnose vpn tunnel list
```

Verify for each tunnel: SA state (active), SPI values (inbound and outbound
present), proxy IDs / traffic selectors match intended protected networks,
encapsulation mode (tunnel or transport), and PFS status.

Common Phase 2 failures:
- **Transform set mismatch:** encryption or hash algorithm differs
- **Proxy ID mismatch:** local/remote network definitions do not match between peers — the most common interop failure
- **PFS DH group mismatch:** one side requires PFS, other has it disabled or uses a different DH group
- **No interesting traffic:** policy-based VPN requires matching traffic to trigger Quick Mode

### Step 5: Assess Tunnel Health

For established tunnels, evaluate operational health indicators.

**Counter analysis:**
Check encap/decap counters in IPSec SA output. Both should increment steadily.

| Condition | Interpretation |
|-----------|----------------|
| Encap incrementing, decap zero | Outbound traffic sent but nothing returned — remote peer issue, routing, or ACL |
| Decap incrementing, encap zero | Receiving traffic but not sending — local routing or crypto ACL issue |
| Both incrementing | Tunnel passing traffic in both directions |
| Both zero | Tunnel established but no traffic matched — verify routing and proxy IDs |
| Encrypt/decrypt errors rising | Crypto processing failures — check for hardware crypto engine issues |
| Replay failures | Anti-replay window exceeded — packet reordering, QoS, or async routing |

**DPD health:** Verify DPD packets are exchanged. If DPD declares a peer dead,
check the underlying transport path — DPD failures indicate loss of reachability,
not a crypto problem.

**Rekey status:** Verify SAs are rekeying before expiry. A tunnel that fails to
rekey will drop traffic when the SA expires. Check lifetime remaining and
compare against rekey margin.

**NAT-T health:** If NAT-T is active (UDP 4500), verify NAT keepalive interval
is shorter than the NAT device's UDP session timeout. Typical NAT timeout is
60–300s; keepalive should be 10–30s.

### Step 6: Generate Report

Compile findings using the Report Template below. Classify each finding by
severity and include the IKE state or counter evidence that supports the
diagnosis.

## Threshold Tables

Operational parameter norms for IPSec/IKE VPN — protocol-level expectations.

| Parameter | Typical Default | Warning | Critical |
|-----------|----------------|---------|----------|
| IKE SA Lifetime | 86400s (24h) | <10% remaining without rekey initiated | Expired without rekey |
| IPSec SA Lifetime | 3600s (1h) | <10% remaining without rekey initiated | Expired without rekey |
| DPD Interval | 10–30s | >60s (slow detection) | DPD disabled on critical tunnels |
| DPD Retries | 3–5 | >10 (slow failover) | 0 (DPD disabled) |
| NAT-T Keepalive | 20s | >NAT timeout / 2 | >NAT session timeout |
| Rekey Margin | 540s (IKE), 270s (IPSec) | <60s (tight rekey window) | 0s (rekey at expiry) |

**Counter Thresholds:**

| Counter | Healthy | Warning | Critical |
|---------|---------|---------|----------|
| Encap packets | Incrementing | Flat for >5 min | Zero after tunnel up >10 min |
| Decap packets | Incrementing | Flat for >5 min | Zero after tunnel up >10 min |
| Encrypt errors | 0 | >0 but <0.1% of encap | >1% of encap |
| Decrypt errors | 0 | >0 but <0.1% of decap | >1% of decap |
| Replay failures | 0 | >0 occasional | Sustained >10/min |
| Rekey failures | 0 | 1 (recovered) | >1 consecutive |

**Crypto Strength Minimums (current best practice):**

| Parameter | Minimum | Recommended | Avoid |
|-----------|---------|-------------|-------|
| Encryption | AES-128 | AES-256 | DES, 3DES |
| Hash / PRF | SHA-256 | SHA-384+ | MD5, SHA-1 |
| DH Group | 14 (2048-bit) | 19/20 (ECP 256/384) | 1, 2, 5 |

## Decision Trees

### IKE SA State Triage

```
VPN tunnel not working
├── No IKE SA exists
│   ├── Tunnel never configured? → Verify crypto map / IKE gateway config
│   ├── Peer unreachable? → Ping peer, check UDP 500 path
│   ├── No interesting traffic? → (Policy-based) verify crypto ACL matches
│   └── SA cleared / expired? → Check logs for delete or expiry events
│
├── IKE SA exists but NOT established
│   ├── IKEv1 MM_NO_STATE / AG_NO_STATE
│   │   ├── No response from peer → UDP 500 blocked or peer not configured
│   │   └── Proposal mismatch → Compare ISAKMP policies on both sides
│   │
│   ├── IKEv1 MM_SA_SETUP (stuck)
│   │   └── DH group mismatch → Align DH groups in proposals
│   │
│   ├── IKEv1 MM_KEY_EXCH (stuck)
│   │   ├── PSK mismatch → Verify pre-shared keys on both peers
│   │   ├── Certificate failure → Check cert chain, expiry, CRL
│   │   └── ID type mismatch → Verify peer ID (IP vs FQDN)
│   │
│   ├── IKEv2 NO_PROPOSAL_CHOSEN
│   │   └── No overlapping crypto suite → Align enc, PRF, integrity, DH
│   │
│   ├── IKEv2 AUTHENTICATION_FAILED
│   │   ├── PSK mismatch → Verify keys
│   │   └── Certificate error → Check chain, OCSP/CRL, SAN
│   │
│   └── IKEv2 TS_UNACCEPTABLE
│       └── Traffic selector mismatch → Align proxy IDs / encryption domains
│
├── IKE SA established, no IPSec SA (Phase 2 failure)
│   ├── Transform set mismatch → Compare Phase 2 proposals
│   ├── Proxy ID mismatch → Compare local/remote network definitions
│   ├── PFS DH group mismatch → Align or disable PFS on both sides
│   └── No traffic trigger → (Policy-based) send matching traffic
│
└── Both SAs established, no traffic
    ├── Routing? → Verify routes point through tunnel interface
    ├── Encap up, decap zero → Remote peer or return-path issue
    ├── Both counters zero → No matching traffic; check ACL/policy
    └── Errors incrementing → Check crypto engine, replay, MTU
```

### Tunnel Flapping Triage

```
Tunnel repeatedly drops and re-establishes
├── DPD declaring peer dead
│   ├── Underlying transport unstable → Check physical link, ISP circuit
│   ├── QoS dropping IKE keepalives → Verify DSCP marking for IKE traffic
│   └── DPD timer too aggressive → Increase interval or retries
│
├── Rekey failure
│   ├── Lifetime mismatch → Both sides rekey at different times
│   ├── Simultaneous rekey collision → One side should be initiator-only
│   └── Crypto engine overloaded → Check CPU during rekey burst
│
├── Certificate expiry
│   └── Cert expired mid-session → Monitor cert validity, automate renewal
│
└── NAT mapping expiry
    ├── Keepalive > NAT timeout → Reduce NAT-T keepalive interval
    └── NAT device rebooted → SA stale until DPD detects and renegotiates
```

## Report Template

```
VPN/IPSEC TROUBLESHOOTING REPORT
==================================
Device: [hostname]
Vendor: [Cisco | JunOS | PAN-OS | FortiGate]
IKE Version: [IKEv1 | IKEv2]
Check Time: [timestamp]
Performed By: [operator/agent]

TUNNEL INVENTORY:
- Total configured tunnels: [n]
- IKE SAs established: [n] | Failed/Missing: [n]
- IPSec SAs active: [n] | Failed/Missing: [n]
- Tunnels requiring attention: [list with states]

FINDINGS:
1. [Severity] [Category] — [Description]
   Tunnel: [peer address / tunnel name]
   IKE State: [current state]
   Observed: [state, counter, or error]
   Expected: [normal state or value]
   Root Cause: [diagnosis from decision tree]
   Action: [recommended remediation]

CRYPTO PARAMETER SUMMARY:
- IKE: [encryption] / [hash] / [DH group] / [auth method] / [lifetime]
- IPSec: [encryption] / [hash] / [PFS group] / [lifetime]
- Strength Assessment: [meets minimum | below minimum — specify gap]

TUNNEL HEALTH:
- Encap/Decap: [incrementing | flat | zero]
- Errors: [count and type]
- DPD: [active | disabled | peer-dead events]
- NAT-T: [active on port 4500 | not detected | misconfigured]
- Last Rekey: [timestamp] | Next Rekey: [timestamp]

RECOMMENDATIONS:
- [Prioritized action list]

NEXT CHECK: [CRITICAL: 1hr, WARNING: 8hr, HEALTHY: 24hr]
```

## Troubleshooting

### Proxy ID / Traffic Selector Mismatch

The most common multi-vendor interop failure. Each vendor expresses protected
networks differently. Cisco uses crypto ACLs, JunOS uses address-book entries,
PAN-OS uses proxy IDs in the tunnel config, FortiGate uses phase2 selectors.
Compare the effective local/remote network pairs on both sides — they must
mirror (local on one = remote on the other). For IKEv2, check TS_UNACCEPTABLE
notify in logs.

### NAT-T Not Activating

If NAT exists between peers but tunnels use ESP (protocol 50) instead of UDP
4500, verify NAT-T is enabled on both sides. **[Cisco]** requires
`crypto isakmp nat-traversal`; **[FortiGate]** enables it by default;
**[JunOS]** and **[PAN-OS]** enable it automatically when NAT is detected.
Firewalls between peers must allow both UDP 500 and UDP 4500.

### DPD Premature Failover

DPD declares peer dead when keepalive probes are lost. If the tunnel is
functional but DPD triggers, the underlying path may have transient loss or
QoS may deprioritize IKE/ESP. Increase the DPD retry count or interval.
Verify the DPD mode: **[Cisco]** `on-demand` only sends probes when there is
outbound traffic; `periodic` sends probes regardless.

### Rekey Failures

If a tunnel drops at SA expiry instead of rekeying, check: (1) lifetime
mismatch causing both sides to rekey simultaneously, (2) IKE SA expired before
IPSec SA rekey completed (IKE SA must be active to negotiate new IPSec SA),
(3) crypto engine busy (high tunnel count causing rekey storm). Stagger
lifetimes by 5–10% between peers to avoid simultaneous rekey.

### MTU / Fragmentation Issues

IPSec overhead (ESP header, IV, padding, ICV) reduces effective MTU. With
AES-256/SHA-256 in tunnel mode, overhead is approximately 73 bytes. If
traffic requires near-MTU packets, set tunnel interface MTU to 1400 and
TCP MSS to 1360. Symptoms of MTU issues: small packets pass, large transfers
stall or fail. **[Cisco]** `crypto ipsec df-bit clear` clears the DF bit to
allow fragmentation. Pre-fragmentation (before encryption) is preferred over
post-fragmentation.
