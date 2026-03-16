---
id: T03
parent: S01
milestone: M001
provides:
  - README.md with install commands, skill catalog table, usage example, and CI badge
  - CONTRIBUTING.md with complete SKILL.md format reference, safety tier docs, validation instructions, and PR checklist
key_files:
  - README.md
  - CONTRIBUTING.md
key_decisions:
  - Usage example shows a realistic multi-step agent triage interaction rather than a minimal snippet — demonstrates how skills drive agent behavior end-to-end
patterns_established:
  - Catalog table format: Skill (linked to SKILL.md), Description, Safety Tier columns — new skills add a row
  - CONTRIBUTING PR checklist as the canonical pre-submit gate for contributors
observability_surfaces:
  - none
duration: ~10 minutes
verification_result: passed
completed_at: 2026-03-15
blocker_discovered: false
---

# T03: Write README and CONTRIBUTING with install commands and format reference

**Wrote project README with install commands, skill catalog, and usage example; wrote CONTRIBUTING guide with complete SKILL.md format reference, safety tier documentation, and two-layer validation instructions.**

## What Happened

Wrote two public-facing docs covering the full current state of the repo.

README covers: project purpose, `npx skills add` install command with correct repo path, skill catalog table (one row for the skeleton skill), a realistic usage example showing an agent loading and executing a health check skill step-by-step, repo structure overview, validation instructions, and a CI badge linking to the workflow.

CONTRIBUTING covers: complete frontmatter schema (all 6 keys with types and descriptions), all 7 required body sections explained, safety tier convention with `read-only` and `read-write` definitions and examples, `references/` directory purpose and naming conventions, two-layer validation instructions with exact commands, and a PR checklist.

## Verification

All must-haves verified:
- README: `npx skills add vahagn-madatyan/network-security-skills-suite` present ✓
- README: Catalog table with `Safety Tier` column and skeleton skill row ✓
- README: Usage example with `Loading skill: example-device-health` ✓
- CONTRIBUTING: Frontmatter schema section ✓
- CONTRIBUTING: All 7 required body sections documented ✓
- CONTRIBUTING: Safety tier values explained with examples ✓
- CONTRIBUTING: Local validation instructions (both layers) ✓

Structural checks:
- All referenced file paths exist in repo ✓
- Code fences balanced in both files ✓

Slice-level verification results:
- `agentskills validate skills/example-device-health` — PASS
- `bash scripts/validate.sh` — PASS
- `actionlint .github/workflows/validate.yml` — PASS
- README contains `npx skills add` and catalog table — PASS
- CONTRIBUTING covers frontmatter, body sections, safety tiers, validation, PR process — PASS
- `npx skills add . --list` — not run (Node.js environment check, deferred to slice-level)

## Diagnostics

none

## Deviations

none

## Known Issues

none

## Files Created/Modified

- `README.md` — Project readme with install commands, catalog table, usage example, CI badge, and repo structure
- `CONTRIBUTING.md` — Contributor guide with SKILL.md format reference, safety tiers, validation instructions, and PR checklist
