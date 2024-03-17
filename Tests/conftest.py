from typing import Generator
import pytest
from playwright.sync_api import (
    Browser,
    BrowserContext,
    BrowserType,
    Page,
    Playwright,
    Selectors,
    sync_playwright,
)


@pytest.fixture(scope="session")
def playwright() -> Generator[Playwright, None, None]:
    with sync_playwright() as p:
        yield p


@pytest.fixture(scope="session")
def browser_type(
    playwright: Playwright, browser_name: str
) -> Generator[BrowserType, None, None]:
    browser_type = None
    if browser_name == "chromium":
        browser_type = playwright.chromium
    elif browser_name == "firefox":
        browser_type = playwright.firefox
    elif browser_name == "webkit":
        browser_type = playwright.webkit
    assert browser_type, f"Unkown browser name '{browser_name}'"
    yield browser_type

@pytest.fixture(scope="session")
def browser(
    browser_type: BrowserType
) -> Generator[Browser, None, None]:
    browser = browser_type.launch(headless=True, slow_mo=1000)
    browser.new_context(
        permissions=['notifications'],
    )
    yield browser
    browser.close()

@pytest.fixture(scope="session")
def context(browser: Browser) -> Generator[BrowserContext, None, None]:
    context = browser.new_context(permissions=['geolocation'],
                                  geolocation={'longitude': 12.492507, 'latitude': 41.889938},
                                  locale='en-GB')
    context.tracing.start()
    yield context

@pytest.fixture(scope="session")
def page(context: BrowserContext) -> Generator[Page, None, None]:
    page = context.new_page()
    yield page
    context.tracing.stop(path="trace.zip")
    context.close()
    page.close()

@pytest.fixture(scope="session")
def selectors(playwright: Playwright) -> Selectors:
    return playwright.selectors