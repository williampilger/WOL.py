FROM python:3.11-slim

# Instalar dependências do sistema
RUN apt-get update && apt-get install -y \
    nmap \
    iputils-ping \
    net-tools \
    && rm -rf /var/lib/apt/lists/*

# Definir diretório de trabalho
WORKDIR /app

# Copiar requirements primeiro para cache do Docker
COPY requirements.txt .

# Instalar dependências Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código da aplicação
COPY . .

# Criar diretório para banco de dados
RUN mkdir -p /app/data

# Expor porta
EXPOSE 5000

# Variáveis de ambiente
ENV FLASK_APP=run.py
ENV FLASK_ENV=production
ENV DATABASE_PATH=/app/data/wol_system.db

# Comando para iniciar a aplicação
CMD ["python", "run.py"]
