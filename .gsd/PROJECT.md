# Project

## What This Is

A comprehensive suite of agentic AI skills for network engineering and security, distributed as a public monorepo via skills.sh. Each skill is a SKILL.md file following the Agent Skills open standard (agentskills.io), encoding deep procedural knowledge — protocol state reasoning, threshold tables, decision trees, and report templates — that any AI coding agent can consume.

The suite fills a major gap in the skills.sh ecosystem: zero network engineering or infrastructure security skills exist today. NetClaw proved the concept (82 skills on OpenClaw), but is locked to one agent framework and distributed via a fragile bash installer. This project delivers the same depth of domain knowledge in an agent-agnostic, properly packaged format that works with Claude Code, Codex, Cursor, Windsurf, Copilot, and Gemini CLI.

## Core Value

Deep network engineering and security expertise encoded as portable, agent-agnostic SKILL.md files — installable in one command via `npx skills add`.

## Current State

M001 complete — all 4 slices delivered 12 skills (1 example + 11 real). M002 S01 complete — delivered 4 vendor-specific firewall audit skills. M002 S02 complete — delivered 3 rule analysis and compliance skills (acl-rule-analysis, cis-benchmark-audit, nist-compliance-assessment), retiring D026 CIS copyright risk. M002 S03 complete — delivered 3 security operations skills (vulnerability-assessment, siem-log-analysis, incident-response-network), retiring M002 SIEM vendor fragmentation risk (D029). Suite now has 22 skills total, all passing `bash scripts/validate.sh` with 0 errors. R001–R026 validated. S04 (VPN, zero-trust, wireless + suite finalization) remains.

## Architecture / Key Patterns

- **Monorepo layout:** `skills/<skill-name>/SKILL.md` with optional `references/` subdirectories
- **SKILL.md format:** YAML frontmatter (name, description, safety tier metadata) + markdown body (procedures, thresholds, decision trees, report templates)
- **Safety tiers:** Each skill tagged `safety: read-only` or `safety: read-write` in frontmatter metadata. Read-write skills use inline ⚠️ WRITE markers.
- **Tool-agnostic:** Skills describe WHAT to do, not HOW — no dependency on specific MCP servers or automation libraries
- **Progressive disclosure:** Tier 1 (name+description ~100 tokens) → Tier 2 (full SKILL.md body <5000 tokens) → Tier 3 (reference files on demand)
- **Distribution:** `npx skills add owner/repo` via skills.sh, GitHub Actions CI validation
- **Vendor coverage:** Multi-vendor (Cisco, Juniper, Arista) with `[Cisco]`/`[JunOS]`/`[EOS]` inline labels; Cisco-only skills use `[IOS-XE]`/`[NX-OS]`
- **Procedure shapes:** Threshold-comparison (device health, interface health, vulnerability assessment), protocol state machine (routing), iterative seed expansion (topology discovery), event-driven lifecycle (change verification), ongoing monitoring (config management), policy audit (firewall), compliance assessment (CIS/NIST), forensic timeline (incident response, SIEM), maturity scoring (zero-trust)

## Capability Contract

See `.gsd/REQUIREMENTS.md` for the explicit capability contract, requirement status, and coverage mapping.

## Milestone Sequence

- [x] M001: Foundation & Network Device Skills — monorepo scaffold, validation CI, 12 network device, routing protocol, and operations skills
- [ ] M002: Security Skills — firewall auditing, compliance frameworks, vulnerability management, incident response
- [ ] M003: Cloud, Infrastructure & Observability — cloud networking, SOT integration, monitoring, log analysis
