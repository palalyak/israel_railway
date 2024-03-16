import re

from playwright.sync_api import  expect

class TravelPage:

    def __init__(self, page, base_url="https://www.rail.co.il/?page=routePlanSearchResults&fromStation="):
        self.base_url = base_url
        self.page = page

    def get_price_window(self, train_details, price_details):
        train_selector = f"#trainNumber_{train_details["trainNumber"]}"
        price_type = price_details.get("type")
        single_trip_price = price_details.get("נסיעה אחת")
        daily_pass_price = price_details.get("חופשי יומי")
        monthly_pass_price = price_details.get("חופשי חודשי")

        '''open trip price modal window from train slot'''
        self.page.click(f"{train_selector} button")
        expect(self.page.locator(f"{train_selector} .modal .desktop"), "The window with prices should be visible").to_be_visible()

        '''open list of price categories'''
        self.page.locator(f"{train_selector} .modal .desktop svg").click()

        '''select the price categories'''
        self.page.locator(".custom-list").get_by_text(price_type, exact=True).click()
        expect(self.page.locator(".custom-list"), "Price list should be hidden").to_be_hidden()

        trip_locator = self.page.get_by_text("נסיעה אחת")
        price_locator = trip_locator.locator("xpath=following-sibling::div")
        expected_price_text = str(price_details["נסיעה אחת"])
        expect(price_locator, f"wrong price for {expected_price_text} / {price_type}").to_contain_text(expected_price_text)

        # expect(page.get_by_role("listitem")).to_have_text(["apple", "banana", "orange"])

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
