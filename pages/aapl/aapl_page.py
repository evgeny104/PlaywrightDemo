import re

import allure
from playwright.sync_api import Locator, expect

from pages.base_page import BasePage

TABS = ("Overview", "Statement", "Statistics", "Dividends", "Documents")


class AaplBasePage(BasePage):
    BASE_URL = "https://www.metatrader.com/en/symbols/nasdaq/aapl"
    URL = BASE_URL
    _URL_PATTERN = r"/nasdaq/aapl"

    # Locators

    @property
    def symbol_heading(self) -> Locator:
        """h1 на странице содержит тикер 'AAPL'."""
        return self.page.get_by_role("heading", name=re.compile("AAPL", re.IGNORECASE), level=1).first

    def tab_link(self, name: str) -> Locator:
        """Ссылка вкладки навигации по имени (регистронезависимо через роль)."""
        return self.page.get_by_role("link", name=name, exact=True)

    # Actions

    @allure.step("Переходим на вкладку '{name}'")
    def go_to_tab(self, name: str) -> None:
        """Кликает по вкладке навигации."""
        self.tab_link(name).click()

    @allure.step("Проверяем наличие всех вкладок навигации AAPL")
    def assert_all_tabs_visible(self) -> None:
        """Проверяет, что все вкладки тикера видны на странице."""
        for name in TABS:
            with allure.step(f"Вкладка '{name}' видна"):
                self._expect_visible(
                    self.tab_link(name),
                    description=f"вкладка навигации «{name}»",
                )

    def _assert_url(self) -> str | None:
        """Проверяет URL; возвращает сообщение об ошибке или None."""
        try:
            expect(self.page).to_have_url(re.compile(self._URL_PATTERN))
            return None
        except AssertionError as e:
            lines = (line for line in str(e).splitlines() if line.strip())
            return "\n".join(
                line for line in lines
                if not line.startswith(("Call log", "Aria snapshot", "-", " "))
            )
