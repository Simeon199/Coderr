FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt gunicorn

COPY . .

RUN python manage.py collectstatic --noinput || true

EXPOSE 8080

CMD python manage.py migrate --noinput && gunicorn core.wsgi:application --bind 0.0.0.0:8080 --workers 2