# Zero Trust Control Validation — CLI Reference

Read-only verification commands for zero trust controls across Cisco IOS-XE,
Juniper JunOS, Palo Alto PAN-OS, and FortiGate FortiOS. Commands are
organized by ZT control category for use during pillar assessments.

All commands are non-disruptive and require read-only administrative access.

## 802.1X / NAC Verification

| Control | [Cisco] | [JunOS] | [PAN-OS] | [FortiGate] |
|---------|---------|---------|----------|-------------|
| 802.1X global status | `show dot1x all` | `show dot1x interface` | N/A (external NAC) | `get switch-controller managed-switch` |
| Auth sessions | `show authentication sessions` | `show dot1x authentication-failed-users` | N/A | `diagnose switch-controller dump managed-switch port-security` |
| NAC posture | `show identity policy` | `show captive-portal` | `show global-protect-gateway` | `diagnose endpoint record list` |
| Port auth state | `show authentication sessions interface Gi1/0/1` | `show dot1x interface ge-0/0/1 detail` | N/A | `get switch-controller managed-switch port-stats` |
| MAC auth bypass | `show mab all` | `show dot1x static-mac` | N/A | `get switch-controller mac-policy` |

## AAA / RADIUS / TACACS+

| Control | [Cisco] | [JunOS] | [PAN-OS] | [FortiGate] |
|---------|---------|---------|----------|-------------|
| AAA config | `show running-config \| section aaa` | `show configuration system authentication-order` | `show config running \| match authentication-profile` | `get system admin` |
| RADIUS servers | `show aaa servers` | `show configuration access radius-server` | `show config running \| match radius` | `get user radius` |
| TACACS+ servers | `show tacacs` | `show configuration system tacplus-server` | `show config running \| match tacplus` | `get user tacacs+` |
| Auth method order | `show aaa method-lists` | `show configuration system authentication-order` | `show authentication-sequence` | `get system admin setting` |
| Active sessions | `show users` | `show system users` | `show admins all` | `get system info admin` |

## MFA / Certificate-Based Authentication

| Control | [Cisco] | [JunOS] | [PAN-OS] | [FortiGate] |
|---------|---------|---------|----------|-------------|
| PKI certificates | `show crypto pki certificates` | `show security pki local-certificate` | `show certificate` | `get vpn certificate local` |
| CA trust chain | `show crypto pki trustpoints` | `show security pki ca-certificate` | `show config running \| match certificate-profile` | `get vpn certificate ca` |
| CRL status | `show crypto pki crls` | `show security pki crl` | `show config running \| match crl` | `get vpn certificate crl` |
| SSH key auth | `show ip ssh` | `show configuration system services ssh` | `show config running \| match ssh` | `get system admin ssh` |
| Client cert auth | `show crypto ssl profile` | `show configuration system services web-management` | `show config running \| match client-cert` | `get vpn ssl settings` |

## Micro-Segmentation Verification

| Control | [Cisco] | [JunOS] | [PAN-OS] | [FortiGate] |
|---------|---------|---------|----------|-------------|
| Security zones | N/A (zone-based FW only) | `show security zones` | `show zone` | `get system zone` |
| VLAN inventory | `show vlan brief` | `show vlans` | N/A | `get system interface \| grep vlan` |
| VRF/VRF-lite | `show vrf` | `show route instance` | `show config running \| match virtual-router` | `get router info vrf` |
| SGT/TrustSec | `show cts interface all` | N/A | N/A | N/A |
| SGT assignments | `show cts role-based sgt-map all` | N/A | N/A | N/A |
| Inter-zone policy | `show policy-map type inspect zone-pair` | `show security policies` | `show running security-rule` | `get firewall policy` |
| VDOM segmentation | N/A | N/A | N/A | `get system vdom-property` |

## Encryption Status

| Control | [Cisco] | [JunOS] | [PAN-OS] | [FortiGate] |
|---------|---------|---------|----------|-------------|
| MACsec interfaces | `show macsec summary` | `show security macsec connections` | N/A | N/A |
| IPsec tunnel status | `show crypto ipsec sa` | `show security ipsec sa` | `show vpn ipsec-sa` | `get vpn ipsec tunnel summary` |
| SSH version | `show ip ssh` | `show configuration system services ssh` | `show config running \| match ssh` | `get system admin ssh` |
| SNMPv3 config | `show snmp user` | `show configuration snmp v3` | `show config running \| match snmp` | `get system snmp user` |
| TLS/HTTPS config | `show ip http server status` | `show configuration system services web-management https` | `show config running \| match ssl-tls` | `get system global \| grep ssl` |

## Policy Enforcement Points

| Control | [Cisco] | [JunOS] | [PAN-OS] | [FortiGate] |
|---------|---------|---------|----------|-------------|
| Firewall rule count | `show access-lists \| include permit\|deny` | `show security policies \| count` | `show running security-rule \| count` | `get firewall policy \| grep -c policyid` |
| Deny-all baseline | `show access-lists \| include deny` | `show security policies from-zone any to-zone any` | `show running security-rule \| match action deny` | `get firewall policy \| grep DENY` |
| Explicit logging | `show access-lists \| include log` | `show security policies detail \| match log` | `show running security-rule \| match log` | `get firewall policy \| grep logtraffic` |
| Rule hit counts | `show access-list [name] \| include hits` | `show security policies hit-count` | `show rule-hit-count` | `get firewall policy \| grep hit` |
| Unused rules | `show access-list [name] \| include 0 matches` | `show security policies hit-count \| match "0 "` | `show rule-hit-count no-hit-count-rules` | `diagnose firewall iprope list \| grep never` |

## Continuous Monitoring and Logging

| Control | [Cisco] | [JunOS] | [PAN-OS] | [FortiGate] |
|---------|---------|---------|----------|-------------|
| Syslog targets | `show logging` | `show configuration system syslog` | `show config running \| match syslog` | `get log syslogd setting` |
| NTP status | `show ntp associations` | `show ntp associations` | `show ntp` | `get system ntp` |
| NTP auth | `show ntp associations detail \| include auth` | `show configuration system ntp` | `show config running \| match ntp` | `get system ntp \| grep authentication` |
| NetFlow/IPFIX | `show flow monitor` | `show services flow-monitoring` | `show config running \| match netflow` | `get system netflow` |
| SIEM integration | `show logging host` | `show configuration system syslog host` | `show log-forwarding` | `get log syslogd filter` |
