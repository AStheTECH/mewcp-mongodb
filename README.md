**Manage MongoDB Atlas projects and clusters through the Atlas Administration API.**

A Model Context Protocol (MCP) server that exposes MongoDB Atlas's Administration API for managing Atlas projects (groups) and reading Atlas cluster configuration and status.


## Overview

The mewcp-mongodb MCP Server provides direct, authenticated access to the MongoDB Atlas Administration API:

- Full lifecycle management of Atlas projects (groups) — create, read, list, update, and delete
- Read access to cluster configuration and status, scoped to a single project or aggregated across every project the service account can access
- Authenticates as a MongoDB Atlas service account using OAuth 2.0 client-credentials and makes raw HTTP calls directly to the Atlas Administration API, since no official Atlas Python SDK exists

Perfect for:

- Automating project provisioning and teardown across a MongoDB Cloud organization
- Auditing cluster configuration, version, and status across one or many projects
- Building agents and workflows that need programmatic visibility into Atlas infrastructure


## Tools

### Projects

<details>
<summary><code>create_project</code> — Create a new Atlas project (group) in an organization</summary>

Creates one new project inside a MongoDB Cloud organization and returns the created project's details, including its generated `id`.

**Inputs:**
```
- `name` (string, required) — Human-readable label that identifies the project, as a plain string 1-64 characters (e.g. 'Production').
- `orgId` (string, required) — Unique 24-hexadecimal digit string that identifies the MongoDB Cloud organization the project belongs to (e.g. '32b6e34b3d91647abb20e7b8').
- `regionUsageRestrictions` (string, optional, default: null) — Atlas for Government only — restricts available regions for the project. One of 'COMMERCIAL_FEDRAMP_REGIONS_ONLY' or 'GOV_REGIONS_ONLY'. In commercial Atlas this field is rejected by the API. Optional, defaults to 'COMMERCIAL_FEDRAMP_REGIONS_ONLY' on the server.
- `tags` (array, optional, default: null) — List of key-value pairs for tagging and categorizing the project, e.g. [{'key': 'env', 'value': 'prod'}]. Each key and value must be 1-255 characters. Optional.
- `withDefaultAlertsSettings` (boolean, optional, default: null) — Whether to create the project with default alert settings. Optional, defaults to true on the server.
- `projectOwnerId` (string, optional, default: null) — Unique 24-hexadecimal digit string that identifies the MongoDB Cloud user to grant the Project Owner role on the new project. Overrides the default of the oldest Organization Owner. Optional — sent as a query parameter.
```

**Output `data` schema:**

```typescript
{
  id: string | null;
  name: string | null;
  orgId: string | null;
  clusterCount: number | null;
  created: string | null;
  regionUsageRestrictions: string | null;
  withDefaultAlertsSettings: boolean | null;
  tags: {
    key: string | null;
    value: string | null;
  }[] | null;
  links: {
    href: string | null;
    rel: string | null;
  }[] | null;
} | null
```

</details>


<details>
<summary><code>get_project</code> — Fetch one Atlas project by ID</summary>

Returns one project by its unique ID, including cluster count, tags, and organization details.

**Inputs:**
```
- `groupId` (string, required) — Unique 24-hexadecimal digit string that identifies the project (e.g. '32b6e34b3d91647abb20e7b8'). Groups and projects are synonymous terms — your group id is the same as your project id.
```

**Output `data` schema:**

```typescript
{
  id: string | null;
  name: string | null;
  orgId: string | null;
  clusterCount: number | null;
  created: string | null;
  regionUsageRestrictions: string | null;
  withDefaultAlertsSettings: boolean | null;
  tags: {
    key: string | null;
    value: string | null;
  }[] | null;
  links: {
    href: string | null;
    rel: string | null;
  }[] | null;
} | null
```

</details>


<details>
<summary><code>list_projects</code> — List all Atlas projects the service account can access</summary>

Returns all projects to which the requesting service account has access.

**Inputs:**
```
- `includeCount` (boolean, optional, default: null) — Whether the response includes the total number of items (totalCount). Optional, defaults to true on the server.
- `itemsPerPage` (integer, optional, default: null) — Number of items to return per page (1-500). Optional, defaults to 100 on the server.
- `pageNum` (integer, optional, default: null) — Page number of the results to return, minimum 1. Optional, defaults to 1 on the server.
```

**Output `data` schema:**

```typescript
{
  results: {
    id: string | null;
    name: string | null;
    orgId: string | null;
    clusterCount: number | null;
    created: string | null;
    regionUsageRestrictions: string | null;
    withDefaultAlertsSettings: boolean | null;
    tags: {
      key: string | null;
      value: string | null;
    }[] | null;
    links: {
      href: string | null;
      rel: string | null;
    }[] | null;
  }[];
  totalCount: number | null;
  links: {
    href: string | null;
    rel: string | null;
  }[] | null;
} | null
```

