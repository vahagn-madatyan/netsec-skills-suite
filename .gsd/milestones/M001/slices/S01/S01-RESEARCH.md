# S01: Monorepo Foundation & Skill Templates — Research

**Date:** 2026-03-15

## Summary

This slice establishes the repo scaffold, SKILL.md template, CI pipeline, README, and CONTRIBUTING guide. Research confirms the skills.sh ecosystem is simpler than initially spec'd — no package.json or pnpm workspace is needed. Anthropic's own skills repo (`anthropics/skills`) is pure markdown with a `skills/` directory. The `skills-ref` Python library (v0.1.1) validates only frontmatter (6 allowed keys, name format, description presence) — it does NOT validate body sections, custom metadata values, or file structure. We need a thin custom validation layer on top for our requirements: safety tier values, required body sections, and references/ directory presence.

The confirmed zero-network-skills gap on skills.sh validates this project's value proposition. The only "network" skills found are app-layer libraries (Flutter/iOS networking, hybrid cloud), not infrastructure device/protocol skills. The niche is wide open.

The critical design tension is between the Agent Skills spec's minimalism (arbitrary metadata, no enforced body structure) and our need for consistency across 40+ skills (safety tiers, threshold tables, decision trees, report templates). Resolution: enforce our conventions through CI, not through the spec — our custom validator checks what `skills-ref` can't.

## Recommendation

Build a minimal pure-markdown repo with `skills/` directory convention, a two-layer CI validation pipeline (`skills-ref` for spec compliance + custom bash/python script for our conventions), and a skeleton example skill (`skills/example-device-health/`) that proves the full pipeline end-to-end. Skip pnpm workspace setup — it's unnecessary for a markdown-only repo and adds tooling friction for zero benefit.

The skeleton skill should be a realistic device health check (not a toy) so it can double as the template AND validate that deep procedural content fits within the ~5000 token body budget. Delete it before S02 starts or keep it as a template reference in `_templates/`.

## Don't Hand-Roll

| Problem | Existing Solution | Why Use It |
|---------|------------------|------------|
| SKILL.md frontmatter validation | `skills-ref` (pip install skills-ref, `agentskills validate`) | Official Anthropic library, validates all 6 frontmatter fields, name format, directory match. Catches the spec-level errors. |
| Skill scaffolding | `npx skills init <name>` | Generates correct SKILL.md stub with frontmatter. Use as starting point for template. |
| Skill discovery testing | `npx skills add <path> --list` | Confirms skills.sh CLI discovers all skills in the repo without installing. Use in CI for integration check. |
| YAML frontmatter parsing | `strictyaml` (transitive dep of skills-ref) | Already installed. If custom validator needs to parse frontmatter, import from skills-ref internals or use strictyaml directly. |

## Existing Code and Patterns

- `compass_artifact_wf-3c00d46c-*.md` — Complete skills.sh publishing guide. Key facts: 6 allowed frontmatter keys, metadata is arbitrary key-value map, progressive disclosure tiers (catalog ~100 tokens, body <5000 tokens, references on-demand), no publish step needed.
- `compass_artifact_wf-c0136c8b-*.md` — NetClaw analysis. 82 skills, SKILL.md with YAML frontmatter, threshold tables, decision trees, report templates in body. Validates that deep procedural markdown works for network engineering.
- `/tmp/anthropic-skills/skills/` — Anthropic's official skills repo. Pure markdown, no package.json, `skills/<name>/SKILL.md` convention. 17 skills. References pattern used in `gha-security-review` (9 reference files). This is our structural model.
- `/tmp/sentry-skills/plugins/sentry-skills/skills/` — Sentry's skills repo. Uses `plugins/` prefix but same SKILL.md convention. No SKILL.md validation CI — they rely on Warden (AI code review). Shows the gap: even major publishers don't validate skills in CI.
- `skills-ref` source (`validator.py`) — Validates: name lowercase/kebab-case/max-64/matches-dir, description non-empty/max-1024, only 6 allowed top-level keys, compatibility max-500. Does NOT validate: body content, metadata values, file structure, references/ presence.

## Constraints

- **6 allowed frontmatter keys only**: name, description, license, compatibility, metadata, allowed-tools. Any extra top-level key fails `skills-ref` validation. Safety tier MUST go in `metadata.safety`, not as a top-level key.
- **Name must match directory**: `skills-ref` enforces `name` field == parent directory name. Kebab-case, lowercase, 1-64 chars, no consecutive hyphens, no leading/trailing hyphens.
- **Description max 1024 chars**: Must describe what the skill does AND when to use it — this is the agent's trigger mechanism.
- **No package.json required**: skills.sh CLI scans recursively for SKILL.md files. Anthropic/Sentry/Vercel skills repos have no package.json. Adding one is optional (for npm metadata) but not functionally needed.
- **Body target <5000 tokens, <500 lines**: Agent Skills spec recommendation. Deep procedural skills with threshold tables + decision trees will push this limit. References/ is the overflow valve.
- **`metadata` value type**: The spec says `map[string→string]` but `skills-ref` actually accepts nested maps (tested: `metadata.safety: read-only` passes as nested YAML). This is important — it means our `metadata.safety` convention works as-is.
- **GitHub Actions runners**: Ubuntu-latest has Python 3 and pip. `skills-ref` has only 2 deps (click, strictyaml). Install is fast (<5s).

