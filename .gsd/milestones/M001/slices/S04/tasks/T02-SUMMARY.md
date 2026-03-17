---
id: T02
parent: S04
milestone: M001
provides:
  - network-topology-discovery skill with iterative L2/L3 discovery procedure
key_files:
  - skills/network-topology-discovery/SKILL.md
  - skills/network-topology-discovery/references/cli-reference.md
  - skills/network-topology-discovery/references/discovery-workflow.md
key_decisions: []
patterns_established:
  - Iterative procedure shape — seed expansion algorithm with layer-by-layer discovery (vs threshold-comparison shape used in device-health and interface-health skills)
  - Completeness/freshness threshold tables for discovery-type skills (vs error-rate thresholds for health-check skills)
observability_surfaces:
  - "agentskills validate skills/network-topology-discovery → exit 0"
  - "bash scripts/validate.sh → includes network-topology-discovery, PASS"
  - "Word count: 2272 words (≤2700 limit)"
duration: 12m
verification_result: passed
completed_at: 2026-03-16
blocker_discovered: false
---

# T02: Create network-topology-discovery skill with CDP/LLDP, ARP/MAC, and routing table analysis

**Created complete network-topology-discovery skill with 6-step iterative L2→L3 procedure, 3-vendor coverage, completeness/freshness threshold tables, and topology consolidation methodology.**

## What Happened

Built the network-topology-discovery skill with three files following the established patterns from bgp-analysis and interface-health. The skill introduces a unique iterative procedure shape — unlike threshold-based health checks, the procedure works outward from a seed device using a seed expansion algorithm.

SKILL.md covers 6 procedure steps: (1) Seed device identification, (2) L2 neighbor discovery via CDP/LLDP, (3) MAC address table analysis, (4) ARP table correlation, (5) Routing table analysis, (6) Topology consolidation. Each step builds on prior data, expanding the discovery outward layer by layer.

The cli-reference.md organizes multi-vendor commands by discovery layer (neighbor protocols, MAC tables, ARP tables, routing tables, routing protocol neighbors, device identification) with CDP vs LLDP availability notes and VRF-aware variants.

The discovery-workflow.md describes the topology data model (per-device, per-link, per-subnet records), the seed expansion algorithm with pseudocode, deduplication/reconciliation patterns for handling links seen from both ends, and scope control mechanisms (by subnet, VRF, hostname pattern, hop count).

## Verification

- `agentskills validate skills/network-topology-discovery` → exit 0 ✅
- `bash scripts/validate.sh` → 10 skills checked, 0 errors, PASS ✅
- Body word count: 2272 words (≤2700) ✅
- Frontmatter: 6 keys with `metadata.safety: read-only` ✅
- H2 sections: all 7 required sections present ✅
- References: `cli-reference.md` and `discovery-workflow.md` present ✅

### Slice-level verification (partial — T02 of T05):
- `agentskills validate` passes for 10 skills (T01 + T02 added) ✅
- `bash scripts/validate.sh` → PASS across all 10 skills ✅
- README catalog update and 12-skill final validation deferred to T05

## Diagnostics

- `agentskills validate skills/network-topology-discovery` — structural validation
- `bash scripts/validate.sh` — suite-wide validation
- `awk 'BEGIN{c=0}/^---$/{c++;if(c==2){f=1;next}}f{print}' skills/network-topology-discovery/SKILL.md | wc -w` — body word count
- `ls skills/network-topology-discovery/references/` — reference file inventory

## Deviations

- Pre-flight fix: Added `## Observability Impact` section to T02-PLAN.md as required by the pre-flight check.

## Known Issues

None.

## Files Created/Modified

- `skills/network-topology-discovery/SKILL.md` — Complete topology discovery skill with 6-step iterative procedure, 3-vendor commands, completeness thresholds, and decision trees
- `skills/network-topology-discovery/references/cli-reference.md` — Multi-vendor CLI commands organized by discovery layer (neighbor protocols, MAC, ARP, routing, device ID)
- `skills/network-topology-discovery/references/discovery-workflow.md` — Topology data model, seed expansion algorithm, deduplication patterns, scope control
- `.gsd/milestones/M001/slices/S04/tasks/T02-PLAN.md` — Added Observability Impact section (pre-flight fix)
