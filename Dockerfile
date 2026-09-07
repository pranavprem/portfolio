# Multi-architecture index verified through Docker Hub's tag API on 2026-09-06.
FROM python:3.13.15-slim-bookworm@sha256:ed86c82274b3c69b52fb5820f358f0bd7df0b603332063cb5c6e32bd220c3e6e

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PORTFOLIO_ENV=production \
    PORTFOLIO_HSTS=0

WORKDIR /srv/portfolio
COPY --chown=0:0 --chmod=0444 requirements.txt ./requirements.txt
RUN python -m pip install --no-cache-dir --require-hashes --only-binary=:all: -r requirements.txt
COPY --chown=0:0 app/ ./app/
RUN chmod -R a=rX app

USER 10001:10001
RUN python -c "from app import create_app; create_app()"
EXPOSE 8000

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "2", "--worker-class", "sync", "--timeout", "30", "--graceful-timeout", "20", "--worker-tmp-dir", "/tmp", "--limit-request-line", "2048", "--limit-request-fields", "32", "--limit-request-field_size", "4096", "--forwarded-allow-ips", "", "--forwarder-headers", "", "--no-control-socket", "--logger-class", "app.SafeGunicornLogger", "--error-logfile", "-", "--log-level", "error", "app:create_app()"]
