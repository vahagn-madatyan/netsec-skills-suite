---
name: siem-log-analysis
description: >-
  Network-security-focused SIEM log analysis across Splunk, ELK, and QRadar
  platforms. Guides forensic timeline construction from network device syslog
  events — firewall denies, authentication failures, configuration changes,
  interface events, VPN tunnel state, and lateral movement indicators. Provides
  platform-independent diagnostic reasoning with platform-specific query syntax
  using [Splunk]/[ELK]/[QRadar] inline labels.
license: Apache-2.0
metadata:
  safety: read-only
  author: network-security-skills-suite
  version: "1.0.0"
---

# Network Security SIEM Log Analysis

Forensic timeline construction and threat detection from network device syslog
events across SIEM platforms. This skill guides network-security-focused log
analysis — it is not general SIEM administration, dashboard building, or
data onboarding.

The diagnostic reasoning is platform-independent: what to look for, how to
correlate, and what constitutes an anomaly applies regardless of SIEM platform.
Only query syntax diverges. Platform-specific queries use `[Splunk]` (SPL),
`[ELK]` (KQL/Lucene), and `[QRadar]` (AQL) inline labels. Reference
`references/query-reference.md` for complete side-by-side query patterns
covering seven network security use cases.

All investigation data sources are network device syslog events: firewall
permit/deny logs, authentication messages, configuration change notifications,
interface state changes, VPN tunnel events, and routing protocol messages.
Endpoint logs, application logs, and cloud audit trails are out of scope.

## When to Use

- **Security incident investigation** — build a forensic timeline from network
  device logs when a security event is detected or reported
- **Threat hunting** — proactively search for indicators of compromise in
  network event data (lateral movement, unusual destinations, auth anomalies)
- **Alert triage** — evaluate SIEM alerts from network device sources to
  determine true positive, false positive, or informational classification
- **Compliance log review** — verify that required log sources are active and
  retention policies are met (PCI-DSS 10.6, NIST 800-53 AU-6, ISO 27001
  A.12.4)
- **Anomalous behavior detection** — identify deviations from baseline traffic
  patterns, event volumes, or connection profiles
- **Post-incident timeline construction** — reconstruct the sequence of
  network events surrounding a confirmed security incident for root cause
  analysis and lessons learned

## Prerequisites

- **SIEM platform access:** Search-level privileges on Splunk (Search &
  Reporting), ELK (Kibana Discover + Dev Tools), or QRadar (Log Activity +
  Advanced Search). Read-only access is sufficient for all queries.
- **Network device syslog forwarding:** Target network devices must be
  forwarding syslog events to the SIEM. Use the commands in
  `references/cli-reference.md` to verify forwarding configuration.
- **Time synchronization:** All network devices and the SIEM platform must
  use NTP-synchronized time. Skewed timestamps corrupt correlation and
  timeline accuracy. Verify with `[Cisco]` `show ntp status`, `[JunOS]`
  `show system ntp`, `[EOS]` `show ntp status`.
- **Log familiarity:** Understanding of network device syslog message formats
  — Cisco %FACILITY-SEVERITY-MNEMONIC, Juniper structured syslog, Palo Alto
  CSV-format traffic/threat logs, Arista event format.
- **Baseline data:** At least 7 days of historical log data for statistical
  anomaly detection. Without baseline data, anomaly detection in Step 5
  is limited to manual threshold comparison.

## Procedure

Follow these six steps sequentially. The procedure builds a forensic timeline
from raw syslog events through correlation, anomaly detection, and triage.
Each step produces artifacts consumed by subsequent steps.

### Step 1: Verify Syslog Sources

Before investigating, confirm that all relevant network devices are actively
forwarding syslog events to the SIEM. Missing sources create blind spots
that invalidate investigation conclusions.

Verify on each network device that syslog is configured and forwarding:

- **[Cisco]** — `show logging` confirms syslog destination IP, trap level,
  and facility code
- **[JunOS]** — `show system syslog` shows configured syslog hosts and
  facility/severity filters
- **[EOS]** — `show logging` displays syslog server address and logging level
- **[PAN-OS]** — `show log-interface-setting` confirms log forwarding interface
- **[FortiGate]** — `get log setting` shows syslog server and severity filter;
  `diagnose log test` generates a test event for receipt verification

Confirm SIEM-side receipt of events from each device:

**[Splunk]** — Run `| metadata type=sources index=network` and verify each
device appears with a recent `lastTime` value. Gaps exceeding the device's
expected log rate indicate forwarding failures.

