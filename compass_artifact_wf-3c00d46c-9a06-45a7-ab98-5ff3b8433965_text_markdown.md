# Publishing and ingesting skills into skills.sh: the complete technical guide

**skills.sh has no publish command.** Skills appear automatically when users install them via `npx skills add owner/repo`, which sends anonymous telemetry that indexes the skill on the leaderboard. The entire ecosystem is built on the **Agent Skills open standard** (agentskills.io), created by Anthropic in December 2025, which defines the universal SKILL.md format now adopted by **26+ platforms** including Claude Code, OpenAI Codex, Cursor, Windsurf, GitHub Copilot, and Gemini CLI. This report covers the exact schemas, file structures, and CI/CD patterns for every part of the skills publishing pipeline.

---

## 1. How skills.sh ingestion actually works

skills.sh is built by **Vercel** (source: github.com/vercel-labs/skills) as "The Agent Skills Directory." It is a discovery platform and CLI, not a traditional registry with a submission flow. The npm package `skills` provides the CLI interface that handles installation across **41+ AI coding agents**.

When you run `npx skills add owner/repo`, the CLI clones the repository to a temp directory, recursively scans for directories containing `SKILL.md` files, presents an interactive TUI for selecting which skills to install and which agents to target, then symlinks (default) or copies the skill to agent-specific directories. Anonymous telemetry is sent to skills.sh, which indexes the skill and tracks install counts on the leaderboard. There is no review process, no approval queue, and no explicit publish step.

The CLI accepts multiple source formats:

```bash
npx skills add vercel-labs/agent-skills          # GitHub shorthand
npx skills add https://github.com/org/repo       # Full URL
npx skills add https://github.com/org/repo/tree/main/skills/specific-skill  # Direct path
npx skills add ./my-local-skills                  # Local path
npx skills add https://gitlab.com/org/repo        # GitLab URL
```

Key CLI commands beyond `add` include `npx skills list` (list installed), `npx skills find [query]` (search), `npx skills remove` (uninstall), `npx skills check` (check updates), `npx skills update` (update all), and `npx skills init [name]` (scaffold new skill). For CI/CD, the `-y` flag skips confirmation prompts, and `--skill <name>` targets a specific skill within a monorepo.

Installation destinations vary by agent: **Claude Code** uses `~/.claude/skills/` (global) or `.claude/skills/` (project); **Cursor** uses `.cursor/skills/`; **Codex** uses `~/.codex/skills/` or `.agents/skills/`; **Copilot** uses `.github/skills/`; and the canonical cross-agent path is `~/.agents/skills/`. A lock file at `~/.agents/.skill-lock.json` (global) or `skills-lock.json` (local, git-committable) tracks installed skills.

---

## 2. The exact SKILL.md YAML frontmatter schema

The SKILL.md specification is formally defined at agentskills.io/specification, maintained in the `agentskills/agentskills` GitHub repository (**13.1k stars**). The spec is deliberately minimal — only **six allowed top-level frontmatter keys** exist, and any key outside this set causes validation failure:

| Field | Required | Type | Constraints |
|-------|----------|------|-------------|
| `name` | **Yes** | string | Max 64 chars. Lowercase `[a-z0-9-]` only. Must not start/end with hyphen. No consecutive hyphens. **Must match parent directory name.** |
| `description` | **Yes** | string | Max 1024 chars. Non-empty. Must describe what the skill does AND when to use it. This is the **primary trigger mechanism** — agents read descriptions to decide whether to load a skill. |
| `license` | No | string | SPDX identifier or reference to bundled license file |
| `compatibility` | No | string | Max 500 chars. Environment requirements |
| `metadata` | No | map[string→string] | Arbitrary key-value pairs (author, version, etc.) |
| `allowed-tools` | No | string | Space-delimited pre-approved tools (experimental) |

A minimal valid SKILL.md:

```markdown
---
name: network-audit
description: Audit network device configurations for security compliance. Use when reviewing router, switch, or firewall configs against CIS benchmarks.
---

# Network Audit Skill

## When to use
Use this skill when the user needs to audit network device configurations...

## Steps
1. Identify the target device type and OS
2. Collect running configuration
3. Compare against compliance baselines
```

A full-featured SKILL.md with all fields:

