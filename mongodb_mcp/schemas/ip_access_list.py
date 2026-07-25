"""IP access list group schemas: list_ip_access_list_entries, get_ip_access_list_entry."""

from pydantic import BaseModel, ConfigDict

from ._base import ToolResult


class IpAccessListEntryData(BaseModel):
    model_config = ConfigDict(extra="allow")

    awsSecurityGroup: str | None = None
    cidrBlock: str | None = None
    comment: str | None = None
    deleteAfterDate: str | None = None
    groupId: str | None = None
    ipAddress: str | None = None
    links: list | None = None


class IpAccessListEntryResult(ToolResult):
    data: IpAccessListEntryData | None = None


class IpAccessListEntryListData(BaseModel):
    model_config = ConfigDict(extra="allow")

    links: list | None = None
    results: list[IpAccessListEntryData]
    totalCount: int


class IpAccessListEntryListResult(ToolResult):
    data: IpAccessListEntryListData | None = None
