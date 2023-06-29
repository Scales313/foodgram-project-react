FROM python:3.9

WORKDIR /app

ENV PYTHONUNBUFFERED 1

RUN pip install --no-cache-dir gunicorn==20.1.0

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

RUN mkdir -p /backend_static/static/

COPY . .

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "kittygram_backend.wsgi"]