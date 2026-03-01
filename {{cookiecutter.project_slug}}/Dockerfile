FROM python:3.12-slim

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

ENV PYTHONUNBUFFERED=1
ENV WORKDIR=/app

WORKDIR $WORKDIR

# Copy dependency files
COPY pyproject.toml .

# Install dependencies directly into the system environment
RUN uv pip install --system -e .

# Copy application code
COPY src/ ./src/

# Expose FastAPI port
EXPOSE 8000

CMD ["gunicorn", "src.backend.main:app", "-w", "4", "-k", "uvicorn.workers.UvicornWorker", "-b", "0.0.0.0:8000"]