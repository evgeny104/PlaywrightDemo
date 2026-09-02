"""
Техника: Smoke Testing + Checklist

Smoke — базовые проверки: страница открылась, ключевые элементы видны.
Checklist — перечень обязательных блоков страницы Overview.
"""
import allure
from playwright.sync_api import expect
from pages.nvda.symbol_page import NvdaSymbolPage


@allure.feature("Вкладка Overview NVDA")
class TestOverviewPage:

    @allure.title("Страница Overview открывается с корректным URL")
    def test_overview_opens(self, nvda_overview: NvdaSymbolPage):
        # Smoke: страница достижима и URL корректен
        nvda_overview.should_be_opened()

    @allure.title("Заголовок с тикером NVDA виден на странице")
    def test_nvidia_heading_visible(self, nvda_overview: NvdaSymbolPage):
        # Checklist: заголовок с тикером — обязательный элемент страницы
        expect(nvda_overview.symbol_heading).to_be_visible()

    @allure.title("Заголовок содержит тикер 'NVDA'")
    def test_nvidia_heading_text(self, nvda_overview: NvdaSymbolPage):
        # h1 отображает тикер "NVDA", а не полное название компании
        expect(nvda_overview.symbol_heading).to_contain_text("NVDA")

    @allure.title("Текущая цена акции отображается")
    def test_price_is_displayed(self, nvda_overview: NvdaSymbolPage):
        # Checklist: котировка — ключевой элемент страницы тикера
        expect(nvda_overview.price_value).to_be_visible()

    @allure.title("График цены присутствует на странице")
    def test_chart_is_present(self, nvda_overview: NvdaSymbolPage):
        # Checklist: графический виджет обязателен для страницы символа
        expect(nvda_overview.chart_container).to_be_visible()

    @allure.title("Описание компании отображается")
    def test_company_description_visible(self, nvda_overview: NvdaSymbolPage):
        # Checklist: блок с информацией о компании
        expect(nvda_overview.company_description).to_be_visible()
