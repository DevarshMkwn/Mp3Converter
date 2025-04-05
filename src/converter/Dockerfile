FROM python:3.9-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
  build-essential \
  gcc \
  default-libmysqlclient-dev \
  pkg-config \
  ffmpeg \
  && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY ./requirements.txt /app
RUN python -m pip install --upgrade pip && \
    pip install --no-cache-dir --requirement /app/requirements.txt

COPY . /app

CMD ["python3", "consumer.py"]