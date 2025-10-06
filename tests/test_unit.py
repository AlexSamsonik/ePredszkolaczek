"""There are tests for helpers functions."""

import pytest

from src.helpers import calculate_interval_hours
from dotenv import load_dotenv

load_dotenv()


@pytest.mark.parametrize(
    "start_time, end_time, expected_hours",
    [
        ("07:59", "08:00", 1),
        ("07:00", "08:00", 1),
        ("06:30", "07:45", 2),
        ("08:00", "13:00", 0),
        ("08:00", "13:01", 1),
        ("12:59", "13:01", 1),
        ("13:00", "14:00", 1),
        ("13:01", "15:00", 2),
        ("07:00", "14:00", 2),
        ("07:00", "15:00", 3),
        ("07:59", "13:01", 2),
        ("07:59", "14:00", 2),
        ("07:30", "08:30", 1),
        ("12:30", "14:30", 2),
        ("13:59", "15:59", 2),
        ("06:00", "16:00", 5),
        ("07:00", "13:00", 1),
        ("13:00", "13:01", 1),
        ("07:59", "08:01", 1),
        ("12:59", "13:02", 1),
        ("08:04", "14:09", 2),
    ],
)
def test_calculate_interval_hours(start_time, end_time, expected_hours):
    """Test validate correctly calculates the total hours outside the core time interval.

    :param start_time: Start time in the format "HH:MM", representing the beginning of the interval.
    :param end_time: End time in the format "HH:MM", representing the end of the interval.
    :param expected_hours: Expected total hours outside the core time interval, used for assertion.
    :return: None. Asserts the function output against expected_hours.
    """
    assert calculate_interval_hours(start_time, end_time) == expected_hours
