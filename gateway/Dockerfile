FROM python:3.11-slim AS base
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY ../common /app/common
COPY main.py /app/
EXPOSE 8080
HEALTHCHECK CMD curl -fsS http://localhost:8080/health || exit 1
USER 1000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
