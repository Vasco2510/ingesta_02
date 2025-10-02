FROM python:3-slim
WORKDIR /programas/ingesta

# Instala las librerías necesarias: boto3 para S3 y pymysql para MySQL.
RUN pip3 install boto3 pymysql


# Copia los archivos de la aplicación.
COPY . .

# Comando para ejecutar el script de ingesta.
CMD [ "python3", "./ingesta.py" ]