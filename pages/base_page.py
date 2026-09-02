import allure
from playwright.sync_api import Page, Locator, expect


class BasePage:

    def __init__(self, page: Page):
        self.page = page

    def _expect_visible(self, locator: Locator, description: str, timeout: int = 5000) -> None:
        """Проверяет видимость элемента; при падении — чистое Expected/Actual без Aria-snapshot."""
        try:
            expect(locator).to_be_visible(timeout=timeout)
        except AssertionError:
            allure.attach(
                f"Ожидалось:  «{description}» — виден на странице\n"
                f"Фактически: элемент не найден",
                name="Expected vs Actual",
                attachment_type=allure.attachment_type.TEXT,
            )
            raise AssertionError(f"Не найдено на странице: «{description}»") from None

    def _expect_text(self, locator: Locator, expected: str, description: str) -> None:
        """Проверяет точный текст; при падении показывает ожидаемое vs фактическое."""
        try:
            expect(locator).to_have_text(expected)
        except AssertionError:
            try:
                actual = locator.inner_text().strip()
            except Exception:
                actual = "не удалось получить значение"
            allure.attach(
                f"Ожидалось:  «{description}» = «{expected}»\n"
                f"Фактически: «{actual}»",
                name="Expected vs Actual",
                attachment_type=allure.attachment_type.TEXT,
            )
            raise AssertionError(
                f"«{description}»: ожидалось «{expected}», получено «{actual}»"
            ) from None

    def _expect_contains_text(self, locator: Locator, expected: str, description: str) -> None:
        """Проверяет наличие подстроки; при падении показывает ожидаемое vs фактическое."""
        try:
            expect(locator).to_contain_text(expected)
        except AssertionError:
            try:
                actual = locator.inner_text().strip()
            except Exception:
                actual = "не удалось получить значение"
            allure.attach(
                f"Ожидалось:  «{description}» содержит «{expected}»\n"
                f"Фактически: «{actual}»",
                name="Expected vs Actual",
                attachment_type=allure.attachment_type.TEXT,
            )
            raise AssertionError(
                f"«{description}» не содержит «{expected}»; получено: «{actual}»"
            ) from None

    def _expect_page_title(self, pattern, description: str) -> None:
        """Проверяет заголовок страницы; при падении показывает фактический title."""
        try:
            expect(self.page).to_have_title(pattern)
        except AssertionError:
            try:
                actual = self.page.title()
            except Exception:
                actual = "не удалось получить title"
            allure.attach(
                f"Ожидалось:  заголовок страницы содержит «{description}»\n"
                f"Фактически: «{actual}»",
                name="Expected vs Actual",
                attachment_type=allure.attachment_type.TEXT,
            )
            raise AssertionError(
                f"Заголовок страницы не содержит «{description}»; получено: «{actual}»"
            ) from None
