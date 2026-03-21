# NEMONET.md — NemoNet Integration Plan

> NemoNet-specific design for consuming netsec-skills-suite in NVIDIA NemoClaw fork.
> See DESIGN-CLAW.md for this-repo changes (OpenClaw metadata, ClawHub, submodule support).

---

## Table of Contents

1. [What NemoNet Is](#1-what-nemonet-is)
2. [NemoNet Repo Integration](#2-nemonet-repo-integration)
3. [Deployment Targets](#3-deployment-targets)
4. [MCP Server Coordination](#4-mcp-server-coordination)
5. [NemoNet-Specific Security](#5-nemonet-specific-security)
6. [Naming Decision](#6-naming-decision)
7. [NemoNet Scripts](#7-nemonet-scripts)
8. [Implementation Checklist — Phase 4 (NemoNet Repo Setup)](#8-implementation-checklist--phase-4-nemonet-repo-setup)

---

## 1. What NemoNet Is

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

## 2. NemoNet Repo Integration

### 2.1 Submodule Setup (NemoNet repo)

```bash
cd nemonet/
git submodule add https://github.com/vahagn-madatyan/netsec-skills-suite.git \
    skills/netsec-skills-suite
git commit -m "feat: add netsec-skills-suite as submodule"
```

### 2.2 Dockerfile.sandbox

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

### 2.3 Launchable setup.sh

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

## 3. Deployment Targets

| Target                      | Use Case              | Skills Source                    | Inference          |
|-----------------------------|-----------------------|----------------------------------|--------------------|
| **NVIDIA Brev Launchable**  | Demos, evaluation     | `git clone` (latest HEAD)        | NVIDIA Cloud       |
| **AWS EC2 (production)**    | 24/7 ops              | Submodule (pinned version)       | Claude Opus/Sonnet |
| **DGX Spark**               | Air-gapped demos      | Baked into container image       | Local Nemotron NIM |
| **EKS / OpenShift**         | Multi-tenant SaaS     | Container image per release      | Mixed              |

---

## 4. MCP Server Coordination

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

## 5. NemoNet-Specific Security

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

## 6. Naming Decision

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

## 7. NemoNet Scripts

### 7.1 `scripts/nemonet-install.sh`

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

### 7.2 `scripts/generate-egress-policy.sh`

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

## 8. Implementation Checklist — Phase 4 (NemoNet Repo Setup)

- [ ] Fork NVIDIA/NemoClaw → your-org/nemonet
- [ ] Add `netsec-skills-suite` as git submodule
- [ ] Create `nemonet-blueprint/` with network-specific policies
- [ ] Build custom sandbox Docker image with skills + MCP servers
- [ ] Create `launchable/` directory with Brev config
- [ ] Publish Launchable to NVIDIA Brev Explore catalog
- [ ] Add launch badge to README

---

*Last updated: 2026-03-21*
*License: Apache-2.0*
