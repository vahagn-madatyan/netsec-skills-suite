# S01: Vendor-Specific Firewall Audit Skills

**Goal:** Deliver 4 vendor-specific firewall audit skills (PAN-OS, FortiGate, Check Point, Cisco ASA/FTD) that encode real vendor expertise — not generic security checklists — within the established SKILL.md template, with vendor-specific policy models and CLI references offloaded to `references/` subdirectories.

**Demo:** `bash scripts/validate.sh` passes with 16 skills (12 M001 + 4 new firewall). Each firewall skill contains vendor-specific policy evaluation flows. README catalog table shows 16 rows with a new "Security Skills" section header.

## Must-Haves

- 4 new skill directories: `skills/palo-alto-firewall-audit/`, `skills/fortigate-firewall-audit/`, `skills/checkpoint-firewall-audit/`, `skills/cisco-firewall-audit/`
- Each skill has `SKILL.md` with `metadata.safety: read-only` frontmatter, all 7 required H2 sections
- Each skill body ≤2700 words (measured by `wc -w` after stripping frontmatter)
- Each skill has `references/policy-model.md` and `references/cli-reference.md`
- PAN-OS skill encodes zone-based security profiles, App-ID, Content-ID chain — not generic firewall best practices
- FortiGate skill encodes VDOM segmentation, UTM profile binding, SD-WAN SLA evaluation
- Check Point skill encodes rulebase layers, blade activation, SmartConsole management plane
- Cisco skill encodes ASA security levels AND FTD Access Control Policy evaluation as dual-platform coverage
- Procedure shape: "policy audit" — systematic rule-by-rule analysis against best practices (per D028)
- README catalog updated with 4 new rows under a "Security Skills" section header

## Proof Level

- This slice proves: contract (validate.sh + word count + vendor content depth)
- Real runtime required: no
- Human/UAT required: yes — spot-check that firewall skills encode real vendor expertise

## Verification

- `bash scripts/validate.sh` exits 0 and reports "Skills checked: 16"
- `for skill in palo-alto-firewall-audit fortigate-firewall-audit checkpoint-firewall-audit cisco-firewall-audit; do body_words=$(sed '1,/^---$/d' "skills/$skill/SKILL.md" | sed '1,/^---$/d' | wc -w); echo "$skill: $body_words"; [ "$body_words" -le 2700 ] || echo "FAIL: over word budget"; done`
- `grep -c 'firewall-audit' README.md` returns 4
- `grep -l 'zone\|App-ID\|Content-ID' skills/palo-alto-firewall-audit/SKILL.md` confirms vendor specificity
- `grep -l 'VDOM\|UTM' skills/fortigate-firewall-audit/SKILL.md` confirms vendor specificity
- `grep -l 'rulebase layer\|blade' skills/checkpoint-firewall-audit/SKILL.md` confirms vendor specificity
- `grep -l 'security-level\|Access Control Policy\|FTD' skills/cisco-firewall-audit/SKILL.md` confirms vendor specificity
- `bash scripts/validate.sh 2>&1 | grep -c 'ERROR:'` returns 0 — confirms no failure diagnostics emitted

## Observability / Diagnostics

- **Validation surface:** `bash scripts/validate.sh` reports per-skill pass/fail with named error reasons (missing section, bad safety value, missing references/). Exit code 0 = all pass, 1 = any fail. Skill count in output confirms discovery.
- **Word budget inspection:** `sed '1,/^---$/d' skills/SKILLNAME/SKILL.md | sed '1,/^---$/d' | wc -w` — per-skill body word count. Must be ≤2700.
- **Vendor specificity check:** `grep -l 'VENDOR_TERM' skills/SKILLNAME/SKILL.md` — confirms vendor-specific content is present, not generic firewall boilerplate.
- **Failure state visibility:** validate.sh prints `ERROR: <reason>` lines to stderr for each failed check, making failure diagnosis immediate. The error count is summarized at the end.
- **Redaction:** No secrets or credentials in skill files. All CLI commands are read-only `show`/`get`/`diagnose` — no configuration-modifying commands.

## Integration Closure

