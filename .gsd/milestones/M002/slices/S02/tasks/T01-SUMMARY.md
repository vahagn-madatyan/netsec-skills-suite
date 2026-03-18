---
id: T01
parent: S02
milestone: M002
provides:
  - acl-rule-analysis skill (R021) with shadowed/permissive/unused/redundant rule detection
  - Multi-vendor inline label pattern extended to 6 vendors for security audit skills
key_files:
  - skills/acl-rule-analysis/SKILL.md
  - skills/acl-rule-analysis/references/cli-reference.md
  - skills/acl-rule-analysis/references/rule-patterns.md
key_decisions: []
patterns_established:
  - 6-vendor inline labels ([Cisco]/[JunOS]/[EOS]/[PAN-OS]/[FortiGate]/[CheckPoint]) for security audit skills covering both ACL and firewall policy platforms
  - "Rule analysis" procedure shape — collect → detect patterns → classify severity → recommend — reusable for future rule-focused skills
observability_surfaces:
  - "bash scripts/validate.sh" — reports acl-rule-analysis with all OK checks (17 skills total)
  - "awk body word count" — 2458 words (within 2700 limit)
  - "grep -c 'shadowed|permissive|unused|redundant' skills/acl-rule-analysis/SKILL.md" — confirms all 4 analysis categories present
duration: 12m
verification_result: passed
completed_at: 2026-03-16
blocker_discovered: false
---

# T01: Build vendor-agnostic ACL rule analysis skill with multi-vendor inline labels

**Created acl-rule-analysis skill with shadowed rule detection, overly permissive rule identification, unused rule discovery, redundant rule flagging, and rule ordering optimization across 6 vendor platforms.**

## What Happened

Created 3 files for the acl-rule-analysis skill following the established SKILL.md structure from S01 (palo-alto-firewall-audit) and multi-vendor inline labeling from M001 (bgp-analysis).

SKILL.md contains: frontmatter with `name: acl-rule-analysis`, `metadata.safety: read-only`, `license: Apache-2.0`; intro paragraph establishing vendor-agnostic scope; 7 required H2 sections. The Procedure section follows a 7-step "rule analysis" shape: collect rulebase → identify shadowed rules → detect overly permissive rules → find unused rules → identify redundant rules → rule ordering optimization → generate recommendations. Threshold Tables use "Rule Risk Severity Classification" with Critical/High/Medium/Low categories. Decision Trees cover remediation priority and rule reordering safety checks.

The cli-reference.md covers all 6 platforms (Cisco IOS, Cisco ASA, JunOS, EOS, PAN-OS, FortiGate, CheckPoint) with per-platform tables for rule retrieval and hit count commands, plus API equivalents for PAN-OS, FortiGate, and CheckPoint.

The rule-patterns.md provides detailed detection algorithms for shadowed rules (superset comparison), redundant rules (overlap detection), overly permissive patterns (enumerated per platform), unused rules (hit count thresholds with false positive caveats), rule ordering optimization (performance vs security), and conflict detection.

Also fixed pre-flight observability gaps: added `## Observability / Diagnostics` section to S02-PLAN.md and `## Observability Impact` section to T01-PLAN.md.

## Verification

- `bash scripts/validate.sh` → **Skills checked: 17, Result: PASS (0 errors)** — acl-rule-analysis passes all checks (metadata.safety, 7 H2 sections, references/ directory)
- Body word count: **2458 words** (≤2700 limit) via awk method (K001)
- Reference file count: **2 files** (cli-reference.md, rule-patterns.md)
- `grep -l 'shadowed' skills/acl-rule-analysis/SKILL.md` → returns file path ✓
- All 6 vendor labels present: [Cisco] (7), [JunOS] (5), [EOS] (5), [PAN-OS] (6), [FortiGate] (6), [CheckPoint] (6)
- `bash scripts/validate.sh 2>&1 | grep -c 'ERROR:'` → 0 (no regressions)

## Verification Evidence

| # | Command | Exit Code | Verdict | Duration |
|---|---------|-----------|---------|----------|
| 1 | `bash scripts/validate.sh` | 0 | ✅ pass — "Skills checked: 17, Result: PASS (0 errors)" | 3s |
| 2 | `awk … SKILL.md \| wc -w` | 0 | ✅ pass — 2458 words (≤2700) | <1s |
| 3 | `ls skills/acl-rule-analysis/references/ \| wc -l` | 0 | ✅ pass — 2 files | <1s |
| 4 | `grep -l 'shadowed' skills/acl-rule-analysis/SKILL.md` | 0 | ✅ pass — file path returned | <1s |
| 5 | `grep -c '\[Cisco\]\|\[JunOS\]\|\[EOS\]\|\[PAN-OS\]\|\[FortiGate\]\|\[CheckPoint\]' SKILL.md` | 0 | ✅ pass — 35 vendor labels | <1s |
| 6 | `bash scripts/validate.sh 2>&1 \| grep -c 'ERROR:'` | 0 | ✅ pass — 0 errors (no regressions) | 3s |

### Slice-level checks status (T01 of 4):
- ✅ validate.sh: 17 skills, 0 errors (expected 19 at slice completion)
- ✅ acl-rule-analysis word count ≤2700
- ✅ acl-rule-analysis 2 ref files
- ✅ Content depth: "shadowed" in SKILL.md
- ⏳ cis-benchmark-audit checks (T02)
- ⏳ nist-compliance-assessment checks (T03)
- ⏳ README 3 new rows (T04)
- ⏳ Full 19-skill validation (T04)

## Diagnostics

- `bash scripts/validate.sh 2>&1 | grep 'acl-rule-analysis'` — check this skill's validation status
- `awk 'BEGIN{c=0} /^---$/{c++; if(c==2){found=1; next}} found{print}' skills/acl-rule-analysis/SKILL.md | wc -w` — body word count
- `grep -c '\[Cisco\]\|\[JunOS\]\|\[EOS\]\|\[PAN-OS\]\|\[FortiGate\]\|\[CheckPoint\]' skills/acl-rule-analysis/SKILL.md` — vendor label count

## Deviations

None.

## Known Issues

None.

## Files Created/Modified

- `skills/acl-rule-analysis/SKILL.md` — Vendor-agnostic ACL/firewall rule analysis skill (2458 words, 7 H2 sections, 6 vendor inline labels)
- `skills/acl-rule-analysis/references/cli-reference.md` — Multi-vendor CLI commands for ACL/rulebase/hit-count retrieval (6 platforms)
- `skills/acl-rule-analysis/references/rule-patterns.md` — Rule analysis pattern definitions with detection algorithms (6 patterns)
- `.gsd/milestones/M002/slices/S02/S02-PLAN.md` — Added Observability / Diagnostics section, failure-path diagnostic check
- `.gsd/milestones/M002/slices/S02/tasks/T01-PLAN.md` — Added Observability Impact section
