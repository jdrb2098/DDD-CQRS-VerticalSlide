FROM python:3.12

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Instalar dependencias del sistema y PostgreSQL client
RUN apt-get update && apt-get install -y \
    postgresql-client \
    curl \
    unzip \
    && rm -rf /var/lib/apt/lists/*

# Instalar pip requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Instalar AWS CLI v2
RUN curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip" \
    && unzip awscliv2.zip \
    && ./aws/install \
    && rm -rf awscliv2.zip aws

WORKDIR /app
COPY . /app

EXPOSE 8000
EXPOSE 5678

CMD ["uvicorn", "asisya_api.main:app", "--host", "0.0.0.0", "--port", "8000"]
