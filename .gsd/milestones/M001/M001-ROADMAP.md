# M001: Foundation & Network Device Skills

**Vision:** Establish the monorepo foundation and deliver 15+ network device skills that fill the complete gap in the skills.sh ecosystem — multi-vendor device health checks, routing protocol analysis with state machine reasoning, and network operations workflows. Every skill encodes deep procedural knowledge with threshold tables, decision trees, and report templates.

## Success Criteria

- `npx skills add` discovers and installs all skills from the repo
- GitHub Actions CI validates all SKILL.md files on every push (frontmatter, naming, sections)
- 15+ skills covering Cisco, Juniper, and Arista across device health, routing protocols, and network ops
- Every skill has safety tier metadata, threshold tables, decision trees, and structured report templates
- Skills are agent-agnostic — no dependency on specific tools or MCP servers
- Bundled reference files provide progressive disclosure depth

## Key Risks / Unknowns

- **Deep procedural content within token budget** — SKILL.md body target is <5000 tokens; encoding CCIE-level protocol reasoning with thresholds and decision trees may not fit without heavy use of references/
- **Multi-vendor CLI variation** — Same protocol (e.g., BGP) has very different CLI across Cisco/Juniper/Arista; skills must be useful regardless of vendor without being so abstract they're useless
- **Validation tooling gaps** — skills-ref may not validate our custom metadata fields (safety tier)

## Proof Strategy

- **Token budget** → retire in S02 by writing the first real device health skill and measuring token count. If over budget, establish the references/ offload pattern.
- **Multi-vendor CLI variation** → retire in S03 by writing BGP skill with vendor-specific sections and verifying it reads well for each vendor
- **Validation gaps** → retire in S01 by building the CI pipeline and testing against a skeleton skill with custom metadata

## Verification Classes

- Contract verification: SKILL.md frontmatter schema validation, directory naming checks, required section presence, safety tier metadata presence
- Integration verification: `npx skills add` installs skills correctly into agent skill directories
- Operational verification: none (static markdown files)
- UAT / human verification: Load a skill into a real agent session and confirm it provides useful, deep guidance (not boilerplate)

## Milestone Definition of Done

This milestone is complete only when all are true:

- All 15+ SKILL.md files pass GitHub Actions CI validation
- Every skill has: safety tier metadata, threshold tables, decision trees, report template, references/ subdirectory
- `npx skills add <owner>/network-security-skills-suite` discovers and presents all skills for selection
- README has install commands, skill catalog table with descriptions and safety tiers, usage examples
- CONTRIBUTING guide documents the SKILL.md format and contribution process
- At least one skill per slice has been loaded into an agent and produces non-trivial guidance
- All success criteria re-verified against the actual repo state

## Requirement Coverage

- Covers: R001, R002, R003, R004, R005, R006, R007, R008, R009, R010, R011, R012, R013, R014, R015, R016
- Partially covers: none
- Leaves for later: R017-R038 (M002, M003)
- Orphan risks: none

## Slices

- [x] **S01: Monorepo Foundation & Skill Templates** `risk:low` `depends:[]`
  > After this: repo has skills/ directory convention, SKILL.md template with safety tier metadata, GitHub Actions CI that catches malformed skills, README with install commands, CONTRIBUTING guide. A skeleton example skill validates the full pipeline.

- [x] **S02: Multi-Vendor Device Health Checks** `risk:medium` `depends:[S01]`
  > After this: 3 deep procedural health check skills (Cisco IOS-XE/NX-OS, Juniper JunOS, Arista EOS) with vendor-specific thresholds, decision trees, and structured report templates. Token budget pattern established.

- [x] **S03: Routing Protocol Analysis Suite** `risk:high` `depends:[S01]`
  > After this: 4 routing protocol skills (BGP, OSPF, EIGRP, IS-IS) with protocol state machine reasoning, multi-vendor CLI reference tables, adjacency diagnosis decision trees, and convergence analysis. Multi-vendor abstraction pattern proven.

- [ ] **S04: Network Operations & Change Management** `risk:medium` `depends:[S01,S02]`
  > After this: 4 network operations skills (topology discovery, config management/drift detection, interface health monitoring, change pre/post verification). Complete M001 skill set validated end-to-end via `npx skills add`.

## Boundary Map

### S01 → S02, S03, S04

Produces:
- `skills/` directory convention — kebab-case dirs, each with SKILL.md
- SKILL.md template — frontmatter schema (name, description, license, metadata.safety, metadata.author, metadata.version), body sections (When to Use, Prerequisites, Procedure, Threshold Tables, Decision Trees, Report Template, Troubleshooting)
- `references/` subdirectory convention — per-skill reference files for progressive disclosure
- `.github/workflows/validate.yml` — CI pipeline that validates all SKILL.md files
- `README.md` — install commands, skill catalog table, usage examples
- `CONTRIBUTING.md` — skill authoring guide, format reference, PR process
- Safety tier convention — `metadata.safety: read-only | read-write` in frontmatter

Consumes:
- nothing (first slice)

### S02 → S04

Produces:
- `skills/cisco-device-health/` — Cisco IOS-XE/NX-OS health check skill with SKILL.md + references/
- `skills/juniper-device-health/` — Juniper JunOS health check skill with SKILL.md + references/
- `skills/arista-device-health/` — Arista EOS health check skill with SKILL.md + references/
- Established pattern: vendor-specific threshold tables, decision tree format, report template format
- Proven token budget: SKILL.md body within ~5000 tokens, overflow to references/

Consumes from S01:
- SKILL.md template structure
- Safety tier metadata convention
- references/ subdirectory convention
- CI validation pipeline

### S03 → S04

Produces:
- `skills/bgp-analysis/` — BGP protocol analysis skill with SKILL.md + references/
- `skills/ospf-analysis/` — OSPF protocol analysis skill with SKILL.md + references/
- `skills/eigrp-analysis/` — EIGRP protocol analysis skill with SKILL.md + references/
- `skills/isis-analysis/` — IS-IS protocol analysis skill with SKILL.md + references/
- Established pattern: multi-vendor CLI reference tables, protocol state machine encoding, adjacency diagnosis trees

Consumes from S01:
- SKILL.md template structure
- Safety tier metadata convention
- references/ subdirectory convention
- CI validation pipeline

### S04 (final)

Produces:
- `skills/network-topology-discovery/` — topology discovery skill
- `skills/config-management/` — config management and drift detection skill
- `skills/interface-health/` — interface and link health monitoring skill
- `skills/change-verification/` — pre/post change verification skill
- Updated README.md — complete skill catalog for M001
- Final validation: all 15+ skills pass CI, `npx skills add` works end-to-end

Consumes from S01:
- SKILL.md template, CI pipeline, README structure
Consumes from S02:
- Threshold table and decision tree patterns (reused in interface health skill)
- Vendor-specific section pattern (reused in topology and config skills)
