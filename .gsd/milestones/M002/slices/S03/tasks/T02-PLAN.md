---
estimated_steps: 5
estimated_files: 3
---

# T02: Build siem-log-analysis skill with multi-platform query patterns

**Slice:** S03 — Security Operations Skills
**Milestone:** M002

## Description

Create the siem-log-analysis skill covering R025 (SIEM log analysis — syslog parsing, event correlation, alert triage, threat hunting queries). This skill retires the M002 key risk #3 (SIEM vendor fragmentation) by proving that `[Splunk]`/`[ELK]`/`[QRadar]` labeled query patterns with platform-independent diagnostic reasoning is genuinely useful — not generic log-reading advice.

The SIEM skill is structurally novel for this suite: instead of `[Cisco]`/`[JunOS]`/`[EOS]` network device labels, it uses `[Splunk]`/`[ELK]`/`[QRadar]` SIEM platform labels. The diagnostic reasoning (what to look for, how to correlate, what constitutes an anomaly) remains platform-independent. Only the query syntax (SPL vs KQL/Lucene vs AQL) diverges across platforms.

Critical constraint: this must NOT become a generic "how to use Splunk" tutorial. Every query pattern must solve a specific network-security investigation question (firewall denies, auth failures, config changes, interface events, VPN events, lateral movement indicators).

## Steps

1. **Create `skills/siem-log-analysis/references/cli-reference.md`** — Two sections:
   - SIEM platform access/management: `[Splunk]` search commands (| search, | stats, | timechart, | tstats), `[ELK]` Kibana/Discover access and Dev Tools console, `[QRadar]` Log Activity and Advanced Search access
   - Network device syslog configuration verification: `[Cisco]` `show logging`, `[JunOS]` `show system syslog`, `[EOS]` `show logging`, `[PAN-OS]` `show log-interface-setting`, `[FortiGate]` `diagnose log test` / `get log setting` — organized in table format. Include syslog facility/severity mapping (RFC 5424 levels 0-7) since all SIEM platforms parse these.

2. **Create `skills/siem-log-analysis/references/query-reference.md`** — Side-by-side query patterns organized by security use case. For each use case, show `[Splunk]` SPL, `[ELK]` KQL, and `[QRadar]` AQL syntax. Use cases to cover:
   - Authentication failures (failed login attempts by source IP)
   - Configuration changes (config modification events)
   - Firewall/ACL denies (blocked connections by source/destination)
   - Interface state changes (link up/down events)
   - VPN tunnel events (tunnel establishment/teardown)
   - Anomalous traffic patterns (unusual volume, new destinations)
   - Lateral movement indicators (internal-to-internal connections on unusual ports)
   Each use case: 3 query variants + brief explanation of what the query returns. Target ~600-800 words total for the reference file.

3. **Create `skills/siem-log-analysis/SKILL.md`** — Full skill file with:
   - YAML frontmatter: name `siem-log-analysis`, description (network security SIEM analysis focus), license Apache-2.0, metadata.safety: read-only
   - Intro paragraph: this skill guides network-security-focused log analysis across SIEM platforms — not general SIEM administration. The diagnostic reasoning is platform-independent; query syntax uses `[Splunk]`/`[ELK]`/`[QRadar]` labels.
   - **When to Use**: security incident investigation, threat hunting, alert triage, compliance log review, anomalous behavior detection, post-incident timeline construction
   - **Prerequisites**: SIEM platform access with search privileges, network device syslog forwarding configured, familiarity with network device log formats
   - **Procedure**: 6-step forensic timeline shape: (1) Verify syslog sources — confirm network devices are forwarding with vendor-labeled commands, (2) Normalize events — identify source types, parse fields, map to common taxonomy, (3) Correlate across sources — join events from multiple devices by timestamp/IP/session, (4) Build timeline — chronologically sequence correlated events, (5) Identify anomalies — compare against baselines using `[Splunk]`/`[ELK]`/`[QRadar]` statistical queries, (6) Triage and classify — severity assignment, false positive elimination, escalation decision
   - **Threshold Tables**: Alert severity classification (Critical/High/Medium/Low/Info), event volume anomaly thresholds (>2σ from baseline), correlation confidence scoring
   - **Decision Trees**: Alert triage flow (true positive → investigate → IR engagement vs false positive → tune rule vs informational → document trend)
   - **Report Template**: investigation summary, timeline of events, affected devices, query evidence, severity classification, recommendations
   - **Troubleshooting**: missing log sources, time synchronization issues, log parsing failures, query performance problems, incomplete correlation
   - Each inline query example in the Procedure must use the `[Splunk]`/`[ELK]`/`[QRadar]` label convention with platform-specific syntax. Target ≥10 SIEM platform label instances in the SKILL.md body.
   - Target ≤2700 body words. Offload detailed query syntax to references/query-reference.md.

