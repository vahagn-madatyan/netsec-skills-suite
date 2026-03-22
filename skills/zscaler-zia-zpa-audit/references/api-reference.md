# Zscaler ZIA + ZPA API Reference

API endpoint reference for auditing Zscaler Internet Access (ZIA) and Zscaler
Private Access (ZPA) deployments. Covers authentication flows, policy retrieval
endpoints, connector management, and rate limiting. All endpoints are read-only
operations suitable for audit use.

## Authentication

### ZIA API Authentication

ZIA uses session-based authentication with an obfuscated API key. The API key
must be obfuscated using a timestamp-based algorithm before submission.

**API key obfuscation algorithm:**
1. Get current Unix timestamp in milliseconds
2. Convert timestamp to string
3. Extract the last 6 digits of the timestamp string
4. For each digit n at position i, take character at index n from the API key
5. Append the extracted characters to form the obfuscation result
6. Concatenate the obfuscation result with the timestamp

**Authentication request:**

```
POST https://zsapi.<cloud>/api/v1/authenticatedSession
Content-Type: application/json

{
  "apiKey": "<obfuscated_api_key>",
  "username": "<admin_email>",
  "password": "<admin_password>",
  "timestamp": "<timestamp_ms>"
}
```

**Response:** Sets a `JSESSIONID` cookie used for subsequent requests.

**Cloud-specific base URLs:**

| Cloud | API Base URL |
|-------|-------------|
| zscaler.net | `https://zsapi.zscaler.net` |
| zscalerone.net | `https://zsapi.zscalerone.net` |
| zscalertwo.net | `https://zsapi.zscalertwo.net` |
| zscloud.net | `https://zsapi.zscloud.net` |
| zscalerthree.net | `https://zsapi.zscalerthree.net` |
| zscalerbeta.net | `https://zsapi.zscalerbeta.net` |
| zscalergov.net | `https://zsapi.zscalergov.net` |

**Session lifecycle:**
- Sessions expire after 30 minutes of inactivity
- Maximum session duration is 1 hour
- Call `DELETE /api/v1/authenticatedSession` to end session explicitly
- Only one active session per admin is permitted

### ZPA API Authentication

ZPA uses OAuth 2.0 client credentials flow. API credentials are created in
the ZPA Admin Portal under Administration > API Keys.

**Token request:**

```
POST https://config.<cloud>/signin
Content-Type: application/x-www-form-urlencoded

client_id=<ZPA_CLIENT_ID>&client_secret=<ZPA_CLIENT_SECRET>
```

**Response:**

```json
{
  "token_type": "Bearer",
  "access_token": "<jwt_token>"
}
```

**Usage:** Include the token in subsequent requests:

```
Authorization: Bearer <access_token>
```

**ZPA API base URLs:**

| Cloud | Config API Base URL |
|-------|-------------------|
| Production (US) | `https://config.private.zscaler.com` |
| Production (EU) | `https://config.zscaler.com` |
| Beta | `https://config.zpabeta.net` |
| Gov | `https://config.zpagov.net` |

**Token lifecycle:**
- Tokens are valid for 3600 seconds (1 hour)
- Re-authenticate to obtain a new token before expiration
- No refresh token mechanism — request a new token directly

## ZIA Policy Endpoints

### URL Filtering

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/v1/urlFilteringRules` | GET | Retrieve all URL filtering rules |
| `/api/v1/urlFilteringRules/{ruleId}` | GET | Retrieve a specific URL filtering rule |
| `/api/v1/urlCategories` | GET | List all URL categories (predefined + custom) |
| `/api/v1/urlCategories/{categoryId}` | GET | Retrieve a specific URL category |
| `/api/v1/urlCategories?type=URL_CATEGORY` | GET | List predefined URL categories only |
| `/api/v1/urlCategories?type=CUSTOM` | GET | List custom URL categories only |

**Key response fields for `urlFilteringRules`:**

| Field | Type | Description |
|-------|------|-------------|
| `id` | integer | Rule ID |
| `name` | string | Rule name |
| `order` | integer | Rule evaluation order (1 = first) |
| `state` | string | `ENABLED` or `DISABLED` |
| `action` | string | `ALLOW`, `BLOCK`, `CAUTION`, `ISOLATE` |
| `urlCategories` | array | URL category names this rule applies to |
| `locations` | array | Location objects this rule is scoped to |
| `departments` | array | Department objects this rule is scoped to |
| `groups` | array | User group objects this rule is scoped to |
| `blockOverride` | boolean | Whether users can request override |

### Cloud Firewall

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/v1/firewallRules` | GET | Retrieve all Cloud Firewall rules |
| `/api/v1/firewallRules/{ruleId}` | GET | Retrieve a specific firewall rule |
| `/api/v1/networkServices` | GET | List all network service definitions |
| `/api/v1/networkServices/{serviceId}` | GET | Retrieve a specific network service |
| `/api/v1/networkServiceGroups` | GET | List network service groups |
| `/api/v1/ipSourceGroups` | GET | List IP source groups |
| `/api/v1/ipDestinationGroups` | GET | List IP destination groups |

