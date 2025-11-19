FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY tpa_turbo_forward_bot.py .

ENV PYTHONUNBUFFERED=True

RUN mkdir -p /app/logs

CMD ["python", "tpa_turbo_forward_bot.py"]
