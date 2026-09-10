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
