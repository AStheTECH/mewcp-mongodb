"""Schemas for the projects tool group (Atlas Admin API /groups endpoints).

Projects and groups are synonymous terms in the Atlas Admin API — the resource
and its endpoints use `groups`, but the MongoDB Cloud UI and this tool group
use `project`.
"""

from pydantic import BaseModel, ConfigDict

from ._base import ToolResult


class ProjectTagData(BaseModel):
    model_config = ConfigDict(extra="allow")

    key: str | None = None
    value: str | None = None


class ProjectLinkData(BaseModel):
    model_config = ConfigDict(extra="allow")

    href: str | None = None
    rel: str | None = None


class ProjectData(BaseModel):
    """A single Atlas project (a.k.a. group). `id` is what every other project endpoint takes."""

    model_config = ConfigDict(extra="allow")

    id: str | None = None
    name: str | None = None
    orgId: str | None = None
    clusterCount: int | None = None
    created: str | None = None
    regionUsageRestrictions: str | None = None
    withDefaultAlertsSettings: bool | None = None
    tags: list[ProjectTagData] | None = None
    links: list[ProjectLinkData] | None = None


class ProjectResult(ToolResult):
    data: ProjectData | None = None


class ProjectListData(BaseModel):
    model_config = ConfigDict(extra="allow")

    results: list[ProjectData]
    totalCount: int | None = None
    links: list[ProjectLinkData] | None = None


class ProjectListResult(ToolResult):
    data: ProjectListData | None = None


class ProjectUpdateData(BaseModel):
    """State of the project immediately before the update call, and after it."""

    model_config = ConfigDict(extra="allow")

    before: ProjectData
    after: ProjectData


class ProjectUpdateResult(ToolResult):
    data: ProjectUpdateData | None = None
