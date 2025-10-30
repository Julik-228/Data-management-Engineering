"""Transformations for raw DataFrame: приведение типов и сохранение parquet"""

from __future__ import annotations

import os

import pandas as pd


def transform_df(df: pd.DataFrame) -> tuple[pd.DataFrame, str]:
    """Привести типы колонок, вернуть transformed df и путь к parquet в data/processed.

    - приводит строки, пытается превратить в числа, даты
    - переводит колонки с низкой кардинальностью в category
    """
    df = df.copy()
    df = df.convert_dtypes()

    for col in df.columns:
        if df[col].dtype == "string" or df[col].dtype == object:
            s = df[col].astype("string").str.strip()

            s_num = pd.to_numeric(s.str.replace(",", ".", regex=False), errors="coerce")
            if s_num.notna().sum() / len(s) >= 0.9:
                df[col] = s_num
                continue

            date_columns = ["Deposition Date", "Release Date"]
            if col in date_columns:
                s_dt = pd.to_datetime(s, errors="coerce", format="%Y-%m-%d")
                if s_dt.notna().sum() / len(s) >= 0.9:
                    df[col] = s_dt
                    continue

            if df[col].nunique(dropna=True) / len(df) < 0.5:
                df[col] = s.astype("category")
            else:
                df[col] = s

    out_dir = os.path.join("data", "processed")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "rcsb_dataset.parquet")
    df.to_parquet(out_path, index=False)
    return df, out_path
