# Reconciliation Workflow — Diff Methodology & Scoring

This reference details the entity matching algorithm, gap classification
taxonomy, and data quality scoring framework used in the SOT reconciliation
procedure.

---

## Entity Matching Algorithm

### Primary Matching: Hostname

Match SOT device records to live discovery results using hostname as the
primary key. Both sides must be normalized before comparison:

1. **Lowercase** — `CORE-RTR-01` and `core-rtr-01` are the same device
2. **Strip domain suffix** — `core-rtr-01.example.com` → `core-rtr-01`
3. **Trim whitespace** — trailing spaces in SNMP sysName are common

```
SOT hostname → lowercase → strip domain → normalized key
Live sysName → lowercase → strip domain → normalized key
Match on normalized key equality
```

### Secondary Matching: Fallback Keys

When hostname matching produces ambiguous results (duplicates, naming
convention violations, or hostname changes during migration):

| Priority | Match Key | Source (SOT) | Source (Live) | Notes |
|----------|-----------|-------------|---------------|-------|
| 1 | Hostname | `device.name` | SNMP `sysName.0` | Primary — use after normalization |
| 2 | Serial number | `device.serial` | `show inventory` / SNMP `entPhysicalSerialNum` | Best for hardware identity |
| 3 | Management IP | `device.primary_ip` | Discovery source IP | Reliable if mgmt IP is stable |
| 4 | MAC address | `interface.mac_address` (mgmt) | ARP/SNMP `ifPhysAddress` | Last resort — MAC can change on virtual chassis |

### Matching Result Categories

| Category | Definition | Count Metric |
|----------|-----------|-------------|
| Matched | Entity found in both SOT and live | `matched_count` |
| SOT-only | Entity in SOT but not in live discovery | `sot_only_count` |
| Live-only | Entity in live discovery but not in SOT | `live_only_count` |
| Ambiguous | Entity with multiple potential matches | `ambiguous_count` (requires manual review) |

---

## Gap Classification Taxonomy

### Category 1: SOT-Only (Stale Records)

| Subcategory | Description | Severity | Remediation |
|-------------|-------------|----------|-------------|
| Decommissioned device | Device physically removed but SOT record remains | Medium | Archive record, set status to Decommissioned |
| Planned not deployed | Device in SOT with Planned status, not yet physical | Low | Verify project timeline, keep or remove |
| Discovery gap | Device exists but was unreachable during discovery | High | Re-verify — could be false stale |
| Site mismatch | Device at different site than SOT records | Medium | Update SOT location |

### Category 2: Live-Only (Undocumented Assets)

| Subcategory | Description | Severity | Remediation |
|-------------|-------------|----------|-------------|
| Emergency deployment | Device deployed during incident without SOT update | Critical | Create record immediately |
| Lab/temporary | Test equipment not entered into production SOT | Low | Create record or exclude from scope |
| Shadow IT | Unauthorized device on production network | Critical | Security review + SOT record |
| Scope expansion | Device outside original SOT coverage scope | Medium | Expand SOT scope or document exclusion |

### Category 3: Attribute Mismatches

| Attribute | Comparison | Severity | Impact |
|-----------|-----------|----------|--------|
| Hostname | SOT name vs live sysName | High | Breaks automation lookups |
| Model/type | SOT device_type vs live sysDescr | Medium | Incorrect spare inventory |
| Serial number | SOT serial vs live inventory | Medium | Asset tracking failure |
| Firmware version | SOT local_context vs live sysDescr | Low | Patch compliance blind spot |
| Site/location | SOT site vs expected mgmt subnet | Medium | Topology visualization error |
| Rack/position | SOT rack + position vs physical | Low | DCIM diagram inaccuracy |
| Interface status | SOT enabled vs live ifAdminStatus | High | Operational impact risk |
| Interface description | SOT description vs live ifAlias | Low | Cosmetic |
| IP assignment | SOT IP vs live interface IP | High | Addressing conflict risk |

### Category 4: Relationship Gaps

| Relationship | Expected Source | Verified Against | Severity |
|-------------|----------------|-----------------|----------|
| Cable records | SOT cables | LLDP/CDP neighbors | Medium |
| Circuit assignments | SOT circuits | Interface descriptions + provider | Medium |
| VLAN membership | SOT VLAN assignments | Live switchport config | Medium |
| Prefix-to-VLAN | SOT prefix→VLAN mapping | Live SVI + VLAN database | Low |
| Device-to-rack | SOT rack position | Physical audit / LLDP location TLV | Low |

---

## Data Quality Scoring Framework

### Dimension Definitions

**Completeness** measures field population against a per-role requirement
template. Different device roles have different required fields:

| Device Role | Required Fields |
|-------------|----------------|
| Core router | hostname, mgmt IP, serial, model, site, rack, position, loopback IP, BGP ASN, firmware |
| Distribution switch | hostname, mgmt IP, serial, model, site, rack, position, VLAN trunks |
| Access switch | hostname, mgmt IP, serial, model, site, rack, position, access VLANs |
| Firewall | hostname, mgmt IP, serial, model, site, rack, zone assignments |
| Wireless AP | hostname, mgmt IP, serial, model, site, mounting location, controller |

```
completeness_score = (populated_required_fields / total_required_fields) × 100%
```

**Accuracy** measures how many populated fields match live-observed values.
Only fields with a live-observable equivalent are scored:

```
accuracy_score = (fields_matching_live / discoverable_populated_fields) × 100%
```

Fields NOT accuracy-scoreable (no live equivalent): rack position, custom
notes, organizational tags, planned changes.

**Freshness** measures record currency using the `last_updated` timestamp:

```
freshness_score = average(days_since_last_updated) across all in-scope records
```

Score interpretation: <30 days = Good, 30–90 days = Warning, >90 days = Critical.

**Coverage** measures SOT inventory completeness against live reality:

```
coverage_score = (matched_devices / total_live_devices) × 100%
```

### Composite SOT Health Score

Weighted combination of the four dimensions:

```
health_score = (coverage × 0.30) + (accuracy × 0.30) + (completeness × 0.25) + (freshness_normalized × 0.15)
```

Where `freshness_normalized` converts average days to a 0–100% scale:
- 0 days = 100%
- 30 days = 80%
- 90 days = 50%
- 180+ days = 0%

### Threshold Recommendations

| Dimension | Good | Warning | Critical |
|-----------|------|---------|----------|
| Coverage | ≥95% | 90–95% | <90% |
| Accuracy | ≥90% | 80–90% | <80% |
| Completeness | ≥85% | 70–85% | <70% |
| Freshness (avg days) | <30 | 30–90 | >90 |
| **Composite Health** | **≥85%** | **70–85%** | **<70%** |

### Trending and Reporting

Track composite health score and dimension scores over successive
reconciliation cycles. Plot month-over-month trend to demonstrate
SOT maturity improvement. Alert when any dimension drops below its
warning threshold or when composite score decreases by >5% between
cycles.
