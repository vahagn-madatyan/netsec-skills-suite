---
estimated_steps: 5
estimated_files: 3
---

# T03: Build incident-response-network skill for network forensics

**Slice:** S03 — Security Operations Skills
**Milestone:** M002

## Description

Create the incident-response-network skill covering R026 (network forensics during incident response). This skill reuses the event-driven lifecycle procedure shape from M001's change-verification skill (before → during → after phases) narrowed to network forensics evidence.

Critical scope constraint: this is network forensics ONLY (per R026). Packet captures, flow data (NetFlow/sFlow/IPFIX), ARP/MAC/CAM tables, routing table snapshots, syslog/SNMP traps, and lateral movement detection via network evidence. NOT general IR (NIST 800-61 lifecycle — that's R038/M003), NOT endpoint forensics, NOT malware analysis, NOT organizational communication plans.

Containment verification steps are read-only (confirm ACLs applied, verify routing changes took effect) — not containment execution. This aligns with D027 (all M002 skills read-only).

## Steps

1. **Create `skills/incident-response-network/references/cli-reference.md`** — Network device forensic data collection commands organized by evidence type across 3 vendors (`[Cisco]`/`[JunOS]`/`[EOS]`). Evidence types to cover:
   - Packet capture: `[Cisco]` `monitor capture`, `[JunOS]` `monitor traffic`, `[EOS]` `bash tcpdump` / ERSPAN
   - Flow export verification: `[Cisco]` `show flow monitor`, `[JunOS]` `show services flow-monitoring`, `[EOS]` `show flow tracking`
   - ARP/MAC/CAM tables: `show arp`, `show mac address-table` variants per vendor
   - Routing table snapshots: `show ip route` / `show route` / `show ip route` per vendor
   - ACL hit counts (containment verification): `show access-list` hit counter variants
   - SNMP trap/syslog status: logging config verification per vendor
   Table format, organized by evidence category.

2. **Create `skills/incident-response-network/references/forensics-workflow.md`** — Evidence collection methodology covering:
   - Chain-of-custody documentation patterns (timestamp, collector, device, evidence type, hash/verification)
   - Network artifact types and their forensic value: packet captures (full content), NetFlow/sFlow/IPFIX (metadata), ARP/MAC/CAM (L2 mapping), routing tables (path analysis), syslog (event timeline), SNMP traps (state changes)
   - Evidence volatility ordering (most volatile first: ARP/MAC → routing state → flow data → configs → logs)
   - Timeline reconstruction approach: anchor events, correlation by timestamp/IP/session, gap identification
   - Evidence preservation commands (save to file, not just view — `show tech-support redirect`, `copy running-config`)

3. **Create `skills/incident-response-network/SKILL.md`** — Full skill file with:
   - YAML frontmatter: name `incident-response-network`, description (network forensics during security incidents), license Apache-2.0, metadata.safety: read-only
   - Intro paragraph: this skill guides network-specific evidence collection and analysis during security incidents — not general IR. Scope is network artifacts: packet captures, flow records, forwarding tables, routing state, and device logs. References forensics-workflow.md for methodology and cli-reference.md for collection commands.
   - **When to Use**: active security incident requiring network evidence, post-incident network forensics, lateral movement investigation, unauthorized access investigation, data exfiltration analysis, network-based containment verification
   - **Prerequisites**: device CLI access (read-only sufficient), flow collection infrastructure (NetFlow/sFlow/IPFIX), centralized logging, known-good baseline configs for comparison
   - **Procedure**: 6-step event-driven lifecycle: (1) Evidence preservation — capture volatile data first (ARP/MAC/CAM → routing state → flow data → configs) using vendor-labeled commands, (2) Initial triage — identify scope from log/flow data (affected devices, time window, involved IPs), (3) Lateral movement detection — trace internal-to-internal connections via flow records and MAC/ARP table changes with `[Cisco]`/`[JunOS]`/`[EOS]` commands, (4) Containment verification (read-only) — confirm ACL hit counts show blocked traffic, verify routing changes took effect, validate no bypass paths via routing table analysis, (5) Timeline reconstruction — build chronological sequence from syslog + flow data + routing changes + ARP/MAC transitions, (6) Post-incident documentation — evidence inventory, timeline summary, affected device list, recommendations
   - **Threshold Tables**: Evidence priority classification (Critical: active packet captures during incident, High: flow records from affected time window, Medium: routing/ARP table snapshots, Low: historical config archives)
   - **Decision Trees**: Evidence collection priority flow (active threat → capture live traffic first vs post-incident → start with logs/flow vs containment verification → check ACL counters + routing state)
   - **Report Template**: incident network evidence summary, evidence inventory with chain-of-custody, timeline of network events, lateral movement map (if detected), containment verification results, recommendations
   - **Troubleshooting**: insufficient flow data coverage, time synchronization gaps, evidence overwritten by log rotation, packet capture performance impact, incomplete ARP/MAC aging
   - Use `[Cisco]`/`[JunOS]`/`[EOS]` vendor labels. Target ≥5 vendor label instances.
   - Target ≤2700 body words. Offload detailed methodology to forensics-workflow.md.

4. **Verify the skill passes validation** — Run `bash scripts/validate.sh` and confirm 22 skills, 0 errors. Check body word count ≤2700 via K001 `awk` method. Verify `grep -ci 'lateral movement\|packet capture\|netflow\|evidence' skills/incident-response-network/SKILL.md` returns ≥5. Confirm `ls skills/incident-response-network/references/` shows exactly 2 files.

5. **Fix any issues** — If word count exceeds 2700, compress Report Template or Troubleshooting sections (proven trim targets). If vendor labels are sparse, add more `[Cisco]`/`[JunOS]`/`[EOS]` examples in the Procedure steps.

## Must-Haves

- [ ] SKILL.md has `metadata.safety: read-only` in YAML frontmatter
- [ ] All 7 required H2 sections present
- [ ] Body word count ≤2700 (K001 `awk` method)
- [ ] Scope is network forensics only — no endpoint forensics, malware analysis, or general IR lifecycle
- [ ] Containment verification steps are read-only (check counters/state, not execute changes)
- [ ] `[Cisco]`/`[JunOS]`/`[EOS]` vendor labels appear ≥5 times
- [ ] `references/cli-reference.md` exists with forensic data collection commands for 3 vendors
- [ ] `references/forensics-workflow.md` exists with evidence methodology, chain-of-custody, timeline reconstruction
- [ ] `grep -ci 'lateral movement\|packet capture\|netflow\|evidence'` returns ≥5
- [ ] `bash scripts/validate.sh` reports 22 skills, 0 errors

## Verification

- `bash scripts/validate.sh` exits 0, reports "Skills checked: 22" and "Result: PASS (0 errors)"
- `awk 'BEGIN{c=0} /^---$/{c++; if(c==2){found=1; next}} found{print}' skills/incident-response-network/SKILL.md | wc -w` returns ≤2700
- `ls skills/incident-response-network/references/` shows exactly `cli-reference.md` and `forensics-workflow.md`
- `grep -ci 'lateral movement\|packet capture\|netflow\|evidence' skills/incident-response-network/SKILL.md` returns ≥5
- `grep -c '\[Cisco\]\|\[JunOS\]\|\[EOS\]' skills/incident-response-network/SKILL.md` returns ≥5
- All 21 prior skills still pass validation (0 errors total)

## Inputs

- T01 + T02 completed: vulnerability-assessment and siem-log-analysis skills validated (21 skills total)
- M001 change-verification skill for event-driven lifecycle procedure shape reference
- Existing S01 firewall skills for vendor label convention reference
- D027 — read-only safety tier (containment verification = read-only checks, not execution)
- D028 — event-driven lifecycle (from M001) adapted for forensic phases
- K001 — use `awk` word count, not BSD `sed`

## Expected Output

- `skills/incident-response-network/SKILL.md` — Network forensics IR skill (~2200-2600 body words) with 3-vendor labels, evidence-driven lifecycle, lateral movement detection
- `skills/incident-response-network/references/cli-reference.md` — Packet capture, flow export, ARP/MAC/CAM, routing snapshot commands for Cisco/JunOS/EOS
- `skills/incident-response-network/references/forensics-workflow.md` — Evidence collection methodology, chain-of-custody, artifact types, timeline reconstruction
- `bash scripts/validate.sh` reporting 22 skills, 0 errors
