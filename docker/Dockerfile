FROM python:3.12.7-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY src/ /app/src

ENV PYTHONUNBUFFERED=1

EXPOSE 5000

CMD ["python", "src/api/app.py"]