**Key response fields for `firewallRules`:**

| Field | Type | Description |
|-------|------|-------------|
| `id` | integer | Rule ID |
| `name` | string | Rule name |
| `order` | integer | Rule evaluation order |
| `state` | string | `ENABLED` or `DISABLED` |
| `action` | string | `ALLOW`, `BLOCK_DROP`, `BLOCK_RESET`, `BLOCK_ICMP` |
| `srcIpGroups` | array | Source IP group objects |
| `destIpGroups` | array | Destination IP group objects |
| `nwServices` | array | Network service objects (port/protocol) |
| `nwApplications` | array | Network application objects |
| `locations` | array | Location objects this rule is scoped to |
| `departments` | array | Department objects |
| `enableLogging` | boolean | Whether logging is active for this rule |

### SSL Inspection

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/v1/sslInspectionRules` | GET | Retrieve all SSL inspection rules |
| `/api/v1/sslInspectionRules/{ruleId}` | GET | Retrieve a specific SSL inspection rule |

**Key response fields for `sslInspectionRules`:**

| Field | Type | Description |
|-------|------|-------------|
| `id` | integer | Rule ID |
| `name` | string | Rule name |
| `order` | integer | Rule evaluation order |
| `state` | string | `ENABLED` or `DISABLED` |
| `action` | string | `INSPECT` or `DO_NOT_INSPECT` |
| `urlCategories` | array | URL categories subject to this rule |
| `locations` | array | Location scoping |
| `cloudApplications` | array | Cloud apps subject to this rule |

### DLP

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/v1/dlpEngines` | GET | List all DLP engines |
| `/api/v1/dlpDictionaries` | GET | List all DLP dictionaries |
| `/api/v1/dlpDictionaries/{dictId}` | GET | Retrieve a specific DLP dictionary |
| `/api/v1/dlpNotificationTemplates` | GET | List DLP notification templates |
| `/api/v1/dlpExactDataMatchSchemas` | GET | List EDM schemas |

**Key response fields for `dlpDictionaries`:**

| Field | Type | Description |
|-------|------|-------------|
| `id` | integer | Dictionary ID |
| `name` | string | Dictionary name |
| `dictionaryType` | string | `PATTERNS_AND_PHRASES` or `EXACT_DATA_MATCH` |
| `customPhraseMatchType` | string | `MATCH_ALL_CUSTOM_PHRASE_PATTERN_DICTIONARY` or `MATCH_ANY` |
| `phrases` | array | Pattern/phrase entries in the dictionary |
| `custom` | boolean | Whether this is a custom dictionary |

### Locations and Users

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/v1/locations` | GET | List all locations |
| `/api/v1/locations/{locationId}` | GET | Retrieve a specific location |
| `/api/v1/locations/{locationId}/sublocations` | GET | List sub-locations |
| `/api/v1/departments` | GET | List all departments |
| `/api/v1/users` | GET | List users (paginated) |
| `/api/v1/users?page={n}&pageSize={size}` | GET | Paginated user retrieval |

**Key response fields for `locations`:**

| Field | Type | Description |
|-------|------|-------------|
| `id` | integer | Location ID |
| `name` | string | Location name |
| `parentId` | integer | Parent location ID (0 if top-level) |
| `sslScanEnabled` | boolean | Whether SSL inspection is active |
| `surrogateIP` | boolean | IP surrogate authentication enabled |
| `authRequired` | boolean | User authentication required |
| `vpnCredentials` | array | VPN credentials associated |

### Tenant Status

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/v1/status` | GET | Tenant activation status |
| `/api/v1/status/activation` | PUT | Activate pending changes (write — audit only) |

