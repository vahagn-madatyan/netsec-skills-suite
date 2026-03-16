# Project

## What This Is

A comprehensive suite of agentic AI skills for network engineering and security, distributed as a public monorepo via skills.sh. Each skill is a SKILL.md file following the Agent Skills open standard (agentskills.io), encoding deep procedural knowledge — protocol state reasoning, threshold tables, decision trees, and report templates — that any AI coding agent can consume.

The suite fills a major gap in the skills.sh ecosystem: zero network engineering or infrastructure security skills exist today. NetClaw proved the concept (82 skills on OpenClaw), but is locked to one agent framework and distributed via a fragile bash installer. This project delivers the same depth of domain knowledge in an agent-agnostic, properly packaged format that works with Claude Code, Codex, Cursor, Windsurf, Copilot, and Gemini CLI.

## Core Value

Deep network engineering and security expertise encoded as portable, agent-agnostic SKILL.md files — installable in one command via `npx skills add`.

## Current State

Empty repo with Apache-2.0 license and planning artifacts. No skills written yet.

## Architecture / Key Patterns

- **Monorepo layout:** `skills/<skill-name>/SKILL.md` with optional `references/` subdirectories
- **SKILL.md format:** YAML frontmatter (name, description, safety tier metadata) + markdown body (procedures, thresholds, decision trees, report templates)
- **Safety tiers:** Each skill tagged `safety: read-only` or `safety: read-write` in frontmatter metadata
- **Tool-agnostic:** Skills describe WHAT to do, not HOW — no dependency on specific MCP servers or automation libraries
- **Progressive disclosure:** Tier 1 (name+description ~100 tokens) → Tier 2 (full SKILL.md body <5000 tokens) → Tier 3 (reference files on demand)
- **Distribution:** `npx skills add owner/repo` via skills.sh, GitHub Actions CI validation
- **Vendor coverage:** Multi-vendor (Cisco, Juniper, Arista, Palo Alto, Fortinet, Check Point) + cloud (AWS, Azure, GCP)

## Capability Contract

See `.gsd/REQUIREMENTS.md` for the explicit capability contract, requirement status, and coverage mapping.

## Milestone Sequence

- [ ] M001: Foundation & Network Device Skills — monorepo scaffold, validation CI, 15+ network device and routing protocol skills
- [ ] M002: Security Skills — firewall auditing, compliance frameworks, vulnerability management, incident response
- [ ] M003: Cloud, Infrastructure & Observability — cloud networking, SOT integration, monitoring, log analysis
