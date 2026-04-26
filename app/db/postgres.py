import logging
from typing import Any, Optional

import psycopg2
from psycopg2.extras import Json

from app.core.config import settings

logger = logging.getLogger(__name__)


def run_query(query: str, params: Optional[tuple[Any, ...]] = None, fetch: bool = False) -> list[tuple[Any, ...]]:
    connection = None
    cursor = None
    try:
        connection = psycopg2.connect(
            host=settings.postgres_host,
            port=settings.postgres_port,
            dbname=settings.postgres_db,
            user=settings.postgres_user,
            password=settings.postgres_password,
        )
        cursor = connection.cursor()
        cursor.execute(query, params)
        rows = cursor.fetchall() if fetch else []
        connection.commit()
        return rows
    except Exception:
        logger.exception("Database query failed")
        return []
    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None:
            connection.close()


def as_json(value: dict[str, Any]) -> Json:
    return Json(value)
