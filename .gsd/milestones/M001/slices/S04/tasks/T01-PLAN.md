---
estimated_steps: 5
estimated_files: 3
---

# T01: Create interface-health skill with error counters, optical thresholds, and discard analysis

**Slice:** S04 — Network Operations & Change Management
**Milestone:** M001

## Description

Create the `skills/interface-health/` skill directory with SKILL.md and two reference files. This skill guides an agent through interface and link health assessment — analyzing CRC errors, input/output errors, discards, resets, optical power levels (dBm), and utilization metrics across Cisco IOS-XE/NX-OS, Juniper JunOS, and Arista EOS.

This is the most similar skill to S02's device health checks — it's threshold-heavy with severity-tiered tables and counter-based analysis. The key distinction from device health is that this skill focuses exclusively on interface-level metrics, going deeper into physical/data-link layer diagnosis than the system-level health checks.

**Relevant installed skills:** none needed — this is markdown content authoring following an established template.

## Steps

1. **Create `skills/interface-health/SKILL.md`** with:
   - 6 frontmatter keys: `name: interface-health`, `description` (interface error analysis across 3 vendors), `license: Apache-2.0`, `metadata.safety: read-only`, `metadata.author: network-security-skills-suite`, `metadata.version: "1.0.0"`
   - H1 title, introductory paragraph, vendor labeling note (`[Cisco]`/`[JunOS]`/`[EOS]`)
   - 7 required H2 sections: When to Use, Prerequisites, Procedure, Threshold Tables, Decision Trees, Report Template, Troubleshooting
   - **Procedure** should cover: (1) Interface status overview — admin/operational state, speed/duplex; (2) Error counter analysis — CRC, frame, input/output errors, runts, giants; (3) Discard analysis — input/output discards, queue drops; (4) Interface reset/flap detection — reset counters, last flap timestamps; (5) Optical power monitoring — Tx/Rx power in dBm, laser bias current, temperature; (6) Utilization assessment — bandwidth usage, peak vs sustained
   - **Threshold Tables** in the body should summarize key thresholds (error rates, optical power ranges) with 4 severity tiers (Normal/Warning/Critical/Emergency). Detailed tables are in `references/threshold-tables.md`.
   - **Decision Trees** should encode: high error rate → check physical layer (cable, SFP, patch panel) vs config (MTU, duplex mismatch); high discards → check QoS policy vs buffer allocation vs control plane policing; optical power out of range → check SFP seating, fiber cleanliness, distance limits
   - Use `[Cisco]`/`[JunOS]`/`[EOS]` vendor labels where commands diverge
   - Body must stay ≤ 2700 words

2. **Create `skills/interface-health/references/cli-reference.md`** with:
   - Multi-vendor CLI command tables organized by diagnostic category (interface status, error counters, optical/transceiver, utilization)
   - 3-column format: Cisco | JunOS | EOS
   - Include interpretation notes where output format differs significantly across vendors
   - Note IOS-XE vs NX-OS differences where relevant

3. **Create `skills/interface-health/references/threshold-tables.md`** with:
   - Detailed 4-tier severity tables for: error rates (CRC, frame, input, output), discard rates, interface resets/flaps, optical power (Tx dBm, Rx dBm, laser bias, temperature), utilization percentages
   - Thresholds should use per-interval rates (errors/5min) not absolute counters
   - Include optical power tables for common SFP types (1G-SX, 10G-SR, 10G-LR, 25G-SR, 100G-SR4) with manufacturer spec ranges
   - Each table should have Normal/Warning/Critical/Emergency columns

4. **Validate the skill:**
   - Run `agentskills validate skills/interface-health` → must exit 0
   - Run `bash scripts/validate.sh` → must pass with 0 errors
   - Check body word count: `awk 'BEGIN{c=0}/^---$/{c++;if(c==2){f=1;next}}f{print}' skills/interface-health/SKILL.md | wc -w` → must be ≤ 2700

5. **Verify structure:**
   - Confirm 6 frontmatter keys present with `safety: read-only`
   - Confirm 7 required H2 sections present
   - Confirm `references/` has exactly 2 files: `cli-reference.md` and `threshold-tables.md`

## Must-Haves

- [ ] SKILL.md has 6 frontmatter keys with `metadata.safety: read-only`
- [ ] SKILL.md has all 7 required H2 sections
- [ ] SKILL.md body ≤ 2700 words
- [ ] Uses `[Cisco]`/`[JunOS]`/`[EOS]` vendor labeling pattern
- [ ] `references/cli-reference.md` exists with multi-vendor command tables
- [ ] `references/threshold-tables.md` exists with 4-severity-tier tables for error rates, optical power, and discards
- [ ] `agentskills validate skills/interface-health` exits 0
- [ ] `bash scripts/validate.sh` passes

## Verification

- `agentskills validate skills/interface-health` → exit 0
- `bash scripts/validate.sh` → includes interface-health in checks, 0 errors
- `awk 'BEGIN{c=0}/^---$/{c++;if(c==2){f=1;next}}f{print}' skills/interface-health/SKILL.md | wc -w` → ≤ 2700
- `ls skills/interface-health/references/` → shows `cli-reference.md` and `threshold-tables.md`

## Observability Impact

- **Signals changed:** No runtime signals — this task produces static markdown files only.
- **Inspection for future agents:** Run `agentskills validate skills/interface-health` (exit 0 = healthy). Run `bash scripts/validate.sh` and check for `interface-health` in output. Word count: `awk 'BEGIN{c=0}/^---$/{c++;if(c==2){f=1;next}}f{print}' skills/interface-health/SKILL.md | wc -w` (must be ≤ 2700).
- **Failure state visibility:** If SKILL.md is malformed, `agentskills validate` prints specific missing-field errors. If required H2 sections are missing, `validate.sh` prints `ERROR: Missing required section: ## <Name>`. If references/ directory or files are missing, `validate.sh` prints `ERROR: references/ directory missing`.

## Inputs

- `skills/bgp-analysis/SKILL.md` — Reference for 3-vendor labeling pattern (`[Cisco]`/`[JunOS]`/`[EOS]`) and frontmatter structure
- `skills/cisco-device-health/references/threshold-tables.md` — Reference for 4-severity-tier threshold table format
- `scripts/validate.sh` — Validation script that checks all skills

## Expected Output

- `skills/interface-health/SKILL.md` — Complete interface health monitoring skill with 3-vendor coverage
- `skills/interface-health/references/cli-reference.md` — Multi-vendor interface CLI command reference
- `skills/interface-health/references/threshold-tables.md` — Detailed threshold tables for interface error metrics and optical power
