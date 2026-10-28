"""
Техника: State Transition Testing + Equivalence Partitioning

State Transition — каждая вкладка = состояние, клик = переход.
Equivalence Partitioning — все 5 вкладок образуют группу «валидных переходов»;
каждый параметризованный кейс проверяет одного представителя группы.
"""
import re
import pytest
import allure
from playwright.sync_api import expect
from pages.nvda.symbol_page import NvdaSymbolPage
from pages.nvda.documents_page import NvdaDocumentsPage
from pages.symbol_base_page import TABS

TABS_URL = [
    ("Overview",   r"/nasdaq/nvda(?:/overview)?$"),
    ("Statement",  r"/nasdaq/nvda/statement"),
    ("Statistics", r"/nasdaq/nvda/statistics"),
    ("Dividends",  r"/nasdaq/nvda/dividends"),
    ("Documents",  r"/nasdaq/nvda/documents"),
]


@allure.feature("Навигация по вкладкам NVDA")
class TestTabsNavigation:

    @allure.title("Все 5 вкладок присутствуют на странице Overview")
    def test_all_tabs_present(self, nvda_overview: NvdaSymbolPage):
        # Checklist: проверяем каждую из 5 вкладок по очереди
        nvda_overview.assert_all_tabs_visible()

    @pytest.mark.parametrize("tab_name,url_pattern", TABS_URL, ids=[t[0] for t in TABS_URL])
    @allure.title("Переход на вкладку меняет URL: {tab_name}")
    def test_tab_click_changes_url(self, nvda_overview: NvdaSymbolPage, tab_name: str, url_pattern: str):
        allure.dynamic.parameter("Вкладка", tab_name)
        allure.dynamic.parameter("Ожидаемый URL-паттерн", url_pattern)
        # EP: представитель группы «валидных вкладок» — URL меняется корректно
        # State Transition: Overview → tab_name
        nvda_overview.go_to_tab(tab_name)
        with allure.step(f"URL содержит паттерн '{url_pattern}'"):
            expect(nvda_overview.page).to_have_url(re.compile(url_pattern))

    @allure.title("Последовательный обход всех вкладок слева направо")
    def test_sequential_tab_navigation(self, nvda_overview: NvdaSymbolPage):
        # State Transition: полный обход цепочки Overview→Statement→Statistics→Dividends→Documents
        for tab_name, url_pattern in TABS_URL[1:]:
            with allure.step(f"Переходим на '{tab_name}'"):
                nvda_overview.go_to_tab(tab_name)
                expect(nvda_overview.page).to_have_url(re.compile(url_pattern))

    @allure.title("Обратный переход: Documents → Overview")
    def test_navigate_back_to_overview(self, nvda_documents: NvdaDocumentsPage):
        # State Transition: переход из последней вкладки обратно в первую
        nvda_documents.go_to_tab("Overview")
        with allure.step("URL возвращается к базовому NVDA"):
            expect(nvda_documents.page).to_have_url(re.compile(r"/nasdaq/nvda(?:/overview)?$"))

    @pytest.mark.parametrize("tab_name", TABS)
    @allure.title("Панель вкладок не исчезает при открытии: {tab_name}")
    def test_tabs_visible_on_each_page(self, nvda_overview: NvdaSymbolPage, tab_name: str):
        allure.dynamic.parameter("Открытая вкладка", tab_name)
        # Проверяем что nav-бар со вкладками есть на каждой странице раздела
        nvda_overview.go_to_tab(tab_name)
        nvda_overview.assert_all_tabs_visible()
