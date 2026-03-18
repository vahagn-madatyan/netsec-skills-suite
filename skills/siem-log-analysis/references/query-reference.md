# SIEM Query Reference — Network Security Use Cases

Side-by-side query patterns for Splunk SPL, ELK KQL, and QRadar AQL
organized by network security investigation use case. Each query targets
network device syslog events — not endpoint or application logs.

## Authentication Failures

Identify failed login attempts across network devices by source IP.
Useful for detecting brute-force attacks against management interfaces.

**[Splunk]** SPL:
```
index=network sourcetype=syslog "authentication failure" OR "Login failed"
| stats count by src_ip, host
| where count > 5
| sort -count
```

**[ELK]** KQL:
```
event.outcome: "failure" AND (message: "authentication failure" OR message: "Login failed")
| Filter: source.ip exists
```
Aggregate in Kibana Lens: split by `source.ip`, metric `count`, filter `count > 5`.

**[QRadar]** AQL:
```sql
SELECT sourceip, COUNT(*) AS attempts
FROM events
WHERE LOGSOURCETYPENAME(logsourceid) ILIKE '%network%'
AND (UTF8(payload) ILIKE '%authentication failure%' OR UTF8(payload) ILIKE '%Login failed%')
GROUP BY sourceip
HAVING COUNT(*) > 5
ORDER BY attempts DESC
LAST 24 HOURS
```

**Returns:** Source IPs with >5 failed authentication attempts against
network device management interfaces within the search window.

## Configuration Changes

Detect configuration modification events on network devices. Critical
for change management auditing and unauthorized change detection.

**[Splunk]** SPL:
```
index=network sourcetype=syslog "Configured from" OR "SYSTEM_MSG" OR "commit complete"
| table _time, host, user, _raw
| sort -_time
```

**[ELK]** KQL:
```
message: "Configured from" OR message: "commit complete" OR message: "SYSTEM_MSG"
```

**[QRadar]** AQL:
```sql
SELECT starttime, sourceip, UTF8(payload) AS event_detail
FROM events
WHERE category = 4002
OR UTF8(payload) ILIKE '%configured from%'
OR UTF8(payload) ILIKE '%commit complete%'
ORDER BY starttime DESC
LAST 7 DAYS
```

**Returns:** Timestamped list of configuration change events with
the user or source that initiated the change.

## Firewall and ACL Denies

Identify blocked connections by source/destination to detect scanning,
exfiltration attempts, or misconfigured access policies.

**[Splunk]** SPL:
```
index=network sourcetype=syslog action=denied OR action=dropped OR "Deny" OR "denied"
| stats count by src_ip, dest_ip, dest_port
| where count > 100
| sort -count
```

**[ELK]** KQL:
```
event.action: "denied" OR event.action: "dropped" OR message: "Deny"
```
Aggregate in Kibana: split by `source.ip` and `destination.port`, metric `count`.

**[QRadar]** AQL:
```sql
SELECT sourceip, destinationip, destinationport, COUNT(*) AS deny_count
FROM events
WHERE eventdirection = 'L2R' AND category = 5001
GROUP BY sourceip, destinationip, destinationport
HAVING COUNT(*) > 100
ORDER BY deny_count DESC
LAST 24 HOURS
```

**Returns:** Source/destination pairs with high deny counts, revealing
scanning activity or blocked lateral movement attempts.

## Interface State Changes

Track network interface link up/down events to detect physical layer
issues, cable pulls, or deliberate interface shutdowns during incidents.

**[Splunk]** SPL:
```
index=network sourcetype=syslog "LINK-3-UPDOWN" OR "LINEPROTO-5-UPDOWN" OR "SNMP_TRAP_LINK"
| table _time, host, _raw
| sort -_time
```

**[ELK]** KQL:
```
message: "UPDOWN" OR message: "link up" OR message: "link down" OR message: "SNMP_TRAP_LINK"
```

**[QRadar]** AQL:
```sql
SELECT starttime, LOGSOURCENAME(logsourceid) AS device, UTF8(payload) AS event
FROM events
WHERE UTF8(payload) ILIKE '%UPDOWN%' OR UTF8(payload) ILIKE '%link down%'
ORDER BY starttime DESC
LAST 24 HOURS
```

**Returns:** Chronological list of interface state changes across
network devices — correlate with other events to identify cascading failures.

