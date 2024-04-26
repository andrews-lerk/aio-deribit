import datetime


def now_utc() -> int:
    return int(datetime.datetime.now(tz=datetime.UTC).timestamp()) * 1000