## ZPA Policy Endpoints

### Application Segments

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/mgmtconfig/v1/admin/customers/{custId}/application` | GET | List all application segments |
| `/mgmtconfig/v1/admin/customers/{custId}/application/{appId}` | GET | Retrieve a specific app segment |
| `/mgmtconfig/v1/admin/customers/{custId}/application/segmentGroup` | GET | List segment groups |

**Key response fields for application segments:**

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Application segment ID |
| `name` | string | Segment name |
| `domainNames` | array | Target FQDNs or wildcard domains |
| `tcpPortRanges` | array | TCP port range pairs `[from, to]` |
| `udpPortRanges` | array | UDP port range pairs `[from, to]` |
| `bypassType` | string | `NEVER` (always inspect) or `ALWAYS` (bypass) |
| `doubleEncrypt` | boolean | Whether double encryption is enabled |
| `segmentGroupId` | string | Associated segment group ID |
| `serverGroups` | array | Backend server group references |
| `enabled` | boolean | Segment active status |

### Access Policies

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/mgmtconfig/v1/admin/customers/{custId}/policySet/rules/policyType/ACCESS_POLICY` | GET | List access policy rules |
| `/mgmtconfig/v1/admin/customers/{custId}/policySet/rules/policyType/TIMEOUT_POLICY` | GET | List timeout policy rules |
| `/mgmtconfig/v1/admin/customers/{custId}/policySet/rules/policyType/CLIENT_FORWARDING_POLICY` | GET | List client forwarding rules |
| `/mgmtconfig/v1/admin/customers/{custId}/policySet/rules/policyType/ISOLATION_POLICY` | GET | List browser isolation rules |

**Key response fields for access policy rules:**

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Policy rule ID |
| `name` | string | Rule name |
| `action` | string | `ALLOW` or `DENY` |
| `policyType` | string | Policy type (ACCESS_POLICY, TIMEOUT, etc.) |
| `conditions` | array | Rule conditions (operands for identity, posture, app) |
| `appConnectorGroups` | array | Connector groups assigned |
| `appServerGroups` | array | Server groups assigned |
| `customMsg` | string | Custom deny message |
| `operator` | string | Condition operator (`AND` or `OR`) |

**Condition operand types:**

| Object Type | Description |
|-------------|-------------|
| `APP` | Application segment match |
| `APP_GROUP` | Application segment group match |
| `SAML` | SAML attribute condition |
| `SCIM` | SCIM attribute condition |
| `SCIM_GROUP` | SCIM group membership condition |
| `POSTURE` | Posture profile condition |
| `TRUSTED_NETWORK` | Trusted network condition |
| `CLIENT_TYPE` | Client type (ZPA Client Connector, Browser Access, etc.) |

### Connectors

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/mgmtconfig/v1/admin/customers/{custId}/connector` | GET | List all connectors |
| `/mgmtconfig/v1/admin/customers/{custId}/connector/{connId}` | GET | Retrieve a specific connector |
| `/mgmtconfig/v1/admin/customers/{custId}/connectorGroup` | GET | List all connector groups |
| `/mgmtconfig/v1/admin/customers/{custId}/connectorGroup/{grpId}` | GET | Retrieve a specific connector group |

**Key response fields for connectors:**

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Connector ID |
| `name` | string | Connector name |
| `enabled` | boolean | Connector enabled state |
| `currentVersion` | string | Running software version |
| `expectedVersion` | string | Expected (latest) version |
| `upgradeAttempt` | string | Last upgrade attempt timestamp |
| `connectorGroupId` | string | Parent connector group |
| `privateIp` | string | Connector private IP address |
| `publicIp` | string | Connector public IP address |
| `platform` | string | Deployment platform (VMware, AWS, Azure, etc.) |
| `runtimeOS` | string | Operating system |
| `lastBrokerConnectTime` | string | Last successful broker connection |

### Server Groups

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/mgmtconfig/v1/admin/customers/{custId}/serverGroup` | GET | List all server groups |
| `/mgmtconfig/v1/admin/customers/{custId}/serverGroup/{grpId}` | GET | Retrieve a specific server group |

