import boto3
import pymysql
import csv

# Configuración de conexion
config_mysql = {
    'host': 'mysql_db2',      # Ej: 'localhost' o '192.168.1.100'
    'user': 'root',         # Ej: 'root'
    'password': 'mafer',    # Ej: 'mi_password'
    'database': 'startup',          # Ej: 'empresa'
    'port': 3306
}

def main():
    # 1. Conectar y extraer datos de MySQL
    conexion = pymysql.connect(**config_mysql)
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM clientes") 
    datos = cursor.fetchall()
    
    with open('data_export.csv', 'w', newline='') as archivo:
        writer = csv.writer(archivo)
        writer.writerows(datos)
    
    print(f"Datos exportados: {len(datos)} registros")
    
    s3 = boto3.client('s3')
    s3.upload_file('data_export.csv', 'ingesta-escobar', 'ingesta/data_export.csv')
    
    print("Ingesta completada")
    conexion.close()

if __name__ == "__main__":
    main()