- Upstream surfaces consumed: M001 SKILL.md template (frontmatter schema + 7 H2 sections), `scripts/validate.sh`, `references/` subdirectory convention, README catalog table format
- New wiring introduced in this slice: 4 new `skills/*/` directories discovered by validate.sh and `npx skills add . --list`
- What remains before the milestone is truly usable end-to-end: S02 (compliance), S03 (security operations), S04 (remaining security skills + final assembly reaching 25 total)

## Tasks

- [x] **T01: Author PAN-OS firewall audit skill with policy-model and CLI references** `est:1h`
  - Why: PAN-OS is the most complex vendor policy model (zone-based profiles, App-ID/Content-ID/URL-ID chain, Security Profile Groups). Building it first retires the key risk — if PAN-OS fits within ~2700 words with overflow to `references/`, the other three vendors will too. Covers R017.
  - Files: `skills/palo-alto-firewall-audit/SKILL.md`, `skills/palo-alto-firewall-audit/references/policy-model.md`, `skills/palo-alto-firewall-audit/references/cli-reference.md`
  - Do: Create `skills/palo-alto-firewall-audit/` directory with SKILL.md following the established template (see `skills/bgp-analysis/SKILL.md` for format). Frontmatter must have `name: palo-alto-firewall-audit`, `metadata.safety: read-only`. Body must contain all 7 required H2 sections: "When to Use", "Prerequisites", "Procedure", "Threshold Tables", "Decision Trees", "Report Template", "Troubleshooting". Procedure must use "policy audit" shape (D028): systematic rule-by-rule analysis. Encode PAN-OS specifics: zone-based architecture, security policy evaluation order (intrazone → interzone → universal), App-ID flow (L4 session → App-ID → Content-ID → URL-ID), Security Profile Groups (AV, AS, VP, URL, FB, WF, DP), Zone Protection Profiles, DoS Protection. CLI reference file should use `show` and `set`/`test` read-only commands (PA-OS `show running security`, `show running zone`, `test security-policy-match`). Policy model reference should document the evaluation chain.
  - Verify: `bash scripts/validate.sh` passes with skill counted; `wc -w` body ≤2700; `grep -l 'App-ID\|Content-ID\|zone' skills/palo-alto-firewall-audit/SKILL.md` finds matches
  - Done when: `skills/palo-alto-firewall-audit/` exists with SKILL.md (≤2700 body words, valid frontmatter, all 7 sections) + 2 reference files, passes validate.sh, contains PAN-OS-specific policy evaluation content

- [x] **T02: Author FortiGate firewall audit skill with VDOM/UTM model and CLI references** `est:1h`
  - Why: FortiGate is the second largest firewall vendor with a fundamentally different architecture (VDOM segmentation, UTM profiles, FortiGuard integration, SD-WAN SLA). Confirms the pattern established by T01 transfers to a different vendor model. Covers R018.
  - Files: `skills/fortigate-firewall-audit/SKILL.md`, `skills/fortigate-firewall-audit/references/policy-model.md`, `skills/fortigate-firewall-audit/references/cli-reference.md`
  - Do: Create `skills/fortigate-firewall-audit/` directory. Follow same template as T01's PAN-OS skill but with FortiOS-specific content. Encode: VDOM architecture (root VDOM, management VDOM, inter-VDOM links), FortiOS policy evaluation (interface-pair policy lookup, policy ID ordering, implicit deny), UTM profile types (antivirus, web-filter, application-control, IPS, email-filter, DLP), FortiGuard service validation, SD-WAN SLA monitoring and rule-based traffic steering security implications. CLI reference should use FortiOS `diagnose` and `get`/`show` commands (`get firewall policy`, `diagnose sys session list`, `get system status`). Policy model reference should document VDOM segmentation and UTM inspection chain.
  - Verify: `bash scripts/validate.sh` passes; `wc -w` body ≤2700; `grep -l 'VDOM\|UTM' skills/fortigate-firewall-audit/SKILL.md` finds matches
  - Done when: `skills/fortigate-firewall-audit/` exists with SKILL.md (≤2700 body words, valid frontmatter, all 7 sections) + 2 reference files, passes validate.sh, contains FortiOS-specific content

