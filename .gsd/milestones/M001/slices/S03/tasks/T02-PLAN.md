---
estimated_steps: 5
estimated_files: 3
---

# T02: Write OSPF analysis skill reusing 3-vendor pattern

**Slice:** S03 — Routing Protocol Analysis Suite
**Milestone:** M001

## Description

Create the OSPF analysis skill — the most common enterprise IGP. Reuses the 3-vendor (`[Cisco]`/`[JunOS]`/`[EOS]`) labeling pattern established and proven in T01 (BGP). OSPF has a different and more granular FSM (Down→Init→2-Way→ExStart→Exchange→Loading→Full) where stuck-state diagnosis is the core value — ExStart stuck = MTU mismatch or DR/BDR election issue, Exchange stuck = LSDB too large to synchronize.

Follow the same structural pattern as T01's BGP skill: protocol-first reasoning in the procedure, selective 1-command-per-vendor inline CLI, full vendor tables in references/cli-reference.md, FSM detail in references/state-machine.md.

**Relevant decisions:** D003 (tool-agnostic), D004 (deep procedural), D005 (references/ overflow), D009 (skill layout)

## Steps

1. Create directory structure: `skills/ospf-analysis/` with `references/` subdirectory.

2. Write `skills/ospf-analysis/SKILL.md` with:
   - **Frontmatter:** `name: ospf-analysis`, `description` (OSPF adjacency diagnosis, area design validation, LSA analysis, SPF convergence — multi-vendor Cisco/JunOS/EOS), `license: Apache-2.0`, `metadata.safety: read-only`, `metadata.author: network-security-skills-suite`, `metadata.version: "1.0.0"`
   - **H1 title:** `# OSPF Protocol Analysis`
   - **Intro paragraph:** Protocol-reasoning-driven analysis for OSPF. 3-vendor labeling convention.
   - **## When to Use** (~100 words): Adjacency not forming or stuck, unexpected route changes, area design review, SPF running too frequently, post-change verification of OSPF config, LSDB growing unexpectedly
   - **## Prerequisites** (~80 words): Device access, OSPF enabled, awareness of area topology and expected neighbor relationships, router IDs known
   - **## Procedure** (~1400 words, 5-6 H3 steps): `[Cisco]`/`[JunOS]`/`[EOS]` labels, 1 command per vendor per step.
     - Step 1: OSPF Instance & Interface Inventory — verify OSPF is running, check which interfaces participate, area assignments
     - Step 2: Neighbor State Assessment — list all neighbors, compare against expected topology, interpret FSM state for non-Full neighbors (Init = hellos received but not bidirectional; 2-Way = bidirectional but not adjacent; ExStart = DR/BDR election or MTU mismatch; Exchange = LSDB sync issue; Loading = incomplete LSDB sync)
     - Step 3: Area Design Validation — verify backbone connectivity (area 0 contiguous or virtual links), stub/NSSA configuration consistency, ABR/ASBR identification
     - Step 4: LSDB Analysis — check LSA types (1-Router, 2-Network, 3-Summary, 4-ASBR, 5-External, 7-NSSA), LSA age (max 3600s, refresh at 1800s), LSA count per area, identify unexpected external LSAs
     - Step 5: SPF Convergence Assessment — SPF run count and frequency, SPF throttle timers, route installation time, check for frequent SPF triggers (unstable link, flapping interface)
   - **## Threshold Tables** (~300 words): Operational parameter norms — hello/dead interval defaults (10/40 broadcast, 30/120 NBMA), expected LSA counts by network size, SPF run frequency norms, LSA age thresholds
   - **## Decision Trees** (~500 words): Two trees:
     - **Adjacency Not Forming:** stuck state → Init (hellos not bidirectional → area mismatch, auth mismatch, ACL blocking) → ExStart (MTU mismatch → compare MTU both sides) → Exchange (LSDB too large → check area scope) → Loading (DB description incomplete → check stability)
     - **Unexpected Routes/Missing Routes:** check LSDB for LSA presence → check area type (stub filters Type 5) → check ABR summarization → check route redistribution → check SPF calculation
   - **## Report Template** (~150 words): Structured OSPF analysis findings format
   - **## Troubleshooting** (~200 words): Common issues — MTU mismatch (most common ExStart stuck cause), duplicate router IDs, area 0 discontinuity, excessive redistribution, Type 7 to Type 5 translation issues

