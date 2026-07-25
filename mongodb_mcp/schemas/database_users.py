"""Schemas for the database_users tool group (Atlas Admin API
/groups/{groupId}/databaseUsers endpoints).
"""

from typing import Any

from pydantic import BaseModel, ConfigDict

from ._base import ToolResult


class DatabaseUserData(BaseModel):
    """A single Atlas database user. `databaseName` + `username` identify the user."""

    model_config = ConfigDict(extra="allow")

    username: str | None = None
    databaseName: str | None = None
    awsIAMType: str | None = None
    deleteAfterDate: str | None = None
    description: str | None = None
    labels: list[dict[str, Any]] | None = None
    ldapAuthType: str | None = None
    oidcAuthType: str | None = None
    roles: list[dict[str, Any]] | None = None
    scopes: list[dict[str, Any]] | None = None
    x509Type: str | None = None
    links: list[dict[str, Any]] | None = None


class DatabaseUserResult(ToolResult):
    data: DatabaseUserData | None = None
