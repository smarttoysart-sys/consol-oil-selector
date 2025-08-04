# ai_oil_selector.py

from fastapi import FastAPI, Request
from pydantic import BaseModel
import openai
import os
import pandas as pd
import re
import urllib.parse

app = FastAPI()

openai.api_key = os.getenv("OPENAI_API_KEY")

# Загрузка базы масел Consol при запуске
xls = pd.ExcelFile("CONSOL.xlsx")
oil_data = xls.parse("прайс февраль 2025")
oil_data = oil_data[oil_data["Класс SAE"].notna()]  # Удаление строк-заголовков

def find_matching_oils(gpt_text):
    # Поиск ключевых слов из ответа GPT
    sae_match = re.search(r"\bSAE\s?(\d{1,2}W-\d{1,2})\b", gpt_text)
    api_match = re.search(r"API\s([A-Z]{2,3})", gpt_text)
    acea_match = re.search(r"ACEA\s([A-Z0-9\-/]+)", gpt_text)

    sae = sae_match.group(1) if sae_match else None
    api = api_match.group(1) if api_match else None
    acea = acea_match.group(1) if acea_match else None

    # Фильтрация
    filtered = oil_data.copy()
    if sae:
        filtered = filtered[filtered['Класс SAE'] == sae]
    if api:
        filtered = filtered[filtered['Классиф.API'].str.contains(api, na=False)]
    if acea:
        filtered = filtered[filtered['Спецификации и соответствия'].str.contains(acea, na=False)]

    # Форматирование результатов
    if filtered.empty:
        return "\n\n❌ Подходящих масел Consol не найдено."

    result = "\n\n✅ Подходящие масла Consol:\n"
    for _, row in filtered.iterrows():
        name = row['Наименование']
        sae = row['Класс SAE']
        api = row['Классиф.API']
        article = int(row['Артикул']) if pd.notna(row['Артикул']) else 'n/a'
        volume = row['л./кг']
        query = urllib.parse.quote_plus(str(name))
        url = f"https://consol-oil.ru/search/?q={query}"
        result += f"- [{name}]({url}) ({sae}, API {api}) — артикул {article}, фасовка: {volume} л\n"
    return result

class VehicleData(BaseModel):
    brand: str
    model: str
    year: int
    engine: str
    mileage: int
    climate: str
    driving_style: str

SYSTEM_PROMPT = """ 
Ты — моторный эксперт.
На основе марки, модели, года выпуска, типа двигателя, пробега, климата и стиля вождения подбирай оптимальное моторное масло. 
Учитывай рекомендации SAE, API, ACEA, ILSAC. Не используй базы данных VIN. Работай как эксперт на основе логики, пробега и условий эксплуатации.
"""

@app.post("/recommend")
async def recommend_oil(data: VehicleData):
    user_prompt = f""" 
Марка: {data.brand}
Модель: {data.model}
Год: {data.year}
Двигатель: {data.engine}
Пробег: {data.mileage} км
Климат: {data.climate}
Стиль вождения: {data.driving_style}

Подбери подходящее моторное масло. Укажи:
- Вязкость (SAE)
- Спецификации (API, ACEA, ILSAC)
- Тип основы (минеральное, полусинтетика, синтетика)
- Интервал замены
- Аргументированную рекомендацию
"""

    completion = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt}
        ]
    )
    gpt_result = completion.choices[0].message["content"]
    matching_oils = find_matching_oils(gpt_result)
    full_response = gpt_result + matching_oils
    return {"recommendation": full_response}