## VPN Tunnel Events

Monitor VPN tunnel establishment and teardown events for site-to-site
and remote access VPN connections.

**[Splunk]** SPL:
```
index=network sourcetype=syslog "CRYPTO-6-ISAKMP" OR "IKE_PHASE" OR "tunnel" "established" OR "removed"
| table _time, host, src_ip, dest_ip, _raw
| sort -_time
```

**[ELK]** KQL:
```
message: "IKE" OR message: "ISAKMP" OR (message: "tunnel" AND (message: "established" OR message: "removed"))
```

**[QRadar]** AQL:
```sql
SELECT starttime, sourceip, destinationip, UTF8(payload) AS event
FROM events
WHERE UTF8(payload) ILIKE '%ISAKMP%' OR UTF8(payload) ILIKE '%IKE%'
OR (UTF8(payload) ILIKE '%tunnel%' AND (UTF8(payload) ILIKE '%established%' OR UTF8(payload) ILIKE '%removed%'))
ORDER BY starttime DESC
LAST 7 DAYS
```

**Returns:** VPN tunnel lifecycle events — unexpected teardowns may
indicate connectivity issues or active attacks on VPN infrastructure.

## Anomalous Traffic Patterns

Detect unusual event volume or connections to new destinations that
deviate from established baselines.

**[Splunk]** SPL:
```
index=network sourcetype=syslog
| timechart span=1h count AS event_count
| eventstats avg(event_count) AS avg_count, stdev(event_count) AS stdev_count
| eval anomaly=if(event_count > avg_count + 2*stdev_count, "YES", "NO")
| where anomaly="YES"
```

**[ELK]** KQL:
Use Kibana ML (Machine Learning) anomaly detection job on the
`network-*` index with `event_rate` as the detector function and
`host.name` as the partition field. Alternatively, create a threshold
rule alert on event count per host.

**[QRadar]** AQL:
```sql
SELECT DATEFORMAT(starttime, 'YYYY-MM-dd HH') AS hour, COUNT(*) AS event_count
FROM events
WHERE LOGSOURCETYPENAME(logsourceid) ILIKE '%network%'
GROUP BY DATEFORMAT(starttime, 'YYYY-MM-dd HH')
ORDER BY hour DESC
LAST 7 DAYS
```
Compare results against baseline averages. QRadar's built-in anomaly
detection rules can also flag deviations automatically.

**Returns:** Time periods where event volume exceeds 2 standard
deviations from baseline — indicative of scanning, DDoS, or data
exfiltration activity.

## Lateral Movement Indicators

Detect internal-to-internal connections on unusual ports or protocols
that may indicate post-compromise lateral movement.

**[Splunk]** SPL:
```
index=network sourcetype=syslog src_ip=10.0.0.0/8 OR src_ip=172.16.0.0/12 OR src_ip=192.168.0.0/16
dest_ip=10.0.0.0/8 OR dest_ip=172.16.0.0/12 OR dest_ip=192.168.0.0/16
NOT dest_port IN (22, 53, 80, 443, 3389)
| stats dc(dest_ip) AS unique_dests, dc(dest_port) AS unique_ports by src_ip
| where unique_dests > 10 OR unique_ports > 20
```

**[ELK]** KQL:
```
source.ip: (10.0.0.0/8 OR 172.16.0.0/12 OR 192.168.0.0/16)
AND destination.ip: (10.0.0.0/8 OR 172.16.0.0/12 OR 192.168.0.0/16)
AND NOT destination.port: (22 OR 53 OR 80 OR 443 OR 3389)
```
Aggregate by `source.ip`, cardinality of `destination.ip` and `destination.port`.

**[QRadar]** AQL:
```sql
SELECT sourceip, COUNT(DISTINCT destinationip) AS unique_dests,
       COUNT(DISTINCT destinationport) AS unique_ports
FROM events
WHERE INCIDR('10.0.0.0/8', sourceip) AND INCIDR('10.0.0.0/8', destinationip)
AND destinationport NOT IN (22, 53, 80, 443, 3389)
GROUP BY sourceip
HAVING COUNT(DISTINCT destinationip) > 10
ORDER BY unique_dests DESC
LAST 24 HOURS
```

**Returns:** Internal source IPs connecting to many internal
destinations on non-standard ports — a strong lateral movement indicator
requiring immediate investigation.
