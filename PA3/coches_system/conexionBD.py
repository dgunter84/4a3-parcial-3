import mysql.connector

conexion = None
cursor = None

try:
    conexion = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="",
        database="bd_coches",
    )
    cursor = conexion.cursor(buffered=True)
except mysql.connector.Error as error:
    print(f"No es posible conectarse a la base de datos: {error}")