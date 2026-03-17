---
id: T03
parent: S04
milestone: M001
provides:
  - config-management skill with backup, drift detection, and golden config validation (first read-write safety tier skill)
key_files:
  - skills/config-management/SKILL.md
  - skills/config-management/references/cli-reference.md
  - skills/config-management/references/drift-detection.md
key_decisions:
  - Used read-write safety tier for config management — procedures include config archival, rollback, and remediation that modify device state
  - Marked write operations with ⚠️ WRITE labels inline to distinguish from read-only assessment steps
patterns_established:
  - Read-write safety tier pattern with inline ⚠️ WRITE markers for steps that modify device state
  - Compliance rule definitions with Required (REQ-xxx) and Forbidden (FRB-xxx) pattern IDs for structured compliance checking
  - Drift severity scoring system (numeric points per finding with aggregate thresholds) for quantified drift reporting
observability_surfaces:
  - agentskills validate skills/config-management — structural validation (exit 0 = healthy)
  - bash scripts/validate.sh — suite-wide validation including config-management
  - grep 'safety: read-write' skills/config-management/SKILL.md — confirms read-write tier
  - Word count check via awk pipeline — body ≤ 2700 words (actual: 2049)
duration: 8m
verification_result: passed
completed_at: 2026-03-16
blocker_discovered: false
---

# T03: Create config-management skill with backup, drift detection, and golden config validation

**Created complete config-management skill with 7-step procedure including read-write operations, 3-vendor coverage, drift severity classification, and compliance validation rules.**

## What Happened

Created the `skills/config-management/` directory with SKILL.md and two reference files. This is the first `read-write` safety tier skill in the repo — previous skills were all `read-only`.

SKILL.md contains a 7-step procedure: (1) config collection, (2) running vs startup comparison, (3) config archival with timestamped naming, (4) golden config baseline establishment, (5) section-by-section drift detection across 5 config domains, (6) compliance validation with required/forbidden pattern checking, (7) remediation guidance with rollback options. Write operations are marked with ⚠️ WRITE labels and a safety note in the introduction explains the read-write designation.

The cli-reference.md covers 5 command categories (display, archive/export, compare/diff, rollback/replace, session/staged) with clear safety labeling. It documents the architectural differences between Cisco's dual-config model, JunOS's candidate-commit model, and EOS's hybrid model with session-config support.

The drift-detection.md defines section-by-section diff methodology, golden config normalization rules per vendor, 7 required compliance patterns (REQ-001 through REQ-007), 6 forbidden patterns (FRB-001 through FRB-006), a severity classification matrix, and a numeric drift scoring system for aggregate trending.

Scope was kept to ongoing config management (detect drift, validate compliance, manage archives) — event-driven change verification is reserved for T04.

## Verification

- `bash scripts/validate.sh` → 11 skills checked, 0 errors, PASS (config-management included with `safety: read-write`)
- `awk` word count → 2049 words (≤ 2700 limit)
- `grep 'safety: read-write'` → matches in frontmatter
- `ls skills/config-management/references/` → `cli-reference.md` and `drift-detection.md`
- `grep '^## '` → all 7 required H2 sections present (When to Use, Prerequisites, Procedure, Threshold Tables, Decision Trees, Report Template, Troubleshooting)
- `agentskills validate` → npm package not found (known issue from prior tasks — not installed in this environment; validate.sh covers the same checks)

### Slice-level verification (partial — T03 is task 3 of 5):
- ✅ `bash scripts/validate.sh` → PASS (0 errors) for all 11 skills
- ✅ config-management has `safety: read-write`
- ✅ Word count ≤ 2700
- ✅ 6 frontmatter keys, 7 H2 sections, 2 reference files
- ⬜ T04 (change-verification) not yet created
- ⬜ T05 (README catalog update + final validation) not yet done

## Diagnostics

- Run `agentskills validate skills/config-management` to verify structural validity (requires agentskills npm package)
- Run `bash scripts/validate.sh` to verify as part of full suite
- Check body word count: `awk 'BEGIN{c=0}/^---$/{c++;if(c==2){f=1;next}}f{print}' skills/config-management/SKILL.md | wc -w`
- List references: `ls skills/config-management/references/`

## Deviations

None — implemented exactly as planned.

## Known Issues

- `npx agentskills validate` fails with npm 404 — the `agentskills` package is not published to the npm registry. This is a pre-existing issue from prior tasks. The custom `scripts/validate.sh` covers the same structural checks.

## Files Created/Modified

- `skills/config-management/SKILL.md` — Complete config management skill with read-write safety tier, 7-step procedure, threshold tables, decision trees, report template, and troubleshooting
- `skills/config-management/references/cli-reference.md` — Multi-vendor CLI command reference with 5 command categories, safety labels, and architectural difference notes
- `skills/config-management/references/drift-detection.md` — Drift detection methodology with section definitions, normalization rules, compliance patterns (REQ/FRB), severity matrix, and scoring system
- `.gsd/milestones/M001/slices/S04/tasks/T03-PLAN.md` — Added Observability Impact section (pre-flight fix)
