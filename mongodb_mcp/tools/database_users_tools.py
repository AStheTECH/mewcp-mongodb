"""Database_users group: create_database_user, get_database_user."""

import logging
from typing import Any

from fastmcp import FastMCP
from mcp.types import ToolAnnotations
from pydantic import Field

from .. import service
from ..config import CONNECT_TIMEOUT, READ_TIMEOUT
from ..logging_utils import ToolLogger
from ..schemas.database_users import DatabaseUserData, DatabaseUserResult
from ._helpers import _err, _handle_request_exc, _upstream_err

logger = logging.getLogger("mongodb-mcp.tools.database_users")

TIMEOUT = (CONNECT_TIMEOUT, READ_TIMEOUT)


def register_database_users_tools(mcp: FastMCP) -> None:

    @mcp.tool(
        name="create_database_user",
        description=(
            "Creates one new database user with specified roles and authentication "
            "method for a project."
        ),
        annotations=ToolAnnotations(readOnlyHint=False, destructiveHint=False, openWorldHint=True),
    )
    def create_database_user(
        groupId: str = Field(
            description=(
                "Unique 24-hexadecimal digit string that identifies your project. Use "
                "the /groups endpoint to retrieve all projects to which the authenticated "
                "user has access. Groups and projects are synonymous terms."
            )
        ),
        databaseName: str = Field(
            description=(
                "The database against which the database user authenticates. If the "
                "user authenticates with AWS IAM, x.509, LDAP, or OIDC Workload this "
                "value should be $external. If the user authenticates with SCRAM-SHA or "
                "OIDC Workforce, this value should be admin. Values are admin or $external."
            )
        ),
        username: str = Field(
            description=(
                "Human-readable label that represents the user that authenticates to "
                "MongoDB. The format depends on the authentication method used (AWS IAM, "
                "x.509, LDAP, OIDC Workforce, OIDC Workload, or SCRAM-SHA). Maximum length "
                "is 1024."
            )
        ),
        roles: list[dict[str, Any]] = Field(
            description="List that provides the pairings of one role with one applicable database."
        ),
        password: str | None = Field(
            default=None,
            description=(
                "Alphanumeric string that authenticates this database user against the "
                "database specified in databaseName. Must be specified to authenticate "
                "with SCRAM-SHA. Does not appear in the response. Minimum length is 8. "
                "Optional."
            ),
        ),
        awsIAMType: str | None = Field(
            default=None,
            description=(
                "Human-readable label that indicates whether the new database user "
                "authenticates with AWS IAM credentials associated with the user or the "
                "user's role. Values are NONE, USER, or ROLE. Default value is NONE."
            ),
        ),
        deleteAfterDate: str | None = Field(
            default=None,
            description=(
                "Date and time when MongoDB Cloud deletes the user, expressed in ISO "
                "8601 UTC format. Must be a future date within one week of the request. "
                "Optional."
            ),
        ),
        description: str | None = Field(
            default=None,
            description="Description of this database user. Maximum length is 100. Optional.",
        ),
        labels: list[dict[str, Any]] | None = Field(
            default=None,
            description=(
                "List that contains the key-value pairs for tagging and categorizing the "
                "MongoDB database user. These labels do not appear in the console. Optional."
            ),
        ),
        ldapAuthType: str | None = Field(
            default=None,
            description=(
                "Part of the LDAP record that the database uses to authenticate this "
                "database user on the LDAP host. Values are NONE, GROUP, or USER. Default "
                "value is NONE."
            ),
        ),
        oidcAuthType: str | None = Field(
            default=None,
            description=(
                "Indicates whether the new database user or group authenticates with "
                "OIDC federated authentication. Specify USER to create a federated "
                "authentication user, or IDP_GROUP to create a federated authentication "
                "group. Values are NONE, IDP_GROUP, or USER. Default value is NONE."
            ),
        ),
        scopes: list[dict[str, Any]] | None = Field(
            default=None,
            description=(
                "List that contains clusters, MongoDB Atlas Data Lakes, and MongoDB "
                "Atlas Streams Workspaces that this database user can access. If omitted, "
                "MongoDB Cloud grants the database user access to all clusters, Data "
                "Lakes, and Streams Workspaces in the project. Optional."
            ),
        ),
        x509Type: str | None = Field(
            default=None,
            description=(
                "X.509 method that MongoDB Cloud uses to authenticate the database user. "
                "Specify MANAGED for application-managed X.509, or CUSTOMER for "
                "self-managed X.509. Values are NONE, CUSTOMER, or MANAGED. Default value "
                "is NONE."
            ),
        ),
        envelope: bool | None = Field(
            default=None,
            description=(
                "Flag that indicates whether the response is wrapped in an envelope JSON "
                "object, for API clients that cannot access HTTP response headers or "
                "status code. Default value is false. Optional."
            ),
        ),
        pretty: bool | None = Field(
            default=None,
            description=(
                "Flag that indicates whether the response body should be in the "
                "prettyprint format. Default value is false. Optional."
            ),
        ),
    ) -> DatabaseUserResult:
        tlog = ToolLogger(logger, "create_database_user")

        if not groupId or not groupId.strip():
            return _err(DatabaseUserResult, tlog, "VALIDATION_ERROR", "groupId must be a non-empty string", 400)
        if not databaseName or not databaseName.strip():
            return _err(DatabaseUserResult, tlog, "VALIDATION_ERROR", "databaseName must be a non-empty string", 400)
        if not username or not username.strip():
            return _err(DatabaseUserResult, tlog, "VALIDATION_ERROR", "username must be a non-empty string", 400)
        if not roles:
            return _err(DatabaseUserResult, tlog, "VALIDATION_ERROR", "roles must be a non-empty list", 400)
        if password is not None and len(password) < 8:
            return _err(DatabaseUserResult, tlog, "VALIDATION_ERROR", "password must be at least 8 characters", 400)

        body: dict = {"databaseName": databaseName, "username": username, "roles": roles}
        if password is not None:
            body["password"] = password
        if awsIAMType is not None:
            body["awsIAMType"] = awsIAMType
        if deleteAfterDate is not None:
            body["deleteAfterDate"] = deleteAfterDate
        if description is not None:
            body["description"] = description
        if labels is not None:
            body["labels"] = labels
        if ldapAuthType is not None:
            body["ldapAuthType"] = ldapAuthType
        if oidcAuthType is not None:
            body["oidcAuthType"] = oidcAuthType
        if scopes is not None:
            body["scopes"] = scopes
        if x509Type is not None:
            body["x509Type"] = x509Type

        params: dict = {}
        if envelope is not None:
            params["envelope"] = envelope
        if pretty is not None:
            params["pretty"] = pretty

        try:
            data, status, retry_after = service.api_request(
                "POST", f"/groups/{groupId}/databaseUsers",
                body=body, params=params or None, timeout=TIMEOUT,
            )
        except Exception as exc:
            return _handle_request_exc(DatabaseUserResult, tlog, exc)

        if not (200 <= status < 300):
            return _upstream_err(DatabaseUserResult, tlog, status, data, retry_after)

        tlog.success()
        return DatabaseUserResult(success=True, statusCode=status, data=DatabaseUserData(**data))

    @mcp.tool(
        name="get_database_user",
        description="Returns one database user by authentication database and username.",
        annotations=ToolAnnotations(readOnlyHint=True, destructiveHint=False, openWorldHint=True),
    )
    def get_database_user(
        groupId: str = Field(
            description=(
                "Unique 24-hexadecimal digit string that identifies your project. Use "
                "the /groups endpoint to retrieve all projects to which the authenticated "
                "user has access. Groups and projects are synonymous terms."
            )
        ),
        databaseName: str = Field(
            description=(
                "The database against which the database user authenticates. If the "
                "user authenticates with AWS IAM, x.509, LDAP, or OIDC Workload this "
                "value should be $external. If the user authenticates with SCRAM-SHA or "
                "OIDC Workforce, this value should be admin."
            )
        ),
        username: str = Field(
            description=(
                "Human-readable label that represents the user that authenticates to "
                "MongoDB. The format depends on the authentication method used (AWS IAM, "
                "x.509, LDAP, OIDC Workforce, OIDC Workload, or SCRAM-SHA)."
            )
        ),
        envelope: bool | None = Field(
            default=None,
            description=(
                "Flag that indicates whether the response is wrapped in an envelope JSON "
                "object, for API clients that cannot access HTTP response headers or "
                "status code. Default value is false. Optional."
            ),
        ),
        pretty: bool | None = Field(
            default=None,
            description=(
                "Flag that indicates whether the response body should be in the "
                "prettyprint format. Default value is false. Optional."
            ),
        ),
    ) -> DatabaseUserResult:
        tlog = ToolLogger(logger, "get_database_user")

        if not groupId or not groupId.strip():
            return _err(DatabaseUserResult, tlog, "VALIDATION_ERROR", "groupId must be a non-empty string", 400)
        if not databaseName or not databaseName.strip():
            return _err(DatabaseUserResult, tlog, "VALIDATION_ERROR", "databaseName must be a non-empty string", 400)
        if not username or not username.strip():
            return _err(DatabaseUserResult, tlog, "VALIDATION_ERROR", "username must be a non-empty string", 400)

        params: dict = {}
        if envelope is not None:
            params["envelope"] = envelope
        if pretty is not None:
            params["pretty"] = pretty

        try:
            data, status, retry_after = service.api_request(
                "GET", f"/groups/{groupId}/databaseUsers/{databaseName}/{username}",
                params=params or None, timeout=TIMEOUT,
            )
        except Exception as exc:
            return _handle_request_exc(DatabaseUserResult, tlog, exc)

        if not (200 <= status < 300):
            return _upstream_err(DatabaseUserResult, tlog, status, data, retry_after)

        tlog.success()
        return DatabaseUserResult(success=True, statusCode=status, data=DatabaseUserData(**data))
