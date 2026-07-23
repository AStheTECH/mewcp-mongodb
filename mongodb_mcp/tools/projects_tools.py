"""Projects group: create_project, delete_project, get_project, list_projects, update_project."""

import logging

from fastmcp import FastMCP
from mcp.types import ToolAnnotations
from pydantic import Field

from .. import service
from ..config import CONNECT_TIMEOUT, READ_TIMEOUT
from ..logging_utils import ToolLogger
from ..schemas.projects import (
    ProjectData,
    ProjectListData,
    ProjectListResult,
    ProjectResult,
    ProjectUpdateData,
    ProjectUpdateResult,
)
from ._helpers import _err, _handle_request_exc, _upstream_err

logger = logging.getLogger("mongodb-mcp.tools.projects")

TIMEOUT = (CONNECT_TIMEOUT, READ_TIMEOUT)


def register_projects_tools(mcp: FastMCP) -> None:

    @mcp.tool(
        name="create_project",
        description=(
            "Creates one new project inside a MongoDB Cloud organization and returns the "
            "created project's details, including its generated `id`."
        ),
        annotations=ToolAnnotations(readOnlyHint=False, destructiveHint=False, openWorldHint=True),
    )
    def create_project(
        name: str = Field(
            description=(
                "Human-readable label that identifies the project, as a plain string "
                "1-64 characters (e.g. 'Production'). Required."
            )
        ),
        orgId: str = Field(
            description=(
                "Unique 24-hexadecimal digit string that identifies the MongoDB Cloud "
                "organization the project belongs to (e.g. '32b6e34b3d91647abb20e7b8'). "
                "Required."
            )
        ),
        regionUsageRestrictions: str | None = Field(
            default=None,
            description=(
                "Atlas for Government only — restricts available regions for the project. "
                "One of 'COMMERCIAL_FEDRAMP_REGIONS_ONLY' or 'GOV_REGIONS_ONLY'. In "
                "commercial Atlas this field is rejected by the API. Optional, defaults to "
                "'COMMERCIAL_FEDRAMP_REGIONS_ONLY' on the server."
            ),
        ),
        tags: list[dict[str, str]] | None = Field(
            default=None,
            description=(
                "List of key-value pairs for tagging and categorizing the project, e.g. "
                "[{'key': 'env', 'value': 'prod'}]. Each key and value must be 1-255 "
                "characters. Optional."
            ),
        ),
        withDefaultAlertsSettings: bool | None = Field(
            default=None,
            description=(
                "Whether to create the project with default alert settings. Optional, "
                "defaults to true on the server."
            ),
        ),
        projectOwnerId: str | None = Field(
            default=None,
            description=(
                "Unique 24-hexadecimal digit string that identifies the MongoDB Cloud user "
                "to grant the Project Owner role on the new project. Overrides the default "
                "of the oldest Organization Owner. Optional — sent as a query parameter."
            ),
        ),
    ) -> ProjectResult:
        tlog = ToolLogger(logger, "create_project")

        if not name or not name.strip():
            return _err(ProjectResult, tlog, "VALIDATION_ERROR", "name must be a non-empty string", 400)
        if not orgId or not orgId.strip():
            return _err(ProjectResult, tlog, "VALIDATION_ERROR", "orgId must be a non-empty string", 400)

        body: dict = {"name": name, "orgId": orgId}
        if regionUsageRestrictions is not None:
            body["regionUsageRestrictions"] = regionUsageRestrictions
        if tags is not None:
            body["tags"] = tags
        if withDefaultAlertsSettings is not None:
            body["withDefaultAlertsSettings"] = withDefaultAlertsSettings

        params = {"projectOwnerId": projectOwnerId} if projectOwnerId else None

        try:
            data, status, retry_after = service.api_request(
                "POST", "/groups", body=body, params=params, timeout=TIMEOUT,
            )
        except Exception as exc:
            return _handle_request_exc(ProjectResult, tlog, exc)

        if not (200 <= status < 300):
            return _upstream_err(ProjectResult, tlog, status, data, retry_after)

        tlog.success()
        return ProjectResult(success=True, statusCode=status, data=ProjectData(**data))

    @mcp.tool(
        name="get_project",
        description=(
            "Returns one project by its unique ID, including cluster count, tags, and "
            "organization details."
        ),
        annotations=ToolAnnotations(readOnlyHint=True, destructiveHint=False, openWorldHint=True),
    )
    def get_project(
        groupId: str = Field(
            description=(
                "Unique 24-hexadecimal digit string that identifies the project "
                "(e.g. '32b6e34b3d91647abb20e7b8'). Groups and projects are synonymous "
                "terms — your group id is the same as your project id. Required."
            )
        ),
    ) -> ProjectResult:
        tlog = ToolLogger(logger, "get_project")

        if not groupId or not groupId.strip():
            return _err(ProjectResult, tlog, "VALIDATION_ERROR", "groupId must be a non-empty string", 400)

        try:
            data, status, retry_after = service.api_request(
                "GET", f"/groups/{groupId}", timeout=TIMEOUT,
            )
        except Exception as exc:
            return _handle_request_exc(ProjectResult, tlog, exc)

        if not (200 <= status < 300):
            return _upstream_err(ProjectResult, tlog, status, data, retry_after)

        tlog.success()
        return ProjectResult(success=True, statusCode=status, data=ProjectData(**data))

    @mcp.tool(
        name="list_projects",
        description="Returns all projects to which the requesting service account has access.",
        annotations=ToolAnnotations(readOnlyHint=True, destructiveHint=False, openWorldHint=True),
    )
    def list_projects(
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
    ) -> ProjectListResult:
        tlog = ToolLogger(logger, "list_projects")

        if itemsPerPage is not None and not (1 <= itemsPerPage <= 500):
            return _err(ProjectListResult, tlog, "VALIDATION_ERROR", "itemsPerPage must be between 1 and 500", 400)
        if pageNum is not None and pageNum < 1:
            return _err(ProjectListResult, tlog, "VALIDATION_ERROR", "pageNum must be 1 or greater", 400)

        params: dict = {}
        if includeCount is not None:
            params["includeCount"] = includeCount
        if itemsPerPage is not None:
            params["itemsPerPage"] = itemsPerPage
        if pageNum is not None:
            params["pageNum"] = pageNum

        try:
            data, status, retry_after = service.api_request(
                "GET", "/groups", params=params or None, timeout=TIMEOUT,
            )
        except Exception as exc:
            return _handle_request_exc(ProjectListResult, tlog, exc)

        if not (200 <= status < 300):
            return _upstream_err(ProjectListResult, tlog, status, data, retry_after)

        tlog.success()
        return ProjectListResult(success=True, statusCode=status, data=ProjectListData(**data))

    @mcp.tool(
        name="update_project",
        description=(
            "Updates the name, tags, or default alert settings of one project. Only the "
            "fields you provide are changed — others keep their current value. "
            "NOTE: this overwrites the current field values — the original state is not "
            "stored after the call. "
            "The response includes both the before and after state so you have a full "
            "record of what changed."
        ),
        annotations=ToolAnnotations(readOnlyHint=False, destructiveHint=False, openWorldHint=True),
    )
    def update_project(
        groupId: str = Field(
            description=(
                "Unique 24-hexadecimal digit string that identifies the project to update "
                "(e.g. '32b6e34b3d91647abb20e7b8'). Required."
            )
        ),
        name: str | None = Field(
            default=None,
            description="New human-readable label for the project. Optional — leave unset to keep the current name.",
        ),
        tags: list[dict[str, str]] | None = Field(
            default=None,
            description=(
                "New list of key-value pairs for tagging and categorizing the project, e.g. "
                "[{'key': 'env', 'value': 'staging'}]. Replaces the current tags entirely. "
                "Optional — leave unset to keep the current tags."
            ),
        ),
        withDefaultAlertsSettings: bool | None = Field(
            default=None,
            description=(
                "Whether the project can automatically create default alerts. Optional — "
                "leave unset to keep the current setting."
            ),
        ),
    ) -> ProjectUpdateResult:
        tlog = ToolLogger(logger, "update_project")

        if not groupId or not groupId.strip():
            return _err(ProjectUpdateResult, tlog, "VALIDATION_ERROR", "groupId must be a non-empty string", 400)
        if name is None and tags is None and withDefaultAlertsSettings is None:
            return _err(
                ProjectUpdateResult, tlog, "VALIDATION_ERROR",
                "At least one of name, tags, or withDefaultAlertsSettings must be provided", 400,
            )

        try:
            before_data, before_status, before_retry = service.api_request(
                "GET", f"/groups/{groupId}", timeout=TIMEOUT,
            )
            if not (200 <= before_status < 300):
                return _upstream_err(ProjectUpdateResult, tlog, before_status, before_data, before_retry)

            body: dict = {}
            if name is not None:
                body["name"] = name
            if tags is not None:
                body["tags"] = tags
            if withDefaultAlertsSettings is not None:
                body["withDefaultAlertsSettings"] = withDefaultAlertsSettings

            after_data, status, retry_after = service.api_request(
                "PATCH", f"/groups/{groupId}", body=body, timeout=TIMEOUT,
            )
        except Exception as exc:
            return _handle_request_exc(ProjectUpdateResult, tlog, exc)

        if not (200 <= status < 300):
            return _upstream_err(ProjectUpdateResult, tlog, status, after_data, retry_after)

        tlog.success()
        return ProjectUpdateResult(
            success=True, statusCode=status,
            data=ProjectUpdateData(before=ProjectData(**before_data), after=ProjectData(**after_data)),
        )

    @mcp.tool(
        name="delete_project",
        description=(
            "DESTRUCTIVE — REQUIRES EXPLICIT USER CONFIRMATION BEFORE CALLING. "
            "Permanently removes one project, which must have no clusters. "
            "This action is irreversible — the project and its configuration cannot be "
            "recovered. "
            "NEVER call this tool autonomously or as part of an automated flow. "
            "You MUST stop, tell the user exactly what will be deleted and that it is "
            "permanent, and wait for their explicit written confirmation before proceeding."
        ),
        annotations=ToolAnnotations(readOnlyHint=False, destructiveHint=True, openWorldHint=True),
    )
    def delete_project(
        groupId: str = Field(
            description=(
                "Unique 24-hexadecimal digit string that identifies the project to remove "
                "(e.g. '32b6e34b3d91647abb20e7b8'). The project must have no clusters. "
                "Required."
            )
        ),
    ) -> ProjectResult:
        tlog = ToolLogger(logger, "delete_project")

        if not groupId or not groupId.strip():
            return _err(ProjectResult, tlog, "VALIDATION_ERROR", "groupId must be a non-empty string", 400)

        try:
            data, status, retry_after = service.api_request(
                "DELETE", f"/groups/{groupId}", timeout=TIMEOUT,
            )
        except Exception as exc:
            return _handle_request_exc(ProjectResult, tlog, exc)

        if not (200 <= status < 300):
            return _upstream_err(ProjectResult, tlog, status, data, retry_after)

        # 204 No Content on success — nothing to parse into ProjectData.
        tlog.success()
        return ProjectResult(success=True, statusCode=204, data=None)
