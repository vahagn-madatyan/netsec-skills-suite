---
name: zscaler-zia-zpa-audit
description: >-
  Zscaler Internet Access and Private Access SASE policy audit — URL filtering
  policy analysis, SSL inspection coverage validation, Cloud Firewall rule
  assessment, ZPA application segment review, access policy evaluation, and
  connector health verification across ZIA and ZPA tenants.
license: Apache-2.0
metadata:
  safety: read-only
  author: network-security-skills-suite
  version: "1.0.0"
  openclaw: '{"emoji":"🌐","safetyTier":"read-only","requires":{"bins":[],"env":["ZIA_API_KEY","ZPA_CLIENT_ID","ZPA_CLIENT_SECRET"]},"tags":["zscaler","zia","zpa","sase","zero-trust"],"mcpDependencies":[],"egressEndpoints":["*.zscaler.net:443","*.private.zscaler.com:443","*.zscalerone.net:443"]}'
---

# Zscaler ZIA + ZPA SASE Policy Audit

Comprehensive policy audit of Zscaler Internet Access (ZIA) and Zscaler Private
Access (ZPA) SASE deployments. Unlike generic cloud security reviews that check
surface-level settings, this skill evaluates the full Zscaler security stack:
URL filtering rule effectiveness, Cloud Firewall rule ordering and shadow
detection, SSL inspection bypass gaps, DLP engine coverage, ZPA application
segment scoping, access policy posture enforcement, and connector health across
all connector groups.

Covers ZIA (cloud-delivered SWG, Cloud Firewall, Sandbox, DLP) and ZPA
(ZTNA application access, App Connectors, posture-based policy). For multi-tenant
deployments, audit each tenant independently and compare policy consistency.
Reference `references/api-reference.md` for ZIA and ZPA API endpoint details,
authentication flows, and rate limiting guidance.

## When to Use

- Post-change policy review after ZIA URL filtering, Cloud Firewall, or SSL
  inspection policy modifications
- Quarterly or annual compliance audit requiring documented evidence of SASE
  policy coverage and enforcement
- ZPA access policy gap analysis — identifying application segments reachable
  without posture verification or with overly broad access conditions
- SSL inspection bypass review — quantifying what percentage of traffic evades
  content inspection through do-not-inspect rules
- Connector health investigation — troubleshooting connectivity failures,
  version drift, or redundancy gaps across ZPA connector groups
- Tenant consolidation assessment — evaluating policy consistency before merging
  ZIA or ZPA tenants during M&A or organizational restructuring
- Zero trust maturity validation — measuring how effectively ZIA+ZPA enforce
  identity-aware, posture-verified, least-privilege access
- DLP coverage audit — verifying that data loss prevention engines and
  dictionaries cover regulated data types across all egress paths

## Prerequisites

- ZIA admin portal access or API key with read-only permissions (requires
  `ZIA_API_KEY` environment variable for API-driven audits)
- ZPA admin portal access or API credentials with read-only scope (`ZPA_CLIENT_ID`
  and `ZPA_CLIENT_SECRET` environment variables for API-driven audits)
- Knowledge of the ZIA cloud name (e.g., `zscaler.net`, `zscalerone.net`,
  `zscalertwo.net`, `zscloud.net`) for correct API base URL selection
- Understanding of the location and department hierarchy configured in ZIA —
  policies may be scoped to specific locations, sub-locations, or departments
- ZPA connector group topology — which connector groups serve which application
  segments, and expected redundancy (minimum 2 connectors per group)
- IdP integration details — which identity provider is federated with ZIA/ZPA,
  SCIM provisioning status, SAML attribute mappings
- Awareness of compliance requirements that dictate SSL inspection exemptions
  (healthcare, financial categories) and DLP dictionary requirements

## Procedure

Follow this audit flow sequentially. Each step builds on prior findings.
The procedure moves from tenant authentication through ZIA policy analysis,
then ZPA policy and connector assessment, concluding with identity and
posture integration validation.

### Step 1: Tenant Inventory and Authentication

Authenticate to both ZIA and ZPA APIs and collect tenant metadata.

**[ZIA] Authenticate and collect tenant info:**

```
POST https://zsapi.<cloud>/api/v1/authenticatedSession
{
  "apiKey": "<obfuscated_key>",
  "username": "<admin_user>",
  "password": "<admin_password>",
  "timestamp": "<timestamp>"
}
```

