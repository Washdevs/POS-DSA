#=================================================
# ARQUIVO: Dockerfile
#=================================================
# Imagem base
FROM python:3.12-slim

# Define o diretório de trabalho dentro do contêiner
WORKDIR /usr/src/app

# Copia e instala as dependências Python
COPY ./app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --upgrade streamlit crewai litellm

# Copia o restante dos arquivos da aplicação
COPY ./app .

# Expõe a porta do Streamlit
EXPOSE 8501

# Comando para iniciar a aplicação Streamlit
# Mesmo que escrever cada um no cmd um por vez
CMD ["streamlit", "run", "app.py", "--server.port=8505", "--server.address=0.0.0.0"]