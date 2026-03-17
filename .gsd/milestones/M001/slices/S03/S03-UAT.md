# S03: Routing Protocol Analysis Suite — UAT

**Milestone:** M001
**Written:** 2026-03-16

## UAT Type

- UAT mode: artifact-driven
- Why this mode is sufficient: All deliverables are static markdown files — validation is structural (frontmatter, sections, word count, vendor labels) with no runtime component

## Preconditions

- Repository cloned with all S03 files present in `skills/bgp-analysis/`, `skills/ospf-analysis/`, `skills/eigrp-analysis/`, `skills/isis-analysis/`
- Node.js available (for npx) — though `agentskills` npm package may 404; `bash scripts/validate.sh` is the fallback
- `bash`, `awk`, `grep`, `wc` available (standard Unix tools)

## Smoke Test

Run `bash scripts/validate.sh` from the repo root. Expected: "Skills checked: 8" and "Result: PASS (0 errors)". All 8 skills (4 device health + 4 routing protocol) pass with zero errors.

## Test Cases

### 1. BGP skill validates and contains protocol-first reasoning

1. Run `agentskills validate skills/bgp-analysis` (or check via `bash scripts/validate.sh`)
2. Open `skills/bgp-analysis/SKILL.md` and verify frontmatter has `name: bgp-analysis`, `metadata.safety: read-only`
3. Verify all 7 H2 sections present: `grep '^## ' skills/bgp-analysis/SKILL.md`
4. Check body word count: `awk 'BEGIN{c=0}/^---$/{c++;if(c==2){f=1;next}}f{print}' skills/bgp-analysis/SKILL.md | wc -w`
5. Verify 3-vendor labels: `grep -c '\[Cisco\]\|\[JunOS\]\|\[EOS\]' skills/bgp-analysis/SKILL.md`
6. Verify `references/cli-reference.md` and `references/state-machine.md` exist
7. **Expected:** Exit 0, all 7 H2 sections present, body ≤ 2700 words (actual: 2070), vendor label count ≥ 10 (actual: 19), both reference files present

### 2. OSPF skill validates with stuck-state diagnosis

1. Run `agentskills validate skills/ospf-analysis` (or check via `bash scripts/validate.sh`)
2. Check body word count ≤ 2700 (actual: 2229)
3. Verify 3-vendor labels present: `grep -c '\[Cisco\]\|\[JunOS\]\|\[EOS\]' skills/ospf-analysis/SKILL.md`
4. Open SKILL.md and confirm the Decision Trees section references ExStart stuck state → MTU mismatch reasoning
5. Verify `references/state-machine.md` covers all 8 OSPF neighbor states (Down, Attempt, Init, 2-Way, ExStart, Exchange, Loading, Full)
6. **Expected:** Exit 0, body ≤ 2700, vendor labels ≥ 10 (actual: 16), ExStart/MTU reasoning present, all 8 states documented

### 3. EIGRP skill uses dual-platform labels (NOT 3-vendor)

1. Run `agentskills validate skills/eigrp-analysis` (or check via `bash scripts/validate.sh`)
2. Check body word count ≤ 2700 (actual: 2047)
3. Verify dual-platform labels: `grep -c '\[IOS-XE\]\|\[NX-OS\]' skills/eigrp-analysis/SKILL.md` — should be ≥ 10 (actual: 13)
4. Verify NO 3-vendor labels: `grep -c '\[Cisco\]\|\[JunOS\]\|\[EOS\]' skills/eigrp-analysis/SKILL.md` — **must be 0**
5. Open SKILL.md and confirm Procedure covers DUAL feasibility condition (reported distance < feasible distance)
6. Verify `references/state-machine.md` covers Passive/Active states and feasibility condition math
7. **Expected:** Exit 0, body ≤ 2700, dual-platform labels ≥ 10, 3-vendor labels = 0, DUAL reasoning present

### 4. IS-IS skill validates with LSPDB and level 1/2 coverage

