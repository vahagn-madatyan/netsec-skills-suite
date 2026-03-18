---
estimated_steps: 5
estimated_files: 3
---

# T01: Build vendor-agnostic ACL rule analysis skill with multi-vendor inline labels

**Slice:** S02 — Rule Analysis & Compliance Skills
**Milestone:** M002

## Description

Create the `acl-rule-analysis` skill (R021) — a vendor-agnostic ACL and firewall rule analysis skill that detects shadowed rules, overly permissive rules, unused rules, and recommends rule ordering optimization. Uses the "policy audit" procedure shape proven in S01, but applies it to universal rule patterns rather than vendor-specific policy evaluation.

This skill uses 6-vendor inline labels (`[Cisco]`/`[JunOS]`/`[EOS]`/`[PAN-OS]`/`[FortiGate]`/`[CheckPoint]`) for CLI commands, following the same multi-vendor labeling convention as M001 routing skills (see `skills/bgp-analysis/SKILL.md` for the pattern). The analysis algorithms (shadowed rule detection, redundancy check, etc.) are vendor-agnostic — only the "how to retrieve rules" commands are vendor-specific.

Three files are created: SKILL.md + `references/cli-reference.md` + `references/rule-patterns.md`.

## Steps

1. Create directory `skills/acl-rule-analysis/references/` (mkdir -p).

2. Create `skills/acl-rule-analysis/SKILL.md` with:
   - **Frontmatter:** `name: acl-rule-analysis`, `description` mentioning shadowed rules / overly permissive / unused / rule ordering, `license: Apache-2.0`, `metadata.safety: read-only`, `metadata.author: network-security-skills-suite`, `metadata.version: "1.0.0"`.
   - **Intro paragraph:** Vendor-agnostic rule analysis. Unlike vendor-specific firewall audit skills (S01), this skill focuses on universal rule patterns: shadowed rules, redundant rules, overly permissive rules, unused rules. Covers ACLs (Cisco/JunOS/EOS) and firewall policies (PAN-OS/FortiGate/CheckPoint). Reference the two reference files.
   - **7 required H2 sections:**
     - `## When to Use` — post-migration rule cleanup, periodic rulebase hygiene, compliance preparation, incident investigation (did a rule allow bad traffic?)
     - `## Prerequisites` — read-only access to device, rulebase with hit counters, for unused rule detection need hit count data over extended period (30+ days)
     - `## Procedure` — 7 steps following "policy audit" shape:
       1. Collect rulebase from target device (multi-vendor CLI with inline labels)
       2. Identify shadowed rules (rule A precedes rule B; A's match criteria is superset of B's — B never matches)
       3. Detect overly permissive rules (any/any source-dest, permit ip any any, broad service groups, "any" application)
       4. Find unused rules (zero hit count over extended period — platform-specific hit count commands)
       5. Identify redundant/duplicate rules (overlapping match criteria with same action)
       6. Rule ordering optimization (most-hit rules near top for performance; deny rules before matching permits)
       7. Generate consolidated rule recommendations
     - `## Threshold Tables` — "Rule Risk Severity Classification" table: Critical (any/any permit, shadowed deny overridden by permit), High (broad subnet permits, unused rules with permit action), Medium (redundant rules, suboptimal ordering), Low (unused deny rules, cosmetic naming issues)
     - `## Decision Trees` — remediation priority flowchart: Is rule overly permissive? → Is it actively used? → Can it be narrowed? → etc.
     - `## Report Template` — fenced markdown template with sections: Executive Summary, Shadowed Rules, Overly Permissive Rules, Unused Rules, Redundant Rules, Ordering Recommendations
     - `## Troubleshooting` — common issues: hit counters cleared after reboot, ACL vs firewall policy semantics differences, implicit deny handling varies by platform
   - Use `[Cisco]`/`[JunOS]`/`[EOS]`/`[PAN-OS]`/`[FortiGate]`/`[CheckPoint]` inline labels for vendor-specific commands. Keep the body under 2700 words — offload vendor CLI details to references.

3. Create `skills/acl-rule-analysis/references/cli-reference.md`:
   - Multi-vendor CLI commands for retrieving ACLs, rulebases, and hit counts
   - Table format: `| Function | CLI Command |` with section headers per vendor or per audit category
   - Cover: Cisco IOS/ASA (`show access-lists`, `show ip access-lists`), JunOS (`show firewall filter`, `show configuration firewall`), EOS (`show ip access-lists`, `show access-lists counters`), PAN-OS (`show running security-policy`, XML API queries), FortiOS (`diagnose firewall policy`, `get firewall policy`), Check Point (`fw stat`, `cpstat fw`, SmartConsole export)
   - Include hit count retrieval commands per platform

