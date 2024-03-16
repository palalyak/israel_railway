import pytest
from playwright.sync_api import Page

from API.RailAPIClient import RailAPIClient


def test_get_schedule():
    client = RailAPIClient()
    from_station = "3700"
    to_station = "7300"
    date = "2024-03-14"
    hours = "07:00"
    response = client.get_schedule(from_station, to_station, date, hours)
    assert response is not None
    train_number_450_found = any(
        train.trainNumber == 429
        for travel in response.result.travels
        for train in travel.trains
    )

    assert train_number_450_found, "Поезд с номером 450 не найден в расписании"

