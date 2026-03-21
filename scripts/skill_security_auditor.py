#!/usr/bin/env python3
"""
Skill Security Auditor — Scan AI agent skills for security risks.

Adapted for network security skills that contain shell commands in
SKILL.md procedure blocks and reference files.

Usage:
    python3 skill_security_auditor.py /path/to/skill/
    python3 skill_security_auditor.py /path/to/skill/ --strict --json
    python3 skill_security_auditor.py skills/          # scan all skills

Exit codes:
    0 = PASS (safe to install)
    1 = FAIL (critical findings, do not install)
    2 = WARN (review manually before installing)
"""

import argparse
import json
import os
import re
import sys
from dataclasses import dataclass, field, asdict
from enum import IntEnum
from pathlib import Path
from typing import Optional


class Severity(IntEnum):
    INFO = 0
    HIGH = 1
    CRITICAL = 2


SEVERITY_LABELS = {
    Severity.INFO: "⚪ INFO",
    Severity.HIGH: "🟡 HIGH",
    Severity.CRITICAL: "🔴 CRITICAL",
}

SEVERITY_NAMES = {
    Severity.INFO: "INFO",
    Severity.HIGH: "HIGH",
    Severity.CRITICAL: "CRITICAL",
}


@dataclass
class Finding:
    severity: Severity
    category: str
    file: str
    line: int
    pattern: str
    risk: str
    fix: str

    def to_dict(self):
        d = asdict(self)
        d["severity"] = SEVERITY_NAMES[self.severity]
        return d


@dataclass
class AuditReport:
    skill_name: str
    skill_path: str
    findings: list = field(default_factory=list)
    files_scanned: int = 0
    scripts_scanned: int = 0
    md_files_scanned: int = 0

    @property
    def critical_count(self):
        return sum(1 for f in self.findings if f.severity == Severity.CRITICAL)

    @property
    def high_count(self):
        return sum(1 for f in self.findings if f.severity == Severity.HIGH)

    @property
    def info_count(self):
        return sum(1 for f in self.findings if f.severity == Severity.INFO)

    @property
    def verdict(self):
        if self.critical_count > 0:
            return "FAIL"
        if self.high_count > 0:
            return "WARN"
        return "PASS"

    def to_dict(self):
        return {
            "skill_name": self.skill_name,
            "skill_path": self.skill_path,
            "verdict": self.verdict,
            "summary": {
                "critical": self.critical_count,
                "high": self.high_count,
                "info": self.info_count,
                "total": len(self.findings),
            },
            "stats": {
                "files_scanned": self.files_scanned,
                "scripts_scanned": self.scripts_scanned,
                "md_files_scanned": self.md_files_scanned,
            },
            "findings": [f.to_dict() for f in self.findings],
        }


# =============================================================================
# COMMAND / CODE EXECUTION PATTERNS
# =============================================================================

