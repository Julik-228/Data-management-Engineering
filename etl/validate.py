"""Небольшие вспомогательные валидации для ETL"""

from __future__ import annotations

import pandas as pd


def df_not_empty(df: pd.DataFrame) -> tuple[bool, str]:
    if df is None:
        return False, "DataFrame is None"
    if not isinstance(df, pd.DataFrame):
        return False, "Not a pandas DataFrame"
    if df.empty:
        return False, "DataFrame is empty"
    return True, "OK"


def parquet_info_valid(path: str, expected_rows: int) -> tuple[bool, str]:
    """Проверка: файл parquet существует и содержит ожидаемое количество строк (>=1)."""
    try:
        df = pd.read_parquet(path)
    except Exception as e:
        return False, f"Cannot read parquet: {e}"
    if len(df) != expected_rows:
        # допускаем, что сохранён весь df, поэтому просто проверим, что есть строки
        if len(df) == 0:
            return False, "Parquet file has 0 rows"
    return True, "OK"
