---
estimated_steps: 5
estimated_files: 3
---

# T03: Write EIGRP analysis skill with Cisco dual-platform labels

**Slice:** S03 — Routing Protocol Analysis Suite
**Milestone:** M001

## Description

Create the EIGRP analysis skill — Cisco-proprietary, covering IOS-XE and NX-OS. Uses the dual-platform `[IOS-XE]`/`[NX-OS]` labeling pattern established in S02 (D015), NOT the 3-vendor pattern from T01/T02. EIGRP's DUAL algorithm is the unique analytical core — successor/feasible successor selection, the feasibility condition (reported distance < feasible distance), and stuck-in-active diagnosis.

This is the simplest skill in terms of vendor variation (Cisco only, 2 platforms) but has unique protocol reasoning: DUAL is fundamentally different from link-state FSMs. The skill must encode the DUAL computation logic and feasibility condition math, not just show commands.

**Relevant decisions:** D003 (tool-agnostic), D004 (deep procedural), D005 (references/), D009 (layout), D015 (dual-platform `[IOS-XE]`/`[NX-OS]` labels)

## Steps

1. Create directory structure: `skills/eigrp-analysis/` with `references/` subdirectory.

2. Write `skills/eigrp-analysis/SKILL.md` with:
   - **Frontmatter:** `name: eigrp-analysis`, `description` (EIGRP DUAL analysis, successor/feasible successor, stuck-in-active diagnosis, K-value validation — Cisco IOS-XE and NX-OS), `license: Apache-2.0`, `metadata.safety: read-only`, `metadata.author: network-security-skills-suite`, `metadata.version: "1.0.0"`
   - **H1 title:** `# EIGRP Protocol Analysis`
   - **Intro paragraph:** DUAL-reasoning-driven analysis for Cisco EIGRP. Uses `[IOS-XE]`/`[NX-OS]` labels where commands diverge.
   - **## When to Use** (~100 words): Route missing or suboptimal, stuck-in-active condition, neighbor not forming, K-value mismatch suspected, post-change verification after EIGRP config changes, redistribution loop suspected
   - **## Prerequisites** (~80 words): Cisco IOS-XE or NX-OS access, EIGRP enabled (classic or named mode), awareness of AS number and expected neighbors
   - **## Procedure** (~1400 words, 5-6 H3 steps): `[IOS-XE]`/`[NX-OS]` labels, 1 command per platform per step.
     - Step 1: EIGRP Instance & Neighbor Inventory — verify EIGRP running, list neighbors, compare against expected topology, check uptime for recent restarts
     - Step 2: Topology Table Analysis — examine successor and feasible successor for key routes, interpret feasible distance (FD) and reported distance (RD), verify feasibility condition (RD < FD of current successor)
     - Step 3: Stuck-in-Active Diagnosis — identify SIA routes, determine which neighbor(s) aren't responding to queries, check query scope (stub configuration, summarization, distribution lists)
     - Step 4: K-Value and Metric Validation — verify K-values match across all neighbors (K1=K3=1, K2=K4=K5=0 default), check for wide metric mode (named EIGRP), validate delay and bandwidth values on key interfaces
     - Step 5: Redistribution & Route Filtering — check for mutual redistribution (routing loops), verify distribute-lists and route-maps, examine external routes (D EX) for unexpected sources
   - **## Threshold Tables** (~300 words): Operational parameters — SIA timer defaults (3 min active, configurable), hello/hold intervals (5/15 LAN, 60/180 WAN), expected route counts, stuck-in-active frequency norms
   - **## Decision Trees** (~500 words): Two trees:
     - **Stuck-in-Active:** SIA route detected → check query scope (too broad? → configure stubs/summarization) → check unresponsive neighbor (reachable? → interface/link issue; reachable but not responding? → CPU overload, SIA timer too short, complex topology causing query cascade)
     - **Missing or Suboptimal Route:** check topology table (route present? → feasibility condition, successor selection; route absent? → redistribution, network statement, passive-interface)
   - **## Report Template** (~150 words): Structured EIGRP analysis findings format
   - **## Troubleshooting** (~200 words): Common issues — K-value mismatch (prevents adjacency), stuck-in-active cascading, redistribution loops with OSPF, passive-interface misconfiguration, named vs classic mode confusion