CODE_PATTERNS = [
    # Command injection — CRITICAL
    {
        "regex": r"\bos\.system\s*\(",
        "category": "CMD-INJECT",
        "severity": Severity.CRITICAL,
        "risk": "Arbitrary command execution via os.system()",
        "fix": "Use subprocess.run() with list arguments and shell=False",
    },
    {
        "regex": r"\bos\.popen\s*\(",
        "category": "CMD-INJECT",
        "severity": Severity.CRITICAL,
        "risk": "Command execution via os.popen()",
        "fix": "Use subprocess.run() with list arguments and capture_output=True",
    },
    {
        "regex": r"\bsubprocess\.\w+\([^)]*shell\s*=\s*True",
        "category": "CMD-INJECT",
        "severity": Severity.CRITICAL,
        "risk": "Shell injection via subprocess with shell=True",
        "fix": "Use subprocess.run() with list arguments and shell=False",
    },
    # Code execution — CRITICAL
    {
        "regex": r"\beval\s*\(",
        "category": "CODE-EXEC",
        "severity": Severity.CRITICAL,
        "risk": "Arbitrary code execution via eval()",
        "fix": "Use ast.literal_eval() for data parsing or explicit parsing logic",
    },
    {
        "regex": r"\bexec\s*\(",
        "category": "CODE-EXEC",
        "severity": Severity.CRITICAL,
        "risk": "Arbitrary code execution via exec()",
        "fix": "Remove exec() — rewrite logic to avoid dynamic code execution",
    },
    {
        "regex": r"\b__import__\s*\(",
        "category": "CODE-EXEC",
        "severity": Severity.CRITICAL,
        "risk": "Dynamic module import — can load arbitrary code",
        "fix": "Use explicit import statements",
    },
    # Obfuscation — CRITICAL
    {
        "regex": r"\bbase64\.b64decode\s*\(",
        "category": "OBFUSCATION",
        "severity": Severity.CRITICAL,
        "risk": "Base64 decoding — may hide malicious payloads",
        "fix": "Review decoded content. If not processing user data, remove base64 usage",
    },
    {
        "regex": r"\\x[0-9a-fA-F]{2}(?:\\x[0-9a-fA-F]{2}){7,}",
        "category": "OBFUSCATION",
        "severity": Severity.CRITICAL,
        "risk": "Long hex-encoded string — likely obfuscated payload",
        "fix": "Decode and inspect the content. Replace with readable strings",
    },
    # Network exfiltration — CRITICAL
    {
        "regex": r"\brequests\.(?:post|put|patch)\s*\(",
        "category": "NET-EXFIL",
        "severity": Severity.CRITICAL,
        "risk": "Outbound HTTP write request — potential data exfiltration",
        "fix": "Remove outbound POST/PUT/PATCH or verify destination is trusted",
    },
    {
        "regex": r"\bsocket\.(?:connect|create_connection)\s*\(",
        "category": "NET-EXFIL",
        "severity": Severity.CRITICAL,
        "risk": "Raw socket connection — potential C2 or exfiltration channel",
        "fix": "Remove raw socket usage unless absolutely required",
    },
    # Credential harvesting — CRITICAL
    {
        "regex": r"(?:open|read|Path)\s*\([^)]*(?:\.ssh|\.aws|\.config/secrets|\.gnupg|\.npmrc|\.pypirc)",
        "category": "CRED-HARVEST",
        "severity": Severity.CRITICAL,
        "risk": "Reads credential files (SSH keys, AWS creds, secrets)",
        "fix": "Remove all access to credential directories",
    },
    {
        "regex": r"\bos\.environ\s*\[\s*['\"](?:AWS_|GITHUB_TOKEN|API_KEY|SECRET|PASSWORD|TOKEN|PRIVATE)",
        "category": "CRED-HARVEST",
        "severity": Severity.CRITICAL,
        "risk": "Extracts sensitive environment variables",
        "fix": "Remove credential access unless skill explicitly requires it",
    },
    # Privilege escalation — CRITICAL
    {
        "regex": r"\bos\.set(?:e)?uid\s*\(",
        "category": "PRIV-ESC",
        "severity": Severity.CRITICAL,
        "risk": "UID manipulation — privilege escalation",
        "fix": "Remove UID manipulation. Skills must run as the invoking user",
    },
    # Unsafe deserialization — HIGH
    {
        "regex": r"\bpickle\.loads?\s*\(",
        "category": "DESERIAL",
        "severity": Severity.HIGH,
        "risk": "Pickle deserialization — can execute arbitrary code",
        "fix": "Use json.loads() or other safe serialization formats",
    },
    {
        "regex": r"\byaml\.(?:load|unsafe_load)\s*\(",
        "category": "DESERIAL",
        "severity": Severity.HIGH,
        "risk": "Unsafe YAML loading — can execute arbitrary code",
        "fix": "Use yaml.safe_load()",
    },
]

# =============================================================================
# SHELL COMMAND PATTERNS (for commands in SKILL.md code blocks and .sh files)
# =============================================================================

