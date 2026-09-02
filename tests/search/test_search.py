import allure
from playwright.sync_api import expect
from pages.search import HomePage


@allure.title("Поисковая строка видна на главной странице")
def test_search_input_is_visible(home: HomePage):
    expect(home.search_input).to_be_visible()


@allure.title("Нажатие '/' фокусирует поисковую строку")
def test_search_opens_with_slash_key(home: HomePage):
    home.page.keyboard.press("/")
    expect(home.search_input).to_be_focused()


@allure.title("Вводе тикера появляется дропдаун")
def test_search_dropdown_appears(home: HomePage):
    home.search_input.fill("alp")
    expect(home.first_dropdown_item).to_be_visible()


@allure.title("Поиск с префиксом $NVDA показывает дропдаун")
def test_search_by_symbol_prefix(home: HomePage):
    home.search_input.fill("$NVDA")
    expect(home.first_dropdown_item).to_be_visible()