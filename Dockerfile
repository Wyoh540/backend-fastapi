FROM python:3.10-slim-bullseye

ENV PYTHONUNBUFFERED=1

WORKDIR /app/

EXPOSE 80

# Install uv
# Ref: https://docs.astral.sh/uv/guides/integration/docker/#installing-uv
COPY --from=ghcr.io/astral-sh/uv:0.5.11 /uv /uvx /bin/

# Place executables in the environment at the front of the path
# Ref: https://docs.astral.sh/uv/guides/integration/docker/#using-the-environment
ENV PATH="/app/.venv/bin:$PATH"

ENV PYTHONPATH=/app

# Copy the application into the container.
COPY ./app /app/app
COPY ./pyproject.toml ./uv.lock ./alembic.ini ./scripts ./static /app/

# Install the application dependencies.
RUN uv sync --frozen --no-cache


CMD ["fastapi", "run", "--workers", "4", "app/main.py", "--port", "80", "--host", "0.0.0.0"]