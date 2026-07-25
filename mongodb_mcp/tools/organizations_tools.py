"""Organizations group: list_organizations, get_organization, list_organization_projects."""

import logging

from fastmcp import FastMCP
from mcp.types import ToolAnnotations
from pydantic import Field

from .. import service
from ..config import CONNECT_TIMEOUT, READ_TIMEOUT
from ..logging_utils import ToolLogger
from ..schemas.organizations import (
    OrganizationData,
    OrganizationListData,
    OrganizationListResult,
    OrganizationProjectListData,
    OrganizationProjectListResult,
    OrganizationResult,
)
from ._helpers import _err, _handle_request_exc, _upstream_err

logger = logging.getLogger("mongodb-mcp.tools.organizations")

TIMEOUT = (CONNECT_TIMEOUT, READ_TIMEOUT)


def register_organizations_tools(mcp: FastMCP) -> None:

    @mcp.tool(
        name="list_organizations",
        description="Returns all organizations to which the requesting service account has access.",
        annotations=ToolAnnotations(readOnlyHint=True, destructiveHint=False, openWorldHint=True),
    )
    def list_organizations(
        name: str | None = Field(
            default=None,
            description=(
                "Human-readable label of the organization to filter the returned list by. "
                "Performs a case-insensitive search for an organization whose name starts "
                "with this value. Optional."
            ),
        ),
        includeCount: bool | None = Field(
            default=None,
            description=(
                "Whether the response includes the total number of items (totalCount). "
                "Optional, defaults to true on the server."
            ),
        ),
        itemsPerPage: int | None = Field(
            default=None,
            description="Number of items to return per page (1-500). Optional, defaults to 100 on the server.",
        ),
        pageNum: int | None = Field(
            default=None,
            description="Page number of the results to return, minimum 1. Optional, defaults to 1 on the server.",
        ),
        envelope: bool | None = Field(
            default=None,
            description=(
                "Whether to wrap the response in an envelope JSON object, for API clients "
                "that cannot access HTTP response headers or status codes. Optional, "
                "defaults to false on the server."
            ),
        ),
        pretty: bool | None = Field(
            default=None,
            description=(
                "Whether the response body should be in the prettyprint format. Optional, "
                "defaults to false on the server."
            ),
        ),
    ) -> OrganizationListResult:
        tlog = ToolLogger(logger, "list_organizations")

        if itemsPerPage is not None and not (1 <= itemsPerPage <= 500):
            return _err(OrganizationListResult, tlog, "VALIDATION_ERROR", "itemsPerPage must be between 1 and 500", 400)
        if pageNum is not None and pageNum < 1:
            return _err(OrganizationListResult, tlog, "VALIDATION_ERROR", "pageNum must be 1 or greater", 400)

        params: dict = {}
        if name is not None:
            params["name"] = name
        if includeCount is not None:
            params["includeCount"] = includeCount
        if itemsPerPage is not None:
            params["itemsPerPage"] = itemsPerPage
        if pageNum is not None:
            params["pageNum"] = pageNum
        if envelope is not None:
            params["envelope"] = envelope
        if pretty is not None:
            params["pretty"] = pretty

        try:
            data, status, retry_after = service.api_request(
                "GET", "/orgs", params=params or None, timeout=TIMEOUT,
            )
        except Exception as exc:
            return _handle_request_exc(OrganizationListResult, tlog, exc)

        if not (200 <= status < 300):
            return _upstream_err(OrganizationListResult, tlog, status, data, retry_after)

        tlog.success()
        return OrganizationListResult(success=True, statusCode=status, data=OrganizationListData(**data))

    @mcp.tool(
        name="get_organization",
        description="Returns one organization by its unique ID.",
        annotations=ToolAnnotations(readOnlyHint=True, destructiveHint=False, openWorldHint=True),
    )
    def get_organization(
        orgId: str = Field(
            description=(
                "Unique 24-hexadecimal digit string that identifies the organization "
                "(e.g. '32b6e34b3d91647abb20e7b8'). Use `list_organizations` to retrieve "
                "all organizations to which the authenticated user has access."
            )
        ),
        envelope: bool | None = Field(
            default=None,
            description=(
                "Whether to wrap the response in an envelope JSON object, for API clients "
                "that cannot access HTTP response headers or status codes. Optional, "
                "defaults to false on the server."
            ),
        ),
        pretty: bool | None = Field(
            default=None,
            description=(
                "Whether the response body should be in the prettyprint format. Optional, "
                "defaults to false on the server."
            ),
        ),
    ) -> OrganizationResult:
        tlog = ToolLogger(logger, "get_organization")

        if not orgId or not orgId.strip():
            return _err(OrganizationResult, tlog, "VALIDATION_ERROR", "orgId must be a non-empty string", 400)

        params: dict = {}
        if envelope is not None:
            params["envelope"] = envelope
        if pretty is not None:
            params["pretty"] = pretty

        try:
            data, status, retry_after = service.api_request(
                "GET", f"/orgs/{orgId}", params=params or None, timeout=TIMEOUT,
            )
        except Exception as exc:
            return _handle_request_exc(OrganizationResult, tlog, exc)

        if not (200 <= status < 300):
            return _upstream_err(OrganizationResult, tlog, status, data, retry_after)

        tlog.success()
        return OrganizationResult(success=True, statusCode=status, data=OrganizationData(**data))

    @mcp.tool(
        name="list_organization_projects",
        description="Returns all projects inside one organization.",
        annotations=ToolAnnotations(readOnlyHint=True, destructiveHint=False, openWorldHint=True),
    )
    def list_organization_projects(
        orgId: str = Field(
            description=(
                "Unique 24-hexadecimal digit string that identifies the organization "
                "(e.g. '32b6e34b3d91647abb20e7b8'). Use `list_organizations` to retrieve "
                "all organizations to which the authenticated user has access."
            )
        ),
        name: str | None = Field(
            default=None,
            description=(
                "Human-readable label of the project to filter the returned list by. "
                "Performs a case-insensitive search for a project within the organization "
                "whose name is prefixed by this value. Optional."
            ),
        ),
        includeCount: bool | None = Field(
            default=None,
            description=(
                "Whether the response includes the total number of items (totalCount). "
                "Optional, defaults to true on the server."
            ),
        ),
        itemsPerPage: int | None = Field(
            default=None,
            description="Number of items to return per page (1-500). Optional, defaults to 100 on the server.",
        ),
        pageNum: int | None = Field(
            default=None,
            description="Page number of the results to return, minimum 1. Optional, defaults to 1 on the server.",
        ),
        envelope: bool | None = Field(
            default=None,
            description=(
                "Whether to wrap the response in an envelope JSON object, for API clients "
                "that cannot access HTTP response headers or status codes. Optional, "
                "defaults to false on the server."
            ),
        ),
        pretty: bool | None = Field(
            default=None,
            description=(
                "Whether the response body should be in the prettyprint format. Optional, "
                "defaults to false on the server."
            ),
        ),
    ) -> OrganizationProjectListResult:
        tlog = ToolLogger(logger, "list_organization_projects")

        if not orgId or not orgId.strip():
            return _err(OrganizationProjectListResult, tlog, "VALIDATION_ERROR", "orgId must be a non-empty string", 400)
        if itemsPerPage is not None and not (1 <= itemsPerPage <= 500):
            return _err(OrganizationProjectListResult, tlog, "VALIDATION_ERROR", "itemsPerPage must be between 1 and 500", 400)
        if pageNum is not None and pageNum < 1:
            return _err(OrganizationProjectListResult, tlog, "VALIDATION_ERROR", "pageNum must be 1 or greater", 400)

        params: dict = {}
        if name is not None:
            params["name"] = name
        if includeCount is not None:
            params["includeCount"] = includeCount
        if itemsPerPage is not None:
            params["itemsPerPage"] = itemsPerPage
        if pageNum is not None:
            params["pageNum"] = pageNum
        if envelope is not None:
            params["envelope"] = envelope
        if pretty is not None:
            params["pretty"] = pretty

        try:
            data, status, retry_after = service.api_request(
                "GET", f"/orgs/{orgId}/groups", params=params or None, timeout=TIMEOUT,
            )
        except Exception as exc:
            return _handle_request_exc(OrganizationProjectListResult, tlog, exc)

        if not (200 <= status < 300):
            return _upstream_err(OrganizationProjectListResult, tlog, status, data, retry_after)

        tlog.success()
        return OrganizationProjectListResult(
            success=True, statusCode=status, data=OrganizationProjectListData(**data),
        )
