"""
Техника: Equivalence Partitioning + Boundary Value Analysis

EP — метрики делятся на три класса эквивалентности:
     - Оценочные мультипликаторы (Price-to-*)
     - Показатели рентабельности (*margin %)
     - Коэффициенты ликвидности (*ratio)
     Параметризованный тест проверяет представителя каждого класса.

BVA — заголовок таблицы: крайняя левая колонка = 2020 (нижняя граница),
      крайняя правая = Current (верхняя граница/актуальное значение).
      Значение Current должно быть числом > 0.
"""
import re
import pytest
import allure
from pages.nvda.statistics_page import NvdaStatisticsPage

VALUATION_METRICS     = ["Price to earnings ratio", "Price to sales ratio", "Price to book ratio"]
PROFITABILITY_METRICS = ["Gross margin %", "Operating margin %", "Net margin %"]
LIQUIDITY_METRICS     = ["Quick ratio", "Current ratio"]


@allure.feature("Вкладка Statistics NVDA")
class TestStatisticsPage:

    @allure.title("Страница Statistics открывается с корректным URL")
    def test_statistics_page_opens(self, nvda_statistics: NvdaStatisticsPage):
        # Smoke: страница достижима, URL и таблица корректны
        nvda_statistics.should_be_opened()

    @allure.title("Заголовок таблицы содержит граничные колонки: Value и Current")
    def test_table_header_has_boundary_columns(self, nvda_statistics: NvdaStatisticsPage):
        # BVA: Value = нижняя граница описания, Current = верхняя (актуальная)
        nvda_statistics.assert_header_has_years()

    @pytest.mark.parametrize("metric", VALUATION_METRICS)
    @allure.title("Оценочный мультипликатор присутствует: {metric}")
    def test_valuation_metric_present(self, nvda_statistics: NvdaStatisticsPage, metric: str):
        allure.dynamic.parameter("Метрика", metric)
        allure.dynamic.description(
            f"Техника: Equivalence Partitioning\n"
            f"Класс: оценочные мультипликаторы (Price-to-*).\n\n"
            f"Шаги воспроизведения:\n"
            f"  1. Открыть {NvdaStatisticsPage.URL}\n"
            f"  2. Найти строку «{metric}» в таблице.\n\n"
            f"Ожидаемый результат: строка видна на странице."
        )
        nvda_statistics.assert_metrics_present(metric)

    @pytest.mark.parametrize("metric", PROFITABILITY_METRICS)
    @allure.title("Показатель рентабельности присутствует: {metric}")
    def test_profitability_metric_present(self, nvda_statistics: NvdaStatisticsPage, metric: str):
        allure.dynamic.parameter("Метрика", metric)
        allure.dynamic.description(
            f"Техника: Equivalence Partitioning\n"
            f"Класс: показатели рентабельности (*margin %).\n\n"
            f"Шаги воспроизведения:\n"
            f"  1. Открыть {NvdaStatisticsPage.URL}\n"
            f"  2. Найти строку «{metric}» в таблице.\n\n"
            f"Ожидаемый результат: строка видна на странице."
        )
        nvda_statistics.assert_metrics_present(metric)

    @pytest.mark.parametrize("metric", LIQUIDITY_METRICS)
    @allure.title("Коэффициент ликвидности присутствует: {metric}")
    def test_liquidity_metric_present(self, nvda_statistics: NvdaStatisticsPage, metric: str):
        allure.dynamic.parameter("Метрика", metric)
        allure.dynamic.description(
            f"Техника: Equivalence Partitioning\n"
            f"Класс: коэффициенты ликвидности (*ratio).\n\n"
            f"Шаги воспроизведения:\n"
            f"  1. Открыть {NvdaStatisticsPage.URL}\n"
            f"  2. Найти строку «{metric}» в таблице.\n\n"
            f"Ожидаемый результат: строка видна на странице."
        )
        nvda_statistics.assert_metrics_present(metric)

    @allure.title("Значение 'Current' для P/E — валидное положительное число")
    def test_pe_ratio_current_value_is_numeric(self, nvda_statistics: NvdaStatisticsPage):
        # BVA: граничное (актуальное) значение мультипликатора должно быть числом > 0
        raw = nvda_statistics.metric_current_value("Price to earnings ratio").inner_text().strip()
        assert re.match(r"^\d+\.?\d*$", raw), f"Значение Current P/E должно быть числом, получено: '{raw}'"
        assert float(raw) > 0, f"P/E ratio должен быть > 0, получено: {raw}"

    @allure.title("Gross margin % меньше 100 (граничное значение рентабельности)")
    def test_gross_margin_below_100(self, nvda_statistics: NvdaStatisticsPage):
        # BVA: верхняя граница валидного значения маржи — 100%
        raw = nvda_statistics.metric_current_value("Gross margin %").inner_text().strip()
        value = float(raw)
        assert 0 < value < 100, f"Gross margin % должен быть в диапазоне (0, 100), получено: {value}"