After authentication, retrieve tenant status:

```
GET /api/v1/status
```

Record the ZIA cloud name, activation status, and last policy push timestamp.
A stale policy push (>24 hours old) indicates changes pending activation.

**[ZPA] Authenticate via OAuth:**

```
POST https://config.<cloud>/signin
{
  "client_id": "<ZPA_CLIENT_ID>",
  "client_secret": "<ZPA_CLIENT_SECRET>"
}
```

Retrieve tenant profile:

```
GET /mgmtconfig/v1/admin/customers/{customerId}
```

Document both tenant IDs, admin roles used for the audit, and the API base
URLs. Verify that API credentials have read-only scope — write access is not
required and should not be used.

### Step 2: ZIA URL Filtering Policy Audit

Retrieve and evaluate all URL filtering rules.

```
[ZIA] GET /api/v1/urlFilteringRules
```

For each URL filtering rule, evaluate:

- **Rule ordering:** Rules are evaluated top-down. A broad allow rule above
  a specific block rule creates a bypass. Identify rules where ordering
  permits traffic that a later rule intends to deny.
- **Overly permissive allow rules:** Rules that allow all URL categories or
  allow categories like `Miscellaneous` or `Other` without justification.
  These categories contain unclassified sites and are high-risk.
- **Blocked category bypasses:** Check for rules that explicitly allow
  categories that the organization's acceptable use policy should block
  (e.g., `Peer-to-Peer`, `Anonymizer`, `Malware`).
- **Caution/Warn actions:** Rules using `CAUTION` action allow users to
  click through warnings. Verify this is intentional for each category.
- **Location and department scoping:** Rules scoped to `Any` location and
  `Any` department apply globally. Verify that global rules are intentional
  and not overly broad.

Retrieve URL category details for custom categories:

```
[ZIA] GET /api/v1/urlCategories
```

Check custom URL categories for stale entries, overly broad wildcard patterns
(e.g., `*.com`), and categories with no associated policy rule.

### Step 3: ZIA Cloud Firewall Rule Assessment

Retrieve the Cloud Firewall rule set:

```
[ZIA] GET /api/v1/firewallRules
```

Evaluate each firewall rule against these criteria:

- **Any-any rules:** Rules with source `Any`, destination `Any`, and
  application `Any` are effectively permit-all. Flag as Critical unless
  they are the explicit default-deny at the bottom of the rulebase.
- **Rule ordering and shadows:** A rule is shadowed when a preceding rule
  matches all the same traffic with equal or broader criteria. Shadowed
  rules never match and create audit confusion.
- **Source and destination granularity:** Rules should reference specific
  IP groups, locations, or departments — not `Any` for both source and
  destination. Evaluate whether address groups can narrow scope.
- **Application granularity:** Rules permitting entire application groups
  (e.g., `Web Browsing`) when only specific applications are needed.
- **Disabled rules:** Rules with `state: DISABLED` consume rulebase space.
  Flag for cleanup.
- **Logging:** Rules without logging enabled (`enableLogging: false`) create
  visibility gaps for incident investigation.

Retrieve network services for port/protocol mapping:

```
[ZIA] GET /api/v1/networkServices
```

Verify that custom network services use specific port ranges rather than
broad ranges (e.g., `1-65535`).

### Step 4: ZIA SSL Inspection Coverage

Retrieve SSL inspection rules:

```
[ZIA] GET /api/v1/sslInspectionRules
```

SSL inspection is critical for content-based threat detection. Without
inspection, ZIA cannot analyze encrypted payload content for malware,
data exfiltration, or policy violations.

Evaluate SSL inspection coverage:

- **Do-not-inspect rules:** Each rule that bypasses SSL inspection creates
  a blind spot. Quantify the percentage of traffic categories that are
  excluded from inspection.
- **Justified exclusions:** Financial and healthcare categories may require
  SSL bypass for compliance (PCI DSS, HIPAA). Verify that each exclusion
  has documented justification.
- **Certificate deployment:** SSL inspection requires the Zscaler root CA
  certificate installed on endpoints. Check if certificate deployment
  coverage is tracked and if exceptions exist.
- **Inspection by location:** Some locations may have SSL inspection
  disabled entirely. Identify locations without inspection coverage.

