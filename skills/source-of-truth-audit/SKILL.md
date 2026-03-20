---
name: source-of-truth-audit
description: >-
  Network source-of-truth reconciliation audit comparing intended state in
  [NetBox] or [Nautobot] against live network discovery results. Uses
  [NetBox]/[Nautobot] inline labels where API patterns diverge. Focuses on
  reconciliation methodology, gap classification, and data quality scoring.
license: Apache-2.0
metadata:
  safety: read-only
  author: network-security-skills-suite
  version: "1.0.0"
---

# Source-of-Truth Reconciliation Audit

Network source-of-truth (SOT) reconciliation audit for comparing intended
infrastructure state recorded in [NetBox] or [Nautobot] against live network
reality. This skill provides a systematic reconciliation methodology —
what to extract, what to compare, how to classify gaps, and how to score
data quality — not a comprehensive API tutorial for either platform.

SOT platforms maintain the authoritative record of what the network
*should* look like: device inventory, interface assignments, IP allocations,
VLAN mappings, site/rack topology, and cable records.
Live network state — collected via SNMP, CLI, or streaming telemetry —
represents what the network *actually* looks like. The gap between
intent and reality is the reconciliation target. Where API patterns
diverge between platforms, [NetBox] and [Nautobot] inline labels mark
the platform-specific approach while shared logic remains unlabeled.

Reference `references/cli-reference.md` for [NetBox] REST API and
pynetbox patterns, [Nautobot] REST API and pynautobot patterns, plus
SNMP and CLI discovery commands for live state collection. Reference
`references/reconciliation-workflow.md` for the diff methodology,
gap classification taxonomy, and data quality scoring framework.

## When to Use

- Periodic SOT hygiene audit — scheduled reconciliation to measure and improve data quality
- Pre-automation gate — validating SOT accuracy before trusting it as the source for automation pipelines
- Post-change verification — confirming that executed changes are reflected in the SOT within the expected sync window
- Network migration planning — establishing a baseline of what the SOT knows vs what exists before migration
- Incident root-cause analysis — determining whether a SOT discrepancy contributed to an outage
- Compliance audit preparation — demonstrating that the network inventory is accurate and complete for audit requirements

## Prerequisites

- **[NetBox] access** — API token with read permissions on DCIM, IPAM, circuits, and tenancy modules; base URL confirmed (`curl -s -H "Authorization: Token <token>" https://<netbox>/api/status/` returns version)
- **[Nautobot] access** — API token with read permissions on DCIM, IPAM, circuits, and tenancy; base URL confirmed (`curl -s -H "Authorization: Token <token>" https://<nautobot>/api/status/` returns version); GraphQL endpoint at `/api/graphql/` for bulk extraction
- **Live network discovery credentials** — SNMP v2c community strings or v3 credentials for device polling; SSH/NETCONF credentials for CLI collection; read-only access sufficient
- **Device scope defined** — target sites, device roles, and platforms identified before extraction; large environments should scope by site or region
- **Baseline expectations** — understand the SOT's intended coverage: does it track all devices or only core/distribution infrastructure? Findings are only meaningful against defined coverage scope

## Procedure

Follow these six steps sequentially. Each step builds on the previous —
SOT extraction and live discovery feed the diff analysis, which feeds
gap classification and quality scoring, culminating in the reconciliation
report.

### Step 1: SOT Inventory Extraction

Extract the authoritative device inventory, interface assignments, IP
allocations, and topology data from the SOT platform. The goal is a
complete snapshot of intended state for the in-scope devices.

**[NetBox]** Use the REST API to extract device records with all
relevant attributes. Filter by site or region to scope the extraction:

```
GET /api/dcim/devices/?site=<site-slug>&limit=1000
GET /api/dcim/interfaces/?device_id=<id>&limit=500
GET /api/ipam/ip-addresses/?device_id=<id>
GET /api/ipam/prefixes/?site=<site-slug>
GET /api/dcim/cables/?device_id=<id>
```

Use `?include=custom_fields` to capture organization-specific metadata.
Paginate using `offset` and `limit` parameters — check the `count`
field in responses to ensure complete extraction. For large sites,
pynetbox bulk retrieval is more efficient than raw curl pagination
(see `references/cli-reference.md`).

**[Nautobot]** Use the REST API for the same data extraction. Nautobot
endpoint structure mirrors NetBox with minor namespace differences:

```
GET /api/dcim/devices/?location=<location-slug>&limit=1000
GET /api/dcim/interfaces/?device=<uuid>
GET /api/ipam/ip-addresses/?device=<uuid>
GET /api/ipam/prefixes/?location=<location-slug>
```

For efficient bulk extraction, [Nautobot] offers a GraphQL endpoint
that can retrieve devices with nested interfaces, IPs, and cables in
a single query — significantly reducing API call volume for large
inventories. See `references/cli-reference.md` for the GraphQL query
pattern.

Record the extraction timestamp — this becomes the SOT snapshot time
for freshness calculations in Step 5.

### Step 2: Live Network Discovery

**SNMP Polling** — Walk `sysName`, `sysDescr`, `sysLocation`, and
`ifTable`/`ifXTable` for each device in the target subnet range.
`sysName.0` provides the hostname for entity matching against SOT
records. `ifAdminStatus` and `ifOperStatus` per interface provide
admin/operational state for comparison against SOT interface status.

**CDP/LLDP Neighbor Discovery** — Collect neighbor tables to map
physical connectivity. Compare against SOT cable records to identify
undocumented connections or missing cable entries. On Cisco devices:
`show cdp neighbors detail`; on multi-vendor environments: `show
lldp neighbors detail`.

**IP Address Collection** — Enumerate configured IP addresses per
interface: `show ip interface brief` (Cisco), `show interfaces terse`
(Juniper). Compare against SOT IP address assignments.

**ARP/MAC Table Collection** — Capture ARP and MAC address tables
to detect endpoint presence and validate SOT-documented connections:
`show ip arp`, `show mac address-table`.

**Routing Table Snapshot** — Collect routing tables to verify prefix
advertisements match SOT prefix allocations: `show ip route summary`,
`show ip bgp summary`.

### Step 3: Diff Analysis

Compare SOT-extracted records against live discovery results across
five entity types, each with its own matching criteria and comparison
attributes.

**Device Existence** — Match SOT device records against live SNMP
`sysName` responses. Classify results as:
- *Matched*: Device exists in both SOT and live discovery
- *SOT-only*: Device in SOT but no live response (potentially decommissioned)
- *Live-only*: Device responding but not in SOT (undocumented/shadow IT)

Entity matching uses hostname as the primary key. When hostnames are
ambiguous, fall back to serial number or management IP as secondary
match keys. See `references/reconciliation-workflow.md` for the
matching algorithm.

**Interface State** — For matched devices, compare interface-level
attributes: SOT admin status vs live `ifAdminStatus`, SOT-documented
description vs live `ifAlias`, SOT speed/duplex vs live `ifHighSpeed`.
Flag interfaces where SOT shows "active" but live shows `ifOperStatus`
down — these are the highest-priority mismatches for operational impact.

**IP Address Assignment** — Compare SOT IP allocations against live
interface IP addresses. Flag addresses configured on devices but not
recorded in the SOT (undocumented allocations), and SOT allocations
with status "Active" but no corresponding live configuration
(phantom allocations).

**VLAN Assignment** — Compare SOT VLAN-to-interface mappings against
live switchport configurations. Identify trunk ports carrying VLANs
not documented in SOT and access ports assigned to VLANs different
from SOT records.

**Topology and Connectivity** — Compare SOT cable records against
CDP/LLDP neighbor data. Identify physical connections observed by
LLDP but absent from SOT cable records (undocumented cabling), and
SOT cable records with no matching LLDP neighbor (stale or incorrect
cable documentation).

### Step 4: Gap Classification

Classify diff results into actionable categories with different
operational implications and remediation approaches.

**SOT-Only Entries (Stale Records)** — Devices, interfaces, or IPs
in the SOT but not in live discovery. Common causes: decommissioned
equipment not cleaned from SOT, planned devices not yet deployed, or
discovery scope not reaching the device. Validate with targeted ping
or console access before classifying as truly stale.

**Live-Only Entries (Undocumented Assets)** — Devices, interfaces, or
IPs discovered live but absent from the SOT. Common causes: emergency
deployments not entered into SOT, lab equipment, shadow IT, or devices
outside the SOT's intended scope. These represent the highest SOT
integrity risk — undocumented devices cannot be managed or automated.

**Attribute Mismatches** — Matched entities with conflicting attribute
values: wrong serial number, incorrect model, outdated firmware
version, wrong site/rack/position, or stale interface descriptions.
Mismatches degrade SOT trustworthiness even when the entity is
documented.

