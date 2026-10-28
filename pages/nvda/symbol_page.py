import allure
from playwright.sync_api import Locator
from pages.nvda.nvda_page import NvdaBasePage


class NvdaSymbolPage(NvdaBasePage):
    URL = NvdaBasePage.BASE_URL
    _URL_PATTERN = r"/nasdaq/nvda(?:/overview)?/?(?:\?.*)?$"

    # Locators

    @property
    def price_value(self) -> Locator:
        return self.page.locator("[class*='price'], [class*='quote']").first

    @property
    def chart_container(self) -> Locator:
        return self.page.locator("canvas, [class*='chart']").first

    @property
    def company_description(self) -> Locator:
        return self.page.locator("[class*='description'], [class*='about'], section p").first

    # Actions

    @allure.step("Проверяем страницу Overview NVDA")
    def should_be_opened(self) -> None:
        with allure.step("URL содержит /nasdaq/nvda"):
            self._expect_url(self._URL_PATTERN, description="/nasdaq/nvda")
        with allure.step("Заголовок с тикером NVDA виден"):
            self._expect_visible(
                self.symbol_heading,
                description="заголовок h1 с тикером NVDA",
            )