Retrieve the do-not-inspect URL categories:

```
[ZIA] GET /api/v1/urlCategories?type=URL_CATEGORY
```

Cross-reference do-not-inspect categories against the URL filtering policy
to identify categories that are both allowed and uninspected — these represent
the highest-risk blind spots.

### Step 5: ZIA DLP Policy Review

Retrieve DLP notification templates and engines:

```
[ZIA] GET /api/v1/dlpNotificationTemplates
[ZIA] GET /api/v1/dlpEngines
[ZIA] GET /api/v1/dlpDictionaries
```

Evaluate DLP coverage:

- **Engine activation:** Verify that DLP engines are enabled and actively
  scanning. Disabled engines provide no protection.
- **Dictionary coverage:** Check that dictionaries cover regulated data types
  required by compliance frameworks (PCI: credit card numbers, HIPAA: PHI
  identifiers, GDPR: EU personal data).
- **Custom dictionaries:** Review custom dictionaries for accuracy — overly
  broad patterns generate false positives, while overly narrow patterns
  miss data.
- **Notification templates:** Verify that DLP violation notifications are
  configured and that incident response contacts are current.
- **Egress channel coverage:** DLP should cover web traffic, SSL-inspected
  HTTPS, and cloud application uploads. Verify that SSL inspection bypasses
  do not create DLP blind spots.

### Step 6: ZPA Application Segment Review

Retrieve all application segments:

```
[ZPA] GET /mgmtconfig/v1/admin/customers/{customerId}/application
```

Application segments define what internal resources are accessible through
ZPA. Overly broad segments violate least-privilege principles.

Evaluate each application segment:

- **Wildcard domains:** Segments using `*.example.com` expose all subdomains.
  Verify that wildcard scope is intentional and not a shortcut for incomplete
  application discovery.
- **Large port ranges:** Segments with port ranges like `1-65535` or `1-1024`
  grant access to all services on target hosts. Narrow to specific
  application ports.
- **Double-encryption (bypass):** Check the `bypassType` field. Segments
  configured to bypass ZPA inspection may indicate misconfigurations or
  legacy workarounds.
- **Segment group assignment:** Every application segment should belong to a
  segment group for organized policy management. Unassigned segments are
  harder to audit and govern.
- **TCP/UDP protocol scope:** Segments allowing both TCP and UDP when the
  application only requires one protocol expand the attack surface.

Retrieve server groups to validate backend connectivity:

```
[ZPA] GET /mgmtconfig/v1/admin/customers/{customerId}/serverGroup
```

Cross-reference server groups with application segments to ensure each segment
has a valid server group with healthy connectors.

### Step 7: ZPA Access Policy Evaluation

Retrieve all access policies:

```
[ZPA] GET /mgmtconfig/v1/admin/customers/{customerId}/policySet/rules/policyType/ACCESS_POLICY
```

Access policies control who can reach application segments and under what
conditions. Evaluate:

- **Default-allow conditions:** Policies that allow access without specifying
  user groups, SCIM attributes, or posture profiles grant overly broad access.
  Every policy should have an explicit identity condition.
- **Missing posture profiles:** Access policies without posture profile
  requirements allow unmanaged or non-compliant devices to access internal
  applications. Flag policies that lack device trust verification.
- **Rule ordering:** Like firewall rules, access policies evaluate top-down.
  A broad allow above a restrictive rule bypasses the restriction.
- **App connector group assignment:** Policies must reference the correct
  connector group for the target application segment. Mismatched assignments
  cause connectivity failures.
- **SCIM attribute conditions:** Policies using SCIM attributes for
  department or group-based access should be validated against current
  IdP group membership.

Retrieve timeout and client forwarding policies:

```
[ZPA] GET /mgmtconfig/v1/admin/customers/{customerId}/policySet/rules/policyType/TIMEOUT_POLICY
[ZPA] GET /mgmtconfig/v1/admin/customers/{customerId}/policySet/rules/policyType/CLIENT_FORWARDING_POLICY
```

Check that timeout policies enforce session limits appropriate for the
application sensitivity and that client forwarding policies route traffic
through ZPA rather than direct internet access for internal applications.

### Step 8: ZPA Connector Health

Retrieve connector status across all connector groups:

```
[ZPA] GET /mgmtconfig/v1/admin/customers/{customerId}/connector
[ZPA] GET /mgmtconfig/v1/admin/customers/{customerId}/connectorGroup
```

