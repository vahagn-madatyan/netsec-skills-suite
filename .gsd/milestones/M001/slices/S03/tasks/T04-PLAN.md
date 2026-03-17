---
estimated_steps: 6
estimated_files: 4
---

# T04: Write IS-IS analysis skill and update README catalog

**Slice:** S03 — Routing Protocol Analysis Suite
**Milestone:** M001

## Description

Create the IS-IS analysis skill (final routing protocol) and update README.md with all 4 new skill catalog rows. IS-IS uses the 3-vendor `[Cisco]`/`[JunOS]`/`[EOS]` pattern proven in T01/T02. IS-IS has unique concepts — NET addressing, level 1/2 routing, DIS election (not DR/BDR like OSPF), LSPDB with LSP lifetime/sequence/purge mechanics.

The README update adds bgp-analysis, ospf-analysis, eigrp-analysis, and isis-analysis to the Skill Catalog table, closing the slice.

**Relevant decisions:** D003 (tool-agnostic), D004 (deep procedural), D005 (references/), D009 (layout), D014 (README usage example style)

## Steps

1. Create directory structure: `skills/isis-analysis/` with `references/` subdirectory.

2. Write `skills/isis-analysis/SKILL.md` with:
   - **Frontmatter:** `name: isis-analysis`, `description` (IS-IS adjacency diagnosis, LSPDB analysis, level 1/2 routing, NET validation — multi-vendor Cisco/JunOS/EOS), `license: Apache-2.0`, `metadata.safety: read-only`, `metadata.author: network-security-skills-suite`, `metadata.version: "1.0.0"`
   - **H1 title:** `# IS-IS Protocol Analysis`
   - **Intro paragraph:** Protocol-reasoning-driven analysis for IS-IS. 3-vendor labeling convention.
   - **## When to Use** (~100 words): Adjacency not forming, unexpected route changes, level 1/2 boundary issues, LSPDB inconsistency, NET address conflict, post-change verification
   - **## Prerequisites** (~80 words): Device access, IS-IS enabled, awareness of level topology (L1, L2, L1/L2), system IDs and NETs known
   - **## Procedure** (~1400 words, 5-6 H3 steps): `[Cisco]`/`[JunOS]`/`[EOS]` labels, 1 command per vendor per step.
     - Step 1: IS-IS Instance & Interface Inventory — verify IS-IS running, check enabled interfaces, NET address, level configuration (L1/L2/L1L2)
     - Step 2: Adjacency Assessment — list all adjacencies, compare against expected topology, check state (Up/Init/Down), verify level matching (L1 neighbors must share area; L2 neighbors can be different areas), DIS election status on broadcast segments
     - Step 3: NET Address Validation — verify NET format (AFI.area.systemID.NSEL), check for system ID uniqueness, confirm area addresses match for L1 adjacencies
     - Step 4: LSPDB Analysis — check LSP count, LSP remaining lifetime (max 1200s default, refresh at 900s), sequence numbers (monotonically increasing), check for LSP purges (indicates instability), compare LSPDB across neighbors for consistency
     - Step 5: Level 1/2 Routing & Route Leaking — verify L1→L2 route redistribution behavior, check for route leaking L2→L1 if configured, verify attached bit on L1/L2 routers, check for suboptimal routing through L1/L2 boundaries
   - **## Threshold Tables** (~300 words): Operational parameters — hello interval defaults (10s LAN, 10s P2P for Cisco; varies by vendor), LSP lifetime default (1200s), CSNP interval (10s), PSNP interval (2s), SPF throttle timers, expected LSPDB sizes
   - **## Decision Trees** (~500 words): Two trees:
     - **Adjacency Not Forming:** check level match (L1 needs same area; L2 any area) → check hello parameters (interval, multiplier, auth) → check interface type (P2P vs broadcast → DIS election) → check MTU → check circuit type mismatch
     - **LSPDB Inconsistency:** LSP purge seen → check for system ID conflict → check for MTU preventing LSP flooding → check for partition (L2 backbone split) → check for overloaded bit set
   - **## Report Template** (~150 words): Structured IS-IS analysis findings format
   - **## Troubleshooting** (~200 words): Common issues — system ID conflict (causes LSP wars), area mismatch preventing L1 adjacency, metric style mismatch (narrow vs wide), authentication mismatch, LSPDB overload from excessive redistribution

3. Write `skills/isis-analysis/references/cli-reference.md`:
   - 3-column tables: Cisco | JunOS | EOS
   - Categories: Instance/Process, Adjacency, LSPDB, Interface, Route/Topology
   - Interpretation notes per category, especially Cisco `show isis` vs `show clns` variations

4. Write `skills/isis-analysis/references/state-machine.md`:
   - IS-IS adjacency states: Down → Initializing → Up (P2P) or Down → Initializing → Up (DIS election on broadcast)
   - DIS election mechanics (highest priority, then highest SNPA/MAC)
   - LSPDB flooding: CSNP/PSNP exchange, LSP generation, refresh, purge, and lifetime
   - Level 1/2 interaction: attached bit, route leaking, area boundaries