4. **Verify the skill passes validation** — Run `bash scripts/validate.sh` and confirm 21 skills, 0 errors. Check body word count ≤2700 via K001 `awk` method. Verify `grep -c '\[Splunk\]\|\[ELK\]\|\[QRadar\]' skills/siem-log-analysis/SKILL.md` returns ≥10. Confirm `ls skills/siem-log-analysis/references/` shows exactly 2 files.

5. **Fix any issues** — If word count exceeds 2700, move more query examples to query-reference.md and reference them from the SKILL.md body. If SIEM label count is <10, add more platform-specific query examples in the Procedure section.

## Must-Haves

- [ ] SKILL.md has `metadata.safety: read-only` in YAML frontmatter
- [ ] All 7 required H2 sections present
- [ ] Body word count ≤2700 (K001 `awk` method)
- [ ] `[Splunk]`/`[ELK]`/`[QRadar]` labels appear ≥10 times in SKILL.md
- [ ] Query patterns are network-security-specific, not generic SIEM administration
- [ ] `references/cli-reference.md` exists with SIEM access + network device syslog verification commands
- [ ] `references/query-reference.md` exists with side-by-side SPL/KQL/AQL patterns by use case
- [ ] `bash scripts/validate.sh` reports 21 skills, 0 errors

## Verification

- `bash scripts/validate.sh` exits 0, reports "Skills checked: 21" and "Result: PASS (0 errors)"
- `awk 'BEGIN{c=0} /^---$/{c++; if(c==2){found=1; next}} found{print}' skills/siem-log-analysis/SKILL.md | wc -w` returns ≤2700
- `ls skills/siem-log-analysis/references/` shows exactly `cli-reference.md` and `query-reference.md`
- `grep -c '\[Splunk\]\|\[ELK\]\|\[QRadar\]' skills/siem-log-analysis/SKILL.md` returns ≥10
- All 20 prior skills still pass validation (0 errors total)

## Inputs

- T01 completed: vulnerability-assessment skill is validated (20 skills total)
- Existing S01/S02 skills for structural reference — especially the `[Cisco]`/`[JunOS]`/`[EOS]` inline label convention which this skill mirrors with `[Splunk]`/`[ELK]`/`[QRadar]`
- D027 — read-only safety tier
- D028 — forensic timeline procedure shape
- K001 — use `awk` word count, not BSD `sed`

## Expected Output

- `skills/siem-log-analysis/SKILL.md` — Network-security SIEM analysis skill (~2200-2600 body words) with ≥10 SIEM vendor labels, platform-independent reasoning + platform-specific queries
- `skills/siem-log-analysis/references/cli-reference.md` — SIEM platform access commands + 5-vendor syslog config verification
- `skills/siem-log-analysis/references/query-reference.md` — Side-by-side SPL/KQL/AQL patterns for 7 network security use cases
- `bash scripts/validate.sh` reporting 21 skills, 0 errors
- M002 key risk #3 (SIEM vendor fragmentation) retired

## Observability Impact

**New signals:**
- `bash scripts/validate.sh` — skill count increments from 20 to 21; siem-log-analysis appears in per-skill OK/ERROR lines
- `grep -c '\[Splunk\]\|\[ELK\]\|\[QRadar\]' skills/siem-log-analysis/SKILL.md` — SIEM vendor label density (≥10 required); this is the key metric for SIEM vendor fragmentation risk retirement
- `awk` K001 word count on SKILL.md body — numeric signal for content scope control (≤2700)
- `ls skills/siem-log-analysis/references/` — structural completeness of reference files (exactly 2)

**Inspection surfaces:**
- `grep '^## ' skills/siem-log-analysis/SKILL.md` — H2 section headers confirm structural completeness
- `wc -l skills/siem-log-analysis/references/*.md` — non-trivial reference content (each file >20 lines)
- `grep 'safety' skills/siem-log-analysis/SKILL.md` — confirms read-only safety tier in frontmatter

**Failure visibility:**
- validate.sh prints `ERROR: siem-log-analysis` with specific failure reason if any structural check fails
- Word count >2700 is a numeric fail — no ambiguous pass/fail boundary
- SIEM label count <10 from `grep -c` is a numeric fail with clear remediation (add more platform-specific query examples)