</details>


<details>
<summary><code>update_project</code> — Update an Atlas project's name, tags, or alert settings</summary>

Updates the name, tags, or default alert settings of one project. Only the fields you provide are changed — others keep their current value. NOTE: this overwrites the current field values — the original state is not stored after the call. The response includes both the before and after state so you have a full record of what changed.

**Inputs:**
```
- `groupId` (string, required) — Unique 24-hexadecimal digit string that identifies the project to update (e.g. '32b6e34b3d91647abb20e7b8').
- `name` (string, optional, default: null) — New human-readable label for the project. Optional — leave unset to keep the current name.
- `tags` (array, optional, default: null) — New list of key-value pairs for tagging and categorizing the project, e.g. [{'key': 'env', 'value': 'staging'}]. Replaces the current tags entirely. Optional — leave unset to keep the current tags.
- `withDefaultAlertsSettings` (boolean, optional, default: null) — Whether the project can automatically create default alerts. Optional — leave unset to keep the current setting.
```

**Output `data` schema:**

```typescript
{
  before: {
    id: string | null;
    name: string | null;
    orgId: string | null;
    clusterCount: number | null;
    created: string | null;
    regionUsageRestrictions: string | null;
    withDefaultAlertsSettings: boolean | null;
    tags: {
      key: string | null;
      value: string | null;
    }[] | null;
    links: {
      href: string | null;
      rel: string | null;
    }[] | null;
  };
  after: {
    id: string | null;
    name: string | null;
    orgId: string | null;
    clusterCount: number | null;
    created: string | null;
    regionUsageRestrictions: string | null;
    withDefaultAlertsSettings: boolean | null;
    tags: {
      key: string | null;
      value: string | null;
    }[] | null;
    links: {
      href: string | null;
      rel: string | null;
    }[] | null;
  };
} | null
```

</details>


<details>
<summary><code>delete_project</code> — Permanently delete an Atlas project (destructive)</summary>

DESTRUCTIVE — REQUIRES EXPLICIT USER CONFIRMATION BEFORE CALLING. Permanently removes one project, which must have no clusters. This action is irreversible — the project and its configuration cannot be recovered. NEVER call this tool autonomously or as part of an automated flow. You MUST stop, tell the user exactly what will be deleted and that it is permanent, and wait for their explicit written confirmation before proceeding.

**Inputs:**
```
- `groupId` (string, required) — Unique 24-hexadecimal digit string that identifies the project to remove (e.g. '32b6e34b3d91647abb20e7b8'). The project must have no clusters.
```

**Output `data` schema:**

```typescript
{
  id: string | null;
  name: string | null;
  orgId: string | null;
  clusterCount: number | null;
  created: string | null;
  regionUsageRestrictions: string | null;
  withDefaultAlertsSettings: boolean | null;
  tags: {
    key: string | null;
    value: string | null;
  }[] | null;
  links: {
    href: string | null;
    rel: string | null;
  }[] | null;
} | null
```

On success the upstream API returns `204 No Content`, so `data` is `null`.

</details>


### Clusters

<details>
<summary><code>get_cluster</code> — Fetch one cluster's full configuration and status</summary>

Returns the full configuration and status details for one cluster identified by project (groupId) and cluster name.

**Inputs:**
```
- `group_id` (string, required) — Unique 24-hexadecimal digit string that identifies the project (group). Format: ^([a-f0-9]{24})$.
- `cluster_name` (string, required) — Human-readable label that identifies this cluster. Format: ^[a-zA-Z0-9][a-zA-Z0-9-]*$.
```

**Output `data` schema:**

```typescript
{
  acceptDataRisksAndForceReplicaSetReconfig: string | null;
  adaptiveCapacity: string | null;
  advancedConfiguration: Record<string, unknown> | null;
  backupEnabled: boolean | null;
  biConnector: Record<string, unknown> | null;
  clusterType: string | null;
  configServerManagementMode: string | null;
  configServerType: string | null;
  connectionStrings: Record<string, unknown> | null;
  createDate: string | null;
  diskWarmingMode: string | null;
  effectiveReplicationSpecs: unknown[] | null;
  encryptionAtRestProvider: string | null;
  featureCompatibilityVersion: string | null;
  featureCompatibilityVersionExpirationDate: string | null;
  globalClusterSelfManagedSharding: boolean | null;
  groupId: string | null;
  id: string | null;
  internalClusterRole: string | null;
  labels: unknown[] | null;
  links: unknown[] | null;
  mongoDBEmployeeAccessGrant: Record<string, unknown> | null;
  mongoDBMajorVersion: string | null;
  mongoDBVersion: string | null;
  name: string | null;
  paused: boolean | null;
  pitEnabled: boolean | null;
  redactClientLogData: boolean | null;
  replicaSetScalingStrategy: string | null;
  replicationSpecs: unknown[] | null;
  retainBackups: boolean | null;
  rootCertType: string | null;
  stateName: string | null;
  tags: unknown[] | null;
  terminationProtectionEnabled: boolean | null;
  useAwsTimeBasedSnapshotCopyForFastInitialSync: boolean | null;
  versionReleaseSystem: string | null;
} | null
```

