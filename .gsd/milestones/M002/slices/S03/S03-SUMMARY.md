---
id: S03
parent: M002
milestone: M002
provides:
  - vulnerability-assessment skill with CVE mapping, CVSS v3.1 scoring, and 5-vendor version retrieval
  - siem-log-analysis skill with [Splunk]/[ELK]/[QRadar] labeled query patterns and platform-independent diagnostic reasoning
  - incident-response-network skill with 6-step evidence-driven lifecycle, 3-vendor forensic commands, and read-only containment verification
  - M002 SIEM vendor fragmentation risk retired (key risk #3)
requires:
  - slice: S01
    provides: Proven security audit skill pattern (read-only analysis with structured findings), vendor CLI reference conventions, ~2700 word budget proven
affects:
  - S04
key_files:
  - skills/vulnerability-assessment/SKILL.md
  - skills/vulnerability-assessment/references/cli-reference.md
  - skills/vulnerability-assessment/references/vulnerability-reference.md
  - skills/siem-log-analysis/SKILL.md
  - skills/siem-log-analysis/references/cli-reference.md
  - skills/siem-log-analysis/references/query-reference.md
  - skills/incident-response-network/SKILL.md
  - skills/incident-response-network/references/cli-reference.md
  - skills/incident-response-network/references/forensics-workflow.md
  - README.md
key_decisions:
  - D029 — [Splunk]/[ELK]/[QRadar] inline labels mirror device vendor convention; platform-independent reasoning with platform-specific query syntax
  - D030 — IR skill scoped to read-only containment verification (check ACLs/routes, never execute changes); evidence ordered by volatility
patterns_established:
  - SIEM multi-platform labeling — [Splunk]/[ELK]/[QRadar] inline labels with full side-by-side query tables in references/query-reference.md
  - Forensic evidence lifecycle procedure — preserve → triage → detect → verify → reconstruct → document (adapts D028 event-driven lifecycle to forensic phases)
  - Vulnerability threshold-comparison — CVSS scores as thresholds mapping to severity tiers and remediation SLAs (extends D028)
  - cli-reference.md dual-purpose pattern (SIEM) — covers both SIEM platform access commands AND network device syslog verification since syslog forwarding is a SIEM prerequisite
observability_surfaces:
  - bash scripts/validate.sh — 22 skills, 0 errors
  - awk K001 word count — 2446 / 2682 / 2698 (all ≤2700)
  - grep -c '[Splunk]|[ELK]|[QRadar]' siem-log-analysis/SKILL.md — 24 (≥10 required)
  - grep -c 'CVE|CVSS|NVD' vulnerability-assessment/SKILL.md — 79 (≥5 required)
  - grep -ci forensic terms incident-response-network/SKILL.md — 61 (≥5 required)
  - grep -c new skills in README.md — 3
drill_down_paths:
  - .gsd/milestones/M002/slices/S03/tasks/T01-SUMMARY.md
  - .gsd/milestones/M002/slices/S03/tasks/T02-SUMMARY.md
  - .gsd/milestones/M002/slices/S03/tasks/T03-SUMMARY.md
  - .gsd/milestones/M002/slices/S03/tasks/T04-SUMMARY.md
duration: 59m
verification_result: passed
completed_at: 2026-03-17
---

# S03: Security Operations Skills

**Delivered 3 security operations skills (vulnerability-assessment, siem-log-analysis, incident-response-network) bringing the suite to 22 validated skills and retiring M002's SIEM vendor fragmentation risk**

## What Happened

Built three security operations skills in four tasks, each following the proven S01/S02 patterns with security-domain-specific procedure shapes.

**T01: vulnerability-assessment** — Created a CVE assessment skill using the threshold-comparison pattern from M001 device health skills. CVSS v3.1 scores map to severity tiers and remediation SLAs. The 6-step procedure covers version inventory across 5 vendors ([Cisco]/[JunOS]/[EOS]/[PAN-OS]/[FortiGate]), CPE construction for NVD queries, combined risk classification (severity × exposure × exploitability), and prioritized remediation planning. Reference files provide vendor CLI commands for version/patch retrieval and a complete CVSS v3.1 breakdown with vendor advisory portal URLs. Body: 2446 words.

**T02: siem-log-analysis** — Created a multi-platform SIEM skill that retires M002 key risk #3 (SIEM vendor fragmentation). The key innovation is the [Splunk]/[ELK]/[QRadar] inline labeling convention (D029) — mirroring the device vendor pattern — where diagnostic reasoning stays platform-independent and only query syntax diverges. The skill covers 7 network-security-specific use cases (auth failures, config changes, firewall denies, interface events, VPN tunnels, anomalous traffic, lateral movement) with SPL/KQL/AQL patterns. Full side-by-side query tables offloaded to references/query-reference.md. The cli-reference.md uniquely serves dual purpose: SIEM platform access commands plus network device syslog verification (since syslog forwarding is a SIEM prerequisite). Body: 2682 words.

**T03: incident-response-network** — Created a network forensics skill scoped deliberately narrow: network evidence only (packet captures, flow data, ARP/MAC/CAM, routing snapshots) — NOT general IR, endpoint forensics, or malware analysis. The 6-step evidence-driven lifecycle (preserve → triage → detect → verify → reconstruct → document) adapts D028's event-driven lifecycle to forensic phases. Containment verification is strictly read-only per D027/D030: check ACL counters, confirm null routes, verify VLAN isolation — never execute containment. Evidence collection ordered by volatility (ARP/MAC first, configs last). Body: 2698 words.

**T04: README catalog update** — Added 3 catalog rows to README.md and ran the full verification battery confirming all 22 skills pass with 0 errors.

All three skills required minor word count trimming (Troubleshooting section tightening) — a proven technique from S01/S02 that consistently recovers 20–40 words without losing diagnostic value.

## Verification

Full slice verification battery (11 checks) passed:

| Check | Result |
|-------|--------|
| `bash scripts/validate.sh` | 22 skills, 0 errors, EXIT_CODE=0 |
| vulnerability-assessment word count | 2446 ≤ 2700 ✅ |
| siem-log-analysis word count | 2682 ≤ 2700 ✅ |
| incident-response-network word count | 2698 ≤ 2700 ✅ |
| Reference files (2 per skill) | 6 files confirmed ✅ |
| SIEM vendor labels ([Splunk]/[ELK]/[QRadar]) | 24 ≥ 10 ✅ |
| CVE/CVSS/NVD terms | 79 ≥ 5 ✅ |
| IR forensic terms | 61 ≥ 5 ✅ |
| README catalog rows | 3 ✅ |
| ERROR/WARNING count | 0 ✅ |
| M001/S01/S02 regression | 0 errors ✅ |

## Requirements Advanced

- R024 — CVE assessment skill built with 5-vendor version-to-CVE mapping, CVSS v3.1 scoring, and SLA-driven remediation prioritization
- R025 — SIEM log analysis skill built with 24 [Splunk]/[ELK]/[QRadar] labels across 7 network-security use cases
- R026 — Network forensics IR skill built with evidence-driven lifecycle, 3-vendor forensic commands, and read-only containment verification

## Requirements Validated

- R024 — skills/vulnerability-assessment/SKILL.md passes validate.sh (0 errors), body 2446 words, 79 CVE/CVSS/NVD occurrences, 5-vendor version retrieval, CVSS v3.1 scoring with severity-to-SLA mapping
- R025 — skills/siem-log-analysis/SKILL.md passes validate.sh (0 errors), body 2682 words, 24 SIEM vendor labels, 7 network-security-specific use cases, M002 SIEM vendor fragmentation risk retired
- R026 — skills/incident-response-network/SKILL.md passes validate.sh (0 errors), body 2698 words, 61 forensic terms, 21 vendor labels, 6-step evidence lifecycle, network-only scope confirmed

## New Requirements Surfaced

- none

## Requirements Invalidated or Re-scoped

- none

## Deviations

None. All four tasks executed as planned. Word count trimming (2707→2698 for IR, 2721→2682 for SIEM) was anticipated in task plans and followed the proven Troubleshooting trim approach.

## Known Limitations

- SIEM skill covers SPL/KQL/AQL only — other platforms (Sentinel, Chronicle, LogRhythm) would need additional labels
- Vulnerability assessment references NVD API v2 methods — API changes would need reference file updates
- IR skill covers Cisco/JunOS/EOS only — firewall vendor forensic commands (PAN-OS, FortiGate) not included in this skill's scope

## Follow-ups

- S04 can reuse the forensic timeline procedure shape from incident-response-network for wireless security rogue AP investigation workflows (per boundary map S03→S04)
- S04 README finalization should update the catalog row count in any README summary text

## Files Created/Modified

- `skills/vulnerability-assessment/SKILL.md` — CVE assessment skill (2446 body words) with 5-vendor version mapping, CVSS scoring, remediation prioritization
- `skills/vulnerability-assessment/references/cli-reference.md` — Version/patch retrieval CLI commands for 5 vendors with CPE construction
- `skills/vulnerability-assessment/references/vulnerability-reference.md` — CVSS v3.1 breakdown, NVD API queries, severity-to-SLA mapping, vendor advisory sources
- `skills/siem-log-analysis/SKILL.md` — SIEM log analysis skill (2682 body words) with [Splunk]/[ELK]/[QRadar] labels, 7 network-security use cases
- `skills/siem-log-analysis/references/cli-reference.md` — SIEM platform access + 5-vendor syslog verification commands
- `skills/siem-log-analysis/references/query-reference.md` — Side-by-side SPL/KQL/AQL patterns for 7 use cases
- `skills/incident-response-network/SKILL.md` — Network forensics IR skill (2698 body words) with evidence lifecycle, lateral movement detection
- `skills/incident-response-network/references/cli-reference.md` — Forensic data collection commands for 6 evidence types across 3 vendors
- `skills/incident-response-network/references/forensics-workflow.md` — Evidence methodology, chain-of-custody template, timeline reconstruction
- `README.md` — Added 3 catalog rows for S03 skills under Security Skills section

## Forward Intelligence

### What the next slice should know
- S03 skills collectively prove that the security audit pattern (read-only analysis → structured findings → vendor-labeled commands) works for three very different domains: vulnerability management, SIEM operations, and incident response. S04's VPN/zero-trust/wireless skills can follow the same shape.
- The [Splunk]/[ELK]/[QRadar] labeling convention (D029) is a clean abstraction — if S04 wireless security needs SIEM correlation, it can reference the siem-log-analysis skill rather than duplicating query patterns.
- The forensics-workflow.md reference file establishes a chain-of-custody and timeline reconstruction methodology that S04's wireless security skill can adapt for rogue AP investigation.

### What's fragile
- Word counts are tight: siem-log-analysis at 2682 and incident-response-network at 2698 leave only 18–2 words of headroom. Any additions to these skills require compensating cuts.
- The vulnerability-reference.md mentions NVD API v2 specifics — if NVD changes their API, the reference file needs updating (but the skill procedure stays stable since it describes the reasoning, not the API).

### Authoritative diagnostics
- `bash scripts/validate.sh` — the single source of truth for structural validity across all 22 skills. Returns per-skill OK/ERROR lines with specific failure reasons.
- `awk 'BEGIN{c=0} /^---$/{c++; if(c==2){found=1; next}} found{print}' skills/<name>/SKILL.md | wc -w` — authoritative body word count per K001.

### What assumptions changed
- No assumptions changed. The ~2700 word budget, 2-reference-file pattern, and security audit procedure shape all worked exactly as proven in S01/S02. SIEM vendor fragmentation risk (M002 key risk #3) was successfully retired — the inline label pattern scales from device vendors to SIEM platforms.