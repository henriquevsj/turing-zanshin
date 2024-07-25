# Usar uma imagem base do Python
FROM python:3.11

# Instalar dependências do sistema
RUN apt-get update && apt-get install -y cron

# Instalar PyArmor versão 8
RUN pip install pyarmor

# Definir o diretório de trabalho dentro do container
WORKDIR /app

# Copiar os arquivos de requisitos para o diretório de trabalho
COPY requirements.txt .

# Instalar as dependências da aplicação
RUN pip install --no-cache-dir -r requirements.txt

# Copiar o código-fonte da aplicação para o contêiner
COPY sonarqubeclass.py .
COPY common ./common

# Ofuscar os arquivos Python usando PyArmor 8
RUN pyarmor gen -O . sonarqubeclass.py common

# Definir a porta em que a aplicação irá rodar
EXPOSE 7070

# Definir variáveis de ambiente
ENV MONGO_USER_NAME visualcode
ENV MONGO_PASSWORD cpNjHzz5Wn1CJ0pr
ENV MONGO_URL cluster01.it0lbcv.mongodb.net
ENV MONGO_DB_NAME doconnect_db
ENV MONGO_CLUSTER_NAME Cluster01
ENV LICENSE_SERVICE_VERIFY_URL https://license-service-development.azurewebsites.net/api/verify-token
ENV LICENSE_SERVICE_LOGIN_URL https://license-service-development.azurewebsites.net/api/login
ENV LICENSE_SERVICE_USERNAME henrique
ENV LICENSE_SERVICE_PASSWORD dcrrwmp3

# Copiar o crontab
COPY crontab /etc/cron.d/sonarqube-cron

# Dar permissão para o arquivo crontab
RUN chmod 0644 /etc/cron.d/sonarqube-cron

# Aplicar o crontab
RUN crontab /etc/cron.d/sonarqube-cron

# Criar o arquivo de log do cron
RUN touch /var/log/cron.log

# Comando para rodar o cron e o serviço
CMD ["sh", "-c", "cron && tail -f /var/log/cron.log"]
