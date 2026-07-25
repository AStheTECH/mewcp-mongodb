"""Clusters group: get_cluster, list_clusters, list_all_clusters."""

import logging

from fastmcp import FastMCP
from mcp.types import ToolAnnotations
from pydantic import Field

from .. import service
from ..config import CONNECT_TIMEOUT, READ_TIMEOUT
from ..logging_utils import ToolLogger
from ..schemas.clusters import (
    AllClusterListResult,
    AllClusterListData,
    CloudProviderRegionListData,
    CloudProviderRegionListResult,
    ClusterData,
    ClusterListData,
    ClusterListResult,
    ClusterResult,
)
from ._helpers import _err, _handle_request_exc, _upstream_err

logger = logging.getLogger("mongodb-mcp.tools.clusters")


def register_clusters_tools(mcp: FastMCP) -> None:

    @mcp.tool(
        name="get_cluster",
        description=(
            "Returns the full configuration and status details for one cluster identified by "
            "project (groupId) and cluster name."
        ),
        annotations=ToolAnnotations(readOnlyHint=True, destructiveHint=False, openWorldHint=True),
    )
    def get_cluster(
        group_id: str = Field(
            description="Unique 24-hexadecimal digit string that identifies the project (group). Format: ^([a-f0-9]{24})$."
        ),
        cluster_name: str = Field(
            description="Human-readable label that identifies this cluster. Format: ^[a-zA-Z0-9][a-zA-Z0-9-]*$."
        ),
    ) -> ClusterResult:
        tlog = ToolLogger(logger, "get_cluster")

        if not group_id or not group_id.strip():
            return _err(ClusterResult, tlog, "VALIDATION_ERROR", "group_id is required", 400)
        if not cluster_name or not cluster_name.strip():
            return _err(ClusterResult, tlog, "VALIDATION_ERROR", "cluster_name is required", 400)

        try:
            data, status, retry_after = service.api_request(
                "GET", f"/groups/{group_id}/clusters/{cluster_name}",
                timeout=(CONNECT_TIMEOUT, READ_TIMEOUT),
            )
            if 200 <= status < 300:
                tlog.success()
                return ClusterResult(success=True, statusCode=status, data=ClusterData(**data))
            return _upstream_err(ClusterResult, tlog, status, data, retry_after)
        except Exception as exc:
            return _handle_request_exc(ClusterResult, tlog, exc)

    @mcp.tool(
        name="list_clusters",
        description=(
            "Returns all clusters in one project, including each cluster's configuration and status."
        ),
        annotations=ToolAnnotations(readOnlyHint=True, destructiveHint=False, openWorldHint=True),
    )
    def list_clusters(
        group_id: str = Field(
            description="Unique 24-hexadecimal digit string that identifies the project (group). Format: ^([a-f0-9]{24})$."
        ),
        include_count: bool = Field(
            default=True, description="Flag that indicates whether the response returns the total number of items (totalCount). Optional, defaults to true."
        ),
        items_per_page: int = Field(
            default=100, description="Number of items that the response returns per page. Min 1, max 500. Optional, defaults to 100."
        ),
        page_num: int = Field(
            default=1, description="Number of the page that displays the current set of the total objects. Min 1. Optional, defaults to 1."
        ),
        include_deleted_with_retained_backups: bool = Field(
            default=False, description="Flag that indicates whether to return clusters with retained backups. Optional, defaults to false."
        ),
    ) -> ClusterListResult:
        tlog = ToolLogger(logger, "list_clusters")

        if not group_id or not group_id.strip():
            return _err(ClusterListResult, tlog, "VALIDATION_ERROR", "group_id is required", 400)
        if items_per_page < 1 or items_per_page > 500:
            return _err(ClusterListResult, tlog, "VALIDATION_ERROR", "items_per_page must be 1-500", 400)
        if page_num < 1:
            return _err(ClusterListResult, tlog, "VALIDATION_ERROR", "page_num must be >= 1", 400)

        try:
            data, status, retry_after = service.api_request(
                "GET", f"/groups/{group_id}/clusters",
                params={
                    "includeCount": include_count,
                    "itemsPerPage": items_per_page,
                    "pageNum": page_num,
                    "includeDeletedWithRetainedBackups": include_deleted_with_retained_backups,
                },
                timeout=(CONNECT_TIMEOUT, READ_TIMEOUT),
            )
            if 200 <= status < 300:
                tlog.success()
                return ClusterListResult(success=True, statusCode=status, data=ClusterListData(**data))
            return _upstream_err(ClusterListResult, tlog, status, data, retry_after)
        except Exception as exc:
            return _handle_request_exc(ClusterListResult, tlog, exc)

    @mcp.tool(
        name="list_all_clusters",
        description=(
            "Returns all clusters across every project the requester can access, grouped by project."
        ),
        annotations=ToolAnnotations(readOnlyHint=True, destructiveHint=False, openWorldHint=True),
    )
    def list_all_clusters(
        include_count: bool = Field(
            default=True, description="Flag that indicates whether the response returns the total number of items (totalCount). Optional, defaults to true."
        ),
        items_per_page: int = Field(
            default=100, description="Number of items that the response returns per page. Min 1, max 500. Optional, defaults to 100."
        ),
        page_num: int = Field(
            default=1, description="Number of the page that displays the current set of the total objects. Min 1. Optional, defaults to 1."
        ),
    ) -> AllClusterListResult:
        tlog = ToolLogger(logger, "list_all_clusters")

        if items_per_page < 1 or items_per_page > 500:
            return _err(AllClusterListResult, tlog, "VALIDATION_ERROR", "items_per_page must be 1-500", 400)
        if page_num < 1:
            return _err(AllClusterListResult, tlog, "VALIDATION_ERROR", "page_num must be >= 1", 400)

        try:
            data, status, retry_after = service.api_request(
                "GET", "/clusters",
                params={
                    "includeCount": include_count,
                    "itemsPerPage": items_per_page,
                    "pageNum": page_num,
                },
                timeout=(CONNECT_TIMEOUT, READ_TIMEOUT),
            )
            if 200 <= status < 300:
                tlog.success()
                return AllClusterListResult(success=True, statusCode=status, data=AllClusterListData(**data))
            return _upstream_err(AllClusterListResult, tlog, status, data, retry_after)
        except Exception as exc:
            return _handle_request_exc(AllClusterListResult, tlog, exc)

    @mcp.tool(
        name="list_cloud_provider_regions",
        description=(
            "Returns the cloud provider regions available for cluster creation."
        ),
        annotations=ToolAnnotations(readOnlyHint=True, destructiveHint=False, openWorldHint=True),
    )
    def list_cloud_provider_regions(
        group_id: str = Field(
            description="Unique 24-hexadecimal digit string that identifies the project (group). Format: ^([a-f0-9]{24})$."
        ),
        envelope: bool = Field(
            default=False, description="Wraps the response in an envelope JSON object. Optional, defaults to false."
        ),
        include_count: bool = Field(
            default=True, description="Flag that indicates whether the response returns the total number of items (totalCount). Optional, defaults to true."
        ),
        items_per_page: int = Field(
            default=100, description="Number of items that the response returns per page. Min 1, max 500. Optional, defaults to 100."
        ),
        page_num: int = Field(
            default=1, description="Number of the page that displays the current set of the total objects. Min 1. Optional, defaults to 1."
        ),
        pretty: bool = Field(
            default=False, description="Flag that indicates whether the response body should be in the prettyprint format. Optional, defaults to false."
        ),
        providers: list[str] | None = Field(
            default=None, description="Cloud providers whose regions to retrieve. When multiple providers are specified, the response can return only tiers and regions that support multi-cloud clusters."
        ),
        tier: str | None = Field(
            default=None, description="Cluster tier for which to retrieve the regions."
        ),
    ) -> CloudProviderRegionListResult:
        tlog = ToolLogger(logger, "list_cloud_provider_regions")

        if not group_id or not group_id.strip():
            return _err(CloudProviderRegionListResult, tlog, "VALIDATION_ERROR", "group_id is required", 400)
        if items_per_page < 1 or items_per_page > 500:
            return _err(CloudProviderRegionListResult, tlog, "VALIDATION_ERROR", "items_per_page must be 1-500", 400)
        if page_num < 1:
            return _err(CloudProviderRegionListResult, tlog, "VALIDATION_ERROR", "page_num must be >= 1", 400)

        try:
            data, status, retry_after = service.api_request(
                "GET", f"/groups/{group_id}/clusters/provider/regions",
                params={
                    "envelope": envelope,
                    "includeCount": include_count,
                    "itemsPerPage": items_per_page,
                    "pageNum": page_num,
                    "pretty": pretty,
                    "providers": providers,
                    "tier": tier,
                },
                timeout=(CONNECT_TIMEOUT, READ_TIMEOUT),
            )
            if 200 <= status < 300:
                tlog.success()
                return CloudProviderRegionListResult(success=True, statusCode=status, data=CloudProviderRegionListData(**data))
            return _upstream_err(CloudProviderRegionListResult, tlog, status, data, retry_after)
        except Exception as exc:
            return _handle_request_exc(CloudProviderRegionListResult, tlog, exc)
