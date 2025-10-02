import boto3
import pymysql
import csv

# Configuración (debes cambiar estos valores)
config_mysql = {
    'host': 'sql_container',      # Ej: 'localhost' o '192.168.1.100'
    'user': 'root',         # Ej: 'root'
    'password': 'mafer',    # Ej: 'mi_password'
    'database': 'startup',          # Ej: 'empresa'
    'port': 3306
}

def main():
    # 1. Conectar y extraer datos de MySQL
    conexion = pymysql.connect(**config_mysql)
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM clientes")  # Cambia 'clientes' por tu tabla
    datos = cursor.fetchall()
    
    # 2. Crear archivo CSV
    with open('data_export.csv', 'w', newline='') as archivo:
        writer = csv.writer(archivo)
        writer.writerows(datos)
    
    print(f"Datos exportados: {len(datos)} registros")
    
    # 3. Subir a S3 (tu código original)
    s3 = boto3.client('s3')
    s3.upload_file('data_export.csv', 'ingesta-escobar', 'ingesta/data_export.csv')
    
    print("Ingesta completada")
    conexion.close()

if __name__ == "__main__":
    main()