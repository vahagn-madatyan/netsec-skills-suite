# VPN/IPSec CLI Reference — 4-Vendor Diagnostic Commands

Read-only show/diagnostic commands organized by diagnosis phase for IPSec/IKE
troubleshooting across Cisco IOS/IOS-XE, Juniper JunOS, Palo Alto PAN-OS,
and FortiGate FortiOS. All commands are non-modifying.

## IKE SA Status

| Function | Cisco | JunOS | PAN-OS | FortiGate |
|----------|-------|-------|--------|-----------|
| IKEv1 SA summary | `show crypto isakmp sa` | `show security ike security-associations` | `show vpn ike-sa` | `diagnose vpn ike gateway list` |
| IKEv2 SA summary | `show crypto ikev2 sa` | `show security ike security-associations` | `show vpn ike-sa` | `diagnose vpn ike gateway list` |
| SA detail (single peer) | `show crypto isakmp sa detail` | `show security ike security-associations detail` | `show vpn ike-sa gateway <name>` | `diagnose vpn ike gateway list name <name>` |
| SA remaining lifetime | Included in `sa detail` | `show security ike security-associations detail` | `show vpn ike-sa` | `diagnose vpn ike gateway list` |
| Active SA count | `show crypto isakmp sa count` | `show security ike security-associations` | `show vpn ike-sa` | `diagnose vpn ike gateway list` |

### IKE SA Status Notes

- Cisco shows IKEv1 and IKEv2 SAs via separate commands; JunOS, PAN-OS, and FortiGate display both versions in unified output.
- On FortiGate, `diagnose vpn ike` requires `diagnose debug enable` first for debug-level commands, but `list` is read-only.
- PAN-OS `show vpn ike-sa` displays IKEv1 state names (MM_ACTIVE, AG_AUTH) and IKEv2 states (ESTABLISHED) in the same table.

## IPSec SA Status (Phase 2 / Child SA)

| Function | Cisco | JunOS | PAN-OS | FortiGate |
|----------|-------|-------|--------|-----------|
| IPSec SA summary | `show crypto ipsec sa` | `show security ipsec security-associations` | `show vpn ipsec-sa` | `diagnose vpn tunnel list` |
| SA detail (single tunnel) | `show crypto ipsec sa peer <IP>` | `show security ipsec security-associations detail` | `show vpn ipsec-sa tunnel <name>` | `diagnose vpn tunnel list name <name>` |
| Proxy ID / traffic selectors | Included in `ipsec sa` detail | `show security ipsec security-associations detail` | `show vpn ipsec-sa` | `diagnose vpn tunnel list` |
| SA lifetime remaining | `show crypto ipsec sa` | SA detail output | `show vpn ipsec-sa` | `diagnose vpn tunnel list` |
| Active tunnel count | `show crypto ipsec sa count` | `show security ipsec statistics` | `show vpn ipsec-sa` | `diagnose vpn tunnel list` |

## Crypto Parameter Verification

| Function | Cisco | JunOS | PAN-OS | FortiGate |
|----------|-------|-------|--------|-----------|
| IKE proposals configured | `show crypto isakmp policy` | `show security ike proposal` | `show vpn ike crypto-profiles` | `diagnose vpn ike config list` |
| IKEv2 proposals | `show crypto ikev2 proposal` | `show security ike proposal` | `show vpn ike crypto-profiles` | `diagnose vpn ike config list` |
| IPSec transform sets | `show crypto ipsec transform-set` | `show security ipsec proposal` | `show vpn ipsec crypto-profiles` | `diagnose vpn ike config list` |
| DH groups in use | Included in SA detail | `show security ike security-associations detail` | `show vpn ike-sa` | `diagnose vpn ike gateway list` |
| Encryption algorithm | Included in SA detail | SA detail output | SA detail output | `diagnose vpn ike gateway list` |
| Hash / integrity algorithm | Included in SA detail | SA detail output | SA detail output | `diagnose vpn ike gateway list` |

### Crypto Verification Notes

- When comparing proposals across vendors, map algorithm names: Cisco uses `aes-256`, JunOS uses `aes-256-cbc`, PAN-OS uses `aes-256-cbc`, FortiGate uses `aes256`.
- DH group numbers are consistent across vendors (group 14 = 2048-bit MODP everywhere).
- Lifetime values must match or the shorter side controls the rekey interval. Some platforms negotiate, others require exact match.

## Tunnel Counters