3. Write `skills/ospf-analysis/references/cli-reference.md`:
   - 3-column tables: Cisco | JunOS | EOS
   - Categories: Interface & Instance, Neighbor/Adjacency, LSDB, SPF/Route, Area Config
   - Interpretation notes per category

4. Write `skills/ospf-analysis/references/state-machine.md`:
   - OSPF neighbor FSM: Down → Attempt → Init → 2-Way → ExStart → Exchange → Loading → Full
   - Each state: definition, entry conditions, exit transitions, stuck-state causes and fixes
   - DR/BDR election interaction with adjacency formation
   - LSDB synchronization process (DBD, LSR, LSU, LSAck exchange)

5. Verify:
   - `agentskills validate skills/ospf-analysis` → exit 0
   - Body word count ≤ 2700
   - `bash scripts/validate.sh` → ospf-analysis checks all OK

## Must-Haves

- [ ] SKILL.md has all 6 frontmatter keys with `name: ospf-analysis` and `metadata.safety: read-only`
- [ ] All 7 required H2 sections present
- [ ] Procedure uses `[Cisco]`/`[JunOS]`/`[EOS]` labels with max 1 command per vendor per step
- [ ] Decision trees encode adjacency stuck-state reasoning, not just command lists
- [ ] Body word count ≤ 2700
- [ ] `references/cli-reference.md` has 3-vendor OSPF command tables
- [ ] `references/state-machine.md` has full OSPF neighbor FSM with stuck-state diagnosis
- [ ] `agentskills validate skills/ospf-analysis` exits 0

## Verification

- `agentskills validate skills/ospf-analysis` → "Valid skill" (exit 0)
- `awk 'BEGIN{c=0}/^---$/{c++;if(c==2){f=1;next}}f{print}' skills/ospf-analysis/SKILL.md | wc -w` → ≤ 2700
- `bash scripts/validate.sh` → ospf-analysis: all checks OK

## Inputs

- `skills/bgp-analysis/SKILL.md` — T01's proven 3-vendor pattern to replicate (frontmatter structure, `[Cisco]`/`[JunOS]`/`[EOS]` labeling, protocol-first reasoning approach)
- `skills/bgp-analysis/references/cli-reference.md` — Reference for CLI table format (replicate structure for OSPF)
- `skills/bgp-analysis/references/state-machine.md` — Reference for FSM documentation format (replicate for OSPF FSM)
- `scripts/validate.sh` — Validator (checks 7 H2 sections, safety tier, references/)

## Expected Output

- `skills/ospf-analysis/SKILL.md` — OSPF protocol analysis skill with 3-vendor labeling, adjacency diagnosis reasoning, ≤2700 word body
- `skills/ospf-analysis/references/cli-reference.md` — Full 3-vendor OSPF CLI command tables
- `skills/ospf-analysis/references/state-machine.md` — OSPF neighbor FSM states, transitions, stuck-state causes

## Observability Impact

- **New validation target:** `agentskills validate skills/ospf-analysis` becomes a new exit-0 check — failure means frontmatter or structure is invalid.
- **Word budget signal:** `awk 'BEGIN{c=0}/^---$/{c++;if(c==2){f=1;next}}f{print}' skills/ospf-analysis/SKILL.md | wc -w` — must return ≤ 2700. Exceeding indicates content needs to be moved to references/.
- **Aggregate validation:** `bash scripts/validate.sh` now covers ospf-analysis in addition to existing skills. Per-skill ERROR lines identify specific failures (missing H2 sections, invalid safety tier, absent references/).
- **Vendor label density:** `grep -c '\[Cisco\]\|\[JunOS\]\|\[EOS\]' skills/ospf-analysis/SKILL.md` — should return ≥10 (2+ labels per procedure step × 5 steps). Low count indicates vendor coverage gaps.
- **Failure state visibility:** If ospf-analysis is missing or malformed, `validate.sh` will emit `ERROR:` lines scoped to `ospf-analysis` — failures are self-identifying without manual inspection.
