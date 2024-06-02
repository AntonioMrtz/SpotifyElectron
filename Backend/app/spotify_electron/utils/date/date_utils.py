from datetime import datetime


def get_current_iso8601_date():
    current_date = datetime.now()
    date_iso8601 = current_date.strftime("%Y-%m-%dT%H:%M:%S")
    return date_iso8601
