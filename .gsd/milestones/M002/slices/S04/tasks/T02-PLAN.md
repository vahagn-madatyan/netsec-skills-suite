---
estimated_steps: 5
estimated_files: 3
---

# T02: Build zero-trust assessment skill with maturity scoring rubric

**Slice:** S04 — Additional Security Skills & Suite Finalization
**Milestone:** M002

## Description

Create the zero-trust assessment skill (R028) introducing the "maturity scoring" procedure shape (D028). This is a rubric-based posture assessment where the Threshold Tables section maps naturally to maturity level scoring across 5 ZT pillars (identity, device, network, application, data).

The skill is vendor-agnostic — no inline vendor labels in the SKILL.md body. It assesses architecture posture, not device-specific configurations. References NIST SP 800-207 (public domain). Safety: read-only (D027). Body must be ≤2700 words.

The cli-reference.md file IS multi-vendor ([Cisco]/[JunOS]/[PAN-OS]/[FortiGate]) since validation of ZT controls requires platform-specific commands (802.1X status, segmentation verification, AAA config, policy enforcement points).

## Steps

1. Create `skills/zero-trust-assessment/references/maturity-model.md` documenting the ZT maturity framework:
   - Five ZT pillars with definitions: Identity, Device, Network, Application, Data
   - Five maturity levels: Level 1 (Traditional) → Level 2 (Initial) → Level 3 (Advanced) → Level 4 (Optimal) → Level 5 (Adaptive)
   - Scoring criteria per pillar × level combination (what capabilities define each level for each pillar)
   - Overall maturity calculation methodology (weighted average or lowest-pillar approach)
   - Reference NIST SP 800-207 ZTA tenets as the foundation
   - Assessment methodology: evidence collection → pillar scoring → gap analysis → roadmap

2. Create `skills/zero-trust-assessment/references/cli-reference.md` with validation commands for ZT controls:
   - 802.1X / NAC verification: dot1x status, authentication sessions
   - Micro-segmentation: VLAN/VRF/SGT/TrustSec (Cisco), security-zone (PAN-OS), routing-instance (JunOS), VDOM (FortiGate)
   - AAA/RADIUS/TACACS+: server status, authentication method
   - MFA / certificate-based auth verification
   - Policy enforcement point status
   - Use [Cisco]/[JunOS]/[PAN-OS]/[FortiGate] vendor labels in the reference file
   - Table format organized by ZT control category

3. Create `skills/zero-trust-assessment/SKILL.md` with:
   - Frontmatter: name, description, license: Apache-2.0, metadata.safety: read-only, metadata.author: network-security-skills-suite, metadata.version: "1.0.0"
   - Intro explaining ZT maturity assessment approach — architecture-level posture evaluation, not device-specific config audit
   - 7 required H2 sections: When to Use, Prerequisites, Procedure, Threshold Tables, Decision Trees, Report Template, Troubleshooting
   - Procedure follows maturity scoring shape: (1) Define Assessment Scope → (2) Identity Pillar Assessment → (3) Device Pillar Assessment → (4) Network Pillar Assessment → (5) Application & Data Pillar Assessment → (6) Calculate Maturity Score and Report
   - Threshold Tables: maturity level scoring criteria per pillar — Level 1-5 with specific capability indicators. This is where the "maturity scoring" shape maps to the required section.
   - Decision Trees: ZT maturity triage — which pillar to prioritize based on current weaknesses, quick wins vs strategic investments
   - Key content: NIST 800-207 ZTA tenets, identity verification (MFA, cert-based auth, NAC), micro-segmentation (beyond VLANs — SGT/TrustSec, VRF-lite, PAN-OS zones), least privilege (rule permissiveness scoring), continuous verification (session monitoring, re-auth)

4. Verify word count: `awk 'BEGIN{c=0} /^---$/{c++; if(c==2){found=1; next}} found{print}' skills/zero-trust-assessment/SKILL.md | wc -w` → must be ≤2700. If over budget, compress Troubleshooting section.

5. Run validation: `bash scripts/validate.sh 2>&1 | grep -E 'Skills checked|Result'` → must show 24 skills, PASS.

## Must-Haves

- [ ] SKILL.md has valid frontmatter with `metadata.safety: read-only`
- [ ] All 7 required H2 sections present
- [ ] Procedure follows maturity scoring shape: scope → pillar assessments → scoring → report
- [ ] 5-pillar framework: identity, device, network, application, data
- [ ] Threshold Tables used for maturity level scoring (Level 1-5)
- [ ] Vendor-agnostic in SKILL.md body (no inline vendor labels)
- [ ] references/maturity-model.md covers 5 pillars × 5 levels with scoring criteria
- [ ] references/cli-reference.md has multi-vendor validation commands
- [ ] Body ≤2700 words (awk K001 method)
- [ ] `bash scripts/validate.sh` passes with 24 skills

## Verification

- `bash scripts/validate.sh 2>&1 | grep 'Skills checked'` → "Skills checked: 24"
- `bash scripts/validate.sh 2>&1 | grep 'Result'` → "Result: PASS (0 errors)"
- `awk 'BEGIN{c=0} /^---$/{c++; if(c==2){found=1; next}} found{print}' skills/zero-trust-assessment/SKILL.md | wc -w` → ≤2700
- `ls skills/zero-trust-assessment/references/ | wc -l` → 2
- `grep -c 'maturity\|pillar\|score\|Level' skills/zero-trust-assessment/SKILL.md` → ≥10
- `grep -c 'NIST\|800-207' skills/zero-trust-assessment/SKILL.md` → ≥1

## Inputs

- `skills/cis-benchmark-audit/SKILL.md` — Threshold Tables scoring pattern precedent (severity tiers as scoring rubric)
- `skills/palo-alto-firewall-audit/SKILL.md` — Policy audit procedure shape for reference
- `scripts/validate.sh` — Convention validator
- T01 completed: validate.sh passes 23 skills (VPN/IPSec skill added)

## Expected Output

- `skills/zero-trust-assessment/SKILL.md` — ZT maturity assessment skill with 5-pillar scoring rubric, vendor-agnostic body, ≤2700 words
- `skills/zero-trust-assessment/references/maturity-model.md` — ZT maturity framework with pillar definitions, level criteria, and scoring methodology
- `skills/zero-trust-assessment/references/cli-reference.md` — Multi-vendor ZT control validation commands
