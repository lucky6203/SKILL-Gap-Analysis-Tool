FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY ../../common /app/common
COPY app.py /app/
EXPOSE 8002
HEALTHCHECK CMD curl -fsS http://localhost:8002/health || exit 1
USER 1000
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8002"]
