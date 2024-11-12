"""This module provides helper functions that are commonly used across different parts of the application."""

from calendar import monthrange
from datetime import date
from datetime import datetime
from math import ceil
from os import environ
from typing import Union, Tuple


def get_first_and_last_day_of_month(
    month: Union[str, int, None] = None, year: Union[str, int, None] = None
) -> Tuple[str, str]:
    """Calculate the first and last day of the specified month and year, or the current month and year if not specified.

    :param month: Optional; an integer (1-12) or a string representing the month. If not specified, the current month is used.
    :param year: Optional; an integer representing the year or a string that can be converted to an integer. If not specified, the current year is used.
    :return: A tuple containing two strings, the first and last day of the specified or current month and year in 'YYYY-MM-DD' format.
    """
    today = date.today()
    if year is None:
        year = today.year
    else:
        if isinstance(year, str) or isinstance(year, int):
            year = int(year)
        else:
            raise ValueError("Year must be a string or integer that can be converted to an integer")

    if month is None:
        month = today.month
    else:
        if isinstance(month, str) or isinstance(month, int):
            month = int(month)
        else:
            raise ValueError("Month must be a string or integer that can be converted to an integer")

    if not 1 <= month <= 12:
        raise ValueError("Month must be between 1 and 12")

    first_day = date(year, month, 1)
    last_day = date(year, month, monthrange(year, month)[1])
    return first_day.strftime("%Y-%m-%d"), last_day.strftime("%Y-%m-%d")


def calculate_interval_hours(start_time, end_time) -> int:
    """Calculate the total number of hours outside the interval for a given time range.

    :param start_time: Start time in the format "HH:MM", representing the beginning of the interval.
    :param end_time: End time in the format "HH:MM", representing the end of the interval.
    :return: Total number of full hours outside the interval, rounded up to the nearest hour.
    """
    time_format = "%H:%M"

    time_start_arrival = datetime.strptime(start_time, time_format)
    time_end_arrival = datetime.strptime(end_time, time_format)

    time_start = datetime.strptime(environ["TIME_START"], time_format)
    time_end = datetime.strptime(environ["TIME_END"], time_format)

    total_hours: int = 0

    if time_start_arrival < time_start:
        end_time = min(time_start, time_end_arrival)
        delta = end_time - time_start_arrival
        total_hours += ceil(delta.seconds / 3600)

    if time_end_arrival > time_end:
        start_time = max(time_end, time_start_arrival)
        delta = time_end_arrival - start_time
        total_hours += ceil(delta.seconds / 3600)

    return total_hours
