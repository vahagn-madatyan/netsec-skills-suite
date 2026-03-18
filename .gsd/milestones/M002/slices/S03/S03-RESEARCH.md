# S03: Security Operations Skills — Research

**Date:** 2026-03-17
**Researcher:** auto

## Summary

S03 delivers 3 security operations skills (vulnerability-assessment, siem-log-analysis, incident-response-network) covering R024–R026. The codebase is at 19 validated skills after S01/S02 — all patterns are proven. S03's three skills each use a different established procedure shape and introduce no new infrastructure. The main novel element is the SIEM skill's `[Splunk]`/`[ELK]`/`[QRadar]` vendor-labeling convention for query patterns, which mirrors the existing multi-vendor label approach but with SIEM platforms instead of network vendors.

Risk is low. The vulnerability-assessment skill is the most structured (CVE lookup → CVSS scoring → prioritization — closest to the threshold-comparison pattern). The SIEM skill requires three sets of platform-specific query syntax but the diagnostic reasoning is platform-independent. The incident-response-network skill reuses the event-driven lifecycle shape from change-verification (before → during → after phases) narrowed to network forensics evidence.

All three skills are `metadata.safety: read-only` per D027. Each needs exactly 2 reference files and the 7 required H2 sections. The 2700-word budget is proven comfortable — S01/S02 averaged well under budget with only FortiGate (2692) and Cisco firewall (2694) tight.

## Recommendation

Build in order: **vulnerability-assessment → siem-log-analysis → incident-response-network**. Vulnerability assessment is the most structured and has no novel elements — it proves the slice is on track quickly. SIEM second because it retires the M002 #3 key risk (SIEM vendor fragmentation — proving that `[Splunk]`/`[ELK]`/`[QRadar]` labeled query patterns with platform-independent diagnostic reasoning works). Incident response last because it depends conceptually on both the vulnerability context (CVE triage informs IR priority) and SIEM context (log analysis is a core IR evidence source).

Update README catalog with 3 new rows under the existing "Security Skills" separator after all three skills pass validation.

## Implementation Landscape

### Key Files

**Skill 1: vulnerability-assessment**
- `skills/vulnerability-assessment/SKILL.md` — CVE assessment for network devices: version-to-CVE mapping, CVSS scoring interpretation, remediation prioritization, patch guidance. Multi-vendor labels: `[Cisco]`/`[JunOS]`/`[EOS]`/`[PAN-OS]`/`[FortiGate]`. Procedure shape: threshold-comparison + compliance assessment hybrid (collect version info → query CVE data → score with CVSS → prioritize by severity × exposure × exploitability).
- `skills/vulnerability-assessment/references/cli-reference.md` — Version/patch retrieval commands per vendor (show version, show install, system info equivalents).
- `skills/vulnerability-assessment/references/vulnerability-reference.md` — CVSS v3.1 scoring breakdown, NVD query approach, severity-to-SLA mapping table, vendor-specific advisory sources (Cisco PSIRT, Palo Alto security advisories, Juniper JSA, Fortinet PSIRT, Arista security advisories).

**Skill 2: siem-log-analysis**
- `skills/siem-log-analysis/SKILL.md` — Syslog parsing, event correlation, alert triage, threat hunting queries. Uses `[Splunk]`/`[ELK]`/`[QRadar]` inline labels for platform-specific query syntax. Procedure shape: forensic timeline (collect logs → normalize → correlate events → build timeline → identify anomalies → triage alerts). Diagnostic reasoning is platform-independent; only query syntax diverges.
- `skills/siem-log-analysis/references/cli-reference.md` — SIEM platform access commands, syslog configuration verification on network devices ([Cisco]/[JunOS]/[EOS]/[PAN-OS]/[FortiGate] syslog config verification commands).
- `skills/siem-log-analysis/references/query-reference.md` — Side-by-side query patterns for Splunk SPL, ELK KQL/Lucene, QRadar AQL. Organized by use case (authentication failures, config changes, interface events, ACL denies, VPN events, anomalous traffic patterns).

**Skill 3: incident-response-network**
- `skills/incident-response-network/SKILL.md` — Network forensics during security incidents: traffic analysis, lateral movement detection, containment verification, evidence preservation. Procedure shape: event-driven lifecycle (evidence preservation → initial triage → lateral movement detection → containment verification → timeline reconstruction → post-incident documentation). Scope is network evidence only (per R026 — not general IR or endpoint forensics).
- `skills/incident-response-network/references/cli-reference.md` — Packet capture, flow export, log collection commands per vendor ([Cisco]/[JunOS]/[EOS] — network device forensic data collection).
- `skills/incident-response-network/references/forensics-workflow.md` — Evidence collection methodology, chain-of-custody documentation patterns, network artifact types (packet captures, NetFlow/sFlow/IPFIX, ARP/MAC/CAM tables, routing table snapshots, syslog), timeline reconstruction approach.

