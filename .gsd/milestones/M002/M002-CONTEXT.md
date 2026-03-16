# M002: Security Skills — Context

**Gathered:** 2026-03-15
**Status:** Ready for planning (pending M001 completion)

## Project Description

Second milestone of the network security skills suite. Delivers 12-15 security-focused skills covering multi-vendor firewall auditing (Palo Alto, Fortinet, Check Point, Cisco ASA/FTD), compliance frameworks (CIS benchmarks, NIST CSF/800-53), vulnerability management, SIEM integration, incident response, VPN troubleshooting, zero-trust assessment, and wireless security.

## Why This Milestone

Security skills are the second major gap in the skills.sh ecosystem. While M001 covers network device operations, M002 addresses the security operations domain — firewall policy auditing, compliance assessment, and incident response. These skills complement M001's network skills to create a comprehensive network + security suite.

## User-Visible Outcome

### When this milestone is complete, the user can:

- Install firewall audit skills for all four major vendors and get guided through policy analysis with best practice references
- Run CIS benchmark and NIST compliance assessments against network device configurations
- Use vulnerability management skills to triage CVEs and prioritize remediation
- Follow structured incident response workflows with network forensics guidance
- Assess VPN configurations, zero-trust maturity, and wireless security posture

### Entry point / environment

- Entry point: `npx skills add <owner>/network-security-skills-suite` (same repo, new skills)
- Environment: Any AI coding agent
- Live dependencies involved: none

## Completion Class

- Contract complete means: All security SKILL.md files pass validation, include bundled compliance references
- Integration complete means: Skills install alongside M001 network skills without conflicts
- Operational complete means: none

## Final Integrated Acceptance

To call this milestone complete, we must prove:

- All security skills pass CI validation
- Firewall audit skills cover vendor-specific policy analysis, not generic checklists
- Compliance skills reference actual CIS/NIST control IDs, not vague categories
- The full suite (M001 + M002) installs cleanly via `npx skills add`

## Risks and Unknowns

- **Compliance reference depth** — CIS benchmarks are copyrighted; need to reference controls by ID without reproducing full benchmark text
- **Vendor-specific firewall knowledge** — each vendor's policy model is substantially different; skills must encode real vendor expertise
- **SIEM vendor fragmentation** — making a vendor-agnostic SIEM skill useful requires careful abstraction

## Existing Codebase / Prior Art

- M001 foundation — SKILL.md template, validation CI, monorepo structure
- M001 network skills — established patterns for multi-vendor coverage, threshold tables, decision trees
- Sentry's `security-review` skill — reference for OWASP-informed security auditing patterns
- NetClaw's Cisco ASA/FMC skills — reference for firewall audit skill structure

> See `.gsd/DECISIONS.md` for all architectural and pattern decisions.

## Relevant Requirements

- R017-R020 — Multi-vendor firewall auditing
- R021-R023 — Rule analysis and compliance
- R024-R026 — Vulnerability management, SIEM, incident response
- R027-R029 — VPN, zero-trust, wireless

## Scope

### In Scope

- 4 vendor-specific firewall audit skills (Palo Alto, Fortinet, Check Point, Cisco)
- 3 compliance/governance skills (ACL optimization, CIS, NIST)
- 3 security operations skills (vulnerability management, SIEM, incident response)
- 3 additional security skills (VPN/IPSec, zero-trust, wireless)
- Bundled compliance reference files (CIS control IDs, NIST categories, OWASP references)

### Out of Scope / Non-Goals

- Cloud security (M003)
- Endpoint security (EDR, antivirus)
- Application security / code review (covered by Sentry's existing skills)
- Penetration testing tools

## Technical Constraints

- CIS benchmark content is copyrighted — reference control IDs and categories, do not reproduce full benchmark text
- Maintain the SKILL.md template and safety tier conventions established in M001
- Firewall audit skills are safety: read-only (analysis only, no policy changes)
- Config change skills (if any) must be safety: read-write

## Integration Points

- M001 foundation — uses same monorepo structure, CI pipeline, SKILL.md template
- M001 network skills — security skills may cross-reference network health skills
- CIS benchmark database — skills reference control IDs
- NVD/CVE database — vulnerability skills reference CVE identifiers

## Open Questions

- **CIS reference approach** — How much benchmark content can we include without copyright issues? Will research during M002 planning.
- **Firewall vendor depth** — How deep to go on each vendor vs. keeping skills vendor-agnostic? M001 experience will inform this.
