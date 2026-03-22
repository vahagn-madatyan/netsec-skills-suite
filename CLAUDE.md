# CLAUDE.md — Network Security Skills Suite

## What This Project Is

A curated collection of 37 AI agent skills for network and security operations. Each skill is a structured SKILL.md file that agents load and execute. Skills are read-only (35) or read-write (2, require approval).

## Project Structure

```
skills/<skill-name>/SKILL.md        # Skill definition
skills/<skill-name>/references/     # Supporting CLI refs, threshold tables
manifest.json                       # Central inventory with metadata and profiles
scripts/validate.sh                 # Convention validator (safety tiers, sections, refs/)
scripts/skill_security_auditor.py   # Security scanner (injection, obfuscation, creds)
```

## SKILL.md Format

Every SKILL.md requires:
- **YAML frontmatter** with: name, description, license, metadata.safety, metadata.author, metadata.version, metadata.openclaw
- **7 required H2 sections** (in order): When to Use, Prerequisites, Procedure, Threshold Tables, Decision Trees, Report Template, Troubleshooting
- **references/ directory** alongside SKILL.md with at least one .md file

## Safety Tiers

- `read-only` — collects data only (show commands, log reads, audits)
- `read-write` — may modify device state; requires approval and clearly marked state-modifying steps

## Validation

Run locally before pushing:

```bash
make check    # runs all validation (spec + conventions + manifest)
```

Or individually:

```bash
make validate   # spec + convention validation
make audit      # security audit on all skills
make manifest   # manifest.json drift and schema check
```

CI runs 5 validation layers: spec, conventions, security audit, VirusTotal, OpenSSF Scorecard.

## Key Rules

- All CI GitHub Actions are SHA-pinned (no tags)
- Python dependencies are hash-pinned in requirements/validate.txt
- manifest.json must stay in sync with skills/ directories — CI checks both directions
- Use `skills.sh` for installation, not custom install scripts
- OpenClaw metadata in frontmatter must mirror metadata.safety in safetyTier field
