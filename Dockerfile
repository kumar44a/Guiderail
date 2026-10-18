# GuideRail: API and UI image. The index is built at image build time from the synthetic corpus,
# so the container needs no network and no API key to answer questions (extractive generator).
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 PIP_NO_CACHE_DIR=1
WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY pyproject.toml ./
COPY src ./src
COPY scripts ./scripts
COPY prompts ./prompts
COPY ui ./ui
COPY data/guidelines ./data/guidelines

# Fails the build if two independent index builds are not byte-identical.
RUN python scripts/pipeline.py --check-determinism

RUN useradd --create-home --uid 10001 guiderail && chown -R guiderail /app
USER guiderail

ENV GUIDERAIL_INDEX_DIR=/app/index PYTHONPATH=/app/src
EXPOSE 9070 8501

HEALTHCHECK --interval=15s --timeout=3s --start-period=20s --retries=3 \
  CMD python -c "import urllib.request,sys; sys.exit(0 if urllib.request.urlopen('http://localhost:9070/health', timeout=2).status == 200 else 1)"

CMD ["uvicorn", "guiderail.api:app", "--host", "0.0.0.0", "--port", "9070"]