```markdown
---
name: pdf-processing
description: Extract text and tables from PDF files, fill forms, merge documents. Use when working with PDF documents or when the user mentions PDFs, forms, or document extraction.
license: Apache-2.0
compatibility: Requires poppler-utils for PDF extraction
metadata:
  author: example-org
  version: "1.0"
allowed-tools: Bash(pdftotext:*) Read Write
---

# PDF Processing Skill

## Steps
1. Validate the PDF file exists
2. Run extraction script: scripts/extract.py
3. Present the extracted text
```

**Progressive disclosure** is a core design principle. Loading happens in three tiers: **Tier 1 (Catalog)** loads only `name` + `description` (~100 tokens per skill) at session startup for ALL installed skills. **Tier 2 (Instructions)** loads the full SKILL.md body (recommended under **5,000 tokens**) only when the skill is activated. **Tier 3 (Resources)** loads files from `scripts/`, `references/`, and `assets/` directories only when explicitly referenced. This means a project can have dozens of installed skills without overwhelming the context window.

skills.sh indexes `name`, `description`, source repository (`owner/repo`), and install count. **There is no category or tag system.** The homepage offers suggested search terms — "code review, git workflow, testing, documentation, refactoring, API design, debugging, performance, security, deployment" — but these are not enforced taxonomies. Skills are ranked by install count with "All Time," "Trending (24h)," and "Hot" views.

---

## 3. Multi-skill repos and monorepo conventions

**A single GitHub repository can and commonly does contain multiple skills.** This is the standard pattern used by nearly every major skill provider. The directory convention is a `skills/` subdirectory, where each skill occupies its own named folder containing a `SKILL.md`:

```
my-skills-repo/
├── skills/
│   ├── code-review/
│   │   ├── SKILL.md
│   │   └── references/
│   │       └── checklist.md
│   ├── security-audit/
│   │   ├── SKILL.md
│   │   ├── scripts/
│   │   │   └── scan.py
│   │   └── references/
│   │       ├── owasp-top-10.md
│   │       └── cis-benchmarks.md
│   └── deploy-production/
│       └── SKILL.md
└── README.md
```

When you run `npx skills add owner/repo` on a multi-skill repo, the CLI discovers all SKILL.md files, presents an interactive selection UI, and lets you install individual skills (`--skill skill-name`), multiple skills, or all skills (`--all`). On skills.sh, each skill gets its own page at `skills.sh/owner/repo/skill-name`.

Real-world examples demonstrate the pattern. **Anthropic's `anthropics/skills`** contains skills like `frontend-design`, `pdf`, `skill-creator`, and `mcp-builder`. **Vercel's `vercel-labs/agent-skills`** has `vercel-react-best-practices`, `web-design-guidelines`, and `vercel-composition-patterns`. **Sentry's `getsentry/skills`** includes `code-review`, `security-review`, `gha-security-review`, and `django-access-review`. **Composio's `composiohq/awesome-claude-skills`** is the largest monorepo at **78+ skills**, one per SaaS integration (gmail-automation, slack-automation, github-automation, etc.).

---

## 4. The Agent Skills open standard at agentskills.io

The Agent Skills specification was **created by Anthropic** and released as an open standard on **December 18, 2025**. It lives at agentskills.io (published via Mintlify from `github.com/agentskills/agentskills`, 13.1k stars). The code is Apache 2.0; documentation is CC-BY-4.0.

The GitHub organization `agentskills` (not `agent-skills`) contains two repositories: the main spec repo and a `.github` profile repo. **skills.sh is a separate project by Vercel** that is built on top of the Agent Skills standard — it is not part of the official spec but fully implements it.

The spec includes a **client implementation guide** at agentskills.io/integrate-skills that defines how agent platforms should discover and load skills. The recommended discovery paths are project-level (`<project>/.<your-client>/skills/` and `<project>/.agents/skills/`) and user-level (`~/.<your-client>/skills/` and `~/.agents/skills/`). The `.agents/skills/` path is the cross-client interoperability convention.

For presenting skills to the model, the spec recommends an XML catalog format:

```xml
<available_skills>
  <skill>
    <name>pdf-processing</name>
    <description>Extract PDF text, fill forms, merge files.</description>
    <location>/home/user/.agents/skills/pdf-processing/SKILL.md</location>
  </skill>
</available_skills>
```

An official **reference Python library** called `skills-ref` (`pip install skills-ref`) provides CLI commands: `agentskills validate path/to/skill` (validate a skill directory), `agentskills read-properties path/to/skill` (output JSON of skill metadata), and `agentskills to-prompt path/to/skill-a path/to/skill-b` (generate the XML catalog). This library is labeled as "intended for demonstration purposes only, not meant for production."