**[ELK]** — Query `GET /network-*/_search?size=1&sort=@timestamp:desc&q=host.name:<device>`
for each device. Compare the returned timestamp against the current time.

**[QRadar]** — Navigate to Admin → Log Sources and verify each network device
shows a non-zero event count and recent "Last Event" timestamp.

See `references/cli-reference.md` for the full syslog verification command
reference including RFC 5424 severity and facility mapping.

### Step 2: Normalize Events

Map raw syslog events to a common field taxonomy so that events from different
vendors and platforms can be correlated. Key normalization fields:

| Common Field | Description | Source Examples |
|-------------|-------------|----------------|
| `timestamp` | Event time (UTC) | syslog header timestamp |
| `source_device` | Originating device hostname | syslog host field |
| `event_type` | Normalized event category | auth, config, traffic, interface, vpn |
| `source_ip` | Source IP address | parsed from message body |
| `dest_ip` | Destination IP address | parsed from message body |
| `dest_port` | Destination port | parsed from message body |
| `action` | Outcome (permit/deny/info) | parsed from message body |
| `user` | Associated username | parsed from auth messages |
| `severity` | RFC 5424 severity (0–7) | syslog PRI field |

**[Splunk]** — Source types (e.g., `cisco:ios`, `juniper:junos`, `pan:firewall`)
provide automatic field extraction via Technology Add-ons (TAs). Verify field
extraction accuracy with `| fieldsummary` on the relevant source type.

**[ELK]** — Ingest pipelines and Logstash filters perform field extraction.
Verify parsed fields in Kibana Discover by expanding an event document.
Missing fields indicate parsing pipeline issues.

**[QRadar]** — Device Support Modules (DSMs) provide automatic parsing.
Check Log Source Extensions if standard DSMs do not extract required fields
for a device type.

### Step 3: Correlate Across Sources

Join events from multiple network devices by shared attributes — timestamp
windows, IP addresses, session identifiers, or user accounts. Correlation
transforms isolated events into investigation threads.

**Correlation strategies:**

1. **IP-based correlation** — join firewall deny events with authentication
   failure events sharing the same source IP within a time window
2. **Time-window correlation** — group events within ±60 seconds of a
   trigger event (e.g., interface down → routing change → traffic shift)
3. **Session-based correlation** — track VPN tunnel establishment through
   to teardown using tunnel/session identifiers
4. **User-based correlation** — follow a user's activity across devices
   (authentication → config change → logout)

**[Splunk]** — Use `| transaction` or `| join` commands to correlate events
across source types. `| transaction src_ip maxspan=5m` groups events by
source IP within 5-minute windows.

**[ELK]** — Use Elasticsearch aggregations with `composite` or `terms`
buckets on shared fields. For complex correlation, use the EQL (Event Query
Language) sequence queries in Security → Timelines.

**[QRadar]** — Offense rules automatically correlate related events. For
manual correlation, use AQL `JOIN` syntax or the "Event Correlation" search
to group events by shared properties.

### Step 4: Build Timeline

Arrange correlated events chronologically to reconstruct the sequence of
network activity. The timeline is the primary investigation artifact.

**Timeline construction:**

1. Select correlated events from Step 3
2. Sort by timestamp (ascending) — ensure UTC normalization
3. Annotate each event with: device, event type, source/dest, action
4. Identify phase transitions: reconnaissance → initial access →
   lateral movement → objectives
5. Mark decision points where the attacker or anomaly changed behavior

**[Splunk]** — `| sort _time | table _time, host, event_type, src_ip, dest_ip, action`
produces a chronological event table. Use `| streamstats` to compute
inter-event time deltas for pattern recognition.

**[ELK]** — Elastic Security → Timelines provides an interactive timeline
builder. Drag correlated events into a timeline and annotate phases.
Alternatively, use Discover sorted by `@timestamp` ascending.

**[QRadar]** — Within an Offense, the "Events" tab shows correlated events
in chronological order. Export to CSV for external timeline tools.

### Step 5: Identify Anomalies

Compare observed events against baselines to surface deviations that may
indicate security threats. Anomalies include unusual event volume, new
source/destination pairs, unexpected protocols, and off-hours activity.

**Statistical anomaly detection:**

**[Splunk]** — Use `| eventstats` to compute rolling averages and standard
deviations, then flag events exceeding 2σ from baseline:
```
| timechart span=1h count | eventstats avg(count) as avg, stdev(count) as sd
| eval anomaly=if(count > avg + 2*sd, 1, 0)
```

**[ELK]** — Configure Kibana ML anomaly detection jobs on the network index
with `event_rate` detectors partitioned by `host.name`. Review anomaly
scores in the ML Explorer. Threshold rule alerts can flag volume spikes
without ML.

