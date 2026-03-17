# S03: Routing Protocol Analysis Suite

**Goal:** Deliver 4 routing protocol analysis skills (BGP, OSPF, EIGRP, IS-IS) with protocol state machine reasoning, multi-vendor CLI reference tables, adjacency diagnosis decision trees, and convergence analysis. Prove the multi-vendor (3-vendor) abstraction pattern.

**Demo:** `bash scripts/validate.sh` passes all skills including the 4 new routing protocol skills. Each skill encodes protocol-specific diagnostic reasoning (not just CLI cheat sheets) — state machine interpretation, stuck-state diagnosis, path/route analysis. BGP, OSPF, and IS-IS cover Cisco/JunOS/EOS; EIGRP covers IOS-XE/NX-OS. README catalog lists all routing protocol skills with `read-only` safety tier.

## Must-Haves

- 4 SKILL.md files: `bgp-analysis`, `ospf-analysis`, `eigrp-analysis`, `isis-analysis` — each with all 6 frontmatter keys and all 7 required H2 sections
- Protocol-first procedure structure: diagnostic reasoning chains, not just show commands with thresholds
- Multi-vendor CLI: `[Cisco]`/`[JunOS]`/`[EOS]` labels in BGP, OSPF, IS-IS; `[IOS-XE]`/`[NX-OS]` labels in EIGRP
- Each skill body ≤ 2700 words — inline CLI limited to 1 command per vendor per step, full tables in references/
- `references/cli-reference.md` per skill with full vendor CLI command tables
- `references/state-machine.md` per skill with protocol FSM detail, transition triggers, and failure modes
- README updated with 4 new catalog rows
- All skills pass `agentskills validate` and `bash scripts/validate.sh`

## Proof Level

- This slice proves: contract (3-vendor labeling pattern) + integration (CI validation of new skill type)
- Real runtime required: no (static markdown)
- Human/UAT required: no (verification via existing tooling)

## Verification

- `agentskills validate skills/bgp-analysis` → exit 0
- `agentskills validate skills/ospf-analysis` → exit 0
- `agentskills validate skills/eigrp-analysis` → exit 0
- `agentskills validate skills/isis-analysis` → exit 0
- `bash scripts/validate.sh` → all skills PASS, 0 errors
- Word count per SKILL.md body ≤ 2700 (measure with: `awk 'BEGIN{c=0}/^---$/{c++;if(c==2){f=1;next}}f{print}' skills/<name>/SKILL.md | wc -w`)
- README.md contains 4 new catalog rows: bgp-analysis, ospf-analysis, eigrp-analysis, isis-analysis
- Each skill has `references/` with `cli-reference.md` and `state-machine.md`
- All frontmatter has `metadata.safety: read-only`

## Integration Closure

- Upstream surfaces consumed: SKILL.md template (S01), `scripts/validate.sh` (S01), CI workflow (S01), README catalog format (S01/S02)
- New wiring introduced in this slice: none — follows established conventions
- What remains before the milestone is truly usable end-to-end: S04 (network operations skills) + final README validation

## Tasks

- [x] **T01: Write BGP analysis skill with 3-vendor pattern proof** `est:45m`
  - Why: BGP is the most complex routing protocol skill and proves the 3-vendor (`[Cisco]`/`[JunOS]`/`[EOS]`) labeling pattern. Must be written first to validate word budget and readability before committing to the pattern for OSPF and IS-IS. Covers R009.
  - Files: `skills/bgp-analysis/SKILL.md`, `skills/bgp-analysis/references/cli-reference.md`, `skills/bgp-analysis/references/state-machine.md`
  - Do: Create `skills/bgp-analysis/` directory with 3 files. SKILL.md: frontmatter (name: bgp-analysis, safety: read-only), all 7 H2 sections. Procedure encodes BGP diagnostic reasoning — peer state diagnosis via FSM interpretation (Idle→Connect→Active→OpenSent→OpenConfirm→Established), path selection analysis (AS path, local pref, MED, weight), route filtering validation, convergence assessment. Use `[Cisco]`/`[JunOS]`/`[EOS]` labels with 1 command per vendor per step. Decision trees must encode reasoning chains (e.g., "peer stuck in Active → TCP connects but no OPEN → check remote config, ACLs, peer AS"). Threshold Tables section contains operational parameter norms (hold timer defaults, table size norms, convergence targets). cli-reference.md: full 3-vendor command tables by diagnostic category. state-machine.md: BGP FSM states, transition triggers, stuck-state causes.
  - Verify: `agentskills validate skills/bgp-analysis` exit 0; body word count ≤ 2700; `bash scripts/validate.sh` shows bgp-analysis PASS
  - Done when: BGP skill passes all validation, body ≤ 2700 words, 3-vendor labeling is scannable and proven

- [x] **T02: Write OSPF analysis skill reusing 3-vendor pattern** `est:35m`
  - Why: OSPF is the most common enterprise IGP. Reuses the 3-vendor pattern proven in T01 with a different FSM (Down→Init→2-Way→ExStart→Exchange→Loading→Full). Covers R010.
  - Files: `skills/ospf-analysis/SKILL.md`, `skills/ospf-analysis/references/cli-reference.md`, `skills/ospf-analysis/references/state-machine.md`
  - Do: Create `skills/ospf-analysis/` directory with 3 files. SKILL.md: frontmatter (name: ospf-analysis, safety: read-only), all 7 H2 sections. Procedure encodes OSPF diagnostic reasoning — adjacency diagnosis (stuck-state interpretation per FSM), area design validation (stub/NSSA/backbone connectivity), LSA analysis (type 1-5,7 interpretation), SPF convergence assessment. Use `[Cisco]`/`[JunOS]`/`[EOS]` labels, 1 command per vendor per step. Decision trees encode adjacency stuck-state diagnosis (ExStart stuck = MTU mismatch or DR/BDR election issue). Threshold Tables: hello/dead interval defaults, LSA age norms, SPF run frequency. cli-reference.md: 3-vendor OSPF tables. state-machine.md: OSPF neighbor FSM with stuck-state diagnosis.
  - Verify: `agentskills validate skills/ospf-analysis` exit 0; body word count ≤ 2700; `bash scripts/validate.sh` shows ospf-analysis PASS
  - Done when: OSPF skill passes all validation, body ≤ 2700 words, 3-vendor pattern consistent with BGP

