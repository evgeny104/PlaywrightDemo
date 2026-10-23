# PlaywrightDemo

UI-автотесты для [metatrader.com](https://www.metatrader.com/). Python + Playwright + pytest + Allure. POM-архитектура.

**Стек:** Python 3.12 • Playwright 1.61 • pytest 9.1.1 • Allure 2.13.5

---

## Установка

```bash
pip install -r requirements.txt
playwright install chromium
```

## Запуск тестов

```bash
# все тесты, без отчёта (быстро)
pytest tests/

# все тесты + собрать Allure-отчёт
pytest tests/ --alluredir=reports/allure_report

# один модуль (NVDA / AAPL / search)
pytest tests/nvda/
pytest tests/aapl/
pytest tests/search/

# один тест по имени
pytest tests/nvda/test_statistics.py::TestStatisticsPage::test_valuation_metric_present
```

## Allure-отчёт

```bash
allure serve reports/allure_report
```

При падении теста в отчёте: шаги воспроизведения, блок **Expected vs Actual**, скриншот страницы.

## Структура

```
pages/
  base_page.py        # BasePage + helpers _expect_visible / _expect_text / ...
  search/             # HomePage
  nvda/               # 5 вкладок акции NVDA
  aapl/               # Overview AAPL (создан AI-пайплайном)

tests/
  search/             # поиск на главной
  nvda/
  aapl/
```

---

## AI-driven workflow

Проект демонстрирует работу с [Claude Code](https://claude.com/claude-code) по схеме **policy + two-agent pipeline**: правила в одном файле, два агента отвечают за код и ревью.

```
                 CLAUDE.md
          (10 правил Playwright
       + 9 жёстких правил проекта)
                    │
         ┌──────────┴──────────┐
         ▼                     ▼
  metatrader-pom       metatrader-reviewer
     (writer)              (reviewer)
  пишет POM + тесты    находит нарушения
  до зелёного pytest    path:line + rule
```

### Файлы пайплайна

| Файл | Назначение |
|---|---|
| [`CLAUDE.md`](./CLAUDE.md) | Политика проекта. Автоматически инжектится в контекст Claude Code и каждого субагента. |
| [`.claude/agents/metatrader-pom.md`](./.claude/agents/metatrader-pom.md) | Writer — пишет Page Object и pytest-тесты по образцу `pages/nvda/*`. |
| [`.claude/agents/metatrader-reviewer.md`](./.claude/agents/metatrader-reviewer.md) | Reviewer — проверяет код против `CLAUDE.md`, возвращает структурированный отчёт. |
| [`.claude/commands/review-loop.md`](./.claude/commands/review-loop.md) | Слэш-команда `/review-loop` — writer↔reviewer в автоцикле до `approve` (max 3 итерации). |
| [`agents/rules for the playwright.txt`](./agents/rules%20for%20the%20playwright.txt) | Первоисточник правил (TS-синтаксис). `CLAUDE.md` — python-адаптация. |

### Как запускать

**1. Writer — покрыть новый тикер:**
```
Используя metatrader-pom, добавь Page Object и тесты для вкладки
Overview акции AAPL (nasdaq) по образцу NVDA.
```
→ создаёт `pages/aapl/*`, `tests/aapl/*`, прогоняет `pytest` до зелёного.

**2. Reviewer — проверить код:**
```
Запусти metatrader-reviewer на pages/aapl/* и tests/aapl/*.
```
→ возвращает таблицу `path:line / severity / правило / описание / рекомендация` и вердикт `approve` | `request changes` | `reject`.

**3. Автоцикл до чистого approve:**
```
/review-loop pages/aapl tests/aapl
```
→ reviewer проверяет; если есть находки — writer правит; повтор до `approve`, падения pytest или лимита в 3 итерации.

### Пример реального прогона на AAPL

| Итерация | Reviewer | Writer | pytest |
|---|---|---|---|
| 1 | 6 находок (3 major, 1 minor, 2 nit) → `request changes` | — | — |
| 2 | — | 4 fixed, 1 wontfix (grandfathered), 1 N/A | 6 passed |
| 3 | нарушений нет → `approve` | — | 6 passed |

### Принципы пайплайна

- **Единый source of truth** — правила в `CLAUDE.md`, не дублируются в агентах.
- **Разделение ролей** — writer пишет, reviewer находит; правки — вторым витком.
- **Воспроизводимость** — любой тикер покрывается одним промтом.
- **Human-in-the-loop** — финальное решение за разработчиком.
