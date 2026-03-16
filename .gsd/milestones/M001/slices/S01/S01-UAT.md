# S01: Monorepo Foundation & Skill Templates — UAT

**Milestone:** M001
**Written:** 2026-03-15

## UAT Type

- UAT mode: artifact-driven
- Why this mode is sufficient: S01 produces static files (SKILL.md, scripts, CI workflow, docs) — all verifiable by running validation tools and checking file contents. No runtime or UI to test.

## Preconditions

- Python 3.x with `pip3 install skills-ref==0.1.1` (for `agentskills validate`)
- Node.js with `npx` available (for `npx skills add` discovery test)
- `actionlint` installed (for CI workflow syntax check — optional, can skip)
- Repo cloned locally

## Smoke Test

Run `bash scripts/validate.sh` from repo root — should output PASS with 0 errors.

## Test Cases

### 1. Spec-layer validation passes for skeleton skill

1. `agentskills validate skills/example-device-health`
2. **Expected:** Output includes "Valid skill" and exit code 0

### 2. Convention-layer validation passes for all skills

1. `bash scripts/validate.sh`
2. **Expected:** All checks show OK, final line reads "Result: PASS (0 errors)"

### 3. CI workflow is syntactically valid

1. `actionlint .github/workflows/validate.yml`
2. **Expected:** Zero errors, exit code 0

### 4. Skills discovery works via npx

1. `npx skills add . --list`
2. **Expected:** Output includes "Found 1 skill" and lists `example-device-health`

### 5. README has required content

1. Open `README.md` and check for:
   - `npx skills add vahagn-madatyan/network-security-skills-suite` install command
   - Skill catalog table with Safety Tier column
   - Usage example showing agent loading a skill
2. **Expected:** All three present and rendering correctly

### 6. CONTRIBUTING has required content

1. Open `CONTRIBUTING.md` and check for:
   - Frontmatter schema section with all 6 keys
   - All 7 required body sections listed
   - Safety tier convention (`read-only` / `read-write`)
   - Validation instructions (both layers)
   - PR checklist
2. **Expected:** All five areas covered

## Edge Cases

### Invalid safety tier is caught

1. Edit `skills/example-device-health/SKILL.md` — change `safety: read-only` to `safety: destructive`
2. Run `bash scripts/validate.sh`
3. **Expected:** ERROR on safety tier check, final result FAIL (exit 1)
4. Restore the original value after testing

### Missing required section is caught

1. Edit `skills/example-device-health/SKILL.md` — remove the `## Threshold Tables` heading
2. Run `bash scripts/validate.sh`
3. **Expected:** ERROR on missing section, final result FAIL (exit 1)
4. Restore the heading after testing

## Failure Signals

- `scripts/validate.sh` exits non-zero or shows ERROR lines
- `agentskills validate` reports invalid skill
- `actionlint` reports workflow errors
- `npx skills add . --list` fails to discover any skills
- README or CONTRIBUTING missing key sections described above

## Requirements Proved By This UAT

- R001 — Scaffold validated by skills discovery and validation passing
- R002 — SKILL.md template validated by both spec and convention layers, plus edge case mutation tests
- R003 — CI pipeline syntax validated by actionlint
- R004 — README content verified manually
- R005 — CONTRIBUTING content verified manually

## Not Proven By This UAT

- CI workflow execution in actual GitHub Actions environment (only syntax-checked locally)
- Skills discovery from a remote GitHub URL (only tested with local path `.`)
- Behavior with multiple skills in the repo (only one skeleton skill exists)

## Notes for Tester

The skeleton skill `example-device-health` contains realistic but abbreviated content — it's a template demonstration, not a production skill. S02 will produce the first real production-quality skills. Edge case tests require manual file edits — remember to restore originals after testing.