**Relationship Gaps** — Missing or incorrect relationships between
entities: cable records absent for LLDP-confirmed connections, prefix
assignments missing VLAN associations, circuits not linked to
interfaces. Relationship gaps break topology visualization and
impact-analysis accuracy.

See `references/reconciliation-workflow.md` for the full gap
classification taxonomy with severity mappings.

### Step 5: Data Quality Scoring

Compute quantitative data quality metrics across four dimensions
to track SOT health over time and identify which areas need the
most remediation attention.

**Completeness** — Percentage of required fields populated per device
record. Required fields vary by device role: core routers need BGP
ASN and loopback IPs; access switches need port profiles and VLAN
assignments. Calculate as `populated_required_fields / total_required_fields × 100%` per device, then average across the inventory.

**Accuracy** — Percentage of populated SOT fields that match live
state. Only measurable for attributes observable via discovery
(hostname, model, serial, interface state, IP assignment). Calculate
as `matching_fields / discoverable_populated_fields × 100%`. Accuracy
below 85% indicates systematic SOT update failures.

**Freshness** — Days since `last_updated` timestamp per record.
[NetBox] exposes `last_updated` on all objects via the API.
[Nautobot] provides `last_updated` with the same semantics. Flag
records not updated in 90+ days as potentially stale — especially
for dynamic attributes like interface operational state.

**Coverage** — Percentage of live-discovered devices with
corresponding SOT records. Calculate as
`matched_devices / total_live_devices × 100%`. Coverage below 95%
means the SOT has blind spots for automation relying on its inventory.

Aggregate the four dimensions into a composite SOT Health Score
for trending. See `references/reconciliation-workflow.md` for the
scoring framework with threshold recommendations.

### Step 6: Reconciliation Report

Compile findings into a structured report with executive summary,
gap inventory, data quality scorecard, and prioritized remediation.

**Executive Summary** — Total devices in scope, match rate, gap
counts by category (SOT-only, live-only, mismatch, relationship),
composite data quality score, and comparison to prior reconciliation
if available.

**Gap Inventory** — Complete list of gaps organized by classification
(Step 4). Each entry includes the affected entity, gap type, severity,
and recommended remediation. Prioritize live-only devices and interface
state mismatches at the top.

**Data Quality Scorecard** — Present the four quality dimensions
as percentages with trend arrows if prior data exists. Break down
scores by site or device role to identify which segments drag down
overall quality.

**Remediation Priorities** — Rank gaps by operational impact:
(1) undocumented live devices → create SOT records immediately,
(2) decommissioned device records → archive or delete,
(3) attribute mismatches → update SOT from live data,
(4) relationship gaps → rebuild cable/circuit records from LLDP.
Estimate effort per category to enable sprint planning.

## Threshold Tables

| Metric | Good | Warning | Critical | Notes |
|--------|------|---------|----------|-------|
| Coverage | ≥95% | 90–95% | <90% | % of live devices with SOT records |
| Accuracy | ≥90% | 80–90% | <80% | % of populated fields matching live state |
| Completeness | ≥85% | 70–85% | <70% | % of required fields populated |
| Freshness | <30 days avg | 30–90 days | >90 days | Average days since last_updated |
| SOT-only rate | <5% | 5–15% | >15% | Stale/decommissioned entries still in SOT |
| Live-only rate | <3% | 3–10% | >10% | Undocumented devices — highest risk |
| Interface mismatch | <10% | 10–25% | >25% | Admin/oper state disagreement |
| Cable record coverage | ≥80% | 60–80% | <60% | LLDP neighbors with matching cable records |

## Decision Trees

