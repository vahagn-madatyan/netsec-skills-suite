# IKE State Machines

Reference for IKE negotiation state machines used in IPSec VPN establishment.
Covers IKEv1 Main Mode, IKEv1 Aggressive Mode, IKEv2 exchange model, and
Quick Mode (IPSec Phase 2). Each section describes the exchange sequence,
per-message payloads, and common stuck-state causes.

## IKEv1 Main Mode (Phase 1)

Six-message exchange in three pairs. Establishes an IKE SA (ISAKMP SA) with
identity protection — peer identities are encrypted in the final pair.

```
Initiator                          Responder
    │                                  │
    │── MSG 1: SA Proposal ──────────→ │  Pair 1: SA Negotiation
    │←── MSG 2: SA Accepted ──────────│
    │                                  │
    │── MSG 3: KE + Nonce ───────────→ │  Pair 2: Key Exchange
    │←── MSG 4: KE + Nonce ──────────│
    │                                  │
    │── MSG 5: ID + Auth (encrypted) → │  Pair 3: Authentication
    │←── MSG 6: ID + Auth (encrypted)│
    │                                  │
    [IKE SA Established — MM_ACTIVE]
```

### Message Payloads

| Pair | Messages | Initiator Sends | Responder Sends |
|------|----------|-----------------|-----------------|
| 1 — SA | MSG 1, 2 | SA proposals (encryption, hash, DH group, auth method, lifetime) | Selected SA proposal |
| 2 — KE | MSG 3, 4 | KE payload (DH public value), Nonce | KE payload (DH public value), Nonce |
| 3 — Auth | MSG 5, 6 | ID, Auth hash (encrypted with session keys) | ID, Auth hash (encrypted with session keys) |

### Cisco IKEv1 Main Mode States

| State | Meaning | What Happened |
|-------|---------|---------------|
| MM_NO_STATE | Initial / failed | SA proposal sent but no response received |
| MM_SA_SETUP | SA negotiated | MSG 1–2 complete; SA proposal accepted |
| MM_KEY_EXCH | DH exchange done | MSG 3–4 complete; key material exchanged |
| MM_KEY_AUTH | Authenticated | MSG 5–6 complete; identities verified |
| QM_IDLE | Phase 1 complete | IKE SA established, ready for Quick Mode |

### Stuck States and Causes

| Stuck State | Typical Cause | Diagnosis |
|-------------|---------------|-----------|
| MM_NO_STATE | No response from peer | Peer unreachable, UDP 500 blocked, no matching crypto map on peer, peer not configured |
| MM_SA_SETUP (stuck) | DH group mismatch | Initiator and responder disagree on DH group; MSG 3 KE payload rejected |
| MM_KEY_EXCH (stuck) | Authentication failure | Pre-shared key mismatch, certificate validation failure, or ID type mismatch |
| QM_IDLE (no phase 2) | Phase 2 not triggered | No matching crypto ACL traffic, proxy ID mismatch, or transform set mismatch |

## IKEv1 Aggressive Mode (Phase 1)

Three-message exchange — faster than Main Mode but exposes peer identities in
cleartext (no identity protection).

```
Initiator                          Responder
    │                                  │
    │── MSG 1: SA + KE + Nonce + ID ─→ │
    │←── MSG 2: SA + KE + Nonce + ID + Auth │
    │── MSG 3: Auth ─────────────────→ │
    │                                  │
    [IKE SA Established — AG_AUTH]
```

| Message | Content |
|---------|---------|
| MSG 1 | SA proposals, KE payload, Nonce, Initiator ID (cleartext) |
| MSG 2 | Selected SA, KE payload, Nonce, Responder ID (cleartext), Auth hash |
| MSG 3 | Initiator Auth hash |

**Security concern:** Identities sent in cleartext in MSG 1 and 2. Aggressive
Mode is vulnerable to offline dictionary attacks against PSK and should be
avoided where possible. IKEv2 replaces both modes.

### Stuck States

- **AG_NO_STATE:** No response to MSG 1 — same causes as MM_NO_STATE.
- **AG_INIT_EXCH:** MSG 1 sent, no reply — peer unreachable or proposal mismatch.
- **AG_AUTH:** Authentication failed on MSG 2 or MSG 3 — PSK or certificate mismatch.

## IKEv2 Exchange Model

IKEv2 (RFC 7296) replaces IKEv1 with a simpler request/response model.
Two exchanges establish both IKE SA and first Child SA (IPSec SA).

```
Initiator                          Responder
    │                                  │
    │── IKE_SA_INIT request ─────────→ │  Exchange 1: IKE SA
    │←── IKE_SA_INIT response ───────│
    │                                  │
    │── IKE_AUTH request (encrypted) → │  Exchange 2: Auth + Child SA
    │←── IKE_AUTH response (encrypted)│
    │                                  │
    [IKE SA + first Child SA established]
```

### IKE_SA_INIT Exchange

| Direction | Payloads |
|-----------|----------|
| Request | SAi1 (crypto proposals), KEi (DH public value), Ni (Nonce) |
| Response | SAr1 (selected proposal), KEr (DH public value), Nr (Nonce) |

Establishes the IKE SA cryptographic parameters and generates shared key
material. If the responder rejects all proposals, it returns NO_PROPOSAL_CHOSEN.
If a DH group mismatch occurs, the responder returns INVALID_KE_PAYLOAD with
the preferred group — the initiator retries with the correct group.

