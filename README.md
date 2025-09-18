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

### Запуск скрипта загрузки данных

Для выполнения основного скрипта загрузки данных:

```bash
python data_loader.py
```

Данный скрипт выполняет следующее:
- Загружает данные из датасета на Google Drive
- Загружает данные с помощью pandas
- Отображает первые 10 строк датасета

### Структура проекта

```
Data-management-Engineering/
├── data_loader.py          # Основной скрипт для загрузки и отображения данных
├── requirements.txt        # Зависимости Python
└── README.md              # Документация проекта
```

## Пример вывода скрипта

**Домашнее задание №2**: <img width="1150" height="291" alt="image" src="https://github.com/user-attachments/assets/3fc164d9-4047-4271-bb18-cee4129a2038" />

## Зависимости

Проект использует следующие пакеты Python:
- `pandas` - Обработка и анализ данных
- `requests` - HTTP-библиотека для выполнения запросов
- `numpy` - Библиотека для численных вычислений

Все зависимости перечислены в `requirements.txt` и будут установлены автоматически при следовании инструкциям по настройке выше.
