import pytest
import allure
from playwright.sync_api import Page
from pages.search import HomePage
from pages.nvda.symbol_page import NvdaSymbolPage
from screenshot_store import _pages


@pytest.fixture
def home(page: Page, request) -> HomePage:
    _pages[request.node.nodeid] = page
    with allure.step("Открываем главную страницу MetaTrader"):
        page.goto("https://www.metatrader.com/")
    yield HomePage(page)
    _pages.pop(request.node.nodeid, None)


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    return {
        **browser_context_args,
        "locale": "en-US",
    }


@pytest.fixture(scope="session")
def browser_type_launch_args(browser_type_launch_args):
    return {
        **browser_type_launch_args,
        "slow_mo": 1300,
    }


@pytest.fixture
def nvda_page(page: Page, request) -> NvdaSymbolPage:
    _pages.setdefault(request.node.nodeid, page)
    yield NvdaSymbolPage(page)


def pytest_runtest_logreport(report):
    if report.when == "call" and report.failed:
        page = _pages.get(report.nodeid)
        if page:
            allure.attach(
                page.screenshot(full_page=True),
                name="Screenshot on failure",
                attachment_type=allure.attachment_type.PNG,
            )