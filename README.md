**Manage MongoDB Atlas projects, clusters, organizations, network access, and database users through the Atlas Administration API.**

A Model Context Protocol (MCP) server that exposes MongoDB Atlas's Administration API for managing Atlas projects (groups), reading cluster and organization state, auditing project network access, and managing database users.


## Overview

The mewcp-mongodb MCP Server provides direct, authenticated access to the MongoDB Atlas Administration API:

- Full lifecycle management of Atlas projects (groups) — create, read, list, update, and delete — plus project-scoped outbound IP addresses and configurable resource limits
- Read access to cluster configuration and status and available cloud provider regions, scoped to a single project or aggregated across every project the service account can access
- Read access to organizations and the projects that belong to them
- Read access to a project's IP access list entries for auditing network access rules
- Create and read database users, including their roles, authentication method, and access scopes
- Authenticates as a MongoDB Atlas service account using OAuth 2.0 client-credentials and makes raw HTTP calls directly to the Atlas Administration API, since no official Atlas Python SDK exists

Perfect for:

- Automating project provisioning and teardown across a MongoDB Cloud organization
- Auditing cluster configuration, network access, resource limits, and database user permissions across one or many projects
- Building agents and workflows that need programmatic visibility into Atlas infrastructure and security posture


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


<details>
<summary><code>get_project_by_name</code> — Fetch one Atlas project by its name</summary>

Returns one project matched by its name.

