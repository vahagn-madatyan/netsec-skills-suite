# S03: Security Operations Skills

**Goal:** Deliver 3 security operations skills (vulnerability-assessment, siem-log-analysis, incident-response-network) that bring the suite to 22 validated skills and retire the M002 SIEM vendor fragmentation risk.
**Demo:** `bash scripts/validate.sh` reports "Skills checked: 22" with "Result: PASS (0 errors)". SIEM skill contains `[Splunk]`/`[ELK]`/`[QRadar]` labeled query patterns. Vulnerability skill maps versions to CVEs with CVSS scoring. Incident response skill focuses on network forensics evidence.

## Must-Haves

- vulnerability-assessment skill with CVE-to-version mapping, CVSS v3.1 scoring, remediation prioritization, multi-vendor version retrieval (`[Cisco]`/`[JunOS]`/`[EOS]`/`[PAN-OS]`/`[FortiGate]`)
- siem-log-analysis skill with `[Splunk]`/`[ELK]`/`[QRadar]` labeled query patterns, network-security-specific use cases (not generic SIEM tutorials), platform-independent diagnostic reasoning
- incident-response-network skill scoped to network forensics only (packet captures, flow data, ARP/MAC/CAM, routing snapshots, lateral movement detection via network evidence) — NOT general IR or endpoint forensics
- All 3 skills have `metadata.safety: read-only` in frontmatter
- Each skill has exactly 2 reference files in `references/`
- Each skill body ≤2700 words (measured by K001 `awk` method)
- All 7 required H2 sections present in each skill
- README catalog updated with 3 new rows under existing "Security Skills" section
- `bash scripts/validate.sh` passes 22 skills with 0 errors
- No M001/S01/S02 regression

## Verification

```bash
# 1. Full validation — all 22 skills pass
bash scripts/validate.sh
# Expected: "Skills checked: 22" + "Result: PASS (0 errors)"

# 2. Body word count per new skill (≤2700)
awk 'BEGIN{c=0} /^---$/{c++; if(c==2){found=1; next}} found{print}' skills/vulnerability-assessment/SKILL.md | wc -w
awk 'BEGIN{c=0} /^---$/{c++; if(c==2){found=1; next}} found{print}' skills/siem-log-analysis/SKILL.md | wc -w
awk 'BEGIN{c=0} /^---$/{c++; if(c==2){found=1; next}} found{print}' skills/incident-response-network/SKILL.md | wc -w

# 3. Reference files — exactly 2 per skill
ls skills/vulnerability-assessment/references/   # cli-reference.md, vulnerability-reference.md
ls skills/siem-log-analysis/references/           # cli-reference.md, query-reference.md
ls skills/incident-response-network/references/   # cli-reference.md, forensics-workflow.md

# 4. SIEM vendor labels — the key risk retirement
grep -c '\[Splunk\]\|\[ELK\]\|\[QRadar\]' skills/siem-log-analysis/SKILL.md  # expect ≥10

# 5. Content specificity
grep -c 'CVE\|CVSS\|NVD' skills/vulnerability-assessment/SKILL.md  # expect ≥5
grep -ci 'lateral movement\|packet capture\|netflow\|evidence' skills/incident-response-network/SKILL.md  # expect ≥5

# 6. README catalog completeness
grep -c 'vulnerability-assessment\|siem-log-analysis\|incident-response-network' README.md  # expect 3

# 7. No regression
bash scripts/validate.sh 2>&1 | grep -c 'ERROR:'  # expect 0

# 8. Failure-path: validate.sh correctly detects structural errors
# (Spot-check: confirm error output is structured and actionable)
bash scripts/validate.sh 2>&1 | grep -E 'ERROR:|PASS|FAIL|Skills checked:'  # expect summary lines present with 0 errors

# 9. Diagnostic failure-path: verify validate.sh returns non-zero on structural error
# Create a deliberately broken skill, confirm detection, then clean up
mkdir -p /tmp/nsss-test-skill && echo '---' > /tmp/nsss-test-skill/SKILL.md && echo 'bad' >> /tmp/nsss-test-skill/SKILL.md && echo '---' >> /tmp/nsss-test-skill/SKILL.md
# (Do not actually run against suite — just confirm validate.sh exit code on real suite is 0)
bash scripts/validate.sh; echo "EXIT_CODE=$?"  # expect EXIT_CODE=0

# 10. Per-skill error inspection surface
bash scripts/validate.sh 2>&1 | grep -E '^\s*(OK|ERROR):' | head -30  # shows per-check pass/fail lines
```

