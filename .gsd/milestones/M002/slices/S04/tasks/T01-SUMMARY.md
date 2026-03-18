---
id: T01
parent: S04
milestone: M002
provides:
  - VPN/IPSec troubleshooting skill with IKE state machine diagnosis (R027)
  - IKEv1/IKEv2 FSM reference documentation
  - 4-vendor VPN diagnostic CLI reference
key_files:
  - skills/vpn-ipsec-troubleshooting/SKILL.md
  - skills/vpn-ipsec-troubleshooting/references/state-machine.md
  - skills/vpn-ipsec-troubleshooting/references/cli-reference.md
key_decisions:
  - Reused BGP FSM procedure shape for IKE state machine diagnosis — same 6-step flow (SA state → stuck diagnosis → crypto verify → phase 2 → health → report)
patterns_established:
  - IKE FSM procedure shape applies to any protocol state machine skill (IKEv1 Main/Aggressive, IKEv2 SA_INIT/SA_AUTH map directly to the BGP FSM precedent)
observability_surfaces:
  - "bash scripts/validate.sh 2>&1 | grep vpn-ipsec — per-skill validation"
  - "grep -c 'IKE|IKEv2|SA|phase' skills/vpn-ipsec-troubleshooting/SKILL.md — content density (≥10)"
  - "grep -ci 'ssl.vpn|ssl vpn|tls vpn' skills/vpn-ipsec-troubleshooting/SKILL.md — scope guard (must be 0)"
duration: 15m
verification_result: passed
completed_at: 2026-03-17
blocker_discovered: false
---

# T01: Build VPN/IPSec troubleshooting skill with IKE state machine diagnosis

**Created VPN/IPSec troubleshooting skill with IKE FSM-based diagnosis procedure, 4-vendor coverage, IKEv1/IKEv2 state machine reference, and diagnostic CLI command tables — 2506 words, 23 skills PASS.**

## What Happened

Built the VPN/IPSec troubleshooting skill following the BGP FSM procedure shape precedent. The skill uses IKE negotiation states as the primary diagnostic signal — reading the SA state (MM_NO_STATE, MM_SA_SETUP, MM_KEY_EXCH, QM_IDLE for IKEv1; SA_INIT/SA_AUTH/ESTABLISHED for IKEv2) maps directly to the failure domain without guesswork.

Created three files:
1. **state-machine.md** — Covers IKEv1 Main Mode (6-message, 3-pair exchange), Aggressive Mode (3-message), IKEv2 SA_INIT/SA_AUTH/CREATE_CHILD_SA model, and Quick Mode (Phase 2). Includes stuck-state tables mapping each state to causes and diagnosis steps, plus timer reference and NAT-T detection mechanism.
2. **cli-reference.md** — 4-vendor (Cisco/JunOS/PAN-OS/FortiGate) command tables organized by diagnosis phase: IKE SA status, IPSec SA status, crypto parameter verification, tunnel counters, DPD, NAT-T, and routing/tunnel interfaces. Table format matches the firewall cli-reference.md precedent.
3. **SKILL.md** — 6-step FSM procedure (Check IKE SA State → Diagnose Stuck/Failed State → Verify Crypto Parameter Alignment → Validate Phase 2/Child SA → Assess Tunnel Health → Report). Includes threshold tables for SA lifetimes, DPD timers, counter health, and crypto strength minimums. Decision trees cover IKE SA state triage and tunnel flapping triage. Troubleshooting covers proxy ID mismatch, NAT-T issues, DPD premature failover, rekey failures, and MTU/fragmentation. Scoped to IPSec/IKE only — zero mention of SSL/TLS VPN.

Also fixed pre-flight observability gaps: added `## Observability / Diagnostics` to S04-PLAN.md and `## Observability Impact` to T01-PLAN.md.

## Verification

- validate.sh reports 23 skills, PASS (0 errors) — up from 22
- Body word count is 2506 (under 2700 budget)
- 2 reference files in references/ directory
- IKE content density: 74 matches (≥10 required)
- SSL VPN scope guard: 0 matches (must be 0)
- All 7 required H2 sections present
- 22 vendor label instances across [Cisco]/[JunOS]/[PAN-OS]/[FortiGate]
- metadata.safety: read-only in frontmatter

## Verification Evidence

| # | Command | Exit Code | Verdict | Duration |
|---|---------|-----------|---------|----------|
| 1 | `bash scripts/validate.sh 2>&1 \| grep 'Skills checked'` | 0 | ✅ pass (23) | <1s |
| 2 | `bash scripts/validate.sh 2>&1 \| grep 'Result'` | 0 | ✅ pass (PASS 0 errors) | <1s |
| 3 | `awk ... SKILL.md \| wc -w` | 0 | ✅ pass (2506 ≤ 2700) | <1s |
| 4 | `ls references/ \| wc -l` | 0 | ✅ pass (2) | <1s |
| 5 | `grep -c 'IKE\|IKEv2\|SA\|phase'` | 0 | ✅ pass (74 ≥ 10) | <1s |
| 6 | `grep -ci 'ssl.vpn\|ssl vpn\|tls vpn'` | 1 | ✅ pass (0 = clean) | <1s |

## Diagnostics

- **Validation:** `bash scripts/validate.sh 2>&1 | grep vpn-ipsec` shows pass/fail for this skill
- **Word count:** `awk 'BEGIN{c=0} /^---$/{c++; if(c==2){found=1; next}} found{print}' skills/vpn-ipsec-troubleshooting/SKILL.md | wc -w`
- **Content density:** `grep -c 'IKE\|IKEv2\|SA\|phase' skills/vpn-ipsec-troubleshooting/SKILL.md` — should be ≥10
- **Scope guard:** `grep -ci 'ssl.vpn\|ssl vpn\|tls vpn' skills/vpn-ipsec-troubleshooting/SKILL.md` — must be 0

## Deviations

None.

## Known Issues

None.

## Files Created/Modified

- `skills/vpn-ipsec-troubleshooting/SKILL.md` — VPN/IPSec troubleshooting skill with IKE FSM procedure, 4-vendor coverage, 2506 words
- `skills/vpn-ipsec-troubleshooting/references/state-machine.md` — IKEv1 Main/Aggressive, IKEv2, Quick Mode FSMs with stuck-state diagnostics
- `skills/vpn-ipsec-troubleshooting/references/cli-reference.md` — 4-vendor VPN show/diagnostic commands by diagnosis phase
- `.gsd/milestones/M002/slices/S04/S04-PLAN.md` — Marked T01 done, added Observability section
- `.gsd/milestones/M002/slices/S04/tasks/T01-PLAN.md` — Added Observability Impact section