**Key response fields for server groups:**

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Server group ID |
| `name` | string | Server group name |
| `enabled` | boolean | Group active status |
| `dynamicDiscovery` | boolean | Dynamic server discovery enabled |
| `connectorGroups` | array | Associated connector groups |
| `servers` | array | Backend server list |
| `appConnectorGroups` | array | Connector groups for this server group |

### Identity and Posture

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/mgmtconfig/v1/admin/customers/{custId}/idp` | GET | List configured IdPs |
| `/mgmtconfig/v1/admin/customers/{custId}/idp/{idpId}` | GET | Retrieve a specific IdP configuration |
| `/mgmtconfig/v1/admin/customers/{custId}/posture` | GET | List posture profiles |
| `/mgmtconfig/v1/admin/customers/{custId}/posture/{postureId}` | GET | Retrieve a specific posture profile |
| `/mgmtconfig/v1/admin/customers/{custId}/samlAttribute` | GET | List SAML attributes |
| `/mgmtconfig/v1/admin/customers/{custId}/scimAttributeHeader` | GET | List SCIM attribute headers |

**Key response fields for IdP configuration:**

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | IdP configuration ID |
| `name` | string | IdP display name |
| `idpType` | string | `USER`, `ADMIN`, or `USER_AND_ADMIN` |
| `ssoType` | array | SSO types (`SAML`, `OIDC`) |
| `domainList` | array | Domains associated with this IdP |
| `enableScimBasedPolicy` | boolean | SCIM-based policy enabled |
| `scimEnabled` | boolean | SCIM provisioning active |
| `loginUrl` | string | IdP login URL |
| `certificates` | array | SAML signing certificates (check expiration) |

### Provisioning Keys

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/mgmtconfig/v1/admin/customers/{custId}/associationType/CONNECTOR_GRP/provisioningKey` | GET | Connector provisioning keys |
| `/mgmtconfig/v1/admin/customers/{custId}/associationType/SERVICE_EDGE_GRP/provisioningKey` | GET | Service Edge provisioning keys |

**Key response fields:**

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Provisioning key ID |
| `name` | string | Key name |
| `enabled` | boolean | Key active state |
| `maxUsage` | integer | Maximum enrollment count |
| `usageCount` | integer | Current usage count |
| `expirationInEpochSec` | string | Key expiration timestamp |
| `associationType` | string | `CONNECTOR_GRP` or `SERVICE_EDGE_GRP` |

## Rate Limiting

### ZIA Rate Limits

| Scope | Limit | Window |
|-------|-------|--------|
| General API calls | 40 requests | 10 seconds |
| Authentication | 5 attempts | 60 seconds |
| Bulk export endpoints | 10 requests | 60 seconds |

**Rate limit response:** HTTP 429 with `Retry-After` header indicating
seconds until the rate limit resets. Implement exponential backoff starting
at 1 second with a maximum of 30 seconds between retries.

### ZPA Rate Limits

| Scope | Limit | Window |
|-------|-------|--------|
| GET requests (read) | 20 requests | 10 seconds |
| POST/PUT/DELETE (write) | 10 requests | 10 seconds |
| Authentication | 5 attempts | 60 seconds |

**Rate limit response:** HTTP 429. ZPA does not provide a `Retry-After`
header — implement client-side backoff with 2-second initial delay,
doubling on each retry up to 30 seconds maximum.

### Pagination

ZPA endpoints that return lists support pagination:

```
GET /mgmtconfig/v1/admin/customers/{custId}/application?page=1&pagesize=500
```

| Parameter | Default | Maximum | Description |
|-----------|---------|---------|-------------|
| `page` | 1 | N/A | Page number (1-indexed) |
| `pagesize` | 20 | 500 | Results per page |

Response includes `totalPages` for iteration control. Always iterate
through all pages to get the complete data set for audit purposes.

ZIA endpoints generally return all results in a single response for
policy rules (URL filtering, firewall, SSL inspection). User endpoints
support pagination with `page` and `pageSize` query parameters.