**[QRadar]** — QRadar's Anomaly Detection rules (Administrative Offense
rules) identify behavioral deviations automatically. For manual analysis,
query hourly event counts with AQL and compare against 7-day averages.

**Key anomalies for network security:**
- Event volume >2σ from hourly baseline (possible scanning or DDoS)
- New internal-to-internal destination IPs not seen in prior 30 days
- Connections on non-standard ports from internal sources (lateral movement)
- Authentication attempts from IP addresses not in known management ranges
- Configuration changes outside approved maintenance windows
- VPN tunnels established from unexpected source IPs or at unusual times

See `references/query-reference.md` for complete anomaly detection and
lateral movement query patterns across all three platforms.

### Step 6: Triage and Classify

Assign severity to findings, eliminate false positives, and determine
escalation actions. This step transforms investigation results into
actionable decisions.

**Classification process:**

1. Review each anomaly or correlated event chain from Steps 3–5
2. Compare against known benign patterns (scheduled maintenance, authorized
   scanning, expected VPN sources)
3. Assign severity using the Alert Severity Classification table
4. Determine disposition: true positive, false positive, or informational
5. Apply the triage decision tree (see Decision Trees section)

## Threshold Tables

### Alert Severity Classification

| Severity | Criteria | Response |
|----------|----------|----------|
| **Critical** | Confirmed active compromise, data exfiltration evidence, unauthorized admin access | Immediate IR engagement, executive notification |
| **High** | Lateral movement indicators, multiple auth failures + success, unauthorized config changes | Priority investigation within 1 hour, security team alert |
| **Medium** | Anomalous volume >2σ, new destination patterns, single unauthorized access attempt | Investigation within 4 hours, document and track |
| **Low** | Minor policy violations, single firewall deny from known scanner, informational anomaly | Review within 24 hours, tune rules if recurring |
| **Info** | Baseline deviation within normal variance, expected maintenance activity | Log for trending, no immediate action |

### Event Volume Anomaly Thresholds

| Metric | Normal | Warning (>1σ) | Alert (>2σ) | Critical (>3σ) |
|--------|--------|---------------|-------------|-----------------|
| Events per hour (per device) | Baseline ± 1σ | 1–2σ above baseline | 2–3σ above baseline | >3σ above baseline |
| Unique destination IPs (internal host) | ≤20/hour | 21–50/hour | 51–100/hour | >100/hour |
| Failed auth attempts (per source IP) | ≤3/hour | 4–10/hour | 11–50/hour | >50/hour |
| Firewall denies (per source IP) | ≤50/hour | 51–200/hour | 201–1000/hour | >1000/hour |
| Config change events (per device) | ≤2/day | 3–5/day | 6–10/day | >10/day |

### Correlation Confidence Scoring

| Confidence | Criteria | Action |
|------------|----------|--------|
| **High (>0.8)** | 3+ correlated events across 2+ devices with matching IPs and tight time window (<5 min) | Treat as confirmed, escalate |
| **Medium (0.5–0.8)** | 2 correlated events or single-device chain with circumstantial evidence | Investigate further before escalating |
| **Low (<0.5)** | Single event or loose time correlation (>30 min window) | Monitor, do not escalate without additional evidence |

## Decision Trees

### Alert Triage Flow

```
Alert received from SIEM
├── Source device in scope (network infrastructure)?
│   ├── No → Route to appropriate team (endpoint, application, cloud)
│   └── Yes → Continue network security triage
│
├── Known benign pattern?
│   ├── Matches scheduled maintenance window → FALSE POSITIVE
│   │   └── Document, tune alert rule if recurring (>3 occurrences)
│   ├── Matches authorized scanning activity → FALSE POSITIVE
│   │   └── Add scanner IP to allowlist in correlation rule
│   └── No known benign match → Continue investigation
│
├── Correlation confidence (from Step 3)?
│   ├── High (>0.8) → TRUE POSITIVE — escalate
│   │   ├── Critical/High severity → Engage incident response
│   │   │   └── Preserve evidence, initiate IR playbook
│   │   └── Medium/Low severity → Assign to security analyst
│   ├── Medium (0.5–0.8) → PROBABLE — investigate further
│   │   └── Run additional queries from query-reference.md
│   │       └── Confidence increases → Reclassify as True Positive
│   │       └── No supporting evidence → INFORMATIONAL
│   └── Low (<0.5) → INFORMATIONAL
│       └── Document trend, monitor for recurrence
│
└── Disposition recorded?
    ├── Yes → Close alert with classification and notes
    └── No → Document before closing — all alerts require disposition
```

