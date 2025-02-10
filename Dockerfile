# Use a imagem oficial do Python 3.10 como imagem base
FROM python:3.10-slim

# Defina o diretório de trabalho no container para /app
WORKDIR /app

# Copie o conteúdo do diretório atual para o diretório de trabalho no container
COPY . /app

# Instale os pacotes necessários do arquivo requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Instale o driver ODBC da Microsoft para SQL Server
RUN apt-get update \
    && apt-get install -y curl gnupg2 unixodbc-dev \
    && curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - \
    && curl https://packages.microsoft.com/config/debian/10/prod.list > /etc/apt/sources.list.d/mssql-release.list \
    && apt-get update \
    && ACCEPT_EULA=Y apt-get install -y msodbcsql17 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

