# M001/S03 — Research

**Date:** 2026-03-16

## Summary

S03 delivers 4 routing protocol analysis skills (BGP, OSPF, EIGRP, IS-IS) that encode protocol state machine reasoning with multi-vendor CLI coverage. The primary challenge is the shift from S02's "health check" pattern (run commands → compare thresholds) to a "protocol analysis" pattern (reason about protocol state machines → diagnose adjacency/convergence issues). The secondary challenge is 3-vendor CLI coverage (Cisco/JunOS/EOS) in BGP, OSPF, and IS-IS without blowing the ~2700 word budget.

S02's forward intelligence explicitly flags this: "S03's multi-vendor routing skills will need a similar approach but across 3 vendors — consider whether 3-way labeled blocks remain scannable or need a different structure." The answer is: **protocol-first procedures with selective inline vendor examples, full vendor CLI tables offloaded to references/**. Routing protocol analysis is fundamentally about understanding protocol behavior (FSM states, adjacency requirements, metric calculations), not about running vendor-specific show commands. The procedure body should encode the reasoning; the CLI commands are the tool, not the diagnosis.

EIGRP is the simplest skill — Cisco-only protocol, no multi-vendor concern. BGP is the most complex and proves the 3-vendor pattern. Build BGP first as the pattern proof, then OSPF, IS-IS, and EIGRP.

## Recommendation

**Protocol-first procedure structure** with inline vendor examples limited to 1 key command per vendor per step. Full 3-vendor command tables in `references/cli-reference.md`. Protocol state machine detail in a new `references/state-machine.md` reference file (BGP FSM, OSPF FSM, EIGRP DUAL, IS-IS adjacency states). This keeps SKILL.md body focused on diagnostic reasoning while still being actionable across vendors.

The rationale: S02's health check skills are command-driven — "run this, check that threshold." Routing protocol skills are reasoning-driven — "the peer is stuck in Active state, which means OpenSent succeeded but OpenConfirm failed, which means OPEN message parameters disagree." The procedure must encode the reasoning chain, not just the command sequence. Vendor CLI is a means to an end.

Use `**[Cisco]**` / `**[JunOS]**` / `**[EOS]**` labels consistent with S02's `**[IOS-XE]**` / `**[NX-OS]**` pattern, but show only the primary diagnostic command per vendor per step. This keeps 3-vendor procedure steps to ~6 lines of code blocks rather than ~15.

## Implementation Landscape

### Key Files

Per-skill structure (4 skills × 3 files each = 12 new files + README update):

- `skills/bgp-analysis/SKILL.md` — BGP protocol analysis with peer state diagnosis, path selection, route filtering, convergence assessment. Multi-vendor (Cisco/JunOS/EOS).
- `skills/bgp-analysis/references/cli-reference.md` — 3-vendor BGP CLI command tables organized by diagnostic category
- `skills/bgp-analysis/references/state-machine.md` — BGP FSM (Idle→Connect→Active→OpenSent→OpenConfirm→Established) with transition triggers and failure modes
- `skills/ospf-analysis/SKILL.md` — OSPF adjacency diagnosis, area design validation, LSA analysis, SPF convergence. Multi-vendor.
- `skills/ospf-analysis/references/cli-reference.md` — 3-vendor OSPF CLI tables
- `skills/ospf-analysis/references/state-machine.md` — OSPF neighbor FSM (Down→Init→2-Way→ExStart→Exchange→Loading→Full) with stuck-state diagnosis
- `skills/eigrp-analysis/SKILL.md` — EIGRP DUAL analysis, successor/feasible successor, stuck-in-active, K-values. Cisco-only.
- `skills/eigrp-analysis/references/cli-reference.md` — Cisco EIGRP CLI tables (IOS-XE and NX-OS)
- `skills/eigrp-analysis/references/state-machine.md` — DUAL FSM and feasibility condition math
- `skills/isis-analysis/SKILL.md` — IS-IS adjacency diagnosis, LSPDB analysis, level 1/2 routing, NET validation. Multi-vendor.
- `skills/isis-analysis/references/cli-reference.md` — 3-vendor IS-IS CLI tables
- `skills/isis-analysis/references/state-machine.md` — IS-IS adjacency states and LSPDB flooding mechanics
- `README.md` — Add 4 new rows to skill catalog table

