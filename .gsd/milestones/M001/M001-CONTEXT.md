# M001: Foundation & Network Device Skills — Context

**Gathered:** 2026-03-15
**Status:** Ready for planning

## Project Description

A comprehensive monorepo of agentic AI skills for network engineering, distributed via skills.sh. M001 establishes the monorepo foundation, validation pipeline, and delivers the first 15+ network device and routing protocol skills — covering multi-vendor health checks (Cisco, Juniper, Arista), all major routing protocols (BGP, OSPF, EIGRP, IS-IS), and network operations workflows.

## Why This Milestone

No network engineering skills exist on skills.sh today. This milestone fills the gap with a properly structured, validated, multi-vendor skill set that establishes the repo as the go-to source for network/security AI skills. The foundation (scaffold, CI, templates) must be solid because M002 and M003 build on it.

## User-Visible Outcome

### When this milestone is complete, the user can:

- Run `npx skills add <owner>/network-security-skills-suite` and install any or all network skills into their AI coding agent
- Open a Cisco/Juniper/Arista health check skill and get guided through a full device triage with thresholds, decision trees, and structured report output
- Use routing protocol skills to diagnose BGP peer failures, OSPF stuck states, EIGRP SIA conditions with protocol state machine reasoning
- Use network operations skills for topology discovery, config drift detection, and change verification workflows

### Entry point / environment

- Entry point: `npx skills add <owner>/network-security-skills-suite`
- Environment: Any AI coding agent (Claude Code, Codex, Cursor, Windsurf, Copilot, Gemini CLI)
- Live dependencies involved: none (skills are markdown files — no runtime dependencies)

## Completion Class

- Contract complete means: All SKILL.md files pass validation, frontmatter is correct, required sections present, names match directories
- Integration complete means: Skills install correctly via `npx skills add` and are discoverable by agents
- Operational complete means: none (static files, no runtime)

## Final Integrated Acceptance

To call this milestone complete, we must prove:

- `npx skills add` successfully discovers and presents all skills for installation
- GitHub Actions CI passes on all SKILL.md files (frontmatter schema, naming, required sections)
- At least one skill from each slice is manually loaded by an agent and produces useful guidance (not just boilerplate)

## Risks and Unknowns

- **Domain knowledge depth** — encoding CCIE-level protocol reasoning in markdown requires deep expertise; risk of skills being too shallow to be useful
- **SKILL.md format constraints** — the 5000-token recommended limit may be tight for skills with threshold tables + decision trees + report templates; may need to lean heavily on references/
- **Validation tooling** — skills-ref Python library may not cover our custom metadata (safety tier); may need custom validation

## Existing Codebase / Prior Art

- `compass_artifact_wf-3c00d46c-*.md` — Detailed skills.sh publishing guide, SKILL.md format reference, monorepo conventions
- `compass_artifact_wf-c0136c8b-*.md` — NetClaw deep analysis, 82 skill inventory, domain coverage, safety model analysis
- NetClaw (`github.com/automateyournetwork/netclaw`) — Reference for network skill content structure, threshold tables, protocol reasoning patterns

> See `.gsd/DECISIONS.md` for all architectural and pattern decisions — it is an append-only register; read it during planning, append to it during execution.

## Relevant Requirements

- R001-R005 — Foundation (scaffold, templates, CI, README, CONTRIBUTING)
- R006-R008 — Multi-vendor device health checks
- R009-R012 — Routing protocol analysis suite
- R013-R016 — Network operations and change management

## Scope

### In Scope

- Monorepo scaffold (skills/ directory, package.json, CI)
- SKILL.md template with safety tier metadata convention
- GitHub Actions validation pipeline
- README, CONTRIBUTING, LICENSE
- 3 vendor-specific device health check skills (Cisco, Juniper, Arista)
- 4 routing protocol analysis skills (BGP, OSPF, EIGRP, IS-IS)
- 4 network operations skills (topology, config management, interface health, change verification)
- Bundled reference files for each skill
- Multi-vendor CLI reference tables where applicable

### Out of Scope / Non-Goals

- MCP server implementations (skills only)
- Security/firewall skills (M002)
- Cloud networking skills (M003)
- Agent runtime or orchestration
- Automated testing of skill procedures against live devices

## Technical Constraints

- SKILL.md body should target <5000 tokens for progressive disclosure efficiency
- Frontmatter must use only the 6 allowed top-level keys (name, description, license, compatibility, metadata, allowed-tools)
- Safety tier goes in `metadata.safety` field (advisory, not enforced)
- Skill directory names must be kebab-case, match the `name` frontmatter field
- Reference files go in `references/` subdirectory per skill

## Integration Points

- **skills.sh CLI** — `npx skills add` discovers SKILL.md files recursively in the repo
- **Agent Skills spec** — agentskills.io defines the format; our skills must be fully compliant
- **GitHub Actions** — CI validation on push to main and PRs
- **skills-ref** — Python validation library for SKILL.md format checking

## Open Questions

- **Token budget per skill** — Need to test whether deep procedural skills fit in 5000 tokens or need to offload more to references/. Will resolve during S02 when writing the first real skill.
- **Validation strictness** — How much custom validation beyond skills-ref is worth building? Will determine in S01.
