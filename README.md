# Data-management-Engineering

Репозиторий для проекта **"Инжиниринг управления данными ИТМО"**.

## Ссылки на датасеты

**Ссылка на датасеты**: [Папка на Google Drive](https://drive.google.com/drive/folders/1QAz7jx7AGHJcXc0OftuolaaU4slls4CO?usp=sharing)  

**Исходный источник датасета**: [RCSB PDB Macromolecular Structure Dataset на Kaggle](https://www.kaggle.com/datasets/samiraalipour/rcsb-pdb-macromolecular-structure-dataset?utm_source=chatgpt.com&select=RCSB_PDB_Macromolecular_Structure_Dataset.csv)

## Настройка проекта

### Предварительные требования
- Python 3.7 или выше
- pip (установщик пакетов Python)

### Настройка виртуального окружения

1. **Клонировать репозиторий:**
   ```bash
   git clone https://github.com/Julik-228/Data-management-Engineering.git
   cd Data-management-Engineering
   ```

2. **Создать виртуальное окружение:**
   ```bash
   python -m venv venv
   ```

3. **Активировать виртуальное окружение:**
   
   **На Windows:**
   ```bash
   venv\Scripts\activate
   ```
   
   **На macOS/Linux:**
   ```bash
   source venv/bin/activate
   ```

4. **Установить необходимые зависимости:**
   ```bash
   pip install -r requirements.txt
   ```

### Запуск скриптов

#### Загрузка данных

Для выполнения скрипта загрузки данных:

```bash
python data_loader.py
```

Данный скрипт выполняет следующее:
- Загружает данные из датасета на Google Drive
- Загружает данные с помощью pandas
- Отображает первые 10 строк датасета

#### Обработка данных

Для выполнения скрипта обработки данных:

```bash
python data_processing.py
```

Данный скрипт выполняет следующее:
- Импортирует данные из `data_loader.py`
- Анализирует структуру данных и пропущенные значения
- Автоматически определяет и преобразует типы данных:
  - Преобразует строки в числовые значения (с заменой запятых на точки)
  - Обрабатывает даты в столбцах 'Deposition Date' и 'Release Date'
  - Конвертирует столбцы с низкой кардинальностью в категориальные типы
- Сохраняет обработанные данные в формате Parquet (`rcsb_dataset.parquet`)

### Структура проекта

```
Data-management-Engineering/
├── data_loader.py          # Скрипт для загрузки и отображения данных
├── data_processing.py      # Скрипт для обработки и преобразования данных
├── requirements.txt        # Зависимости Python
├── rcsb_dataset.parquet   # Обработанные данные в формате Parquet (создается после выполнения data_processing.py)
└── README.md              # Документация проекта
```

## Пример вывода скрипта

**Домашнее задание №2**: <img width="1150" height="291" alt="image" src="https://github.com/user-attachments/assets/3fc164d9-4047-4271-bb18-cee4129a2038" />

## Зависимости

Проект использует следующие пакеты Python:
- `pandas` - Обработка и анализ данных
- `requests` - HTTP-библиотека для выполнения запросов
- `numpy` - Библиотека для численных вычислений
- `fastparquet` - Библиотека для работы с файлами формата Parquet

Все зависимости перечислены в `requirements.txt` и будут установлены автоматически при следовании инструкциям по настройке выше.
