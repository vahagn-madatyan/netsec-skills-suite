---
id: S01
parent: M001
milestone: M001
provides:
  - skills/ directory convention with kebab-case dirs, SKILL.md + references/ per skill
  - SKILL.md template with all 6 frontmatter keys including metadata.safety (read-only | read-write)
  - Custom validation script (scripts/validate.sh) enforcing safety tier, 7 required body sections, references/ presence
  - GitHub Actions CI workflow with two-layer validation (spec + convention)
  - README with npx skills add install command, skill catalog table, usage example, CI badge
  - CONTRIBUTING guide with SKILL.md format reference, safety tier docs, validation instructions, PR checklist
  - Skeleton example skill (example-device-health) proving the full pipeline end-to-end
requires:
  - slice: none
    provides: first slice — no dependencies
affects:
  - S02
  - S03
  - S04
key_files:
  - skills/example-device-health/SKILL.md
  - skills/example-device-health/references/cli-reference.md
  - skills/example-device-health/references/threshold-tables.md
  - scripts/validate.sh
  - .github/workflows/validate.yml
  - README.md
  - CONTRIBUTING.md
key_decisions:
  - agentskills validate takes one skill dir at a time, not the parent skills/ dir — custom script handles iteration
  - CI pins actions/checkout@v4, actions/setup-python@v5, skills-ref==0.1.1 for reproducibility
  - CI uses permissions contents:read for least-privilege
  - Usage example shows realistic multi-step agent triage, not a minimal snippet
