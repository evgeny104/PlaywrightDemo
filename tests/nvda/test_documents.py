"""
Техника: Boundary Value Analysis + Equivalence Partitioning

BVA — первый документ (нижняя граница списка) и общее количество > 0.
      href: пустая строка или "#" = невалидная граница; непустой путь = валидная.

EP — ссылки делятся на классы: валидные (непустой href, не якорь "#"),
     невалидные (пустые, только "#"). Все документы должны быть из валидного класса.
"""
import allure
from playwright.sync_api import expect
from pages.nvda.documents_page import NvdaDocumentsPage


@allure.feature("Вкладка Documents NVDA")
class TestDocumentsPage:

    @allure.title("Страница Documents открывается с корректным URL")
    def test_documents_page_opens(self, nvda_documents: NvdaDocumentsPage):
        # Smoke: страница достижима и URL корректен
        nvda_documents.should_be_opened()

    @allure.title("Раздел документов виден на странице")
    def test_documents_section_visible(self, nvda_documents: NvdaDocumentsPage):
        # Smoke: основной контейнер рендерится
        expect(nvda_documents.documents_section).to_be_visible()

    @allure.title("Список документов не пустой")
    def test_documents_list_not_empty(self, nvda_documents: NvdaDocumentsPage):
        # BVA: нижняя граница — минимум 1 документ в списке
        nvda_documents.assert_documents_not_empty()

    @allure.title("Количество документов больше нуля")
    def test_documents_count_positive(self, nvda_documents: NvdaDocumentsPage):
        # BVA: граничное значение количества — > 0
        count = nvda_documents.get_documents_count()
        assert count > 0, f"Ожидается минимум 1 документ, найдено: {count}"

    @allure.title("Первый документ содержит непустой href")
    def test_first_document_has_valid_href(self, nvda_documents: NvdaDocumentsPage):
        # BVA: первый элемент (нижняя граница) имеет непустой href
        # EP: href принадлежит классу «валидных ссылок» (не пустой и не "#")
        href = nvda_documents.first_document_link.get_attribute("href")
        assert href and href != "#", f"Первый документ должен иметь непустой href, получено: '{href}'"

    @allure.title("Все документы имеют непустые href (EP: класс валидных ссылок)")
    def test_all_document_links_have_href(self, nvda_documents: NvdaDocumentsPage):
        # EP: любая ссылка из списка — представитель класса «валидные ссылки»
        count = nvda_documents.get_documents_count()
        for i in range(count):
            link = nvda_documents.document_links.nth(i)
            with allure.step(f"Документ #{i + 1} имеет href"):
                href = link.get_attribute("href")
                assert href and href != "#", f"Документ #{i + 1}: недопустимый href='{href}'"
