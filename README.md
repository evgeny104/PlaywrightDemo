# PlaywrightDemo

Автотесты для [metatrader.com](https://www.metatrader.com/) на Python + Playwright + pytest.

## Стек

- Python 3.12+
- Playwright 1.61
- pytest 9.1.1
- Allure 2.13.5

## Установка

```bash
pip install -r requirements.txt
playwright install chromium
```

## Запуск тестов

**Все тесты:**
```bash
pytest tests/ --alluredir=reports/allure_report
```

**Только NVDA:**
```bash
pytest tests/nvda/ --alluredir=reports/allure_report
```

**Один тест:**
```bash
pytest tests/nvda/test_statistics.py::TestStatisticsPage::test_valuation_metric_present --alluredir=reports/allure_report
```

**Без allure (быстро):**
```bash
pytest tests/
```

## Allure отчёт

```bash
allure serve reports/allure_report
```

Откроется браузер с отчётом. При падении теста в отчёте будут:
- шаги воспроизведения
- блок **Expected vs Actual**
- скриншот страницы

## Структура

```
tests/
  search/      # поиск на главной странице
  nvda/        # страница акции NVDA (5 вкладок)

pages/
  search/      # HomePage
  nvda/        # NvdaSymbolPage, StatementPage, StatisticsPage, DividendsPage, DocumentsPage
```
