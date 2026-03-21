# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| latest  | :white_check_mark: |

## Reporting a Vulnerability

If you discover a security vulnerability in this project, please report it
responsibly. **Do not open a public GitHub issue for security vulnerabilities.**

### How to Report

- **Email:** [me@vahagn.dev](mailto:me@vahagn.dev)
- **Subject line:** `[SECURITY] netsec-skills-suite — <brief description>`

### What to Include

- A description of the vulnerability and its potential impact
- Steps to reproduce the issue
- Any proof-of-concept code or screenshots
- Your suggested fix (if applicable)

### Disclosure Timeline

- **Acknowledgement:** We will acknowledge receipt of your report within
  **48 hours**.
- **Initial assessment:** We will provide an initial assessment within
  **7 days**.
- **Resolution target:** We aim to resolve confirmed vulnerabilities within
  **90 days** of disclosure.
- **Public disclosure:** We will coordinate with you on public disclosure
  timing after a fix is released.

### Scope

The following are in scope for security reports:

- Prompt injection vectors in skill definitions
- Command injection or code execution risks in skill procedures
- Credential harvesting or data exfiltration patterns
- Obfuscated or encoded payloads within skill files
- Vulnerabilities in CI/CD workflows (GitHub Actions)
- Misconfigured permissions or secrets exposure

### Out of Scope

- Skills functioning as designed (e.g., `config-management` performing
  writes when explicitly marked `read-write`)
- Issues in third-party dependencies (report those upstream)
- Social engineering attacks

## Security Measures

This repository employs the following security controls:

- **SkillCheck Security Audit** — automated scanning for prompt injection,
  command injection, credential harvesting, and obfuscation
- **VirusTotal Scanning** — all release artifacts scanned via VirusTotal API
- **OpenSSF Scorecard** — continuous supply chain security assessment
- **CodeQL Analysis** — GitHub Advanced Security static analysis
- **Branch Protection** — required PR reviews, no force pushes, deletion
  prevention
- **SHA-Pinned Actions** — all GitHub Actions pinned to immutable commit SHAs
- **Dependabot** — automated dependency update monitoring