SHELL_PATTERNS = [
    {
        "regex": r"\bcurl\s+.*\|\s*(?:ba)?sh\b",
        "category": "CMD-INJECT",
        "severity": Severity.CRITICAL,
        "risk": "Pipe-to-shell pattern — downloads and executes arbitrary code",
        "fix": "Download script first, inspect it, then execute explicitly",
    },
    {
        "regex": r"\bwget\s+.*&&\s*(?:ba)?sh\b",
        "category": "CMD-INJECT",
        "severity": Severity.CRITICAL,
        "risk": "Download-and-execute pattern",
        "fix": "Download script first, inspect it, then execute explicitly",
    },
    {
        "regex": r"\brm\s+-rf\s+/(?!\s*#)",
        "category": "FS-ABUSE",
        "severity": Severity.CRITICAL,
        "risk": "Recursive deletion from root — catastrophic data loss",
        "fix": "Remove destructive root-level deletion commands",
    },
    {
        "regex": r"\bchmod\s+(?:u\+s|4[0-7]{3})\b",
        "category": "PRIV-ESC",
        "severity": Severity.CRITICAL,
        "risk": "Setting SUID bit — privilege escalation",
        "fix": "Remove SUID modifications. Skills should never set SUID",
    },
    {
        "regex": r">\s*/dev/(?:sd[a-z]|nvme|loop)",
        "category": "FS-ABUSE",
        "severity": Severity.CRITICAL,
        "risk": "Direct write to block device — data destruction",
        "fix": "Remove direct block device writes",
    },
    {
        "regex": r"\bnc\s+-[el]|\bncat\s+-[el]|\bnetcat\b",
        "category": "NET-EXFIL",
        "severity": Severity.CRITICAL,
        "risk": "Netcat listener/connection — potential reverse shell",
        "fix": "Remove netcat usage",
    },
    {
        "regex": r"\b(?:python|python3|node|perl|ruby)\s+-c\s+['\"]",
        "category": "CODE-EXEC",
        "severity": Severity.HIGH,
        "risk": "Inline code execution in shell context",
        "fix": "Move code to a separate, inspectable script file",
    },
    {
        "regex": r"\bsudo\b",
        "category": "PRIV-ESC",
        "severity": Severity.CRITICAL,
        "risk": "Sudo invocation — privilege escalation attempt",
        "fix": "Remove sudo usage. Skills should never require elevated privileges",
    },
]

# =============================================================================
# PROMPT INJECTION PATTERNS (for markdown content)
# =============================================================================