**Existing files to update:**
- `README.md` — Add 3 new rows under the existing "Security Skills" separator row (line 41). Current last security row is line 48 (nist-compliance-assessment). New rows go after line 48.

### Build Order

1. **vulnerability-assessment** — Most structured, no novel elements. Closest to existing threshold-comparison pattern from M001 device health skills (CVSS scores map to severity thresholds). Proves the slice quickly.
2. **siem-log-analysis** — Retires the M002 #3 key risk (SIEM vendor fragmentation). The `[Splunk]`/`[ELK]`/`[QRadar]` labeling convention is new but follows the same approach as M001's `[Cisco]`/`[JunOS]`/`[EOS]` labels.
3. **incident-response-network** — Reuses event-driven lifecycle from change-verification skill. Scope is deliberately narrow (network forensics only, not general IR per R026 notes). Last because it's the most prose-heavy (forensic methodology) and can reference concepts from skills 1 and 2.
4. **README + validation** — Add 3 catalog rows and run full validation confirming 22 skills pass with 0 errors.

### Verification Approach

Per-skill (same as S01/S02):
```bash
# 1. Convention validation — all 22 skills pass
bash scripts/validate.sh
# Expected: "Skills checked: 22" + "Result: PASS (0 errors)"

# 2. Body word count per new skill (≤2700)
awk 'BEGIN{c=0} /^---$/{c++; if(c==2){found=1; next}} found{print}' skills/vulnerability-assessment/SKILL.md | wc -w
awk 'BEGIN{c=0} /^---$/{c++; if(c==2){found=1; next}} found{print}' skills/siem-log-analysis/SKILL.md | wc -w
awk 'BEGIN{c=0} /^---$/{c++; if(c==2){found=1; next}} found{print}' skills/incident-response-network/SKILL.md | wc -w

# 3. Reference files — exactly 2 per skill
ls skills/vulnerability-assessment/references/
ls skills/siem-log-analysis/references/
ls skills/incident-response-network/references/

# 4. Vendor label verification
grep -c '\[Splunk\]\|\[ELK\]\|\[QRadar\]' skills/siem-log-analysis/SKILL.md  # expect ≥10
grep -c '\[Cisco\]\|\[JunOS\]\|\[EOS\]' skills/incident-response-network/SKILL.md  # expect ≥5

# 5. Content specificity
grep -c 'CVE\|CVSS\|NVD' skills/vulnerability-assessment/SKILL.md  # expect ≥5
grep -ci 'lateral movement\|packet capture\|netflow\|evidence' skills/incident-response-network/SKILL.md  # expect ≥5

# 6. README catalog
grep -c 'vulnerability-assessment\|siem-log-analysis\|incident-response-network' README.md  # expect 3

# 7. No M001/S01/S02 regression
bash scripts/validate.sh 2>&1 | grep -c 'ERROR:'  # expect 0
```

## Constraints

- All 3 skills are `metadata.safety: read-only` (D027). No containment actions, no device modifications. Incident response skill describes evidence *collection* and *analysis* procedures — containment verification checks are read-only (confirm ACLs applied, verify routing changes took effect), not containment *execution*.
- SIEM skill must not become generic "how to use Splunk" — the query patterns must be network-security-specific (firewall denies, auth failures, config changes, lateral movement indicators).
- Incident response scope is network forensics only (R026): packet captures, flow data, log correlation, lateral movement detection. NOT endpoint forensics, malware analysis, or full NIST 800-61 IR lifecycle (that's R038 in M003).
- NVD/CVE data is public domain — no copyright concern for the vulnerability-assessment skill referencing CVE IDs, CVSS scores, or NVD query approaches.
- Use K001 `awk` word count approach (not BSD `sed`) for body word counting on macOS.

## Common Pitfalls

- **SIEM skill becoming a Splunk tutorial** — The skill must provide network-security-focused query patterns, not general SIEM administration. Each query pattern should solve a specific security investigation question (e.g., "find all denied connections from a source IP in the last 24 hours") with `[Splunk]`/`[ELK]`/`[QRadar]` syntax variants.
- **Incident response scope creep** — R026 is "network forensics during incident response," not general IR. Avoid covering endpoint isolation, malware sandboxing, user account lockout, or organizational communication plans. Stay focused on: packet captures, flow records, ARP/MAC/CAM tables, routing table snapshots, syslog/SNMP trap analysis, and lateral movement detection via network evidence.
- **Vulnerability assessment becoming a patch management guide** — The skill should guide CVE triage and prioritization, not detailed patching procedures (which are vendor-specific and operational). Focus on: identify vulnerable versions → map to CVEs → score with CVSS → prioritize by risk × exposure → recommend remediation timeline.
- **"Threshold Tables" section mismatch** — Security ops skills don't always have clean threshold metrics. Follow the pattern from S01/S02: use this section for severity classification tables. Vulnerability assessment → CVSS severity tiers + remediation SLA mapping. SIEM → alert severity classification. Incident response → evidence priority classification.
