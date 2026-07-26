FROM python:3.14-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY deprecation_auditor/ ./deprecation_auditor/

# python -m deprecation_auditor.cli needs to find the deprecation_auditor
# package regardless of the container's working directory -- GitHub Actions
# overrides CWD to /github/workspace (the checked-out target repo) at
# runtime, not /app, so this can't rely on CWD alone. /app is only the
# WORKDIR (a filesystem path), not part of the actual Python package name.
ENV PYTHONPATH=/app

ENTRYPOINT ["python", "-m", "deprecation_auditor.cli"]