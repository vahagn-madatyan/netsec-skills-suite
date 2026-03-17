---
estimated_steps: 5
estimated_files: 3
---

# T01: Write BGP analysis skill with 3-vendor pattern proof

**Slice:** S03 — Routing Protocol Analysis Suite
**Milestone:** M001

## Description

Create the BGP analysis skill — the most complex routing protocol skill and the pattern proof for 3-vendor (`[Cisco]`/`[JunOS]`/`[EOS]`) labeling. BGP encodes the deepest diagnostic reasoning: FSM state interpretation, path selection analysis, route filtering validation, and convergence assessment. This task proves that 3-vendor code blocks remain scannable within the ~2700 word budget before committing to the pattern for OSPF and IS-IS.

The key shift from S02's device health skills: health checks are command-driven ("run this, check that threshold"), but routing protocol skills are reasoning-driven ("the peer is stuck in Active state → TCP connection succeeds but no OPEN received → check remote BGP config, ACLs, or peer AS mismatch"). The procedure must encode the reasoning chain, not just the command sequence.

**Relevant decisions:**
- D003: Tool-agnostic — describe WHAT to check and WHY, not which tool to use
- D004: Deep procedural — threshold tables, decision trees, report templates
- D005: References in references/ subdirectory for progressive disclosure
- D009: skills/<kebab-name>/SKILL.md layout

**Relevant skills for executor:** None needed — this is markdown content authoring following established patterns.

## Steps

1. Create directory structure: `skills/bgp-analysis/` with `references/` subdirectory.

