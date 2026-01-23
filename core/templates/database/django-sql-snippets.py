"""
Django SQL Snippets - Template/Snippet Reutilizável

This module provides helper functions for executing raw SQL queries safely,
converting query results to lists or dictionaries, and escaping SQL values.
It protects against SQL injection by using parameterized queries.

**IMPORTANTE:** Este é um template/snippet. Copie e adapte para seu projeto.

Usage:
    from core.templates.database.django_sql_snippets import sql_to_dict, sql_to_list, query_value, exec_sql, sql_escape

    # Get results as list of dicts
    results = sql_to_dict("SELECT * FROM users WHERE email = %s", param=("user@example.com",))

    # Get single value
    count = query_value("SELECT COUNT(*) FROM users")

    # Execute update
    exec_sql("UPDATE users SET status = 'active' WHERE id = %s", param=(user_id,))
"""

import logging
from typing import Any, Dict, List, Optional, Tuple, Union

try:
    from django.conf import settings
    from django.db import connections, transaction
    DJANGO_AVAILABLE = True
except ImportError:
    DJANGO_AVAILABLE = False
    settings = None
    connections = None
    transaction = None

logger = logging.getLogger(__name__)


def sql_to_list(
    select_sql: str,
    field: str,
    param: Optional[Union[Tuple, List, Dict]] = None,
    database_alias: Optional[str] = "default",
) -> List[Any]:
    """
    Execute a SQL query and return a list of values for a specific field.

    Args:
        select_sql: The SQL SELECT statement to execute (use %s for parameters).
        field: The field name to extract from each row.
        param: Parameter(s) to pass to the SQL query (tuple, list, or dict).
        database_alias: The database alias to use (default: "default").

    Returns:
        List: A list of values for the specified field from the query result.

    Raises:
        ImportError: If Django is not available.
        AssertionError: If the database_alias is not defined in settings.DATABASES.
        KeyError: If the specified field does not exist in the result.
    """
    if not DJANGO_AVAILABLE:
        raise ImportError("Django is required for this function. Install django or use SQLAlchemy version.")

    results = sql_to_dict(select_sql, param=param, database_alias=database_alias)
    return [r[field] for r in results]


def sql_to_dict(
    select_sql: str,
    param: Optional[Union[Tuple, List, Dict]] = None,
    database_alias: Optional[str] = "default",
) -> List[Dict[str, Any]]:
    """
    Execute a SQL query and return the result as a list of dictionaries.

    This function uses parameterized queries to protect against SQL injection.

    Args:
        select_sql: The SQL SELECT statement to execute (use %s for parameters).
        param: Parameter(s) to pass to the SQL query (tuple, list, or dict).
        database_alias: The database alias to use (default: "default").

    Returns:
        List[Dict[str, Any]]: A list of dictionaries, each representing a row.

    Raises:
        ImportError: If Django is not available.
        AssertionError: If the database_alias is not defined in settings.DATABASES.
        Exception: If the SQL execution fails.
    """
    if not DJANGO_AVAILABLE:
        raise ImportError("Django is required for this function. Install django or use SQLAlchemy version.")

    assert database_alias in settings.DATABASES, f"Database alias '{database_alias}' not found in settings.DATABASES"

    cursor = connections[database_alias].cursor()
    cursor.execute(select_sql, param)
    fields_names = [name[0] for name in cursor.description]
    return [dict(zip(fields_names, row)) for row in cursor.fetchall()]


def query_value(
    select_sql: str,
    param: Optional[Union[Tuple, List, Dict]] = None,
    database_alias: Optional[str] = "default",
) -> Optional[Any]:
    """
    Execute a SQL query and return the value of the first column of the first row.

    Args:
        select_sql: The SQL SELECT statement to execute (use %s for parameters).
        param: Parameter(s) to pass to the SQL query (tuple, list, or dict).
        database_alias: The database alias to use (default: "default").

    Returns:
        Any: The value of the first column of the first row, or None if no result.

    Raises:
        ImportError: If Django is not available.
        AssertionError: If the database_alias is not defined in settings.DATABASES.
        Exception: If the SQL execution fails.
    """
    if not DJANGO_AVAILABLE:
        raise ImportError("Django is required for this function. Install django or use SQLAlchemy version.")

    assert database_alias in settings.DATABASES, f"Database alias '{database_alias}' not found in settings.DATABASES"

    cursor = connections[database_alias].cursor()
    cursor.execute(select_sql, param)
    result = cursor.fetchone()
    return result[0] if result else None


def exec_sql(
    sql_command: str,
    param: Optional[Union[Tuple, List, Dict]] = None,
    database_alias: Optional[str] = "default",
) -> None:
    """
    Execute a SQL command (such as INSERT, UPDATE, DELETE) on the specified database.

    This function uses parameterized queries and transactions to ensure data integrity.

    Args:
        sql_command: The SQL command to execute (use %s for parameters).
        param: Parameter(s) to pass to the SQL command (tuple, list, or dict).
        database_alias: The database alias to use (default: "default").

    Returns:
        None

    Raises:
        ImportError: If Django is not available.
        AssertionError: If the database_alias is not defined in settings.DATABASES.
        Exception: If the SQL execution or commit fails.
    """
    if not DJANGO_AVAILABLE:
        raise ImportError("Django is required for this function. Install django or use SQLAlchemy version.")

    assert database_alias in settings.DATABASES, f"Database alias '{database_alias}' not found in settings.DATABASES"

    with transaction.atomic(using=database_alias):
        con = connections[database_alias]
        cursor = con.cursor()
        cursor.execute(sql_command, param)
        con.commit()


def sql_escape(value: str) -> str:
    """
    Escape special characters in a string for safe use in SQL queries.

    **WARNING:** This function should only be used when parameterized queries are not possible.
    Prefer using parameterized queries (%s placeholders) instead of this function.

    Args:
        value: The string value to escape.

    Returns:
        str: The escaped string, with percent signs and single quotes handled.
    """
    if not isinstance(value, str):
        value = str(value)
    return value.replace(r"%", "").replace("'", "''")

