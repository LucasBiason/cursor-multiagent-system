# ============================================
# Dockerfile Multi-Stage para Django
# ============================================
# 
# Este Dockerfile segue as melhores práticas de multi-stage builds.
# Para detalhes completos sobre Dockerfiles, consulte:
# - Dockerfile Generator Skill: skills/infrastructure/dockerfile-generator/SKILL.md
# - Dockerfile Guide: core/templates/django/DOCKERFILE_GUIDE.md
#
# Características:
# - Multi-stage build (builder, test, runtime)
# - Otimização de cache (dependências antes do código)
# - Usuário não-root (appuser)
# - Healthcheck configurado
# - Suporte a Poetry e pip/requirements.txt
#
# ============================================
# Stage 1: Builder (instala dependências e roda testes)
# ============================================
FROM python:3.11-slim AS builder

ARG POETRY_VERSION=1.5.1
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_NO_INTERACTION=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

# Instalar dependências de build
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    g++ \
    libpq-dev \
    python3-dev \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copiar arquivos de dependências primeiro (cache layer)
# Suporte a Poetry e requirements.txt
COPY pyproject.toml poetry.lock* requirements.txt* ./

# Instalar dependências
# Prioridade: Poetry > requirements.txt
RUN if [ -f pyproject.toml ]; then \
        pip install --upgrade pip && \
        pip install "poetry==$POETRY_VERSION" && \
        poetry install --no-dev --no-interaction --no-ansi && \
        rm -rf "$POETRY_CACHE_DIR"; \
    elif [ -f requirements.txt ]; then \
        pip install --upgrade pip && \
        pip install --no-cache-dir -r requirements.txt; \
    else \
        echo "ERROR: Neither pyproject.toml nor requirements.txt found" && exit 1; \
    fi

# Copiar código da aplicação
COPY . /app

# Rodar testes (falha cedo se testes quebrarem)
# Comentar se não quiser rodar testes no build
# RUN pytest --cov=app --cov-report=term-missing --cov-fail-under=90 -v || exit 1

# Coletar arquivos estáticos (Django)
RUN python manage.py collectstatic --no-input || echo "⚠️  collectstatic skipped (manage.py not found or not configured)"

# ============================================
# Stage 2: Test (opcional - para rodar testes isoladamente)
# ============================================
FROM builder AS test

# Instalar dependências de desenvolvimento para testes
RUN if [ -f pyproject.toml ]; then \
        poetry install --no-interaction --no-ansi; \
    elif [ -f requirements-dev.txt ]; then \
        pip install --no-cache-dir -r requirements-dev.txt; \
    fi

# Rodar testes
CMD ["pytest", "--cov=app", "--cov-report=term-missing", "--cov-report=html", "-v"]

# ============================================
# Stage 3: Runtime (imagem final minimalista)
# ============================================
FROM python:3.11-slim AS runtime

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PATH="/usr/local/bin:$PATH"

# Instalar apenas dependências de runtime (sem build tools)
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Criar usuário não-root
RUN useradd --create-home --shell /bin/bash appuser

WORKDIR /app

# Copiar dependências instaladas do builder
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copiar código da aplicação
COPY --from=builder /app /app

# Copiar entrypoint
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Ajustar permissões (não rodar como root)
RUN chown -R appuser:appuser /app && \
    chmod -R 755 /app

USER appuser

# Labels OCI para metadata
LABEL org.opencontainers.image.title="Django Application" \
      org.opencontainers.image.description="Django application with multi-stage build" \
      org.opencontainers.image.vendor="Cursor Multiagent System" \
      org.opencontainers.image.authors="Cursor Multiagent System"

EXPOSE 8000

# Healthcheck
HEALTHCHECK --interval=30s --timeout=3s --start-period=10s --retries=3 \
    CMD curl -f http://127.0.0.1:8000/health/ || exit 1

# Entrypoint e CMD padrão
ENTRYPOINT ["/entrypoint.sh"]
CMD ["prod"]

