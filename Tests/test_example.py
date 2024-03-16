import pytest
from API.RailAPIClient import RailAPIClient
from Pages.travel_page import TravelPage


@pytest.fixture(scope="class")
def get_train_data(request):
    request.cls.train_data = train_data
    yield


@pytest.fixture(scope="class")
def setup_travel_page(page, request):
    travel_page = TravelPage(page)
    train_details = train_data["train_details"]
    travel_page.goto(train_details)
    request.cls.window = travel_page
    yield


train_data = dict(
    train_details={'trainNumber': "221", 'from_station': "3700", 'to_station': "5150", 'date': "2024-03-17",
                   'hours': "07", 'minutes': "00"},
    prices={
        "senior_citizen_price": {"type": "אזרח ותיק", "נסיעה אחת": 4.5, "חופשי יומי": 9, "חופשי חודשי": 127.5},
        "blind_escort_price": {"type": "כללי", "נסיעה אחת": 9, "חופשי יומי": 18, "חופשי חודשי": 255},
        "children_price": {"type": "נוער עד גיל 18", "נסיעה אחת": 9, "חופשי יומי": 18, "חופשי חודשי": 127.5},
        "ordinary_price": {"type": "כללי", "נסיעה אחת": 9, "חופשי יומי": 18, "חופשי חודשי": 255},
        "disabled_price": {"type": "נכה", "נסיעה אחת": 9, "חופשי יומי": 18, "חופשי חודשי": 255},
        "discount_price": {"type": "זכאי ביטוח לאומי", "נסיעה אחת": 9, "חופשי יומי": 18, "חופשי חודשי": 255},
        "student_price": {"type": "סטודנט רגיל", "נסיעה אחת": 9, "חופשי יומי": 18, "חופשי חודשי": 255},
    })


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
@pytest.mark.usefixtures("setup_travel_page", "get_train_data")
class TestPriceDetails:
    window: TravelPage
    train_data: dict

    def test_ticket_prices_ui(self):
        train_details = self.train_data["train_details"]
        price_type = self.train_data["prices"]

        self.window.prices(train_details, price_type["senior_citizen_price"])
        self.window.prices(train_details, price_type["blind_escort_price"])
        self.window.prices(train_details, price_type["children_price"])
        self.window.prices(train_details, price_type["ordinary_price"])
        self.window.prices(train_details, price_type["disabled_price"])
        self.window.prices(train_details, price_type["discount_price"])
        self.window.prices(train_details, price_type["student_price"])


@pytest.mark.skip
@pytest.mark.usefixtures("setup_travel_page", "get_train_data")
class TestSlotDetails:
    window: TravelPage
    train_data: dict
    def test_my_element(self, snapshot):
        train_details = self.train_data["train_details"]
        self.window.train_slots(train_details, snapshot)




