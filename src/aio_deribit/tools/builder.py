from typing import Any


def query_builder(**kwargs: Any) -> str:
    query_string = ""
    for k, v in kwargs.items():
        query_string += f"&{k}={v}"
    return query_string