2. Write `skills/bgp-analysis/SKILL.md` with:
   - **Frontmatter:** 6 keys exactly — `name: bgp-analysis`, `description` (BGP protocol analysis with peer state diagnosis, path selection, route filtering, convergence — multi-vendor Cisco/JunOS/EOS), `license: Apache-2.0`, `metadata.safety: read-only`, `metadata.author: network-security-skills-suite`, `metadata.version: "1.0.0"`
   - **H1 title:** `# BGP Protocol Analysis`
   - **Introductory paragraph:** Explain this is a protocol-reasoning-driven analysis skill, not a health check. Note the 3-vendor labeling convention.
   - **## When to Use** (~100 words): BGP peer down/stuck, route leak suspected, path selection not as expected, convergence too slow, post-change verification of BGP config, capacity planning for table size growth
   - **## Prerequisites** (~80 words): SSH/console access, BGP enabled, knowledge of expected peer topology, awareness of configured policies (route-maps, prefix-lists, community filters)
   - **## Procedure** (~1400 words, 5-6 H3 steps): Each step uses `**[Cisco]**` / `**[JunOS]**` / `**[EOS]**` labels with ONE command per vendor per step. Steps should follow this diagnostic flow:
     - Step 1: BGP Session Inventory — collect all peer states, compare against expected topology
     - Step 2: Peer State Diagnosis — for any non-Established peer, interpret FSM state (Idle = no route to peer or admin down; Connect/Active = TCP failing; OpenSent = OPEN sent, no response; OpenConfirm = OPEN parameter mismatch). This step encodes the core reasoning chain.
     - Step 3: Route Table Analysis — check received/advertised prefix counts, best path selection, unexpected paths
     - Step 4: Path Selection Verification — walk the BGP best path algorithm (Weight → Local Preference → Originate → AS Path Length → Origin → MED → eBGP over iBGP → IGP metric → Router ID). Identify which attribute is selecting the current best.
     - Step 5: Route Filtering Validation — verify route-maps, prefix-lists, community filters are applying as intended. Check for route leaks (routes in table that shouldn't be).
     - Step 6: Convergence Assessment — check for route flapping (dampening state), table churn, convergence time after changes
   - **## Threshold Tables** (~300 words): Operational parameter norms, NOT resource thresholds. Include: default hold/keepalive timers (60/180 Cisco, 90/270 JunOS), expected table sizes by deployment type (edge ~10K, full table ~950K), convergence time targets, prefix-limit guidelines.
   - **## Decision Trees** (~500 words): The core diagnostic value. Two trees:
     - **Peer Not Established:** State → Idle (admin down? no route? AS mismatch?) → Active (TCP fails? ACL? firewall?) → OpenSent (remote not responding? version mismatch?) → OpenConfirm (capability mismatch? AFI/SAFI?) → Established but dropping (hold timer? keepalive?)
     - **Unexpected Route Selection:** Check path attributes in best-path order → identify which attribute is causing unexpected selection → common issues (missing route-map, stale MED, unexpected weight)
   - **## Report Template** (~150 words): Structured output format for BGP analysis findings
   - **## Troubleshooting** (~200 words): Common issues — session flapping, route oscillation, memory pressure from full table, community stripping

3. Write `skills/bgp-analysis/references/cli-reference.md`:
   - 3-column tables organized by diagnostic category: Session Management, Route Table, Path Attributes, Filtering, Convergence/Dampening
   - Columns: Cisco IOS-XE/NX-OS | JunOS | EOS
   - Include both show commands and common operational commands
   - Add interpretation notes per category explaining vendor-specific output differences

4. Write `skills/bgp-analysis/references/state-machine.md`:
   - BGP FSM: Idle → Connect → Active → OpenSent → OpenConfirm → Established
   - Each state: definition, entry conditions, exit transitions, common stuck-state causes
   - Timer interactions: ConnectRetry, Hold, Keepalive
   - Event-driven transitions: TCP connect success/fail, OPEN received, KEEPALIVE received, NOTIFICATION received

5. Verify:
   - Run `agentskills validate skills/bgp-analysis` → expect exit 0
   - Run body word count: `awk 'BEGIN{c=0}/^---$/{c++;if(c==2){f=1;next}}f{print}' skills/bgp-analysis/SKILL.md | wc -w` → expect ≤ 2700
   - Run `bash scripts/validate.sh` → expect bgp-analysis checks all OK

## Must-Haves

- [ ] SKILL.md has all 6 frontmatter keys with `name: bgp-analysis` and `metadata.safety: read-only`
- [ ] All 7 required H2 sections present: When to Use, Prerequisites, Procedure, Threshold Tables, Decision Trees, Report Template, Troubleshooting
- [ ] Procedure uses `[Cisco]`/`[JunOS]`/`[EOS]` labels with max 1 command per vendor per step
- [ ] Decision trees encode diagnostic reasoning chains, not just command lists
- [ ] Body word count ≤ 2700
- [ ] `references/cli-reference.md` has 3-vendor command tables
- [ ] `references/state-machine.md` has full BGP FSM with stuck-state causes
- [ ] `agentskills validate skills/bgp-analysis` exits 0
- [ ] `bash scripts/validate.sh` shows bgp-analysis PASS

## Verification

- `agentskills validate skills/bgp-analysis` → "Valid skill" (exit 0)
- `awk 'BEGIN{c=0}/^---$/{c++;if(c==2){f=1;next}}f{print}' skills/bgp-analysis/SKILL.md | wc -w` → ≤ 2700
- `bash scripts/validate.sh` → bgp-analysis: all checks OK, overall PASS

## Observability Impact

- **New validation signal:** `agentskills validate skills/bgp-analysis` — exit 0 confirms frontmatter schema and structural validity
- **Word budget check:** `awk 'BEGIN{c=0}/^---$/{c++;if(c==2){f=1;next}}f{print}' skills/bgp-analysis/SKILL.md | wc -w` → must be ≤ 2700
- **Vendor label coverage:** `grep -c '\[Cisco\]\|\[JunOS\]\|\[EOS\]' skills/bgp-analysis/SKILL.md` — confirms 3-vendor labeling throughout procedure
- **Failure visibility:** `bash scripts/validate.sh` emits `ERROR:` lines per missing section or invalid safety value — failures are self-describing
- **Inspection surface:** `references/cli-reference.md` and `references/state-machine.md` can be `cat`/`wc` inspected for completeness

## Inputs

- `skills/cisco-device-health/SKILL.md` — Reference for frontmatter schema, H2 section names, and `[IOS-XE]`/`[NX-OS]` labeling pattern (adapt to `[Cisco]`/`[JunOS]`/`[EOS]` for 3-vendor)
- `skills/cisco-device-health/references/cli-reference.md` — Reference for CLI table format
- `scripts/validate.sh` — Validator that will check this skill (required H2 sections, safety tier, references/ presence)
- S01 established: 7 required H2 section names that validate.sh checks for literally
- S02 established: `[IOS-XE]`/`[NX-OS]` dual-platform labeling; adapt to `[Cisco]`/`[JunOS]`/`[EOS]` for 3-vendor routing protocols

## Expected Output

- `skills/bgp-analysis/SKILL.md` — BGP protocol analysis skill with 3-vendor labeling, protocol-first reasoning, ≤2700 word body
- `skills/bgp-analysis/references/cli-reference.md` — Full 3-vendor BGP CLI command tables
- `skills/bgp-analysis/references/state-machine.md` — BGP FSM states, transitions, stuck-state causes
