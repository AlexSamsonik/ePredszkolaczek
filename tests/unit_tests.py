"""There are tests for helpers functions."""

import pytest

from src.helpers import get_first_and_last_day_of_month


@pytest.mark.parametrize(
    "month, year, expected",
    [
        (1, 2022, ("2022-01-01", "2022-01-31")),
        (2, 2024, ("2024-02-01", "2024-02-29")),
        (2, 2023, ("2023-02-01", "2023-02-28")),
        (3, 2022, ("2022-03-01", "2022-03-31")),
        (4, 2022, ("2022-04-01", "2022-04-30")),
        (5, 2022, ("2022-05-01", "2022-05-31")),
        (6, 2022, ("2022-06-01", "2022-06-30")),
        (7, 2022, ("2022-07-01", "2022-07-31")),
        (8, 2022, ("2022-08-01", "2022-08-31")),
        (9, 2022, ("2022-09-01", "2022-09-30")),
        (10, 2022, ("2022-10-01", "2022-10-31")),
        (11, 2022, ("2022-11-01", "2022-11-30")),
        (12, 2022, ("2022-12-01", "2022-12-31")),
    ],
)
def test_valid_months_and_years(month, year, expected):
    """Test the get_first_and_last_day_of_month function with valid month and year inputs.

    :param month: The month to test, an integer.
    :param year: The year to test, an integer.
    :param expected: The expected result tuple containing the first and last day of the month.
    :return: Asserts that the output from the function matches the expected tuple.
    """
    assert get_first_and_last_day_of_month(month, year) == expected


@pytest.mark.parametrize("invalid_month", [-1, 0, 5.5, 13, 14, 99, 100, "invalid", "@", "", "a", "b", "z"])
def test_invalid_months(invalid_month):
    """Test the get_first_and_last_day_of_month function with invalid month inputs.

    :param invalid_month: The invalid month input to test, which can be a non-integer, out-of-range integer, or non-numeric string.
    :return: Asserts that the function raises a ValueError when provided with invalid month inputs.
    """
    with pytest.raises(ValueError):
        get_first_and_last_day_of_month(invalid_month)
