import pytest
from playwright.sync_api import Page
from API.RailAPIClient import RailAPIClient
from Pages.travel_page import TravelPage


@pytest.mark.regression
@pytest.mark.parametrize(
    "trainNumber, from_station, to_station, date, hours", [
        (223, "3700", "5150", "2024-03-17", "07:00"),
        (221, "3700", "5150", "2024-03-18", "07:00"),
        (223, "3700", "5150", "2024-03-19", "07:00"),
        (223, "3700", "5150", "2024-03-20", "07:00"),
        (223, "3700", "5150", "2024-03-21", "07:00"),
        (6503, "3700", "5150", "2024-03-22", "07:00"),
        (7501, "3700", "5150", "2024-03-23", "07:00"),
    ]
)
def test_get_schedule_api(trainNumber, from_station, to_station, date, hours):
    response = RailAPIClient().get_schedule(from_station, to_station, date, hours)

    assert response is not None, "schedule not available"

    train_found = any(
        train.trainNumber == trainNumber
        for travel in response.result.travels
        for train in travel.trains
    )
    assert train_found, f'Train number {trainNumber} on the {date} was not found in the schedule'

@pytest.mark.regression
@pytest.mark.parametrize(
    "train_data", [
        ({
            "train_details": {"trainNumber": "221", "from_station": "3700", "to_station": "5150", "date": "2024-03-17", "hours": "07", "minutes": "00"},
            "prices": {
                "senior_citizen_price": {"type": "אזרח ותיק", "נסיעה אחת": 4.6, "חופשי יומי": 9, "חופשי חודשי": 127.5},
                "blind_escort_price": {"type": "מלווה לקוי ראייה", "נסיעה אחת": 9, "חופשי יומי": 18, "חופשי חודשי": 255},
                "children_price": {"type": "נוער עד גיל 18", "נסיעה אחת": 9, "חופשי יומי": 18, "חופשי חודשי": 127.5},
                "ordinary_price": {"type": "כללי", "נסיעה אחת": 9, "חופשי יומי": 18, "חופשי חודשי": 255},
                "disabled_price": {"type": "נכה", "נסיעה אחת": 9, "חופשי יומי": 18, "חופשי חודשי": 255},
                "discount_price": {"type": "זכאי ביטוח לאומי", "נסיעה אחת": 9, "חופשי יומי": 18, "חופשי חודשי": 255},
                "student_price": {"type": "סטודנט רגיל", "נסיעה אחת": 9, "חופשי יומי": 18, "חופשי חודשי": 255},
                "old_citizen_price_price": {"type": "אזרח ותיק 75+", "trip": "חינם"},
                "blind_price": {"type": "לקוי ראייה", "trip": "חינם"}
            }
        })
    ]
)
def test_ticket_prices_UI(page: Page, train_data):
    travel = TravelPage(page)
    train_details = train_data["train_details"]
    prices = train_data["prices"]

    travel.goto(train_details)
    travel.get_price_window(train_details, prices["senior_citizen_price"])