PROMPT_INJECTION_PATTERNS = [
    {
        "regex": r"(?i)ignore\s+(?:all\s+)?(?:previous|prior|above)\s+instructions",
        "category": "PROMPT-OVERRIDE",
        "severity": Severity.CRITICAL,
        "risk": "Attempts to override system prompt and prior instructions",
        "fix": "Remove instruction override attempts",
    },
    {
        "regex": r"(?i)you\s+are\s+now\s+(?:a|an|the)\s+",
        "category": "PROMPT-OVERRIDE",
        "severity": Severity.CRITICAL,
        "risk": "Role hijacking — attempts to redefine the AI's identity",
        "fix": "Remove role redefinition. Skills should provide instructions, not identity changes",
    },
    {
        "regex": r"(?i)(?:disregard|forget|override)\s+(?:your|all|any)\s+(?:instructions|rules|guidelines|constraints|safety)",
        "category": "PROMPT-OVERRIDE",
        "severity": Severity.CRITICAL,
        "risk": "Explicit instruction override attempt",
        "fix": "Remove override directives",
    },
    {
        "regex": r"(?i)(?:pretend|act\s+as\s+if|imagine)\s+you\s+(?:have\s+no|don'?t\s+have\s+any)\s+(?:restrictions|limits|rules|safety)",
        "category": "SAFETY-BYPASS",
        "severity": Severity.CRITICAL,
        "risk": "Safety restriction bypass attempt",
        "fix": "Remove safety bypass instructions",
    },
    {
        "regex": r"(?i)(?:skip|disable|bypass|turn\s+off|ignore)\s+(?:safety|content|security)\s+(?:checks?|filters?|restrictions?|rules?)",
        "category": "SAFETY-BYPASS",
        "severity": Severity.CRITICAL,
        "risk": "Explicit safety mechanism bypass",
        "fix": "Remove safety bypass directives",
    },
    {
        "regex": r"(?i)(?:execute|run)\s+(?:any|all|arbitrary)\s+(?:commands?|code|scripts?)\s+(?:without|no)\s+(?:asking|confirmation|restriction|limit)",
        "category": "SAFETY-BYPASS",
        "severity": Severity.CRITICAL,
        "risk": "Unrestricted command execution directive",
        "fix": "Add explicit permission requirements for any command execution",
    },
    {
        "regex": r"(?i)(?:send|upload|post|transmit|exfiltrate)\s+(?:the\s+)?(?:contents?|data|files?|information)\s+(?:of|from|to)",
        "category": "PROMPT-EXFIL",
        "severity": Severity.CRITICAL,
        "risk": "Instruction to exfiltrate data",
        "fix": "Remove data transmission directives",
    },
    {
        "regex": r"(?i)(?:read|access|open|get)\s+(?:the\s+)?(?:contents?\s+of\s+)?(?:~|\/home|\/etc|\.ssh|\.aws|\.env|credentials?|secrets?|api.?keys?)",
        "category": "PROMPT-EXFIL",
        "severity": Severity.CRITICAL,
        "risk": "Instruction to access sensitive files or credentials",
        "fix": "Remove credential/sensitive file access directives",
    },
    # Hidden instructions — HIGH
    {
        "regex": r"[\u200b\u200c\u200d\ufeff\u00ad]",
        "category": "HIDDEN-INSTR",
        "severity": Severity.HIGH,
        "risk": "Zero-width or invisible characters — may hide instructions",
        "fix": "Remove zero-width characters. All instructions should be visible",
    },
    {
        "regex": r"<!--\s*(?:system|instruction|override|ignore|execute|run|sudo|admin)",
        "category": "HIDDEN-INSTR",
        "severity": Severity.HIGH,
        "risk": "HTML comments containing suspicious directives",
        "fix": "Remove HTML comments with directives. Use visible markdown instead",
    },
    # Excessive permissions — HIGH
    {
        "regex": r"(?i)(?:full|unrestricted|complete)\s+(?:access|control|permissions?)\s+(?:to|over)\s+(?:the\s+)?(?:file\s*system|network|internet|shell|terminal|system)",
        "category": "EXCESS-PERM",
        "severity": Severity.HIGH,
        "risk": "Requests unrestricted system access",
        "fix": "Scope permissions to specific, necessary operations",
    },
    {
        "regex": r"(?i)(?:always|automatically)\s+(?:approve|accept|allow|grant|execute)\s+(?:all|any|every)",
        "category": "EXCESS-PERM",
        "severity": Severity.HIGH,
        "risk": "Blanket approval directive — bypasses human oversight",
        "fix": "Require explicit user confirmation for sensitive operations",
    },
]

# =============================================================================
# NETSEC-SPECIFIC: Safety tier validation
# =============================================================================

# Commands that indicate device state modification (read-write)
# These only match inside fenced code blocks, not in decision tree prose.
# Patterns are intentionally strict to avoid false positives on words like
# "reload" appearing in diagnostic context (e.g., "show reload cause").
READWRITE_INDICATORS = [
    r"^\s*configure\s+terminal",
    r"^\s*conf\s+t\s*$",
    r"^\s*no\s+shutdown",
    r"^\s*shutdown\s*$",
    r"^\s*clear\s+counters",
    r"^\s*clear\s+ip\s+bgp",
    r"^\s*clear\s+ip\s+ospf",
    r"^\s*clear\s+ip\s+route",
    r"^\s*write\s+memory",
    r"^\s*copy\s+running-config",
    r"^\s*reload\s*$",
    r"^\s*request\s+system\s+reboot",
    r"^\s*set\s+firewall",
    r"^\s*set\s+security",
    r"^\s*commit\s*$",
    r"^\s*commit\s+confirmed",
    r"^\s*rollback\s+\d+",
    r"^\s*delete\s+configuration",
    r"^\s*ip\s+access-list",
    r"^\s*access-list\b.*\b(?:permit|deny)\b",
]


