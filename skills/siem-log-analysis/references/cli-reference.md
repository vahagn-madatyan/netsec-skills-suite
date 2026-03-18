# SIEM Log Analysis CLI Reference — Platform Access and Syslog Verification

Commands for accessing SIEM search interfaces and verifying that network
devices are correctly forwarding syslog data. Used during Step 1 (Verify
Syslog Sources) of the SIEM log analysis procedure.

## SIEM Platform Search Access

### [Splunk] Search Commands

| Command | Purpose |
|---------|---------|
| `\| search index=network sourcetype=syslog` | Search network syslog events in the default network index |
| `\| stats count by src_ip, action` | Aggregate event counts by source IP and action (allow/deny) |
| `\| timechart span=1h count by sourcetype` | Time-series event volume by source type (1-hour buckets) |
| `\| tstats count WHERE index=network by _time, host` | Accelerated search using indexed fields for fast counting |
| `\| inputlookup` | Load lookup tables for enrichment (asset lists, known IPs) |
| `\| table _time, host, src_ip, dest_ip, action` | Format results as a flat table with selected fields |

**Access path:** Splunk Web → Search & Reporting → New Search. Use the
time picker to set the investigation window. For large datasets, use
`| tstats` with indexed fields instead of `| search` for faster results.

### [ELK] Kibana Access

| Method | Purpose |
|--------|---------|
| Kibana → Discover → Select `network-*` index pattern | Browse and filter syslog events interactively |
| Kibana → Dev Tools Console → `GET /network-*/_search` | Direct Elasticsearch API queries with KQL or Lucene |
| `GET /network-*/_count` | Fast event count without retrieving documents |
| `GET /_cat/indices/network-*?v` | List network indices with document counts and sizes |
| KQL filter bar: `event.action: "denied"` | Quick filter using Kibana Query Language |

**Access path:** Kibana → Menu → Discover. Select the appropriate index
pattern (e.g., `network-syslog-*`). Use the KQL filter bar for
interactive filtering. For complex queries, use Dev Tools Console
with the Elasticsearch Query DSL.

### [QRadar] Advanced Search

| Method | Purpose |
|--------|---------|
| Log Activity → Advanced Search → AQL query | Execute AQL queries against the event store |
| `SELECT * FROM events WHERE ...` | AQL base query syntax for event searching |
| `SELECT * FROM flows WHERE ...` | AQL query for NetFlow/IPFIX data |
| Log Activity → Quick Filter → Log Source | Filter events by log source (device) |
| Admin → Log Sources → Log Source Management | Verify configured log sources and parsing status |

**Access path:** QRadar Console → Log Activity tab → click "Advanced
Search" to switch from Quick Filter to AQL mode. AQL queries support
`GROUP BY`, `ORDER BY`, `LAST N MINUTES/HOURS/DAYS` time clauses.

## Network Device Syslog Configuration Verification

Verify that network devices are forwarding syslog events to the SIEM
platform. Run these read-only commands on each device to confirm syslog
destination, facility, and severity settings.

### Syslog Forwarding Status

| Vendor | Command | Key Output Fields |
|--------|---------|-------------------|
| **[Cisco]** | `show logging` | Logging destination (host IP:port), facility, trap level |
| **[JunOS]** | `show system syslog` | Syslog host configuration, facility/severity filters |
| **[EOS]** | `show logging` | Syslog server address, facility, logging level |
| **[PAN-OS]** | `show log-interface-setting` | Log forwarding interface and destination |
| **[FortiGate]** | `get log setting` | Syslog server, facility, severity filter |
| **[FortiGate]** | `diagnose log test` | Generates test log entries — verify SIEM receives them |

### Verification Steps

1. Confirm syslog destination IP matches the SIEM collector/forwarder address
2. Verify facility code matches the SIEM source type or parsing expectation
3. Check severity level is set to capture events needed for investigation
   (typically level 6/informational or lower for full visibility)
4. Validate transport protocol (UDP 514, TCP 514, or TLS 6514) matches
   SIEM listener configuration
5. Run a test event (where supported) and confirm receipt in the SIEM

### Syslog Facility and Severity Reference (RFC 5424)

All SIEM platforms parse syslog using RFC 5424 facility and severity codes.
Understanding these codes is essential for configuring source types and
building severity-based queries.

**Severity Levels:**

| Level | Keyword | Description | SIEM Use |
|-------|---------|-------------|----------|
| 0 | Emergency | System unusable | Always alert |
| 1 | Alert | Immediate action needed | Always alert |
| 2 | Critical | Critical conditions | High-priority events |
| 3 | Error | Error conditions | Operational errors, auth failures |
| 4 | Warning | Warning conditions | Config changes, threshold warnings |
| 5 | Notice | Normal but significant | Login events, state changes |
| 6 | Informational | Informational messages | Traffic logs, session logs |
| 7 | Debug | Debug-level messages | Troubleshooting only — high volume |

**Common Facility Codes for Network Devices:**

| Code | Facility | Typical Use |
|------|----------|-------------|
| 0 | kern | Kernel messages (OS-level events) |
| 4 | auth | Authentication/authorization events |
| 10 | authpriv | Private authentication (SSH, TACACS+) |
| 16–23 | local0–local7 | User-defined — network devices typically use local0–local7 |

**Vendor defaults:** **[Cisco]** defaults to `local7` (facility 23).
**[JunOS]** defaults to facility based on process (e.g., `daemon` for
routing). **[EOS]** defaults to `local4` (facility 20). **[PAN-OS]**
uses `user` facility (1) by default. **[FortiGate]** defaults to
`local7` (facility 23).

### Log Source Health Checks

After verifying device-side configuration, confirm the SIEM is receiving
and parsing events:

- **[Splunk]** — `| metadata type=sources index=network` shows last
  event time per source. Gaps indicate forwarding failures.
- **[ELK]** — `GET /network-*/_search?size=1&sort=@timestamp:desc`
  returns the most recent event per index. Compare timestamp to
  current time.
- **[QRadar]** — Admin → System and License Management → Event
  Count per log source. Zero counts or declining trends indicate
  collection failures.
