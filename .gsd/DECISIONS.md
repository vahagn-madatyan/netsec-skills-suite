# Decisions Register

<!-- Append-only. Never edit or remove existing rows.
     To reverse a decision, add a new row that supersedes it.
     Read this file at the start of any planning or research phase. -->

| # | When | Scope | Decision | Choice | Rationale | Revisable? |
|---|------|-------|----------|--------|-----------|------------|
| D001 | M001 | arch | Skill distribution format | SKILL.md via skills.sh (npx skills add) | Agent Skills open standard, 26+ platform adoption, zero publishing friction | No |
| D002 | M001 | arch | Safety tier mechanism | Advisory metadata tag (metadata.safety: read-only/read-write) | User chose advisory over structural separation; agents can respect it optionally | Yes — if enforcement needed |
| D003 | M001 | arch | Tool dependency approach | Tool-agnostic (skills describe WHAT, agent decides HOW) | Maximum portability; no coupling to pyATS, Netmiko, or specific MCP servers | No |
| D004 | M001 | arch | Skill depth model | Deep procedural (threshold tables, decision trees, report templates) | Match NetClaw quality; shallow how-to guides don't differentiate from docs | No |
| D005 | M001 | arch | Reference file strategy | Bundled in references/ subdirectory per skill | Progressive disclosure tier 3; keeps SKILL.md body under ~5000 tokens | Yes — if token budget changes |
| D006 | M001 | scope | MCP server scope | Skills only — no MCP server implementations | User explicitly chose skills-only; MCP servers are separate concern | Yes — if demand emerges |
| D007 | M001 | scope | Target user | Network/security engineer + AI agent pair | Skills augment human workflow, not autonomous unattended operation | No |
| D008 | M001 | scope | Vendor coverage strategy | Multi-vendor breadth (Cisco, Juniper, Arista, Palo Alto, Fortinet, Check Point) | Fill ecosystem gap wide rather than going deep on one vendor | No |
| D009 | M001 | convention | Monorepo layout | skills/<kebab-name>/SKILL.md with optional references/ | Matches skills.sh discovery convention and agentskills.io spec | No |
| D010 | M001 | convention | License | Apache-2.0 | Already in repo, matches NetClaw and most skills ecosystem | No |
| D011 | M001/S01 | convention | agentskills validate invocation | Per-skill-directory, not parent skills/ dir | agentskills CLI only accepts individual skill dirs; custom script and CI iterate over skills/* | No |
| D012 | M001/S01 | convention | CI action pinning | checkout@v4, setup-python@v5, skills-ref==0.1.1 | Reproducible builds; avoid surprise breakage from upstream changes | Yes — update pins periodically |
| D013 | M001/S01 | convention | CI permissions | contents: read (least privilege) | No write access needed for validation-only workflow | Yes — if CI needs write |
| D014 | M001/S01 | convention | README usage example style | Multi-step realistic agent triage interaction | Demonstrates how skills drive agent behavior end-to-end, not just install | No |