# =============================================================================
# SCANNER
# =============================================================================

CODE_EXTENSIONS = {".py", ".sh", ".bash", ".js", ".ts", ".mjs", ".cjs"}
MD_EXTENSIONS = {".md", ".mdx", ".markdown"}


def extract_code_blocks(content: str) -> list:
    """Extract fenced code blocks from markdown content."""
    blocks = []
    in_block = False
    block_lines = []
    block_start = 0

    for i, line in enumerate(content.split("\n"), 1):
        if line.strip().startswith("```") and not in_block:
            in_block = True
            block_start = i + 1
            block_lines = []
        elif line.strip().startswith("```") and in_block:
            in_block = False
            blocks.append((block_start, block_lines))
        elif in_block:
            block_lines.append((i, line))

    return blocks


def scan_file_code(filepath: Path, report: AuditReport):
    """Scan a code file for dangerous patterns."""
    try:
        content = filepath.read_text(encoding="utf-8", errors="replace")
    except Exception:
        return

    lines = content.split("\n")
    ext = filepath.suffix.lower()

    patterns = list(CODE_PATTERNS)
    if ext in {".sh", ".bash"}:
        patterns.extend(SHELL_PATTERNS)

    for i, line in enumerate(lines, 1):
        stripped = line.strip()
        # Skip comments
        if stripped.startswith("#") and ext in {".py", ".sh", ".bash"}:
            continue
        if stripped.startswith("//") and ext in {".js", ".ts", ".mjs", ".cjs"}:
            continue

        for pat in patterns:
            if re.search(pat["regex"], line):
                report.findings.append(
                    Finding(
                        severity=pat["severity"],
                        category=pat["category"],
                        file=str(filepath),
                        line=i,
                        pattern=stripped[:120],
                        risk=pat["risk"],
                        fix=pat["fix"],
                    )
                )

    report.scripts_scanned += 1


def scan_markdown_content(filepath: Path, report: AuditReport):
    """Scan markdown for prompt injection AND embedded shell commands."""
    try:
        content = filepath.read_text(encoding="utf-8", errors="replace")
    except Exception:
        return

    lines = content.split("\n")

    # Scan for prompt injection patterns
    for i, line in enumerate(lines, 1):
        for pat in PROMPT_INJECTION_PATTERNS:
            if re.search(pat["regex"], line):
                report.findings.append(
                    Finding(
                        severity=pat["severity"],
                        category=pat["category"],
                        file=str(filepath),
                        line=i,
                        pattern=line.strip()[:120],
                        risk=pat["risk"],
                        fix=pat["fix"],
                    )
                )

    # Scan code blocks for shell command patterns
    code_blocks = extract_code_blocks(content)
    for block_start, block_lines in code_blocks:
        for line_num, line in block_lines:
            for pat in SHELL_PATTERNS:
                if re.search(pat["regex"], line):
                    report.findings.append(
                        Finding(
                            severity=pat["severity"],
                            category=pat["category"],
                            file=str(filepath),
                            line=line_num,
                            pattern=line.strip()[:120],
                            risk=pat["risk"],
                            fix=pat["fix"],
                        )
                    )

    report.md_files_scanned += 1


