import allure
from playwright.sync_api import Locator, expect
from pages.nvda.nvda_page import NvdaBasePage


class NvdaDividendsPage(NvdaBasePage):
    URL = f"{NvdaBasePage.BASE_URL}/dividends"
    _URL_PATTERN = r"/nasdaq/nvda/dividends"

    # Locators — структура: div.table > label.row > span.cell (как в Statistics)

    @property
    def dividends_section(self) -> Locator:
        return self.page.locator("div.table").filter(has_text="Dividends per share").first

    @property
    def dividend_yield_row(self) -> Locator:
        return self.page.locator("label.row").filter(has_text="Dividend yield %").first

    @property
    def per_share_row(self) -> Locator:
        return self.page.locator("label.row").filter(has_text="Dividends per share").first

    @property
    def dividend_yield_current_value(self) -> Locator:
        # span.cell.last = значение TTM (последняя колонка)
        return self.dividend_yield_row.locator("span.cell.last")

    @property
    def dividends_table_rows(self) -> Locator:
        return self.dividends_section.locator("label.row")

    # Actions

    @allure.step("Проверяем страницу Dividends NVDA")
    def should_be_opened(self) -> None:
        with allure.step("URL содержит /nasdaq/nvda/dividends"):
            if msg := self._assert_url():
                raise AssertionError(msg)
        with allure.step("Таблица с данными дивидендов видна"):
            self._expect_visible(
                self.dividends_section,
                description="таблица с данными дивидендов",
            )

    @allure.step("Проверяем строку Dividend yield % присутствует")
    def assert_dividend_yield_visible(self) -> None:
        self._expect_visible(
            self.dividend_yield_row,
            description="строка «Dividend yield %» в таблице Dividends",
        )

    @allure.step("Проверяем таблица дивидендов не пустая")
    def assert_dividends_history_not_empty(self) -> None:
        with allure.step("Таблица видна"):
            self._expect_visible(
                self.dividends_section,
                description="таблица с данными дивидендов",
            )
        with allure.step("В таблице есть строки с данными"):
            self._expect_visible(
                self.dividends_table_rows.first,
                description="первая строка данных в таблице дивидендов",
            )
