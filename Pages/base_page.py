class BasePage:
    def __init__(self, page):
        self.page = page

    def click_on(self, selector):
        locator = self.page.locator(selector)
        locator.highlight()
        locator.click()
