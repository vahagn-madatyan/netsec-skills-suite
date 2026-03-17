---
id: T04
parent: S04
milestone: M001
provides:
  - change-verification skill with event-driven pre/post baseline, diff analysis, and rollback decision guidance
key_files:
  - skills/change-verification/SKILL.md
  - skills/change-verification/references/cli-reference.md
  - skills/change-verification/references/checklist-templates.md
key_decisions:
  - Offloaded per-change-type checklists (routing, switching, security, upgrade) to references/checklist-templates.md to keep SKILL.md body within 2700-word budget
  - Included rollback decision matrix in checklist-templates.md using severity×scope and severity×timing cross-reference grids
patterns_established:
  - Event-driven change lifecycle procedure shape (before→during→after) vs ongoing drift detection (config-management) — clear scope boundary between T03 and T04
  - 4-tier impact classification for post-change deviations (Expected-Intended, Expected-Side Effect, Unexpected-Minor, Unexpected-Critical)
  - Commit-confirm safety pattern documented per vendor (JunOS commit confirmed, EOS configure session + commit timer, Cisco configure replace)
observability_surfaces:
  - "agentskills validate skills/change-verification — structural validation"
  - "bash scripts/validate.sh — suite-wide check (12 skills, 0 errors)"
  - "Word count: awk body extraction | wc -w → 2475 (≤2700)"
  - "grep safety: read-write — confirms read-write designation"
duration: ~20m
verification_result: passed
completed_at: 2026-03-16
blocker_discovered: false
---

# T04: Create change-verification skill with pre/post baselines, diff analysis, and rollback guidance

**Created complete change-verification skill with 6-step event-driven procedure, 4-tier impact classification, rollback decision matrices, and per-change-type checklists for routing/switching/security/upgrade across 3 vendors.**

## What Happened

Created the `skills/change-verification/` directory with SKILL.md and two reference files. The SKILL.md follows the established 7-section template with `read-write` safety tier (second such skill after config-management).

The procedure is structured as a 6-step event-driven lifecycle: (1) pre-change baseline capture, (2) change scope documentation, (3) change execution with commit-confirm patterns, (4) post-change verification with diff analysis, (5) impact assessment using a 4-tier classification, (6) rollback decision criteria.

Threshold tables cover acceptable deviation thresholds (route count ±2%/±5%/±10%, BGP/OSPF adjacency loss, interface errors) and rollback timing thresholds (convergence windows, soak periods).

Decision trees encode three key post-change scenarios: unexpected config diff lines, adjacency loss detection, and route count deviation — each with scope-aware classification paths.

Per-change-type checklists (routing, switching, security, upgrade) were offloaded to `references/checklist-templates.md` per plan guidance, keeping the SKILL.md body at 2475 words. The checklist file also includes a rollback decision matrix with severity×scope and severity×timing grids plus escalation triggers.

## Verification

- `bash scripts/validate.sh` → 12 skills checked, 0 errors, PASS ✅
- Body word count: 2475 (≤2700) ✅
- `grep 'safety: read-write'` → matches ✅
- `ls skills/change-verification/references/` → `checklist-templates.md`, `cli-reference.md` ✅
- All 7 required H2 sections present ✅
- 6 frontmatter keys confirmed (name, description, license, metadata.safety, metadata.author, metadata.version) ✅
- Scope correctly limited to event-driven change verification (no overlap with T03 config-management ongoing drift) ✅

Slice-level checks (4 S04 skills):
- interface-health: 2176 words, read-only, 2 refs ✅
- network-topology-discovery: 2272 words, read-only, 2 refs ✅
- config-management: 2049 words, read-write, 2 refs ✅
- change-verification: 2475 words, read-write, 2 refs ✅

Remaining slice checks for T05: README catalog update (12 real skill rows), `npx skills add . --list` discovery.

## Diagnostics

- Run `agentskills validate skills/change-verification` to verify structural validity (requires agentskills npm package)
- Run `bash scripts/validate.sh` to verify as part of full suite
- Check body word count: `awk 'BEGIN{c=0}/^---$/{c++;if(c==2){f=1;next}}f{print}' skills/change-verification/SKILL.md | wc -w`
- List references: `ls skills/change-verification/references/`

## Deviations

- Added `## Observability Impact` section to T04-PLAN.md per pre-flight requirement (plan was missing it).

## Known Issues

- `agentskills` npm package not found on public registry — same as prior tasks. `validate.sh` serves as the authoritative validator.

## Files Created/Modified

- `skills/change-verification/SKILL.md` — Complete change verification skill with read-write safety tier, 6-step procedure, threshold tables, decision trees
- `skills/change-verification/references/cli-reference.md` — Multi-vendor CLI commands organized by change lifecycle phase (baseline, commit/rollback, verification)
- `skills/change-verification/references/checklist-templates.md` — Pre/post checklists, 4 change-type-specific checklists, rollback decision matrix
- `.gsd/milestones/M001/slices/S04/tasks/T04-PLAN.md` — Added Observability Impact section
- `.gsd/milestones/M001/slices/S04/S04-PLAN.md` — Marked T04 as done
