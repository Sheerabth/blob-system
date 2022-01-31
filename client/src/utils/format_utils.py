from datetime import datetime
from typing import Union

from dateutil import tz


def format_iso_string(iso_string: str) -> str:
    utc_time = datetime.fromisoformat(iso_string)
    local_time = utc_time.astimezone(tz.tzlocal())
    return local_time.strftime("%Y-%m-%d %H:%M:%S")


def auto_unit(number: Union[int, float]) -> str:
    """
    Returns a human-readable formatted size
    credit: glances
    """
    if number is None:
        return "-"
    units = [
        (1208925819614629174706176, "Y"),
        (1180591620717411303424, "Z"),
        (1152921504606846976, "E"),
        (1125899906842624, "P"),
        (1099511627776, "T"),
        (1073741824, "G"),
        (1048576, "M"),
        (1024, "K"),
    ]

    for unit, suffix in units:
        value = float(number) / unit
        if value > 1:
            precision = 0
            if value < 10:
                precision = 2
            elif value < 100:
                precision = 1
            if suffix == "K":
                precision = 0
            return "{:.{decimal}f}{suffix}".format(value, decimal=precision, suffix=suffix)

    return "{!s}".format(number)
