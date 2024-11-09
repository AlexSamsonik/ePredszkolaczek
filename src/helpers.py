"""This module provides helper functions that are commonly used across different parts of the application."""

from calendar import monthrange
from datetime import date
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