### Reference File Convention

S01/S02 established `cli-reference.md` and `threshold-tables.md` as the standard reference files. S03 replaces `threshold-tables.md` with `state-machine.md` because routing protocol skills are about state reasoning, not resource thresholds. The threshold concept doesn't apply the same way — BGP timers are configuration, not health thresholds. Protocol state machines are the core reference material that overflows from the SKILL.md body.

This is consistent with D005 (references/ for progressive disclosure) and the CONTRIBUTING guide (references/ subdirectory per skill, no filename constraints).

### Skill Body Structure (all 4 skills)

Each SKILL.md follows the 7 required H2 sections from S01:

1. **When to Use** — Protocol-specific trigger conditions (peer down, stuck state, route leak, convergence issue)
2. **Prerequisites** — Device access, protocol version, topology awareness
3. **Procedure** — Protocol-reasoning-driven steps with selective inline vendor CLI
4. **Threshold Tables** — Protocol-specific operational parameters (timer defaults, table size norms, convergence targets) — kept as an H2 even though deeper data is in state-machine.md
5. **Decision Trees** — Protocol state diagnosis trees (the core value of these skills)
6. **Report Template** — Protocol analysis report format
7. **Troubleshooting** — Common protocol-specific issues and resolutions

### Multi-Vendor Labeling (BGP, OSPF, IS-IS)

Inside procedure steps, use selective 3-vendor code blocks:

```markdown
### Step 2: Peer State Assessment

Check the current state of all BGP peers against expected topology.

**[Cisco]**
\`\`\`
show ip bgp summary
\`\`\`

**[JunOS]**
\`\`\`
show bgp summary
\`\`\`

**[EOS]**
\`\`\`
show ip bgp summary
\`\`\`

A numeric value in State/PfxRcd = Established. Any text = not established.
Interpret the state against the BGP FSM...
```

One command per vendor per step. Full command inventory (neighbor detail, route specifics, filtering, etc.) in `references/cli-reference.md`.

### EIGRP Exception

EIGRP is Cisco-proprietary. Use `**[IOS-XE]**` / `**[NX-OS]**` dual-platform labels from S02's Cisco pattern (D015). No JunOS or EOS coverage.

### Build Order

1. **BGP first** — Most complex protocol, most needed (R009: "BGP is the internet's routing protocol"), and proves the 3-vendor pattern. If the 3-vendor labeling is scannable and fits the word budget at BGP complexity, all other skills will fit.
2. **OSPF second** — Most common IGP (R010), same 3-vendor challenge as BGP but simpler state machine. Reuses proven pattern from BGP.
3. **EIGRP third** — Cisco-only (R011), simplest multi-vendor challenge (dual-platform only). DUAL FSM is unique and interesting but no vendor-variation risk.
4. **IS-IS fourth** — Similar structure to OSPF but different state model (R012). 3-vendor coverage. By this point the pattern is proven 3x.
5. **README update** — Add all 4 skills to catalog table. Can be done as part of the last task or as a final step.

BGP is the gating proof point. If it works, the rest is pattern application.

### Token Budget Strategy

S02 proved ~2700 words fits. Routing protocol skills have more conceptual depth but fewer inline commands (offloaded to references/). Budget allocation per skill:

- When to Use: ~100 words
- Prerequisites: ~80 words  
- Procedure (5-6 steps): ~1400 words (protocol reasoning + selective inline commands)
- Threshold Tables: ~300 words (timer defaults, table size norms)
- Decision Trees: ~500 words (protocol state diagnosis — the core value)
- Report Template: ~150 words
- Troubleshooting: ~200 words
- **Total: ~2730 words** — tight but within budget

