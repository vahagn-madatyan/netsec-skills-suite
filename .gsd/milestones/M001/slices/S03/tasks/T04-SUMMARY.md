---
id: T04
parent: S03
milestone: M001
provides:
  - IS-IS protocol analysis skill with 3-vendor (Cisco/JunOS/EOS) labeling
  - README catalog updated with all 4 routing protocol skills (bgp, ospf, eigrp, isis)
  - S03 slice completed — all 8 skills pass validation
key_files:
  - skills/isis-analysis/SKILL.md
  - skills/isis-analysis/references/cli-reference.md
  - skills/isis-analysis/references/state-machine.md
  - README.md
key_decisions:
  - IS-IS state-machine.md covers DIS election comparison table (DIS vs OSPF DR) since this is the most common point of confusion for engineers transitioning between protocols
patterns_established:
  - IS-IS 3-state adjacency FSM (Down/Init/Up) is simpler than OSPF's 7-state FSM — state-machine.md compensates by covering LSPDB flooding (CSNP/PSNP) and DIS mechanics in more depth
  - IS-IS SKILL.md at 2496 words confirms all 4 routing protocol skills fit within the 2700-word budget
observability_surfaces:
  - "agentskills validate skills/isis-analysis — frontmatter spec compliance"
  - "bash scripts/validate.sh — all 8 skills PASS, 0 errors"
  - "grep -c vendor labels in SKILL.md — 16 vendor labels across 5 procedure steps"
  - "grep -c 4 new skill names in README.md — 4 (one per routing protocol)"
duration: 15m
verification_result: passed
completed_at: 2026-03-16
blocker_discovered: false
---

# T04: Write IS-IS analysis skill and update README catalog

**Created IS-IS protocol analysis skill with 3-vendor Cisco/JunOS/EOS labeling, LSPDB analysis, level 1/2 routing, DIS election, and NET validation — then updated README with all 4 new routing protocol skills, completing S03.**

## What Happened

Created `skills/isis-analysis/` with SKILL.md, cli-reference.md, and state-machine.md following the 3-vendor pattern proven in T01 (BGP) and T02 (OSPF).

IS-IS SKILL.md (2496 words) has 5 procedure steps: Instance/Interface Inventory → Adjacency Assessment → NET Address Validation → LSPDB Analysis → Level 1/2 Routing and Route Leaking. Each step uses `[Cisco]`/`[JunOS]`/`[EOS]` labels with 1 command per vendor. Two decision trees cover adjacency-not-forming (level mismatch, hello params, circuit type, DIS election, MTU) and LSPDB inconsistency (purges, system ID conflict, MTU flooding, partition, overload bit).

The cli-reference.md has 5 categories (Instance/Process, Adjacency, LSPDB, Interface, Route/Topology) with vendor-specific notes including the Cisco `show isis` vs `show clns` distinction.

The state-machine.md covers IS-IS's simpler 3-state adjacency FSM (Down→Init→Up) but compensates with extensive DIS election mechanics (preemptive vs OSPF non-preemptive, DIS vs DR comparison table), LSPDB flooding (CSNP/PSNP exchange on broadcast vs P2P), LSP lifecycle (generation, refresh, purge, fragmentation), and level 1/2 interaction (attached bit, route leaking, area boundaries).

Updated README.md with 4 new catalog rows: bgp-analysis, ospf-analysis, eigrp-analysis, isis-analysis — all with `read-only` safety tier, placed after the device health skills.

## Verification

All must-haves verified:

- `agentskills validate skills/isis-analysis` → "Valid skill" (exit 0) ✓
- IS-IS body word count: 2496 ≤ 2700 ✓
- `bash scripts/validate.sh` → 8 skills checked, 0 errors, PASS ✓
- `grep -c 'bgp-analysis|ospf-analysis|eigrp-analysis|isis-analysis' README.md` → 4 ✓
- All 7 H2 sections present: When to Use, Prerequisites, Procedure, Threshold Tables, Decision Trees, Report Template, Troubleshooting ✓
- 16 vendor labels (`[Cisco]`/`[JunOS]`/`[EOS]`) across procedure steps ✓
- references/ directory with 2 files (cli-reference.md, state-machine.md) ✓

Slice-level verification (S03 complete):
- `agentskills validate skills/bgp-analysis` → exit 0 ✓
- `agentskills validate skills/ospf-analysis` → exit 0 ✓
- `agentskills validate skills/eigrp-analysis` → exit 0 ✓
- `agentskills validate skills/isis-analysis` → exit 0 ✓
- `bash scripts/validate.sh` → 8 skills PASS, 0 errors ✓
- README contains all 4 new catalog rows ✓
- All frontmatter has `metadata.safety: read-only` ✓

## Diagnostics

- Validate IS-IS: `agentskills validate skills/isis-analysis`
- Validate all: `bash scripts/validate.sh`
- Check word count: `awk 'BEGIN{c=0}/^---$/{c++;if(c==2){f=1;next}}f{print}' skills/isis-analysis/SKILL.md | wc -w`
- Check vendor labels: `grep -c '\[Cisco\]\|\[JunOS\]\|\[EOS\]' skills/isis-analysis/SKILL.md`
- Inspect H2 sections: `grep '^## ' skills/isis-analysis/SKILL.md`
- Check README catalog: `grep 'isis-analysis\|bgp-analysis\|ospf-analysis\|eigrp-analysis' README.md`

## Deviations

None — all steps executed as planned.

## Known Issues

None.

## Files Created/Modified

- `skills/isis-analysis/SKILL.md` — IS-IS protocol analysis skill with 3-vendor labeling (2496 words)
- `skills/isis-analysis/references/cli-reference.md` — 3-vendor IS-IS CLI command tables (5 categories)
- `skills/isis-analysis/references/state-machine.md` — IS-IS adjacency FSM, DIS election, LSPDB flooding, level interaction
- `README.md` — Added 4 routing protocol skill catalog rows (8 total skills)
- `.gsd/milestones/M001/slices/S03/tasks/T04-PLAN.md` — Added Observability Impact section (pre-flight fix)
- `.gsd/milestones/M001/slices/S03/S03-PLAN.md` — Marked T04 as `[x]`
