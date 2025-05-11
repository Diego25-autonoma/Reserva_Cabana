#!/usr/bin/env bash
# Instalar dependencias necesarias para pyodbc
apt-get update && apt-get install -y \
    unixodbc \
    unixodbc-dev \
    libssl-dev \
    libffi-dev \
    libpq-dev \
    gcc \
    g++ \
    curl \
    make

# Instalar ODBC Driver para SQL Server
curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add -
curl https://packages.microsoft.com/config/ubuntu/20.04/prod.list > /etc/apt/sources.list.d/mssql-release.list
apt-get update
ACCEPT_EULA=Y apt-get install -y msodbcsql18 mssql-tools
echo 'export PATH="$PATH:/opt/mssql-tools/bin"' >> ~/.bashrc
source ~/.bashrc

