"""Модуль выгрузки: запись processed parquet и загрузка в БД (sqlite/postgresql)"""

from __future__ import annotations

import os
import sqlite3

import pandas as pd
from sqlalchemy import create_engine, text


def get_pg_creds(sqlite_path: str) -> dict[str, str] | None:
    """Безопасное получение учетных данных PostgreSQL из SQLite.

    Возвращает словарь с credentials или None при ошибке.
    ВАЖНО: не логировать и не выводить значения учетных данных!
    """
    try:
        conn = sqlite3.connect(sqlite_path)
        cur = conn.cursor()
        cur.execute("SELECT url, port, user, pass FROM access LIMIT 1;")
        row = cur.fetchone()
        conn.close()

        if not row:
            return None

        url, port, user, password = row
        return {"url": url, "port": port, "user": user, "password": password, "dbname": "homeworks"}
    except Exception:
        return None


def save_parquet(df: pd.DataFrame, *, out_dir: str = "data/processed", filename: str = "rcsb_dataset.parquet") -> str:
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, filename)
    df.to_parquet(out_path, index=False)
    return out_path


def load_to_db(
    df: pd.DataFrame,
    *,
    table_name: str = "etl_table",
    max_rows: int = 100,
    creds_db: str | None = None,
    output_db: str = "data/output.db",
) -> tuple[int, str]:
    """Записать до max_rows строк в БД. Если указан creds_db, пробует PostgreSQL, иначе SQLite.

    Args:
        df: DataFrame для записи
        table_name: имя таблицы
        max_rows: макс. строк для записи (<=100)
        creds_db: путь к БД с учетными данными PostgreSQL
        output_db: путь к SQLite БД (если creds_db не указан)

    Returns:
        (rows_written, connection_info) - число записанных строк и информация о подключении
    """
    if max_rows > 100:
        max_rows = 100  # жесткое ограничение

    to_write = df.head(max_rows)

    # попытка PostgreSQL если указан creds_db
    if creds_db:
        creds = get_pg_creds(creds_db)
        if creds:
            try:
                conn_str = f"postgresql+psycopg2://{creds['user']}:{creds['password']}@{creds['url']}:{creds['port']}/{creds['dbname']}"
                engine = create_engine(conn_str)
                to_write.to_sql(table_name, engine, schema="public", if_exists="replace", index=False)

                with engine.connect() as conn:
                    result = conn.execute(text(f"SELECT COUNT(*) FROM {table_name};"))
                    count = result.scalar_one()
                return int(count), f"PostgreSQL table: public.{table_name}"
            except Exception:
                # при ошибке PostgreSQL используем SQLite
                pass

    # SQLite fallback
    os.makedirs(os.path.dirname(output_db), exist_ok=True)
    engine = create_engine(f"sqlite:///{output_db}")
    to_write.to_sql(table_name, engine, if_exists="replace", index=False)

    with engine.connect() as conn:
        result = conn.execute(text(f"SELECT COUNT(*) FROM {table_name};"))
        count = result.scalar_one()

    return int(count), f"SQLite: {output_db}"


def load(
    df: pd.DataFrame,
    *,
    table_name: str = "etl_table",
    max_rows: int = 100,
    creds_db: str | None = None,
) -> tuple[dict, dict]:
    """Унифицированная функция: сохраняет parquet и записывает в БД.

    Если указан creds_db, попробует PostgreSQL, иначе SQLite.
    Возвращает два словаря: info_parquet, info_db
    """
    parquet_path = save_parquet(df)
    rows_written, db_info = load_to_db(df, table_name=table_name, max_rows=max_rows, creds_db=creds_db)

    info_parquet = {"path": parquet_path, "rows": len(df), "cols": len(df.columns)}
    info_db = {"connection": db_info, "table": table_name, "rows_written": rows_written}
    return info_parquet, info_db
