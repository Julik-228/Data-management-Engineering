import sqlite3
import pandas as pd
from sqlalchemy import create_engine, text

conn = sqlite3.connect("src/creds.db")
cur = conn.cursor()

# список всех таблиц
cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
print('Таблицы в creds.db:', cur.fetchall())

# структура таблицы access
print('\nОписание таблицы access:')
cur.execute('PRAGMA table_info(access);')
for col in cur.fetchall():
    print(col)

# учетка в access
cur.execute('SELECT url, port, user, pass FROM access LIMIT 1;')
row = cur.fetchone()
conn.close()

url, port, user, password = row
dbname = 'homeworks' 

print('\nУчетные данные успешно считаны:')
print(f'url = {url}')
print(f'port = {port}')
print(f'dbname = {dbname}')
print(f'user = {user}')

# postgreesql 
print('\nПодключение к PostgreSQL')
conn_str = f'postgresql+psycopg2://{user}:{password}@{url}:{port}/{dbname}'
engine = create_engine(conn_str)
print('Подключение к PostgreSQL создано успешно')

# загрузка датасета

print('\nЗагрузка датасета rcsb_dataset.parquet')
df = pd.read_parquet('data/rcsb_dataset.parquet')
print(f'Датасет успешно загружен. Всего строк: {len(df)}, столбцов: {len(df.columns)}')

print('\nПервые 100 строк для загрузки')
df = df.head(100)
print(f'Подготовлено {len(df)} строк для записи в БД')

# запись данных в бд
table_name = 'zinnurova'
print(f'\nЗапись данных в таблицу "{table_name}" (схема public)')

df.to_sql(table_name, engine, schema="public", if_exists="replace", index=False)

print(f'Таблица "{table_name}" успешно записана ({len(df)} строк)')

# проверка записи

print('\nПроверка записи данных в таблицу')
with engine.connect() as conn:
    result = conn.execute(text(f'SELECT * FROM {table_name} LIMIT 3;'))
    rows = result.fetchall()

if rows:
    print(f'Таблица "{table_name}" существует. Пример строк:')
    for r in rows:
        print(r)
else:
    print('Таблица создана, но не удалось прочитать данные')

print('\nСкрипт завершен без ошибок')









