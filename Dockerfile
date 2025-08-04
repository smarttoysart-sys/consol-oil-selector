# Используем официальный образ Python
FROM python:3.10-slim

# Установка зависимостей системы
RUN apt-get update && apt-get install -y build-essential libpq-dev curl && rm -rf /var/lib/apt/lists/*

# Установка рабочей директории
WORKDIR /app

# Копирование файлов проекта
COPY . .

# Установка зависимостей Python
RUN pip install --no-cache-dir -r requirements.txt

# Указание порта
EXPOSE 8000

# Запуск приложения
CMD ["uvicorn", "ai_oil_selector:app", "--host", "0.0.0.0", "--port", "8000"]