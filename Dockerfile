FROM python:3.12-slim

WORKDIR /app

COPY pyproject.toml .
COPY .env.example .
COPY .gitignore .
COPY README.md .
COPY docs/ ./docs/
COPY server/ ./server/

RUN pip install uv && \
    uv pip install -e .[dev] && \
    rm -rf /root/.cache

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=3s \
  CMD curl -f http://localhost:8000/api/v1/health || exit 1

CMD ["uvicorn", "server.main:app", "--host", "0.0.0.0", "--port", "8000"]
