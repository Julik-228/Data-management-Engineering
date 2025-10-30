"""extract: загрузка и базовая валидация исходных данных"""

from __future__ import annotations

import os
from io import StringIO

import pandas as pd
import requests


def download_csv_from_google(file_id: str) -> pd.DataFrame:
    """Скачать CSV-файл с Google Drive по file_id и вернуть DataFrame.

    Raises requests.HTTPError при ошибке сети/запроса.
    """
    file_url = f"https://drive.google.com/uc?export=download&id={file_id}"
    resp = requests.get(file_url)
    resp.raise_for_status()
    return pd.read_csv(StringIO(resp.text))


def save_raw_csv(df: pd.DataFrame, *, out_path: str = "data/raw/raw.csv") -> str:
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    df.to_csv(out_path, index=False)
    return out_path


def validate_raw(df: pd.DataFrame) -> tuple[bool, str]:
    """Простейшая валидация: не пустой, есть столбцы.

    Возвращает (is_valid, message).
    """
    if df is None:
        return False, "DataFrame is None"
    if not isinstance(df, pd.DataFrame):
        return False, "Object is not a pandas DataFrame"
    if df.empty:
        return False, "DataFrame is empty"
    if df.shape[1] == 0:
        return False, "No columns in DataFrame"
    return True, "OK"


def load_source(file_id: str | None = None, url: str | None = None) -> tuple[pd.DataFrame, str]:
    """Загрузить источник. Принимает либо file_id (Google Drive), либо прямой url.

    Возвращает (df, saved_csv_path).
    """
    if file_id is None and url is None:
        raise ValueError("Either file_id or url must be provided")

    if file_id:
        df = download_csv_from_google(file_id)
    else:
        resp = requests.get(url)
        resp.raise_for_status()
        df = pd.read_csv(StringIO(resp.text))

    valid, msg = validate_raw(df)
    if not valid:
        raise ValueError(f"Validation failed for raw data: {msg}")

    saved = save_raw_csv(df)
    return df, saved