</details>


<details>
<summary><code>list_clusters</code> — List all clusters in one project</summary>

Returns all clusters in one project, including each cluster's configuration and status.

**Inputs:**
```
- `group_id` (string, required) — Unique 24-hexadecimal digit string that identifies the project (group). Format: ^([a-f0-9]{24})$.
- `include_count` (boolean, optional, default: true) — Flag that indicates whether the response returns the total number of items (totalCount). Optional, defaults to true.
- `items_per_page` (integer, optional, default: 100) — Number of items that the response returns per page. Min 1, max 500. Optional, defaults to 100.
- `page_num` (integer, optional, default: 1) — Number of the page that displays the current set of the total objects. Min 1. Optional, defaults to 1.
- `include_deleted_with_retained_backups` (boolean, optional, default: false) — Flag that indicates whether to return clusters with retained backups. Optional, defaults to false.
```

**Output `data` schema:**

```typescript
{
  links: unknown[] | null;
  results: {
    // same shape as get_cluster's output schema above
    acceptDataRisksAndForceReplicaSetReconfig: string | null;
    adaptiveCapacity: string | null;
    advancedConfiguration: Record<string, unknown> | null;
    backupEnabled: boolean | null;
    biConnector: Record<string, unknown> | null;
    clusterType: string | null;
    configServerManagementMode: string | null;
    configServerType: string | null;
    connectionStrings: Record<string, unknown> | null;
    createDate: string | null;
    diskWarmingMode: string | null;
    effectiveReplicationSpecs: unknown[] | null;
    encryptionAtRestProvider: string | null;
    featureCompatibilityVersion: string | null;
    featureCompatibilityVersionExpirationDate: string | null;
    globalClusterSelfManagedSharding: boolean | null;
    groupId: string | null;
    id: string | null;
    internalClusterRole: string | null;
    labels: unknown[] | null;
    links: unknown[] | null;
    mongoDBEmployeeAccessGrant: Record<string, unknown> | null;
    mongoDBMajorVersion: string | null;
    mongoDBVersion: string | null;
    name: string | null;
    paused: boolean | null;
    pitEnabled: boolean | null;
    redactClientLogData: boolean | null;
    replicaSetScalingStrategy: string | null;
    replicationSpecs: unknown[] | null;
    retainBackups: boolean | null;
    rootCertType: string | null;
    stateName: string | null;
    tags: unknown[] | null;
    terminationProtectionEnabled: boolean | null;
    useAwsTimeBasedSnapshotCopyForFastInitialSync: boolean | null;
    versionReleaseSystem: string | null;
  }[];
  totalCount: number;
} | null
```

</details>


<details>
<summary><code>list_all_clusters</code> — List all clusters across every accessible project</summary>

Returns all clusters across every project the requester can access, grouped by project.

**Inputs:**
```
- `include_count` (boolean, optional, default: true) — Flag that indicates whether the response returns the total number of items (totalCount). Optional, defaults to true.
- `items_per_page` (integer, optional, default: 100) — Number of items that the response returns per page. Min 1, max 500. Optional, defaults to 100.
- `page_num` (integer, optional, default: 1) — Number of the page that displays the current set of the total objects. Min 1. Optional, defaults to 1.
```

**Output `data` schema:**

```typescript
{
  links: unknown[] | null;
  results: {
    groupId: string | null;
    groupName: string | null;
    orgId: string | null;
    orgName: string | null;
    planType: string | null;
    tags: unknown[] | null;
    clusters: {
      clusterId: string | null;
      name: string | null;
      type: string | null;
      nodeCount: number | null;
      dataSizeBytes: number | null;
      authEnabled: boolean | null;
      sslEnabled: boolean | null;
      backupEnabled: boolean | null;
      availability: string | null;
      alertCount: number | null;
      versions: unknown[] | null;
    }[];
  }[];
  totalCount: number;
} | null
```

</details>