If BGP exceeds budget, reduce inline vendor examples to 2 vendors (Cisco + JunOS, EOS in references only) or compress troubleshooting. Measure BGP first before committing to a pattern for all 4.

### Verification Approach

Same verification stack as S02:

1. `agentskills validate skills/bgp-analysis` (and each other skill) → exit 0
2. `bash scripts/validate.sh` → all skills PASS, 0 errors
3. Word count per SKILL.md body ≤ 2700
4. README.md contains 4 new catalog rows with correct skill names and `read-only` safety tier
5. Each skill has `references/` with `cli-reference.md` and `state-machine.md`

Note: `scripts/validate.sh` checks for `references/` directory existence and file count, but doesn't enforce specific filenames. The switch from `threshold-tables.md` to `state-machine.md` won't break validation.

## Constraints

- **~2700 word body limit** — proven in S02 but routing protocol skills have deeper reasoning to encode. 3-vendor inline commands consume more budget than 2-platform. Offloading CLI to references/ is mandatory.
- **7 required H2 sections** — `scripts/validate.sh` checks for exactly these H2 names. All 4 skills must include "Threshold Tables" as an H2 even though the concept maps differently for protocols (timer/table norms rather than resource thresholds).
- **Frontmatter schema** — 6 keys exactly: name, description, license, metadata (safety, author, version). Name must match directory name (kebab-case).
- **Safety tier** — All 4 skills are `read-only` (protocol analysis is observation-only).
- **Tool-agnostic** (D003) — Skills describe WHAT to check and WHY, not which tool to use. No pyATS, Netmiko, or MCP server references.

## Common Pitfalls

- **Protocol analysis ≠ health check** — Don't just list show commands with thresholds. The value of these skills is encoding the diagnostic reasoning chain: "peer in Active state → TCP connection succeeds but no OPEN received → check remote BGP config, ACLs, or peer AS mismatch." Without the reasoning, these are just CLI cheat sheets.
- **3-vendor code block explosion** — Showing every relevant command for 3 vendors inline makes procedure steps 80% code blocks and 20% reasoning. Limit inline to 1 command per vendor per step; put the full command inventory in references/.
- **"Threshold Tables" section mismatch** — Routing protocols don't have resource thresholds like CPU/memory. This section should contain operational parameter norms (BGP hold timer defaults, OSPF dead interval norms, expected route table sizes) — reframe as "operational parameters" content under the required "Threshold Tables" heading.
- **EIGRP vendor scope** — EIGRP is Cisco-proprietary but runs on both IOS-XE and NX-OS. Don't label it "single vendor" — use the S02 dual-platform `[IOS-XE]`/`[NX-OS]` pattern.

## Open Risks

- **3-vendor readability** — The 3-vendor labeled code block pattern hasn't been proven yet. BGP (task 1) must validate that procedure steps with `[Cisco]`/`[JunOS]`/`[EOS]` blocks remain scannable. If not, fall back to single representative vendor inline with full vendor matrix in references only.
- **BGP word budget** — BGP is the most complex protocol with the most procedure steps (peer state, path selection, route filtering, convergence). It may exceed 2700 words even with aggressive CLI offloading. Measure after writing; adjust pattern if needed before OSPF/IS-IS.

## Skills Discovered

| Technology | Skill | Status |
|------------|-------|--------|
| BGP routing | `zebbern/secops-cli-guides@bgp-routing-protocol` | available — 5 installs, not relevant (generic CLI guide, not protocol analysis) |
| Routing protocols | `automateyournetwork/netclaw@pyats-routing` | available — 8 installs, not relevant (pyATS-specific, violates D003 tool-agnostic) |
| Network analysis | `wshobson/agents@protocol-reverse-engineering` | available — 3.1K installs, not relevant (protocol reverse engineering, different domain) |

No skills installed — none are relevant to protocol state machine analysis skills.
