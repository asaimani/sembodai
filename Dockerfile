FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN SECRET_KEY=dummy DB_HOST=localhost python manage.py collectstatic --noinput

EXPOSE 8080

CMD python manage.py migrate && python manage.py load_initial_data && gunicorn sembodai.wsgi:application --bind 0.0.0.0:$PORT