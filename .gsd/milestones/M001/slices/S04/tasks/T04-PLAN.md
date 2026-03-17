---
estimated_steps: 5
estimated_files: 3
---

# T04: Create change-verification skill with pre/post baselines, diff analysis, and rollback guidance

**Slice:** S04 — Network Operations & Change Management
**Milestone:** M001

## Description

Create the `skills/change-verification/` skill directory with SKILL.md and two reference files. This skill guides an agent through structured change management — capturing pre-change baselines, providing change execution guidance, performing post-change verification with diff analysis, and making rollback decisions across Cisco, Juniper, and Arista platforms.

This is the second `read-write` safety tier skill. The `read-write` designation covers the change execution phase where configuration changes are applied and potentially rolled back.

**Critical scope boundary:** This skill covers *event-driven* change verification (a specific change window: before → during → after). It does NOT cover *ongoing* config drift detection — that's T03's config-management skill. The procedure is structured around a single change event lifecycle.

**Word budget risk:** Pre/post checklists for multiple change types (routing, switching, security, upgrade) can bloat the SKILL.md body. Keep the procedure generic — offload per-change-type checklists to `references/checklist-templates.md`.

**Relevant installed skills:** none needed — this is markdown content authoring.

## Steps

1. **Create `skills/change-verification/SKILL.md`** with:
   - 6 frontmatter keys: `name: change-verification`, `description` (pre/post change verification with baseline capture and diff analysis across 3 vendors), `license: Apache-2.0`, `metadata.safety: read-write`, `metadata.author: network-security-skills-suite`, `metadata.version: "1.0.0"`
   - H1 title, introductory paragraph, vendor labeling note (`[Cisco]`/`[JunOS]`/`[EOS]`), and a **safety note** about read-write operations during change execution
   - 7 required H2 sections: When to Use, Prerequisites, Procedure, Threshold Tables, Decision Trees, Report Template, Troubleshooting
   - **Procedure** should cover: (1) Pre-change baseline capture — snapshot running config, routing tables, interface states, neighbor adjacencies, hardware status; (2) Change scope definition — document what is being changed, expected impact, rollback plan; (3) Change execution guidance — commit-confirm patterns, staged rollout, validation gates; (4) Post-change verification — re-capture all baseline metrics, diff against pre-change snapshots; (5) Impact assessment — classify deviations as expected (intended change effect) vs unexpected (collateral damage); (6) Rollback decision — criteria for rollback vs accept, timing windows, escalation triggers
   - **Threshold Tables** for this skill: acceptable deviation thresholds (how much route count change is ok, how many interface flaps are expected during maintenance), rollback timing thresholds (how long to wait before declaring success)
   - **Decision Trees** should encode: post-change diff shows unexpected changes → classify severity → check if related to change scope → rollback vs investigate; adjacency loss detected → check if device was in change scope → check if interface was bounced intentionally; route count deviation → compare against change plan → determine if prefix addition/removal is expected
   - Use `[Cisco]`/`[JunOS]`/`[EOS]` vendor labels where commands diverge
   - Body must stay ≤ 2700 words — offload detailed per-change-type checklists to references/

2. **Create `skills/change-verification/references/cli-reference.md`** with:
   - Multi-vendor CLI command tables organized by change lifecycle phase (baseline capture, config commit/rollback, post-change verification)
   - 3-column format: Cisco | JunOS | EOS
   - Include commit-confirm and rollback commands with safety notes
   - Note vendor-specific rollback capabilities: JunOS `rollback N` vs Cisco `configure replace` vs EOS `configure sessions`

3. **Create `skills/change-verification/references/checklist-templates.md`** with:
   - Pre-change checklist template (generic — what to capture before any change)
   - Post-change checklist template (generic — what to verify after any change)
   - Change-type-specific checklists: routing changes (BGP/OSPF/EIGRP), switching changes (VLAN/STP/MLAG), security changes (ACL/firewall/AAA), software upgrades (ISSU/non-disruptive/full reboot)
   - Each checklist should list specific show commands to run and what to compare
   - Rollback decision matrix — criteria grid with severity vs scope vs timing

4. **Validate the skill:**
   - Run `agentskills validate skills/change-verification` → must exit 0
   - Run `bash scripts/validate.sh` → must pass with 0 errors
   - Check body word count ≤ 2700
   - Verify frontmatter has `metadata.safety: read-write`

5. **Verify structure:**
   - Confirm 6 frontmatter keys with `safety: read-write`
   - Confirm 7 required H2 sections
   - Confirm `references/` has `cli-reference.md` and `checklist-templates.md`

## Must-Haves

- [ ] SKILL.md has 6 frontmatter keys with `metadata.safety: read-write`
- [ ] SKILL.md has all 7 required H2 sections
- [ ] SKILL.md body ≤ 2700 words
- [ ] Uses `[Cisco]`/`[JunOS]`/`[EOS]` vendor labeling pattern
- [ ] Scope is event-driven change verification, NOT ongoing drift detection
- [ ] Per-change-type checklists are in references/, not bloating the SKILL.md body
- [ ] `references/cli-reference.md` exists with commit/rollback/verification commands
- [ ] `references/checklist-templates.md` exists with pre/post checklists by change type
- [ ] `agentskills validate skills/change-verification` exits 0
- [ ] `bash scripts/validate.sh` passes

## Verification

- `agentskills validate skills/change-verification` → exit 0
- `bash scripts/validate.sh` → includes change-verification in checks, 0 errors
- `awk 'BEGIN{c=0}/^---$/{c++;if(c==2){f=1;next}}f{print}' skills/change-verification/SKILL.md | wc -w` → ≤ 2700
- `grep 'safety: read-write' skills/change-verification/SKILL.md` → matches
- `ls skills/change-verification/references/` → shows `cli-reference.md` and `checklist-templates.md`

## Inputs

- `skills/bgp-analysis/SKILL.md` — Reference for 3-vendor labeling pattern and frontmatter structure
- `scripts/validate.sh` — Validation script (already accepts `read-write` as valid safety value)
- T03 context: config-management handles ongoing drift; this skill handles event-driven change windows. No file overlap.

## Expected Output

- `skills/change-verification/SKILL.md` — Complete change verification skill with `read-write` safety tier
- `skills/change-verification/references/cli-reference.md` — Multi-vendor change lifecycle CLI commands
- `skills/change-verification/references/checklist-templates.md` — Pre/post verification checklists by change type with rollback decision matrix
