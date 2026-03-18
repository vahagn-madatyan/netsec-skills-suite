# S04: Additional Security Skills & Suite Finalization

**Goal:** Deliver the final 3 security skills (VPN/IPSec troubleshooting, zero-trust assessment, wireless security audit) and finalize the full 25-skill suite with README catalog completion and milestone verification.
**Demo:** `bash scripts/validate.sh` passes 25 skills with 0 errors, `npx skills add . --list` discovers all 25, README catalog is complete with all 13 M002 security skills.

## Must-Haves

- VPN/IPSec troubleshooting skill with IKEv1/IKEv2 state machine diagnosis, 4-vendor coverage ([Cisco]/[JunOS]/[PAN-OS]/[FortiGate]), references/state-machine.md + references/cli-reference.md
- Zero-trust assessment skill with 5-pillar maturity scoring rubric (identity, device, network, application, data), Threshold Tables used for maturity level scoring, references/maturity-model.md + references/cli-reference.md
- Wireless security audit skill with SSID policy audit, 802.1X validation, rogue AP detection, 3-vendor coverage ([Cisco WLC]/[Aruba]/[Meraki]), references/security-standards.md + references/cli-reference.md
- All 3 skills are safety: read-only with ≤2700 word bodies
- README catalog has 3 new rows under existing "Security Skills" header
- `bash scripts/validate.sh` → 25 skills, 0 errors
- `npx skills add . --list` → "Found 25 skills"
- Zero regression on all 22 existing skills

## Proof Level

- This slice proves: final-assembly
- Real runtime required: no
- Human/UAT required: no

## Verification

- `bash scripts/validate.sh` → "Skills checked: 25", "Result: PASS (0 errors)"
- `npx skills add . --list` → "Found 25 skills"
- `awk 'BEGIN{c=0} /^---$/{c++; if(c==2){found=1; next}} found{print}' skills/vpn-ipsec-troubleshooting/SKILL.md | wc -w` → ≤2700
- `awk 'BEGIN{c=0} /^---$/{c++; if(c==2){found=1; next}} found{print}' skills/zero-trust-assessment/SKILL.md | wc -w` → ≤2700
- `awk 'BEGIN{c=0} /^---$/{c++; if(c==2){found=1; next}} found{print}' skills/wireless-security-audit/SKILL.md | wc -w` → ≤2700
- `ls skills/vpn-ipsec-troubleshooting/references/ | wc -l` → 2
- `ls skills/zero-trust-assessment/references/ | wc -l` → 2
- `ls skills/wireless-security-audit/references/ | wc -l` → 2
- `grep -c 'IKE\|IKEv2\|SA\|phase' skills/vpn-ipsec-troubleshooting/SKILL.md` → ≥10
- `grep -c 'maturity\|pillar\|score\|Level' skills/zero-trust-assessment/SKILL.md` → ≥10
- `grep -c '802.1X\|WPA3\|rogue\|SSID' skills/wireless-security-audit/SKILL.md` → ≥5
- `grep -c 'vpn-ipsec\|zero-trust\|wireless-security' README.md` → 3

## Observability / Diagnostics

- **Validation signal:** `bash scripts/validate.sh` — checks frontmatter safety tier, 7 required H2 sections, and references/ directory for every skill. Reports per-skill pass/fail with total count and error summary.
- **Word-count inspection:** `awk 'BEGIN{c=0} /^---$/{c++; if(c==2){found=1; next}} found{print}' skills/<name>/SKILL.md | wc -w` — must return ≤2700 for each new skill.
- **Scope guard:** `grep -ci 'ssl.vpn\|ssl vpn\|tls vpn' skills/vpn-ipsec-troubleshooting/SKILL.md` — must return 0 to confirm IPSec-only scope.
- **Content density:** `grep -c 'IKE\|IKEv2\|SA\|phase' skills/vpn-ipsec-troubleshooting/SKILL.md` (≥10), `grep -c 'maturity\|pillar\|score\|Level' skills/zero-trust-assessment/SKILL.md` (≥10), `grep -c '802.1X\|WPA3\|rogue\|SSID' skills/wireless-security-audit/SKILL.md` (≥5).
- **Reference file count:** `ls skills/<name>/references/ | wc -l` — must be 2 per skill.
- **Failure visibility:** validate.sh exits non-zero and prints `FAIL (N errors)` with per-skill ERROR lines to stderr identifying missing sections, bad frontmatter, or absent references/.
- **Redaction:** No secrets or credentials — all skills are documentation-only with example CLI commands.

## Integration Closure

- Upstream surfaces consumed: S01 proven security audit skill pattern, S02 compliance scoring pattern (Threshold Tables for maturity), M001 BGP FSM procedure shape (for VPN/IPSec state machine)
- New wiring introduced in this slice: none — 3 new skills follow established conventions
- What remains before the milestone is truly usable end-to-end: nothing — this is the final slice

## Tasks

