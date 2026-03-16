# M003: Cloud, Infrastructure & Observability — Context

**Gathered:** 2026-03-15
**Status:** Ready for planning (pending M002 completion)

## Project Description

Third milestone of the network security skills suite. Delivers 8-10 skills covering cloud networking (AWS, Azure, GCP), cloud security posture assessment, source-of-truth integration (NetBox/Nautobot), IPAM/DNS management, monitoring (Grafana/Prometheus), log analysis, and network incident response workflows.

## Why This Milestone

Cloud networking and observability complete the suite's coverage. Modern networks span on-prem and cloud — engineers need skills that cover both. Infrastructure management (SOT, IPAM/DNS) and observability (monitoring, logging) are the operational backbone that ties network and security together.

## User-Visible Outcome

### When this milestone is complete, the user can:

- Audit and troubleshoot cloud networking across all three major providers (AWS, Azure, GCP)
- Assess cloud security posture with IAM, encryption, and public exposure analysis
- Reconcile network inventory between source-of-truth systems and live devices
- Build and validate monitoring dashboards and alert rules
- Follow structured incident response workflows from detection through post-mortem

### Entry point / environment

- Entry point: `npx skills add <owner>/network-security-skills-suite` (same repo)
- Environment: Any AI coding agent
- Live dependencies involved: none

## Completion Class

- Contract complete means: All cloud/infra/observability SKILL.md files pass validation
- Integration complete means: Full suite (M001 + M002 + M003, ~40-50 skills) installs cleanly
- Operational complete means: none

## Final Integrated Acceptance

To call this milestone complete, we must prove:

- All skills pass CI validation
- Cloud skills cover provider-specific constructs (VPC, TGW, VNet, NSG), not generic cloud advice
- The complete suite (~40-50 skills) installs via `npx skills add` without conflicts
- README catalog table is complete with all skills listed and categorized

## Risks and Unknowns

- **Cloud provider API churn** — AWS/Azure/GCP networking features evolve rapidly; skills may need frequent updates
- **SOT integration depth** — NetBox and Nautobot have different APIs and data models; making a useful skill without being tool-specific is challenging
- **Suite size** — 40-50 skills in one repo may be unwieldy for skills.sh discovery; may need to evaluate splitting

## Existing Codebase / Prior Art

- M001 + M002 skills — established patterns, templates, conventions
- NetClaw's AWS/GCP skills — reference for cloud networking skill structure
- NetClaw's NetBox/Nautobot/Grafana skills — reference for infrastructure skills

> See `.gsd/DECISIONS.md` for all architectural and pattern decisions.

## Relevant Requirements

- R030-R032 — Cloud networking (AWS, Azure, GCP)
- R033 — Cloud security posture
- R034-R035 — NetBox/Nautobot SOT, IPAM/DNS
- R036-R038 — Grafana/Prometheus, log analysis, incident response

## Scope

### In Scope

- 3 cloud networking skills (AWS, Azure, GCP)
- 1 cloud security posture assessment skill
- 2 infrastructure management skills (SOT, IPAM/DNS)
- 3 observability skills (monitoring, log analysis, incident response)
- Final README polish with complete skill catalog

### Out of Scope / Non-Goals

- Cloud-specific MCP servers or CLI wrappers
- Multi-cloud orchestration or Terraform/IaC skills
- Application performance monitoring (APM)

## Technical Constraints

- Cloud skills must be provider-specific (not generic "cloud" advice) while maintaining the tool-agnostic approach
- SOT skills should work conceptually with both NetBox and Nautobot
- Maintain all conventions from M001/M002

## Integration Points

- M001 network skills — cloud skills may reference on-prem networking concepts
- M002 security skills — cloud security posture skill complements firewall and compliance skills
- NetBox/Nautobot APIs — skills describe operations against these platforms
- Grafana/Prometheus — skills describe dashboard and query patterns

## Open Questions

- **Repo split** — Should cloud skills be a separate repo for cleaner skills.sh presentation, or keep everything in one monorepo? Defer to M003 planning.
- **Cloud freshness** — How to handle cloud provider changes over time? May need a maintenance strategy.
