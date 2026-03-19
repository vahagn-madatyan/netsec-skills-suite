# Wireless Controller CLI / API Reference

Read-only commands and API endpoints for wireless security audit across
Cisco WLC, Aruba, and Meraki platforms. Organized by audit category
matching the procedure steps in SKILL.md.

All commands are read-only (show/display/GET). No configuration changes.

## SSID Configuration Audit

| Audit Check | [Cisco WLC] | [Aruba] | [Meraki] |
|-------------|-------------|---------|----------|
| List all SSIDs | `show wlan summary` | `show wlan ssid-profile` | `GET /networks/{networkId}/wireless/ssids` |
| SSID detail (security, VLAN, auth) | `show wlan <id>` | `show wlan ssid-profile <name>` | `GET /networks/{networkId}/wireless/ssids/{number}` |
| SSID status (enabled/disabled) | `show wlan summary` (Status column) | `show wlan virtual-ap` | Response field `enabled` in SSID endpoint |
| VLAN assignment | `show wlan <id>` → Interface field | `show wlan virtual-ap` → VLAN | Response field `vlanId` in SSID endpoint |
| Broadcast SSID / hidden | `show wlan <id>` → Broadcast SSID | `show wlan ssid-profile <name>` → Hide SSID | Response field `visible` in SSID endpoint |

## Authentication and Encryption Audit

| Audit Check | [Cisco WLC] | [Aruba] | [Meraki] |
|-------------|-------------|---------|----------|
| Encryption mode (WPA2/WPA3) | `show wlan <id>` → Security Policies | `show wlan ssid-profile <name>` → WPA version | Response field `encryptionMode` in SSID endpoint |
| Auth method (PSK/802.1X/Open) | `show wlan <id>` → Authentication | `show wlan ssid-profile <name>` → Authentication | Response field `authMode` in SSID endpoint |
| PMF status | `show wlan <id>` → PMF | `show wlan ssid-profile <name>` → Management Frame Protection | Response field `wpa3` settings in SSID endpoint |
| Key management | `show wlan <id>` → AKM | `show wlan ssid-profile <name>` → Key Management | `GET /networks/{networkId}/wireless/ssids/{number}` |
| Cipher suite | `show wlan <id>` → Encryption Cipher | `show ap wlan-encryption-stats` | Response field `splashPage` and auth settings |

## 802.1X / RADIUS Validation

| Audit Check | [Cisco WLC] | [Aruba] | [Meraki] |
|-------------|-------------|---------|----------|
| RADIUS server list | `show radius summary` | `show aaa authentication-server all` | `GET /networks/{networkId}/wireless/ssids/{number}` → `radiusServers` |
| RADIUS server status | `show radius auth statistics` | `show aaa authentication-server radius statistics` | Dashboard: Wireless > Access Control > RADIUS servers |
| RADIUS accounting | `show radius acct statistics` | `show aaa accounting statistics` | Response field `radiusAccountingEnabled` |
| EAP type (on RADIUS side) | `show client detail <mac>` → EAP Type | `show user <mac>` → Authentication method | `GET /networks/{networkId}/clients/{clientId}` |
| Certificate auth status | `show certificate summary` | `show crypto pki certificate` | Dashboard: Organization > Certificates |
| Timeout / retry config | `show radius summary` → Timeout | `show aaa authentication-server radius` → Timeout | SSID endpoint → `radiusServers[].timeout` |

## Rogue AP Detection

| Audit Check | [Cisco WLC] | [Aruba] | [Meraki] |
|-------------|-------------|---------|----------|
| Rogue AP summary | `show rogue ap summary` | `show wids-event` | `GET /networks/{networkId}/wireless/airMarshal` |
| Rogue AP detail | `show rogue ap detailed <mac>` | `show wids-event detail <id>` | Air Marshal event detail in response body |
| Rogue classification | `show rogue ap summary` → Class column | `show wids-event` → Classification | Response field `type` (allowed values: rogue, interferer) |
| Rogue containment status | `show rogue ap summary` → Containment | `show wids containment` | Air Marshal: containment status in response |
| Rogue client count | `show rogue ap clients <mac>` | `show wids-event` → Associated clients | Air Marshal response includes client details |

## RF Security Assessment

| Audit Check | [Cisco WLC] | [Aruba] | [Meraki] |
|-------------|-------------|---------|----------|
| Channel assignment | `show 802.11a` / `show 802.11b` | `show ap radio-database` | `GET /networks/{networkId}/wireless/rfProfiles` |
| Transmit power | `show 802.11a` / `show 802.11b` | `show ap radio-database` → Power | `GET /devices/{serial}/wireless/status` |
| Channel utilization | `show 802.11a cleanair device ap` | `show ap arm-rf-summary` | `GET /networks/{networkId}/wireless/channelUtilizationHistory` |
| AP radio status | `show ap summary` | `show ap database` | `GET /networks/{networkId}/devices` |
| Noise floor | `show 802.11a cleanair` | `show ap arm-state` | `GET /networks/{networkId}/wireless/channelUtilizationHistory` |
| DFS events | `show 802.11a dfs` | `show ap dfs-event` | Dashboard: Wireless > Radio settings |

## Client Assessment

| Audit Check | [Cisco WLC] | [Aruba] | [Meraki] |
|-------------|-------------|---------|----------|
| Connected clients | `show client summary` | `show user-table` | `GET /networks/{networkId}/wireless/clients` |
| Client detail | `show client detail <mac>` | `show user <mac>` | `GET /networks/{networkId}/clients/{clientId}` |
| Client protocol (WPA2/WPA3) | `show client detail <mac>` → Security | `show user <mac>` → Auth type | Client endpoint → `status` field |
| Client RSSI/SNR | `show client detail <mac>` → RSSI | `show user <mac>` → Signal/SNR | `GET /networks/{networkId}/wireless/clients/{clientId}/connectionStats` |
| Guest portal clients | `show custom-web webauth-bundle` | `show captive-portal` | `GET /networks/{networkId}/wireless/ssids/{number}/splashSettings` |

## Notes on Platform Differences

### Meraki — API-Only Automation

Meraki wireless management is cloud-based with no device-level CLI access.
All automation uses the Meraki Dashboard API:
- Base URL: `https://api.meraki.com/api/v1`
- Authentication: API key via `X-Cisco-Meraki-API-Key` header
- Rate limit: 10 requests per second per organization
- Air Marshal (rogue detection) requires the appropriate license tier

### Aruba — AOS and AOS-CX Variation

Commands listed are for AOS (Aruba Mobility Controller / Virtual MC).
AOS-CX switches acting as gateways use different command syntax. Verify
the platform OS version before executing commands.

### Cisco WLC — AireOS vs IOS-XE (C9800)

Commands listed are for AireOS-based WLCs (55xx, 85xx, virtual).
Catalyst 9800 WLCs running IOS-XE use different command syntax:
- AireOS: `show wlan summary`
- IOS-XE (C9800): `show wlan summary` (similar) but `show ap summary`
  output format differs significantly. Verify platform before auditing.