- [ ] **T03: Write EIGRP analysis skill with Cisco dual-platform labels** `est:30m`
  - Why: EIGRP is Cisco-proprietary but still widely deployed. Uses the dual-platform `[IOS-XE]`/`[NX-OS]` pattern from S02 (D015) instead of 3-vendor labels. DUAL FSM is unique. Covers R011.
  - Files: `skills/eigrp-analysis/SKILL.md`, `skills/eigrp-analysis/references/cli-reference.md`, `skills/eigrp-analysis/references/state-machine.md`
  - Do: Create `skills/eigrp-analysis/` directory with 3 files. SKILL.md: frontmatter (name: eigrp-analysis, safety: read-only), all 7 H2 sections. Procedure encodes EIGRP diagnostic reasoning — DUAL algorithm (successor/feasible successor analysis, feasibility condition: reported distance < feasible distance), stuck-in-active diagnosis, K-value validation across neighbors, route redistribution issues. Use `[IOS-XE]`/`[NX-OS]` labels per D015. Decision trees: stuck-in-active triage, successor loss analysis. Threshold Tables: SIA timer defaults, route count norms, hello/hold intervals. cli-reference.md: IOS-XE/NX-OS EIGRP tables. state-machine.md: DUAL FSM, feasibility condition math, SIA process.
  - Verify: `agentskills validate skills/eigrp-analysis` exit 0; body word count ≤ 2700; `bash scripts/validate.sh` shows eigrp-analysis PASS
  - Done when: EIGRP skill passes all validation, body ≤ 2700 words, uses `[IOS-XE]`/`[NX-OS]` labels (not 3-vendor)

- [ ] **T04: Write IS-IS analysis skill and update README catalog** `est:35m`
  - Why: IS-IS is the final routing protocol skill. 3-vendor coverage. Also updates README with all 4 new skill catalog rows to close the slice. Covers R012 and supports R004.
  - Files: `skills/isis-analysis/SKILL.md`, `skills/isis-analysis/references/cli-reference.md`, `skills/isis-analysis/references/state-machine.md`, `README.md`
  - Do: Create `skills/isis-analysis/` directory with 3 files. SKILL.md: frontmatter (name: isis-analysis, safety: read-only), all 7 H2 sections. Procedure encodes IS-IS diagnostic reasoning — adjacency diagnosis (DIS election, level 1/2 adjacency requirements), NET address validation, LSPDB analysis (LSP lifetime, sequence numbers, purges), TLV analysis, level 1/2 routing and route leaking. Use `[Cisco]`/`[JunOS]`/`[EOS]` labels, 1 command per vendor per step. Decision trees: adjacency failure triage, LSPDB inconsistency diagnosis. Threshold Tables: hello interval defaults, LSP lifetime norms, CSNP/PSNP intervals. cli-reference.md: 3-vendor IS-IS tables. state-machine.md: IS-IS adjacency states and LSPDB flooding mechanics. Then update README.md: add 4 new rows to the Skill Catalog table (bgp-analysis, ospf-analysis, eigrp-analysis, isis-analysis) with descriptions and `read-only` safety tier. Place them after the existing device health rows.
  - Verify: `agentskills validate skills/isis-analysis` exit 0; body word count ≤ 2700; `bash scripts/validate.sh` → all 8 skills PASS, 0 errors; README contains all 4 new catalog rows
  - Done when: IS-IS skill passes all validation, README updated with 4 routing protocol skills, full `scripts/validate.sh` passes with 0 errors across all 8 skills

## Observability / Diagnostics

- **Validation signals:** `agentskills validate skills/<name>` exit code per skill; `bash scripts/validate.sh` aggregate PASS/FAIL with per-skill error counts
- **Word budget signal:** `awk 'BEGIN{c=0}/^---$/{c++;if(c==2){f=1;next}}f{print}' skills/<name>/SKILL.md | wc -w` — must be ≤ 2700 per skill
- **Inspection surfaces:** Each `SKILL.md` body can be inspected for H2 section presence, vendor label count (`grep -c '\[Cisco\]\|\[JunOS\]\|\[EOS\]'`), and command-per-step density
- **Failure visibility:** `validate.sh` emits per-skill `ERROR:` lines for missing sections, invalid safety tier, or absent `references/` directory — failures are self-describing
- **Redaction constraints:** None — all content is static markdown with no secrets or runtime state

## Files Likely Touched

- `skills/bgp-analysis/SKILL.md`
- `skills/bgp-analysis/references/cli-reference.md`
- `skills/bgp-analysis/references/state-machine.md`
- `skills/ospf-analysis/SKILL.md`
- `skills/ospf-analysis/references/cli-reference.md`
- `skills/ospf-analysis/references/state-machine.md`
- `skills/eigrp-analysis/SKILL.md`
- `skills/eigrp-analysis/references/cli-reference.md`
- `skills/eigrp-analysis/references/state-machine.md`
- `skills/isis-analysis/SKILL.md`
- `skills/isis-analysis/references/cli-reference.md`
- `skills/isis-analysis/references/state-machine.md`
- `README.md`