**Inputs:**
```
- `groupName` (string, required) — Human-readable label that identifies this project. Minimum length is 1, maximum length is 64.
- `envelope` (boolean, optional, default: null) — Flag that indicates whether the response is wrapped in an envelope JSON object. Default: false.
- `pretty` (boolean, optional, default: null) — Flag that indicates whether the response body should be in the prettyprint format. Default: false.
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
<summary><code>list_project_ip_addresses</code> — List the outbound IP addresses Atlas uses for a project</summary>

Returns the outbound IP addresses Atlas uses for cluster infrastructure and peered/private networks in this project.

**Inputs:**
```
- `groupId` (string, required) — Unique 24-hexadecimal digit string that identifies the project.
- `envelope` (boolean, optional, default: null) — Flag that indicates whether the response is wrapped in an envelope JSON object. Default: false.
- `pretty` (boolean, optional, default: null) — Flag that indicates whether the response body should be in the prettyprint format. Default: false.
```

**Output `data` schema:**

```typescript
{
  groupId: string | null;
  services: {
    clusters: {
      clusterName: string | null;
      inbound: string[] | null;
      outbound: string[] | null;
      futureInbound: string[] | null;
      futureOutbound: string[] | null;
    }[] | null;
  } | null;
} | null
```

</details>


<details>
<summary><code>list_project_limits</code> — List all configurable resource limits and usage for a project</summary>

Returns all configurable resource limits and their current usage for one project.

**Inputs:**
```
- `groupId` (string, required) — Unique 24-hexadecimal digit string that identifies the project.
- `envelope` (boolean, optional, default: null) — Flag that indicates whether the response is wrapped in an envelope JSON object. Default: false.
- `pretty` (boolean, optional, default: null) — Flag that indicates whether the response body should be in the prettyprint format. Default: false.
```

**Output `data` schema:**

```typescript
{
  limits: {
    name: string | null;
    value: number | null;
    currentUsage: number | null;
    defaultLimit: number | null;
    maximumLimit: number | null;
  }[];
} | null
```

</details>


<details>
<summary><code>get_project_limit</code> — Fetch one configurable resource limit for a project</summary>

Returns one resource limit by name for one project.

**Inputs:**
```
- `groupId` (string, required) — Unique 24-hexadecimal digit string that identifies the project.
- `limitName` (string, required) — Human-readable label that identifies this project limit. One of: atlas.project.security.databaseAccess.users, atlas.project.deployment.clusters, atlas.project.deployment.serverlessMTMs, atlas.project.security.databaseAccess.customRoles, atlas.project.security.networkAccess.entries, atlas.project.security.networkAccess.crossRegionEntries, atlas.project.deployment.nodesPerPrivateLinkRegion, dataFederation.bytesProcessed.query, dataFederation.bytesProcessed.daily, dataFederation.bytesProcessed.weekly, dataFederation.bytesProcessed.monthly, atlas.project.deployment.privateServiceConnectionsPerRegionGroup, or atlas.project.deployment.privateServiceConnectionsSubnetMask.
- `envelope` (boolean, optional, default: null) — Flag that indicates whether the response is wrapped in an envelope JSON object. Default: false.
- `pretty` (boolean, optional, default: null) — Flag that indicates whether the response body should be in the prettyprint format. Default: false.
```

**Output `data` schema:**

```typescript
{
  name: string | null;
  value: number | null;
  currentUsage: number | null;
  defaultLimit: number | null;
  maximumLimit: number | null;
} | null
```

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


<details>
<summary><code>list_cloud_provider_regions</code> — List cloud provider regions available for cluster creation</summary>

Returns the cloud provider regions available for cluster creation.

**Inputs:**
```
- `group_id` (string, required) — Unique 24-hexadecimal digit string that identifies the project (group). Format: ^([a-f0-9]{24})$.
- `envelope` (boolean, optional, default: false) — Wraps the response in an envelope JSON object. Optional, defaults to false.
- `include_count` (boolean, optional, default: true) — Flag that indicates whether the response returns the total number of items (totalCount). Optional, defaults to true.
- `items_per_page` (integer, optional, default: 100) — Number of items that the response returns per page. Min 1, max 500. Optional, defaults to 100.
- `page_num` (integer, optional, default: 1) — Number of the page that displays the current set of the total objects. Min 1. Optional, defaults to 1.
- `pretty` (boolean, optional, default: false) — Flag that indicates whether the response body should be in the prettyprint format. Optional, defaults to false.
- `providers` (array, optional, default: null) — Cloud providers whose regions to retrieve. When multiple providers are specified, the response can return only tiers and regions that support multi-cloud clusters. Optional, defaults to all providers.
- `tier` (string, optional, default: null) — Cluster tier for which to retrieve the regions. Optional, defaults to all tiers.
```

**Output `data` schema:**

```typescript
{
  links: unknown[] | null;
  results: {
    provider: string | null;
    instanceSizes: {
      name: string | null;
      availableRegions: {
        name: string | null;
        default: boolean | null;
      }[] | null;
    }[] | null;
  }[];
  totalCount: number;
} | null
```

</details>


### Organizations

<details>
<summary><code>list_organizations</code> — List all MongoDB Cloud organizations the service account can access</summary>

Returns all organizations to which the requesting service account has access.

**Inputs:**
```
- `name` (string, optional, default: null) — Human-readable label of the organization to filter the returned list by. Performs a case-insensitive search for an organization whose name starts with this value. Optional.
- `includeCount` (boolean, optional, default: null) — Whether the response includes the total number of items (totalCount). Optional, defaults to true on the server.
- `itemsPerPage` (integer, optional, default: null) — Number of items to return per page (1-500). Optional, defaults to 100 on the server.
- `pageNum` (integer, optional, default: null) — Page number of the results to return, minimum 1. Optional, defaults to 1 on the server.
- `envelope` (boolean, optional, default: null) — Whether to wrap the response in an envelope JSON object, for API clients that cannot access HTTP response headers or status codes. Optional, defaults to false on the server.
- `pretty` (boolean, optional, default: null) — Whether the response body should be in the prettyprint format. Optional, defaults to false on the server.
```

**Output `data` schema:**

```typescript
{
  results: {
    id: string | null;
    name: string | null;
    isDeleted: boolean | null;
    skipDefaultAlertsSettings: boolean | null;
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
<summary><code>get_organization</code> — Fetch one organization by ID</summary>

Returns one organization by its unique ID.

**Inputs:**
```
- `orgId` (string, required) — Unique 24-hexadecimal digit string that identifies the organization (e.g. '32b6e34b3d91647abb20e7b8'). Use `list_organizations` to retrieve all organizations to which the authenticated user has access.
- `envelope` (boolean, optional, default: null) — Whether to wrap the response in an envelope JSON object, for API clients that cannot access HTTP response headers or status codes. Optional, defaults to false on the server.
- `pretty` (boolean, optional, default: null) — Whether the response body should be in the prettyprint format. Optional, defaults to false on the server.
```

**Output `data` schema:**

```typescript
{
  id: string | null;
  name: string | null;
  isDeleted: boolean | null;
  skipDefaultAlertsSettings: boolean | null;
  links: {
    href: string | null;
    rel: string | null;
  }[] | null;
} | null
```

</details>


<details>
<summary><code>list_organization_projects</code> — List all projects inside one organization</summary>

Returns all projects inside one organization.

**Inputs:**
```
- `orgId` (string, required) — Unique 24-hexadecimal digit string that identifies the organization (e.g. '32b6e34b3d91647abb20e7b8'). Use `list_organizations` to retrieve all organizations to which the authenticated user has access.
- `name` (string, optional, default: null) — Human-readable label of the project to filter the returned list by. Performs a case-insensitive search for a project within the organization whose name is prefixed by this value. Optional.
- `includeCount` (boolean, optional, default: null) — Whether the response includes the total number of items (totalCount). Optional, defaults to true on the server.
- `itemsPerPage` (integer, optional, default: null) — Number of items to return per page (1-500). Optional, defaults to 100 on the server.
- `pageNum` (integer, optional, default: null) — Page number of the results to return, minimum 1. Optional, defaults to 1 on the server.
- `envelope` (boolean, optional, default: null) — Whether to wrap the response in an envelope JSON object, for API clients that cannot access HTTP response headers or status codes. Optional, defaults to false on the server.
- `pretty` (boolean, optional, default: null) — Whether the response body should be in the prettyprint format. Optional, defaults to false on the server.
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


### IP Access List

<details>
<summary><code>list_ip_access_list_entries</code> — List all IP access list entries for a project</summary>

Returns all IP access list entries for one project.

**Inputs:**
```
- `group_id` (string, required) — Unique 24-hexadecimal digit string that identifies your project. Use the /groups endpoint to retrieve all projects to which the authenticated user has access. Format should match the following pattern: ^([a-f0-9]{24})$.
- `envelope` (boolean, optional, default: false) — Flag that indicates whether Application wraps the response in an envelope JSON object. Some API clients cannot access the HTTP response headers or status code. To remediate this, set envelope=true in the query. Endpoints that return a list of results use the results object as an envelope. Application adds the status parameter to the response body. Optional, defaults to false.
- `include_count` (boolean, optional, default: true) — Flag that indicates whether the response returns the total number of items (totalCount) in the response. Optional, defaults to true.
- `items_per_page` (integer, optional, default: 100) — Number of items that the response returns per page. Minimum value is 1, maximum value is 500. Optional, defaults to 100.
- `page_num` (integer, optional, default: 1) — Number of the page that displays the current set of the total objects that the response returns. Minimum value is 1. Optional, defaults to 1.
- `pretty` (boolean, optional, default: false) — Flag that indicates whether the response body should be in the prettyprint format. Optional, defaults to false.
```

**Output `data` schema:**

```typescript
{
  links: unknown[] | null;
  results: {
    awsSecurityGroup: string | null;
    cidrBlock: string | null;
    comment: string | null;
    deleteAfterDate: string | null;
    groupId: string | null;
    ipAddress: string | null;
    links: unknown[] | null;
  }[];
  totalCount: number;
} | null
```

</details>


<details>
<summary><code>get_ip_access_list_entry</code> — Fetch one IP access list entry by its value</summary>

Returns one IP access list entry by its value.

**Inputs:**
```
- `group_id` (string, required) — Unique 24-hexadecimal digit string that identifies your project. Use the /groups endpoint to retrieve all projects to which the authenticated user has access. Format should match the following pattern: ^([a-f0-9]{24})$.
- `entry_value` (string, required) — Access list entry that you want to return from the project's IP access list. This value can use one of the following: one AWS security group ID, one IP address, or one CIDR block of addresses. For CIDR blocks that use a subnet mask, replace the forward slash (/) with its URL-encoded value (%2F). Format should match the following pattern: ^([0-9]{1,3}\.){3}[0-9]{1,3}(%2[fF][0-9]{1,3})?|([0-9a-f]{1,4}\:){7}[0-9a-f]{1,4}(%2[fF][0-9]{1,3})?|([0-9a-f]{1,4}\:){1,6}\:(%2[fF][0-9]{1,3})|(sg\-[a-f0-9]{8})?$.
- `envelope` (boolean, optional, default: false) — Flag that indicates whether Application wraps the response in an envelope JSON object. Some API clients cannot access the HTTP response headers or status code. To remediate this, set envelope=true in the query. Endpoints that return a list of results use the results object as an envelope. Application adds the status parameter to the response body. Optional, defaults to false.
- `pretty` (boolean, optional, default: false) — Flag that indicates whether the response body should be in the prettyprint format. Optional, defaults to false.
```

**Output `data` schema:**

```typescript
{
  awsSecurityGroup: string | null;
  cidrBlock: string | null;
  comment: string | null;
  deleteAfterDate: string | null;
  groupId: string | null;
  ipAddress: string | null;
  links: unknown[] | null;
} | null
```

</details>


### Database Users

<details>
<summary><code>create_database_user</code> — Create a new database user with roles and authentication method</summary>

Creates one new database user with specified roles and authentication method for a project.

**Inputs:**
```
- `groupId` (string, required) — Unique 24-hexadecimal digit string that identifies your project. Use the /groups endpoint to retrieve all projects to which the authenticated user has access. Groups and projects are synonymous terms.
- `databaseName` (string, required) — The database against which the database user authenticates. If the user authenticates with AWS IAM, x.509, LDAP, or OIDC Workload this value should be $external. If the user authenticates with SCRAM-SHA or OIDC Workforce, this value should be admin. Values are admin or $external.
- `username` (string, required) — Human-readable label that represents the user that authenticates to MongoDB. The format depends on the authentication method used (AWS IAM, x.509, LDAP, OIDC Workforce, OIDC Workload, or SCRAM-SHA). Maximum length is 1024.
- `roles` (array, required) — List that provides the pairings of one role with one applicable database.
- `password` (string, optional, default: null) — Alphanumeric string that authenticates this database user against the database specified in databaseName. Must be specified to authenticate with SCRAM-SHA. Does not appear in the response. Minimum length is 8. Optional.
- `awsIAMType` (string, optional, default: null) — Human-readable label that indicates whether the new database user authenticates with AWS IAM credentials associated with the user or the user's role. Values are NONE, USER, or ROLE. Default value is NONE.
- `deleteAfterDate` (string, optional, default: null) — Date and time when MongoDB Cloud deletes the user, expressed in ISO 8601 UTC format. Must be a future date within one week of the request. Optional.
- `description` (string, optional, default: null) — Description of this database user. Maximum length is 100. Optional.
- `labels` (array, optional, default: null) — List that contains the key-value pairs for tagging and categorizing the MongoDB database user. These labels do not appear in the console. Optional.
- `ldapAuthType` (string, optional, default: null) — Part of the LDAP record that the database uses to authenticate this database user on the LDAP host. Values are NONE, GROUP, or USER. Default value is NONE.
- `oidcAuthType` (string, optional, default: null) — Indicates whether the new database user or group authenticates with OIDC federated authentication. Specify USER to create a federated authentication user, or IDP_GROUP to create a federated authentication group. Values are NONE, IDP_GROUP, or USER. Default value is NONE.
- `scopes` (array, optional, default: null) — List that contains clusters, MongoDB Atlas Data Lakes, and MongoDB Atlas Streams Workspaces that this database user can access. If omitted, MongoDB Cloud grants the database user access to all clusters, Data Lakes, and Streams Workspaces in the project. Optional.
- `x509Type` (string, optional, default: null) — X.509 method that MongoDB Cloud uses to authenticate the database user. Specify MANAGED for application-managed X.509, or CUSTOMER for self-managed X.509. Values are NONE, CUSTOMER, or MANAGED. Default value is NONE.
- `envelope` (boolean, optional, default: null) — Flag that indicates whether the response is wrapped in an envelope JSON object, for API clients that cannot access HTTP response headers or status code. Default value is false. Optional.
- `pretty` (boolean, optional, default: null) — Flag that indicates whether the response body should be in the prettyprint format. Default value is false. Optional.
```

**Output `data` schema:**

```typescript
{
  username: string | null;
  databaseName: string | null;
  awsIAMType: string | null;
  deleteAfterDate: string | null;
  description: string | null;
  labels: Record<string, unknown>[] | null;
  ldapAuthType: string | null;
  oidcAuthType: string | null;
  roles: Record<string, unknown>[] | null;
  scopes: Record<string, unknown>[] | null;
  x509Type: string | null;
  links: Record<string, unknown>[] | null;
} | null
```

</details>


<details>
<summary><code>get_database_user</code> — Fetch one database user by database and username</summary>

Returns one database user by authentication database and username.

**Inputs:**
```
- `groupId` (string, required) — Unique 24-hexadecimal digit string that identifies your project. Use the /groups endpoint to retrieve all projects to which the authenticated user has access. Groups and projects are synonymous terms.
- `databaseName` (string, required) — The database against which the database user authenticates. If the user authenticates with AWS IAM, x.509, LDAP, or OIDC Workload this value should be $external. If the user authenticates with SCRAM-SHA or OIDC Workforce, this value should be admin.
- `username` (string, required) — Human-readable label that represents the user that authenticates to MongoDB. The format depends on the authentication method used (AWS IAM, x.509, LDAP, OIDC Workforce, OIDC Workload, or SCRAM-SHA).
- `envelope` (boolean, optional, default: null) — Flag that indicates whether the response is wrapped in an envelope JSON object, for API clients that cannot access HTTP response headers or status code. Default value is false. Optional.
- `pretty` (boolean, optional, default: null) — Flag that indicates whether the response body should be in the prettyprint format. Default value is false. Optional.
```

**Output `data` schema:**

```typescript
{
  username: string | null;
  databaseName: string | null;
  awsIAMType: string | null;
  deleteAfterDate: string | null;
  description: string | null;
  labels: Record<string, unknown>[] | null;
  ldapAuthType: string | null;
  oidcAuthType: string | null;
  roles: Record<string, unknown>[] | null;
  scopes: Record<string, unknown>[] | null;
  x509Type: string | null;
  links: Record<string, unknown>[] | null;
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
- `envelope` — Whether to wrap the response in an envelope JSON object, for API clients that cannot access HTTP response headers or status codes. Optional, defaults to false.
- `pretty` — Whether the response body should be in the prettyprint format. Optional, defaults to false.

Projects, organizations, and database users tools use camelCase parameter names (`itemsPerPage`, `pageNum`, `includeCount`, `groupId`, `orgId`); clusters and IP access list tools use snake_case (`items_per_page`, `page_num`, `include_count`, `group_id`) — use the exact casing shown in each tool's Inputs.

</details>

<details>
<summary><strong>Resource Formats</strong></summary>

**Project / Group ID:**

```
24-hexadecimal digit string
Example: 32b6e34b3d91647abb20e7b8
Pattern: ^([a-f0-9]{24})$
```

Projects and groups are synonymous terms in the Atlas Administration API — the resource and its endpoints use `groups`, but the MongoDB Cloud UI and this tool group use `project`. Projects and database users tools name this parameter `groupId`; clusters and IP access list tools name it `group_id`. Both accept the same value.

**Organization ID:**

```
24-hexadecimal digit string
Example: 32b6e34b3d91647abb20e7b8
```

**Cluster Name:**

```
^[a-zA-Z0-9][a-zA-Z0-9-]*$
```

**IP Access List Entry Value:**

```
One of: an IP address, a CIDR block (URL-encode the "/" as "%2F"), or an AWS security group ID.
Pattern: ^([0-9]{1,3}\.){3}[0-9]{1,3}(%2[fF][0-9]{1,3})?|([0-9a-f]{1,4}\:){7}[0-9a-f]{1,4}(%2[fF][0-9]{1,3})?|([0-9a-f]{1,4}\:){1,6}\:(%2[fF][0-9]{1,3})|(sg\-[a-f0-9]{8})?$
Example: 192.0.2.0%2F24
```

**Project Limit Name:**

```
One of: atlas.project.security.databaseAccess.users, atlas.project.deployment.clusters,
atlas.project.deployment.serverlessMTMs, atlas.project.security.databaseAccess.customRoles,
atlas.project.security.networkAccess.entries, atlas.project.security.networkAccess.crossRegionEntries,
atlas.project.deployment.nodesPerPrivateLinkRegion, dataFederation.bytesProcessed.query,
dataFederation.bytesProcessed.daily, dataFederation.bytesProcessed.weekly,
dataFederation.bytesProcessed.monthly, atlas.project.deployment.privateServiceConnectionsPerRegionGroup,
atlas.project.deployment.privateServiceConnectionsSubnetMask
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
  2. Connect your MongoDB Atlas account (OAuth)
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
  1. Check MongoDB Atlas service status at [MongoDB Atlas Status Page](https://status.mongodb.com/)
  2. Verify your credential has the required permissions
  3. Review the error message for specific details

</details>

---

<details>
<summary><strong>Resources</strong></summary>

- **[MongoDB Atlas Administration API Documentation](https://www.mongodb.com/docs/atlas/administration-api/)** — Official API reference
- **[MongoDB Atlas API Resources (v2)](https://www.mongodb.com/docs/atlas/reference/api-resources-spec/v2/)** — Complete endpoint reference
- **[FastMCP Docs](https://gofastmcp.com/v2/getting-started/welcome)** — FastMCP specification
- **[FastMCP Credentials](https://pypi.org/project/fastmcp-credentials/)** — FastMCP Credentials package for credential handling


</details>
