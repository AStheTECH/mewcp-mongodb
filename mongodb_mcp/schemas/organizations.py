"""Schemas for the organizations tool group (Atlas Admin API /orgs endpoints)."""

from pydantic import BaseModel, ConfigDict

from ._base import ToolResult
from .projects import ProjectData


class OrganizationLinkData(BaseModel):
    model_config = ConfigDict(extra="allow")

    href: str | None = None
    rel: str | None = None


class OrganizationData(BaseModel):
    """A single MongoDB Cloud organization. `id` is what every other organization endpoint takes."""

    model_config = ConfigDict(extra="allow")

    id: str | None = None
    name: str | None = None
    isDeleted: bool | None = None
    skipDefaultAlertsSettings: bool | None = None
    links: list[OrganizationLinkData] | None = None


class OrganizationResult(ToolResult):
    data: OrganizationData | None = None


class OrganizationListData(BaseModel):
    model_config = ConfigDict(extra="allow")

    results: list[OrganizationData]
    totalCount: int | None = None
    links: list[OrganizationLinkData] | None = None


class OrganizationListResult(ToolResult):
    data: OrganizationListData | None = None


class OrganizationProjectListData(BaseModel):
    """Projects belonging to one organization. Reuses `ProjectData` — same fields as /groups."""

    model_config = ConfigDict(extra="allow")

    results: list[ProjectData]
    totalCount: int | None = None
    links: list[OrganizationLinkData] | None = None


class OrganizationProjectListResult(ToolResult):
    data: OrganizationProjectListData | None = None
