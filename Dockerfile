FROM python:3.13-slim

# Define diretório de trabalho
WORKDIR /app

# Copia o arquivo de dependências
COPY app/requirements.txt .

# Instala as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copia o restante da aplicação
COPY app/ .

# Comando para iniciar a API com uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