## API Parameters Reference

<details>
<summary><strong>Response Envelope</strong></summary>

Every tool returns the same top-level envelope. Only `data` varies per tool.

```json
// Success
{
  "success": true,
  "statusCode": 200,
  "retriable": false,
  "retry_after_seconds": null,
  "error": null,
  "data": { ... }
}

// Error
{
  "success": false,
  "statusCode": 400,
  "retriable": false,
  "retry_after_seconds": null,
  "error": { "code": "{ERROR_CODE}", "message": "{description}", "details": {} },
  "data": null
}
```

- `retriable` — `true` when it is safe to retry (rate limit, network error, 503). `false` for validation and auth errors.
- `retry_after_seconds` — seconds to wait before retrying; present only when `retriable` is `true` and the upstream specifies a delay.
- `error.code` — machine-readable string: `VALIDATION_ERROR`, `AUTH_ERROR`, `UPSTREAM_ERROR`, `SERVER_ERROR`.

</details>

<details>
<summary><strong>Common Parameters</strong></summary>

- `itemsPerPage` / `items_per_page` — Number of items to return per page. Min 1, max 500. Optional, defaults to 100.
- `pageNum` / `page_num` — Page number of the results to return. Min 1. Optional, defaults to 1.
- `includeCount` / `include_count` — Whether the response includes the total number of items (`totalCount`). Optional, defaults to true.

Projects tools use camelCase parameter names (`itemsPerPage`, `pageNum`, `includeCount`); clusters tools use snake_case (`items_per_page`, `page_num`, `include_count`) — use the exact casing shown in each tool's Inputs.

</details>

<details>
<summary><strong>Resource Formats</strong></summary>

**Project / Group ID:**

```
24-hexadecimal digit string
Example: 32b6e34b3d91647abb20e7b8
```

Projects and groups are synonymous terms in the Atlas Administration API — the resource and its endpoints use `groups`, but the MongoDB Cloud UI and this tool group use `project`. The projects tools name this parameter `groupId`; the clusters tools name it `group_id`. Both accept the same value and match `^([a-f0-9]{24})$`.

**Cluster Name:**

```
^[a-zA-Z0-9][a-zA-Z0-9-]*$
```

</details>


## Troubleshooting

<details>
<summary><strong>Missing or Invalid Headers</strong></summary>

- **Cause:** API key not provided in request headers or incorrect format
- **Solution:**
  1. Verify `Authorization: Bearer YOUR_API_KEY` and `X-Mewcp-Credential-Id: CREDENTIAL-ID` headers are present
  2. Check API key is active in your MewCP account

</details>

<details>
<summary><strong>Insufficient Credits</strong></summary>

- **Cause:** API calls have exceeded your request limits
- **Solution:**
  1. Check credit usage in your Curious Layer dashboard
  2. Upgrade to a paid plan or add credits for higher limits
  3. Contact support for credit adjustments

</details>

<details>
<summary><strong>Credential Not Connected</strong></summary>

- **Cause:** No MongoDB Atlas credential linked to your account
- **Solution:**
  1. Go to **Credentials** in your MewCP dashboard
  2. Connect your MongoDB Atlas account (OAuth) or add your API key (static)
  3. Retry the request with the correct `X-Mewcp-Credential-Id` header

</details>

<details>
<summary><strong>Malformed Request Payload</strong></summary>

- **Cause:** JSON payload is invalid or missing required fields
- **Solution:**
  1. Validate JSON syntax before sending
  2. Ensure all required tool parameters are included
  3. Check parameter types match expected values

</details>

<details>
<summary><strong>Server Not Found</strong></summary>

- **Cause:** Incorrect server name in the API endpoint
- **Solution:**
  1. Verify endpoint format: `{server-name}/mcp/{tool-name}`
  2. Use correct server name from documentation
  3. Check available servers in your Curious Layer account

</details>

<details>
<summary><strong>MongoDB Atlas API Error</strong></summary>

- **Cause:** Upstream MongoDB Atlas API returned an error
- **Solution:**
  1. Check MongoDB Atlas service status at [MongoDB Atlas Status Page]({link})
  2. Verify your credential has the required permissions
  3. Review the error message for specific details

</details>

---

<details>
<summary><strong>Resources</strong></summary>

- **[MongoDB Atlas API Documentation]({link})** — Official API reference
- **[MongoDB Atlas API Reference]({link})** — Complete endpoint reference
- **[FastMCP Docs](https://gofastmcp.com/v2/getting-started/welcome)** — FastMCP specification
- **[FastMCP Credentials](https://pypi.org/project/fastmcp-credentials/)** — FastMCP Credentials package for credential handling


</details>
