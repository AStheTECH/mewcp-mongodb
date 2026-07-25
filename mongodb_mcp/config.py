"""Configuration for MewCP MongoDB Atlas MCP Server."""

import logging
import os

SERVER_VERSION = "v1.1.0"
BREAKING_CHANGES: list[dict] = []

MONGODB_API_BASE = "https://cloud.mongodb.com/api/atlas/v2"
MONGODB_API_VERSION = "application/vnd.atlas.2025-03-12+json"  # pins Atlas Admin API response shape via Accept header

CONNECT_TIMEOUT = 5    # TCP connection — fixed across all servers
READ_TIMEOUT = 30      # Atlas control-plane reads/writes on projects and clusters; no long-running job endpoints in this build yet — no POLL_TIMEOUT needed


def configure_logging() -> None:
    log_level = os.environ.get("LOG_LEVEL", "INFO").upper()
    try:
        from pythonjsonlogger import jsonlogger
        handler = logging.StreamHandler()
        handler.setFormatter(
            jsonlogger.JsonFormatter(fmt="%(asctime)s %(name)s %(levelname)s %(message)s")
        )
    except ImportError:
        handler = logging.StreamHandler()
    root = logging.getLogger()
    root.handlers.clear()
    root.addHandler(handler)
    root.setLevel(log_level)