App Connectors are the critical data path for ZPA. Evaluate:

- **Connector status:** Each connector should report `enabled` status. Flag
  connectors in `disabled` or `error` state.
- **Version currency:** Compare connector versions against the latest
  available release. Connectors more than two versions behind are at risk
  of missing security patches and feature compatibility.
- **Connector group redundancy:** Each connector group should have a minimum
  of two active connectors for high availability. Single-connector groups
  represent a single point of failure.
- **Connectivity to ZPA broker:** Verify that connectors maintain active
  connections to the ZPA broker infrastructure. Loss of broker connectivity
  prevents new session establishment.
- **Uptime:** Connectors with frequent restarts may indicate resource
  exhaustion, infrastructure instability, or provisioning issues.
- **Geographic distribution:** For globally distributed applications,
  verify that connector groups are deployed in proximity to application
  servers to minimize latency.

Retrieve provisioning keys for operational awareness:

```
[ZPA] GET /mgmtconfig/v1/admin/customers/{customerId}/associationType/{type}/provisioningKey
```

Check for expired or unused provisioning keys. Active keys that have not
been used to enroll connectors may indicate stalled deployments.

### Step 9: Identity and Posture Integration

Validate the IdP and posture configuration that underpins both ZIA and ZPA
policy enforcement.

**[ZPA] Retrieve IdP configuration:**

```
GET /mgmtconfig/v1/admin/customers/{customerId}/idp
```

Verify:
- IdP status is active and SAML/OIDC metadata is current
- SCIM provisioning is enabled and last sync is recent (within 24 hours)
- SAML attribute mapping includes required attributes for policy conditions
  (department, group, email)
- Certificate expiration dates — expired IdP certificates break authentication

**[ZPA] Retrieve posture profiles:**

```
GET /mgmtconfig/v1/admin/customers/{customerId}/posture
```

Evaluate posture profiles for completeness:
- **Device trust:** Profiles should verify device management enrollment
  (MDM/UEM), domain join status, or certificate presence
- **OS version requirements:** Minimum OS version checks prevent access from
  outdated, vulnerable endpoints
- **Disk encryption:** Requiring disk encryption (BitLocker, FileVault)
  protects data on lost or stolen devices
- **Firewall and antivirus:** Verifying endpoint security tool status ensures
  defense-in-depth at the device level

Cross-reference posture profiles against access policies from Step 7.
Identify access policies that do not require any posture profile — these
allow unverified devices to access internal applications.

**[ZIA] Retrieve location and user information:**

```
GET /api/v1/locations
GET /api/v1/departments
GET /api/v1/users
```

Verify that location hierarchy matches the organizational structure and that
department-scoped policies align with current HR department definitions.
Check for orphaned locations (no users assigned) or departments with no
associated policy rules.

## Threshold Tables

### URL Filtering Policy Coverage

| Metric | Normal | Warning | Critical |
|--------|--------|---------|----------|
| Categories with explicit action | >90% | 70-90% | <70% |
| Custom categories with stale entries (>180 days) | 0 | 1-5 | >5 |
| Allow rules for high-risk categories (Anonymizer, P2P) | 0 | 1-2 (justified) | >2 or unjustified |
| Rules with CAUTION action (click-through) | <5 | 5-10 | >10 |
| Rules scoped to Any/Any (location/department) | <3 | 3-5 | >5 |

### SSL Inspection Coverage

| Metric | Normal | Warning | Critical |
|--------|--------|---------|----------|
| Traffic categories inspected | >85% | 60-85% | <60% |
| Do-not-inspect rules | <5 (justified) | 5-15 | >15 |
| Locations with inspection disabled | 0 | 1-2 | >2 |
| Categories both allowed and uninspected | 0 | 1-3 | >3 |
| Certificate deployment coverage | >95% | 80-95% | <80% |

### Cloud Firewall Rule Health

| Metric | Normal | Warning | Critical |
|--------|--------|---------|----------|
| Total rule count | <100 | 100-250 | >250 |
| Any-any permit rules (non-default) | 0 | 1 | >1 |
| Shadowed (unreachable) rules | 0 | 1-5 | >5 |
| Rules without logging enabled | 0 | 1-10 | >10 |
| Disabled rules in rulebase | <5 | 5-15 | >15 |
| Network services with port range >1000 | 0 | 1-3 | >3 |