5. Update `README.md`:
   - Add 4 new rows to the Skill Catalog table, after the existing device health rows:
     ```
     | [bgp-analysis](skills/bgp-analysis/SKILL.md) | BGP protocol analysis — peer state diagnosis, path selection, route filtering, convergence (Cisco/JunOS/EOS) | `read-only` |
     | [ospf-analysis](skills/ospf-analysis/SKILL.md) | OSPF adjacency diagnosis, area design validation, LSA analysis, SPF convergence (Cisco/JunOS/EOS) | `read-only` |
     | [eigrp-analysis](skills/eigrp-analysis/SKILL.md) | EIGRP DUAL analysis — successor/feasible successor, stuck-in-active diagnosis, K-value validation (Cisco IOS-XE/NX-OS) | `read-only` |
     | [isis-analysis](skills/isis-analysis/SKILL.md) | IS-IS adjacency diagnosis, LSPDB analysis, level 1/2 routing, NET validation (Cisco/JunOS/EOS) | `read-only` |
     ```
   - Ensure rows are inserted in the table after `arista-device-health` and before the closing `>` note

6. Verify (full slice verification):
   - `agentskills validate skills/isis-analysis` → exit 0
   - IS-IS body word count ≤ 2700
   - `bash scripts/validate.sh` → ALL 8 skills PASS (4 existing + 4 new), 0 errors
   - README contains all 4 new catalog rows (grep for each skill name)

## Must-Haves

- [ ] IS-IS SKILL.md has all 6 frontmatter keys with `name: isis-analysis` and `metadata.safety: read-only`
- [ ] All 7 required H2 sections present in IS-IS skill
- [ ] IS-IS procedure uses `[Cisco]`/`[JunOS]`/`[EOS]` labels with max 1 command per vendor per step
- [ ] Decision trees encode adjacency and LSPDB diagnostic reasoning
- [ ] IS-IS body word count ≤ 2700
- [ ] `references/cli-reference.md` has 3-vendor IS-IS command tables
- [ ] `references/state-machine.md` has IS-IS adjacency states and LSPDB flooding mechanics
- [ ] README.md updated with 4 new routing protocol skill catalog rows
- [ ] `bash scripts/validate.sh` → all 8 skills PASS, 0 errors (full validation)

## Verification

- `agentskills validate skills/isis-analysis` → "Valid skill" (exit 0)
- `awk 'BEGIN{c=0}/^---$/{c++;if(c==2){f=1;next}}f{print}' skills/isis-analysis/SKILL.md | wc -w` → ≤ 2700
- `bash scripts/validate.sh` → 8 skills checked, 0 errors, PASS
- `grep -c 'bgp-analysis\|ospf-analysis\|eigrp-analysis\|isis-analysis' README.md` → 4 (one per skill)

## Inputs

- `skills/bgp-analysis/SKILL.md` — T01's proven 3-vendor pattern (replicate for IS-IS)
- `skills/ospf-analysis/SKILL.md` — T02's link-state protocol pattern (IS-IS is also link-state, similar structure)
- `README.md` — Current catalog table with 4 existing skills (add 4 new rows after the last device health row)
- `scripts/validate.sh` — Validator for final full-suite verification

## Observability Impact

- **Validation signals:** `agentskills validate skills/isis-analysis` exit code confirms frontmatter spec compliance. `bash scripts/validate.sh` checks all 8 skills including IS-IS for metadata.safety, required H2 sections, and references/ directory.
- **Word budget signal:** `awk 'BEGIN{c=0}/^---$/{c++;if(c==2){f=1;next}}f{print}' skills/isis-analysis/SKILL.md | wc -w` — must be ≤ 2700.
- **Vendor label count:** `grep -c '\[Cisco\]\|\[JunOS\]\|\[EOS\]' skills/isis-analysis/SKILL.md` — confirms 3-vendor labeling coverage in procedure.
- **README catalog completeness:** `grep -c 'bgp-analysis\|ospf-analysis\|eigrp-analysis\|isis-analysis' README.md` — must be 4 (one per new skill).
- **Failure visibility:** `validate.sh` emits per-skill `ERROR:` lines for missing sections, invalid safety tier, or absent `references/` directory. Missing README rows are detectable by grep count < 4.
- **Inspection surfaces:** Each SKILL.md body can be inspected with `grep '^## '` for section presence. Reference files can be checked with `ls skills/isis-analysis/references/`.

## Expected Output

- `skills/isis-analysis/SKILL.md` — IS-IS protocol analysis skill with 3-vendor labeling, ≤2700 word body
- `skills/isis-analysis/references/cli-reference.md` — Full 3-vendor IS-IS CLI command tables
- `skills/isis-analysis/references/state-machine.md` — IS-IS adjacency states, LSPDB flooding, level interaction
- `README.md` — Updated with 4 new routing protocol skill catalog rows (8 total skills in catalog)
