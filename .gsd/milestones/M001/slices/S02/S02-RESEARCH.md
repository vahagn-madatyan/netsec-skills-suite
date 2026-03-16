# S02: Multi-Vendor Device Health Checks — Research

**Date:** 2026-03-15

## Summary

S02 delivers three production device health check skills (Cisco IOS-XE/NX-OS, Juniper JunOS, Arista EOS) that fill a confirmed gap — zero Juniper or Arista skills exist on skills.sh, and the only comparable Cisco skill (NetClaw's `pyats-health-check`, 9 installs) is locked to pyATS rather than tool-agnostic.

The S01 example skill (`example-device-health`) proves the token budget is comfortable: body is ~1547 tokens against a 5000-token target, leaving ample room for NX-OS additions and vendor-specific depth. Each new skill follows the identical structure — 6 frontmatter keys, 7 H2 sections, references/ subdirectory — and must pass both `agentskills validate` and `scripts/validate.sh`.

The primary technical challenge is encoding meaningful vendor-specific procedural knowledge — each vendor has a fundamentally different platform architecture (IOS-XE's QFP/RP split, JunOS's RE/PFE model, EOS's Linux-native approach) that demands distinct triage procedures and thresholds, not just different CLI syntax. Shallow command substitution would produce useless skills.

## Recommendation

Create three new skill directories alongside (not replacing) the existing `example-device-health`:

1. **`skills/cisco-device-health/`** — Full production Cisco skill covering both IOS-XE and NX-OS. Procedure uses H3 subsections to separate platform-specific commands where they diverge. Decision trees account for NX-OS's VDC architecture and different process model. This replaces the example as the "real" Cisco skill while the example remains as a contributor reference.

2. **`skills/juniper-device-health/`** — Focused on JunOS's RE/PFE health model, routing engine failover detection, chassis alarm analysis, and PFE statistics. JunOS has a more hierarchical CLI (`show chassis routing-engine` vs Cisco's `show processes cpu`) that requires its own procedure flow.

3. **`skills/arista-device-health/`** — Focused on data center health: MLAG state validation, VXLAN/EVPN health checks, and hardware monitoring via EOS's Linux-native commands. Arista's Linux accessibility means some checks use `bash` commands directly.

Token budget strategy: Keep SKILL.md body at ~2500–3500 tokens (well under 5000). Offload detailed per-subsystem CLI command tables and expanded threshold tables to references/. This matches S01's proven pattern.

Update README catalog with the three new skills. Keep `example-device-health` as-is.

## Don't Hand-Roll

| Problem | Existing Solution | Why Use It |
|---------|------------------|------------|
| SKILL.md structure | `skills/example-device-health/SKILL.md` | Reference implementation with all 6 frontmatter keys, 7 H2 sections — copy structure exactly |
| Threshold table format | `skills/example-device-health/references/threshold-tables.md` | Proven Normal/Warning/Critical/Emergency 4-tier format with action column |
| CLI reference format | `skills/example-device-health/references/cli-reference.md` | Subsystem-organized command tables with interpretation notes |
| Convention validation | `scripts/validate.sh` | Already checks safety tier, required sections, references/ — no changes needed |
| Spec validation | `agentskills validate` | Per-skill-directory invocation, catches frontmatter schema violations |

## Existing Code and Patterns

- `skills/example-device-health/SKILL.md` — The template to clone. Body structure: H1 title, 7 H2 sections with procedure using H3 steps. ~1547 tokens body, ~8.5KB total. Keep it intact as contributor reference.
- `skills/example-device-health/references/` — Two reference files (cli-reference.md, threshold-tables.md). New skills should mirror this: one CLI ref organized by subsystem, one threshold table organized by parameter category.
- `scripts/validate.sh` — Checks `metadata.safety`, 7 required H2 section names (grep-based, exact match on `## Section Name`), and `references/` directory presence. No changes needed for S02.
- `.github/workflows/validate.yml` — Iterates all `skills/*/SKILL.md`. Adding new skill directories is automatically picked up. No workflow changes needed.
- `README.md` line 27-29 — Catalog table format: `| [name](link) | description | \`safety-tier\` |`. Add three rows.

## Constraints

- **SKILL.md body must stay under ~5000 tokens** — 1.3x multiplier on word count is the rough guide. S01's example at 1190 words ≈ 1547 tokens. Target 2000-2700 words per body for deeper real skills.
- **7 H2 sections must use exact names** — `scripts/validate.sh` uses literal grep: `## When to Use`, `## Prerequisites`, `## Procedure`, `## Threshold Tables`, `## Decision Trees`, `## Report Template`, `## Troubleshooting`. Case-sensitive, no extra whitespace.
- **`metadata.safety` must be `read-only` or `read-write`** — All three device health skills are `read-only` (show commands only, no config changes).
- **`agentskills validate` per-directory** — Must run against each `skills/<name>/` individually, not `skills/`.
- **Skill directory name must be kebab-case and match frontmatter `name`** — e.g., directory `cisco-device-health` → frontmatter `name: cisco-device-health`.
- **Reference files go in `references/` subdirectory** — Must exist for validate.sh to pass.

## Common Pitfalls

- **Shallow command substitution across vendors** — Simply swapping `show processes cpu` for `show chassis routing-engine` produces useless skills. Each vendor has a different health model: IOS-XE separates RP/QFP, JunOS separates RE/PFE with explicit mastership, EOS exposes full Linux. Procedures must reflect these architectural differences in their triage logic, not just commands.
- **NX-OS vs IOS-XE conflation** — NX-OS uses `show system resources` (not `show processes cpu sorted`), has VDC isolation, different memory model, different process names. Treating them as minor CLI variants will produce incorrect thresholds and bad guidance.
- **Threshold values that are too generic** — Thresholds like "CPU > 70% = critical" need context. NX-OS control plane CPU behaves differently from IOS-XE RP CPU. JunOS RE CPU spikes during commit are normal. Thresholds must account for platform-specific normal behavior.
- **Token budget overflow in Cisco skill** — Covering both IOS-XE AND NX-OS in one SKILL.md could push the body past 5000 tokens if both platforms get full separate procedures. Strategy: shared structure with platform-specific callouts (code blocks labeled per platform), detailed per-platform commands offloaded to references/.
- **Missing `references/` directory** — validate.sh will fail the skill. Must create the directory and populate it with at least one file per skill.

## Open Risks

- **CLI command accuracy for current versions** — Commands are based on general vendor knowledge. Specific version differences (JunOS 21.x vs 23.x, EOS 4.28 vs 4.32) may have subtle CLI changes. Mitigation: target current mainstream versions (IOS-XE 17.x, NX-OS 10.x, JunOS 23.x, EOS 4.30+), note version in Prerequisites.
- **Arista MLAG/VXLAN depth vs general health** — R008 mentions MLAG and VXLAN/EVPN as Arista-specific focus areas. These are feature-specific checks beyond basic device health. Risk of the skill becoming too narrow (DC-only) or too broad (trying to cover both campus and DC). Resolution: frame it as "Arista EOS device health with DC-specific extensions" — core health first, MLAG/VXLAN as additional procedure steps.
- **Example skill disposition** — Keeping `example-device-health` alongside the real `cisco-device-health` means two Cisco-esque skills in the catalog. Could confuse users. Mitigation: the README description clearly differentiates them, and the example's description already says "example." Can defer cleanup to S04 if it becomes an issue.

## Vendor Health Check Architecture

### Cisco IOS-XE / NX-OS (R006)

**IOS-XE architecture:** RP (Route Processor) handles control plane, QFP (QuantumFlow Processor) handles data plane. Health triage must check both planes independently.
- Key commands: `show processes cpu sorted`, `show memory statistics`, `show interfaces counters errors`, `show environment all`
- Platform-specific: `show platform software status control-processor brief`, `show platform hardware qfp active statistics drop`

**NX-OS architecture:** Linux-based, Supervisor with VDC (Virtual Device Context) isolation. Different process model, different command set.
- Key commands: `show system resources`, `show processes cpu sort`, `show module`, `show environment`
- Platform-specific: `show vdc`, `show hardware capacity`, `show system internal`
- NX-OS has no `show processes cpu history` — use `show system resources` trended data instead

**Skill structure decision:** Unified SKILL.md with platform callouts (IOS-XE vs NX-OS code blocks in each procedure step). Not two separate skills — R006 explicitly says "Cisco IOS-XE/NX-OS" as one skill.

### Juniper JunOS (R007)

**JunOS architecture:** RE (Routing Engine) and PFE (Packet Forwarding Engine) are explicitly separated. Dual-RE systems have mastership and failover. Alarms are first-class.
- RE health: `show chassis routing-engine` (CPU, memory, temperature, mastership)
- PFE health: `show pfe statistics traffic`, `show chassis fpc`
- Alarms: `show chassis alarms`, `show system alarms` — JunOS surfaces alarms prominently
- System: `show system processes extensive`, `show system storage`, `show system core-dumps`
- Environment: `show chassis environment`

**Unique triage patterns:**
- RE mastership check is mandatory before any health assessment (wrong RE = wrong data)
- Alarm analysis is a first-class step (JunOS alarm severity: Major, Minor, None)
- PFE health is separate from RE health — can have healthy RE with sick PFE
- Commit history matters: `show system commit` to correlate recent changes with symptoms

### Arista EOS (R008)

**EOS architecture:** Linux-native, processes run as standard Linux daemons. Full bash access. MLAG is the primary HA mechanism. Data center focus with VXLAN/EVPN.
- System: `show processes top` (or `bash top`), `show version` (includes memory)
- Interfaces: `show interfaces counters errors`, `show interfaces status`
- MLAG: `show mlag`, `show mlag detail`, `show mlag interfaces` — MLAG state is critical
- VXLAN/EVPN: `show vxlan vtep`, `show bgp evpn summary` — DC fabric health
- Environment: `show environment all`, `show environment cooling`, `show environment power`
- Agents: `show agent` — EOS-specific, daemon health monitoring

**Unique triage patterns:**
- MLAG state check is often the single most important assessment in a DC
- Linux accessibility means `bash` commands are valid troubleshooting tools
- Agent/daemon health (`show agent`) catches EOS-specific process failures
- VXLAN/EVPN health is a DC-specific extension, not core device health

## Token Budget Analysis

| Component | Example Skill (S01) | Target per S02 Skill |
|-----------|---------------------|---------------------|
| SKILL.md body | ~1190 words / ~1547 tokens | ~2000-2700 words / ~2600-3500 tokens |
| references/cli-reference.md | ~917 words | ~800-1200 words |
| references/threshold-tables.md | ~1302 words | ~1000-1500 words |
| Total SKILL.md file size | ~8.5 KB | ~12-18 KB |

S02 skills will be deeper than the S01 example but still well within budget. The Cisco skill (covering two platforms) will be the largest; measure it first as the budget proof point.

## Deliverables Checklist

- [ ] `skills/cisco-device-health/SKILL.md` — Cisco IOS-XE + NX-OS dual-platform health check
- [ ] `skills/cisco-device-health/references/cli-reference.md` — IOS-XE and NX-OS command tables
- [ ] `skills/cisco-device-health/references/threshold-tables.md` — Platform-specific thresholds
- [ ] `skills/juniper-device-health/SKILL.md` — JunOS RE/PFE health check with alarm analysis
- [ ] `skills/juniper-device-health/references/cli-reference.md` — JunOS command tables
- [ ] `skills/juniper-device-health/references/threshold-tables.md` — JunOS-specific thresholds
- [ ] `skills/arista-device-health/SKILL.md` — Arista EOS health check with MLAG/VXLAN extensions
- [ ] `skills/arista-device-health/references/cli-reference.md` — EOS command tables
- [ ] `skills/arista-device-health/references/threshold-tables.md` — EOS-specific thresholds
- [ ] README.md catalog table updated with three new skills
- [ ] All three skills pass `agentskills validate` and `scripts/validate.sh`
- [ ] Token count measured on Cisco skill body (budget proof point)

## Skills Discovered

| Technology | Skill | Status |
|------------|-------|--------|
| Network device health | `automateyournetwork/netclaw@pyats-health-check` | available (pyATS-specific, not tool-agnostic — not relevant) |
| Cisco | `cisco-ai-defense/skill-scanner@*` | available (AI safety scanner, not network ops — not relevant) |
| Juniper | — | none found |
| Arista | — | none found |
| System health (generic) | `terrylica/cc-skills@system-health-check` | available (general system, not network device — not relevant) |

No skills installed — none are relevant to our tool-agnostic network device health check scope.

## Sources

- Example skill structure and token budget (source: `skills/example-device-health/SKILL.md` — S01 output)
- Validation requirements (source: `scripts/validate.sh` — S01 output)
- Section naming convention (source: `CONTRIBUTING.md` — S01 output)
- Skills ecosystem gap confirmed (source: `npx skills find` for "network device health check", "juniper", "arista" — all return zero relevant results)
- Requirement definitions R006-R008 (source: `.gsd/REQUIREMENTS.md`)
- S01 forward intelligence on fragile areas (source: `.gsd/milestones/M001/slices/S01/S01-SUMMARY.md`)
