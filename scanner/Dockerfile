FROM python:3.14-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY deprecation_auditor/ ./deprecation_auditor/

ENV PYTHONPATH=/app

ENTRYPOINT ["python", "-m", "deprecation_auditor.cli"]