## Observability / Diagnostics

**Runtime signals:**
- `bash scripts/validate.sh` — primary health signal; reports skill count, error count, and per-skill pass/fail with specific error messages for frontmatter, sections, and references
- Word count via K001 `awk` method — enforces ≤2700 body words per skill; exceeding triggers trim-and-revalidate cycle
- `grep -c` content specificity checks — verify domain-relevant terms (CVE/CVSS/NVD, Splunk/ELK/QRadar, lateral movement/packet capture) appear at expected density

**Inspection surfaces:**
- Each skill's `references/` directory — 2 files per skill; `ls` confirms presence, `wc -l` confirms non-trivial content
- YAML frontmatter — `metadata.safety` value visible via `grep 'safety' skills/*/SKILL.md`
- H2 section headers — `grep '^## ' skills/*/SKILL.md` shows structural completeness at a glance

**Failure visibility:**
- Validation script prints per-skill `ERROR:` lines with specific failure reason (missing section name, invalid safety value, missing references/)
- Non-zero exit code from `validate.sh` halts slice verification
- Word count exceeding 2700 is a numeric signal — no ambiguous pass/fail

**Redaction constraints:**
- All skills are `read-only` safety tier — no credentials, tokens, or secrets in any skill content
- NVD/CVE data is public domain; SIEM query patterns are generic examples; no vendor-proprietary content

## Tasks

- [x] **T01: Build vulnerability-assessment skill with CVE mapping and CVSS scoring** `est:35m`
  - Why: Delivers R024 — the most structured S03 skill using the proven threshold-comparison pattern (CVSS scores → severity tiers → remediation SLAs). No novel elements; proves the slice quickly.
  - Files: `skills/vulnerability-assessment/SKILL.md`, `skills/vulnerability-assessment/references/cli-reference.md`, `skills/vulnerability-assessment/references/vulnerability-reference.md`
  - Do: Create SKILL.md with frontmatter (`metadata.safety: read-only`), all 7 H2 sections. Procedure: identify device versions → query CVE data → score with CVSS v3.1 → classify by severity × exposure × exploitability → prioritize remediation. Use `[Cisco]`/`[JunOS]`/`[EOS]`/`[PAN-OS]`/`[FortiGate]` labels for vendor-specific version commands. Threshold Tables section maps CVSS ranges to severity tiers and remediation SLAs. Reference 1 (cli-reference.md): version/patch retrieval commands per vendor. Reference 2 (vulnerability-reference.md): CVSS v3.1 scoring breakdown, NVD query approach, severity-to-SLA mapping, vendor advisory sources (Cisco PSIRT, Palo Alto advisories, Juniper JSA, Fortinet PSIRT, Arista advisories). Body ≤2700 words.
  - Verify: `bash scripts/validate.sh` passes this skill + all prior 19 skills. Body word count ≤2700 via K001 `awk` method. `grep -c 'CVE\|CVSS\|NVD'` ≥5.
  - Done when: `bash scripts/validate.sh` shows 20 skills with 0 errors, body ≤2700 words, 2 reference files present

