import pytest
import allure
from playwright.sync_api import Page

from pages.aapl.symbol_page import AaplSymbolPage
from screenshot_store import _pages


@pytest.fixture
def aapl_overview(page: Page, request) -> AaplSymbolPage:
    _pages[request.node.nodeid] = page
    try:
        with allure.step("Открываем вкладку Overview AAPL"):
            page.goto(AaplSymbolPage.URL)
        yield AaplSymbolPage(page)
    finally:
        _pages.pop(request.node.nodeid, None)
