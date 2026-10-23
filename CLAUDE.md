# PlaywrightDemo — AI-agents instructions

Автотесты для metatrader.com на Python 3.12 + Playwright 1.61 (sync API) + pytest 9.1.1 + Allure 2.13.5. Архитектура — Page Object Model.

Этот файл автоматически загружается в контекст Claude Code и всех субагентов. Соблюдать без исключений.

## Структура

```
pages/
  base_page.py            # BasePage: _expect_visible / _expect_text / _expect_contains_text / _expect_page_title
  <ticker>/
    <ticker>_page.py      # <Ticker>BasePage(BasePage): BASE_URL, _URL_PATTERN, _assert_url()
    symbol_page.py        # вкладка Overview
    statement_page.py / statistics_page.py / dividends_page.py / documents_page.py
tests/
  <ticker>/
    conftest.py           # фикстуры открытия вкладок, _pages[request.node.nodeid]=page
    test_*.py             # @allure.feature на классе, @allure.title на методе
agents/
  rules for the playwright.txt   # первоисточник (TS-синтаксис, этот CLAUDE.md — python-адаптация)
.claude/agents/           # subagent definitions (writer, reviewer)
```

## 10 правил написания тестов (адаптировано под Python + pytest)

### 1. Селекторы — как видит пользователь

Приоритет: `get_by_role` → `get_by_label` → `get_by_text` → `locator("tag[attr]")` → `label.row` + `.filter(has_text=...)` (стиль metatrader).

CSS-пути вида `div.container > span.btn-primary` и XPath — только когда никакой семантики в DOM нет и это зафиксировано комментарием.

```python
# good
self.page.get_by_role("heading", name="NVDA", level=1)
self.page.locator("label.row").filter(has_text="Dividend yield %")

# bad
self.page.locator("div.card > div > span.value")  # сломается при редизайне
```

### 2. Только web-first assertions, никаких `sleep`

Все ожидания — через `expect(locator).to_...` (в тестах) или `self._expect_*(...)` (в Page Object). Эти проверки сами ретраятся до таймаута Playwright.

```python
# good
self._expect_visible(self.price_value, description="цена акции")

# bad
import time; time.sleep(3)                 # запрещено
self.page.wait_for_timeout(3000)           # запрещено
```

Исключение: `page.wait_for_load_state("networkidle")` допустим один раз при открытии страницы в фикстуре.

### 3. Изоляция каждого теста

Каждый тест получает собственный `Page` через фикстуру pytest-playwright. Нет общего state, нет зависимости от порядка выполнения.

- Фикстура открывает страницу: `page.goto(URL)` + `yield PageObject(page)`.
- Регистрация страницы в `_pages[request.node.nodeid] = page` — для хука скриншота при падении.
- Никаких `pytest.fixture(scope="module")` для `page`.

### 4. (N/A для этого проекта)

Правило оригинала — «готовь данные через API, не через UI». metatrader.com — внешний сайт без доступа к бэкенду. Пропускаем. Если в будущем будет свой стенд — вернуть.

### 5. Приоритет локаторов (расширение правила 1)

Порядок выбора селектора — строго сверху вниз, следующий уровень допустим только если верхний не даёт стабильного попадания:

1. `get_by_role(..., name=...)` — ARIA-роль + доступное имя
2. `get_by_label(...)` — для форм
3. `get_by_text(...)` / `get_by_placeholder(...)`
4. CSS по семантическому тегу/атрибуту: `locator("h1")`, `locator("[aria-label=...]")`
5. `data-testid` (на metatrader их нет — не ждите)
6. Структурный CSS (`label.row` + `has_text`) — последний эшелон, принят в проекте для табличных структур

### 6. Трассировка — on-first-retry

Запуск pytest-playwright с `--tracing=retain-on-failure` и `--retries=1`. Включать `--tracing=on` постоянно запрещено — замусоривает диск и замедляет прогон. Скриншот при падении теста собирается хуком через `_pages[request.node.nodeid]`.

### 7. Параллельный запуск по умолчанию

Тесты независимы ⇒ `pytest -n auto` (через pytest-xdist) должен проходить. Если новый тест требует последовательного запуска — это баг теста, не исключение.

### 8. Никаких `if` / `try` в тестах

Тест — один сценарий, одна ветка. Если проверяем «кнопка есть и кликабельна» — это ассерт, не ветвление. `try/except` в тестах прячет реальную причину падения.

```python
# good
expect(checkout).to_be_enabled()
checkout.click()

# bad
if checkout.is_visible():
    checkout.click()         # прячет баг, если кнопка пропала
```

Внутри Page Object `try/except` допустим только для оборачивания в понятный `AssertionError` — так уже сделано в `BasePage._expect_*`.

### 9. Проверяем поведение, не внутренности

Ассерты — только на то, что видно пользователю: текст, видимость, URL, title. Запрещено проверять:
- CSS-классы (`class="is-active"`)
- точную HTML-структуру
- внутренние атрибуты, не отражённые в UX

### 10. Проекты и браузеры — через конфиг, не хардкод

Браузер выбирается через `--browser chromium|firefox|webkit` (pytest-playwright), не хардкодится в тестах. Текущий `pytest.ini` стартует с `--headed` для локальной разработки; CI будет без него.

## Жёсткие правила проекта (сверх 10 выше)

1. **Проверки в Page Object — только через `self._expect_*`**. Голый `expect(...)` в POM — запрещён. В тестах голый `expect()` допустим для простых smoke (как в `tests/nvda/test_overview.py`).
2. **Локаторы — только `@property` внутри Page Object**. В тестовых файлах локаторов быть не должно.
3. **Allure разметка:**
   - `@allure.step("...")` на каждом публичном методе POM
   - `with allure.step("..."):` для подшагов внутри метода
   - `@allure.feature(...)` на тестовом классе, `@allure.title(...)` на тестовом методе
4. **Новый тикер = новый базовый класс:** `pages/<ticker>/<ticker>_page.py` с `<Ticker>BasePage(BasePage)`, `BASE_URL`, `_URL_PATTERN`, `_assert_url()`.
5. **Фикстура тикера:** в `tests/<ticker>/conftest.py` обязательно `_pages[request.node.nodeid] = page` и `_pages.pop(...)` после yield — иначе screenshot-on-failure не сработает.
6. **Язык:** `@allure.step`, `description=`, `AssertionError` — на русском. Код, имена классов и методов — на английском.
7. **URL-паттерны** — через `re.compile`, фрагмент пути без `^`/`$`, кроме случаев точного соответствия.
8. **Не трогать без явной просьбы:** `pages/base_page.py`, `pages/nvda/**`, `pages/search/**`, `tests/nvda/**`, `screenshot_store.py`, `pytest.ini`, `requirements.txt`, корневой `conftest.py`.
9. **Запрещены:**
   - `async`-API Playwright (только sync)
   - `time.sleep(...)` и `page.wait_for_timeout(...)` в прикладном коде
   - голый `assert ...` вместо `_expect_*` в POM
   - комментарии `# TODO`, `# FIXME`, артефакты рефакторинга

## Проверка готовности задачи

Перед тем как отрапортовать «готово»:
1. `pytest tests/<module>/ -v` — зелёный прогон.
2. Нет селекторов в тестовых файлах.
3. Нет голого `expect()` в Page Object.
4. Allure-разметка на месте.
5. Новые/изменённые файлы перечислены с абсолютными путями.