| Function | Cisco | JunOS | PAN-OS | FortiGate |
|----------|-------|-------|--------|-----------|
| Encap packet count | `show crypto ipsec sa` (pkts encrypt) | `show security ipsec statistics` | `show vpn ipsec-sa` | `diagnose vpn tunnel list` |
| Decap packet count | `show crypto ipsec sa` (pkts decrypt) | `show security ipsec statistics` | `show vpn ipsec-sa` | `diagnose vpn tunnel list` |
| Encap byte count | `show crypto ipsec sa` | `show security ipsec statistics` | `show vpn ipsec-sa` | `diagnose vpn tunnel list` |
| Decap byte count | `show crypto ipsec sa` | `show security ipsec statistics` | `show vpn ipsec-sa` | `diagnose vpn tunnel list` |
| Encrypt errors | `show crypto ipsec sa` (send errors) | `show security ipsec statistics` | `show vpn ipsec-sa` | `diagnose vpn tunnel list` |
| Decrypt errors | `show crypto ipsec sa` (recv errors) | `show security ipsec statistics` | `show vpn ipsec-sa` | `diagnose vpn tunnel list` |
| Replay failures | `show crypto ipsec sa` (replay) | `show security ipsec statistics` | `show vpn ipsec-sa` | `diagnose vpn tunnel list` |
| Rekey count | `show crypto ipsec sa` | SA detail output | `show vpn ipsec-sa` | `diagnose vpn tunnel list` |

## Dead Peer Detection (DPD)

| Function | Cisco | JunOS | PAN-OS | FortiGate |
|----------|-------|-------|--------|-----------|
| DPD status | `show crypto isakmp sa detail` | `show security ike security-associations detail` | `show vpn ike-sa` | `diagnose vpn ike gateway list` |
| DPD interval configured | `show running-config \| include dead-peer` | `show security ike gateway` | `show network ike gateway` | `diagnose vpn ike config list` |
| DPD retry count | In running config | In gateway config | In gateway config | In config output |
| DPD packets sent | `show crypto isakmp sa detail` | SA detail (dpd out) | SA detail | `diagnose vpn ike gateway list` |
| DPD packets received | SA detail | SA detail (dpd in) | SA detail | `diagnose vpn ike gateway list` |
| Peer declared dead | Syslog: `%CRYPTO-5-IKMP_PEER_DEAD` | Syslog: `KMD_PM_P1_NEED_DEL` | System log: `ike-nego-p1-fail` | Event log: `ike dpd peer dead` |

## NAT Traversal (NAT-T)

| Function | Cisco | JunOS | PAN-OS | FortiGate |
|----------|-------|-------|--------|-----------|
| NAT-T status | `show crypto ipsec sa` (UDP encap) | `show security ike security-associations detail` | `show vpn ike-sa` (NAT-T column) | `diagnose vpn ike gateway list` |
| Encapsulation mode | `show crypto ipsec sa` (transport/tunnel + UDP) | SA detail (NAT-T flag) | SA detail | tunnel list output |
| NAT-T port in use | SA shows port 4500 | SA detail shows 4500 | SA shows port 4500 | Shows port 4500 |
| NAT-T keepalive interval | `show running-config \| include nat keepalive` | `show security ike gateway` | IKE gateway config | `diagnose vpn ike config list` |

### NAT-T Notes

- When NAT-T is active, ESP (IP protocol 50) is encapsulated in UDP port 4500. Firewalls between peers must permit UDP 500 (initial exchange) and UDP 4500 (NAT-T data).
- If NAT-T is detected but not configured, the tunnel may fail at Phase 2 or pass Phase 1 but drop data-plane traffic.
- FortiGate enables NAT-T by default; Cisco requires `crypto isakmp nat-traversal` globally.

## Routing and Tunnel Interface

| Function | Cisco | JunOS | PAN-OS | FortiGate |
|----------|-------|-------|--------|-----------|
| Tunnel interface status | `show interface tunnel <n>` | `show interfaces st0` | `show interface tunnel` | `diagnose netlink interface list <name>` |
| Routes via tunnel | `show ip route \| include Tunnel` | `show route table inet.0 \| match st0` | `show routing route \| match tunnel` | `get router info routing-table all` |
| Policy-based VPN match | `show crypto map` | `show security ipsec security-associations` | `show vpn flow` | `diagnose vpn tunnel list` |
| MTU / MSS settings | `show interface tunnel <n>` | `show interfaces st0 detail` | `show interface tunnel` | `diagnose netlink interface list` |
