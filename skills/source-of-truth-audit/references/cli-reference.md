# CLI Reference — Source-of-Truth Reconciliation

API endpoints, SDK patterns, and discovery commands organized by
reconciliation step. [NetBox] and [Nautobot] labels mark platform-
specific syntax; unlabeled commands apply to both or to live discovery.

---

## SOT Inventory Extraction

### [NetBox] REST API

Base URL: `https://<netbox-host>/api/`

**Device inventory:**
```bash
# List devices at a site with full attributes
curl -s -H "Authorization: Token $NETBOX_TOKEN" \
  "https://<netbox>/api/dcim/devices/?site=<slug>&limit=500&offset=0"

# Get interfaces for a specific device
curl -s -H "Authorization: Token $NETBOX_TOKEN" \
  "https://<netbox>/api/dcim/interfaces/?device_id=<id>&limit=500"

# IP addresses assigned to a device
curl -s -H "Authorization: Token $NETBOX_TOKEN" \
  "https://<netbox>/api/ipam/ip-addresses/?device_id=<id>"

# Prefixes for a site
curl -s -H "Authorization: Token $NETBOX_TOKEN" \
  "https://<netbox>/api/ipam/prefixes/?site=<slug>"

# Cable records for a device
curl -s -H "Authorization: Token $NETBOX_TOKEN" \
  "https://<netbox>/api/dcim/cables/?device_id=<id>"
```

**pynetbox bulk extraction:**
```python
import pynetbox

nb = pynetbox.api("https://<netbox>", token="<token>")

# All devices at a site
devices = nb.dcim.devices.filter(site="<slug>")
for d in devices:
    print(f"{d.name} | {d.device_type} | {d.serial} | {d.status}")

# Interfaces for a device
interfaces = nb.dcim.interfaces.filter(device_id=d.id)
for iface in interfaces:
    print(f"  {iface.name} | enabled={iface.enabled} | {iface.description}")

# IP addresses for a device
ips = nb.ipam.ip_addresses.filter(device_id=d.id)
for ip in ips:
    print(f"  {ip.address} | status={ip.status} | interface={ip.assigned_object}")
```

### [Nautobot] REST API

Base URL: `https://<nautobot-host>/api/`

**Device inventory:**
```bash
# List devices at a location
curl -s -H "Authorization: Token $NAUTOBOT_TOKEN" \
  "https://<nautobot>/api/dcim/devices/?location=<slug>&limit=500&offset=0"

# Interfaces for a specific device (UUID-based)
curl -s -H "Authorization: Token $NAUTOBOT_TOKEN" \
  "https://<nautobot>/api/dcim/interfaces/?device=<uuid>"

# IP addresses assigned to a device
curl -s -H "Authorization: Token $NAUTOBOT_TOKEN" \
  "https://<nautobot>/api/ipam/ip-addresses/?device=<uuid>"

# Prefixes for a location
curl -s -H "Authorization: Token $NAUTOBOT_TOKEN" \
  "https://<nautobot>/api/ipam/prefixes/?location=<slug>"
```

**[Nautobot] GraphQL bulk extraction:**
```graphql
query DeviceReconciliation($location: String!) {
  devices(location: $location) {
    name
    serial
    device_type { model manufacturer { name } }
    status { name }
    location { name }
    rack { name }
    position
    interfaces {
      name
      enabled
      description
      ip_addresses { address }
      connected_endpoint { ... on Interface { device { name } name } }
    }
  }
}
```

**pynautobot extraction:**
```python
import pynautobot

nautobot = pynautobot.api("https://<nautobot>", token="<token>")

# All devices at a location
devices = nautobot.dcim.devices.filter(location="<slug>")
for d in devices:
    print(f"{d.name} | {d.device_type} | {d.serial} | {d.status}")

# GraphQL query for bulk extraction
query = """
  query { devices(location: "site-a") {
    name serial interfaces { name enabled ip_addresses { address } }
  }}
"""
result = nautobot.graphql.query(query=query)
```

### Field Name Mapping

| Concept | [NetBox] Field | [Nautobot] Field |
|---------|---------------|-----------------|
| Location hierarchy | `site` / `region` | `location` / `location_type` |
| Primary key type | Integer ID | UUID |
| Device status | `status` (slug) | `status` (object with `name`) |
| Custom fields | `custom_fields` dict | `custom_fields` or `_custom_field_data` |
| Cable termination | `termination_a` / `termination_b` | `termination_a` / `termination_b` |

---

## Live Network Discovery

### SNMP Polling

```bash
# Device identification
snmpget -v2c -c <community> <ip> sysName.0
snmpget -v2c -c <community> <ip> sysDescr.0
snmpget -v2c -c <community> <ip> sysLocation.0

# Interface table walk (index, name, admin/oper status, speed)
snmpwalk -v2c -c <community> <ip> ifDescr
snmpwalk -v2c -c <community> <ip> ifAdminStatus
snmpwalk -v2c -c <community> <ip> ifOperStatus
snmpwalk -v2c -c <community> <ip> ifHighSpeed

# Interface aliases (descriptions)
snmpwalk -v2c -c <community> <ip> ifAlias

# LLDP neighbor discovery
snmpwalk -v2c -c <community> <ip> lldpRemSysName
snmpwalk -v2c -c <community> <ip> lldpRemPortId
```

### CLI-Based Collection

```
! Cisco IOS/IOS-XE
show cdp neighbors detail
show lldp neighbors detail
show ip interface brief
show interfaces status
show ip arp
show mac address-table
show ip route summary
show inventory

! Juniper Junos
show lldp neighbors
show interfaces terse
show arp no-resolve
show ethernet-switching table
show route summary
show chassis hardware
```

### ARP/MAC Collection

```bash
# Cisco — ARP table
show ip arp

# Cisco — MAC address table
show mac address-table dynamic

# Juniper — ARP
show arp no-resolve

# Juniper — MAC table
show ethernet-switching table
```