### ZPA Connector Health

| Metric | Normal | Warning | Critical |
|--------|--------|---------|----------|
| Connector status | All enabled | 1 disabled | >1 disabled or error |
| Version drift (versions behind latest) | 0-1 | 2 | >2 |
| Connector groups with single connector | 0 | 1-2 | >2 |
| Connectors with uptime <24 hours | 0 | 1 | >1 |
| Unused provisioning keys (>90 days) | 0 | 1-3 | >3 |

### Access Policy Posture Enforcement

| Metric | Normal | Warning | Critical |
|--------|--------|---------|----------|
| Access policies requiring posture profile | >90% | 60-90% | <60% |
| Policies with default-allow (no identity condition) | 0 | 1 | >1 |
| Application segments with wildcard domains | <10% | 10-30% | >30% |
| Segments with port range >100 ports | <10% | 10-25% | >25% |
| Access policies without SCIM group condition | <20% | 20-40% | >40% |

### DLP Coverage

| Metric | Normal | Warning | Critical |
|--------|--------|---------|----------|
| DLP engines enabled | All required | 1 disabled | >1 disabled |
| Regulated data types with dictionaries | 100% | 80-99% | <80% |
| SSL bypass categories without DLP | 0 | 1-3 | >3 |
| Custom dictionaries last reviewed (days) | <90 | 90-180 | >180 |
| Notification templates with valid contacts | 100% | >80% | <80% |

## Decision Trees

### ZIA Policy Gap Prioritization

```
Identified ZIA policy finding
├── SSL inspection gap?
│   ├── Yes → HIGH PRIORITY
│   │   ├── Traffic category both allowed and uninspected?
│   │   │   ├── Yes → CRITICAL: content-blind egress path
│   │   │   │   └── Add to SSL inspection policy or block category
│   │   │   └── No → Evaluate justification for bypass
│   │   │       ├── Compliance-required (financial/health) → Document exception
│   │   │       └── No justification → Add SSL inspection rule
│   │   └── Location with inspection fully disabled?
│   │       └── CRITICAL: entire site uninspected
│   │           └── Deploy Zscaler root CA and enable inspection
│   └── No → Check next finding type
│
├── Cloud Firewall any-any rule?
│   ├── Yes → CRITICAL
│   │   ├── Is this the default deny at rulebase bottom?
│   │   │   ├── Yes → Expected, verify action is BLOCK_DROP
│   │   │   └── No → Identify actual traffic requirements
│   │   │       └── Replace with specific source/dest/app rules
│   │   └── Logging enabled on the rule?
│   │       ├── No → Enable logging immediately for visibility
│   │       └── Yes → Use logs to identify traffic for rule narrowing
│   └── No → Check next finding type
│
├── URL filtering overly permissive?
│   ├── Allowing high-risk categories (Anonymizer, P2P, Malware)?
│   │   ├── Yes → HIGH: block or restrict immediately
│   │   └── No → Review category-by-category against AUP
│   └── Broad CAUTION rules allowing click-through?
│       └── MEDIUM: convert to BLOCK for non-business categories
│
├── DLP coverage gap?
│   ├── Regulated data type without dictionary?
│   │   └── HIGH: add dictionary for compliance requirement
│   └── DLP engine disabled?
│       └── CRITICAL: enable engine, verify no performance impact
│
└── Shadowed or disabled rules?
    └── LOW: cleanup for hygiene, schedule during maintenance window
```

### ZPA Access Policy Remediation

