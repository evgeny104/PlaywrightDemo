import allure
from playwright.sync_api import Locator

from pages.aapl.aapl_page import AaplBasePage


class AaplSymbolPage(AaplBasePage):
    """Page Object для вкладки Overview акции AAPL на metatrader.com.

    DOM-заметки (проверено 2026-10-23):
    - h1 содержит текст 'AAPL'
    - .regular-price — блок текущей цены с процентом изменения
    - .charts — контейнер графика (внутри range-chart блоки)
    - .description — блок с описанием компании
    """

    _URL_PATTERN = r"/nasdaq/aapl(?:/overview)?/?(?:\?.*)?$"

    @property
    def price_value(self) -> Locator:
        # fallback: DOM has no semantic role/text for this element
        return self.page.locator(".regular-price").first

    @property
    def chart_container(self) -> Locator:
        # fallback: DOM has no semantic role/text for this element
        return self.page.locator(".charts").first

    @property
    def company_description(self) -> Locator:
        # fallback: DOM has no semantic role/text for this element
        return self.page.locator(".description").first

    @allure.step("Проверяем страницу Overview AAPL")
    def should_be_opened(self) -> None:
        with allure.step("URL содержит /nasdaq/aapl"):
            self._expect_url(self._URL_PATTERN, description="/nasdaq/aapl")
        with allure.step("Заголовок с тикером AAPL виден"):
            self._expect_visible(
                self.symbol_heading,
                description="заголовок h1 с тикером AAPL",
            )
