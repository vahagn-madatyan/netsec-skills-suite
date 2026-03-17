---
estimated_steps: 5
estimated_files: 3
---

# T02: Create network-topology-discovery skill with CDP/LLDP, ARP/MAC, and routing table analysis

**Slice:** S04 — Network Operations & Change Management
**Milestone:** M001

## Description

Create the `skills/network-topology-discovery/` skill directory with SKILL.md and two reference files. This skill guides an agent through iterative network topology discovery — building a map layer by layer using neighbor discovery protocols, routing tables, and MAC/ARP correlation across Cisco, Juniper, and Arista platforms.

Unlike threshold-based skills, this one has a unique iterative procedure shape: the agent discovers neighbors at each layer, then uses those as seeds to discover the next layer. The procedure builds a topology model progressively from L2 (CDP/LLDP, MAC tables) through L3 (ARP, routing tables) to produce a consolidated network map.

**Relevant installed skills:** none needed — this is markdown content authoring.

## Steps

1. **Create `skills/network-topology-discovery/SKILL.md`** with:
   - 6 frontmatter keys: `name: network-topology-discovery`, `description` (topology discovery via CDP/LLDP/ARP/MAC across 3 vendors), `license: Apache-2.0`, `metadata.safety: read-only`, `metadata.author: network-security-skills-suite`, `metadata.version: "1.0.0"`
   - H1 title, introductory paragraph, vendor labeling note (`[Cisco]`/`[JunOS]`/`[EOS]`)
   - 7 required H2 sections: When to Use, Prerequisites, Procedure, Threshold Tables, Decision Trees, Report Template, Troubleshooting
   - **Procedure** should cover: (1) Seed device identification — establish starting point and access method; (2) L2 neighbor discovery — CDP/LLDP neighbor collection, platform/capability identification; (3) MAC address table analysis — map MACs to ports, identify trunk vs access ports; (4) ARP table correlation — map IPs to MACs, identify L3 boundaries; (5) Routing table analysis — discover next-hops, identify routing domain boundaries; (6) Topology consolidation — merge L2 and L3 views, resolve duplicate entries, build adjacency model
   - **Threshold Tables** for this skill type: focus on completeness metrics (expected vs discovered neighbors, unresolved MACs, unknown next-hops) and staleness (ARP entry age, CDP/LLDP holdtime remaining)
   - **Decision Trees** should encode: missing expected neighbor → check CDP/LLDP enabled, check interface state, check VLAN mismatch; unresolved MAC → check trunk pruning, check spanning-tree state; asymmetric routing view → check VRF membership, check route filtering
   - Use `[Cisco]`/`[JunOS]`/`[EOS]` vendor labels where commands diverge
   - Body must stay ≤ 2700 words

2. **Create `skills/network-topology-discovery/references/cli-reference.md`** with:
   - Multi-vendor CLI command tables organized by discovery layer (neighbor protocols, MAC tables, ARP tables, routing tables)
   - 3-column format: Cisco | JunOS | EOS
   - Include notes on CDP (Cisco-proprietary) vs LLDP (standards-based) availability per vendor
   - Include VRF-aware command variants

3. **Create `skills/network-topology-discovery/references/discovery-workflow.md`** with:
   - Layer-by-layer discovery methodology
   - Topology data model (what data to collect per device, per link, per subnet)
   - Seed expansion algorithm — how to use discovered neighbors as next-hop discovery targets
   - Deduplication and reconciliation patterns — handling the same link seen from both ends
   - Scope control — how to bound discovery to a specific domain/VRF/site

4. **Validate the skill:**
   - Run `agentskills validate skills/network-topology-discovery` → must exit 0
   - Run `bash scripts/validate.sh` → must pass with 0 errors
   - Check body word count ≤ 2700

5. **Verify structure:**
   - Confirm 6 frontmatter keys with `safety: read-only`
   - Confirm 7 required H2 sections
   - Confirm `references/` has `cli-reference.md` and `discovery-workflow.md`

## Must-Haves

- [ ] SKILL.md has 6 frontmatter keys with `metadata.safety: read-only`
- [ ] SKILL.md has all 7 required H2 sections
- [ ] SKILL.md body ≤ 2700 words
- [ ] Uses `[Cisco]`/`[JunOS]`/`[EOS]` vendor labeling pattern
- [ ] Procedure follows iterative layer-by-layer discovery structure (L2 → L3 → consolidation)
- [ ] `references/cli-reference.md` exists with multi-vendor command tables
- [ ] `references/discovery-workflow.md` exists with topology building methodology
- [ ] `agentskills validate skills/network-topology-discovery` exits 0
- [ ] `bash scripts/validate.sh` passes

## Verification

- `agentskills validate skills/network-topology-discovery` → exit 0
- `bash scripts/validate.sh` → includes network-topology-discovery in checks, 0 errors
- `awk 'BEGIN{c=0}/^---$/{c++;if(c==2){f=1;next}}f{print}' skills/network-topology-discovery/SKILL.md | wc -w` → ≤ 2700
- `ls skills/network-topology-discovery/references/` → shows `cli-reference.md` and `discovery-workflow.md`

## Inputs

- `skills/bgp-analysis/SKILL.md` — Reference for 3-vendor labeling pattern and frontmatter structure
- `skills/bgp-analysis/references/cli-reference.md` — Reference for multi-vendor CLI table format
- `scripts/validate.sh` — Validation script that checks all skills

## Expected Output

- `skills/network-topology-discovery/SKILL.md` — Complete topology discovery skill with iterative L2/L3 procedure
- `skills/network-topology-discovery/references/cli-reference.md` — Multi-vendor discovery CLI commands
- `skills/network-topology-discovery/references/discovery-workflow.md` — Topology building methodology and data model
