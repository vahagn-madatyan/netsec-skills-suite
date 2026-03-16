---
id: T02
parent: S01
milestone: M001
provides:
  - GitHub Actions CI workflow with two-layer validation (spec + convention)
key_files:
  - .github/workflows/validate.yml
key_decisions:
  - Pinned actions/checkout@v4 and actions/setup-python@v5 for stability
  - Added explicit permissions (contents: read) for least-privilege CI
patterns_established:
  - CI runs both agentskills validate (spec layer) and scripts/validate.sh (convention layer) as separate named steps
observability_surfaces:
  - CI step names clearly identify which validation layer failed
duration: 10m
verification_result: passed
completed_at: 2026-03-15
blocker_discovered: false
---

# T02: Wire GitHub Actions CI pipeline with two-layer validation

**Created `.github/workflows/validate.yml` with two-layer skill validation on push to main and PRs.**

## What Happened

Created the GitHub Actions workflow with six steps: checkout, Python setup, skills-ref install (pinned to 0.1.1), spec validation via `agentskills validate skills/`, and convention validation via `bash scripts/validate.sh`. Added `permissions: contents: read` for least-privilege. Both validation layers run as separate named steps so CI output clearly shows which layer caught an issue.

## Verification

- `actionlint .github/workflows/validate.yml` — zero errors
- Confirmed triggers: push to main, pull_request
- Confirmed `skills-ref==0.1.1` pinned (not latest)
- Confirmed both validation steps present as separate named steps
- Confirmed `ubuntu-latest` runner
- Confirmed all step names are descriptive

### Slice-level checks (this task):
- ✅ `bash scripts/validate.sh` — PASS (0 errors, 1 skill checked)
- ✅ `actionlint .github/workflows/validate.yml` — valid, zero errors
- ⏳ `agentskills validate skills/` — requires skills-ref install (covered by T01 verification)
- ⏳ `npx skills add . --list` — T03 scope
- ⏳ README / CONTRIBUTING checks — T03 scope

## Diagnostics

- Run `actionlint .github/workflows/validate.yml` to re-verify workflow syntax
- CI step failures will name the specific validation layer that caught the issue

## Deviations

None.

## Known Issues

None.

## Files Created/Modified

- `.github/workflows/validate.yml` — GitHub Actions CI workflow with two-layer skill validation