4. Create `skills/acl-rule-analysis/references/rule-patterns.md`:
   - Rule analysis pattern definitions with detection logic
   - Sections: Shadowed Rule Detection (algorithm: for each rule, check if any preceding rule's match criteria is a superset), Redundant Rule Identification (same action + overlapping match = candidate for merge), Overly Permissive Rule Patterns (enumerate risky patterns: any/any, broad subnets, all-services), Unused Rule Detection (hit count = 0 over 30+ days, caveats: seasonal traffic, backup paths), Rule Ordering Optimization (performance: most-hit first; security: most-specific first), Conflict Detection (permit/deny for same traffic — order determines outcome)

5. Verify:
   - `bash scripts/validate.sh` — should show 17 skills, 0 errors
   - `awk 'BEGIN{c=0} /^---$/{c++; if(c==2){found=1; next}} found{print}' skills/acl-rule-analysis/SKILL.md | wc -w` — must be ≤2700
   - `ls skills/acl-rule-analysis/references/ | wc -l` — must be 2
   - `grep -l 'shadowed' skills/acl-rule-analysis/SKILL.md` — confirms rule analysis depth
   - `grep '\[Cisco\]' skills/acl-rule-analysis/SKILL.md` — confirms multi-vendor labels

## Must-Haves

- [ ] Frontmatter has `name: acl-rule-analysis`, `metadata.safety: read-only`, `license: Apache-2.0`
- [ ] Body has all 7 required H2 sections: When to Use, Prerequisites, Procedure, Threshold Tables, Decision Trees, Report Template, Troubleshooting
- [ ] Procedure covers: shadowed rules, overly permissive rules, unused rules, redundant rules, rule ordering optimization
- [ ] Uses `[Cisco]`/`[JunOS]`/`[EOS]`/`[PAN-OS]`/`[FortiGate]`/`[CheckPoint]` inline labels for vendor CLI
- [ ] Body ≤2700 words (use K001 awk method for word count)
- [ ] `references/` directory has exactly 2 files: `cli-reference.md` and `rule-patterns.md`
- [ ] `bash scripts/validate.sh` passes with 17 skills and 0 errors

## Verification

- `bash scripts/validate.sh` exits 0 with "Skills checked: 17" and "Result: PASS (0 errors)"
- `awk 'BEGIN{c=0} /^---$/{c++; if(c==2){found=1; next}} found{print}' skills/acl-rule-analysis/SKILL.md | wc -w` ≤ 2700
- `ls skills/acl-rule-analysis/references/ | wc -l` = 2
- `grep -l 'shadowed' skills/acl-rule-analysis/SKILL.md` returns the file path
- `grep '\[Cisco\]' skills/acl-rule-analysis/SKILL.md` returns matches

## Inputs

- `skills/palo-alto-firewall-audit/SKILL.md` — reference for SKILL.md structure, frontmatter format, 7 H2 sections, Threshold Tables as severity classification, Report Template as fenced markdown block
- `skills/bgp-analysis/SKILL.md` — reference for multi-vendor inline labeling convention (`[Cisco]`/`[JunOS]`/`[EOS]` pattern)
- `skills/palo-alto-firewall-audit/references/cli-reference.md` — reference for CLI reference table format (`| Function | CLI Command |` with section headers)
- K001 in KNOWLEDGE.md — use `awk` (not `sed`) for body word count on macOS

## Observability Impact

- **New skill in validate.sh:** After T01, `bash scripts/validate.sh` reports 17 skills (was 16). A future agent inspects this task by running validate.sh and confirming `acl-rule-analysis` appears with all OK checks.
- **Word count signal:** `awk 'BEGIN{c=0} /^---$/{c++; if(c==2){found=1; next}} found{print}' skills/acl-rule-analysis/SKILL.md | wc -w` — body word count must stay ≤2700. If a future edit pushes it over, this is the diagnostic command.
- **Content depth:** `grep -c 'shadowed\|permissive\|unused\|redundant' skills/acl-rule-analysis/SKILL.md` — confirms all 4 rule analysis categories are present. A count of 0 for any keyword indicates missing coverage.
- **Multi-vendor label coverage:** `grep -c '\[Cisco\]\|\[JunOS\]\|\[EOS\]\|\[PAN-OS\]\|\[FortiGate\]\|\[CheckPoint\]' skills/acl-rule-analysis/SKILL.md` — confirms inline vendor labels are present.
- **Failure state:** If validate.sh shows `ERROR:` lines for `acl-rule-analysis`, the specific check (metadata.safety, missing H2 section, or missing references/) is named in the error message.

## Expected Output

- `skills/acl-rule-analysis/SKILL.md` — vendor-agnostic ACL/rule analysis skill with shadowed, permissive, unused, redundant rule detection + ordering optimization
- `skills/acl-rule-analysis/references/cli-reference.md` — multi-vendor CLI commands for ACL/rulebase/hit-count retrieval
- `skills/acl-rule-analysis/references/rule-patterns.md` — rule analysis pattern definitions with detection algorithms
