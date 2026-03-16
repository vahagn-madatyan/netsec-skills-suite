---
estimated_steps: 5
estimated_files: 5
---

# T01: Create skills/ scaffold, skeleton skill, and custom validation script

**Slice:** S01 — Monorepo Foundation & Skill Templates
**Milestone:** M001

## Description

Create the `skills/` directory convention with a realistic skeleton device health check skill that exercises every SKILL.md convention: all 6 frontmatter keys, `metadata.safety`, every required body section, and a `references/` subdirectory with progressive disclosure files. Then write a custom validation script that enforces our conventions beyond what `skills-ref` validates. This task establishes the template that all S02-S04 skills will follow.

## Steps

1. Create `skills/example-device-health/SKILL.md` — realistic Cisco IOS-XE device health check content. Frontmatter: name (matching dir), description (trigger-rich, <1024 chars), license (Apache-2.0), metadata (safety: read-only, author, version), allowed-tools (empty or omitted). Body sections: When to Use, Prerequisites, Procedure (with numbered steps), Threshold Tables (CPU/memory/interface), Decision Trees (triage flow), Report Template (structured output format), Troubleshooting (common issues). Target body under ~5000 tokens.
2. Create `skills/example-device-health/references/cli-reference.md` — vendor CLI commands organized by subsystem (CPU, memory, interfaces, routing).
3. Create `skills/example-device-health/references/threshold-tables.md` — detailed threshold tables with warning/critical/emergency levels for all monitored parameters.
4. Write `scripts/validate.sh` — bash script that iterates over every `skills/*/SKILL.md`, checks: (a) `metadata.safety` exists and is `read-only` or `read-write`, (b) all required body sections present as H2 headers, (c) `references/` directory exists alongside SKILL.md. Exit non-zero on any failure, with clear error messages per-skill.
5. Verify: run `agentskills validate skills/` and `bash scripts/validate.sh` — both pass. Then intentionally break a skill (remove a section, bad safety value) and confirm the custom script catches it.

## Must-Haves

- [ ] SKILL.md frontmatter has all 6 allowed keys with `metadata.safety: read-only`
- [ ] SKILL.md body has all required sections: When to Use, Prerequisites, Procedure, Threshold Tables, Decision Trees, Report Template, Troubleshooting
- [ ] `references/` directory exists with at least 2 reference files
- [ ] Skeleton content is realistic (not placeholder/lorem ipsum) — a real device health triage procedure
- [ ] `scripts/validate.sh` catches: missing/invalid safety tier, missing body sections, missing references/ dir
- [ ] `agentskills validate skills/` passes for the skeleton skill

## Verification

- `pip install skills-ref==0.1.1 && agentskills validate skills/` exits 0
- `bash scripts/validate.sh` exits 0 with all checks passing
- Modify skeleton to have `metadata.safety: destructive` → `bash scripts/validate.sh` exits non-zero
- Remove `## Threshold Tables` section → `bash scripts/validate.sh` exits non-zero

## Inputs

- S01-RESEARCH.md — SKILL.md format rules, 6 allowed frontmatter keys, `skills-ref` validation behavior, body token budget (<5000)
- DECISIONS.md — D002 (advisory safety tiers), D004 (deep procedural content), D005 (references/ strategy), D009 (kebab-case dir layout)

## Expected Output

- `skills/example-device-health/SKILL.md` — complete template-quality skill with realistic device health content
- `skills/example-device-health/references/cli-reference.md` — CLI reference for progressive disclosure
- `skills/example-device-health/references/threshold-tables.md` — detailed threshold tables
- `scripts/validate.sh` — custom convention validator, executable, with clear error output