```
Identified ZPA access policy finding
├── Default-allow policy (no identity condition)?
│   ├── Yes → CRITICAL: unrestricted application access
│   │   ├── Identify intended user population
│   │   │   └── Add explicit SCIM group or IdP attribute condition
│   │   └── Add posture profile requirement
│   │       └── Minimum: device trust + OS version + disk encryption
│   └── No → Check posture enforcement
│
├── Missing posture profile on access policy?
│   ├── Yes → HIGH: unverified devices accessing internal apps
│   │   ├── Application sensitivity?
│   │   │   ├── High (finance, HR, admin) → Require full posture (trust + OS + AV + encryption)
│   │   │   ├── Medium (general business) → Require device trust + OS version
│   │   │   └── Low (informational) → Require device trust minimum
│   │   └── Posture profile exists but not bound?
│   │       ├── Yes → Bind existing profile to access policy
│   │       └── No → Create profile, test with monitor-only, then enforce
│   └── No → Check application segment scope
│
├── Overly broad application segment?
│   ├── Wildcard domain (*.example.com)?
│   │   ├── Intentional for entire subdomain tree?
│   │   │   ├── Yes → Document justification, ensure access policy is restrictive
│   │   │   └── No → Narrow to specific FQDNs
│   │   └── Large port range (>100 ports)?
│   │       ├── Application ports known?
│   │       │   ├── Yes → Narrow to specific ports
│   │       │   └── No → Use connector logs to identify actual ports in use
│   │       └── Both TCP and UDP when only one needed?
│   │           └── Restrict to required protocol
│   └── No → Check connector health
│
└── Connector group issue?
    ├── Single connector in group?
    │   └── HIGH: deploy second connector for redundancy
    ├── Connector version outdated?
    │   └── MEDIUM: schedule upgrade during maintenance window
    └── Connector in error state?
        └── CRITICAL: troubleshoot immediately
            ├── Check provisioning key validity
            ├── Verify network connectivity to ZPA broker
            └── Review connector resource utilization (CPU/memory/disk)
```

## Report Template

```
ZSCALER ZIA + ZPA SASE POLICY AUDIT REPORT
=============================================
ZIA Tenant: [cloud name / tenant ID]
ZPA Tenant: [customer ID]
ZIA Cloud: [zscaler.net / zscalerone.net / zscloud.net]
Audit Date: [timestamp]
Performed By: [operator/agent]
Assessment Scope: [full tenant / specific locations / specific app segments]

ZIA TENANT STATUS:
- Policy activation status: [activated / pending changes]
- Last policy push: [timestamp]
- Locations configured: [count]
- Departments configured: [count]

ZPA TENANT STATUS:
- Connector groups: [count]
- Active connectors: [n] / [total]
- Application segments: [count]
- Access policies: [count]

ZIA FINDINGS — URL FILTERING:
- Total URL filtering rules: [count]
- Categories with explicit action: [n] / [total] ([%])
- High-risk categories allowed: [list]
- Rules with CAUTION action: [count]
- Custom categories with stale entries: [count]
  1. [Severity] — [Description]
     Rule: [rule name / ID]
     Scope: [location] / [department]
     Issue: [specific problem]
     Recommendation: [specific remediation]

ZIA FINDINGS — CLOUD FIREWALL:
- Total firewall rules: [count]
- Any-any permit rules: [count]
- Shadowed rules: [count]
- Rules without logging: [count]
  1. [Severity] — [Description]
     Rule: [rule name / ID]
     Issue: [specific problem]
     Recommendation: [specific remediation]

ZIA FINDINGS — SSL INSPECTION:
- Traffic categories inspected: [n] / [total] ([%])
- Do-not-inspect rules: [count]
- Justified bypasses: [count] | Unjustified: [count]
- Locations without inspection: [list]
- Categories both allowed and uninspected: [list]
  1. [Severity] — [Description]
     Recommendation: [specific remediation]

ZIA FINDINGS — DLP:
- DLP engines active: [n] / [total]
- Regulated data types covered: [list]
- Regulated data types missing: [list]
- SSL bypass categories without DLP: [count]
  1. [Severity] — [Description]
     Recommendation: [specific remediation]

ZPA FINDINGS — APPLICATION SEGMENTS:
- Total application segments: [count]
- Segments with wildcard domains: [n] ([%])
- Segments with port ranges >100: [n] ([%])
- Segments without segment group: [count]
  1. [Severity] — [Description]
     Segment: [segment name]
     Domain/IP: [target]
     Ports: [port range]
     Recommendation: [specific remediation]

ZPA FINDINGS — ACCESS POLICIES:
- Total access policies: [count]
- Policies requiring posture profile: [n] / [total] ([%])
- Policies with default-allow: [count]
- Policies without SCIM group condition: [count]
  1. [Severity] — [Description]
     Policy: [policy name]
     Condition: [current condition]
     Recommendation: [specific remediation]

ZPA FINDINGS — CONNECTORS:
- Total connectors: [count]
- Connectors enabled: [n] | Disabled: [n] | Error: [n]
- Connector groups with single connector: [count]
- Connectors with outdated version: [count]
  1. [Severity] — [Description]
     Connector: [connector name]
     Group: [connector group]
     Status: [current status]
     Recommendation: [specific remediation]

IDENTITY AND POSTURE INTEGRATION:
- IdP status: [active / inactive]
- SCIM last sync: [timestamp]
- SAML certificate expiration: [date]
- Posture profiles configured: [count]
- Posture checks enforced: [device trust / OS / encryption / AV]

SEVERITY SUMMARY:
- Critical: [count]
- High: [count]
- Medium: [count]
- Low: [count]

REMEDIATION ROADMAP:
  Phase 1 — Immediate (0-7 days):
    - [Critical findings requiring immediate action]

  Phase 2 — Short-term (7-30 days):
    - [High findings — policy tightening, posture enforcement]

  Phase 3 — Medium-term (30-90 days):
    - [Medium findings — segment narrowing, connector upgrades]

  Phase 4 — Ongoing:
    - [Low findings — cleanup, documentation, process improvements]

NEXT AUDIT: [based on findings — Critical: 30d, High: 90d, clean: 180d]
```

