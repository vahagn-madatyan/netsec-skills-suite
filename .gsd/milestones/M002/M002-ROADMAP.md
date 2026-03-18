# M002: Security Skills

**Vision:** Deliver 13 security-focused skills covering multi-vendor firewall auditing, compliance frameworks, vulnerability management, SIEM integration, incident response, VPN troubleshooting, zero-trust assessment, and wireless security — complementing M001's network skills to create a comprehensive network + security suite installable via `npx skills add`.

## Success Criteria

- All 13 security SKILL.md files pass `bash scripts/validate.sh` with 0 errors
- `npx skills add . --list` discovers all 25 skills (12 M001 + 13 M002)
- Firewall audit skills encode vendor-specific policy analysis (PAN-OS zone-based security profiles, FortiOS VDOM/UTM, Check Point rulebase layers/blades, Cisco ASA security levels vs FTD ACP evaluation) — not generic checklists
- Compliance skills reference actual CIS control IDs and NIST control families with network device mappings — not vague categories
- Each skill body stays within ≤2700 words with vendor-specific detail offloaded to `references/`
- README catalog table includes all 13 new skills with descriptions and safety tiers
- No regression — all 12 M001 skills continue to pass validation unchanged

## Key Risks / Unknowns

- **Vendor-specific firewall depth vs word budget** — Four completely different vendor policy models (PAN-OS zone/profile chain, FortiOS VDOM/UTM, Check Point layers/blades, ASA/FTD dual-platform) must each encode real vendor expertise within ~2700 words. If PAN-OS (the most complex) doesn't fit, the template needs rethinking.
- **CIS copyright-safe reference approach** — CIS benchmarks are commercially licensed. The `control-reference.md` strategy (cite control IDs and categories, describe audit checks independently) must be proven to be both copyright-safe and genuinely useful.
- **SIEM vendor fragmentation** — Making a vendor-agnostic SIEM skill useful across Splunk, ELK, and QRadar requires careful abstraction without becoming generic log-reading advice.

## Proof Strategy

- **Vendor depth vs word budget** → retire in S01 by building the Palo Alto firewall audit skill first (most complex policy model). If PAN-OS fits within ~2700 words with overflow to `references/policy-model.md`, the other three vendors will too.
- **CIS copyright approach** → retire in S02 by building the CIS benchmark audit skill with `references/control-reference.md` that cites control IDs/categories without reproducing benchmark text. Proven when the skill provides actionable audit guidance using only public-domain descriptions of what to check.
- **SIEM abstraction** → retire in S03 by building the SIEM log analysis skill with `[Splunk]`/`[ELK]`/`[QRadar]` labeled query patterns. Proven when the skill provides platform-specific syntax examples with platform-independent diagnostic reasoning.

## Verification Classes

- Contract verification: `bash scripts/validate.sh` (safety tier, 7 H2 sections, references/ directory) + `wc -w` body ≤2700 per skill + `npx skills add . --list` discovers 25 skills
- Integration verification: Full suite (M001 + M002) installs without conflicts; no M001 skill regression
- Operational verification: none (static content files, no runtime)
- UAT / human verification: Spot-check that firewall skills encode real vendor expertise (not generic checklists) and compliance skills reference actual control IDs (not vague categories)

## Milestone Definition of Done

This milestone is complete only when all are true:

- All 13 security SKILL.md files pass `bash scripts/validate.sh` with 0 errors
- All 13 skills have `metadata.safety: read-only` in frontmatter
- Each skill has a `references/` subdirectory with exactly 2 reference files
- Each skill body is ≤2700 words (measured by `wc -w` after stripping frontmatter)
- `npx skills add . --list` returns "Found 25 skills" (12 M001 + 13 M002)
- README catalog table has 25 rows total with a "Security Skills" section
- All 12 M001 skills continue to pass validation unchanged
- Firewall skills contain vendor-specific policy evaluation flows, not generic security checklists
- Compliance skills cite CIS control IDs / NIST control families with concrete network device audit mappings
- Success criteria are re-checked against actual repo state, not just authoring assumptions

## Requirement Coverage

- Covers: R017, R018, R019, R020, R021, R022, R023, R024, R025, R026, R027, R028, R029
- Partially covers: none
- Leaves for later: R030–R038 (M003), R039–R041 (deferred), R042–R043 (out-of-scope)
- Orphan risks: none — all 13 active M002 requirements mapped to slices

## Slices

- [x] **S01: Vendor-Specific Firewall Audit Skills** `risk:high` `depends:[]`
  > After this: `bash scripts/validate.sh` passes 16 skills (12 M001 + 4 new firewall), each firewall skill encodes vendor-specific policy analysis with `references/policy-model.md` and `references/cli-reference.md`, README catalog updated with 4 new rows
- [x] **S02: Rule Analysis & Compliance Skills** `risk:medium` `depends:[S01]`
  > After this: `bash scripts/validate.sh` passes 19 skills, ACL rule analysis skill detects shadowed/overly permissive rules, CIS benchmark skill references actual control IDs in `references/control-reference.md` without reproducing copyrighted text, NIST skill maps network security to CSF Protect/Detect functions, README catalog updated with 3 new rows
- [x] **S03: Security Operations Skills** `risk:medium` `depends:[S01]`
  > After this: `bash scripts/validate.sh` passes 22 skills, CVE assessment skill maps versions to CVEs and prioritizes patches, SIEM skill uses `[Splunk]`/`[ELK]`/`[QRadar]` labeled query patterns, incident response skill focuses on network forensics evidence (not general IR), README catalog updated with 3 new rows
- [ ] **S04: Additional Security Skills & Suite Finalization** `risk:low` `depends:[S01]`
  > After this: `bash scripts/validate.sh` passes 25 skills, `npx skills add . --list` discovers all 25, VPN/IPSec skill reuses FSM pattern from M001, zero-trust skill introduces maturity scoring rubric, README catalog complete with all 13 M002 skills and "Security Skills" section header

## Boundary Map

### S01 → S02

Produces:
- Proven policy audit procedure shape (systematic rule-by-rule analysis against best practices) reusable by ACL rule analysis skill
- Vendor-specific firewall CLI reference pattern (`references/cli-reference.md` per vendor) that S02 compliance skills can cross-reference
- Demonstrated that ~2700 word budget works for security audit skills with vendor detail offloaded to `references/policy-model.md`

Consumes:
- M001 foundation: SKILL.md template, `scripts/validate.sh`, CI pipeline, `references/` subdirectory convention

### S01 → S03

Produces:
- Firewall vendor context (policy models, CLI patterns) that incident response and SIEM skills can reference when discussing firewall log analysis and security event correlation

Consumes:
- M001 foundation: SKILL.md template, `scripts/validate.sh`, CI pipeline

### S01 → S04

Produces:
- Security audit skill pattern (read-only analysis with structured findings) reusable by VPN, zero-trust, and wireless audit skills

Consumes:
- M001 foundation: SKILL.md template, `scripts/validate.sh`, CI pipeline

### S02 → S04

Produces:
- Compliance reference file pattern (`references/control-reference.md`) that wireless security skill can reference for 802.1X compliance mapping
- Scoring/severity classification pattern in "Threshold Tables" section reusable by zero-trust maturity scoring

Consumes:
- S01 proven word budget and procedure shape patterns

### S03 → S04

Produces:
- Forensic timeline procedure shape that wireless security audit can adapt for rogue AP investigation workflows

Consumes:
- S01 proven security audit skill patterns
