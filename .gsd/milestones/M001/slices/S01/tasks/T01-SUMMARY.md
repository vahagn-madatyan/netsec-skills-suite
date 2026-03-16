---
id: T01
parent: S01
milestone: M001
provides:
  - Skeleton skill (example-device-health) proving SKILL.md template with all conventions
  - Custom validation script enforcing safety tier, required sections, references/ presence
  - skills/ directory convention established
key_files:
  - skills/example-device-health/SKILL.md
  - skills/example-device-health/references/cli-reference.md
  - skills/example-device-health/references/threshold-tables.md
  - scripts/validate.sh
key_decisions:
  - agentskills validate takes one skill dir at a time, not the parent skills/ dir — custom script handles iteration
patterns_established:
  - SKILL.md frontmatter with all 6 keys including metadata.safety and metadata.author/version
  - Required body sections as H2 headers (When to Use, Prerequisites, Procedure, Threshold Tables, Decision Trees, Report Template, Troubleshooting)
  - references/ subdirectory for progressive disclosure overflow (cli-reference.md, threshold-tables.md)
  - Custom validator bash script pattern (iterate skills/*/SKILL.md, check frontmatter + body + structure)
observability_surfaces:
  - scripts/validate.sh outputs per-skill per-check OK/ERROR lines with final PASS/FAIL summary
duration: 15m
verification_result: passed
completed_at: 2026-03-15
blocker_discovered: false
---

# T01: Create skills/ scaffold, skeleton skill, and custom validation script

**Built a realistic Cisco IOS-XE device health check skill with full SKILL.md conventions and a custom validation script that catches safety tier, section, and structure violations.**

## What Happened

Created `skills/example-device-health/` with a complete SKILL.md containing all 6 allowed frontmatter keys (name, description, license, metadata with safety/author/version). Body has all 7 required H2 sections with real Cisco IOS-XE content — show commands, threshold interpretation, triage decision trees, structured report template, and troubleshooting guidance.

Added two reference files for progressive disclosure: `cli-reference.md` (vendor CLI commands organized by subsystem) and `threshold-tables.md` (detailed warning/critical/emergency thresholds for CPU, memory, interfaces, routing, and environment).

Wrote `scripts/validate.sh` that iterates all `skills/*/SKILL.md` files and checks: (1) metadata.safety exists and is `read-only` or `read-write`, (2) all 7 required H2 sections present, (3) references/ directory exists. Clear per-check output with final PASS/FAIL summary.

## Verification

- `agentskills validate skills/example-device-health` → "Valid skill" (exit 0)
- `bash scripts/validate.sh` → all 9 checks OK, PASS (exit 0)
- `npx skills add . --list` → "Found 1 skill" — discovery works
- Mutated safety to `destructive` → validate.sh exits 1, catches invalid value
- Removed `## Threshold Tables` header → validate.sh exits 1, catches missing section

## Diagnostics

- Run `bash scripts/validate.sh` to validate all skills against conventions
- Run `agentskills validate skills/<name>` to validate individual skill against Agent Skills spec
- Validation errors are printed per-skill with clear ERROR lines to stderr

## Deviations

- `agentskills validate` accepts a single skill directory, not the parent `skills/` directory. The custom script handles iteration. This is fine — T02 CI workflow will loop over skills or call both tools appropriately.

## Known Issues

None.

## Files Created/Modified

- `skills/example-device-health/SKILL.md` — Complete skeleton skill with realistic Cisco IOS-XE device health check content, all required frontmatter and body sections
- `skills/example-device-health/references/cli-reference.md` — CLI command reference organized by subsystem (CPU, memory, interfaces, routing, environment)
- `skills/example-device-health/references/threshold-tables.md` — Detailed threshold tables with normal/warning/critical/emergency levels for all monitored parameters
- `scripts/validate.sh` — Custom convention validator (executable), checks safety tier, required sections, references/ directory
