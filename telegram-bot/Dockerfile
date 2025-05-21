# Використовуємо офіційний Python образ
FROM python:3.9

# Встановлюємо залежності
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копіюємо код бота
COPY . /app
WORKDIR /app

# Запуск бота
CMD ["python", "bot.py"]

RUN pip install python-telegram-bot prometheus_client
