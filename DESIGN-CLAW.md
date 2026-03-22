# DESIGN-CLAW.md — Multi-Platform Distribution Design

> **netsec-skills-suite → skills.sh + ClawHub + OpenClaw + Submodule**
>
> This document defines how `netsec-skills-suite` serves as the single source of truth
> for 34+ network security skills, consumed by multiple platforms and deployment targets —
> from standalone `npx skills add` to submodule integration in consumer projects.
>
> NemoNet-specific integration (sandbox, Dockerfile, Launchable, MCP servers, egress
> policies) is tracked in the [NemoNet repo](https://github.com/vahagn-madatyan/NemoNet).

---

## Table of Contents

1. [Context & Vision](#1-context--vision)
2. [Architecture Overview](#2-architecture-overview)
3. [Skill Consumption Strategy](#3-skill-consumption-strategy)
4. [Required Changes to netsec-skills-suite](#4-required-changes-to-netsec-skills-suite)
5. [ClawHub Publication](#5-clawhub-publication)
6. [Security Considerations](#6-security-considerations)
7. [Submodule Setup & Documentation](#7-submodule-setup--documentation)
8. [Repo Hygiene](#8-repo-hygiene)
9. [Implementation Checklist](#9-implementation-checklist)
10. [Verification](#10-verification)

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
3. **NemoNet** (fork of NemoClaw) — via git submodule with sandbox deployment (see [NemoNet repo](https://github.com/vahagn-madatyan/NemoNet))
4. **ClawHub** — via `clawhub sync --all` CLI
5. **Any consumer project** — via git submodule at `skills/netsec-skills-suite/`

This repo (`netsec-skills-suite`) remains the **single source of truth** for all
skills. Consumer projects consume them — they do not duplicate them.

---

## 2. Architecture Overview

```
netsec-skills-suite (canonical repo)
├── skills/*/SKILL.md          ← single source of truth (Agent Skills + OpenClaw metadata)
├── manifest.json              ← profiles, MCP deps, egress endpoints
├── scripts/validate.sh        ← convention validator
└── docs/SUBMODULE.md          ← consumer integration guide

Consumption paths:
┌─────────────────────────────────────────────────────────────────────┐
│ 1. npx skills add vahagn-madatyan/netsec-skills-suite              │ → skills.sh
│ 2. clawhub sync --all                                              │ → ClawHub
│ 3. git submodule add ... skills/netsec-skills-suite                │ → NemoNet/forks
│ 4. git clone + submodule                                           │ → direct install
│ 5. OpenClaw skills.load.extraDirs → submodule path                 │ → OpenClaw native
└─────────────────────────────────────────────────────────────────────┘
```

---

## 3. Skill Consumption Strategy

The skills in this repo are consumed through **five parallel paths**.
All draw from this single source of truth — no duplication.

### Path 1: Git Submodule (Pinned Versions)

Consumer projects reference `netsec-skills-suite` as a git submodule. This gives
deterministic, auditable builds.

```bash
# In a consumer repo (one-time setup)
git submodule add https://github.com/vahagn-madatyan/netsec-skills-suite.git \
    skills/netsec-skills-suite

# To update to latest
git submodule update --remote skills/netsec-skills-suite
git add skills/netsec-skills-suite
git commit -m "chore: update netsec-skills-suite to latest"
```

**Pros:** Version pinned, reproducible, auditable, works in air-gapped builds.
**Use:** Production, any regulated deployment, NemoNet (see [NemoNet repo](https://github.com/vahagn-madatyan/NemoNet)).

### Path 2: Git Clone (Always Latest)

Clone the latest `main` from this repo at deploy time.

```bash
git clone --depth 1 https://github.com/vahagn-madatyan/netsec-skills-suite.git \
    /tmp/netsec-skills
```

**Pros:** Always latest, no submodule management, simple.
**Use:** Demos, labs, evaluation.

### Path 3: Direct Install via npx (Standalone)

The existing install command works for users who just want the
skills in their own agent setup:

```bash
npx skills add vahagn-madatyan/netsec-skills-suite
```

**Pros:** Works anywhere, no NemoNet dependency.
**Use:** Individual engineers, any of the 26+ supported platforms.

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

## 4. Required Changes to netsec-skills-suite

All changes are additive — backward compatibility with the existing `agent-skills`
spec and `npx skills add` workflow is fully preserved.

### 4.1 Add OpenClaw-Native Frontmatter to Each SKILL.md

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
| `safetyTier`       | Maps to sandbox permissions (read-only vs read-write)         |
| `requires.bins`    | Binary dependencies the sandbox needs installed               |
| `requires.env`     | Environment variables the skill expects (API keys, etc.)      |
| `tags`             | Used by skill router for intent matching                      |
| `mcpDependencies`  | Which MCP servers this skill calls                            |
| `egressEndpoints`  | Network endpoints this skill needs access to                  |

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

### 4.2 Add MCP Tool References to Skill Bodies

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

### 4.3 Create `manifest.json` at Repo Root

This manifest enables setup scripts to auto-discover skills, resolve
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

---

## 5. ClawHub Publication

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

## 6. Security Considerations

### Existing Security Pipeline (Preserved)

This repo already runs a multi-layer security pipeline that carries forward:

- **SkillCheck security audit** — scans for command injection, prompt injection,
  safety tier mismatches, credential harvesting, obfuscation
- **VirusTotal scan** — 70+ antivirus engines on every PR and release
- **OpenSSF Scorecard** — weekly repository security posture evaluation
- **Claude Code Review** — AI-powered review on pull requests

> For NemoNet-specific security (sandbox isolation, egress policy, safety tier
> enforcement), see [NemoNet repo](https://github.com/vahagn-madatyan/NemoNet).

---

## 7. Submodule Setup & Documentation

### 7.1 Tag first release
- `git tag v1.0.0` — enables version pinning for submodule consumers

### 7.2 Create `docs/SUBMODULE.md`
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
```

---

## 8. Repo Hygiene

- [ ] **Remove stray files from root:** Move `compass_artifact_wf-*.md` to
  `docs/research/`. These could confuse OpenClaw's skill loader if it scans
  for `.md` files at root.
- [ ] **Add `.gitattributes`** for consistent line endings across contributors.
- [ ] **Tag a release** — create `v1.0.0` to enable version pinning in git
  submodules and `npx skills add` version locks.
- [ ] **Verify `.env`** is properly gitignored and not committed with secrets.

---

## 9. Implementation Checklist

### Phase 1 — Skill Compatibility (this repo)

- [ ] Test `metadata.openclaw` on one skill, validate with `agentskills validate`
- [ ] Add `metadata.openclaw` frontmatter to all 34 SKILL.md files
- [ ] Add `## Tool Requirements` section to vendor-API-dependent skills (13 skills)
- [ ] Create `manifest.json` at repo root
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

> **Phase 4 (NemoNet Repo Setup)** has been moved to [NemoNet repo](https://github.com/vahagn-madatyan/NemoNet).

---

## 10. Verification

1. **skills.sh**: `npx skills add vahagn-madatyan/netsec-skills-suite --list` — all 34 skills appear
2. **Validation**: `agentskills validate skills/` and `bash scripts/validate.sh` both pass
3. **ClawHub**: `clawhub sync --all` publishes successfully; skills appear on ClawHub
4. **Submodule**: In a test project, `git submodule add` creates working integration
5. **OpenClaw**: Skills with `metadata.openclaw` are discoverable by OpenClaw's skill loader

> For NemoNet-specific verification (nemonet-install.sh, egress policy generation),
> see [NemoNet repo](https://github.com/vahagn-madatyan/NemoNet).

---

## Files to Create/Modify

| File | Action | Purpose |
|------|--------|---------|
| `skills/*/SKILL.md` (x34) | Modify | Add `metadata.openclaw` field |
| `skills/*/SKILL.md` (x13) | Modify | Add `## Tool Requirements` section |
| `manifest.json` | Create | Profiles, MCP deps, egress endpoints |
| `docs/SUBMODULE.md` | Create | Submodule consumption guide |
| `docs/research/` | Create (move) | Move compass artifacts here |
| `.gitattributes` | Create | Consistent line endings |
| `README.md` | Modify | Multi-platform install instructions |
| `CONTRIBUTING.md` | Modify | OpenClaw metadata + ClawHub docs |

---

*Last updated: 2026-03-21*
*License: Apache-2.0*