- [x] **T03: Author Check Point and Cisco ASA/FTD firewall audit skills** `est:1h30m`
  - Why: Completes the four-vendor firewall coverage. Check Point (rulebase layers, blades, SmartConsole) and Cisco ASA/FTD (dual-platform: ASA security levels + FTD Access Control Policy) are the remaining two vendors. Both follow the proven pattern from T01–T02. Covers R019 and R020.
  - Files: `skills/checkpoint-firewall-audit/SKILL.md`, `skills/checkpoint-firewall-audit/references/policy-model.md`, `skills/checkpoint-firewall-audit/references/cli-reference.md`, `skills/cisco-firewall-audit/SKILL.md`, `skills/cisco-firewall-audit/references/policy-model.md`, `skills/cisco-firewall-audit/references/cli-reference.md`
  - Do: Create both skill directories following the established pattern.
    **Check Point:** Encode R80+ management architecture (SmartConsole → Management Server → Security Gateway), Unified Policy with ordered/inline layers, blade activation model (Firewall, IPS, App Control, URL Filtering, Anti-Bot, Threat Emulation, Content Awareness), NAT policy (automatic vs manual rules), identity awareness integration, SmartEvent/SmartLog analysis. CLI reference uses `fw`, `cpstat`, `cpview`, and `clish` commands.
    **Cisco ASA/FTD:** Encode dual-platform coverage — ASA classic (interface security-level evaluation, ACL-based filtering, NAT order of operations, MPF: class-map → policy-map → service-policy) AND FTD managed by FMC (Access Control Policy evaluation: Prefilter → SSL → Access → Intrusion → File/Malware, Snort inspection engine integration). CLI reference covers ASA `show` commands AND FTD `system support` / FMC REST API queries.
  - Verify: `bash scripts/validate.sh` passes; both skills ≤2700 body words; vendor-specific grep checks pass for each
  - Done when: Both `skills/checkpoint-firewall-audit/` and `skills/cisco-firewall-audit/` exist with valid SKILL.md + 2 reference files each, pass validate.sh, contain vendor-specific policy evaluation content

- [x] **T04: Update README catalog with 4 firewall audit skills and run full 16-skill validation** `est:30m`
  - Why: Closes the slice by updating the user-facing catalog and performing comprehensive validation across all 16 skills. The README is the first thing users see (R004) — it must reflect the new security skills.
  - Files: `README.md`
  - Do: Add a "**Security Skills**" section header row to the README catalog table (after the existing 12 M001 skills). Add 4 new rows for the firewall audit skills with accurate descriptions and `read-only` safety tier. Descriptions must mention vendor-specific capabilities (e.g., "PAN-OS zone-based policy audit with App-ID/Content-ID analysis" not "firewall audit"). Run full validation suite: `bash scripts/validate.sh` (expect 16 skills, 0 errors), word count check on all 4 new skills, `npx skills add . --list` to verify discovery. Verify no M001 regression by confirming all 12 original skills still pass.
  - Verify: `bash scripts/validate.sh` reports "Skills checked: 16" with 0 errors; `grep -c 'firewall-audit' README.md` returns 4; `grep 'Security Skills' README.md` finds the section header
  - Done when: README has 16-row catalog table with "Security Skills" section, `bash scripts/validate.sh` passes all 16 skills, word budget verified for all 4 new skills

## Files Likely Touched

- `skills/palo-alto-firewall-audit/SKILL.md`
- `skills/palo-alto-firewall-audit/references/policy-model.md`
- `skills/palo-alto-firewall-audit/references/cli-reference.md`
- `skills/fortigate-firewall-audit/SKILL.md`
- `skills/fortigate-firewall-audit/references/policy-model.md`
- `skills/fortigate-firewall-audit/references/cli-reference.md`
- `skills/checkpoint-firewall-audit/SKILL.md`
- `skills/checkpoint-firewall-audit/references/policy-model.md`
- `skills/checkpoint-firewall-audit/references/cli-reference.md`
- `skills/cisco-firewall-audit/SKILL.md`
- `skills/cisco-firewall-audit/references/policy-model.md`
- `skills/cisco-firewall-audit/references/cli-reference.md`
- `README.md`
