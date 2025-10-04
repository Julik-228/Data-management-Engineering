import requests
import json
from datetime import datetime
import pandas as pd
from googletrans import Translator

# URL API для шуток
API_URL = "https://icanhazdadjoke.com/"
HEADERS = {"Accept": "application/json"}

def get_dad_jokes(num_jokes=10):
    """Запрашивает указанное (10) количество случайных dad jokes с API."""
    jokes = []
    for _ in range(num_jokes):
        try:
            response = requests.get(API_URL, headers=HEADERS, timeout=5)
            response.raise_for_status()
            data = response.json()
            joke = data.get("joke", "No joke found!")
            if joke not in jokes:
                jokes.append(joke)
        except (requests.exceptions.RequestException, json.JSONDecodeError) as e:
            jokes.append(f"Error fetching joke: {e}")
        if len(jokes) >= num_jokes:
            break
    return jokes

def translate_joke(joke):
    """Переводит шутку на русский через googletrans"""
    if not joke or "Error" in joke:
        return "Не удалось перевести шутку."
    try:
        translator = Translator()
        translation = translator.translate(joke, src="en", dest="ru")
        return translation.text
    except Exception as e:
        return f"Fallback translation failed: {e}. Original joke: {joke}"

def save_to_dataframe(jokes, translated_jokes):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    new_rows = [
        {"Timestamp": timestamp, "Original_Joke": joke, "Translated_Joke": translated_joke}
        for joke, translated_joke in zip(jokes, translated_jokes)
    ]
    new_df = pd.DataFrame(new_rows)

    try:
        df = pd.read_parquet("jokes.parquet")
    except FileNotFoundError:
        df = pd.DataFrame(columns=["Timestamp", "Original_Joke", "Translated_Joke"])

    df = pd.concat([df, new_df], ignore_index=True)

    df.to_parquet("jokes.parquet", index=False)
    print("Шутки и переводы сохранены в jokes.parquet")

    with open("jokes.txt", "a", encoding="utf-8") as f:
        for joke, translated_joke in zip(jokes, translated_jokes):
            f.write(f"[{timestamp}] Original: {joke}\n")
            f.write(f"[{timestamp}] Translated (RU): {translated_joke}\n")
    print("Шутки и переводы сохранены в jokes.txt")
    
    return df

def main():
    print("Генерирую 10 папиных шуток... 🙉🙈🙊")
    jokes = get_dad_jokes(num_jokes=10)
    
    print("\nШутки дня (оригинал):")
    for i, joke in enumerate(jokes, 1):
        print(f"{i}. {joke}")
    
    # Переводим все шутки
    translated_jokes = [translate_joke(joke) for joke in jokes]
    print("\nШутки дня (на русском):")
    for i, translated_joke in enumerate(translated_jokes, 1):
        print(f"{i}. {translated_joke}")
    print("\n")

    df = save_to_dataframe(jokes, translated_jokes)
    print("\nТекущий DataFrame:")
    print(df)

if __name__ == "__main__":
    main()