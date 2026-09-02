import allure
from playwright.sync_api import Locator, expect
from pages.nvda.nvda_page import NvdaBasePage


class NvdaStatisticsPage(NvdaBasePage):
    URL = f"{NvdaBasePage.BASE_URL}/statistics"
    _URL_PATTERN = r"/nasdaq/nvda/statistics"

    # Locators — структура: div.table > label.row > span.cell (Svelte-компоненты)

    @property
    def stats_table(self) -> Locator:
        return self.page.locator("div.table").filter(has_text="Price to earnings ratio").first

    @property
    def header_row(self) -> Locator:
        # span.row.header — заголовочная строка с годами (как в Statement)
        return self.page.locator("span.row.header")

    def metric_row(self, label: str) -> Locator:
        return self.page.locator("label.row").filter(has_text=label).first

    def metric_current_value(self, label: str) -> Locator:
        # span.cell.last = актуальное значение колонки Current
        return self.metric_row(label).locator("span.cell.last")

    # Actions

    @allure.step("Проверяем страницу Statistics NVDA")
    def should_be_opened(self) -> None:
        with allure.step("URL содержит /nasdaq/nvda/statistics"):
            if msg := self._assert_url():
                raise AssertionError(msg)
        with allure.step("Таблица с мультипликаторами видна"):
            self._expect_visible(
                self.stats_table,
                description="таблица мультипликаторов на странице Statistics",
            )

    @allure.step("Проверяем присутствие метрик в таблице")
    def assert_metrics_present(self, *labels: str) -> None:
        for label in labels:
            with allure.step(f"Строка '{label}' видна в таблице"):
                self._expect_visible(
                    self.metric_row(label),
                    description=f"строка «{label}» в таблице Statistics",
                )

    @allure.step("Проверяем заголовок таблицы содержит граничные колонки")
    def assert_header_has_years(self) -> None:
        with allure.step("Колонка 'Value' видна"):
            self._expect_contains_text(
                self.header_row, "Value",
                description="заголовок таблицы Statistics",
            )
        with allure.step("Колонка 'Current' видна (верхняя граница)"):
            self._expect_contains_text(
                self.header_row, "Current",
                description="заголовок таблицы Statistics",
            )
