FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN touch Inference/__init__.py

CMD ["uvicorn", "Inference.main:app", "--host", "0.0.0.0", "--port", "3000"]