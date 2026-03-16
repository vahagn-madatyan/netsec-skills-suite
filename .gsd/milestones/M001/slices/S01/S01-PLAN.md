# S01: Monorepo Foundation & Skill Templates

**Goal:** Establish repo scaffold, SKILL.md template with safety tier metadata, CI validation pipeline, README, and CONTRIBUTING guide — proven end-to-end by a skeleton example skill.
**Demo:** A skeleton skill in `skills/example-device-health/` passes both `agentskills validate` and custom validation, `npx skills add` discovers it, CI workflow is ready to enforce on every push.

## Must-Haves

- `skills/` directory convention with kebab-case dirs, each containing SKILL.md + optional `references/`
- SKILL.md template with all 6 allowed frontmatter keys including `metadata.safety: read-only | read-write`
- Body sections: When to Use, Prerequisites, Procedure, Threshold Tables, Decision Trees, Report Template, Troubleshooting
- Custom validation script checking: safety tier values, required body sections, `references/` directory presence
- GitHub Actions CI with two-layer validation: `skills-ref` (spec compliance) + custom script (our conventions)
- README with `npx skills add` install commands, skill catalog table, usage examples
- CONTRIBUTING guide with SKILL.md format reference, safety tier conventions, PR process
- Skeleton example skill with realistic device health content that proves the full pipeline

## Verification

- `pip install skills-ref==0.1.1 && agentskills validate skills/` — all skills pass spec validation
- `bash scripts/validate.sh` — all skills pass custom convention checks (safety tier, sections, references/)
- `actionlint .github/workflows/validate.yml` or manual syntax review — CI workflow is valid
- `npx skills add . --list` — discovers the skeleton skill (requires Node.js)
- README contains `npx skills add` install command and skill catalog table
- CONTRIBUTING contains SKILL.md format reference with all required sections documented

## Tasks

- [x] **T01: Create skills/ scaffold, skeleton skill, and custom validation script** `est:45m`
  - Why: Everything else depends on having a real skill in the repo. The skeleton skill proves the SKILL.md template works, establishes the `references/` convention, and gives the validation script something to check against. Covers R001 (scaffold), R002 (template with safety tier).
  - Files: `skills/example-device-health/SKILL.md`, `skills/example-device-health/references/cli-reference.md`, `skills/example-device-health/references/threshold-tables.md`, `scripts/validate.sh`
  - Do: Create `skills/example-device-health/` with a realistic Cisco device health check SKILL.md (all required frontmatter keys, `metadata.safety: read-only`, all body sections with real procedural content). Add 2 reference files for progressive disclosure. Write `scripts/validate.sh` that checks every skill for: valid `metadata.safety` value, presence of required body sections, `references/` directory exists. Keep skeleton body under ~5000 tokens.
  - Verify: `agentskills validate skills/` passes AND `bash scripts/validate.sh` passes with zero errors
  - Done when: Skeleton skill validates at both layers and custom script catches intentionally broken skills

- [x] **T02: Wire GitHub Actions CI pipeline with two-layer validation** `est:30m`
  - Why: CI prevents broken skills from landing. Two-layer approach catches both spec violations (`skills-ref`) and convention violations (our custom checks). Covers R003.
  - Files: `.github/workflows/validate.yml`
  - Do: Create workflow triggered on push to main and PRs. Steps: checkout, setup Python, `pip install skills-ref==0.1.1`, `agentskills validate skills/`, `bash scripts/validate.sh`. Pin skills-ref version. Use ubuntu-latest runner. Load `github-workflows` skill for CI authoring guidance.
  - Verify: `actionlint .github/workflows/validate.yml` passes (install actionlint if needed), or manual YAML syntax verification
  - Done when: Workflow file is syntactically valid and both validation layers are wired

- [x] **T03: Write README and CONTRIBUTING with install commands and format reference** `est:30m`
  - Why: README is the first thing users see — must show install commands and skill catalog. CONTRIBUTING enables community contributions with the SKILL.md format reference. Covers R004, R005.
  - Files: `README.md`, `CONTRIBUTING.md`
  - Do: README: project title/description, install command (`npx skills add <owner>/network-security-skills-suite`), skill catalog table (name, description, safety tier — currently just the skeleton), usage example showing how to load a skill, CI badge. CONTRIBUTING: SKILL.md format reference (frontmatter schema, body sections), safety tier convention (read-only vs read-write with examples), `references/` file patterns, validation instructions (`agentskills validate` + `scripts/validate.sh`), PR process. Write for current state — S02-S04 will expand the catalog.
  - Verify: README contains install command and catalog table. CONTRIBUTING contains all required format sections. No broken markdown links.
  - Done when: Both files render correctly and cover all conventions established in T01

## Files Likely Touched

- `skills/example-device-health/SKILL.md`
- `skills/example-device-health/references/cli-reference.md`
- `skills/example-device-health/references/threshold-tables.md`
- `scripts/validate.sh`
- `.github/workflows/validate.yml`
- `README.md`
- `CONTRIBUTING.md`