## Common Pitfalls

- **Over-engineering the scaffold** — This is a markdown repo, not a TypeScript project. No build step, no bundler, no pnpm workspace. Every file that isn't SKILL.md or CI config is friction. The R001 requirement mentioning "pnpm workspace" is over-specified for a markdown-only repo.
- **Relying solely on skills-ref for quality** — `skills-ref` catches spec violations but not domain quality. A skill with valid frontmatter but empty body, no threshold tables, or wrong safety tier passes validation. Custom checks are essential.
- **Description too short or too generic** — The description is the ONLY trigger mechanism. "Cisco device health check" is too terse. Must include trigger phrases: "Use when troubleshooting Cisco IOS-XE or NX-OS devices, checking CPU/memory utilization, interface errors, routing table health, or performing device triage."
- **Token budget surprises** — Need to measure actual token count of the skeleton skill body during this slice. If a realistic device health check body exceeds 5000 tokens, we need to establish the references/ offload pattern here, not discover it in S02.
- **Forgetting to test `npx skills add`** — CI validates file format, but integration testing requires verifying `npx skills add . --list` discovers all skills. This should be a CI step or at minimum a manual verification during this slice.

## Open Risks

- **Custom validation maintenance** — Our custom CI checks (safety tier values, required sections, references/ presence) are not enforced by the spec. If the spec evolves, we'll need to update both layers. Low risk given spec stability.
- **Token measurement accuracy** — The 5000-token target is approximate. Different tokenizers (Claude, GPT-4, etc.) count differently. We should measure with `tiktoken` (cl100k_base) as a reasonable proxy, but actual token consumption depends on which agent loads the skill.
- **skills-ref stability** — Version 0.1.1, described as "intended for demonstration purposes only." It may change validation rules. Pin the version in CI. If it breaks, our custom validator can serve as fallback since we're already writing one.
- **README/CONTRIBUTING scope creep** — These docs need to be useful for S01 but will be updated in S02-S04 as skills are added. Write them for the current state (skeleton + conventions), not for the final 15+ skill catalog.

## Skills Discovered

| Technology | Skill | Status |
|------------|-------|--------|
| GitHub Actions CI | `~/.gsd/agent/skills/github-workflows/` | already installed (bundled) |
| Network engineering skills | none on skills.sh | confirmed gap — no relevant skills exist |
| SKILL.md format / Agent Skills | skills-ref Python library | installed locally (pip), used for validation |

No external skills to install — this is foundational work using the Agent Skills spec directly. The bundled `github-workflows` skill covers CI authoring.

## Requirements Coverage

This slice owns R001–R005:

| Req | Title | Key Research Findings |
|-----|-------|-----------------------|
| R001 | Monorepo scaffold | No pnpm workspace needed — pure markdown repo with `skills/<name>/SKILL.md`. Anthropic's model confirms this. Need: `skills/` dir convention, `.gitignore`, LICENSE (already exists). Optional: minimal `package.json` for GitHub metadata. |
| R002 | SKILL.md template with safety tier | Template needs: frontmatter (name, description, license, metadata.safety, metadata.author, metadata.version), body sections (When to Use, Prerequisites, Procedure, Threshold Tables, Decision Trees, Report Template, Troubleshooting). Safety goes in `metadata.safety: read-only \| read-write`. |
| R003 | GitHub Actions CI | Two-layer: `skills-ref` for spec compliance + custom script for our conventions (safety tier values, required sections, references/ dir). Pin `skills-ref==0.1.1`. Run on push to main and PRs. |
| R004 | README | Install commands (`npx skills add <owner>/network-security-skills-suite`), skill catalog table (name, description, safety tier), usage examples, badges. Start minimal — S02-S04 will add skills to the catalog. |
| R005 | CONTRIBUTING guide | SKILL.md format reference, safety tier convention, reference file patterns, validation instructions, PR process. Include the template from R002 as the canonical reference. |

## Sources

- Agent Skills specification — formal SKILL.md format, 6 allowed frontmatter keys, progressive disclosure model (source: `/tmp/agentskills/docs/specification.mdx`)
- Agent Skills best practices — description optimization, progressive disclosure, context budget management (source: `/tmp/agentskills/docs/skill-creation/best-practices.mdx`)
- skills-ref v0.1.1 validator source — exact validation rules, name regex, allowed fields set (source: `skills_ref/validator.py`)
- Anthropic skills repo — structural model, pure markdown, no package.json (source: `github.com/anthropics/skills`)
- Sentry skills repo — reference file patterns, real-world monorepo structure (source: `github.com/getsentry/skills`)
- Compass artifact (skills.sh guide) — complete publishing pipeline, CLI commands, cross-platform compatibility (source: `compass_artifact_wf-3c00d46c-*.md`)
- Compass artifact (NetClaw analysis) — 82 network skills structure, threshold/decision-tree patterns, token budget evidence (source: `compass_artifact_wf-c0136c8b-*.md`)
- `npx skills add /tmp/mock-repo --list` — confirmed recursive SKILL.md discovery works from `skills/` subdirectory
- `agentskills validate` testing — confirmed validation behavior for: valid skill, uppercase name, name mismatch, missing description, unknown top-level key