patterns_established:
  - SKILL.md frontmatter with 6 keys (name, description, license, metadata.safety, metadata.author, metadata.version)
  - 7 required H2 body sections (When to Use, Prerequisites, Procedure, Threshold Tables, Decision Trees, Report Template, Troubleshooting)
  - references/ subdirectory for progressive disclosure overflow
  - Custom validator iterates skills/*/SKILL.md and checks frontmatter + body + structure
  - Two-layer CI validation — agentskills validate (spec) then scripts/validate.sh (convention)
  - Catalog table format in README — Skill (linked), Description, Safety Tier columns
  - CONTRIBUTING PR checklist as canonical pre-submit gate
observability_surfaces:
  - scripts/validate.sh outputs per-skill per-check OK/ERROR lines with final PASS/FAIL summary
  - CI step names identify which validation layer failed (spec vs convention)
drill_down_paths:
  - .gsd/milestones/M001/slices/S01/tasks/T01-SUMMARY.md
  - .gsd/milestones/M001/slices/S01/tasks/T02-SUMMARY.md
  - .gsd/milestones/M001/slices/S01/tasks/T03-SUMMARY.md
duration: ~35m
verification_result: passed
completed_at: 2026-03-15
---

# S01: Monorepo Foundation & Skill Templates

**Established repo scaffold, SKILL.md template with safety tier metadata, two-layer CI validation, and public-facing docs — proven end-to-end by a skeleton Cisco device health check skill that passes all validation and is discoverable via `npx skills add`.**

## What Happened

Built the monorepo foundation in three tasks.

**T01** created the `skills/example-device-health/` skeleton with a realistic Cisco IOS-XE device health check SKILL.md — all 6 frontmatter keys, all 7 required body sections with real procedural content (show commands, threshold interpretation, triage decision trees, structured report template). Added two reference files for progressive disclosure (`cli-reference.md` with vendor CLI commands, `threshold-tables.md` with detailed thresholds). Wrote `scripts/validate.sh` that checks every skill for valid safety tier, required sections, and references/ presence.

**T02** wired the GitHub Actions CI workflow (`.github/workflows/validate.yml`) triggered on push to main and PRs. Two validation layers run as separate named steps: `agentskills validate` for spec compliance and `scripts/validate.sh` for convention enforcement. Pinned all action versions and skills-ref dependency for reproducibility.

**T03** wrote README.md with `npx skills add` install command, skill catalog table, realistic usage example, repo structure overview, and CI badge. Wrote CONTRIBUTING.md with complete frontmatter schema, all 7 required body sections documented, safety tier convention, references/ patterns, two-layer validation instructions, and PR checklist.

## Verification

All slice-level checks passed:

- `agentskills validate skills/example-device-health` → "Valid skill" (exit 0)
- `bash scripts/validate.sh` → 9/9 checks OK, PASS (exit 0)
- `actionlint .github/workflows/validate.yml` → zero errors (exit 0)
- `npx skills add . --list` → "Found 1 skill" — discovery works
- README contains `npx skills add` command and catalog table with Safety Tier column
- CONTRIBUTING contains frontmatter schema, body sections, safety tiers, validation instructions, PR checklist
- Mutation testing: invalid safety value and missing section both caught by validate.sh

## Requirements Advanced

- R001 — Scaffold fully implemented: skills/ convention, package.json, .gitignore all in place
- R002 — SKILL.md template proven with all conventions: frontmatter schema, body sections, safety tier metadata
- R003 — CI pipeline wired with two-layer validation, actionlint-verified
- R004 — README has install commands, catalog table, usage example — will expand as skills are added in S02-S04
- R005 — CONTRIBUTING guide complete with format reference, safety tier docs, validation instructions

## Requirements Validated

- R001 — `npx skills add . --list` discovers skills, validate.sh enforces directory convention
- R002 — Skeleton skill passes both `agentskills validate` and `scripts/validate.sh`; mutation tests confirm invalid values are caught
- R003 — `actionlint` confirms workflow syntax; two validation layers are wired as separate steps
- R004 — README verified to contain install command, catalog table, and usage example
- R005 — CONTRIBUTING verified to contain all required format sections

## New Requirements Surfaced

- none

## Requirements Invalidated or Re-scoped

- none

## Deviations

none — all three tasks executed as planned.

## Known Limitations

- `agentskills validate` only accepts individual skill directories, not the parent `skills/` directory. The CI workflow and custom script both handle this by iterating, but contributors must know to run against individual dirs.
- CI workflow has not been tested in an actual GitHub Actions run — only validated syntactically via actionlint. First real push to main will confirm.

## Follow-ups

- none — S02 picks up from here with the first real content skills.

## Files Created/Modified

- `skills/example-device-health/SKILL.md` — Skeleton skill with realistic Cisco IOS-XE device health check content
- `skills/example-device-health/references/cli-reference.md` — CLI command reference by subsystem
- `skills/example-device-health/references/threshold-tables.md` — Detailed threshold tables with severity levels
- `scripts/validate.sh` — Custom convention validator (executable)
- `.github/workflows/validate.yml` — GitHub Actions CI with two-layer validation
- `README.md` — Project readme with install commands, catalog, usage example, CI badge
- `CONTRIBUTING.md` — Contributor guide with format reference, safety tiers, validation, PR checklist

## Forward Intelligence

### What the next slice should know
- The SKILL.md template in `skills/example-device-health/SKILL.md` is the reference implementation. Copy its structure exactly for new skills — frontmatter keys, H2 section names, references/ layout.
- `scripts/validate.sh` checks for exactly 7 H2 section names. If S02 needs to add or rename sections, update the validator too.
- `agentskills validate` must be called per-skill-directory, not on the parent. The CI workflow already handles this correctly.

### What's fragile
- `scripts/validate.sh` uses simple grep for section detection — it checks for `## Section Name` literally. Markdown variations (extra spaces, different heading levels) would slip through.
- The skills-ref pin at 0.1.1 — if the spec evolves, we may need to update the pin and adjust frontmatter.

### Authoritative diagnostics
- `bash scripts/validate.sh` — single command that validates all skills against all conventions. Trust its PASS/FAIL.
- `agentskills validate skills/<name>` — authoritative for spec compliance of individual skills.

### What assumptions changed
- No assumptions changed. The skills.sh discovery (`npx skills add . --list`) and agentskills validation both work as expected.