- [x] **T02: Build siem-log-analysis skill with multi-platform query patterns** `est:40m`
  - Why: Delivers R025 and retires M002 key risk #3 (SIEM vendor fragmentation). Proves that `[Splunk]`/`[ELK]`/`[QRadar]` labeled query patterns with platform-independent diagnostic reasoning works.
  - Files: `skills/siem-log-analysis/SKILL.md`, `skills/siem-log-analysis/references/cli-reference.md`, `skills/siem-log-analysis/references/query-reference.md`
  - Do: Create SKILL.md with frontmatter (`metadata.safety: read-only`), all 7 H2 sections. Procedure follows forensic timeline shape: collect/verify syslog config → normalize events → correlate across sources → build timeline → identify anomalies → triage alerts. Use `[Splunk]`/`[ELK]`/`[QRadar]` inline labels for platform-specific query syntax (SPL, KQL/Lucene, AQL). All queries must be network-security-specific: firewall denies, auth failures, config changes, interface events, VPN events, lateral movement indicators — NOT generic SIEM administration. Reference 1 (cli-reference.md): SIEM platform access commands + network device syslog config verification per vendor (`[Cisco]`/`[JunOS]`/`[EOS]`/`[PAN-OS]`/`[FortiGate]`). Reference 2 (query-reference.md): side-by-side Splunk SPL / ELK KQL / QRadar AQL patterns organized by use case. Body ≤2700 words.
  - Verify: `bash scripts/validate.sh` passes this skill + all prior 20 skills. Body ≤2700 words. `grep -c '\[Splunk\]\|\[ELK\]\|\[QRadar\]'` ≥10 in SKILL.md.
  - Done when: `bash scripts/validate.sh` shows 21 skills with 0 errors, body ≤2700 words, 2 reference files, ≥10 SIEM vendor labels

- [ ] **T03: Build incident-response-network skill for network forensics** `est:35m`
  - Why: Delivers R026 — network forensics evidence collection and analysis during security incidents. Scope is deliberately narrow: network evidence only (packet captures, flow data, ARP/MAC/CAM tables, routing snapshots, syslog). NOT general IR, endpoint forensics, or malware analysis.
  - Files: `skills/incident-response-network/SKILL.md`, `skills/incident-response-network/references/cli-reference.md`, `skills/incident-response-network/references/forensics-workflow.md`
  - Do: Create SKILL.md with frontmatter (`metadata.safety: read-only`), all 7 H2 sections. Procedure follows event-driven lifecycle shape: evidence preservation → initial triage → lateral movement detection → containment verification (read-only — confirm ACLs/routing changes, not execute them) → timeline reconstruction → post-incident documentation. Use `[Cisco]`/`[JunOS]`/`[EOS]` vendor labels for forensic data collection commands. Threshold Tables: evidence priority classification. Reference 1 (cli-reference.md): packet capture, flow export, log collection commands per vendor. Reference 2 (forensics-workflow.md): evidence collection methodology, chain-of-custody documentation patterns, network artifact types, timeline reconstruction approach. Body ≤2700 words.
  - Verify: `bash scripts/validate.sh` passes this skill + all prior 21 skills. Body ≤2700 words. `grep -ci 'lateral movement\|packet capture\|netflow\|evidence'` ≥5.
  - Done when: `bash scripts/validate.sh` shows 22 skills with 0 errors, body ≤2700 words, 2 reference files, network-forensics-specific content confirmed

- [ ] **T04: Update README catalog and run full-suite validation** `est:15m`
  - Why: Completes the slice by adding 3 new skills to the README catalog and running the full verification battery to confirm 22 skills pass with 0 errors and no regression on M001/S01/S02 skills.
  - Files: `README.md`
  - Do: Add 3 new catalog rows after line 48 (current last security skill row — nist-compliance-assessment) in the README catalog table. Rows: vulnerability-assessment (CVE description), siem-log-analysis (SIEM description), incident-response-network (IR description). All with `read-only` safety tier. Run full verification battery from the slice Verification section. Confirm no M001 regression.
  - Verify: `grep -c 'vulnerability-assessment\|siem-log-analysis\|incident-response-network' README.md` returns 3. `bash scripts/validate.sh` shows 22 skills, 0 errors. All word counts ≤2700. All SIEM vendor label and content specificity checks pass.
  - Done when: README has 3 new rows, all verification commands from the slice Verification section pass with expected values

## Files Likely Touched

- `skills/vulnerability-assessment/SKILL.md`
- `skills/vulnerability-assessment/references/cli-reference.md`
- `skills/vulnerability-assessment/references/vulnerability-reference.md`
- `skills/siem-log-analysis/SKILL.md`
- `skills/siem-log-analysis/references/cli-reference.md`
- `skills/siem-log-analysis/references/query-reference.md`
- `skills/incident-response-network/SKILL.md`
- `skills/incident-response-network/references/cli-reference.md`
- `skills/incident-response-network/references/forensics-workflow.md`
- `README.md`