Platform-specific extensions are handled through the `metadata` field. **OpenAI Codex** adds an `agents/openai.yaml` file alongside SKILL.md for UI metadata (display_name, icons, brand_color, invocation policy, MCP dependencies). **Claude Code** adds optional frontmatter fields like `context: fork` (run in forked agent), `disable-model-invocation: true`, and `agent: Explore`. These extensions don't break compatibility — platforms that don't understand them simply ignore them.

---

## 5. OpenClaw skill format and NetClaw mapping

OpenClaw (github.com/openclaw/openclaw, **170k+ stars**) is a self-hosted AI assistant platform that uses AgentSkills-compatible SKILL.md files as its primary extensibility mechanism. Skills are discovered from four locations in priority order: workspace skills (`<workspace>/skills/<name>/SKILL.md`), managed skills (`~/.openclaw/skills/<name>/SKILL.md`), bundled skills (shipped with install), and extra directories configured via `skills.load.extraDirs` in `openclaw.json`.

OpenClaw extends the base SKILL.md spec through the `metadata.openclaw` field (a single-line JSON object due to parser limitations):

```yaml
---
name: nano-banana-pro
description: Generate or edit images via Gemini 3 Pro Image
user-invocable: true
disable-model-invocation: false
command-dispatch: tool
command-tool: my-tool-name
metadata: {"openclaw":{"requires":{"bins":["uv"],"env":["GEMINI_API_KEY"]},"primaryEnv":"GEMINI_API_KEY","emoji":"🍌","os":["darwin","linux","win32"],"install":[{"id":"brew","kind":"brew","formula":"gemini-cli","bins":["gemini"]}]}}
---
```

OpenClaw-specific extensions include `requires.bins` (required binaries on PATH), `requires.env` (required environment variables), `requires.config` (required openclaw.json paths), `os` (platform filter), `install` (installer specs for brew/node/go/uv/download), `emoji` (UI decoration), and `primaryEnv` (API key association).

The `openclaw.json` configuration file (JSON5 format, located at `~/.openclaw/openclaw.json`) has a `skills` section:

```json5
{
  skills: {
    install: { nodeManager: "npm" },
    load: { extraDirs: ["/path/to/shared/skills"], watch: true },
    entries: {
      "my-skill": {
        enabled: true,
        apiKey: { source: "env", provider: "default", id: "MY_API_KEY" },
        env: { MY_API_KEY: "key-here" }
      }
    }
  }
}
```

**NetClaw** (github.com/automateyournetwork/netclaw) is a CCIE-level AI network engineering agent built on top of OpenClaw with **82+ network skills** and **37 MCP server backends**. It is NOT a separate format — it uses standard OpenClaw SKILL.md files with network-specific content. NetClaw's `install.sh` bootstrap script installs OpenClaw globally, copies skill files to `~/.openclaw/workspace/skills/`, clones 37 MCP server repositories, and configures environment variables. NetClaw also uses workspace markdown files (`SOUL.md`, `AGENTS.md`, `IDENTITY.md`, `USER.md`, `TOOLS.md`, `HEARTBEAT.md`) injected into the system prompt for deep protocol knowledge (OSPF LSAs, BGP path selection, EIGRP DUAL, etc.).

---

## 6. Claude Code skills format and how it differs

Claude Code uses the **same SKILL.md format** defined at agentskills.io — it is, after all, the creator of the standard. Skills are discovered at `~/.claude/skills/` (personal, all projects) and `.claude/skills/` (project-specific). Claude Code also supports nested discovery: when editing files in `packages/frontend/`, it checks `packages/frontend/.claude/skills/` as well.

Claude Code's discovery mechanism uses **no algorithmic routing, embedding matching, or intent classification.** All available skill names and descriptions are formatted into the Skill tool's prompt, and Claude's language model makes the selection decision purely through LLM reasoning. The `description` field is therefore the primary triggering mechanism and should be written to clearly indicate both what the skill does and when it should be used.

Claude Code adds a few optional frontmatter fields beyond the base spec: `context: fork` runs the skill in a forked Explore agent, `agent: Explore` specifies which subagent to use, and `disable-model-invocation: true` prevents auto-invocation (only user can trigger). These are Claude Code-specific and ignored by other platforms.

The key difference between Claude Code's native skill support and skills.sh is that **skills.sh is a distribution layer**, not a competing format. skills.sh provides the CLI for installing, updating, and discovering skills across all platforms, while Claude Code provides the runtime that loads and activates them. They use the exact same SKILL.md format.

