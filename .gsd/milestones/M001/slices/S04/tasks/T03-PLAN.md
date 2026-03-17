---
estimated_steps: 5
estimated_files: 3
---

# T03: Create config-management skill with backup, drift detection, and golden config validation

**Slice:** S04 — Network Operations & Change Management
**Milestone:** M001

## Description

Create the `skills/config-management/` skill directory with SKILL.md and two reference files. This skill guides an agent through configuration management workflows — backing up configurations, detecting drift between running and intended state, and validating against golden config baselines across Cisco, Juniper, and Arista platforms.

This is the first `read-write` safety tier skill in the repo. The `read-write` designation is necessary because config management procedures may involve config archival, rollback, or remediation operations that modify device state.

**Critical scope boundary:** This skill covers *ongoing* config management (detect drift, validate compliance, manage config archives). It does NOT cover *event-driven* change verification — that's T04's change-verification skill. Keep procedure sections clearly scoped to avoid overlap.

**Relevant installed skills:** none needed — this is markdown content authoring.

## Steps

1. **Create `skills/config-management/SKILL.md`** with:
   - 6 frontmatter keys: `name: config-management`, `description` (config backup, drift detection, golden config validation across 3 vendors), `license: Apache-2.0`, `metadata.safety: read-write`, `metadata.author: network-security-skills-suite`, `metadata.version: "1.0.0"`
   - H1 title, introductory paragraph, vendor labeling note (`[Cisco]`/`[JunOS]`/`[EOS]`), and a **safety note** explaining read-write operations
   - 7 required H2 sections: When to Use, Prerequisites, Procedure, Threshold Tables, Decision Trees, Report Template, Troubleshooting
   - **Procedure** should cover: (1) Config collection — capture running/startup/candidate configs; (2) Running vs startup comparison — detect unsaved changes; (3) Config archival — back up current config with timestamped naming; (4) Golden config baseline — establish/retrieve golden config for comparison; (5) Drift detection — section-by-section comparison of current vs golden/baseline; (6) Compliance validation — check for required/forbidden config patterns (AAA, logging, NTP, SNMP, ACLs); (7) Remediation guidance — how to address drift findings with rollback options
   - **Threshold Tables** for this skill: drift severity based on section affected (routing = critical, logging = warning, cosmetic = info), unsaved change age thresholds, config archive freshness
   - **Decision Trees** should encode: drift detected → classify by section criticality → check if change was authorized → recommend remediation or accept; running ≠ startup → check if change is intentional (maintenance window) vs accidental; compliance violation → severity classification → auto-remediation candidates vs manual review
   - Use `[Cisco]`/`[JunOS]`/`[EOS]` vendor labels where commands diverge
   - Body must stay ≤ 2700 words

2. **Create `skills/config-management/references/cli-reference.md`** with:
   - Multi-vendor CLI command tables: config display (running/startup/candidate), config archive/export, config diff/compare, config rollback, config replace
   - 3-column format: Cisco | JunOS | EOS
   - Note architectural differences: JunOS candidate-config model vs Cisco running/startup model vs EOS session-config model
   - Include both read-only and read-write commands with clear safety labeling

3. **Create `skills/config-management/references/drift-detection.md`** with:
   - Section-by-section diff methodology (routing, switching, security, management plane, services)
   - Golden config comparison patterns — what to normalize before comparing (timestamps, generated lines, certificate data)
   - Compliance rule definitions — required patterns (AAA, logging, NTP, SNMP community rotation) and forbidden patterns (default credentials, insecure protocols)
   - Drift severity classification matrix

4. **Validate the skill:**
   - Run `agentskills validate skills/config-management` → must exit 0
   - Run `bash scripts/validate.sh` → must pass with 0 errors
   - Check body word count ≤ 2700
   - Verify frontmatter has `metadata.safety: read-write` (not read-only)

5. **Verify structure:**
   - Confirm 6 frontmatter keys with `safety: read-write`
   - Confirm 7 required H2 sections
   - Confirm `references/` has `cli-reference.md` and `drift-detection.md`

## Must-Haves

- [ ] SKILL.md has 6 frontmatter keys with `metadata.safety: read-write`
- [ ] SKILL.md has all 7 required H2 sections
- [ ] SKILL.md body ≤ 2700 words
- [ ] Uses `[Cisco]`/`[JunOS]`/`[EOS]` vendor labeling pattern
- [ ] Scope is ongoing drift detection, NOT event-driven change verification
- [ ] `references/cli-reference.md` exists with multi-vendor commands including read-write operations
- [ ] `references/drift-detection.md` exists with comparison methodology and compliance patterns
- [ ] `agentskills validate skills/config-management` exits 0
- [ ] `bash scripts/validate.sh` passes

## Verification

- `agentskills validate skills/config-management` → exit 0
- `bash scripts/validate.sh` → includes config-management in checks, 0 errors
- `awk 'BEGIN{c=0}/^---$/{c++;if(c==2){f=1;next}}f{print}' skills/config-management/SKILL.md | wc -w` → ≤ 2700
- `grep 'safety: read-write' skills/config-management/SKILL.md` → matches
- `ls skills/config-management/references/` → shows `cli-reference.md` and `drift-detection.md`

## Observability Impact

- **New inspection surfaces:** `agentskills validate skills/config-management` validates frontmatter and structure; `bash scripts/validate.sh` includes config-management in suite-wide checks; `grep 'safety: read-write'` confirms first read-write skill in the repo.
- **Failure visibility:** Validation errors name the missing section or invalid field. validate.sh exits non-zero with `FAIL (N errors)` on any structural issue.
- **How a future agent inspects this task:** Run `agentskills validate skills/config-management` (exit 0 = healthy), check body word count with awk pipeline (≤ 2700), verify `ls skills/config-management/references/` shows 2 files.
- **No runtime signals** — this is static markdown content with no processes or APIs.

## Inputs

- `skills/bgp-analysis/SKILL.md` — Reference for 3-vendor labeling pattern and frontmatter structure
- `scripts/validate.sh` — Validation script (already accepts `read-write` as valid safety value)

## Expected Output

- `skills/config-management/SKILL.md` — Complete config management skill with `read-write` safety tier
- `skills/config-management/references/cli-reference.md` — Multi-vendor config management CLI commands
- `skills/config-management/references/drift-detection.md` — Drift detection methodology and compliance patterns