## Troubleshooting

### API Rate Limiting

Zscaler APIs enforce rate limits that vary by endpoint and tenant tier.
ZIA API calls are typically limited to 40 requests per 10-second window.
ZPA API calls are limited per endpoint category. If you receive HTTP 429
responses, implement exponential backoff starting at 1 second. For large
tenants with many rules, batch retrieval endpoints and avoid polling in
tight loops. Use `GET` bulk endpoints (e.g., `/urlFilteringRules` returns
all rules in one call) rather than individual rule retrieval where possible.

### Multi-Tenant Visibility

Organizations with multiple ZIA or ZPA tenants must audit each tenant
independently — there is no cross-tenant API. Maintain separate API
credentials for each tenant and document which tenant each finding belongs
to. For Zscaler Cloud Connector or Branch Connector deployments, verify
that the tenant ID in connector configuration matches the audited tenant.

### Sub-Location vs Location Hierarchy

ZIA policies can be scoped to locations and sub-locations. Sub-locations
inherit parent location settings unless explicitly overridden. When auditing
URL filtering or firewall rules scoped to a location, verify whether
sub-locations have overriding rules that change the effective policy.
Retrieve sub-locations explicitly:

```
[ZIA] GET /api/v1/locations/{locationId}/sublocations
```

A common misconfiguration is applying a restrictive policy to a parent
location while a sub-location override permits the same traffic category.

### ZPA Connector Provisioning Key Issues

Connectors require a valid provisioning key for initial enrollment. Common
issues include:

- **Expired provisioning key:** Keys have a configurable expiration. Expired
  keys prevent new connector enrollment but do not affect already-enrolled
  connectors.
- **Max usage reached:** Each key has a maximum usage count. If all uses are
  consumed, new connectors cannot enroll with that key.
- **Wrong association type:** Provisioning keys are scoped to connector groups
  or service edges. Using a key for the wrong association type fails silently.

Retrieve and validate provisioning keys:

```
[ZPA] GET /mgmtconfig/v1/admin/customers/{customerId}/associationType/CONNECTOR_GRP/provisioningKey
```

### IdP and SCIM Sync Delays

SCIM provisioning syncs user and group data from the IdP to ZPA. Sync
delays cause access policy conditions based on SCIM groups to evaluate
against stale data. Check the last sync timestamp in the IdP configuration.
If sync is delayed more than 24 hours:

- Verify SCIM bearer token has not expired
- Check IdP-side SCIM provisioning logs for errors
- Validate that the SCIM endpoint URL in the IdP matches the ZPA tenant

For ZIA, user and department synchronization depends on the configured
authentication method (SAML, Kerberos, or hosted DB). Verify that the
user database reflects current organizational structure — stale departments
in ZIA cause policy scoping errors.

### Cloud Firewall Rule Count Limits

ZIA tenants have a maximum number of Cloud Firewall rules that varies by
subscription tier. Approaching the rule limit prevents new rule creation
and may force rule consolidation. Check current rule count against the
tenant limit and plan consolidation if utilization exceeds 80%. Consolidation
strategies include merging rules with identical actions and overlapping
criteria, replacing multiple IP-based rules with IP groups, and removing
shadowed or disabled rules.
