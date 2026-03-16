# Contributing to Network Security Skills Suite

This guide covers how to write, validate, and submit a new skill.

## SKILL.md Format Reference

Every skill lives in its own directory under `skills/` and consists of a `SKILL.md` file plus an optional `references/` directory:

```
skills/
  your-skill-name/
    SKILL.md
    references/
      threshold-tables.md
      cli-reference.md
      ...
```

### Frontmatter Schema

The SKILL.md file starts with YAML frontmatter between `---` markers. All six keys are required:

```yaml
---
name: your-skill-name
description: >-
  One to three sentences describing when an agent should use this skill.
  Be specific about the technology, task type, and trigger conditions.
license: Apache-2.0
metadata:
  safety: read-only
  author: your-name-or-org
  version: "1.0.0"
---
```

| Key | Type | Description |
|-----|------|-------------|
| `name` | string | Skill directory name. Lowercase, hyphenated. Must match the directory. |
| `description` | string | When to use this skill. Agents match on this text, so include the technology (e.g., "Cisco IOS-XE"), the task type (e.g., "health check"), and trigger scenarios. |
| `license` | string | SPDX license identifier. Use `Apache-2.0` unless you have a specific reason otherwise. |
| `metadata.safety` | string | Safety tier — `read-only` or `read-write`. See [Safety Tiers](#safety-tiers) below. |
| `metadata.author` | string | Author name or organization. |
| `metadata.version` | string | Semantic version string (quoted to prevent YAML type coercion). |

### Required Body Sections

After the frontmatter, the SKILL.md body must include these sections as H2 (`##`) headers, in order:

| Section | Purpose |
|---------|---------|
| `## When to Use` | Trigger conditions — when should an agent load this skill? List concrete scenarios. |
| `## Prerequisites` | What the agent needs before starting: access requirements, software versions, baseline knowledge. |
| `## Procedure` | The step-by-step procedure the agent follows. Use H3 subsections for individual steps. Include exact commands in fenced code blocks. |
| `## Threshold Tables` | Reference thresholds for interpreting collected data. Use markdown tables with Normal / Warning / Critical columns. May reference files in `references/`. |
| `## Decision Trees` | Triage logic in tree format. The agent follows these to determine next actions based on findings. Use indented text trees or fenced code blocks. |
| `## Report Template` | Structured output format the agent produces as a deliverable. Define the report sections, severity classifications, and expected fields. |
| `## Troubleshooting` | Common issues the agent may encounter while executing the procedure, with workarounds. |

You may add additional H2 sections, but the seven above are required and validated by CI.

## Safety Tiers

Every skill must declare a safety tier in `metadata.safety`. This tells the agent (and the human operator) whether the skill will modify device state.

### `read-only`

The skill only collects information. It runs `show` commands, reads logs, and gathers data — but never changes device configuration or operational state.

**Examples:**
- Device health checks using `show` commands
- Log analysis and pattern matching
- Configuration audits that read but don't modify
- Traffic analysis and capacity reporting

### `read-write`

The skill may modify device configuration or operational state. This includes applying configuration changes, clearing counters, resetting interfaces, or any operation that alters the device beyond data collection.

**Examples:**
- Applying security hardening configurations
- Remediating vulnerabilities by changing settings
- Interface resets or counter clears
- ACL modifications or firewall rule updates

**Convention:** When writing a `read-write` skill, clearly mark which steps modify state in the Procedure section so the agent can prompt for confirmation before executing them.

## The `references/` Directory

Each skill directory must contain a `references/` subdirectory. This holds supporting reference material that the skill's procedure can point to.

### When to Use References

- **Threshold tables** too detailed for the main SKILL.md — put a summary table in the body, full detail in `references/threshold-tables.md`
- **CLI command reference** — syntax details, platform-specific variations, output field descriptions
- **Vendor documentation excerpts** — relevant sections with source attribution
- **Configuration templates** — baseline configs, hardening templates, compliance profiles

### Naming Convention

Use descriptive, hyphenated filenames:
- `threshold-tables.md`
- `cli-reference.md`
- `hardening-baseline.md`
- `compliance-checklist.md`

All files in `references/` should be markdown (`.md`).

## Validation

Skills are validated at two layers. **Both must pass before a PR will be merged.**

### Layer 1: Spec Validation (Agent Skills)

Checks compliance with the Agent Skills SKILL.md specification — frontmatter schema, required top-level fields.

```bash
pip install skills-ref==0.1.1
agentskills validate skills/your-skill-name
```

### Layer 2: Convention Validation (Custom)

Checks network-security-specific conventions — safety tier present and valid, all seven required body sections exist as H2 headers, `references/` directory is present.

```bash
bash scripts/validate.sh
```

This validates all skills in `skills/`. Errors are printed per-skill with clear `ERROR` lines.

### Running Both Layers

To validate everything at once (same as CI):

```bash
pip install skills-ref==0.1.1
agentskills validate skills/
bash scripts/validate.sh
```

### CI Pipeline

CI runs both validation layers automatically on every push to `main` and on every pull request. Check the Actions tab for results.

## PR Checklist

Before submitting a pull request for a new skill:

- [ ] Skill directory created under `skills/` with a descriptive hyphenated name
- [ ] `SKILL.md` has complete frontmatter with all six keys
- [ ] `SKILL.md` has all seven required body sections
- [ ] `metadata.safety` is set to `read-only` or `read-write` as appropriate
- [ ] `references/` directory exists with at least one reference file
- [ ] `agentskills validate skills/your-skill-name` passes
- [ ] `bash scripts/validate.sh` passes
- [ ] Skill catalog table in `README.md` updated with the new skill row
- [ ] Commit messages are clear and descriptive

## Questions?

Open an issue if you're unsure about format conventions or safety tier classification. Include the skill name and a brief description of what it does.
