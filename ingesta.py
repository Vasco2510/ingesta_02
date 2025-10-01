import os
import boto3
import csv
from datetime import datetime
import pymysql.cursors

# --- CONFIGURACIÓN DE ENTORNO (Usando variables de entorno) ---
# Se recomienda encarecidamente usar variables de entorno para los secretos.
MYSQL_HOST = os.getenv('MYSQL_HOST', 'localhost')
MYSQL_USER = os.getenv('MYSQL_USER', 'usuario_db')
MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD', 'password_db')
MYSQL_DB = os.getenv('MYSQL_DB', 'nombre_de_tu_base')
MYSQL_TABLE = os.getenv('MYSQL_TABLE', 'nombre_de_tu_tabla')

# Detalles de S3
NOMBRE_BUCKET = "ingesta-escobar"
PREFIJO_S3 = "ingesta02-tarea"
NOMBRE_ARCHIVO_CSV = "data_mysql_" + datetime.now().strftime("%Y%m%d%H%M%S") + ".csv"
CLAVE_S3 = f"{PREFIJO_S3}/{NOMBRE_ARCHIVO_CSV}" # Ejemplo: ingesta02-tarea/data_mysql_20250930103000.csv

def main():
    try:
        print(f"Intentando conectar a MySQL en host: {MYSQL_HOST}...")
        
        connection = pymysql.connect(
            host=MYSQL_HOST,
            user=MYSQL_USER,
            password=MYSQL_PASSWORD,
            database=MYSQL_DB,
            cursorclass=pymysql.cursors.DictCursor # Permite obtener los resultados como diccionarios
        )
        print("Conexión a MySQL exitosa.")

        with connection.cursor() as cursor:
            sql = f"SELECT * FROM {MYSQL_TABLE}"
            cursor.execute(sql)
            results = cursor.fetchall()
            connection.close() # Cierra la conexión inmediatamente después de leer

            if not results:
                print("No se encontraron registros en la tabla. Finalizando.")
                return

            # Obtener nombres de las columnas para el encabezado del CSV
            column_names = list(results[0].keys())
            
            # 2. GUARDAR EN ARCHIVO CSV LOCAL
            print(f"Escribiendo {len(results)} registros a {NOMBRE_ARCHIVO_CSV}")
            with open(NOMBRE_ARCHIVO_CSV, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=column_names)
                writer.writeheader()
                writer.writerows(results)
            print("Datos guardados en CSV localmente.")

            # 3. SUBIR EL CSV A S3
            print(f"Subiendo {NOMBRE_ARCHIVO_CSV} a s3://{NOMBRE_BUCKET}/{CLAVE_S3}")
            s3 = boto3.client('s3')
            s3.upload_file(NOMBRE_ARCHIVO_CSV, NOMBRE_BUCKET, CLAVE_S3)
            
            print("===================================")
            print("Ingesta completada exitosamente.")
            print(f"Archivo subido a: s3://{NOMBRE_BUCKET}/{CLAVE_S3}")
            print("===================================")

    except Exception as e:
        print(f"Ocurrió un error: {e}")
        
if __name__ == "__main__":
    main()