# Описание проекта

## О проекте

Этот проект представляет собой пример использования API для работы с данными. В данном случае используется API [icanhazdadjoke](https://icanhazdadjoke.com/api), которое предоставляет доступ к огромной коллекции "папиных шуток" (dad jokes).

## Возможности

- Получение случайной шутки
- Поиск шуток по ключевым словам
- Получение шутки по её уникальному идентификатору
- Форматирование шуток в различных форматах (JSON, текст, HTML)

## Используемое API

### Основные эндпоинты:

1. **Случайная шутка**  
   `GET https://icanhazdadjoke.com/`  
   Возвращает случайную шутку. Можно указать заголовок `Accept` для выбора формата ответа:  
   - `application/json` — JSON
   - `text/plain` — текст

2. **Шутка по ID**  
   `GET https://icanhazdadjoke.com/j/<joke_id>`  
   Возвращает шутку с указанным идентификатором.

3. **Поиск шуток**  
   `GET https://icanhazdadjoke.com/search`  
   Позволяет искать шутки по ключевым словам. Поддерживает параметры:
   - `term` — поисковый запрос
   - `page` — номер страницы
   - `limit` — количество результатов на странице (максимум 30)

4. **Шутка в формате изображения**  
   `GET https://icanhazdadjoke.com/j/<joke_id>.png`  
   Возвращает изображение с шуткой.

## Установка и запуск

1. Убедитесь, что у вас установлен Python.
2. Установите зависимости:
   ```bash
   pip install -r requirements.txt
   ```
3. Запустите скрипт `api_reader.py` для работы с API.

## Структура проекта

- `api_reader.py` — основной скрипт для взаимодействия с API.
- `requirements.txt` — список зависимостей проекта.
- `README.md` — документация проекта.

## Пример использования

Пример запроса случайной шутки в формате JSON:
```bash
curl -H "Accept: application/json" https://icanhazdadjoke.com/
```

Пример ответа:
```json
{
  "id": "R7UfaahVfFd",
  "joke": "My dog used to chase people on a bike a lot. It got so bad I had to take his bike away.",
  "status": 200
}
```

Пример вывода программы:
<img width="1368" height="889" alt="image" src="https://github.com/user-attachments/assets/7c70cfc7-e4c3-4958-8ead-25bec082522e" />


## Благодарности

API предоставлено [icanhazdadjoke](https://icanhazdadjoke.com/api).
