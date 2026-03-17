# S04: Network Operations & Change Management — UAT

**Milestone:** M001
**Written:** 2026-03-16

## UAT Type

- UAT mode: artifact-driven
- Why this mode is sufficient: All deliverables are static markdown files (SKILL.md + references/). No runtime, no API, no UI. Validation is structural (frontmatter schema, required sections, word count, file existence) plus SDK discovery (`npx skills add . --list`).

## Preconditions

- Node.js installed (for `npx skills add`)
- Repository cloned with all S01–S04 work present
- `scripts/validate.sh` exists and is executable

## Smoke Test

Run `bash scripts/validate.sh` — expect "12 skills checked, 0 errors, PASS".

## Test Cases

### 1. Full suite validation passes

1. Run `bash scripts/validate.sh`
2. **Expected:** Output shows 12 skills checked, 0 errors, PASS. Each skill shows OK for safety tier, all 7 H2 sections, and references/ directory.

### 2. SDK discovery finds all skills

1. Run `npx skills add . --list`
2. **Expected:** Output shows "Found 12 skills" and lists all skill names.

### 3. Interface-health skill structure

1. Run `awk 'BEGIN{c=0}/^---$/{c++;if(c==2){f=1;next}}f{print}' skills/interface-health/SKILL.md | wc -w`
2. **Expected:** Word count ≤ 2700 (actual: ~2176)
3. Run `grep 'safety:' skills/interface-health/SKILL.md | head -1`
4. **Expected:** Contains `read-only`
5. Run `ls skills/interface-health/references/`
6. **Expected:** Exactly 2 files: `cli-reference.md`, `threshold-tables.md`
7. Run `grep '^## ' skills/interface-health/SKILL.md`
8. **Expected:** 7 sections: When to Use, Prerequisites, Procedure, Threshold Tables, Decision Trees, Report Template, Troubleshooting

### 4. Network-topology-discovery skill structure

1. Run `awk 'BEGIN{c=0}/^---$/{c++;if(c==2){f=1;next}}f{print}' skills/network-topology-discovery/SKILL.md | wc -w`
2. **Expected:** Word count ≤ 2700 (actual: ~2272)
3. Run `grep 'safety:' skills/network-topology-discovery/SKILL.md | head -1`
4. **Expected:** Contains `read-only`
5. Run `ls skills/network-topology-discovery/references/`
6. **Expected:** Exactly 2 files: `cli-reference.md`, `discovery-workflow.md`

### 5. Config-management skill — read-write safety

1. Run `grep 'safety:' skills/config-management/SKILL.md | head -1`
2. **Expected:** Contains `read-write`
3. Run `awk 'BEGIN{c=0}/^---$/{c++;if(c==2){f=1;next}}f{print}' skills/config-management/SKILL.md | wc -w`
4. **Expected:** Word count ≤ 2700 (actual: ~2049)
5. Run `grep -c '⚠️' skills/config-management/SKILL.md`
6. **Expected:** At least 1 (write operation markers present)
7. Run `ls skills/config-management/references/`
8. **Expected:** Exactly 2 files: `cli-reference.md`, `drift-detection.md`

### 6. Change-verification skill — read-write safety

1. Run `grep 'safety:' skills/change-verification/SKILL.md | head -1`
2. **Expected:** Contains `read-write`
3. Run `awk 'BEGIN{c=0}/^---$/{c++;if(c==2){f=1;next}}f{print}' skills/change-verification/SKILL.md | wc -w`
4. **Expected:** Word count ≤ 2700 (actual: ~2475)
5. Run `ls skills/change-verification/references/`
6. **Expected:** Exactly 2 files: `checklist-templates.md`, `cli-reference.md`

### 7. Safety tier audit — exactly 2 read-write skills

1. Run `grep -rl 'safety: read-write' skills/*/SKILL.md`
2. **Expected:** Exactly 2 results: `skills/change-verification/SKILL.md`, `skills/config-management/SKILL.md`
3. Run `grep -rl 'safety: read-only' skills/*/SKILL.md | wc -l`
4. **Expected:** 10

### 8. README catalog completeness

1. Run `grep -c 'skills/.*SKILL.md' README.md`
2. **Expected:** 12 (1 example + 11 real skills)
3. Manually verify the 4 new rows exist: change-verification, config-management, interface-health, network-topology-discovery
4. **Expected:** Each row has skill name, description, and correct safety tier

### 9. Vendor labeling present in all 4 new skills

1. Run `for s in interface-health network-topology-discovery config-management change-verification; do echo "$s:"; grep -c '\[Cisco\]\|\[JunOS\]\|\[EOS\]' skills/$s/SKILL.md; done`
2. **Expected:** Each skill has ≥ 5 vendor labels

### 10. Reference file content is substantive

1. Run `wc -l skills/interface-health/references/threshold-tables.md`
2. **Expected:** > 50 lines (not a stub)
3. Run `wc -l skills/network-topology-discovery/references/discovery-workflow.md`
4. **Expected:** > 50 lines
5. Run `wc -l skills/config-management/references/drift-detection.md`
6. **Expected:** > 50 lines
7. Run `wc -l skills/change-verification/references/checklist-templates.md`
8. **Expected:** > 50 lines

## Edge Cases

### Example skill still passes validation

1. Run `bash scripts/validate.sh 2>&1 | grep example-device-health`
2. **Expected:** Shows OK checks, no errors. The example skill is not broken by adding new skills.

### No duplicate skill names

1. Run `ls -d skills/*/SKILL.md | xargs grep '^name:' | sort | uniq -d`
2. **Expected:** No output (no duplicate names)

### All skills have unique descriptions

1. Run `ls -d skills/*/SKILL.md | xargs grep '^description:' | awk -F: '{print $NF}' | sort | uniq -d`
2. **Expected:** No output (no duplicate descriptions)

## Failure Signals

- `bash scripts/validate.sh` exits non-zero or reports errors
- `npx skills add . --list` shows fewer than 12 skills
- Any SKILL.md body exceeds 2700 words
- Missing `references/` directory or wrong number of reference files
- Safety tier mismatch (e.g., config-management showing `read-only`)
- README catalog missing any of the 4 new skill rows
- Vendor labels (`[Cisco]`/`[JunOS]`/`[EOS]`) absent from procedure sections

## Requirements Proved By This UAT

- R013 — Test case 4 proves topology discovery skill exists with correct structure
- R014 — Test case 5 proves config management skill exists with read-write safety and drift detection references
- R015 — Test case 3 proves interface health skill exists with threshold tables and optical power references
- R016 — Test case 6 proves change verification skill exists with checklist templates and read-write safety
- R004 (supporting) — Test case 8 proves README catalog is complete

## Not Proven By This UAT

- Actual usefulness of skills when loaded into a live agent session (requires human tester with network access)
- Correctness of CLI commands listed in reference files (would require actual device access)
- Token count accuracy (word count ≤ 2700 is a proxy; actual tokenization varies by model)
- GitHub Actions CI runs on push (would require pushing to GitHub and observing the workflow)

## Notes for Tester

- The `agentskills` npm package (for `npx agentskills validate`) is not published — this is a known issue. Use `scripts/validate.sh` as the authoritative validator instead.
- Word counts from `wc -w` may vary by ±5 words depending on locale settings. The important thing is they're well under 2700.
- The README shows 12 total catalog rows (1 example + 11 real). The original plan estimated 13, but S02+S03 delivered 7 real skills (not 8). The "12+" milestone success criterion counts all 12 entries including the example.
