"""There is module to provide functions to collecting data from UI."""

import logging
from os import environ

from requests import Session

logger = logging.getLogger(__name__)
logging.basicConfig(format="%(asctime)s [%(levelname)8s] %(message)s (%(filename)s:%(lineno)s)", level=logging.INFO)


def get_obecnosci(child_id: str, month: str, year: str, cookies: str) -> dict:
    """Fetches attendance data for a specific child for a given month and year.

    This function sends a POST request to an API endpoint to retrieve attendance data.
    It uses session-based HTTP communication and requires specific headers and payload
    parameters to interact with the API.

    :param child_id: The unique identifier of the child whose attendance data is being requested.
    :param month: The month for which attendance data is being requested (e.g., "9" for January).
    :param year: The year for which attendance data is being requested (e.g., "2025").
    :param cookies: A string containing cookies for authentication purposes.
    :return: A dictionary containing the JSON response from the API, which includes attendance data.
    """
    with Session() as s:
        headers = {
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Accept-Language": "en-GB,en;q=0.9,en-US;q=0.8,pl;q=0.7,ru;q=0.6",
            "Connection": "keep-alive",
            "Content-Length": "40",
            "Content-Type": "application/json; charset=UTF-8",
            "Cookie": cookies,
            "DNT": "1",
            "Host": environ["HOST"],
            "Origin": environ["ORIGIN"],
            "Referer": environ["REFERER"],
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "User-Agent": environ["USER_AGENT"],
            "X-Requested-With": "XMLHttpRequest",
            "sec-ch-ua": '"Microsoft Edge";v="141", "Not?A_Brand";v="8", "Chromium";v="141"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
        }
        payload = {"idDziecko": child_id, "aMc": month, "aRok": year}
        response = s.post(url=environ["BASE_URL"] + environ["API_URL_OBECNOSCI"], headers=headers, json=payload)
        return response.json()