### IKE_AUTH Exchange

| Direction | Payloads |
|-----------|----------|
| Request | IDi, AUTH, SAi2 (Child SA proposals), TSi, TSr |
| Response | IDr, AUTH, SAr2 (selected Child SA proposal), TSi, TSr |

All IKE_AUTH payloads are encrypted with the IKE SA keys. Authenticates peers
(PSK, certificates, or EAP) and establishes the first Child SA simultaneously.
Traffic Selectors (TSi/TSr) define what traffic the Child SA protects.

### CREATE_CHILD_SA Exchange

Used for additional Child SAs or IKE SA rekeying after the initial exchange.

| Purpose | Initiator Sends | Responder Sends |
|---------|-----------------|-----------------|
| New Child SA | SA, Ni, [KEi], TSi, TSr | SA, Nr, [KEr], TSi, TSr |
| Rekey IKE SA | SA, Ni, KEi | SA, Nr, KEr |

### IKEv2 States (Platform-Dependent)

| State | Meaning |
|-------|---------|
| SA_INIT_SENT | IKE_SA_INIT request sent, awaiting response |
| SA_INIT_RECV | IKE_SA_INIT received, processing |
| SA_AUTH_SENT | IKE_AUTH request sent, awaiting response |
| ESTABLISHED | IKE SA and at least one Child SA active |
| REKEYING | IKE SA or Child SA rekey in progress |
| DELETING | Delete notification sent, SA being removed |

### IKEv2 Stuck States

| Condition | Cause | Diagnosis |
|-----------|-------|-----------|
| No SA_INIT response | Peer unreachable, UDP 500/4500 blocked | Check connectivity, firewall rules for UDP 500 and 4500 |
| NO_PROPOSAL_CHOSEN | No matching crypto suite | Compare proposals on both sides; check encryption, PRF, integrity, DH group |
| INVALID_KE_PAYLOAD | DH group mismatch | Initiator retries with responder's preferred group; if persistent, align config |
| AUTHENTICATION_FAILED | PSK mismatch or cert validation failure | Verify PSK on both ends, check certificate chain and CRL/OCSP |
| TS_UNACCEPTABLE | Traffic selector mismatch | Proxy IDs / encryption domains do not overlap |
| SA_AUTH timeout | Peer processing delay or packet loss | Check for EAP timeouts, RADIUS server reachability |

## Quick Mode (IKEv1 Phase 2)

Three-message exchange within an established IKE SA to create IPSec SAs.
All messages are encrypted and authenticated by the Phase 1 IKE SA.

```
Initiator                          Responder
    │                                  │
    │── MSG 1: Hash, SA, Nonce, [ID] → │
    │←── MSG 2: Hash, SA, Nonce, [ID]│
    │── MSG 3: Hash ─────────────────→ │
    │                                  │
    [IPSec SA pair established (inbound + outbound)]
```

### Quick Mode Payloads

| Message | Content |
|---------|---------|
| MSG 1 | SA proposals (transform set: ESP/AH, encryption, hash, lifetime), Nonce, optional proxy IDs (local/remote network), optional PFS KE payload |
| MSG 2 | Selected SA, Nonce, optional proxy IDs, optional PFS KE payload |
| MSG 3 | Hash confirmation |

### Quick Mode Stuck States

| Condition | Cause |
|-----------|-------|
| No Quick Mode initiated | No interesting traffic matching crypto ACL, or crypto map not applied to interface |
| QM proposal rejected | Transform set mismatch (encryption, hash, or PFS DH group) |
| Proxy ID mismatch | Local/remote network definitions do not match between peers |
| PFS DH group mismatch | One side requires PFS with a specific DH group, other side differs or has PFS disabled |
| SA lifetime mismatch | Lifetime values differ — shorter side controls rekey interval |

## Timer Reference

| Timer | Purpose | Typical Default |
|-------|---------|-----------------|
| IKE SA Lifetime | Maximum age of Phase 1 / IKE SA | 86400s (24h) |
| IPSec SA Lifetime | Maximum age of Phase 2 / Child SA | 3600s (1h) or 4608000 KB |
| DPD Interval | Dead Peer Detection probe interval | 10–30s |
| DPD Retry | DPD retry count before declaring peer dead | 3–5 retries |
| NAT-T Keepalive | NAT keepalive to maintain NAT mapping | 20s |
| Rekey Margin | Time before expiry to initiate rekey | 540s (IKE), 270s (IPSec) |

## NAT Traversal (NAT-T)

When NAT is detected between peers (via NAT-D payloads in IKEv1 or NAT_DETECTION_*
in IKEv2), IKE switches from UDP 500 to UDP 4500 and encapsulates ESP in UDP.

**Detection mechanism:**
1. Each peer hashes its own IP:port and the peer's IP:port
2. Both hashes are sent in the exchange
3. If the received hash does not match the computed value, NAT is present

**Impact on troubleshooting:**
- Firewalls must permit UDP 4500 in addition to UDP 500
- ESP protocol (IP protocol 50) is no longer needed — everything is UDP-encapsulated
- NAT keepalive timers must be shorter than the NAT device's UDP session timeout
- Some platforms require explicit NAT-T configuration
