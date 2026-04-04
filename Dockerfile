FROM ghcr.io/astral-sh/uv:python3.12-trixie-slim AS builder

ENV PYTHONDONTWRITEBYTECODE=1 \
	PYTHONUNBUFFERED=1 \
	UV_COMPILE_BYTECODE=1 \
	UV_LINK_MODE=copy

WORKDIR /app

COPY pyproject.toml uv.lock ./
RUN uv sync --locked --no-install-project

COPY . .
RUN uv sync --locked

FROM ghcr.io/astral-sh/uv:python3.12-trixie-slim AS runtime

ENV PYTHONDONTWRITEBYTECODE=1 \
	PYTHONUNBUFFERED=1 \
	PATH="/app/.venv/bin:$PATH"

WORKDIR /app

RUN apt-get update \
	&& apt-get install -y --no-install-recommends libpq5 \
	&& rm -rf /var/lib/apt/lists/* \
	&& useradd --create-home --shell /bin/bash appuser

COPY --from=builder --chown=appuser:appuser /app /app

USER appuser

EXPOSE 8007

CMD ["python", "-m", "src.main"]
