FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
	PYTHONUNBUFFERED=1 \
	PIP_NO_CACHE_DIR=1 \
	HF_HOME=/opt/huggingface

WORKDIR /app

# Git is required by some dependency installation paths.
RUN apt-get update \
	&& apt-get install -y --no-install-recommends git \
	&& rm -rf /var/lib/apt/lists/*

# Install dependencies before copying application code to preserve Docker cache layers.
COPY requirements.txt ./
RUN python -m pip install --upgrade pip \
	&& python -m pip install -r requirements.txt

# Download the embedding model while building the image so startup does not depend on network access.
RUN python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('all-MiniLM-L6-v2')" \
	&& chmod -R a+rX /opt/huggingface

COPY . ./

RUN useradd --create-home --uid 10001 appuser \
	&& chown -R appuser:appuser /app

USER appuser

EXPOSE 8080

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]