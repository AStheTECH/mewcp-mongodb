"""MewCP MongoDB Atlas tool registration."""

from fastmcp import FastMCP

from .projects_tools import register_projects_tools
from .clusters_tools import register_clusters_tools


def register_tools(mcp: FastMCP) -> None:
    register_projects_tools(mcp)
    register_clusters_tools(mcp)
