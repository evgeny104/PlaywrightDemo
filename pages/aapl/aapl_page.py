import re

from playwright.sync_api import Locator

from pages.symbol_base_page import SymbolBasePage


class AaplBasePage(SymbolBasePage):
    BASE_URL = "https://www.metatrader.com/en/symbols/nasdaq/aapl"
    URL = BASE_URL
    _URL_PATTERN = r"/nasdaq/aapl"

    @property
    def symbol_heading(self) -> Locator:
        return self.page.get_by_role("heading", name=re.compile("AAPL", re.IGNORECASE), level=1).first
