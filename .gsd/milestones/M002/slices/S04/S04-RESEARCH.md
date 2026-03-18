# S04: Additional Security Skills & Suite Finalization — Research

**Date:** 2026-03-17
**Researcher:** auto

## Summary

S04 is the lowest-risk slice in M002 — three skills using proven patterns from S01/S02/S03 plus a README update and final suite verification. All infrastructure (validate.sh, CI, README catalog structure, references/ convention) is stable with 22 skills passing validation. No new tooling, no new conventions, no copyright constraints.

VPN/IPSec troubleshooting (R027) directly reuses M001's protocol FSM procedure shape from bgp-analysis — IKE negotiation is a state machine exactly like BGP's FSM, with a `references/state-machine.md` documenting IKEv1/IKEv2 phase transitions. Zero-trust assessment (R028) introduces the "maturity scoring" procedure shape (D028), which is structurally simple — a rubric-based posture assessment where Threshold Tables map naturally to maturity level scoring. Wireless security audit (R029) combines the policy audit shape (from S01 firewall skills) with maturity scoring for posture assessment.

The only coordination needed: README catalog gets 3 new rows under the existing "Security Skills" header (per S01 Forward Intelligence — do NOT create new section rows), and the final verification must confirm `npx skills add . --list` reports "Found 25 skills".

## Recommendation

**Build order: VPN/IPSec → zero-trust → wireless → README + final verification.** VPN/IPSec first because it reuses the most proven pattern (FSM from M001). Zero-trust second because the maturity scoring procedure shape is new but structurally simple. Wireless last because it combines patterns from both previous S04 skills plus S01/S02 precedents. README + full suite verification as a final task.

All 3 skills are safety: read-only (D027). Multi-vendor labels for VPN ([Cisco]/[JunOS]/[PAN-OS]/[FortiGate]) and wireless ([Cisco WLC]/[Aruba]/[Meraki]). Zero-trust is vendor-agnostic (no inline labels — it assesses architecture, not device configs).

## Implementation Landscape

### Key Files

**To create:**

- `skills/vpn-ipsec-troubleshooting/SKILL.md` — IKEv1/IKEv2 negotiation diagnosis, SA lifecycle, crypto mismatch troubleshooting. Reuses protocol FSM procedure shape from `skills/bgp-analysis/SKILL.md`. Multi-vendor: [Cisco]/[JunOS]/[PAN-OS]/[FortiGate].
- `skills/vpn-ipsec-troubleshooting/references/state-machine.md` — IKE phase 1 (Main Mode 6-message / Aggressive Mode 3-message) and phase 2 (Quick Mode) state machines with IKEv2 SA_INIT/SA_AUTH exchange. Direct analog to `skills/bgp-analysis/references/state-machine.md`.
- `skills/vpn-ipsec-troubleshooting/references/cli-reference.md` — VPN debug/show commands per vendor: `show crypto isakmp sa` (Cisco), `show security ike/ipsec` (JunOS), `show vpn ike-sa/ipsec-sa` (PAN-OS), `diagnose vpn ike/tunnel` (FortiGate).
- `skills/zero-trust-assessment/SKILL.md` — Maturity scoring rubric across 5 ZT pillars (identity, device, network, application, data). Vendor-agnostic. Threshold Tables section used for maturity level scoring (Level 1–5). New "maturity scoring" procedure shape (D028).
- `skills/zero-trust-assessment/references/maturity-model.md` — ZT maturity framework with pillar definitions, scoring criteria per level, and assessment methodology.
- `skills/zero-trust-assessment/references/cli-reference.md` — Validation commands across vendors for ZT controls: 802.1X status, segmentation verification, AAA config, policy enforcement points.
- `skills/wireless-security-audit/SKILL.md` — SSID policy audit, 802.1X validation, WPA3 assessment, rogue AP detection guidance, RF security posture. Multi-vendor: [Cisco WLC]/[Aruba]/[Meraki]. Combines policy audit + maturity scoring shapes.
- `skills/wireless-security-audit/references/security-standards.md` — 802.1X EAP state machine, WPA3-Enterprise/Personal requirements, RF security best practices, rogue AP classification.
- `skills/wireless-security-audit/references/cli-reference.md` — Wireless controller show/debug commands per vendor for security audit.

