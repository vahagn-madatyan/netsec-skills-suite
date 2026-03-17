---
id: T02
parent: S03
milestone: M001
provides:
  - OSPF protocol analysis skill with 3-vendor (Cisco/JunOS/EOS) labeling
  - OSPF neighbor FSM reference with stuck-state diagnosis (Down→Init→2-Way→ExStart→Exchange→Loading→Full)
  - OSPF CLI reference tables and area design validation procedures
key_files:
  - skills/ospf-analysis/SKILL.md
  - skills/ospf-analysis/references/cli-reference.md
  - skills/ospf-analysis/references/state-machine.md
key_decisions:
  - OSPF procedure structured as 5 steps (Instance/Interface → Neighbor State → Area Design → LSDB → SPF) matching diagnostic reasoning flow
  - Two decision trees cover the two primary OSPF failure domains: adjacency formation and route presence/absence
patterns_established:
  - 3-vendor OSPF skill at 2229 words confirms BGP pattern (2070 words) scales to different protocol complexity within budget
  - OSPF FSM state-machine.md includes DR/BDR election and LSDB sync process as OSPF-specific additions to the FSM doc pattern
observability_surfaces:
  - "agentskills validate skills/ospf-analysis → exit 0"
  - "bash scripts/validate.sh → ospf-analysis: all checks OK (0 errors across all 6 skills)"
  - "Word count: awk body extraction → 2229 words (≤2700 budget)"
  - "Vendor labels: grep count → 16 (≥10 expected)"
duration: ~20m
verification_result: passed
completed_at: 2026-03-16
blocker_discovered: false
---

# T02: Write OSPF analysis skill reusing 3-vendor pattern

**Created OSPF protocol analysis skill with 3-vendor Cisco/JunOS/EOS labeling, neighbor FSM stuck-state diagnosis, area design validation, and LSDB analysis — reusing the pattern proven in T01 (BGP).**

## What Happened

Built the OSPF analysis skill following the exact structural pattern from T01's BGP skill. The OSPF skill has 5 procedure steps covering the full diagnostic flow: instance/interface inventory, neighbor state assessment (with per-FSM-state interpretation), area design validation (backbone contiguity, stub/NSSA consistency, ABR/ASBR identification), LSDB analysis (LSA types 1-5 and 7, age monitoring, count validation), and SPF convergence assessment. Two decision trees encode adjacency stuck-state reasoning (ExStart = MTU mismatch, Init = one-way communication) and missing/unexpected route diagnosis (LSDB presence → area type → summarization → redistribution). The cli-reference.md covers 5 categories (Interface/Instance, Neighbor/Adjacency, LSDB, SPF/Route, Area Config) with interpretation notes. The state-machine.md documents all 8 OSPF neighbor states plus DR/BDR election rules and the LSDB synchronization packet exchange.

## Verification

- `agentskills validate skills/ospf-analysis` → "Valid skill" (exit 0) ✅
- Body word count: 2229 words (≤2700 budget) ✅
- Vendor label count: 16 occurrences of [Cisco]/[JunOS]/[EOS] ✅
- All 7 H2 sections present: When to Use, Prerequisites, Procedure, Threshold Tables, Decision Trees, Report Template, Troubleshooting ✅
- `bash scripts/validate.sh` → 6 skills checked, PASS (0 errors) ✅
- references/ directory: 2 files (cli-reference.md, state-machine.md) ✅
- Frontmatter: all 6 keys present, name=ospf-analysis, metadata.safety=read-only ✅

**Slice-level verification (partial — T02 of T04):**
- `agentskills validate skills/bgp-analysis` → exit 0 ✅
- `agentskills validate skills/ospf-analysis` → exit 0 ✅
- `agentskills validate skills/eigrp-analysis` → not yet created (T03)
- `agentskills validate skills/isis-analysis` → not yet created (T04)
- `bash scripts/validate.sh` → PASS (0 errors) ✅
- README catalog rows for routing protocol skills → not yet (T04)

## Diagnostics

- Validate skill: `agentskills validate skills/ospf-analysis`
- Validate all: `bash scripts/validate.sh`
- Check word count: `awk 'BEGIN{c=0}/^---$/{c++;if(c==2){f=1;next}}f{print}' skills/ospf-analysis/SKILL.md | wc -w`
- Check vendor labels: `grep -c '\[Cisco\]\|\[JunOS\]\|\[EOS\]' skills/ospf-analysis/SKILL.md`
- Inspect H2 sections: `grep '^## ' skills/ospf-analysis/SKILL.md`

## Deviations

None — followed the task plan exactly.

## Known Issues

None.

## Files Created/Modified

- `skills/ospf-analysis/SKILL.md` — OSPF protocol analysis skill (2229 words body, 3-vendor labeling, 5-step procedure, 2 decision trees)
- `skills/ospf-analysis/references/cli-reference.md` — 3-vendor OSPF CLI command tables across 5 diagnostic categories
- `skills/ospf-analysis/references/state-machine.md` — Full OSPF neighbor FSM (8 states), DR/BDR election, LSDB sync process
- `.gsd/milestones/M001/slices/S03/tasks/T02-PLAN.md` — Added Observability Impact section (pre-flight fix)
- `.gsd/milestones/M001/slices/S03/S03-PLAN.md` — Marked T02 as [x] done
