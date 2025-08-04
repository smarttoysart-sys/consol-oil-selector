# AI-сервис подбора моторного масла Consol

Интеллектуальный сервис подбора моторных масел с использованием GPT-4 и логики, без баз данных Olyslager.

---

## 🚀 Быстрый старт

### Установка зависимостей

```bash
pip install -r requirements.txt
```

### Запуск локально

```bash
uvicorn ai_oil_selector:app --reload
```

Откройте `frontend.html` в браузере и подключитесь к `http://localhost:8000/recommend`.

---

## 🔐 Конфигурация

Создайте файл `.env` и добавьте ваш OpenAI API ключ:

```
OPENAI_API_KEY=sk-...
```

---

## 🐳 Docker

### Сборка и запуск

```bash
docker build -t ai-oil-selector .
docker run -d -p 8000:8000 --env OPENAI_API_KEY=sk-... ai-oil-selector
```

---

## 🌐 Деплой на Railway

1. Перейдите на [https://railway.app](https://railway.app)
2. Подключите репозиторий GitHub с этим проектом
3. Установите переменную `OPENAI_API_KEY`
4. Railway автоматически развернёт проект

---

## 🔗 Возможности

- Подбор масла по SAE/API/ACEA/DPF/климату
- Интеграция с GPT-4
- Автопоиск продуктов Consol с ссылками на сайт
- VIN-декодер (на базе NHTSA API)

---

## 📁 Структура

- `ai_oil_selector.py` — FastAPI backend
- `CONSOL.xlsx` — база масел Consol
- `frontend.html` — HTML-интерфейс
- `.env` — конфигурация
- `Dockerfile` — контейнеризация
- `requirements.txt` — зависимости

---

## ✉️ Обратная связь

Поддержка: [https://consol-oil.ru](https://consol-oil.ru)