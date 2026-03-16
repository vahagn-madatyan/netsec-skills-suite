---
estimated_steps: 3
estimated_files: 1
---

# T02: Wire GitHub Actions CI pipeline with two-layer validation

**Slice:** S01 — Monorepo Foundation & Skill Templates
**Milestone:** M001

## Description

Create a GitHub Actions workflow that validates all SKILL.md files on every push to main and on PRs. Two-layer approach: `skills-ref` catches spec violations (frontmatter schema, name format, description), then `scripts/validate.sh` catches convention violations (safety tier, body sections, references/). Pin `skills-ref==0.1.1` for stability.

## Steps

1. Load the `github-workflows` skill for CI authoring patterns.
2. Create `.github/workflows/validate.yml` — trigger on `push` to main and `pull_request`. Job: `validate-skills` on `ubuntu-latest`. Steps: checkout, setup Python 3.x, `pip install skills-ref==0.1.1`, `agentskills validate skills/`, `bash scripts/validate.sh`. Name steps clearly for CI output readability.
3. Verify the workflow YAML is syntactically valid — install/run `actionlint` or manually verify structure against GitHub Actions schema.

## Must-Haves

- [ ] Workflow triggers on push to main and pull_request
- [ ] `skills-ref==0.1.1` pinned (not latest)
- [ ] Both `agentskills validate skills/` and `bash scripts/validate.sh` run as separate steps
- [ ] Uses ubuntu-latest runner
- [ ] Step names are descriptive for CI output

## Verification

- YAML syntax is valid (actionlint or manual review)
- Workflow contains both validation steps as separate named steps
- `skills-ref` version is pinned to 0.1.1

## Inputs

- `scripts/validate.sh` — from T01, must exist and be executable
- `skills/example-device-health/SKILL.md` — from T01, the skill the CI will validate

## Expected Output

- `.github/workflows/validate.yml` — complete CI workflow ready for GitHub
