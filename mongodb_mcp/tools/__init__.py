"""MewCP MongoDB Atlas tool registration."""

from fastmcp import FastMCP

from .projects_tools import register_projects_tools
from .clusters_tools import register_clusters_tools
from .organizations_tools import register_organizations_tools
from .ip_access_list_tools import register_ip_access_list_tools
from .database_users_tools import register_database_users_tools


def register_tools(mcp: FastMCP) -> None:
    register_projects_tools(mcp)
    register_clusters_tools(mcp)
    register_organizations_tools(mcp)
    register_ip_access_list_tools(mcp)
    register_database_users_tools(mcp)
