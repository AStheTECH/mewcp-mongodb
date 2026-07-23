"""Clusters group schemas: get_cluster, list_clusters, list_all_clusters."""

from pydantic import BaseModel, ConfigDict

from ._base import ToolResult


class ClusterData(BaseModel):
    model_config = ConfigDict(extra="allow")

    acceptDataRisksAndForceReplicaSetReconfig: str | None = None
    adaptiveCapacity: str | None = None
    advancedConfiguration: dict | None = None
    backupEnabled: bool | None = None
    biConnector: dict | None = None
    clusterType: str | None = None
    configServerManagementMode: str | None = None
    configServerType: str | None = None
    connectionStrings: dict | None = None
    createDate: str | None = None
    diskWarmingMode: str | None = None
    effectiveReplicationSpecs: list | None = None
    encryptionAtRestProvider: str | None = None
    featureCompatibilityVersion: str | None = None
    featureCompatibilityVersionExpirationDate: str | None = None
    globalClusterSelfManagedSharding: bool | None = None
    groupId: str | None = None
    id: str | None = None
    internalClusterRole: str | None = None
    labels: list | None = None
    links: list | None = None
    mongoDBEmployeeAccessGrant: dict | None = None
    mongoDBMajorVersion: str | None = None
    mongoDBVersion: str | None = None
    name: str | None = None
    paused: bool | None = None
    pitEnabled: bool | None = None
    redactClientLogData: bool | None = None
    replicaSetScalingStrategy: str | None = None
    replicationSpecs: list | None = None
    retainBackups: bool | None = None
    rootCertType: str | None = None
    stateName: str | None = None
    tags: list | None = None
    terminationProtectionEnabled: bool | None = None
    useAwsTimeBasedSnapshotCopyForFastInitialSync: bool | None = None
    versionReleaseSystem: str | None = None


class ClusterResult(ToolResult):
    data: ClusterData | None = None


class ClusterListData(BaseModel):
    model_config = ConfigDict(extra="allow")

    links: list | None = None
    results: list[ClusterData]
    totalCount: int


class ClusterListResult(ToolResult):
    data: ClusterListData | None = None


class ClusterSummary(BaseModel):
    """Lightweight per-cluster summary as returned inside list_all_clusters results[].clusters[]."""

    model_config = ConfigDict(extra="allow")

    clusterId: str | None = None
    name: str | None = None
    type: str | None = None
    nodeCount: int | None = None
    dataSizeBytes: int | None = None
    authEnabled: bool | None = None
    sslEnabled: bool | None = None
    backupEnabled: bool | None = None
    availability: str | None = None
    alertCount: int | None = None
    versions: list | None = None


class ClusterGroupSummary(BaseModel):
    """Per-project group as returned inside list_all_clusters results[]."""

    model_config = ConfigDict(extra="allow")

    groupId: str | None = None
    groupName: str | None = None
    orgId: str | None = None
    orgName: str | None = None
    planType: str | None = None
    tags: list | None = None
    clusters: list[ClusterSummary]


class AllClusterListData(BaseModel):
    model_config = ConfigDict(extra="allow")

    links: list | None = None
    results: list[ClusterGroupSummary]
    totalCount: int


class AllClusterListResult(ToolResult):
    data: AllClusterListData | None = None