def scan_safety_tier(skill_path: Path, report: AuditReport):
    """Validate that safety tier matches actual command usage."""
    skill_md = skill_path / "SKILL.md"
    if not skill_md.exists():
        return

    try:
        content = skill_md.read_text(encoding="utf-8", errors="replace")
    except Exception:
        return

    # Extract safety tier from frontmatter
    safety_tier = None
    in_frontmatter = False
    for line in content.split("\n"):
        if line.strip() == "---":
            if not in_frontmatter:
                in_frontmatter = True
                continue
            else:
                break
        if in_frontmatter and "safety:" in line:
            safety_tier = line.split("safety:")[-1].strip()
            break

    if not safety_tier:
        report.findings.append(
            Finding(
                severity=Severity.HIGH,
                category="SAFETY-TIER",
                file=str(skill_md),
                line=0,
                pattern="",
                risk="No safety tier declared in metadata",
                fix="Add metadata.safety: read-only or read-write to frontmatter",
            )
        )
        return

    # If declared read-only, check for write commands in code blocks
    if safety_tier == "read-only":
        code_blocks = extract_code_blocks(content)
        for block_start, block_lines in code_blocks:
            for line_num, line in block_lines:
                for pattern in READWRITE_INDICATORS:
                    if re.search(pattern, line, re.IGNORECASE):
                        report.findings.append(
                            Finding(
                                severity=Severity.HIGH,
                                category="SAFETY-MISMATCH",
                                file=str(skill_md),
                                line=line_num,
                                pattern=line.strip()[:120],
                                risk=f"Skill declared 'read-only' but contains write command matching '{pattern}'",
                                fix="Change safety tier to 'read-write' or remove the write command",
                            )
                        )


def scan_filesystem(skill_path: Path, report: AuditReport):
    """Scan skill directory structure for suspicious files."""
    for item in skill_path.rglob("*"):
        rel = item.relative_to(skill_path)
        rel_str = str(rel)

        if ".git" in rel.parts:
            continue

        report.files_scanned += 1

        # Hidden files
        if item.name.startswith(".") and item.name not in (
            ".gitignore", ".gitkeep", ".editorconfig",
        ):
            severity = Severity.CRITICAL if item.name == ".env" else Severity.HIGH
            report.findings.append(
                Finding(
                    severity=severity,
                    category="FS-HIDDEN",
                    file=rel_str,
                    line=0,
                    pattern=item.name,
                    risk=f"Hidden file '{item.name}' — may contain secrets or config",
                    fix="Remove hidden files from skill distribution",
                )
            )

        # Binary files
        if item.is_file() and item.suffix.lower() in (
            ".exe", ".dll", ".so", ".dylib", ".bin", ".elf",
            ".com", ".msi", ".deb", ".rpm", ".apk",
        ):
            report.findings.append(
                Finding(
                    severity=Severity.CRITICAL,
                    category="FS-BINARY",
                    file=rel_str,
                    line=0,
                    pattern=item.name,
                    risk="Binary executable in skill — high risk of malicious payload",
                    fix="Remove binary files. Skills should be text-only",
                )
            )

        # Extremely large files (>1MB)
        if item.is_file() and item.stat().st_size > 1_000_000:
            report.findings.append(
                Finding(
                    severity=Severity.HIGH,
                    category="FS-SIZE",
                    file=rel_str,
                    line=0,
                    pattern=f"{item.stat().st_size:,} bytes",
                    risk="Unusually large file — may contain embedded payloads",
                    fix="Review file contents. Skills typically contain small text files",
                )
            )


def audit_skill(skill_path: Path, strict: bool = False) -> AuditReport:
    """Run full security audit on a skill directory."""
    report = AuditReport(
        skill_name=skill_path.name,
        skill_path=str(skill_path),
    )

    if not skill_path.is_dir():
        report.findings.append(
            Finding(
                severity=Severity.CRITICAL,
                category="INVALID",
                file=str(skill_path),
                line=0,
                pattern="",
                risk="Path is not a directory",
                fix="Provide a valid skill directory path",
            )
        )
        return report

    # 1. Filesystem scan
    scan_filesystem(skill_path, report)

    # 2. Scan code files
    for code_file in skill_path.rglob("*"):
        if code_file.suffix.lower() in CODE_EXTENSIONS:
            scan_file_code(code_file, report)

    # 3. Scan markdown files (prompt injection + embedded commands)
    for md_file in skill_path.rglob("*"):
        if md_file.suffix.lower() in MD_EXTENSIONS:
            scan_markdown_content(md_file, report)

    # 4. Safety tier validation (netsec-specific)
    scan_safety_tier(skill_path, report)

    return report


