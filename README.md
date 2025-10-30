# Data-management-Engineering

Проект ETL оформлен с использованием Cookiecutter-шаблона `etl-julia` (https://github.com/Julik-228/etl-julia). Шаблон дает готовую модульную структуру проекта, CLI и стартовые реализации этапов extract / transform / load.

Репозиторий проекта «Инжиниринг управления данными ИТМО». Цель: показать пример простого ETL-пайплайна, набор вспомогательных скриптов для загрузки/обработки данных, а также примеры работы с API и парсинга текстовых файлов.

> Важно: некоторые артефакты (локальные данные, секреты, виртуальные окружения) обычно не добавляются в репозиторий - см. раздел безопасности и notes ниже.

## Содержание проекта

- Скрипты: `data_loader.py`, `data_processing.py` - работа с основным CSV/Parquet датасетом.
- ETL-пакет `etl/` - полноценный CLI-пайплайн (extract, transform, load).
- Примеры: `api_example/`, `parse_example/` - демонстрации работы с API и парсинга.
- Ноутбук `notebooks/EDA.ipynb` - исследовательский анализ данных.

## Ссылки на датасеты

**Ссылка на датасеты**: [Папка на Google Drive](https://drive.google.com/drive/folders/1QAz7jx7AGHJcXc0OftuolaaU4slls4CO?usp=sharing)  

**Исходный источник датасета**: [RCSB PDB Macromolecular Structure Dataset на Kaggle](https://www.kaggle.com/datasets/samiraalipour/rcsb-pdb-macromolecular-structure-dataset?utm_source=chatgpt.com&select=RCSB_PDB_Macromolecular_Structure_Dataset.csv)

---

## Установка и запуск

Требования: Python 3.7+ и pip.

1) Клонировать репозиторий и перейти в папку:

```powershell
git clone https://github.com/Julik-228/Data-management-Engineering.git
cd Data-management-Engineering
```

2) Создать виртуальное окружение и активировать (Windows example):

```powershell
python -m venv venv
venv\Scripts\activate
```

3) Установить зависимости:

```powershell
pip install -r requirements.txt
```

4) Запуск ETL CLI (из корня проекта):

```powershell
python -m etl.cli run all --file-id <FILE_ID> --table-name etl_table
```

ИЛИ запустить конкретный этап:

```powershell
python -m etl.cli run extract --file-id <FILE_ID>
python -m etl.cli run transform --csv-path data/raw/raw.csv
python -m etl.cli run load --table-name my_table --creds-db path/to/creds.db
```

> Примечание: `--creds-db` используется для чтения учетных данных PostgreSQL из локального SQLite-файла. Ни в коем случае не храните реальные пароли в репозитории.

---

## Cтруктура проекта

```
Data-management-Engineering/
├── etl/                    # ETL-пакет (cli, extract, transform, load, validate, utils)
│   ├── __init__.py
│   ├── __main__.py         # точка входа для `python -m etl`
│   ├── cli.py              # Typer CLI: run (extract|transform|load|all)
│   ├── extract.py          # загрузка CSV (Google Drive/URL) + базовая валидация
│   ├── transform.py        # преобразование типов, сохранение parquet
│   ├── load.py             # сохранение parquet и загрузка в БД (Postgres/SQLite)
│   ├── validate.py         # вспомогательная валидация (df_not_empty, parquet_info_valid)
│   └── utils.py            # утилиты (заглушка)
├── experiments/            # Эксперименты и прототипы
│   ├── api_example/        # Примеры работы с API (скрипты, README)
│   ├── parse_example/      # Примеры парсинга текстовых данных
│   ├── notebooks/          # Jupyter notebooks и черновые эксперименты (EDA.ipynb и др.)
│   ├── data_loader.py      # экспериментальные/альтернативные скрипты загрузки
│   ├── data_processing.py  # экспериментальные/альтернативные скрипты обработки
│   ├── write_to_db.py      # пример записи в БД (локальный пример)
│   └── README.md           # README, относящийся к экспериментам
├── requirements.txt
└── README.md
```

---

## Детальное описание важных файлов и модулей

