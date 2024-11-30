FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

EXPOSE 8501

# No need to COPY source files since we're using volumes