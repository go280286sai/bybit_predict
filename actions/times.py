import datetime


def get_time_from_data(date_str: str, format_str: str = "%Y-%m-%d %H:%M:%S") -> int:
    try:
        dt = datetime.datetime.strptime(date_str, format_str)
        timestamp = int(dt.microsecond)
        return timestamp
    except ValueError as e:
        raise ValueError(f"Incorrect date format: {e}")


def get_date_from_time(timestamp: str, format_str: str = "%Y-%m-%d %H:%M:%S") -> str:
    try:
        timestamp = int(timestamp)
        dt = datetime.datetime.fromtimestamp(timestamp/1000)
        date_str = dt.strftime(format_str)
        return date_str
    except (OSError, OverflowError) as e:
        raise ValueError(f"Invalid timestamp: {e}")