**To modify:**

- `README.md` — Add 3 catalog rows under existing "Security Skills" bold separator (line 41). Do NOT add a new section header.

**Unchanged (pattern references):**

- `skills/bgp-analysis/SKILL.md` — FSM procedure shape precedent (6-step protocol state machine diagnosis)
- `skills/bgp-analysis/references/state-machine.md` — FSM reference file structure precedent (215 lines, states + transitions + stuck causes)
- `skills/cis-benchmark-audit/SKILL.md` — Threshold Tables scoring pattern precedent (severity tiers as scoring rubric)
- `skills/palo-alto-firewall-audit/SKILL.md` — Policy audit procedure shape precedent (inventory → rule analysis → profile coverage → assessment)
- `scripts/validate.sh` — No changes needed. Already validates 7 H2 sections, safety tier, references/ directory.

### Build Order

**Task 1: vpn-ipsec-troubleshooting** — Build first because the FSM pattern is the most proven (bgp-analysis is the direct precedent). IKE negotiation maps cleanly: IKEv1 Main Mode has 6 defined states (MM_NO_STATE → MM_SA_SETUP → MM_KEY_EXCH → MM_KEY_AUTH → QM_IDLE); IKEv2 has SA_INIT/SA_AUTH/CHILD_SA exchanges. The procedure follows bgp-analysis flow: check SA state → diagnose stuck state → verify crypto parameters → validate phase 2 → assess tunnel health → report.

Reference files:
- `state-machine.md` — IKEv1 Main/Aggressive mode FSMs, IKEv2 exchange FSMs, Quick Mode (phase 2), common stuck states with causes. Follow the bgp-analysis/references/state-machine.md structure (states → transitions → stuck diagnostics).
- `cli-reference.md` — 4-vendor VPN show/debug commands organized by diagnosis phase (SA status, crypto params, tunnel counters, DPD status, NAT-T detection).

Multi-vendor scope: [Cisco] (IOS-XE `show crypto`), [JunOS] (`show security ike/ipsec`), [PAN-OS] (`show vpn ike-sa/ipsec-sa`), [FortiGate] (`diagnose vpn ike/tunnel`). R027 says "Multi-vendor coverage."

Key content areas: IKEv1 vs IKEv2 differences, crypto parameter mismatch diagnosis (DH group, encryption algo, hash algo, lifetime), NAT-T (NAT Traversal) detection, DPD (Dead Peer Detection) tuning, SA rekey lifecycle, split tunneling vs full tunnel verification. Per R027: "IPSec/IKE troubleshooting" only — NOT SSL VPN.

**Task 2: zero-trust-assessment** — Build second. New "maturity scoring" procedure shape (D028) but structurally simple: assess 5 pillars × 5 maturity levels = scoring matrix. The Threshold Tables section maps perfectly to maturity level definitions. Vendor-agnostic — assesses architecture posture, not device-specific configs.

Reference files:
- `maturity-model.md` — ZT pillars (identity, device, network, application, data), maturity levels (L1 Traditional → L5 Optimal), scoring criteria per pillar×level combination, overall maturity calculation methodology.
- `cli-reference.md` — Validation commands for ZT controls across platforms: 802.1X config verification, micro-segmentation checks (VLAN/VRF/SGT), AAA/RADIUS/TACACS+ config, policy enforcement point status. Multi-vendor where applicable: [Cisco]/[JunOS]/[PAN-OS]/[FortiGate].

Key content areas: NIST SP 800-207 ZTA reference model (public domain), 5-pillar assessment framework, identity verification (MFA, certificate-based auth, NAC), micro-segmentation (network segmentation beyond VLANs — SGT/TrustSec, VRF-lite, PAN-OS zones), least privilege analysis (rule permissiveness scoring from S01/S02 patterns), continuous verification (session monitoring, re-authentication policies).