## Report Template

```
NETWORK SECURITY SIEM INVESTIGATION REPORT
=============================================
Investigation ID: [unique identifier]
Investigation Trigger: [alert ID / hunt hypothesis / compliance requirement]
Investigation Window: [start timestamp] — [end timestamp] (UTC)
SIEM Platform: [Splunk / ELK / QRadar]
Analyst: [name/identifier]

SUMMARY:
- Investigation type: [incident / hunt / compliance / triage]
- Severity classification: [Critical / High / Medium / Low / Info]
- Disposition: [True Positive / False Positive / Informational]
- Devices involved: [count and hostnames]

LOG SOURCE VERIFICATION (Step 1):
- Sources confirmed active: [count] / [total expected]
- Sources with gaps: [list any devices with missing or delayed logs]
- Time sync status: [all synchronized / issues noted]

TIMELINE OF EVENTS (Step 4):
| # | Timestamp (UTC) | Device | Event Type | Source IP | Dest IP | Action | Notes |
|---|-----------------|--------|------------|----------|---------|--------|-------|
| 1 | [time] | [host] | [type] | [src] | [dst] | [action] | [context] |

ANOMALIES DETECTED (Step 5):
- [description of anomaly, statistical basis, affected devices]

QUERY EVIDENCE:
- Platform: [Splunk/ELK/QRadar]
- Query used: [paste query]
- Results: [summary of what the query returned]
- Time range: [search window]

CORRELATION ANALYSIS (Step 3):
- Correlation method: [IP / time-window / session / user]
- Confidence score: [High / Medium / Low]
- Supporting evidence: [list of correlated events]

RECOMMENDATIONS:
1. [immediate action — e.g., block IP, isolate device, engage IR]
2. [short-term — e.g., tune detection rule, add log source]
3. [long-term — e.g., improve baseline, add correlation rule]

NEXT STEPS:
- [ ] [action item with owner and deadline]
```

## Troubleshooting

### Missing Log Sources

**Symptom:** A network device that should be forwarding syslog shows no events
in the SIEM for the investigation window.

**Diagnosis:** Verify syslog configuration on the device using commands from
`references/cli-reference.md`. Check network connectivity between device and
SIEM collector (firewall rules on UDP/TCP 514 or TLS 6514).

**Resolution:** Reconfigure syslog forwarding, verify receipt with a test
event, and document the gap period in the investigation report. Findings
during the gap are inconclusive for the affected device.

### Time Synchronization Issues

**Symptom:** Correlated events have implausible timestamps — events that
should be sequential appear out of order or with large gaps.

**Diagnosis:** Check NTP status on affected devices. Compare device clock
with SIEM server clock. Look for daylight saving time or timezone offset
errors (all timestamps should be UTC or consistently offset-adjusted).

**Resolution:** Fix NTP configuration, recalculate event timestamps with
the known offset, and note the time correction in the investigation timeline.
Events from desynchronized sources have reduced correlation confidence.

### Log Parsing Failures

**Symptom:** Events arrive but key fields (source IP, destination IP, action)
are not extracted — they appear only in the raw message body.

**Diagnosis:** Check SIEM-side parsing. **[Splunk]** — verify the correct
Technology Add-on (TA) is installed. **[ELK]** — check ingest pipeline or
Logstash filter for parsing errors. **[QRadar]** — verify the Device Support
Module (DSM) mapping.

**Resolution:** Install or update parsing configuration for the affected
source type. Reprocess raw events if the SIEM supports reindexing.

### Query Performance Problems

**Symptom:** SIEM queries time out or return slowly, especially statistical
queries over large time ranges.

**Diagnosis:** Check the search time range — broad ranges (>30 days)
against non-accelerated data cause performance issues across all platforms.

**Resolution:** Narrow the time range to the investigation window. Use
accelerated search methods: **[Splunk]** `| tstats` over accelerated data
models instead of `| search`. **[ELK]** — use filtered aggregations instead
of full-text queries. **[QRadar]** — use `LAST N HOURS` clauses and avoid
`SELECT *` in AQL queries.

### Incomplete Correlation

**Symptom:** Correlation in Step 3 produces few results despite evidence
of related activity across multiple devices.

**Diagnosis:** Check field normalization from Step 2. Common issues:
IP addresses in different formats (dotted decimal vs integer), timestamps
in different timezones, hostname mismatches between syslog header and
SIEM device name.

**Resolution:** Normalize the correlation fields before joining. Use CIDR
matching instead of exact IP matching where appropriate. Widen the
correlation time window if device clocks have minor drift.