3. Write `skills/eigrp-analysis/references/cli-reference.md`:
   - 2-column tables: IOS-XE | NX-OS
   - Categories: Instance/Process, Neighbor, Topology Table, Interface, Redistribution
   - Include both classic (`show ip eigrp`) and named mode (`show eigrp address-family`) commands
   - Notes on NX-OS EIGRP differences (always named mode, `feature eigrp` required)

4. Write `skills/eigrp-analysis/references/state-machine.md`:
   - DUAL FSM: Passive → Active → Passive (with success/failure paths)
   - Feasibility condition explained with examples: FD, RD, successor, feasible successor
   - Query/Reply process: query scope, reply tracking, SIA handling
   - Composite metric formula: 256 × (K1×BW + K2×BW/(256-load) + K3×delay) × (K5/(reliability+K4))

5. Verify:
   - `agentskills validate skills/eigrp-analysis` → exit 0
   - Body word count ≤ 2700
   - `bash scripts/validate.sh` → eigrp-analysis checks all OK

## Must-Haves

- [ ] SKILL.md has all 6 frontmatter keys with `name: eigrp-analysis` and `metadata.safety: read-only`
- [ ] All 7 required H2 sections present
- [ ] Procedure uses `[IOS-XE]`/`[NX-OS]` labels (NOT `[Cisco]`/`[JunOS]`/`[EOS]` — EIGRP is Cisco-only)
- [ ] Decision trees encode DUAL reasoning (feasibility condition, SIA triage), not just command lists
- [ ] Body word count ≤ 2700
- [ ] `references/cli-reference.md` has IOS-XE/NX-OS command tables
- [ ] `references/state-machine.md` has DUAL FSM and feasibility condition math
- [ ] `agentskills validate skills/eigrp-analysis` exits 0

## Verification

- `agentskills validate skills/eigrp-analysis` → "Valid skill" (exit 0)
- `awk 'BEGIN{c=0}/^---$/{c++;if(c==2){f=1;next}}f{print}' skills/eigrp-analysis/SKILL.md | wc -w` → ≤ 2700
- `bash scripts/validate.sh` → eigrp-analysis: all checks OK

## Inputs

- `skills/bgp-analysis/SKILL.md` — Reference for protocol analysis skill structure (adapt for DUAL instead of BGP FSM)
- `skills/cisco-device-health/SKILL.md` — Reference for `[IOS-XE]`/`[NX-OS]` dual-platform labeling (D015)
- `scripts/validate.sh` — Validator (checks 7 H2 sections, safety tier, references/)

## Expected Output

- `skills/eigrp-analysis/SKILL.md` — EIGRP protocol analysis skill with dual-platform labeling, DUAL reasoning, ≤2700 word body
- `skills/eigrp-analysis/references/cli-reference.md` — IOS-XE/NX-OS EIGRP CLI command tables
- `skills/eigrp-analysis/references/state-machine.md` — DUAL FSM, feasibility condition, query/reply process

## Observability Impact

- **Validation signal:** `agentskills validate skills/eigrp-analysis` exit code (0 = valid, non-0 = broken frontmatter/structure). Also covered by `bash scripts/validate.sh` aggregate PASS/FAIL.
- **Word budget signal:** `awk 'BEGIN{c=0}/^---$/{c++;if(c==2){f=1;next}}f{print}' skills/eigrp-analysis/SKILL.md | wc -w` — must be ≤ 2700.
- **Vendor label signal:** `grep -c '\[IOS-XE\]\|\[NX-OS\]' skills/eigrp-analysis/SKILL.md` — confirms dual-platform labels used (should be >0); `grep -c '\[Cisco\]\|\[JunOS\]\|\[EOS\]' skills/eigrp-analysis/SKILL.md` — confirms 3-vendor labels NOT used (should be 0).
- **Section inspection:** `grep '^## ' skills/eigrp-analysis/SKILL.md` — lists all H2 sections for structural verification.
- **Failure visibility:** `validate.sh` emits per-skill `ERROR:` lines for missing sections, invalid safety tier, or absent `references/` directory — failures are self-describing.