```
SOT Platform Selection for Extraction:
├─ [NetBox] deployed? → Use REST API with pagination
│  ├─ Large inventory (>5000 devices)? → Use pynetbox bulk retrieval
│  └─ Custom fields in use? → Include ?include=custom_fields
├─ [Nautobot] deployed? → Choose extraction method:
│  ├─ Need nested relationships? → Use GraphQL endpoint
│  └─ Simple entity lists? → Use REST API
└─ Both deployed? → Reconcile between platforms first, then vs live

Gap Severity Assignment:
├─ Live-only device (undocumented)?
│  ├─ Production network? → Critical — immediate SOT update required
│  └─ Lab/staging? → Medium — document within standard cycle
├─ SOT-only device (stale)?
│  ├─ Shows as active/planned status? → High — misleads automation
│  └─ Shows as decommissioned? → Low — cleanup task
├─ Attribute mismatch?
│  ├─ Hostname or management IP? → High — breaks automation lookups
│  ├─ Serial/model/firmware? → Medium — asset tracking impact
│  └─ Description or rack position? → Low — cosmetic
└─ Relationship gap?
   ├─ Missing cable record for active link? → Medium — topology blind spot
   └─ Stale cable record for removed link? → Low — cleanup task

Discovery Method Selection:
├─ Managed devices with SNMP? → SNMP polling (fastest, most complete)
├─ SNMP blocked by policy? → CLI collection via SSH/NETCONF
├─ Need physical topology? → CDP/LLDP neighbor tables (required)
├─ Need endpoint presence? → ARP/MAC table collection
└─ Need routing state? → Route table + BGP summary
```

## Report Template

```markdown
# Source-of-Truth Reconciliation Report

## Executive Summary
- **SOT platform:** [NetBox/Nautobot] version [X.Y]
- **Scope:** [sites/regions] — [device count] devices in scope
- **Reconciliation date:** [date]
- **Composite SOT Health Score:** [score]%

## Data Quality Scorecard
| Dimension    | Score | Trend | Threshold |
|-------------|-------|-------|-----------|
| Coverage     | [%]   | [↑↓→] | ≥95% good |
| Accuracy     | [%]   | [↑↓→] | ≥90% good |
| Completeness | [%]   | [↑↓→] | ≥85% good |
| Freshness    | [days] | [↑↓→] | <30d good |

## Gap Summary
| Category | Count | Critical | High | Medium | Low |
|----------|-------|----------|------|--------|-----|
| SOT-only (stale) | | | | | |
| Live-only (undoc) | | | | | |
| Attribute mismatch | | | | | |
| Relationship gap | | | | | |

## Gap Inventory

### Critical — Undocumented Live Devices
| # | Hostname | mgmt IP | Discovered Via | Site | Action |
|---|----------|---------|----------------|------|--------|

### High — Stale Active Records
| # | SOT Device | Status in SOT | Last Ping | Action |
|---|------------|---------------|-----------|--------|

### Medium / Low — Attribute & Relationship Gaps
[Grouped table with entity, gap type, current SOT value, live value]

## Remediation Priorities
1. [Immediate — Create SOT records for undocumented devices]
2. [Short-term — Archive stale device records]
3. [Medium-term — Resolve attribute mismatches]
4. [Ongoing — Establish automated sync or webhook triggers]

## Appendix
- Extraction parameters and API query details
- Discovery methodology and SNMP/CLI command inventory
- Scoring framework and threshold definitions
```

## Troubleshooting

**SOT API rate limiting** — [NetBox] and [Nautobot] may throttle API
requests under heavy extraction. Both return HTTP 429; implement
backoff in extraction scripts. Use pagination with modest page sizes
(100–500) rather than requesting all records in a single call.
GraphQL on [Nautobot] reduces total API call volume.

**SNMP discovery returns partial inventory** — Ensure SNMP credentials
match across all device platforms. Devices behind firewalls may need
SNMP access rules. Verify reachability with
`snmpget -v2c -c <community> <ip> sysName.0` before full walks.

**Entity matching failures on hostname** — Matching breaks when
devices have inconsistent naming between SOT and live SNMP `sysName`.
Common causes: FQDN in SOT but short name in SNMP, case mismatches,
or domain suffix differences. Normalize both sides (lowercase, strip
domain) before comparison. Fall back to management IP or serial
number for unresolved entries.

**Large environment performance** — Reconciliation of 10,000+ devices
generates significant data volume. Batch by site or region. Run SOT
extraction and live discovery in parallel to minimize the snapshot
window — a 4-hour gap introduces drift that appears as false mismatches.

**Freshness scores skewed by bulk imports** — If the SOT was recently
bulk-imported, all `last_updated` timestamps reflect the import date.
Flag this in the report and exclude freshness from the composite
score until one reconciliation cycle updates records individually.

**[NetBox] vs [Nautobot] field name differences** — Key divergences:
[NetBox] uses `site` while [Nautobot] uses `location`; [NetBox] uses
integer IDs while [Nautobot] uses UUIDs. Normalize field names before
feeding into the diff engine. See `references/cli-reference.md` for
the field mapping table.
