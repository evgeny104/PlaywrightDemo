import allure
from playwright.sync_api import Locator

from pages.aapl.aapl_page import AaplBasePage


class AaplSymbolPage(AaplBasePage):
    """Page Object для вкладки Overview акции AAPL на metatrader.com.

    DOM-заметки (проверено 2026-10-23):
    - h1.svelte-1g56i8g содержит текст 'AAPL'
    - .regular-price — блок текущей цены с процентом изменения
    - .charts — контейнер графика (div, внутри которого находятся range-chart блоки)
    - .description — блок с описанием компании (начинается с 'Apple Inc. - Common Stock')
    - Вкладки: ссылки с классом .tab, текст UPPERCASE, но get_by_role(name=..., exact=True)
      находит их без учёта регистра.
    """

    _URL_PATTERN = r"/nasdaq/aapl(?:/overview)?$"

    # Locators

    @property
    def price_value(self) -> Locator:
        """Блок текущей рыночной цены."""
        # fallback: DOM has no semantic role/text for this element
        return self.page.locator(".regular-price").first

    @property
    def chart_container(self) -> Locator:
        """Контейнер графика цены."""
        # fallback: DOM has no semantic role/text for this element
        return self.page.locator(".charts").first

    @property
    def company_description(self) -> Locator:
        """Блок с описанием компании."""
        # fallback: DOM has no semantic role/text for this element
        return self.page.locator(".description").first

    # Actions

    @allure.step("Проверяем страницу Overview AAPL")
    def should_be_opened(self) -> None:
        """Проверяет, что страница Overview AAPL открыта корректно."""
        with allure.step("URL содержит /nasdaq/aapl"):
            if msg := self._assert_url():
                raise AssertionError(msg)
        with allure.step("Заголовок с тикером AAPL виден"):
            self._expect_visible(
                self.symbol_heading,
                description="заголовок h1 с тикером AAPL",
            )

    @allure.step("Проверяем отображение текущей цены AAPL")
    def assert_price_visible(self) -> None:
        """Проверяет, что блок текущей цены отображается на странице."""
        self._expect_visible(
            self.price_value,
            description="блок текущей рыночной цены AAPL",
        )

    @allure.step("Проверяем наличие графика цены AAPL")
    def assert_chart_visible(self) -> None:
        """Проверяет, что контейнер графика присутствует на странице."""
        self._expect_visible(
            self.chart_container,
            description="контейнер графика цены AAPL",
        )

    @allure.step("Проверяем отображение описания компании Apple")
    def assert_description_visible(self) -> None:
        """Проверяет, что блок описания компании отображается на странице."""
        self._expect_visible(
            self.company_description,
            description="блок описания компании Apple Inc.",
        )

    @allure.step("Проверяем, что описание содержит упоминание Apple")
    def assert_description_contains_apple(self) -> None:
        """Проверяет, что текст описания содержит слово 'Apple'."""
        self._expect_contains_text(
            self.company_description,
            expected="Apple",
            description="описание компании",
        )
