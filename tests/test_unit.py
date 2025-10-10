"""There are tests for helpers functions."""

import pytest
from re import escape
from src.helpers import calculate_interval_hours, compose_string_from_dict_list
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
        ("14:31", "14:35", 1),
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


@pytest.mark.parametrize(
    "dict_list, field_order, expected_result",
    [
        # 1. Basic successful case
        (
            [
                {"name": "field_01", "value": "Value_01"},
                {"name": "field_02", "value": "Value_02"},
                {"name": "field_03", "value": "Value_03"},
            ],
            ["field_01", "field_02", "field_03"],
            "field_01=Value_01; field_02=Value_02; field_03=Value_03",
        ),
        # 2. Field order differs from dictionary order
        (
            [
                {"name": "field_03", "value": "Value_03"},
                {"name": "field_01", "value": "Value_01"},
                {"name": "field_02", "value": "Value_02"},
            ],
            ["field_01", "field_02", "field_03"],
            "field_01=Value_01; field_02=Value_02; field_03=Value_03",
        ),
        # 3. Dictionaries with additional fields
        (
            [
                {"name": "field_01", "value": "Value_01", "extra": "data1"},
                {"name": "field_02", "value": "Value_02", "other": 123},
                {"name": "field_03", "value": "Value_03", "flag": True},
            ],
            ["field_01", "field_02", "field_03"],
            "field_01=Value_01; field_02=Value_02; field_03=Value_03",
        ),
        # 4. Empty field list (valid case)
        ([{"name": "field_01", "value": "Value_01"}, {"name": "field_02", "value": "Value_02"}], [], ""),
        # 5. Fields with empty strings as values
        (
            [
                {"name": "field_01", "value": ""},
                {"name": "field_02", "value": "Value_02"},
                {"name": "field_03", "value": "Value_03"},
            ],
            ["field_01", "field_02", "field_03"],
            "field_01=; field_02=Value_02; field_03=Value_03",
        ),
        # 6. Repeated field names in dict_list (last one should be used)
        (
            [
                {"name": "field_01", "value": "First value"},
                {"name": "field_02", "value": "Value_02"},
                {"name": "field_01", "value": "Override value"},
            ],
            ["field_01", "field_02"],
            "field_01=Override value; field_02=Value_02",
        ),
    ],
)
def test_compose_string_success_cases(dict_list, field_order, expected_result):
    """Test successful scenarios of compose_string_from_dict_list function.

    :param dict_list: List of dictionaries containing field definitions
    :param field_order: List specifying the order of fields in the output
    :param expected_result: Expected formatted string output
    :return: None
    """
    result = compose_string_from_dict_list(dict_list, field_order)
    assert result == expected_result


@pytest.mark.parametrize(
    "dict_list, field_order, exception_msg",
    [
        # 7. Different data types in values
        (
            [
                {"name": "field_01", "value": 123},
                {"name": "field_02", "value": True},
                {"name": "field_03", "value": None},
            ],
            ["field_01", "field_02", "field_03"],
            "Keys '['field_03']' not found in any dictionary.",
        ),
        # 8. Missing one of the required fields - tests error when a single field is missing
        (
            [{"name": "field_01", "value": "Value_01"}, {"name": "field_03", "value": "Value_03"}],
            ["field_01", "field_02", "field_03"],
            "Keys '['field_02']' not found in any dictionary.",
        ),
        # 9. Missing all required fields - tests error when all required fields are missing
        (
            [{"name": "field_04", "value": "Value_04"}, {"name": "field_05", "value": "Value_05"}],
            ["field_01", "field_02", "field_03"],
            "Keys '['field_01', 'field_02', 'field_03']' not found in any dictionary.",
        ),
        # 10. Empty dictionary list - tests error when input list is empty
        ([], ["field_01", "field_02"], "Keys '['field_01', 'field_02']' not found in any dictionary."),
    ],
)
def test_compose_string_failure_cases(dict_list, field_order, exception_msg):
    """Test error scenarios of compose_string_from_dict_list function.

    :param dict_list: List of dictionaries containing field definitions
    :param field_order: List of field names that should cause errors
    :param exception_msg: Expected error message text
    :return: None
    """
    with pytest.raises(ValueError, match=escape(exception_msg)):
        compose_string_from_dict_list(dict_list, field_order)
