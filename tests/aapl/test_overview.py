"""
Техника: Smoke Testing + Checklist

Smoke — базовые проверки: страница открылась, ключевые элементы видны.
Checklist — перечень обязательных блоков страницы Overview AAPL.
"""
import allure
from playwright.sync_api import expect

from pages.aapl.symbol_page import AaplSymbolPage


@allure.feature("Вкладка Overview AAPL")
class TestAaplOverviewPage:

    @allure.title("Страница Overview AAPL открывается с корректным URL")
    def test_overview_opens(self, aapl_overview: AaplSymbolPage):
        # Smoke: страница достижима и URL корректен
        aapl_overview.should_be_opened()

    @allure.title("Заголовок с тикером AAPL виден на странице")
    def test_aapl_heading_visible(self, aapl_overview: AaplSymbolPage):
        # Checklist: заголовок с тикером — обязательный элемент страницы
        expect(aapl_overview.symbol_heading).to_be_visible()

    @allure.title("Заголовок содержит тикер 'AAPL'")
    def test_aapl_heading_text(self, aapl_overview: AaplSymbolPage):
        # h1 отображает тикер "AAPL", а не полное название компании
        expect(aapl_overview.symbol_heading).to_contain_text("AAPL")

    @allure.title("Текущая цена акции Apple отображается")
    def test_price_is_displayed(self, aapl_overview: AaplSymbolPage):
        # Checklist: котировка — ключевой элемент страницы тикера
        expect(aapl_overview.price_value).to_be_visible()

    @allure.title("График цены AAPL присутствует на странице")
    def test_chart_is_present(self, aapl_overview: AaplSymbolPage):
        # Checklist: графический виджет обязателен для страницы символа
        expect(aapl_overview.chart_container).to_be_visible()

    @allure.title("Описание компании Apple отображается")
    def test_company_description_visible(self, aapl_overview: AaplSymbolPage):
        # Checklist: блок с информацией о компании
        expect(aapl_overview.company_description).to_be_visible()
