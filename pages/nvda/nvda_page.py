import re

from playwright.sync_api import Locator

from pages.symbol_base_page import SymbolBasePage


class NvdaBasePage(SymbolBasePage):
    BASE_URL = "https://www.metatrader.com/en/symbols/nasdaq/nvda"
    URL = BASE_URL
    _URL_PATTERN = r"/nasdaq/nvda"

    @property
    def symbol_heading(self) -> Locator:
        return self.page.get_by_role("heading", name=re.compile("NVDA", re.IGNORECASE), level=1).first
