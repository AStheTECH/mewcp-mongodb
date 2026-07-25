"""IP access list group: list_ip_access_list_entries, get_ip_access_list_entry."""

import logging

from fastmcp import FastMCP
from mcp.types import ToolAnnotations
from pydantic import Field

from .. import service
from ..config import CONNECT_TIMEOUT, READ_TIMEOUT
from ..logging_utils import ToolLogger
from ..schemas.ip_access_list import (
    IpAccessListEntryData,
    IpAccessListEntryListData,
    IpAccessListEntryListResult,
    IpAccessListEntryResult,
)
from ._helpers import _err, _handle_request_exc, _upstream_err

logger = logging.getLogger("mongodb-mcp.tools.ip_access_list")


def register_ip_access_list_tools(mcp: FastMCP) -> None:

    @mcp.tool(
        name="list_ip_access_list_entries",
        description="Returns all IP access list entries for one project.",
        annotations=ToolAnnotations(readOnlyHint=True, destructiveHint=False, openWorldHint=True),
    )
    def list_ip_access_list_entries(
        group_id: str = Field(
            description="Unique 24-hexadecimal digit string that identifies your project. Use the /groups endpoint to retrieve all projects to which the authenticated user has access. Format should match the following pattern: ^([a-f0-9]{24})$."
        ),
        envelope: bool = Field(
            default=False, description="Flag that indicates whether Application wraps the response in an envelope JSON object. Some API clients cannot access the HTTP response headers or status code. To remediate this, set envelope=true in the query. Endpoints that return a list of results use the results object as an envelope. Application adds the status parameter to the response body. Optional, defaults to false."
        ),
        include_count: bool = Field(
            default=True, description="Flag that indicates whether the response returns the total number of items (totalCount) in the response. Optional, defaults to true."
        ),
        items_per_page: int = Field(
            default=100, description="Number of items that the response returns per page. Minimum value is 1, maximum value is 500. Optional, defaults to 100."
        ),
        page_num: int = Field(
            default=1, description="Number of the page that displays the current set of the total objects that the response returns. Minimum value is 1. Optional, defaults to 1."
        ),
        pretty: bool = Field(
            default=False, description="Flag that indicates whether the response body should be in the prettyprint format. Optional, defaults to false."
        ),
    ) -> IpAccessListEntryListResult:
        tlog = ToolLogger(logger, "list_ip_access_list_entries")

        if not group_id or not group_id.strip():
            return _err(IpAccessListEntryListResult, tlog, "VALIDATION_ERROR", "group_id is required", 400)
        if items_per_page < 1 or items_per_page > 500:
            return _err(IpAccessListEntryListResult, tlog, "VALIDATION_ERROR", "items_per_page must be 1-500", 400)
        if page_num < 1:
            return _err(IpAccessListEntryListResult, tlog, "VALIDATION_ERROR", "page_num must be >= 1", 400)

        try:
            data, status, retry_after = service.api_request(
                "GET", f"/groups/{group_id}/accessList",
                params={
                    "envelope": envelope,
                    "includeCount": include_count,
                    "itemsPerPage": items_per_page,
                    "pageNum": page_num,
                    "pretty": pretty,
                },
                timeout=(CONNECT_TIMEOUT, READ_TIMEOUT),
            )
            if 200 <= status < 300:
                tlog.success()
                return IpAccessListEntryListResult(success=True, statusCode=status, data=IpAccessListEntryListData(**data))
            return _upstream_err(IpAccessListEntryListResult, tlog, status, data, retry_after)
        except Exception as exc:
            return _handle_request_exc(IpAccessListEntryListResult, tlog, exc)

    @mcp.tool(
        name="get_ip_access_list_entry",
        description="Returns one IP access list entry by its value.",
        annotations=ToolAnnotations(readOnlyHint=True, destructiveHint=False, openWorldHint=True),
    )
    def get_ip_access_list_entry(
        group_id: str = Field(
            description="Unique 24-hexadecimal digit string that identifies your project. Use the /groups endpoint to retrieve all projects to which the authenticated user has access. Format should match the following pattern: ^([a-f0-9]{24})$."
        ),
        entry_value: str = Field(
            description="Access list entry that you want to return from the project's IP access list. This value can use one of the following: one AWS security group ID, one IP address, or one CIDR block of addresses. For CIDR blocks that use a subnet mask, replace the forward slash (/) with its URL-encoded value (%2F). Format should match the following pattern: ^([0-9]{1,3}\\.){3}[0-9]{1,3}(%2[fF][0-9]{1,3})?|([0-9a-f]{1,4}\\:){7}[0-9a-f]{1,4}(%2[fF][0-9]{1,3})?|([0-9a-f]{1,4}\\:){1,6}\\:(%2[fF][0-9]{1,3})|(sg\\-[a-f0-9]{8})?$."
        ),
        envelope: bool = Field(
            default=False, description="Flag that indicates whether Application wraps the response in an envelope JSON object. Some API clients cannot access the HTTP response headers or status code. To remediate this, set envelope=true in the query. Endpoints that return a list of results use the results object as an envelope. Application adds the status parameter to the response body. Optional, defaults to false."
        ),
        pretty: bool = Field(
            default=False, description="Flag that indicates whether the response body should be in the prettyprint format. Optional, defaults to false."
        ),
    ) -> IpAccessListEntryResult:
        tlog = ToolLogger(logger, "get_ip_access_list_entry")

        if not group_id or not group_id.strip():
            return _err(IpAccessListEntryResult, tlog, "VALIDATION_ERROR", "group_id is required", 400)
        if not entry_value or not entry_value.strip():
            return _err(IpAccessListEntryResult, tlog, "VALIDATION_ERROR", "entry_value is required", 400)

        try:
            data, status, retry_after = service.api_request(
                "GET", f"/groups/{group_id}/accessList/{entry_value}",
                params={
                    "envelope": envelope,
                    "pretty": pretty,
                },
                timeout=(CONNECT_TIMEOUT, READ_TIMEOUT),
            )
            if 200 <= status < 300:
                tlog.success()
                return IpAccessListEntryResult(success=True, statusCode=status, data=IpAccessListEntryData(**data))
            return _upstream_err(IpAccessListEntryResult, tlog, status, data, retry_after)
        except Exception as exc:
            return _handle_request_exc(IpAccessListEntryResult, tlog, exc)
