import datetime


def now_utc() -> int:
    """Return UTC timestamp in milliseconds."""
    return int(datetime.datetime.now(tz=datetime.UTC).timestamp()) * 1000
