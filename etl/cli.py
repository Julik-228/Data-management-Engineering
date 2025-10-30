"""Console script and entrypoint for the ETL pipeline."""

from __future__ import annotations

import typer
from rich.console import Console

import extract, load, transform

app = typer.Typer()
console = Console()


@app.command()
def run(
    stage: str = typer.Argument(..., help="Этап для запуска: extract|transform|load|all"),
    file_id: str | None = typer.Option(
        None, "--file-id", "-f", help="Google Drive file id для загрузки CSV. Используйте для этапа extract."
    ),
    url: str | None = typer.Option(
        None, "--url", "-u", help="Прямая ссылка на CSV файл. Альтернатива для --file-id на этапе extract."
    ),
    csv_path: str | None = typer.Option(
        None,
        "--csv-path",
        "-c",
        help="Путь к локальному CSV файлу. Используется на этапе transform, если данные уже загружены.",
    ),
    table_name: str = typer.Option(
        "etl_table", "--table-name", "-t", help="Имя таблицы для записи в БД. Используется на этапе load."
    ),
    max_rows: int = typer.Option(
        100,
        "--max-rows",
        "-n",
        help="Максимальное количество строк для записи в БД (не более 100). Используется на этапе load.",
    ),
    creds_db: str | None = typer.Option(
        None,
        "--creds-db",
        help="Путь к SQLite БД с учетными данными PostgreSQL. Если не указан, используется локальная SQLite.",
    ),
) -> None:
    """ETL pipeline для обработки и загрузки данных.

    Поддерживает три этапа (укажите один через аргумент stage):

    \b
    extract   Загрузка сырых данных из источника (Google Drive или URL)
             Требует --file-id или --url
             Сохраняет в data/raw/raw.csv

    \b
    transform Преобразование данных и типов
             Читает из data/raw/raw.csv или --csv-path
             Сохраняет в data/processed/rcsb_dataset.parquet

    \b
    load     Загрузка в БД (PostgreSQL или SQLite)
             Читает из data/processed/rcsb_dataset.parquet
             Использует --table-name и --max-rows
             Для PostgreSQL требуется --creds-db

    \b
    all      Выполняет все этапы последовательно
             Требует те же параметры, что и extract

    Примеры:
    \b
    # Только загрузка из Google Drive
    $ python main.py run extract --file-id abcd1234

    \b
    # Только трансформация локального CSV
    $ python main.py run transform --csv-path data/my.csv

    \b
    # Загрузка в PostgreSQL через credentials
    $ python main.py run load --table-name my_table --creds-db creds.db

    \b
    # Полный pipeline с загрузкой в локальный SQLite
    $ python main.py run all --file-id abcd1234 --table-name my_table
    """
    """Run ETL stage. stage is required. When omitted Typer shows help.

    Stages: extract, transform, load, all
    """
    stage = stage.lower()
    if stage not in {"extract", "transform", "load", "all"}:
        console.print(f"Unknown stage: {stage}. Choose from extract|transform|load|all")
        raise typer.Exit(code=1)

    df = None
    raw_csv = None

    if stage in {"extract", "all"}:
        if not file_id and not url:
            console.print("For extract stage provide --file-id or --url")
            raise typer.Exit(code=2)
        console.print("Starting extract...")
        df, raw_csv = extract.load_source(file_id=file_id, url=url)
        console.print(f"Saved raw csv to: {raw_csv}")

    if stage in {"transform", "all"}:
        if df is None:
            # try to read csv_path or default
            csv_to_use = csv_path or raw_csv or "data/raw/raw.csv"
            try:
                df = __import__("pandas").read_csv(csv_to_use)
            except Exception as e:
                console.print(f"Cannot read CSV for transform: {e}")
                raise typer.Exit(code=3) from e
        console.print("Starting transform...")
        df, parquet_path = transform.transform_df(df)
        console.print(f"Transformed data saved to: {parquet_path}")

    if stage in {"load", "all"}:
        if df is None:
            # try to read processed parquet
            try:
                pd = __import__("pandas")
                df = pd.read_parquet("data/processed/rcsb_dataset.parquet")
            except Exception as e:
                console.print(f"Cannot read processed parquet for load: {e}")
                raise typer.Exit(code=4) from e

        # enforce max_rows limit
        if max_rows > 100:
            console.print("max_rows capped to 100")
            max_rows = 100

        console.print("Starting load...")
        info_parquet, info_db = load.load(df, table_name=table_name, max_rows=max_rows, creds_db=creds_db)

        # не выводим детали подключения в консоль
        console.print("Load finished. Summary:")
        console.print(
            f"Parquet saved: {info_parquet['path']} ({info_parquet['rows']} rows, {info_parquet['cols']} cols)"
        )
        console.print(f"DB load: wrote {info_db['rows_written']} rows to {info_db['table']}")


if __name__ == "__main__":
    app()
