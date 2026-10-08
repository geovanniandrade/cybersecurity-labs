FROM python:3.12-slim
LABEL org.opencontainers.image.source="https://github.com/geovanniandrade/cybersecurity-labs"
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 DATABASE_PATH=/app/data/ativos.sqlite3
WORKDIR /app
COPY requirements.lock .
RUN pip install --no-cache-dir -r requirements.lock \
    && groupadd --gid 10001 appuser \
    && useradd --uid 10001 --gid appuser --no-create-home appuser \
    && mkdir -p /app/data \
    && chown appuser:appuser /app/data
COPY --chown=appuser:appuser app.py ./
COPY --chown=appuser:appuser templates ./templates
COPY --chown=appuser:appuser static ./static
USER appuser
EXPOSE 8080
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8080/health', timeout=3)"
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "--workers", "1", "--threads", "4", "--access-logfile", "-", "--error-logfile", "-", "app:create_app()"]
