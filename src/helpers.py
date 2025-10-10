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


def print_calculation(first_name: str, presenting: list) -> None:
    """Calculate and log the total days, meal payments, hours, and hour payments for a child in kindergarten.

    :param first_name: The first name of the child.
    :param presenting: List of dictionaries, each containing 'Wejscie' (entrance) and 'Wyjscie' (exit) times.
    """
    hours = sum([(calculate_interval_hours(i["Wejscie"], i["Wyjscie"])) for i in presenting])

    logger.info(f"{first_name}. Days in kindergarten: '{len(presenting)}'.")
    rounded_meals_payment = round(len(presenting) * int(environ["PAYMENT_FOR_MEALS_FOR_DAY"]), 2)
    logger.info(f"{first_name}. Payment for meals: '{'{:.2f}'.format(rounded_meals_payment)}' zl.")

    logger.info(f"{first_name}. Hours in kindergarten: '{hours}'.")
    rounded_hours_payment = round(hours * float(environ["PAYMENT_FOR_HOUR"]), 2)
    logger.info(f"{first_name}. Payment for hours: '{'{:.2f}'.format(rounded_hours_payment)}' zl.")


def compose_string_from_dict_list(dict_list, field_order):
    """Composes a formatted string from values of specified keys in the given order.

    Format for result string: "field1=value1; field2=value2; field3=value3"

    :param dict_list: List of dictionaries (e.g. [{"name": "field_01", "value": "Value_01", "others": "values"})
    :param field_order: List of field names in the required order (e.g. ["field_01", "field_02", "field_03"])

    :raise ValueError: If any of the required keys is missing in the list of dictionaries
    :return: String composed of corresponding key-value pairs in the required format
    """
    # Initialize a dictionary to store found values
    field_values = {field: None for field in field_order}

    # Find the required keys in dictionaries
    for d in dict_list:
        if d.get("name") in field_order:
            field_values[d["name"]] = d["value"]

    # Check that all keys were found
    missing_fields = [field for field in field_order if field_values[field] is None]
    if missing_fields:
        raise ValueError(f"Keys '{missing_fields}' not found in any dictionary.")

    # Compose the string in the required order with proper formatting
    result_parts = []
    for field in field_order:
        result_parts.append(f"{field}={field_values[field]}")

    # Join with the specified separator
    result = "; ".join(result_parts)

    return result


def extract_entrance_exit_times(attendance_data: dict) -> list:
    """Extract entrance and exit times from the attendance response.

    :param attendance_data: Dictionary containing attendance data.
    :return: List of dictionaries, each containing 'Wejscie' (entrance) and 'Wyjscie' (exit) times.
    """
    # Initialize the result list
    result = []

    # Extract the 'Obecnosci' dictionary from the attendance data
    obecnosci = attendance_data.get("d", {}).get("Obecnosci", {})

    # Iterate through each entry in 'Obecnosci'
    for day_key, day_data in obecnosci.items():
        # Extract the entrance and exit times
        entrance = day_data.get("Wejscie", "-")
        exit_time = day_data.get("Wyjscie", "-")

        # Skip entries where either entrance or exit time is '-'
        if entrance == "-" or exit_time == "-":
            continue

        # Add a dictionary with the extracted times to the result list
        result.append({"Wejscie": entrance, "Wyjscie": exit_time})

    return result