**Task 3: wireless-security-audit** — Build last. Combines the policy audit shape (S01) with maturity scoring (Task 2). The most independent skill — no dependency on Task 1 or Task 2 content, only on shared patterns.

Reference files:
- `security-standards.md` — 802.1X/EAP authentication state machine (Supplicant ↔ Authenticator ↔ RADIUS), WPA3-Enterprise (192-bit mode, SAE, PMF) vs WPA3-Personal requirements, RF security (rogue AP classification, WIDS/WIPS capabilities, channel isolation), guest network isolation requirements.
- `cli-reference.md` — Wireless controller commands for [Cisco WLC] (show wlan, show client, show rogue), [Aruba] (show ap, show wlan, show aaa), [Meraki] (Dashboard API endpoints — Meraki is API-only for automation).

Key content areas: SSID security policy audit (encryption mode, authentication method, VLAN assignment), 802.1X validation (RADIUS server reachability, EAP method verification, certificate chain), rogue AP detection methodology (classification: valid, interfering, malicious), RF security assessment (channel utilization, power levels, containment verification), guest network isolation (captive portal, bandwidth limits, VLAN separation).

**Task 4: README catalog + suite finalization** — Final task. Add 3 rows to README catalog. Run full verification battery:
- `bash scripts/validate.sh` → 25 skills, 0 errors
- `npx skills add . --list` → "Found 25 skills"
- Word count all 3 new skills ≤ 2700
- All 22 existing skills pass unchanged (no regression)

### Verification Approach

Per-task verification (same as S01/S02/S03):

1. `agentskills validate skills/<skill-name>` → exit 0
2. `bash scripts/validate.sh` → 0 errors (cumulative: 23 after T01, 24 after T02, 25 after T03)
3. `awk 'BEGIN{c=0} /^---$/{c++; if(c==2){found=1; next}} found{print}' skills/<name>/SKILL.md | wc -w` → ≤ 2700 (K001 pattern)
4. Each skill has `references/` with exactly 2 files
5. Each skill has `metadata.safety: read-only` in frontmatter

Final suite verification (T04):

6. `bash scripts/validate.sh` → "Skills checked: 25", "Result: PASS (0 errors)"
7. `npx skills add . --list` → "Found 25 skills"
8. `grep -c 'vpn-ipsec\|zero-trust\|wireless-security' README.md` → 3
9. All 22 pre-existing skills still pass (no regression — validate.sh covers this)

Content verification (spot-check):

10. VPN skill: `grep -c 'IKE\|IKEv2\|SA\|phase' skills/vpn-ipsec-troubleshooting/SKILL.md` → ≥ 10 (confirms IKE-specific content, not generic VPN)
11. Zero-trust skill: `grep -c 'maturity\|pillar\|score\|Level' skills/zero-trust-assessment/SKILL.md` → ≥ 10 (confirms scoring rubric presence)
12. Wireless skill: `grep -c '802.1X\|WPA3\|rogue\|SSID' skills/wireless-security-audit/SKILL.md` → ≥ 5 (confirms wireless-specific content)

## Constraints

- All 3 skills are safety: read-only (D027). No write operations, no remediation execution.
- ≤ 2700 word body budget per skill (proven across 22 skills). VPN/IPSec may be tight with 4-vendor coverage — monitor word count during authoring, compress Troubleshooting section if needed (proven technique from S01/S03).
- VPN skill scoped to IPSec/IKE only — NOT SSL/TLS VPN (R027 explicit scope).
- Zero-trust skill must use Threshold Tables for maturity scoring (validate.sh requires the section). The scoring rubric is a natural fit.
- Wireless controller vendors differ from network device vendors in M001. [Cisco WLC]/[Aruba]/[Meraki] are new vendor labels not used elsewhere in the suite — consistent with the labeling convention but new platform scopes.
- README catalog rows go under the existing "Security Skills" bold separator row (line 41). Do NOT create a new section header (S01 Forward Intelligence).
