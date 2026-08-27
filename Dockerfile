FROM python:3.13-slim

WORKDIR /app

RUN groupadd --system appgroup && useradd --system --gid appgroup appuser

COPY --chown=appuser:appgroup requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY --chown=appuser:appgroup app.py redis_store.py .

EXPOSE 8000

USER appuser

CMD ["python", "app.py"]