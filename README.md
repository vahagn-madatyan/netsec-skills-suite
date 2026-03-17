# Network Security Skills Suite

AI agent skills for network security operations — device triage, configuration auditing, and incident response procedures for Cisco and multi-vendor environments.

![Validate Skills](https://github.com/vahagn-madatyan/network-security-skills-suite/actions/workflows/validate.yml/badge.svg)

## What Is This?

This repository is a curated collection of [Agent Skills](https://github.com/empoweragents/agent-skills) for network security engineering. Each skill is a structured procedure that an AI coding agent can load and follow — covering device health checks, security audits, configuration reviews, and more.

Skills are written in the Agent Skills SKILL.md format and enhanced with network-specific conventions: safety tier metadata, threshold tables, decision trees, and structured report templates.

## Install

```bash
npx skills add vahagn-madatyan/network-security-skills-suite
```

This discovers and installs all skills from the suite. To list available skills without installing:

```bash
npx skills add vahagn-madatyan/network-security-skills-suite --list
```

## Skill Catalog

| Skill | Description | Safety Tier |
|-------|-------------|-------------|
| [example-device-health](skills/example-device-health/SKILL.md) | Cisco IOS-XE device health check and triage procedure (reference implementation) | `read-only` |
| [cisco-device-health](skills/cisco-device-health/SKILL.md) | Cisco IOS-XE and NX-OS dual-platform device health check with QFP/RP and VDC-aware triage | `read-only` |
| [juniper-device-health](skills/juniper-device-health/SKILL.md) | Juniper JunOS device health check with RE/PFE separation, alarm-first triage, and dual-RE failover detection | `read-only` |
| [arista-device-health](skills/arista-device-health/SKILL.md) | Arista EOS device health check with agent monitoring, MLAG state validation, and VXLAN/EVPN DC extensions | `read-only` |
| [bgp-analysis](skills/bgp-analysis/SKILL.md) | BGP protocol analysis — peer state diagnosis, path selection, route filtering, convergence (Cisco/JunOS/EOS) | `read-only` |
| [ospf-analysis](skills/ospf-analysis/SKILL.md) | OSPF adjacency diagnosis, area design validation, LSA analysis, SPF convergence (Cisco/JunOS/EOS) | `read-only` |
| [eigrp-analysis](skills/eigrp-analysis/SKILL.md) | EIGRP DUAL analysis — successor/feasible successor, stuck-in-active diagnosis, K-value validation (Cisco IOS-XE/NX-OS) | `read-only` |
| [isis-analysis](skills/isis-analysis/SKILL.md) | IS-IS adjacency diagnosis, LSPDB analysis, level 1/2 routing, NET validation (Cisco/JunOS/EOS) | `read-only` |
| [change-verification](skills/change-verification/SKILL.md) | Pre/post change verification with baseline capture, diff analysis, and rollback guidance (Cisco/JunOS/EOS) | `read-write` |
| [config-management](skills/config-management/SKILL.md) | Config backup, drift detection, and golden config validation with compliance checking (Cisco/JunOS/EOS) | `read-write` |
| [interface-health](skills/interface-health/SKILL.md) | Interface error analysis — CRC, discards, resets, optical power monitoring with threshold tables (Cisco/JunOS/EOS) | `read-only` |
| [network-topology-discovery](skills/network-topology-discovery/SKILL.md) | Network topology discovery via CDP/LLDP, ARP/MAC tables, and routing table analysis (Cisco/JunOS/EOS) | `read-only` |
| **Security Skills** | | |
| [palo-alto-firewall-audit](skills/palo-alto-firewall-audit/SKILL.md) | PAN-OS zone-based security policy audit — App-ID/Content-ID analysis, Security Profile Group validation, zone protection assessment | `read-only` |
| [fortigate-firewall-audit](skills/fortigate-firewall-audit/SKILL.md) | FortiGate/FortiOS policy audit — VDOM segmentation analysis, UTM profile binding validation, SD-WAN security assessment | `read-only` |
| [checkpoint-firewall-audit](skills/checkpoint-firewall-audit/SKILL.md) | Check Point R80+ security policy audit — rulebase layer analysis, blade activation audit, SmartConsole management validation | `read-only` |
| [cisco-firewall-audit](skills/cisco-firewall-audit/SKILL.md) | Cisco ASA/FTD dual-platform audit — ASA ACL/security-level analysis, FTD Access Control Policy and Snort IPS assessment | `read-only` |

> **Safety Tiers:** `read-only` skills only collect data and do not modify device state. `read-write` skills may change configuration or operational state. See [CONTRIBUTING.md](CONTRIBUTING.md) for details.

## Usage

Once installed, an agent loads a skill by name and follows its procedure. Here's how a typical interaction looks:

```
User: The core router is showing high CPU. Can you triage it?

Agent: Loading skill: example-device-health

I'll follow the Cisco IOS-XE Device Health Check procedure.

Step 1: Establish Baseline Context
Running: show version | include uptime|Version|bytes of memory

  hostname: core-rtr-01
  software: IOS-XE 17.6.3
  uptime: 47 days, 3 hours

Step 2: CPU Utilization Assessment
Running: show processes cpu sorted | head 20

  5-second: 92% ← CRITICAL (threshold: >90%)
  1-minute: 78% ← WARNING
  5-minute: 71% ← CRITICAL (threshold: >70%)
  Top process: BGP Router (54%)

Decision tree → CPU critical → Top process is BGP Router
→ Check for route churn, peer flap, table size

Step 5: Routing Table Health
Running: show ip bgp summary

  Neighbor 10.0.0.2: 847 state changes in last hour ← CRITICAL

Finding: BGP peer 10.0.0.2 is flapping, causing route churn
and sustained high CPU from BGP table recalculation.

Recommendation: Stabilize BGP peer 10.0.0.2 — check interface
to that neighbor for L1 errors, apply dampening if appropriate.
```

The agent follows the skill's procedure step by step, references threshold tables for classification, uses decision trees for triage logic, and produces a structured report.

## Repository Structure

```
skills/
  example-device-health/
    SKILL.md              # Skill definition (procedure, thresholds, decision trees)
    references/           # Supporting reference material
      threshold-tables.md
      cli-reference.md
scripts/
  validate.sh             # Custom convention validator
.github/
  workflows/
    validate.yml           # CI pipeline — runs on push to main and PRs
```

## Validation

Every skill is validated at two layers:

1. **Spec validation** — `agentskills validate` checks compliance with the Agent Skills SKILL.md specification (frontmatter schema, required fields).
2. **Convention validation** — `scripts/validate.sh` checks network-security-specific conventions (safety tier metadata, required body sections, `references/` directory).

To run both locally:

```bash
pip install skills-ref==0.1.1
agentskills validate skills/
bash scripts/validate.sh
```

CI runs both checks automatically on every push to `main` and on pull requests.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for the complete guide on writing skills, format reference, and submission process.

## License

[Apache-2.0](LICENSE)
