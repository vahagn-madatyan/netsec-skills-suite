---
estimated_steps: 4
estimated_files: 2
---

# T03: Write README and CONTRIBUTING with install commands and format reference

**Slice:** S01 — Monorepo Foundation & Skill Templates
**Milestone:** M001

## Description

Write the two public-facing docs. README is the project's front door: what this is, how to install skills, current catalog. CONTRIBUTING is the contributor guide: how to write a SKILL.md, what conventions to follow, how to validate and submit. Both are written for the current state (skeleton skill only) — S02-S04 will expand the catalog table.

## Steps

1. Write `README.md`: title/tagline, what this repo is (brief), install command (`npx skills add <owner>/network-security-skills-suite`), skill catalog table (columns: Skill, Description, Safety Tier — one row for the skeleton), usage example showing agent loading a skill, CI badge placeholder (`![Validate Skills](...)`), license note.
2. Write `CONTRIBUTING.md`: SKILL.md format reference (frontmatter schema with all 6 keys explained, body section descriptions), safety tier convention (read-only = no device state changes, read-write = may modify config/state), `references/` file patterns (when to use, naming), validation instructions (how to run both layers locally), PR checklist (new skill? update catalog table, run validation, add to catalog).
3. Verify README has install command and catalog table. Verify CONTRIBUTING covers all conventions from T01.
4. Final check: no broken markdown formatting, all code blocks use correct fencing, references to file paths match actual repo layout.

## Must-Haves

- [ ] README has `npx skills add` install command with correct repo path
- [ ] README has skill catalog table with at least the skeleton skill
- [ ] README has usage example showing how a skill gets loaded
- [ ] CONTRIBUTING has complete SKILL.md frontmatter schema reference
- [ ] CONTRIBUTING documents all required body sections
- [ ] CONTRIBUTING explains safety tier values with examples
- [ ] CONTRIBUTING has local validation instructions

## Verification

- README contains string `npx skills add` and a markdown table with `Safety Tier` column
- CONTRIBUTING contains sections on: frontmatter, body sections, safety tiers, validation, PR process
- No orphan markdown links (all referenced files exist in repo)

## Inputs

- `skills/example-device-health/SKILL.md` — from T01, the template this documentation describes
- `scripts/validate.sh` — from T01, referenced in validation instructions
- `.github/workflows/validate.yml` — from T02, referenced in CI section

## Expected Output

- `README.md` — project readme with install commands, catalog, usage examples
- `CONTRIBUTING.md` — contributor guide with complete format reference
