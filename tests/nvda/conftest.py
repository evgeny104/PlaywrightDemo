import pytest
import allure
from playwright.sync_api import Page
from pages.nvda.statement_page import NvdaStatementPage
from pages.nvda.statistics_page import NvdaStatisticsPage
from pages.nvda.dividends_page import NvdaDividendsPage
from pages.nvda.documents_page import NvdaDocumentsPage
from pages.nvda.symbol_page import NvdaSymbolPage
from screenshot_store import _pages


@pytest.fixture
def nvda_overview(page: Page, request) -> NvdaSymbolPage:
    _pages[request.node.nodeid] = page
    with allure.step("Открываем вкладку Overview NVDA"):
        page.goto(NvdaSymbolPage.URL)
    yield NvdaSymbolPage(page)
    _pages.pop(request.node.nodeid, None)


@pytest.fixture
def nvda_statement(page: Page, request) -> NvdaStatementPage:
    _pages[request.node.nodeid] = page
    with allure.step("Открываем страницу Statement NVDA"):
        page.goto(NvdaStatementPage.URL)
    yield NvdaStatementPage(page)
    _pages.pop(request.node.nodeid, None)


@pytest.fixture
def nvda_statistics(page: Page, request) -> NvdaStatisticsPage:
    _pages[request.node.nodeid] = page
    with allure.step("Открываем вкладку Statistics NVDA"):
        page.goto(NvdaStatisticsPage.URL)
    yield NvdaStatisticsPage(page)
    _pages.pop(request.node.nodeid, None)


@pytest.fixture
def nvda_dividends(page: Page, request) -> NvdaDividendsPage:
    _pages[request.node.nodeid] = page
    with allure.step("Открываем вкладку Dividends NVDA"):
        page.goto(NvdaDividendsPage.URL)
    yield NvdaDividendsPage(page)
    _pages.pop(request.node.nodeid, None)


@pytest.fixture
def nvda_documents(page: Page, request) -> NvdaDocumentsPage:
    _pages[request.node.nodeid] = page
    with allure.step("Открываем вкладку Documents NVDA"):
        page.goto(NvdaDocumentsPage.URL)
    yield NvdaDocumentsPage(page)
    _pages.pop(request.node.nodeid, None)
