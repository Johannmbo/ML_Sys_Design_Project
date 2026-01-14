FROM python:3.10-slim

WORKDIR /app

# Устанавливаем curl для работы healthcheck из docker-compose
# RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt-cache/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем всё содержимое проекта в /app
COPY . .

# Создаем __init__.py внутри Inference, чтобы Python видел его как модуль
RUN touch Inference/__init__.py

# Запускаем на порту 3000 (как в вашем compose)
CMD ["uvicorn", "Inference.main:app", "--host", "0.0.0.0", "--port", "3000"]