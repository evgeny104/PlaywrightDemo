import allure
from playwright.sync_api import Locator, expect
from pages.nvda.nvda_page import NvdaBasePage


class NvdaDocumentsPage(NvdaBasePage):
    URL = f"{NvdaBasePage.BASE_URL}/documents"
    _URL_PATTERN = r"/nasdaq/nvda/documents"

    # Locators

    @property
    def documents_section(self) -> Locator:
        return self.page.locator("[class*='document'], ul, [class*='filing']").first

    @property
    def document_links(self) -> Locator:
        return self.page.locator("[class*='document'] a, [class*='filing'] a, ul li a")

    @property
    def first_document_link(self) -> Locator:
        return self.document_links.first

    # Actions

    @allure.step("Проверяем страницу Documents NVDA")
    def should_be_opened(self) -> None:
        with allure.step("URL содержит /nasdaq/nvda/documents"):
            self._expect_url(self._URL_PATTERN, description="/nasdaq/nvda/documents")
        with allure.step("Раздел документов виден на странице"):
            self._expect_visible(
                self.documents_section,
                description="раздел со списком документов",
            )

    @allure.step("Проверяем что список документов не пустой")
    def assert_documents_not_empty(self) -> None:
        self._expect_visible(
            self.first_document_link,
            description="первая ссылка на документ в списке",
        )

    @allure.step("Считаем количество документов")
    def get_documents_count(self) -> int:
        return self.document_links.count()
