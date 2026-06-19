FROM python:3.11-slim

RUN apt-get update \
    && apt-get install -y --no-install-recommends wkhtmltopdf git gcc libffi-dev libssl-dev python3-dev build-essential \
    && rm -rf /var/lib/apt/lists/*

ENV PIPX_HOME=/opt/pipx
ENV PIPX_BIN_DIR=/usr/local/bin
ENV PATH="$PIPX_BIN_DIR:$PATH"

RUN python -m pip install --no-cache-dir --upgrade pip pipx \
    && pipx install git+https://github.com/sherlock-project/sherlock.git

WORKDIR /app
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

ENTRYPOINT ["python", "run_pipeline.py"]
