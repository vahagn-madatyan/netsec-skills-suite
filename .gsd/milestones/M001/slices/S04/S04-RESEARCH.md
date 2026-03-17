# S04 ("Network Operations & Change Management") — Research

**Date:** 2026-03-16

## Summary

S04 creates 4 network operations skills (network-topology-discovery, config-management, interface-health, change-verification), updates the README catalog, and runs final validation across all 12+ skills. This is straightforward application of the proven SKILL.md template, vendor labeling patterns, and reference file conventions established in S01–S03. No new patterns or architectural decisions are needed.

The key content-level decisions are: which vendor labeling pattern per skill, which reference files provide the best progressive-disclosure value, and which skills get `read-write` safety tiers. Requirements R014 (config management) and R016 (change verification) explicitly note `safety: read-write` since they involve config operations and change execution. R013 (topology discovery) and R015 (interface health) are `read-only`.

After S04, all 12 real skills + 1 example skill pass validation, the README catalog is complete for M001, and `npx skills add` discovers the full set.

## Recommendation

Build 4 skills in independent tasks (one per skill), then a final task to update the README and run end-to-end validation. Each skill follows the proven 7-section SKILL.md template with 3-vendor labeling (`[Cisco]`/`[JunOS]`/`[EOS]`), `references/cli-reference.md`, and a second reference file chosen per skill type.

Skill-specific reference files:
- **network-topology-discovery** → `cli-reference.md` + `discovery-workflow.md` (topology building methodology)
- **config-management** → `cli-reference.md` + `drift-detection.md` (golden config comparison patterns)
- **interface-health** → `cli-reference.md` + `threshold-tables.md` (reuses S02 pattern — this skill is threshold-heavy like device health)
- **change-verification** → `cli-reference.md` + `checklist-templates.md` (pre/post check lists by change type)

## Implementation Landscape

### Key Files

- `skills/network-topology-discovery/SKILL.md` — **Create.** Topology discovery via CDP/LLDP, routing tables, ARP/MAC tables. 3-vendor labeling. Safety: `read-only`.
- `skills/network-topology-discovery/references/cli-reference.md` — **Create.** CDP/LLDP, ARP, MAC, route table commands across Cisco/JunOS/EOS.
- `skills/network-topology-discovery/references/discovery-workflow.md` — **Create.** Layer-by-layer discovery methodology, topology map construction patterns.
- `skills/config-management/SKILL.md` — **Create.** Config backup, comparison, drift detection, golden config validation. 3-vendor labeling. Safety: `read-write`.
- `skills/config-management/references/cli-reference.md` — **Create.** Config display, archive, rollback commands across vendors.
- `skills/config-management/references/drift-detection.md` — **Create.** Section-by-section diff patterns, golden config comparison methodology.
- `skills/interface-health/SKILL.md` — **Create.** Interface error analysis — CRC, errors, discards, resets, optical power levels. 3-vendor labeling. Safety: `read-only`.
- `skills/interface-health/references/cli-reference.md` — **Create.** Interface counters, optics, error commands across vendors.
- `skills/interface-health/references/threshold-tables.md` — **Create.** Error rate thresholds, optical power thresholds (dBm), discard rate thresholds with 4 severity tiers.
- `skills/change-verification/SKILL.md` — **Create.** Pre-change baseline, change execution guidance, post-change diff analysis. 3-vendor labeling. Safety: `read-write`.
- `skills/change-verification/references/cli-reference.md` — **Create.** Snapshot, diff, rollback commands across vendors.
- `skills/change-verification/references/checklist-templates.md` — **Create.** Pre/post verification checklists by change type (routing, switching, security, upgrade).
- `README.md` — **Modify.** Add 4 new rows to the skill catalog table after the routing protocol rows.
- `scripts/validate.sh` — **No change.** Works as-is against any number of skills.
- `.github/workflows/validate.yml` — **No change.** Iterates `skills/*/SKILL.md` automatically.

### Build Order

1. **interface-health** (T01) — Most similar to S02 device health skills (threshold-heavy, counter-based). Reuses the threshold-tables.md pattern directly. Low risk, good warm-up.
2. **network-topology-discovery** (T02) — Unique procedure shape (iterative discovery, building a map layer by layer). Introduces discovery-workflow.md reference pattern. Medium complexity.
3. **config-management** (T03) — First `read-write` skill in the repo. Introduces drift detection logic and golden config comparison. The read-write safety tier is a new content variation.
4. **change-verification** (T04) — Second `read-write` skill. Depends conceptually on understanding what config-management provides (they're complementary but distinct: config-management is ongoing drift detection, change-verification is event-driven pre/post). Introduces checklist-templates.md.
5. **README update + final validation** (T05) — Add 4 catalog rows, run `bash scripts/validate.sh` across all 12+ skills, verify word counts, confirm `npx skills add . --list` discovers all skills. This is the M001 completion gate.

Tasks 1–4 are independent (no file overlap) and could run in parallel. T05 depends on all four completing.

### Verification Approach

Per-skill (T01–T04):
- `agentskills validate skills/<name>` → exit 0 (or rely on `scripts/validate.sh` if agentskills npm is still 404)
- `bash scripts/validate.sh` → all skills pass, 0 errors
- Body word count ≤ 2700 via: `awk 'BEGIN{c=0}/^---$/{c++;if(c==2){f=1;next}}f{print}' skills/<name>/SKILL.md | wc -w`
- Frontmatter has all 6 keys, correct `metadata.safety` value (read-only or read-write)
- All 7 required H2 sections present
- `references/` directory has 2 files

Final validation (T05):
- `bash scripts/validate.sh` → 12 skills (excluding example), 0 errors, PASS
- README catalog table has 12 real skill rows + 1 example
- `npx skills add . --list` → discovers all skills
- Safety tiers: config-management and change-verification are `read-write`, all others `read-only`
- Total word count check: no skill exceeds 2700 words

## Constraints

- SKILL.md body must stay ≤ 2700 words (~5000 tokens). Network operations skills are procedurally simpler than routing protocol FSM skills, so budget should be comfortable.
- Safety tier for R014 (config-management) and R016 (change-verification) must be `read-write` — these are the first `read-write` skills in the repo. The validate.sh script already accepts `read-write` as a valid value.
- 3-vendor labeling (`[Cisco]`/`[JunOS]`/`[EOS]`) for all 4 skills since topology, config, interface, and change operations apply to all three vendors.
- Reference files follow established naming: `cli-reference.md` is mandatory, second file name varies by skill type.

## Common Pitfalls

- **config-management vs change-verification scope bleed** — These two skills are complementary but distinct. Config management is *ongoing* (detect drift, validate against golden configs). Change verification is *event-driven* (capture baseline before a specific change, verify after). Keep procedure sections clearly scoped to avoid duplication.
- **Word budget on change-verification** — Pre/post checklists for multiple change types (routing, switching, upgrade, security) can bloat quickly. Offload detailed per-change-type checklists to `references/checklist-templates.md` and keep SKILL.md procedure generic.