Ниже — подробное описание файлов в пакете `etl/` и основных корневых скриптов.

### etl/

- `__init__.py` — метаданные пакета (author, email).

- `__main__.py` — вызывает `app()` из `cli.py`, позволяет запускать пакет командой `python -m etl`.

- `cli.py` - основной CLI (встроен Typer + rich для удобного вывода). Поддерживает команды:
   - extract - загрузка CSV из Google Drive (`file_id`) или по `--url`. Сохраняет в `data/raw/raw.csv`.
   - transform - преобразование типов (числа, даты, категории), сохраняет Parquet в `data/processed/rcsb_dataset.parquet`.
   - load - загрузка в БД: при указании `--creds-db` пытается использовать PostgreSQL (учетные данные читаются из SQLite-файла), иначе - fallback в SQLite (`data/output.db`). Параметры: `--table-name`, `--max-rows`.
   - all - выполняет extract → transform → load.

- `extract.py` - реализация загрузки CSV и базовой валидации:
   - `download_csv_from_google(file_id)` - скачивает CSV по file_id из Google Drive.
   - `save_raw_csv(df, out_path='data/raw/raw.csv')` - сохраняет CSV локально (создает папку).
   - `validate_raw(df)` - простая валидация: не пустой DataFrame, есть колонки.
   - `load_source(file_id=None, url=None)` - обертка, возвращает `(df, saved_csv_path)`.

- `transform.py` - логика преобразования DataFrame:
   - `transform_df(df)` приводит dtypes с помощью `convert_dtypes()`, пробует конвертировать строки в числа (заменяя запятые на точки), пытается парсить даты (столбцы `Deposition Date`, `Release Date`), переводит колонки с низкой кардинальностью в `category`. Сохраняет результат в `data/processed/rcsb_dataset.parquet`.

- `load.py` - сохранение parquet и загрузка в БД:
   - `get_pg_creds(sqlite_path)` - читает из локальной SQLite таблицы `access` параметры подключения к Postgres (url, port, user, pass). Возвращает словарь или None.
   - `save_parquet(df, out_dir='data/processed')` - сохраняет parquet.
   - `load_to_db(df, table_name, max_rows, creds_db, output_db)` - пытается записать в Postgres (если creds найдены), иначе записывает в SQLite (`data/output.db`). Возвращает `(rows_written, connection_info)`.
   - `load(df, ...)` - wrapper: сохранить parquet и выполнить `load_to_db`, возвращает словари с информацией.

- `validate.py` - небольшие проверки: `df_not_empty`, `parquet_info_valid`.

- `utils.py` - заглушка для утилит (можно расширить).

### Подробная документация по ETL (контракт, запуск, отладка)

Ниже расширенная документация, сфокусированная на ETL-пакете: что принимает, что выдает, какие есть параметры и как отлаживать.

1) Краткий контракт (inputs / outputs / side-effects)

- Inputs:
   - для `extract`: `file_id` (Google Drive file id) или `url` (прямая ссылка на CSV).
   - для `transform`: `csv_path` (локальный CSV) или входной pandas.DataFrame.
   - для `load`: `parquet` в `data/processed/rcsb_dataset.parquet` или `df` в памяти; опционально `creds_db` (путь к SQLite с параметрами для Postgres).

- Outputs / side-effects:
   - `data/raw/raw.csv` (при extract)
   - `data/processed/rcsb_dataset.parquet` (при transform / save_parquet)
   - БД: запись в Postgres (если `creds_db` валиден) либо в `data/output.db` (SQLite) - таблица `table_name`.

2) CLI — параметры и примеры

- Основной синтаксис:

```powershell
python -m etl.cli run <stage> [--file-id <id>] [--url <url>] [--csv-path <path>] [--table-name <name>] [--max-rows <n>] [--creds-db <path>]
```

- Примеры PowerShell:

```powershell
# Полный pipeline (extract -> transform -> load) из Google Drive
python -m etl.cli run all --file-id abcd1234 --table-name etl_table

# Только extract из прямой ссылки
python -m etl.cli run extract --url "https://example.com/my.csv"

# Трансформировать локальный CSV
python -m etl.cli run transform --csv-path data/raw/raw.csv

# Загрузить в Postgres, используя локальный sqlite creds.db
python -m etl.cli run load --table-name my_table --creds-db path\to\creds.db
```

