import pandas as pd
import requests
from io import StringIO

from data_loader import raw_data, file_url


response = requests.get(file_url)
raw_data = pd.read_csv(StringIO(response.text))
# print(raw_data.head(10))

df = raw_data.copy()

print(df.info())
print(df.isna().sum().sort_values(ascending=False).head(10))

df = df.convert_dtypes()

for col in df.columns:
    if df[col].dtype == 'string' or df[col].dtype == object:
        s = df[col].astype('string').str.strip()

        s_num = pd.to_numeric(s.str.replace(',', '.', regex=False), errors='coerce')
        if s_num.notna().sum() / len(s) >= 0.9: 
            df[col] = s_num
            continue

        date_columns = ['Deposition Date', 'Release Date']  
        if col in date_columns:
            s_dt = pd.to_datetime(s, errors='coerce', format='%Y-%m-%d')  
            if s_dt.notna().sum() / len(s) >= 0.9:
                df[col] = s_dt
                continue

        if df[col].nunique(dropna=True) / len(df) < 0.5:
            df[col] = s.astype('category')
        else:
            df[col] = s  

print(df.dtypes)


df.to_parquet("rcsb_dataset.parquet", index=False)
print('Сохранено в rcsb_dataset.parquet')
