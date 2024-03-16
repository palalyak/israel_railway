import re

from playwright.sync_api import  expect

from Pages.base_page import BasePage


class TravelPage(BasePage):

    def __init__(self, page, base_url="https://www.rail.co.il/?page=routePlanSearchResults&fromStation="):
        super().__init__(page)
        self.base_url = base_url
        self.page = page

    def get_price_window(self, train_details, price_details):
        train_selector = f"#trainNumber_{train_details["trainNumber"]}"
        price_type = price_details.get("type")
        price_window_locator = self.page.locator(f"{train_selector} .modal .desktop")

        '''open trip price modal window from train slot'''
        if not price_window_locator.is_visible():
            # self.page.click(f"{train_selector} button")
            self.click_on(f"{train_selector} button")
        expect(self.page.locator(f"{train_selector} .modal .desktop"), "The window with prices should be visible").to_be_visible()

        '''open list of price categories'''
        # self.page.locator(f"{train_selector} .modal .desktop svg").click()
        self.click_on(f"{train_selector} .modal .desktop svg")

        '''select the price categories'''
        category = self.page.locator(".custom-list").get_by_text(price_type, exact=True)
        category.highlight()
        category.click()
        expect(self.page.locator(".custom-list"), "Price list should be hidden").to_be_hidden()

        test_instance = TestPrices(self.page)
        test_instance.test_prices(price_details)

    def goto(self, train_details, schedule_type=1):
        from_station = train_details["from_station"]
        to_station = train_details["to_station"]
        date = train_details["date"]
        hours = train_details["hours"]
        minutes = train_details["minutes"]

        full_url = (f"{self.base_url}{from_station}&toStation={to_station}&date={date}&hours={hours}"
                    f"&minutes={minutes}&scheduleType={schedule_type}")

        self.page.goto(full_url)
        pattern = re.compile(
            f"{re.escape(self.base_url)}{from_station}&toStation={to_station}&date={date}&hours={hours}"
            f"&minutes={minutes}&scheduleType={schedule_type}")
        expect(self.page).to_have_url(pattern)
        self.page.wait_for_load_state("load")

        modal_window = self.page.locator("#cookiesModalId button:first-child")
        modal_window.wait_for(state="visible", timeout=5000)
        if modal_window.is_visible:
            modal_window.click()


class TestPrices:
    def __init__(self, page):
        self.page = page
        self.errors = []

    def check_price(self, trip_name, expected_price):
        try:
            trip_locator = self.page.get_by_text(trip_name)
            trip_locator.highlight()
            price_locator = trip_locator.locator("xpath=following-sibling::div")
            price_locator.highlight()
            expected_price_text = str(expected_price)
            expect(price_locator).to_contain_text(expected_price_text)
        except AssertionError as e:
            self.errors.append(f"Wrong price for {trip_name}: {e}")

    def test_prices(self, price_details):
        self.check_price("נסיעה אחת", price_details["נסיעה אחת"])
        self.check_price("חופשי יומי", price_details["חופשי יומי"])
        self.check_price("חופשי חודשי", price_details["חופשי חודשי"])

        if self.errors:
            assert False, "\n".join(self.errors)