def print_report(report: AuditReport, json_output: bool = False):
    """Print audit report to stdout."""
    if json_output:
        print(json.dumps(report.to_dict(), indent=2))
        return

    verdict_icons = {"PASS": "✅", "WARN": "⚠️", "FAIL": "❌"}
    icon = verdict_icons.get(report.verdict, "❓")

    print(f"\n{'='*60}")
    print(f"  Skill Security Audit: {report.skill_name}")
    print(f"{'='*60}")
    print(f"  Verdict: {icon} {report.verdict}")
    print(f"  Files scanned: {report.files_scanned}")
    print(f"  Scripts scanned: {report.scripts_scanned}")
    print(f"  Markdown files scanned: {report.md_files_scanned}")
    print(f"  Findings: {len(report.findings)}")
    print(f"    Critical: {report.critical_count}")
    print(f"    High:     {report.high_count}")
    print(f"    Info:     {report.info_count}")
    print(f"{'='*60}\n")

    if report.findings:
        for f in sorted(report.findings, key=lambda x: x.severity, reverse=True):
            label = SEVERITY_LABELS[f.severity]
            print(f"  {label}")
            print(f"    Category: {f.category}")
            print(f"    File:     {f.file}:{f.line}")
            print(f"    Pattern:  {f.pattern}")
            print(f"    Risk:     {f.risk}")
            print(f"    Fix:      {f.fix}")
            print()


def main():
    parser = argparse.ArgumentParser(description="Skill Security Auditor")
    parser.add_argument("path", help="Path to skill directory or parent directory")
    parser.add_argument("--strict", action="store_true",
                        help="Treat HIGH findings as failures")
    parser.add_argument("--json", action="store_true",
                        help="Output JSON format")
    args = parser.parse_args()

    target = Path(args.path)

    if not target.exists():
        print(f"Error: Path '{target}' does not exist", file=sys.stderr)
        sys.exit(1)

    # Determine if this is a single skill or a directory of skills
    skill_dirs = []
    if (target / "SKILL.md").exists():
        skill_dirs = [target]
    else:
        # Scan all subdirectories that contain SKILL.md
        for child in sorted(target.iterdir()):
            if child.is_dir() and (child / "SKILL.md").exists():
                skill_dirs.append(child)

    if not skill_dirs:
        print(f"Error: No SKILL.md found in '{target}'", file=sys.stderr)
        sys.exit(1)

    all_reports = []
    overall_exit = 0

    for skill_dir in skill_dirs:
        report = audit_skill(skill_dir, strict=args.strict)
        all_reports.append(report)

        if report.verdict == "FAIL":
            overall_exit = 1
        elif report.verdict == "WARN" and args.strict:
            overall_exit = max(overall_exit, 2)
        elif report.verdict == "WARN":
            overall_exit = max(overall_exit, 2)

    if args.json:
        if len(all_reports) == 1:
            print(json.dumps(all_reports[0].to_dict(), indent=2))
        else:
            combined = {
                "total_skills": len(all_reports),
                "overall_verdict": "FAIL" if any(r.verdict == "FAIL" for r in all_reports)
                    else "WARN" if any(r.verdict == "WARN" for r in all_reports)
                    else "PASS",
                "skills": [r.to_dict() for r in all_reports],
            }
            print(json.dumps(combined, indent=2))
    else:
        for report in all_reports:
            print_report(report)

        # Summary
        if len(all_reports) > 1:
            passed = sum(1 for r in all_reports if r.verdict == "PASS")
            warned = sum(1 for r in all_reports if r.verdict == "WARN")
            failed = sum(1 for r in all_reports if r.verdict == "FAIL")
            print(f"\n{'='*60}")
            print(f"  SUMMARY: {len(all_reports)} skills audited")
            print(f"  ✅ PASS: {passed}  ⚠️ WARN: {warned}  ❌ FAIL: {failed}")
            print(f"{'='*60}\n")

    sys.exit(min(overall_exit, 1) if args.strict else 0 if overall_exit != 1 else 1)


if __name__ == "__main__":
    main()
