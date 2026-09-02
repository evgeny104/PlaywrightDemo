import re
import allure
from playwright.sync_api import Locator, expect
from pages.base_page import BasePage

TABS = ("Overview", "Statement", "Statistics", "Dividends", "Documents")


class NvdaBasePage(BasePage):
    BASE_URL = "https://www.metatrader.com/en/symbols/nasdaq/nvda"
    URL = BASE_URL
    _URL_PATTERN = r"/nasdaq/nvda"

    # Locators

    @property
    def symbol_heading(self) -> Locator:
        # h1 на странице содержит тикер "NVDA"
        return self.page.get_by_role("heading", name=re.compile("NVDA", re.IGNORECASE), level=1).first

    def tab_link(self, name: str) -> Locator:
        return self.page.get_by_role("link", name=name, exact=True)

    # Actions

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

    def _assert_url(self) -> str | None:
        try:
            expect(self.page).to_have_url(re.compile(self._URL_PATTERN))
            return None
        except AssertionError as e:
            lines = (l for l in str(e).splitlines() if l.strip())
            return "\n".join(
                l for l in lines
                if not l.startswith(("Call log", "Aria snapshot", "-", " "))
            )
