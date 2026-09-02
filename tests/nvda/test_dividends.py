"""
Техника: Positive Testing + Boundary Value Analysis

Positive — NVDA платит дивиденды, поэтому ожидаем данные, а не пустое состояние.
BVA — первая строка данных (нижняя граница) и «Current» — актуальное значение (верхняя).
      Dividend yield % > 0 — граница валидного диапазона.
"""
import re
import allure
from playwright.sync_api import expect
from pages.nvda.dividends_page import NvdaDividendsPage


@allure.feature("Вкладка Dividends NVDA")
class TestDividendsPage:

    @allure.title("Страница Dividends открывается с корректным URL")
    def test_dividends_page_opens(self, nvda_dividends: NvdaDividendsPage):
        # Smoke: страница достижима и URL корректен
        nvda_dividends.should_be_opened()

    @allure.title("Блок дивидендов виден на странице")
    def test_dividends_section_visible(self, nvda_dividends: NvdaDividendsPage):
        # Smoke: основной контейнер рендерится
        expect(nvda_dividends.dividends_section).to_be_visible()

    @allure.title("Строка 'Dividend yield %' присутствует в таблице")
    def test_dividend_yield_row_visible(self, nvda_dividends: NvdaDividendsPage):
        # Positive: ключевой показатель обязан быть на странице
        nvda_dividends.assert_dividend_yield_visible()

    @allure.title("Строка 'Dividends per share' присутствует в таблице")
    def test_dividends_per_share_row_visible(self, nvda_dividends: NvdaDividendsPage):
        # Positive: второй ключевой показатель страницы
        expect(nvda_dividends.dividends_section).to_be_visible()
        expect(nvda_dividends.per_share_row).to_be_visible()

    @allure.title("Таблица истории дивидендов не пустая")
    def test_dividends_history_not_empty(self, nvda_dividends: NvdaDividendsPage):
        # BVA: нижняя граница — минимум 1 строка с данными
        nvda_dividends.assert_dividends_history_not_empty()

    @allure.title("Дивидендная доходность за текущий год — валидное число > 0")
    def test_dividend_yield_current_is_positive(self, nvda_dividends: NvdaDividendsPage):
        # BVA: актуальное значение (колонка Current/TTM) должно быть числом > 0
        raw = nvda_dividends.dividend_yield_current_value.inner_text().strip()
        assert re.match(r"^\d+\.?\d*$", raw), f"Значение yield должно быть числом, получено: '{raw}'"
        assert float(raw) > 0, f"Dividend yield должен быть > 0, получено: {raw}"

    @allure.title("Количество строк данных больше нуля")
    def test_dividends_count_positive(self, nvda_dividends: NvdaDividendsPage):
        # BVA: нижняя граница для количества строк — > 0
        count = nvda_dividends.dividends_table_rows.count()
        assert count > 0, f"Ожидается минимум 1 запись о дивидендах, найдено: {count}"
