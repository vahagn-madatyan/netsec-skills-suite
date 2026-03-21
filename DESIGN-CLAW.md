# DESIGN-CLAW.md — Multi-Platform Distribution & NemoNet Integration

> **netsec-skills-suite → skills.sh + ClawHub + OpenClaw + NemoNet**
>
> This document defines how `netsec-skills-suite` serves as the single source of truth
> for 34+ network security skills, consumed by multiple platforms and deployment targets —
> from standalone `npx skills add` to sandboxed NemoNet deployments on NVIDIA Brev.

---

## Table of Contents

1. [Context & Vision](#1-context--vision)
2. [Architecture Overview](#2-architecture-overview)
3. [What NemoNet Is](#3-what-nemonet-is)
4. [Skill Consumption Strategy](#4-skill-consumption-strategy)
5. [Required Changes to netsec-skills-suite](#5-required-changes-to-netsec-skills-suite)
6. [Install Script (Multi-Platform)](#6-install-script-multi-platform)
7. [NemoNet Repo Integration](#7-nemonet-repo-integration)
8. [Deployment Targets](#8-deployment-targets)
9. [MCP Server Coordination](#9-mcp-server-coordination)
10. [ClawHub Publication](#10-clawhub-publication)
11. [Security Considerations](#11-security-considerations)
12. [Submodule Setup & Documentation](#12-submodule-setup--documentation)
13. [Naming Decision](#13-naming-decision)
14. [Repo Hygiene](#14-repo-hygiene)
15. [Implementation Checklist](#15-implementation-checklist)
16. [Verification](#16-verification)

---

## 1. Context & Vision

`netsec-skills-suite` is a curated collection of 34+ AI agent skills for network
and security operations. Each skill is a structured SKILL.md procedure covering
device triage, firewall auditing, protocol analysis, compliance assessment, and
incident response across Cisco, Juniper, Arista, Palo Alto, Fortinet, Check Point,
and multi-cloud environments.

The SKILL.md format is already cross-platform (Claude Code, OpenClaw, Cursor,
Codex, Copilot, Gemini CLI, Windsurf — 26+ platforms). The goal is to make this
repo consumable by **every platform** without duplicating content:

1. **skills.sh** — already works (`npx skills add vahagn-madatyan/netsec-skills-suite`)
2. **OpenClaw** — via `metadata.openclaw` in SKILL.md + ClawHub publishing
3. **NemoNet** (fork of NemoClaw) — via git submodule with sandbox deployment
4. **ClawHub** — via `clawhub sync --all` CLI
5. **Any consumer project** — via git submodule at `skills/netsec-skills-suite/`

**NemoNet** is a thin fork of NVIDIA's NemoClaw that bundles these skills alongside
network-specific MCP servers, custom egress policies, and inference routing into a
single deployable package — a sandboxed network automation agent platform.

This repo (`netsec-skills-suite`) remains the **single source of truth** for all
skills. NemoNet consumes them — it does not duplicate them.

---

## 2. Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                    NVIDIA Brev Launchable                       │
│                    (or AWS EC2 / DGX Spark)                     │
├─────────────────────────────────────────────────────────────────┤
│  NemoNet (forked NemoClaw)                                      │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │  OpenShell Sandbox (Landlock + seccomp + netns)           │  │
│  │  ┌─────────────────────────────────────────────────────┐  │  │
│  │  │  OpenClaw Agent Runtime                             │  │  │
│  │  │  ┌───────────────┐  ┌────────────────────────────┐  │  │  │
│  │  │  │ Agentic Loop  │  │ Memory Layer               │  │  │  │
│  │  │  │ Context →     │  │ AGENTS.md / SOUL.md        │  │  │  │
│  │  │  │ Inference →   │  │ MEMORY.md / HEARTBEAT.md   │  │  │  │
│  │  │  │ Tool Exec →   │  │                            │  │  │  │
│  │  │  │ Persist       │  │                            │  │  │  │
│  │  │  └───────┬───────┘  └────────────────────────────┘  │  │  │
│  │  │          │                                          │  │  │
│  │  │          ▼                                          │  │  │
│  │  │  ┌─────────────────────────────────────────────┐    │  │  │
│  │  │  │ netsec-skills-suite (THIS REPO)             │    │  │  │
│  │  │  │ ├── cisco-device-health/SKILL.md            │    │  │  │
│  │  │  │ ├── palo-alto-firewall-audit/SKILL.md       │    │  │  │
│  │  │  │ ├── aws-networking-audit/SKILL.md           │    │  │  │
│  │  │  │ ├── bgp-analysis/SKILL.md                   │    │  │  │
│  │  │  │ ├── zero-trust-assessment/SKILL.md          │    │  │  │
│  │  │  │ └── ... (34+ skills)                        │    │  │  │
│  │  │  └──────────────────┬──────────────────────────┘    │  │  │
│  │  │                     │ tool calls                    │  │  │
│  │  │                     ▼                               │  │  │
│  │  │  ┌─────────────────────────────────────────────┐    │  │  │
│  │  │  │ MCP Servers (separate repo or embedded)     │    │  │  │
│  │  │  │ ├── juniper-mist-mcp                        │    │  │  │
│  │  │  │ ├── palo-alto-mcp                           │    │  │  │
│  │  │  │ ├── aws-network-mcp                         │    │  │  │
│  │  │  │ ├── cno-mcp                                 │    │  │  │
│  │  │  │ └── meraki-mcp                              │    │  │  │
│  │  │  └──────────────────┬──────────────────────────┘    │  │  │
│  │  └─────────────────────┼───────────────────────────────┘  │  │
│  │                        │ egress (policy-controlled)       │  │
│  │  ┌─────────────────────▼───────────────────────────────┐  │  │
│  │  │  Egress Policy Engine (network-ops-sandbox.yaml)    │  │  │
│  │  │  ├── api.mist.com:443           allowed             │  │  │
│  │  │  ├── panorama.mcd-net.com:443   allowed             │  │  │
│  │  │  ├── *.amazonaws.com:443        allowed             │  │  │
│  │  │  └── unknown-host.com           blocked → TUI       │  │  │
│  │  └─────────────────────────────────────────────────────┘  │  │
│  └───────────────────────────────────────────────────────────┘  │
│                                                                 │
│  Inference: Nemotron 120B (NVIDIA Cloud) / Claude Opus / NIM   │
└─────────────────────────────────────────────────────────────────┘
         │                          │                    │
         ▼                          ▼                    ▼
   Juniper Mist Cloud      Palo Alto Panorama       AWS Networking
   (14K sites, 140K APs)   (15K+ firewalls)         (VPCs, TGW, R53)
```

**Standalone consumption (no NemoNet):**

```
netsec-skills-suite (canonical repo)
├── skills/*/SKILL.md          ← single source of truth (Agent Skills + OpenClaw metadata)
├── manifest.json              ← profiles, MCP deps, egress endpoints
├── install.sh                 ← multi-platform installer (symlinks)
├── scripts/validate.sh        ← convention validator
├── scripts/nemonet-install.sh ← profile-aware NemoNet installer
└── docs/SUBMODULE.md          ← consumer integration guide

Consumption paths:
┌─────────────────────────────────────────────────────────────────────┐
│ 1. npx skills add vahagn-madatyan/netsec-skills-suite              │ → skills.sh
│ 2. clawhub sync --all                                              │ → ClawHub
│ 3. git submodule add ... skills/netsec-skills-suite                │ → NemoNet/forks
│ 4. git clone + ./install.sh                                        │ → direct install
│ 5. OpenClaw skills.load.extraDirs → submodule path                 │ → OpenClaw native
└─────────────────────────────────────────────────────────────────────┘
```

---

## 3. What NemoNet Is

NemoNet is a **thin fork** of [NVIDIA NemoClaw](https://github.com/NVIDIA/NemoClaw)
(Apache 2.0) — the open-source stack that sandboxes
[OpenClaw](https://openclaw.ai) agents inside the
[NVIDIA OpenShell](https://github.com/NVIDIA/OpenShell) runtime.

NemoClaw provides:

- **Sandbox isolation** — Landlock LSM, seccomp filters, network namespace
- **Inference routing** — all LLM calls intercepted by OpenShell gateway
- **Declarative egress policy** — YAML-defined network allow/deny rules
- **Blueprint lifecycle** — versioned artifacts for reproducible sandbox setup
- **Single CLI** — `nemoclaw` orchestrates gateway, sandbox, inference, and policy

NemoNet extends this with:

- **Network-specific blueprint** — pre-configured egress for Mist, Panorama, AWS, CNO
- **Pre-loaded skills** — this repo (`netsec-skills-suite`) installed at build time
- **MCP servers** — vendor API integrations bundled in the container image
- **Deployment profiles** — `mcd-production`, `mcd-staging`, `lab`, `launchable-demo`
- **NVIDIA Brev Launchable** — one-click deploy to GPU cloud

### NemoNet Repo Structure

```
nemonet/
├── nemoclaw/                         # git subtree from NVIDIA/NemoClaw upstream
│   ├── nemoclaw/                     # TypeScript CLI plugin (untouched)
│   ├── nemoclaw-blueprint/           # Original blueprint (reference only)
│   └── ...
│
├── nemonet-blueprint/                # Custom network blueprint
│   ├── blueprint.yaml                # Profiles: mcd-prod, launchable-demo, lab
│   ├── orchestrator/
│   │   └── runner.py                 # Extended: vendor API health checks
│   └── policies/
│       ├── network-ops-sandbox.yaml  # Base egress policy
│       ├── mcd-production.yaml       # McDonald's strict profile
│       ├── mcd-govcloud.yaml         # GovCloud + FIPS endpoints
│       └── lab.yaml                  # Permissive for development
│
├── skills/                           # git submodule → netsec-skills-suite
│   └── netsec-skills-suite/          # THIS REPO (pinned version)
│
├── mcp-servers/                      # Network MCP tool servers
│   ├── juniper-mist-mcp/
│   ├── palo-alto-mcp/
│   ├── aws-network-mcp/
│   ├── cno-mcp/
│   ├── meraki-mcp/
│   └── git-netops-mcp/
│
├── docker/
│   ├── Dockerfile.sandbox            # OpenShell + MCP + skills
│   ├── Dockerfile.govcloud           # FIPS variant
│   └── docker-compose.yaml           # Brev Launchable stack
│
├── launchable/                       # NVIDIA Brev Launchable config
│   ├── setup.sh                      # VM boot script
│   ├── docker-compose.yaml           # Compose stack for Container Mode
│   └── README.md                     # Launch badge + instructions
│
├── install.sh
├── package.json
├── pyproject.toml
└── README.md
```

---

## 4. Skill Consumption Strategy

The skills in this repo are consumed through **five parallel paths**.
All draw from this single source of truth — no duplication.

### Path 1: Git Submodule (Production — Pinned Versions)

The NemoNet repo references `netsec-skills-suite` as a git submodule. This gives
deterministic, auditable builds for production deployments.

```bash
# In the NemoNet repo (one-time setup)
git submodule add https://github.com/vahagn-madatyan/netsec-skills-suite.git \
    skills/netsec-skills-suite

# To update to latest
git submodule update --remote skills/netsec-skills-suite
git add skills/netsec-skills-suite
git commit -m "chore: update netsec-skills-suite to latest"
```

In `Dockerfile.sandbox`:

```dockerfile
# Copy skills from submodule (pinned at build time)
COPY skills/netsec-skills-suite/skills/ /sandbox/skills/
```

**Pros:** Version pinned, reproducible, auditable, works in air-gapped builds.
**Use:** Production, GovCloud, any regulated deployment.

### Path 2: Git Clone in Setup Script (Demo — Always Latest)

The Launchable setup script or `nemonet onboard` clones the latest `main`
from this repo at deploy time.

```bash
# In launchable/setup.sh or nemonet onboard hook
git clone --depth 1 https://github.com/vahagn-madatyan/netsec-skills-suite.git \
    /tmp/netsec-skills
bash /tmp/netsec-skills/scripts/nemonet-install.sh /sandbox/skills/
rm -rf /tmp/netsec-skills
```

**Pros:** Always latest, no submodule management, simple.
**Use:** Demos, labs, evaluation Launchables.

### Path 3: Direct Install via npx (Standalone — No NemoNet)

The existing install command works outside NemoNet for users who just want the
skills in their own agent setup:

```bash
npx skills add vahagn-madatyan/netsec-skills-suite
```

**Pros:** Works anywhere, no NemoNet dependency.
**Use:** Individual engineers, non-NemoNet users, any of the 26+ supported platforms.

### Path 4: ClawHub Install (OpenClaw Users)

```bash
clawhub install netsec-skills-suite
```

**Pros:** Native OpenClaw discovery, version tracking, community visibility.
**Use:** OpenClaw community, ClawHub discovery.

### Path 5: OpenClaw extraDirs (Zero-Symlink)

Configure OpenClaw to discover skills directly from the submodule path:

```json5
{
  skills: {
    load: {
      extraDirs: ["./skills/netsec-skills-suite/skills"],
      watch: true
    }
  }
}
```

**Pros:** No symlinking, no install step, live-reloads on git pull.
**Use:** Development, OpenClaw-native projects.

---

## 5. Required Changes to netsec-skills-suite

All changes are additive — backward compatibility with the existing `agent-skills`
spec and `npx skills add` workflow is fully preserved.

### 5.1 Add OpenClaw-Native Frontmatter to Each SKILL.md

OpenClaw's skill router requires specific metadata for auto-discovery and
eligibility filtering. Add a `metadata.openclaw` block to each skill.

**Before (current):**

```yaml
---
name: palo-alto-firewall-audit
description: PAN-OS zone-based security policy audit
license: Apache-2.0
metadata:
  safety: read-only
  author: network-security-skills-suite
  version: "1.0.0"
---
```

**After (with OpenClaw metadata):**

```yaml
---
name: palo-alto-firewall-audit
description: PAN-OS zone-based security policy audit
license: Apache-2.0
metadata:
  safety: read-only
  author: network-security-skills-suite
  version: "1.0.0"
  openclaw: '{"emoji":"🛡️","safetyTier":"read-only","requires":{"bins":[],"env":["PAN_API_KEY"]},"tags":["palo-alto","firewall","audit","security"],"mcpDependencies":["palo-alto-mcp"],"egressEndpoints":["*.paloaltonetworks.com:443"]}'
---
```

The `metadata.openclaw` JSON fields serve these purposes:

| Field              | Purpose                                                       |
|--------------------|---------------------------------------------------------------|
| `emoji`            | Displayed in OpenClaw skill listings and TUI                  |
| `safetyTier`       | Maps to NemoNet sandbox permissions (read-only vs read-write) |
| `requires.bins`    | Binary dependencies the sandbox needs installed               |
| `requires.env`     | Environment variables the skill expects (API keys, etc.)      |
| `tags`             | Used by skill router for intent matching                      |
| `mcpDependencies`  | Which MCP servers this skill calls (NemoNet-specific)         |
| `egressEndpoints`  | Network endpoints this skill needs access to (NemoNet policy) |

**Category templates:**

| Category | emoji | bins | env | tags |
|----------|-------|------|-----|------|
| Device health/routing | `🔍` | `["ssh"]` | `[]` | `["cisco","health","triage"]` etc. |
| Firewall audit | `🛡️` | `[]` | vendor API key | `["firewall","audit","security"]` |
| Cloud audit | `☁️` | `["aws"]`/`["az"]`/`["gcloud"]` | cloud creds | `["cloud","audit"]` |
| Compliance/assessment | `📋` | `["ssh"]` | `[]` | `["compliance","audit"]` |
| Incident response | `🚨` | `["ssh"]` | `[]` | `["incident","forensics"]` |
| Observability | `📊` | `[]` | `[]` | `["monitoring","observability"]` |

**Validation:** The `agentskills validate` parser calls `str(v)` on each metadata
value. A JSON string passes through unchanged. `scripts/validate.sh` only checks
`metadata.safety` and ignores unknown keys. Test on one skill first to confirm.

### 5.2 Add MCP Tool References to Skill Bodies

Skills that interact with vendor APIs should declare which MCP tools they use.
This enables dual-mode operation: MCP-native (inside NemoNet sandbox) and
CLI-fallback (standalone SSH access).

Add a `## Tool Requirements` section to each relevant skill body:

```markdown
## Tool Requirements

**MCP Mode (NemoNet/OpenClaw):**
This skill uses the following MCP tools when available:
- `palo-alto-mcp.get_security_rules` — Pull active rulebase from Panorama
- `palo-alto-mcp.get_security_profiles` — Audit Security Profile Groups
- `palo-alto-mcp.get_zone_protection` — Zone protection profile settings
- `palo-alto-mcp.get_nat_rules` — NAT policy for exposure analysis

**CLI Fallback Mode:**
If MCP tools are unavailable, use `exec` tool with SSH to the target device
and run PAN-OS operational/XML API commands directly.
```

**Skills requiring MCP references:**

| Skill                        | MCP Server Dependency   |
|------------------------------|-------------------------|
| `palo-alto-firewall-audit`   | `palo-alto-mcp`         |
| `cisco-firewall-audit`       | (SSH/CLI or cisco-mcp)  |
| `fortigate-firewall-audit`   | (SSH/CLI or forti-mcp)  |
| `checkpoint-firewall-audit`  | (SSH/CLI or cp-mcp)     |
| `aws-networking-audit`       | `aws-network-mcp`       |
| `azure-networking-audit`     | (az CLI or azure-mcp)   |
| `gcp-networking-audit`       | (gcloud or gcp-mcp)     |
| `cloud-security-posture`     | `aws-network-mcp` + others |
| `source-of-truth-audit`      | (Nautobot/NetBox API)   |
| `ipam-dns-audit`             | (IPAM API)              |
| `wireless-security-audit`    | `juniper-mist-mcp`      |
| `change-verification`        | `git-netops-mcp`        |
| `config-management`          | `git-netops-mcp`        |

Skills that are pure procedure/analysis (protocol analysis, compliance assessment)
with no vendor API dependency do not need MCP references.

### 5.3 Create `manifest.json` at Repo Root

This manifest enables NemoNet's setup scripts to auto-discover skills, resolve
MCP dependencies, and generate egress policy entries.

```json
{
  "name": "netsec-skills-suite",
  "version": "1.0.0",
  "description": "Network & Security Skills Suite",
  "repository": "https://github.com/vahagn-madatyan/netsec-skills-suite",
  "license": "Apache-2.0",
  "nemonet": {
    "minVersion": "0.1.0",
    "defaultProfile": "all"
  },
  "profiles": {
    "all": {
      "description": "Install all skills",
      "skills": "*"
    },
    "networking-only": {
      "description": "Device health, routing protocols, topology, interfaces",
      "skills": [
        "cisco-device-health",
        "juniper-device-health",
        "arista-device-health",
        "bgp-analysis",
        "ospf-analysis",
        "eigrp-analysis",
        "isis-analysis",
        "interface-health",
        "network-topology-discovery"
      ]
    },
    "security-only": {
      "description": "Firewall audits, compliance, vulnerability, incident response",
      "skills": [
        "palo-alto-firewall-audit",
        "fortigate-firewall-audit",
        "checkpoint-firewall-audit",
        "cisco-firewall-audit",
        "acl-rule-analysis",
        "cis-benchmark-audit",
        "nist-compliance-assessment",
        "vulnerability-assessment",
        "siem-log-analysis",
        "incident-response-network",
        "vpn-ipsec-troubleshooting",
        "zero-trust-assessment",
        "wireless-security-audit"
      ]
    },
    "cloud-only": {
      "description": "AWS, Azure, GCP networking and cloud security posture",
      "skills": [
        "aws-networking-audit",
        "azure-networking-audit",
        "gcp-networking-audit",
        "cloud-security-posture",
        "source-of-truth-audit",
        "ipam-dns-audit"
      ]
    },
    "mcd-production": {
      "description": "McDonald's production subset — Cisco, Juniper, PAN, AWS",
      "skills": [
        "cisco-device-health",
        "juniper-device-health",
        "bgp-analysis",
        "ospf-analysis",
        "interface-health",
        "network-topology-discovery",
        "palo-alto-firewall-audit",
        "acl-rule-analysis",
        "zero-trust-assessment",
        "aws-networking-audit",
        "change-verification",
        "config-management",
        "incident-response-network",
        "incident-response-lifecycle",
        "wireless-security-audit"
      ]
    }
  },
  "skills": [
    {
      "name": "example-device-health",
      "path": "skills/example-device-health",
      "safetyTier": "read-only",
      "mcpDependencies": [],
      "egressEndpoints": []
    },
    {
      "name": "cisco-device-health",
      "path": "skills/cisco-device-health",
      "safetyTier": "read-only",
      "mcpDependencies": [],
      "egressEndpoints": []
    },
    {
      "name": "juniper-device-health",
      "path": "skills/juniper-device-health",
      "safetyTier": "read-only",
      "mcpDependencies": [],
      "egressEndpoints": []
    },
    {
      "name": "arista-device-health",
      "path": "skills/arista-device-health",
      "safetyTier": "read-only",
      "mcpDependencies": [],
      "egressEndpoints": []
    },
    {
      "name": "bgp-analysis",
      "path": "skills/bgp-analysis",
      "safetyTier": "read-only",
      "mcpDependencies": [],
      "egressEndpoints": []
    },
    {
      "name": "ospf-analysis",
      "path": "skills/ospf-analysis",
      "safetyTier": "read-only",
      "mcpDependencies": [],
      "egressEndpoints": []
    },
    {
      "name": "eigrp-analysis",
      "path": "skills/eigrp-analysis",
      "safetyTier": "read-only",
      "mcpDependencies": [],
      "egressEndpoints": []
    },
    {
      "name": "isis-analysis",
      "path": "skills/isis-analysis",
      "safetyTier": "read-only",
      "mcpDependencies": [],
      "egressEndpoints": []
    },
    {
      "name": "interface-health",
      "path": "skills/interface-health",
      "safetyTier": "read-only",
      "mcpDependencies": [],
      "egressEndpoints": []
    },
    {
      "name": "network-topology-discovery",
      "path": "skills/network-topology-discovery",
      "safetyTier": "read-only",
      "mcpDependencies": [],
      "egressEndpoints": []
    },
    {
      "name": "change-verification",
      "path": "skills/change-verification",
      "safetyTier": "read-write",
      "mcpDependencies": ["git-netops-mcp"],
      "egressEndpoints": [],
      "requiresApproval": true
    },
    {
      "name": "config-management",
      "path": "skills/config-management",
      "safetyTier": "read-write",
      "mcpDependencies": ["git-netops-mcp"],
      "egressEndpoints": [],
      "requiresApproval": true
    },
    {
      "name": "palo-alto-firewall-audit",
      "path": "skills/palo-alto-firewall-audit",
      "safetyTier": "read-only",
      "mcpDependencies": ["palo-alto-mcp"],
      "egressEndpoints": ["*.paloaltonetworks.com:443"]
    },
    {
      "name": "fortigate-firewall-audit",
      "path": "skills/fortigate-firewall-audit",
      "safetyTier": "read-only",
      "mcpDependencies": [],
      "egressEndpoints": []
    },
    {
      "name": "checkpoint-firewall-audit",
      "path": "skills/checkpoint-firewall-audit",
      "safetyTier": "read-only",
      "mcpDependencies": [],
      "egressEndpoints": []
    },
    {
      "name": "cisco-firewall-audit",
      "path": "skills/cisco-firewall-audit",
      "safetyTier": "read-only",
      "mcpDependencies": [],
      "egressEndpoints": []
    },
    {
      "name": "acl-rule-analysis",
      "path": "skills/acl-rule-analysis",
      "safetyTier": "read-only",
      "mcpDependencies": [],
      "egressEndpoints": []
    },
    {
      "name": "cis-benchmark-audit",
      "path": "skills/cis-benchmark-audit",
      "safetyTier": "read-only",
      "mcpDependencies": [],
      "egressEndpoints": []
    },
    {
      "name": "nist-compliance-assessment",
      "path": "skills/nist-compliance-assessment",
      "safetyTier": "read-only",
      "mcpDependencies": [],
      "egressEndpoints": []
    },
    {
      "name": "vulnerability-assessment",
      "path": "skills/vulnerability-assessment",
      "safetyTier": "read-only",
      "mcpDependencies": [],
      "egressEndpoints": []
    },
    {
      "name": "siem-log-analysis",
      "path": "skills/siem-log-analysis",
      "safetyTier": "read-only",
      "mcpDependencies": [],
      "egressEndpoints": []
    },
    {
      "name": "incident-response-network",
      "path": "skills/incident-response-network",
      "safetyTier": "read-only",
      "mcpDependencies": [],
      "egressEndpoints": []
    },
    {
      "name": "vpn-ipsec-troubleshooting",
      "path": "skills/vpn-ipsec-troubleshooting",
      "safetyTier": "read-only",
      "mcpDependencies": [],
      "egressEndpoints": []
    },
    {
      "name": "zero-trust-assessment",
      "path": "skills/zero-trust-assessment",
      "safetyTier": "read-only",
      "mcpDependencies": [],
      "egressEndpoints": []
    },
    {
      "name": "wireless-security-audit",
      "path": "skills/wireless-security-audit",
      "safetyTier": "read-only",
      "mcpDependencies": ["juniper-mist-mcp"],
      "egressEndpoints": ["api.mist.com:443", "api.eu.mist.com:443"]
    },
    {
      "name": "aws-networking-audit",
      "path": "skills/aws-networking-audit",
      "safetyTier": "read-only",
      "mcpDependencies": ["aws-network-mcp"],
      "egressEndpoints": ["*.amazonaws.com:443"]
    },
    {
      "name": "azure-networking-audit",
      "path": "skills/azure-networking-audit",
      "safetyTier": "read-only",
      "mcpDependencies": [],
      "egressEndpoints": ["management.azure.com:443"]
    },
    {
      "name": "gcp-networking-audit",
      "path": "skills/gcp-networking-audit",
      "safetyTier": "read-only",
      "mcpDependencies": [],
      "egressEndpoints": ["compute.googleapis.com:443"]
    },
    {
      "name": "cloud-security-posture",
      "path": "skills/cloud-security-posture",
      "safetyTier": "read-only",
      "mcpDependencies": ["aws-network-mcp"],
      "egressEndpoints": ["*.amazonaws.com:443", "management.azure.com:443", "*.googleapis.com:443"]
    },
    {
      "name": "source-of-truth-audit",
      "path": "skills/source-of-truth-audit",
      "safetyTier": "read-only",
      "mcpDependencies": [],
      "egressEndpoints": []
    },
    {
      "name": "ipam-dns-audit",
      "path": "skills/ipam-dns-audit",
      "safetyTier": "read-only",
      "mcpDependencies": [],
      "egressEndpoints": []
    },
    {
      "name": "monitoring-dashboard-audit",
      "path": "skills/monitoring-dashboard-audit",
      "safetyTier": "read-only",
      "mcpDependencies": [],
      "egressEndpoints": []
    },
    {
      "name": "network-log-analysis",
      "path": "skills/network-log-analysis",
      "safetyTier": "read-only",
      "mcpDependencies": [],
      "egressEndpoints": []
    },
    {
      "name": "incident-response-lifecycle",
      "path": "skills/incident-response-lifecycle",
      "safetyTier": "read-only",
      "mcpDependencies": [],
      "egressEndpoints": []
    }
  ]
}
```

### 5.4 Create `scripts/nemonet-install.sh`

Profile-aware installer that NemoNet calls during onboard or Launchable setup.

```bash
#!/bin/bash
# scripts/nemonet-install.sh
# Installs netsec-skills-suite into a NemoNet sandbox or OpenClaw workspace.
#
# Usage:
#   ./scripts/nemonet-install.sh [target-dir] [profile]
#
# Arguments:
#   target-dir  Where to install skills (default: /sandbox/skills)
#   profile     Install profile from manifest.json (default: all)
#
# Examples:
#   ./scripts/nemonet-install.sh                           # all skills -> /sandbox/skills
#   ./scripts/nemonet-install.sh /sandbox/skills mcd-production
#   ./scripts/nemonet-install.sh ~/.openclaw/skills security-only

set -euo pipefail

TARGET="${1:-/sandbox/skills}"
PROFILE="${2:-all}"
REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
MANIFEST="${REPO_ROOT}/manifest.json"

echo "netsec-skills-suite installer"
echo "  Profile: ${PROFILE}"
echo "  Target:  ${TARGET}"
echo ""

mkdir -p "${TARGET}"

# If jq is available, use profile filtering
if command -v jq &>/dev/null && [ -f "$MANIFEST" ]; then
  if [ "$PROFILE" = "all" ]; then
    SKILL_DIRS=("${REPO_ROOT}/skills"/*)
  else
    SKILL_NAMES=$(jq -r \
      ".profiles[\"${PROFILE}\"].skills[]" \
      "$MANIFEST" 2>/dev/null) || {
      echo "[ERROR] Profile '${PROFILE}' not found in manifest.json"
      echo "Available profiles:"
      jq -r '.profiles | keys[]' "$MANIFEST"
      exit 1
    }
    SKILL_DIRS=()
    for name in $SKILL_NAMES; do
      SKILL_DIRS+=("${REPO_ROOT}/skills/${name}")
    done
  fi
else
  # Fallback: install all skills if jq unavailable
  echo "[WARN] jq not found — installing all skills"
  SKILL_DIRS=("${REPO_ROOT}/skills"/*)
fi

INSTALLED=0
SKIPPED=0

for skill_dir in "${SKILL_DIRS[@]}"; do
  if [ ! -d "$skill_dir" ]; then
    echo "  SKIP ${skill_dir} (not found)"
    ((SKIPPED++))
    continue
  fi

  skill_name=$(basename "$skill_dir")

  # Skip non-skill directories
  if [ ! -f "${skill_dir}/SKILL.md" ]; then
    continue
  fi

  cp -r "$skill_dir" "${TARGET}/${skill_name}"
  echo "  OK ${skill_name}"
  ((INSTALLED++))
done

echo ""
echo "Installed: ${INSTALLED} skills"
[ "$SKIPPED" -gt 0 ] && echo "Skipped:   ${SKIPPED}"
echo "Location:  ${TARGET}"
```

### 5.5 Create `scripts/generate-egress-policy.sh`

Reads `manifest.json` and generates a NemoNet-compatible egress policy YAML
fragment for all skills that declare `egressEndpoints`.

```bash
#!/bin/bash
# scripts/generate-egress-policy.sh
# Generates NemoNet egress policy YAML from manifest.json
#
# Usage: ./scripts/generate-egress-policy.sh [profile] > policy-fragment.yaml

set -euo pipefail

PROFILE="${1:-all}"
REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
MANIFEST="${REPO_ROOT}/manifest.json"

echo "# Auto-generated egress policy fragment"
echo "# Profile: ${PROFILE}"
echo "# Source: netsec-skills-suite/manifest.json"
echo "# Generated: $(date -u +%Y-%m-%dT%H:%M:%SZ)"
echo ""

jq -r '
  .skills[]
  | select(.egressEndpoints | length > 0)
  | "# Skill: \(.name) (safety: \(.safetyTier))\n" +
    (.egressEndpoints | map("  - \"\(.)\"") | join("\n"))
' "$MANIFEST"
```

---

## 6. Install Script (Multi-Platform)

Create `install.sh` at repo root for standalone (non-NemoNet) installations.

```bash
./install.sh                        # Auto-detect platforms, symlink skills
./install.sh --target claude        # ~/.claude/skills/<name>
./install.sh --target openclaw      # ~/.openclaw/workspace/skills/<name>
./install.sh --target agents        # ~/.agents/skills/<name> (cross-platform)
./install.sh --target project       # ./.agents/skills/<name> (project-local)
./install.sh --list                 # Show available skills
./install.sh --dry-run              # Preview what would happen
./install.sh --uninstall            # Remove symlinks created by this suite
```

Design:
- **Symlinks, not copies** — updates propagate automatically via `git pull` or submodule update
- **Individual skill symlinks** — each skill gets its own symlink (e.g., `~/.claude/skills/bgp-analysis -> /path/to/repo/skills/bgp-analysis/`)
- **Idempotent** — safe to run multiple times
- **Platform detection** — checks which agent directories exist (`~/.claude/`, `~/.openclaw/`, etc.)
- **Submodule-aware** — works when repo is mounted at `skills/netsec-skills-suite/` inside a consumer project

This is distinct from `scripts/nemonet-install.sh` which copies (not symlinks)
and supports profile filtering for sandbox/container deployments.

---

## 7. NemoNet Repo Integration

### 7.1 Submodule Setup (NemoNet repo)

```bash
cd nemonet/
git submodule add https://github.com/vahagn-madatyan/netsec-skills-suite.git \
    skills/netsec-skills-suite
git commit -m "feat: add netsec-skills-suite as submodule"
```

### 7.2 Dockerfile.sandbox

```dockerfile
FROM ghcr.io/nvidia/openshell-community/sandboxes/openclaw:latest

# --- Install MCP servers ---
COPY mcp-servers/ /opt/mcp-servers/
RUN cd /opt/mcp-servers/juniper-mist-mcp && npm install --production
RUN cd /opt/mcp-servers/palo-alto-mcp && npm install --production
RUN cd /opt/mcp-servers/aws-network-mcp && npm install --production

# --- Install skills from netsec-skills-suite submodule ---
COPY skills/netsec-skills-suite/skills/ /sandbox/skills/

# --- Copy network-specific workspace files ---
COPY workspace/AGENTS.md /sandbox/workspace/AGENTS.md
COPY workspace/SOUL.md /sandbox/workspace/SOUL.md
```

### 7.3 Launchable setup.sh

```bash
#!/bin/bash
set -euo pipefail

# Clone NemoNet (includes netsec-skills-suite submodule)
cd /home/ubuntu
git clone --recurse-submodules https://github.com/your-org/nemonet.git
cd nemonet

# Install NemoClaw CLI
npm install -g nemoclaw

# Run NemoNet onboard
nemonet onboard --profile launchable-demo --non-interactive

# Start services
docker compose -f docker/docker-compose.yaml up -d

echo "[NemoNet] Ready — access via Secure Links"
```

---

## 8. Deployment Targets

| Target                      | Use Case              | Skills Source                    | Inference          |
|-----------------------------|-----------------------|----------------------------------|--------------------|
| **NVIDIA Brev Launchable**  | Demos, evaluation     | `git clone` (latest HEAD)        | NVIDIA Cloud       |
| **AWS EC2 (production)**    | 24/7 ops              | Submodule (pinned version)       | Claude Opus/Sonnet |
| **DGX Spark**               | Air-gapped demos      | Baked into container image       | Local Nemotron NIM |
| **EKS / OpenShift**         | Multi-tenant SaaS     | Container image per release      | Mixed              |

---

## 9. MCP Server Coordination

Skills reference MCP servers by name in their `mcpDependencies`. The MCP servers
themselves live in the NemoNet repo (or their own repos).

| MCP Server             | Vendor API                       | Skills That Use It              |
|------------------------|----------------------------------|---------------------------------|
| `juniper-mist-mcp`    | api.mist.com                     | `wireless-security-audit`       |
| `palo-alto-mcp`       | Panorama REST/XML API            | `palo-alto-firewall-audit`      |
| `aws-network-mcp`     | AWS SDK (Boto3)                  | `aws-networking-audit`, `cloud-security-posture` |
| `cno-mcp`             | CNO Platform API                 | (future skills)                 |
| `meraki-mcp`          | Meraki Dashboard API             | (future skills)                 |
| `git-netops-mcp`      | Git + GitHub/GitLab API          | `change-verification`, `config-management` |

Skills without MCP dependencies operate in CLI-fallback mode using SSH/exec.

---

## 10. ClawHub Publication

For broader community adoption, publish skills to ClawHub — the OpenClaw skill registry.

### Via CLI (preferred)

```bash
clawhub login                       # Authenticate via GitHub
clawhub sync --all                  # Batch-publish all 34 skills
```

Each skill gets its own ClawHub page with version tracking, making all 34 skills
discoverable to the OpenClaw user base.

### Via PR (alternative)

1. Fork `openclaw/clawhub`
2. Add each skill as a folder under the appropriate category
3. Ensure each SKILL.md has the `metadata.openclaw` frontmatter
4. Open a pull request

### CI Integration (optional)

Add a step to `.github/workflows/validate.yml` that runs `clawhub` validation
if the CLI is available.

**For enterprise deployments**, use the submodule path rather than ClawHub to
avoid supply chain risks.

---

## 11. Security Considerations

### Existing Security Pipeline (Preserved)

This repo already runs a multi-layer security pipeline that carries forward:

- **SkillCheck security audit** — scans for command injection, prompt injection,
  safety tier mismatches, credential harvesting, obfuscation
- **VirusTotal scan** — 70+ antivirus engines on every PR and release
- **OpenSSF Scorecard** — weekly repository security posture evaluation
- **Claude Code Review** — AI-powered review on pull requests

### NemoNet-Specific Security

- **Sandbox isolation** — skills execute inside OpenShell sandbox with Landlock,
  seccomp, and network namespace isolation
- **Egress policy** — skills can only reach endpoints declared in their
  `egressEndpoints` manifest entry. All other traffic is blocked.
- **Safety tier enforcement** — `read-write` skills (`change-verification`,
  `config-management`) require explicit operator approval in the OpenShell TUI
  before executing write operations
- **No public ClawHub dependency** — production deployments use the submodule
  path, avoiding exposure to supply chain attacks on the public registry

---

## 12. Submodule Setup & Documentation

### 12.1 Tag first release
- `git tag v1.0.0` — enables version pinning for submodule consumers

### 12.2 Create `docs/SUBMODULE.md`
Document how consumer projects consume this repo:

```bash
# Add as submodule (consumer project)
git submodule add https://github.com/vahagn-madatyan/netsec-skills-suite.git skills/netsec-skills-suite

# Initialize after clone
git submodule update --init

# Update to latest
cd skills/netsec-skills-suite && git pull origin main && cd ../..
git add skills/netsec-skills-suite && git commit -m "bump netsec-skills"

# Pin to specific version
cd skills/netsec-skills-suite && git checkout v1.0.0 && cd ../..

# Install skills into agent platforms
./skills/netsec-skills-suite/install.sh --target openclaw
```

---

## 13. Naming Decision

The NemoClaw fork is named **NemoNet** (working title). Candidates:

| Name          | Signal                                         | CLI Feel             |
|---------------|------------------------------------------------|----------------------|
| **NemoNet**   | NemoClaw + networking. Clean, obvious.          | `nemonet deploy`     |
| **NemoWire**  | NemoClaw + wire/infrastructure. Physical feel.  | `nemowire onboard`   |
| **InfraClaw** | Infrastructure + OpenClaw. Domain-first.        | `infraclaw connect`  |
| **NemoGrid**  | NemoClaw + grid/topology. Multi-site feel.      | `nemogrid status`    |
| **NemoLink**  | NemoClaw + network link. Simple.                | `nemolink deploy`    |
| **ClawOps**   | OpenClaw + NetOps. Punchy, product-like.        | `clawops policy set` |
| **NemoEdge**  | NemoClaw + edge networking. DGX Spark aligned.  | `nemoedge connect`   |

---

## 14. Repo Hygiene

- [ ] **Remove stray files from root:** Move `compass_artifact_wf-*.md` to
  `docs/research/`. These could confuse OpenClaw's skill loader if it scans
  for `.md` files at root.
- [ ] **Add `.gitattributes`** for consistent line endings across contributors.
- [ ] **Tag a release** — create `v1.0.0` to enable version pinning in git
  submodules and `npx skills add` version locks.
- [ ] **Verify `.env`** is properly gitignored and not committed with secrets.

---

## 15. Implementation Checklist

### Phase 1 — Skill Compatibility (this repo)

- [ ] Test `metadata.openclaw` on one skill, validate with `agentskills validate`
- [ ] Add `metadata.openclaw` frontmatter to all 34 SKILL.md files
- [ ] Add `## Tool Requirements` section to vendor-API-dependent skills (13 skills)
- [ ] Create `manifest.json` at repo root
- [ ] Create `scripts/nemonet-install.sh`
- [ ] Create `scripts/generate-egress-policy.sh`
- [ ] Create `install.sh` (multi-platform symlinker)
- [ ] Remove `compass_artifact_wf-*.md` files from root (move to `docs/research/`)
- [ ] Add `.gitattributes`
- [ ] Run both validators: `agentskills validate skills/` + `bash scripts/validate.sh`

### Phase 2 — Documentation & Release (this repo)

- [ ] Create `docs/SUBMODULE.md`
- [ ] Update README.md with multi-platform install section
- [ ] Update CONTRIBUTING.md with openclaw metadata + ClawHub docs
- [ ] Tag `v1.0.0` release
- [ ] Update CI to validate `manifest.json` schema

### Phase 3 — ClawHub & Community

- [ ] `clawhub login` + `clawhub sync --all` to publish all skills
- [ ] Verify skills appear on ClawHub
- [ ] Post announcement to OpenClaw Discord

### Phase 4 — NemoNet Repo Setup (separate repo)

- [ ] Fork NVIDIA/NemoClaw → your-org/nemonet
- [ ] Add `netsec-skills-suite` as git submodule
- [ ] Create `nemonet-blueprint/` with network-specific policies
- [ ] Build custom sandbox Docker image with skills + MCP servers
- [ ] Create `launchable/` directory with Brev config
- [ ] Publish Launchable to NVIDIA Brev Explore catalog
- [ ] Add launch badge to README

---

## 16. Verification

1. **skills.sh**: `npx skills add vahagn-madatyan/netsec-skills-suite --list` — all 34 skills appear
2. **Validation**: `agentskills validate skills/` and `bash scripts/validate.sh` both pass
3. **ClawHub**: `clawhub sync --all` publishes successfully; skills appear on ClawHub
4. **Submodule**: In a test project, `git submodule add` + `./install.sh --target claude` creates working symlinks
5. **OpenClaw**: Skills with `metadata.openclaw` are discoverable by OpenClaw's skill loader
6. **NemoNet**: `scripts/nemonet-install.sh /tmp/test mcd-production` installs correct subset
7. **Egress**: `scripts/generate-egress-policy.sh` produces valid YAML fragment

---

## Files to Create/Modify

| File | Action | Purpose |
|------|--------|---------|
| `skills/*/SKILL.md` (x34) | Modify | Add `metadata.openclaw` field |
| `skills/*/SKILL.md` (x13) | Modify | Add `## Tool Requirements` section |
| `manifest.json` | Create | Profiles, MCP deps, egress endpoints |
| `install.sh` | Create | Multi-platform symlink installer |
| `scripts/nemonet-install.sh` | Create | Profile-aware NemoNet installer |
| `scripts/generate-egress-policy.sh` | Create | Egress policy YAML generator |
| `docs/SUBMODULE.md` | Create | Submodule consumption guide |
| `docs/research/` | Create (move) | Move compass artifacts here |
| `.gitattributes` | Create | Consistent line endings |
| `README.md` | Modify | Multi-platform install instructions |
| `CONTRIBUTING.md` | Modify | OpenClaw metadata + ClawHub docs |

---

*Last updated: 2026-03-21*
*License: Apache-2.0*