---

## 7. Cross-platform skill compatibility across all major agents

**SKILL.md is now the universal format**, adopted by 26+ platforms. A second complementary standard, **AGENTS.md** (agents.md, stewarded by the Agentic AI Foundation under the Linux Foundation), provides project-level instructions without frontmatter. Most tools now support both.

Here is how each major platform handles skills:

- **Claude Code**: Native SKILL.md at `.claude/skills/`. Three-tier progressive disclosure. Auto-invocation via LLM reasoning.
- **OpenAI Codex CLI**: Native SKILL.md at `.agents/skills/` + AGENTS.md (plain markdown, no frontmatter, 32 KiB default cap). Optional `agents/openai.yaml` for UI metadata.
- **Cursor**: Project Rules at `.cursor/rules/*.mdc` (MDC format with YAML frontmatter: `description`, `globs`, `alwaysApply`). Also reads AGENTS.md and `.cursorrules` (legacy, deprecated).
- **Windsurf**: Three systems — Rules (`.windsurf/rules/*.md`), Skills (`.windsurf/skills/*/SKILL.md` following Agent Skills spec), and Workflows (`.windsurf/workflows/*.md`, manual-only via `/workflow-name`). Also reads `.agents/skills/` and AGENTS.md.
- **Cline**: `.clinerules/` directory with markdown files. Optional YAML frontmatter with `paths` for conditional activation. Auto-detects `.cursorrules`, `.windsurfrules`, and AGENTS.md for compatibility.
- **GitHub Copilot**: `.github/skills/` and `.agents/skills/`. Full SKILL.md support.
- **Gemini CLI**: `.gemini/skills/` and `.agents/skills/`.

The two emerging open standards are **complementary, not competing**: AGENTS.md is for "always-on" project context (coding conventions, architecture decisions); SKILL.md is for on-demand specialized capabilities with progressive disclosure. A project typically uses both — AGENTS.md for project rules and SKILL.md for reusable tools.

| Feature | Claude Code | Codex CLI | Cursor | Windsurf | Cline |
|---------|------------|-----------|--------|----------|-------|
| **Primary format** | SKILL.md | AGENTS.md + SKILL.md | .cursor/rules/*.mdc | SKILL.md + Rules + Workflows | .clinerules/*.md |
| **SKILL.md native** | ✅ | ✅ | ✅ | ✅ | ✅ |
| **AGENTS.md native** | No | ✅ | ✅ | ✅ | ✅ |
| **Auto-invocation** | LLM decides | Always loaded | Globs/alwaysApply | Description match | Conditional paths |
| **Progressive disclosure** | ✅ 3-tier | Partial | No | ✅ (skills) | No |

---

## 8. MCP server registration at registry.modelcontextprotocol.io

The MCP Registry is a **metaregistry** — it hosts metadata about servers, not the servers themselves. Actual packages live on npm, PyPI, Docker Hub, etc. The registry launched in September 2025, is backed by Anthropic, GitHub, PulseMCP, and Microsoft, and uses a **CLI-based submission process** (not PR-based).

**Registration workflow:**

1. Install the publisher: `brew install mcp-publisher` (or download binary)
2. Initialize: `mcp-publisher init` (creates `server.json` in your project)
3. Add validation metadata to your package (e.g., `"mcpName": "io.github.username/server-name"` in `package.json` for npm)
4. Publish your package to the underlying registry (npm, PyPI, etc.) first
5. Authenticate: `mcp-publisher login github` (opens browser OAuth for `io.github.*` namespaces)
6. Publish metadata: `mcp-publisher publish`

The `server.json` schema (latest: `https://static.modelcontextprotocol.io/schemas/2025-12-11/server.schema.json`):

```json
{
  "$schema": "https://static.modelcontextprotocol.io/schemas/2025-12-11/server.schema.json",
  "name": "io.github.my-username/weather",
  "description": "An MCP server for weather information.",
  "repository": {
    "url": "https://github.com/my-username/mcp-weather-server",
    "source": "github"
  },
  "version": "1.0.0",
  "packages": [
    {
      "registryType": "npm",
      "identifier": "@my-username/mcp-weather-server",
      "version": "1.0.0",
      "transport": { "type": "stdio" },
      "environmentVariables": [
        {
          "description": "Your API key for the service",
          "isRequired": true,
          "format": "string",
          "isSecret": true
        }
      ]
    }
  ]
}
```

Required fields are `name` (reverse-DNS format like `io.github.username/server-name`), `description`, `version`, and at least one of `packages` or `remotes`. Supported package registry types are **npm, PyPI, NuGet, OCI (Docker), and MCPB** (MCP Bundle). Transport types are `stdio`, `sse`, and `streamable-http`. Namespaces use GitHub OAuth for `io.github.*` or DNS verification for custom domains (`com.company.*`).

**skills.sh and the MCP Registry operate at different layers and are complementary.** The MCP Registry answers "how do agents connect to tools?" while skills.sh answers "how do developers share agent workflows?" A deployment skill on skills.sh might orchestrate multiple MCP servers registered in the MCP Registry.

---

## 9. Existing network and security skills on skills.sh

There are **no dedicated network engineering skills** on skills.sh. No router/switch configuration, no Ansible/Nornir network automation, no firewall rule management, no protocol analysis, and no infrastructure security skills exist in the current directory. This represents a significant gap in the ecosystem.

Several **application security** skills exist. The highest quality is **`security-review`** by `getsentry/skills`, which provides OWASP-informed security code auditing with 17 vulnerability-specific reference files (injection, XSS, SSRF, CSRF, auth, crypto, deserialization, file security, API security, and more) plus language guides for Python/Django, JavaScript/Node/React, Go, Rust, and Docker/Kubernetes. Other security-adjacent skills include `security-best-practices` by supercent-io (11.9K installs), `gha-security-review` by Sentry (GitHub Actions security), `audit-website` by squirrelscan (34.6K installs, covering SEO/performance/security/accessibility), and `harden` by pbakaus/impeccable (10.6K installs). No NIST, CIS, SOC2 compliance skills, penetration testing skills, or cloud security skills exist on the platform.

---

## 10. Monorepo-to-skills.sh publishing pipeline

Since skills.sh auto-indexes through install telemetry, the "publishing" pipeline is really a **validation and distribution pipeline**. The pattern is:

1. **Create a public GitHub repo** with valid SKILL.md files in `skills/` subdirectories
2. **Validate in CI** using either the official Python library or the skills CLI:

```yaml
# .github/workflows/validate.yml
name: Validate Skills
on: push
jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: pip install skills-ref
      - run: |
          for skill in skills/*/; do
            agentskills validate "$skill"
          done
