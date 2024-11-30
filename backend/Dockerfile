FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt
RUN pip install debugpy
# No need to COPY source files since we're using volumes

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"] 