3) Формат и схема `creds.db` (что ожидает `get_pg_creds`)

Функция `get_pg_creds(sqlite_path)` ожидает, что в SQLite есть таблица `access` с колонками (пример):

```sql
CREATE TABLE access (
   url TEXT,
   port INTEGER,
   user TEXT,
   pass TEXT
);
```

`get_pg_creds` читает первую запись и возвращает словарь: `{'url','port','user','password','dbname':'homeworks'}`.

ВАЖНО: не держите реальные пароли в Git. Используйте `creds.db` только локально и добавляйте его в `.gitignore`.

4) Ограничения и поведение

- `max_rows` имеет жесткое ограничение: не более 100 (в коде принудительно приводится к 100).
- Если `creds_db` указан, код пробует подключиться к Postgres; при любой ошибке произойдет fallback на SQLite (локально `data/output.db`).
- При `transform` алгоритм автоматически пытается конвертировать значения:
   - строки → числа (замена "," на "."), если ≥90% значений могут быть конвертированы;
   - даты для колонок `Deposition Date` и `Release Date` (формат `%Y-%m-%d`);
   - столбцы с низкой кардинальностью → `category`.

5) Частые ошибки и способы отладки

- Cannot read CSV for transform: убедитесь, что `--csv-path` указывает на существующий CSV или что `data/raw/raw.csv` был создан после extract.
- Cannot read processed parquet for load: выполняйте `transform` перед `load`, либо укажите корректный путь `data/processed/rcsb_dataset.parquet`.
- Проблемы с Postgres: проверьте структуру `creds.db`, корректность пароля/порта/url. Логи ошибок маскируются в `cli` — используйте вызов `load.load_to_db` напрямую из REPL для детальной отладки.

6) Примеры быстрого локального тестирования (в REPL)

Откройте Python в виртуальном окружении и выполните минимальную последовательность:

```powershell
python
>>> from etl import extract, transform, load
>>> df, csv_path = extract.load_source(url='https://example.com/my.csv')
>>> df, parquet = transform.transform_df(df)
>>> info_parquet, info_db = load.load(df, table_name='test', max_rows=10)
>>> info_parquet, info_db
```

7) Рекомендации по безопасности и CI

- Добавьте `creds.db` и содержимое `data/` в `.gitignore`.
- В CI используйте secrets для подключения к реальным БД и тестовым наборам данных.

### Корневые скрипты и папки

- `etl/` - пакет с CLI и реализациями этапов ETL (см. раздел выше).
- `experiments/` - основная папка, где собраны экспериментальные и вспомогательные материалы:
   - `api_example/`, `parse_example/`, `notebooks/` - примеры и ноутбуки находятся внутри `experiments/`.
   - `data_loader.py`, `data_processing.py`, `write_to_db.py` - экспериментальные версии скриптов для загрузки/обработки/записи в БД.
   - `README.md` внутри `experiments/` описывает содержимое этой папки (черновики, прототипы, заметки).
- `requirements.txt` - зависимости проекта.

---

## Безопасность и хорошие практики

- Не храните учетные данные в репозитории. Файл `creds.db` или аналогичные контейнеры с паролями не должны попадать в git. Используйте `.gitignore` и переменные окружения.
- Папку `data/` обычно стоит исключить из репозитория (gitignored). Вместо этого храните в облаке (Google Drive) и добавляйте инструкции по скачиванию (см. ссылку выше).
- При работе с Postgres используйте защищенные секреты (Vault, environment variables, CI secrets) вместо локальных SQLite с паролями.

---

## Примеры использования 

- Запустить полный пайплайн, загрузить CSV из Google Drive, трансформировать и загрузить в локальную SQLite:

```powershell
python -m etl.cli run all --file-id <FILE_ID> --table-name my_table
```

- Трансформировать локальный CSV и сохранить parquet:

```powershell
python -m etl.cli run transform --csv-path data/raw/raw.csv
```


