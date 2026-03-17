---
id: T01
parent: S03
milestone: M001
provides:
  - BGP analysis skill with 3-vendor (Cisco/JunOS/EOS) labeling pattern proof
  - BGP FSM state machine reference with stuck-state diagnosis
  - 3-vendor CLI command reference tables for BGP diagnostics
key_files:
  - skills/bgp-analysis/SKILL.md
  - skills/bgp-analysis/references/cli-reference.md
  - skills/bgp-analysis/references/state-machine.md
key_decisions:
  - 3-vendor labels use `**[Cisco]**` / `**[JunOS]**` / `**[EOS]**` bold format (consistent with S02's `**[IOS-XE]**` / `**[NX-OS]**` pattern)
  - One command per vendor per procedure step — full command tables pushed to references/cli-reference.md for progressive disclosure
  - Procedure encodes reasoning chains ("FSM state → failure domain → root cause") not just command lists — this is the key differentiator from device health skills
patterns_established:
  - 3-vendor labeling within ~2700 word budget is feasible (actual: 2070 words) — confirms pattern for OSPF and IS-IS
  - Decision trees encode diagnostic reasoning chains with branching logic, not flat command lists
  - references/state-machine.md captures protocol FSM with per-state stuck-state causes and NOTIFICATION error codes
observability_surfaces:
  - agentskills validate skills/bgp-analysis → exit 0
  - bash scripts/validate.sh → bgp-analysis PASS with 0 errors
  - Word count check via awk pipeline → 2070 words (≤2700 budget)
duration: ~20min
verification_result: passed
completed_at: 2026-03-16
blocker_discovered: false
---

# T01: Write BGP analysis skill with 3-vendor pattern proof

**Created BGP protocol analysis skill with 3-vendor Cisco/JunOS/EOS labeling, protocol-first diagnostic reasoning, and full FSM reference — proving the pattern for S03's remaining routing protocol skills.**

## What Happened

Created `skills/bgp-analysis/` with three files:

1. **SKILL.md** (2070 words body): Full BGP analysis procedure with 6 H3 diagnostic steps — session inventory, peer state diagnosis via FSM interpretation, route table analysis, path selection verification (walking the best-path algorithm), route filtering validation, and convergence assessment. Each step uses `[Cisco]`/`[JunOS]`/`[EOS]` labels with one command per vendor. Decision trees encode two reasoning chains: "Peer Not Established" (branching by FSM state to root cause) and "Unexpected Route Selection" (walking best-path attribute order). Threshold tables cover protocol-level operational norms (timers, table sizes, convergence targets) rather than device resource thresholds.

2. **references/cli-reference.md**: 5-category 3-vendor command tables (Session Management, Route Table, Path Attributes, Filtering, Convergence/Dampening) with per-category interpretation notes highlighting vendor-specific differences (e.g., JunOS default export policy, weight attribute absence on JunOS).

3. **references/state-machine.md**: Complete BGP FSM (Idle→Connect→Active→OpenSent→OpenConfirm→Established) with per-state definition, entry conditions, exit transitions, and stuck-state causes. Includes timer reference table, event-driven transition matrix, and NOTIFICATION error code table.

The key pattern proof: 3-vendor labeling within the ~2700 word budget is feasible with 630 words of headroom (2070 actual). The approach of one command per vendor per step with full tables in references/ keeps the procedure scannable.

## Verification

- `agentskills validate skills/bgp-analysis` → exit 0 ("Valid skill")
- Body word count: 2070 (≤2700 budget, 630 words headroom)
- `bash scripts/validate.sh` → 5 skills checked, PASS (0 errors), bgp-analysis all OK
- 19 vendor label occurrences across procedure (6 steps × 3 vendors + intro paragraph)
- `metadata.safety: read-only` confirmed in frontmatter
- All 7 required H2 sections present
- `references/` directory with 2 files (cli-reference.md, state-machine.md)

### Slice-Level Verification Status (T01 scope)

| Check | Status |
|-------|--------|
| `agentskills validate skills/bgp-analysis` → exit 0 | ✅ PASS |
| `bash scripts/validate.sh` → all PASS, 0 errors | ✅ PASS (5 skills) |
| Word count ≤ 2700 | ✅ PASS (2070) |
| `references/cli-reference.md` + `state-machine.md` present | ✅ PASS |
| `metadata.safety: read-only` | ✅ PASS |
| `agentskills validate skills/ospf-analysis` | ⬜ Not yet (T02) |
| `agentskills validate skills/eigrp-analysis` | ⬜ Not yet (T03) |
| `agentskills validate skills/isis-analysis` | ⬜ Not yet (T04) |
| README contains 4 new catalog rows | ⬜ Not yet (T04) |

## Diagnostics

- Validate skill: `agentskills validate skills/bgp-analysis`
- Validate all: `bash scripts/validate.sh`
- Check word count: `awk 'BEGIN{c=0}/^---$/{c++;if(c==2){f=1;next}}f{print}' skills/bgp-analysis/SKILL.md | wc -w`
- Check vendor labels: `grep -c '\[Cisco\]\|\[JunOS\]\|\[EOS\]' skills/bgp-analysis/SKILL.md`
- Inspect H2 sections: `grep '^## ' skills/bgp-analysis/SKILL.md`

## Deviations

None. All plan steps executed as specified.

## Known Issues

None.

## Files Created/Modified

- `skills/bgp-analysis/SKILL.md` — BGP protocol analysis skill, 3-vendor labeling, 2070 words body
- `skills/bgp-analysis/references/cli-reference.md` — 3-vendor BGP CLI command tables by diagnostic category
- `skills/bgp-analysis/references/state-machine.md` — BGP FSM states, transitions, stuck-state causes, NOTIFICATION codes
- `.gsd/milestones/M001/slices/S03/S03-PLAN.md` — Added Observability/Diagnostics section, marked T01 done
- `.gsd/milestones/M001/slices/S03/tasks/T01-PLAN.md` — Added Observability Impact section
