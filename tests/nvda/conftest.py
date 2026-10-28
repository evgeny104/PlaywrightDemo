import pytest
import allure
from playwright.sync_api import Page
from pages.nvda.statement_page import NvdaStatementPage
from pages.nvda.statistics_page import NvdaStatisticsPage
from pages.nvda.dividends_page import NvdaDividendsPage
from pages.nvda.documents_page import NvdaDocumentsPage
from pages.nvda.symbol_page import NvdaSymbolPage
from screenshot_store import _pages


def _open_page(page: Page, request, page_object_cls, step_title: str):
    """Общая механика: регистрация страницы для screenshot-хука + goto под allure.step.

    Утечка _pages невозможна даже при падении goto — pop выполняется в finally.
    """
    _pages[request.node.nodeid] = page
    try:
        with allure.step(step_title):
            page.goto(page_object_cls.URL)
        yield page_object_cls(page)
    finally:
        _pages.pop(request.node.nodeid, None)


@pytest.fixture
def nvda_overview(page: Page, request) -> NvdaSymbolPage:
    yield from _open_page(page, request, NvdaSymbolPage, "Открываем вкладку Overview NVDA")


@pytest.fixture
def nvda_statement(page: Page, request) -> NvdaStatementPage:
    yield from _open_page(page, request, NvdaStatementPage, "Открываем страницу Statement NVDA")


@pytest.fixture
def nvda_statistics(page: Page, request) -> NvdaStatisticsPage:
    yield from _open_page(page, request, NvdaStatisticsPage, "Открываем вкладку Statistics NVDA")


@pytest.fixture
def nvda_dividends(page: Page, request) -> NvdaDividendsPage:
    yield from _open_page(page, request, NvdaDividendsPage, "Открываем вкладку Dividends NVDA")


@pytest.fixture
def nvda_documents(page: Page, request) -> NvdaDocumentsPage:
    yield from _open_page(page, request, NvdaDocumentsPage, "Открываем страницу Documents NVDA")