1. Run `agentskills validate skills/isis-analysis` (or check via `bash scripts/validate.sh`)
2. Check body word count ≤ 2700 (actual: 2496)
3. Verify 3-vendor labels: `grep -c '\[Cisco\]\|\[JunOS\]\|\[EOS\]' skills/isis-analysis/SKILL.md` — ≥ 10 (actual: 16)
4. Open SKILL.md and confirm Procedure covers NET address validation and level 1/2 route leaking
5. Verify `references/state-machine.md` covers DIS election and CSNP/PSNP flooding
6. **Expected:** Exit 0, body ≤ 2700 (note: closest to budget at 2496), vendor labels ≥ 10, NET/level topics present

### 5. README catalog contains all 4 routing protocol skills

1. Run `grep -E 'bgp-analysis|ospf-analysis|eigrp-analysis|isis-analysis' README.md`
2. Verify each row has a link to the SKILL.md, description, and `read-only` safety tier
3. Verify the routing skills appear after the device health skills
4. **Expected:** 4 matching lines, each with `read-only` tier, ordered after device health rows

### 6. Full validation suite passes

1. Run `bash scripts/validate.sh`
2. **Expected:** "Skills checked: 8", "Result: PASS (0 errors)", every skill shows "all checks OK"

## Edge Cases

### IS-IS word budget headroom

1. Run word count on IS-IS: `awk 'BEGIN{c=0}/^---$/{c++;if(c==2){f=1;next}}f{print}' skills/isis-analysis/SKILL.md | wc -w`
2. **Expected:** 2496 words — only 204 words under the 2700 limit. If anyone edits this skill, they must check the word count after changes.

### EIGRP vendor label exclusivity

1. Run `grep -c '\[Cisco\]\|\[JunOS\]\|\[EOS\]' skills/eigrp-analysis/SKILL.md`
2. **Expected:** Exactly 0. EIGRP is Cisco-proprietary and must NOT use 3-vendor labels. It uses `[IOS-XE]`/`[NX-OS]` exclusively.

### Reference file consistency

1. For each of the 4 skills, verify: `ls skills/<name>/references/`
2. **Expected:** Every skill has exactly `cli-reference.md` and `state-machine.md` — no more, no less.

## Failure Signals

- `bash scripts/validate.sh` exits non-zero or reports any "ERROR:" lines
- Body word count exceeds 2700 for any skill
- EIGRP skill contains `[Cisco]`, `[JunOS]`, or `[EOS]` labels (wrong vendor pattern)
- Any skill missing `references/cli-reference.md` or `references/state-machine.md`
- README missing any of the 4 routing protocol catalog rows
- Frontmatter `metadata.safety` is anything other than `read-only` for any routing protocol skill

## Requirements Proved By This UAT

- R009 — BGP analysis skill with protocol state machine reasoning, peer state diagnosis, path selection, route filtering, convergence assessment (Test Case 1)
- R010 — OSPF adjacency diagnosis with stuck-state interpretation, area design validation, LSA analysis, SPF convergence (Test Case 2)
- R011 — EIGRP DUAL reasoning with successor/feasible successor, stuck-in-active diagnosis, K-value validation (Test Case 3)
- R012 — IS-IS adjacency/LSPDB analysis, level 1/2 routing, NET validation, TLV analysis (Test Case 4)
- R004 — README catalog updated with 4 new skill rows (Test Case 5)

## Not Proven By This UAT

- Runtime agent loading — UAT does not test loading these skills into an actual AI agent session (human verification deferred to milestone DoD)
- `npx skills add` integration — npm package discovery not tested (known 404 issue)
- Content quality beyond structural validation — UAT verifies presence of sections, vendor labels, and word counts but does not assess whether the diagnostic reasoning is technically correct (requires domain expert review)

## Notes for Tester

- The `agentskills` npm package may return a 404 error. Use `bash scripts/validate.sh` as the primary validation tool — it performs all the same structural checks.
- IS-IS is at 92% of the word budget (2496/2700). If reviewing content quality, do not suggest additions without identifying what to trim.
- EIGRP's decision to use `[IOS-XE]`/`[NX-OS]` instead of `[Cisco]`/`[JunOS]`/`[EOS]` is intentional (D015) — EIGRP is Cisco-proprietary, so JunOS/EOS labels would be incorrect.
- The state-machine.md files have different internal structures because the protocols have different FSM types. BGP/OSPF/IS-IS use linear adjacency FSMs; EIGRP uses DUAL's Passive/Active diffusing computation. This is by design (D019).
