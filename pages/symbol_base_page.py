import allure
from playwright.sync_api import Locator

from pages.base_page import BasePage

TABS = ("Overview", "Statement", "Statistics", "Dividends", "Documents")


class SymbolBasePage(BasePage):
    """Общий базовый класс для страниц любого тикера metatrader.com.

    Наследники определяют BASE_URL, URL, _URL_PATTERN и symbol_heading.
    Навигация по вкладкам (TABS, go_to_tab, assert_all_tabs_visible) — здесь.
    """

    def tab_link(self, name: str) -> Locator:
        return self.page.get_by_role("link", name=name, exact=True)

    @allure.step("Переходим на вкладку '{name}'")
    def go_to_tab(self, name: str) -> None:
        self.tab_link(name).click()

    @allure.step("Проверяем наличие всех вкладок навигации")
    def assert_all_tabs_visible(self) -> None:
        for name in TABS:
            with allure.step(f"Вкладка '{name}' видна"):
                self._expect_visible(
                    self.tab_link(name),
                    description=f"вкладка навигации «{name}»",
                )
