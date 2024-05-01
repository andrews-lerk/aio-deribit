from typing import Any

QueryParams = dict[str, Any]


def query_builder(**kwargs: QueryParams) -> str:
    """Build query string for HTTP URL."""
    query_string = ""
    for k, v in kwargs.items():
        query_string += f"&{k}={v}"
    return query_string
