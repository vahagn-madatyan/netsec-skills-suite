---
estimated_steps: 5
estimated_files: 3
---

# T01: Build VPN/IPSec troubleshooting skill with IKE state machine diagnosis

**Slice:** S04 — Additional Security Skills & Suite Finalization
**Milestone:** M002

## Description

Create the VPN/IPSec troubleshooting skill (R027) using the protocol FSM procedure shape proven by `skills/bgp-analysis/SKILL.md`. IKE negotiation is a state machine exactly like BGP's FSM — IKEv1 Main Mode has defined states (MM_NO_STATE → MM_SA_SETUP → MM_KEY_EXCH → MM_KEY_AUTH → QM_IDLE), and IKEv2 has SA_INIT/SA_AUTH/CHILD_SA exchanges.

The skill covers IPSec/IKE troubleshooting ONLY — NOT SSL/TLS VPN (R027 explicit scope). Multi-vendor with [Cisco]/[JunOS]/[PAN-OS]/[FortiGate] inline labels. Safety: read-only (D027). Body must be ≤2700 words.

## Steps

1. Create `skills/vpn-ipsec-troubleshooting/references/state-machine.md` documenting IKE FSMs:
   - IKEv1 Main Mode 6-message exchange (3 pairs: SA proposal → KE/Nonce → ID/Auth)
   - IKEv1 Aggressive Mode 3-message exchange
   - IKEv2 SA_INIT/SA_AUTH exchange model
   - Quick Mode (IPSec phase 2) SA negotiation
   - Common stuck states with causes: MM_NO_STATE (no response), MM_KEY_EXCH (DH mismatch), QM_IDLE (phase 1 up but no phase 2)
   - Follow the structure of `skills/bgp-analysis/references/state-machine.md`: states → transitions → stuck diagnostics

2. Create `skills/vpn-ipsec-troubleshooting/references/cli-reference.md` with 4-vendor VPN show/debug commands organized by diagnosis phase:
   - SA status: `show crypto isakmp sa` (Cisco), `show security ike security-associations` (JunOS), `show vpn ike-sa` (PAN-OS), `diagnose vpn ike gateway list` (FortiGate)
   - Crypto parameters: proposal/transform-set verification commands
   - Tunnel counters: encap/decap, errors, rekey counters
   - DPD status: Dead Peer Detection timers and stats
   - NAT-T detection: NAT Traversal status and encapsulation mode
   - Use table format organized by audit category (same as firewall cli-reference.md pattern)

3. Create `skills/vpn-ipsec-troubleshooting/SKILL.md` with:
   - Frontmatter: name, description, license: Apache-2.0, metadata.safety: read-only, metadata.author: network-security-skills-suite, metadata.version: "1.0.0"
   - Intro paragraph explaining FSM-based VPN diagnosis approach with [Cisco]/[JunOS]/[PAN-OS]/[FortiGate] vendor labels
   - 7 required H2 sections: When to Use, Prerequisites, Procedure, Threshold Tables, Decision Trees, Report Template, Troubleshooting
   - Procedure follows BGP FSM shape: (1) Check IKE SA State → (2) Diagnose Stuck/Failed State → (3) Verify Crypto Parameter Alignment → (4) Validate Phase 2 / Child SA → (5) Assess Tunnel Health → (6) Report
   - Threshold Tables: SA lifetime percentages, rekey intervals, DPD timer ranges, encap/decap counter thresholds
   - Decision Trees: IKE SA state triage (phase 1 failure vs phase 2 failure vs established-but-no-traffic)
   - Key content: IKEv1 vs IKEv2 differences, crypto mismatch diagnosis (DH group, encryption, hash, lifetime), NAT-T, DPD tuning, SA rekey lifecycle, split-tunnel vs full-tunnel verification

4. Verify word count: `awk 'BEGIN{c=0} /^---$/{c++; if(c==2){found=1; next}} found{print}' skills/vpn-ipsec-troubleshooting/SKILL.md | wc -w` → must be ≤2700. If over budget, compress Troubleshooting section prose (proven technique from S01 FortiGate/Cisco).

5. Run validation: `bash scripts/validate.sh 2>&1 | grep -E 'Skills checked|Result'` → must show 23 skills, PASS.

## Must-Haves

- [ ] SKILL.md has valid frontmatter with `metadata.safety: read-only`
- [ ] All 7 required H2 sections present: When to Use, Prerequisites, Procedure, Threshold Tables, Decision Trees, Report Template, Troubleshooting
- [ ] Procedure uses FSM procedure shape: SA state check → stuck diagnosis → crypto verification → phase 2 → health → report
- [ ] 4-vendor inline labels: [Cisco], [JunOS], [PAN-OS], [FortiGate]
- [ ] Scoped to IPSec/IKE only — zero mention of SSL VPN
- [ ] references/state-machine.md covers IKEv1 Main, Aggressive, IKEv2, Quick Mode
- [ ] references/cli-reference.md has commands for all 4 vendors
- [ ] Body ≤2700 words (awk K001 method)
- [ ] `bash scripts/validate.sh` passes with 23 skills

## Verification

- `bash scripts/validate.sh 2>&1 | grep 'Skills checked'` → "Skills checked: 23"
- `bash scripts/validate.sh 2>&1 | grep 'Result'` → "Result: PASS (0 errors)"
- `awk 'BEGIN{c=0} /^---$/{c++; if(c==2){found=1; next}} found{print}' skills/vpn-ipsec-troubleshooting/SKILL.md | wc -w` → ≤2700
- `ls skills/vpn-ipsec-troubleshooting/references/ | wc -l` → 2
- `grep -c 'IKE\|IKEv2\|SA\|phase' skills/vpn-ipsec-troubleshooting/SKILL.md` → ≥10
- `grep -ci 'ssl.vpn\|ssl vpn\|tls vpn' skills/vpn-ipsec-troubleshooting/SKILL.md` → 0

## Observability Impact

- **New inspection surface:** `bash scripts/validate.sh` will report 23 skills (was 22). The VPN/IPSec skill contributes 3 check lines (safety tier, 7 sections, references/).
- **How a future agent inspects this task:** Run `bash scripts/validate.sh 2>&1 | grep vpn-ipsec` to see pass/fail for this specific skill. Run the word-count awk command to verify body budget. Run `grep -ci 'ssl.vpn\|ssl vpn\|tls vpn'` to confirm IPSec-only scope.
- **Failure state visibility:** If IKE state machine content is missing or incomplete, `grep -c 'IKE\|IKEv2\|SA\|phase'` returns <10, signaling sparse protocol coverage. If word count exceeds 2700, the Troubleshooting section needs compression (proven technique from S01).

## Inputs

- `skills/bgp-analysis/SKILL.md` — FSM procedure shape precedent (6-step protocol state machine diagnosis flow)
- `skills/bgp-analysis/references/state-machine.md` — FSM reference file structure precedent (states → transitions → stuck causes)
- `skills/palo-alto-firewall-audit/SKILL.md` — Frontmatter and H2 section template for security skills
- `scripts/validate.sh` — Convention validator (7 H2 sections, safety tier, references/ directory)

## Expected Output

- `skills/vpn-ipsec-troubleshooting/SKILL.md` — VPN/IPSec troubleshooting skill with IKE FSM-based diagnosis procedure, 4-vendor coverage, ≤2700 body words
- `skills/vpn-ipsec-troubleshooting/references/state-machine.md` — IKEv1/IKEv2 state machines with stuck state diagnostics
- `skills/vpn-ipsec-troubleshooting/references/cli-reference.md` — 4-vendor VPN show/debug commands by diagnosis phase
