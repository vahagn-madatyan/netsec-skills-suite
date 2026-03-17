# S04: Network Operations & Change Management

**Goal:** Deliver 4 network operations skills (interface-health, network-topology-discovery, config-management, change-verification) and complete the M001 skill catalog with end-to-end validation across all 12+ skills.
**Demo:** `bash scripts/validate.sh` passes all 12 real skills with 0 errors, README catalog shows 12 skill rows with correct safety tiers, and `npx skills add . --list` discovers the full set.

## Must-Haves

- 4 new SKILL.md files following the proven 7-section template with 3-vendor labeling (`[Cisco]`/`[JunOS]`/`[EOS]`)
- Each skill has `references/` directory with `cli-reference.md` + one skill-specific reference file
- interface-health and network-topology-discovery use `metadata.safety: read-only`
- config-management and change-verification use `metadata.safety: read-write`
- All SKILL.md bodies ≤ 2700 words
- README catalog updated with 4 new rows (12 real skills total)
- Full validation passes: `bash scripts/validate.sh` → 0 errors, PASS

## Proof Level

- This slice proves: final-assembly
- Real runtime required: no (static markdown files)
- Human/UAT required: no (CI validation + word count checks sufficient)

## Verification

- `agentskills validate skills/<name>` → exit 0 for all 4 new skills
- `bash scripts/validate.sh` → 12+ skills checked, 0 errors, PASS
- Per-skill word count: `awk 'BEGIN{c=0}/^---$/{c++;if(c==2){f=1;next}}f{print}' skills/<name>/SKILL.md | wc -w` ≤ 2700
- Each new SKILL.md: 6 frontmatter keys, correct `metadata.safety` value, 7 required H2 sections
- Each new skill: `references/` directory with exactly 2 files
- README catalog: 12 real skill rows + 1 example row, safety tiers correct
- `npx skills add . --list` → discovers all skills

## Integration Closure

- Upstream surfaces consumed: SKILL.md template from S01 (`skills/example-device-health/SKILL.md`), threshold table pattern from S02 (reused in interface-health), 3-vendor labeling pattern from S03 (reused in all 4 skills), `scripts/validate.sh` and `.github/workflows/validate.yml` from S01
- New wiring introduced in this slice: none — follows existing patterns
- What remains before the milestone is truly usable end-to-end: nothing — S04 is the final slice of M001

## Tasks

- [x] **T01: Create interface-health skill with error counters, optical thresholds, and discard analysis** `est:45m`
  - Why: Delivers R015 — interface error analysis is the most common physical-layer diagnostic. Threshold-heavy like S02 device health skills, making it a natural first task.
  - Files: `skills/interface-health/SKILL.md`, `skills/interface-health/references/cli-reference.md`, `skills/interface-health/references/threshold-tables.md`
  - Do: Write SKILL.md with 3-vendor labeled procedure covering CRC errors, input/output errors, discards, resets, optical power (dBm), and utilization. Reference `threshold-tables.md` for detailed 4-severity-tier thresholds. `cli-reference.md` for vendor commands. Safety: `read-only`.
  - Verify: `agentskills validate skills/interface-health` → exit 0; `bash scripts/validate.sh` passes; body ≤ 2700 words
  - Done when: SKILL.md has 6 frontmatter keys with `safety: read-only`, 7 H2 sections, body ≤ 2700 words, references/ has 2 files, validate.sh passes

- [x] **T02: Create network-topology-discovery skill with CDP/LLDP, ARP/MAC, and routing table analysis** `est:45m`
  - Why: Delivers R013 — topology understanding is prerequisite to most network troubleshooting. Introduces a unique iterative discovery procedure shape (layer-by-layer map building).
  - Files: `skills/network-topology-discovery/SKILL.md`, `skills/network-topology-discovery/references/cli-reference.md`, `skills/network-topology-discovery/references/discovery-workflow.md`
  - Do: Write SKILL.md with 3-vendor labeled procedure for L2 discovery (CDP/LLDP), L3 discovery (routing tables, ARP), MAC table correlation, and topology map construction. Reference `discovery-workflow.md` for methodology. Safety: `read-only`.
  - Verify: `agentskills validate skills/network-topology-discovery` → exit 0; `bash scripts/validate.sh` passes; body ≤ 2700 words
  - Done when: SKILL.md has 6 frontmatter keys with `safety: read-only`, 7 H2 sections, body ≤ 2700 words, references/ has 2 files, validate.sh passes