```

3. **Share install commands** in your README and documentation
4. **As users install**, telemetry auto-indexes on skills.sh's leaderboard

For auto-generating SKILL.md files from existing tool definitions, several tools have emerged. **`@tanstack/intent`** is the most sophisticated, generating skills from library documentation with staleness detection tied to doc changes. **Mintlify** automatically generates `/.well-known/skills/default/skill.md` for all documentation sites, regenerated on every deploy. **Anthropic's `skill-creator` meta-skill** guides Claude through creating new skills interactively with description optimization and test case generation. **Cloudflare's `.well-known/skills/index.json`** discovery protocol lets organizations publish a skills index that the CLI can discover from any URL (`npx skills add https://mintlify.com/docs`).

For npm packages specifically, **`skills-npm`** by Anthony Fu discovers skills shipped inside npm packages with monorepo support (`skills-npm --recursive`), and **`@tanstack/intent`** bundles skills alongside the npm package itself so they update via `npm update`. The `npx skills validate --strict` command (proposed in PR #509 on vercel-labs/skills) treats warnings as errors for CI gating, validating name format (1-64 chars, kebab-case), description length (20-500 chars), SPDX license compliance, and repository URL validity.

---

## Conclusion

The AI agent skills ecosystem has converged remarkably fast around a single format. **SKILL.md with YAML frontmatter** (name + description required, four optional fields) is the universal standard, created by Anthropic and adopted by every major AI coding platform. skills.sh is the dominant distribution hub but requires no explicit publishing — simply maintaining a public GitHub repo with valid SKILL.md files and sharing install commands is sufficient. The MCP Registry operates at a complementary layer for tool connectivity, using `server.json` with reverse-DNS naming and CLI-based publishing.

The most underserved area is **network engineering and infrastructure security** — no skills exist for this domain on skills.sh despite the NetClaw project demonstrating 82+ network skills running on OpenClaw. For monorepo publishing, the validation-in-CI pattern using `skills-ref` or `npx skills validate --strict` is the emerging best practice, with auto-generation tools like `@tanstack/intent` and Mintlify's `.well-known/skills` protocol addressing the "docs-to-skills" pipeline.