- [x] **T01: Build VPN/IPSec troubleshooting skill with IKE state machine diagnosis** `est:45m`
  - Why: Delivers R027. Reuses the FSM procedure shape from bgp-analysis — IKE negotiation is a state machine like BGP's, with IKEv1 Main/Aggressive Mode and IKEv2 SA_INIT/SA_AUTH exchanges.
  - Files: `skills/vpn-ipsec-troubleshooting/SKILL.md`, `skills/vpn-ipsec-troubleshooting/references/state-machine.md`, `skills/vpn-ipsec-troubleshooting/references/cli-reference.md`
  - Do: Create SKILL.md with IKEv1/IKEv2 negotiation diagnosis procedure following BGP FSM shape (check SA state → diagnose stuck state → verify crypto params → validate phase 2 → assess tunnel health → report). Include [Cisco]/[JunOS]/[PAN-OS]/[FortiGate] vendor labels. Create state-machine.md with IKEv1 Main Mode (6-message), Aggressive Mode (3-message), IKEv2 SA_INIT/SA_AUTH, and Quick Mode (phase 2) FSMs. Create cli-reference.md with 4-vendor VPN commands organized by diagnosis phase. Body must be ≤2700 words, safety: read-only. Scoped to IPSec/IKE only — NOT SSL/TLS VPN.
  - Verify: `bash scripts/validate.sh 2>&1 | grep -E 'Skills checked|Result'` → 23 skills, PASS. Word count ≤2700. `grep -c 'IKE\|IKEv2\|SA\|phase' skills/vpn-ipsec-troubleshooting/SKILL.md` → ≥10.
  - Done when: validate.sh passes 23 skills, body ≤2700 words, 2 reference files present, IKE-specific content confirmed

- [x] **T02: Build zero-trust assessment skill with maturity scoring rubric** `est:45m`
  - Why: Delivers R028. Introduces the "maturity scoring" procedure shape (D028) — a rubric-based posture assessment where Threshold Tables map to maturity level scoring across 5 ZT pillars.
  - Files: `skills/zero-trust-assessment/SKILL.md`, `skills/zero-trust-assessment/references/maturity-model.md`, `skills/zero-trust-assessment/references/cli-reference.md`
  - Do: Create SKILL.md with 5-pillar ZT assessment (identity, device, network, application, data) × 5 maturity levels (L1 Traditional → L5 Optimal). Vendor-agnostic — no inline vendor labels. Threshold Tables section maps maturity scores to pillar levels. Reference NIST SP 800-207 ZTA model (public domain). Create maturity-model.md with pillar definitions, scoring criteria, and assessment methodology. Create cli-reference.md with ZT control validation commands across [Cisco]/[JunOS]/[PAN-OS]/[FortiGate]. Body must be ≤2700 words, safety: read-only.
  - Verify: `bash scripts/validate.sh 2>&1 | grep -E 'Skills checked|Result'` → 24 skills, PASS. Word count ≤2700. `grep -c 'maturity\|pillar\|score\|Level' skills/zero-trust-assessment/SKILL.md` → ≥10.
  - Done when: validate.sh passes 24 skills, body ≤2700 words, 2 reference files present, maturity scoring rubric confirmed

- [ ] **T03: Build wireless security audit skill with multi-controller coverage** `est:45m`
  - Why: Delivers R029. Combines the policy audit shape (from S01 firewall skills) with maturity scoring (from T02). Uses new vendor labels: [Cisco WLC]/[Aruba]/[Meraki].
  - Files: `skills/wireless-security-audit/SKILL.md`, `skills/wireless-security-audit/references/security-standards.md`, `skills/wireless-security-audit/references/cli-reference.md`
  - Do: Create SKILL.md with SSID policy audit (encryption, auth, VLAN), 802.1X validation (RADIUS, EAP, certificates), rogue AP detection methodology, RF security assessment, guest network isolation. Use [Cisco WLC]/[Aruba]/[Meraki] vendor labels. Create security-standards.md with 802.1X/EAP state machine, WPA3 requirements, RF security best practices. Create cli-reference.md with wireless controller commands per vendor (note: Meraki uses Dashboard API, not CLI). Body must be ≤2700 words, safety: read-only.
  - Verify: `bash scripts/validate.sh 2>&1 | grep -E 'Skills checked|Result'` → 25 skills, PASS. Word count ≤2700. `grep -c '802.1X\|WPA3\|rogue\|SSID' skills/wireless-security-audit/SKILL.md` → ≥5.
  - Done when: validate.sh passes 25 skills, body ≤2700 words, 2 reference files present, wireless-specific content confirmed

- [ ] **T04: Update README catalog and run full suite verification** `est:15m`
  - Why: Finalizes the suite. Adds 3 catalog rows to README and runs the milestone's key verification: `npx skills add . --list` must report "Found 25 skills". Also confirms zero regression on all 22 pre-existing skills.
  - Files: `README.md`
  - Do: Add 3 rows to the README catalog table under the existing "Security Skills" bold separator (do NOT create a new section header). Rows: vpn-ipsec-troubleshooting, zero-trust-assessment, wireless-security-audit with descriptions and `read-only` safety tier. Run `bash scripts/validate.sh` (25 skills, 0 errors). Run `npx skills add . --list` (Found 25 skills). Verify all 3 new skills word counts ≤2700. Confirm `grep -c 'vpn-ipsec\|zero-trust\|wireless-security' README.md` → 3.
  - Verify: `bash scripts/validate.sh` → 25/PASS. `npx skills add . --list` → Found 25 skills. `grep -c 'vpn-ipsec\|zero-trust\|wireless-security' README.md` → 3.
  - Done when: Full suite passes validation, npx discovers 25 skills, README has 25 catalog rows, zero regression

## Files Likely Touched

- `skills/vpn-ipsec-troubleshooting/SKILL.md`
- `skills/vpn-ipsec-troubleshooting/references/state-machine.md`
- `skills/vpn-ipsec-troubleshooting/references/cli-reference.md`
- `skills/zero-trust-assessment/SKILL.md`
- `skills/zero-trust-assessment/references/maturity-model.md`
- `skills/zero-trust-assessment/references/cli-reference.md`
- `skills/wireless-security-audit/SKILL.md`
- `skills/wireless-security-audit/references/security-standards.md`
- `skills/wireless-security-audit/references/cli-reference.md`
- `README.md`