- [x] **T03: Create config-management skill with backup, drift detection, and golden config validation** `est:45m`
  - Why: Delivers R014 — config drift is the #1 cause of network outages. First `read-write` safety tier skill in the repo.
  - Files: `skills/config-management/SKILL.md`, `skills/config-management/references/cli-reference.md`, `skills/config-management/references/drift-detection.md`
  - Do: Write SKILL.md with 3-vendor labeled procedure for config backup/export, running-vs-startup comparison, golden config validation, section-by-section drift analysis. Reference `drift-detection.md` for comparison methodology. Safety: `read-write`. Keep scope to ongoing drift detection — change verification is T04's scope.
  - Verify: `agentskills validate skills/config-management` → exit 0; `bash scripts/validate.sh` passes; body ≤ 2700 words; frontmatter has `safety: read-write`
  - Done when: SKILL.md has 6 frontmatter keys with `safety: read-write`, 7 H2 sections, body ≤ 2700 words, references/ has 2 files, validate.sh passes

- [x] **T04: Create change-verification skill with pre/post baselines, diff analysis, and rollback guidance** `est:45m`
  - Why: Delivers R016 — structured change management prevents outages. Second `read-write` skill. Complementary to config-management but event-driven (specific change window), not ongoing.
  - Files: `skills/change-verification/SKILL.md`, `skills/change-verification/references/cli-reference.md`, `skills/change-verification/references/checklist-templates.md`
  - Do: Write SKILL.md with 3-vendor labeled procedure for pre-change baseline capture, change execution guidance, post-change verification diffs, rollback decision criteria. Offload per-change-type checklists (routing, switching, security, upgrade) to `checklist-templates.md` to stay within word budget. Safety: `read-write`.
  - Verify: `agentskills validate skills/change-verification` → exit 0; `bash scripts/validate.sh` passes; body ≤ 2700 words; frontmatter has `safety: read-write`
  - Done when: SKILL.md has 6 frontmatter keys with `safety: read-write`, 7 H2 sections, body ≤ 2700 words, references/ has 2 files, validate.sh passes

- [x] **T05: Update README catalog and run final M001 end-to-end validation** `est:20m`
  - Why: Completes R004 (supporting) — README must reflect the full M001 skill catalog. Final validation gate confirms all 12 skills pass, safety tiers are correct, and `npx skills add` discovers everything.
  - Files: `README.md`
  - Do: Add 4 new rows to the skill catalog table (interface-health, network-topology-discovery, config-management, change-verification) with correct descriptions and safety tiers. Run `bash scripts/validate.sh` to confirm all 12 real skills pass. Run `npx skills add . --list` to confirm discovery. Verify safety tier correctness: config-management and change-verification are `read-write`, all others `read-only`.
  - Verify: `bash scripts/validate.sh` → 12+ skills, 0 errors, PASS; README has 12 real skill rows; `npx skills add . --list` discovers all skills
  - Done when: README catalog has 13 rows (1 example + 12 real), validate.sh PASS across all skills, `npx skills add . --list` works

## Observability / Diagnostics

- **Runtime signals:** None — all deliverables are static markdown files. No runtime processes, APIs, or background services.
- **Inspection surfaces:**
  - `agentskills validate skills/<name>` — per-skill structural validation (frontmatter, required fields)
  - `bash scripts/validate.sh` — suite-wide validation across all skills (safety values, H2 sections, references/ directory)
  - Word count check: `awk 'BEGIN{c=0}/^---$/{c++;if(c==2){f=1;next}}f{print}' skills/<name>/SKILL.md | wc -w` — body ≤ 2700 words
  - `ls skills/<name>/references/` — confirms reference file inventory (exactly 2 files per skill)
  - `npx skills add . --list` — confirms AgentSkills SDK discovers all skills
- **Failure visibility:** Validation errors surface as named checks (e.g., "Missing required section: ## Procedure") with per-skill error counts. validate.sh exits non-zero and prints `FAIL (N errors)` on any failure.
- **Redaction constraints:** None — all content is public documentation with no secrets or credentials.

## Files Likely Touched

- `skills/interface-health/SKILL.md`
- `skills/interface-health/references/cli-reference.md`
- `skills/interface-health/references/threshold-tables.md`
- `skills/network-topology-discovery/SKILL.md`
- `skills/network-topology-discovery/references/cli-reference.md`
- `skills/network-topology-discovery/references/discovery-workflow.md`
- `skills/config-management/SKILL.md`
- `skills/config-management/references/cli-reference.md`
- `skills/config-management/references/drift-detection.md`
- `skills/change-verification/SKILL.md`
- `skills/change-verification/references/cli-reference.md`
- `skills/change-verification/references/checklist-templates.md`
- `README.md`
