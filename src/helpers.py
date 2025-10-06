"""This module provides helper functions that are commonly used across different parts of the application."""

from datetime import datetime
from math import ceil
from os import environ
import logging


logger = logging.getLogger(__name__)
logging.basicConfig(format="%(asctime)s [%(levelname)8s] %(message)s (%(filename)s:%(lineno)s)", level=logging.INFO)


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


def print_calculation(first_name: str, presenting: dict) -> None:
    """Calculate and log the total days, meal payments, hours, and hour payments for a child in kindergarten.

    :param first_name: The first name of the child.
    :param presenting: Dictionary with actual start_time and end_time for each day.
    """
    hours = sum([(calculate_interval_hours(i["start_time"], i["end_time"])) for i in presenting])

    logger.info(f"{first_name}. Days in kindergarten: '{len(presenting)}'.")
    rounded_meals_payment = round(len(presenting) * int(environ["PAYMENT_FOR_MEALS_FOR_DAY"]), 2)
    logger.info(f"{first_name}. Payment for meals: '{'{:.2f}'.format(rounded_meals_payment)}' zl.")

    logger.info(f"{first_name}. Hours in kindergarten: '{hours}'.")
    rounded_hours_payment = round(hours * float(environ["PAYMENT_FOR_HOUR"]), 2)
    logger.info(f"{first_name}. Payment for hours: '{'{:.2f}'.format(rounded_hours_payment)}' zl.")
