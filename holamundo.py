import mysql.connector
from mysql.connector import errorcode

# Configuración de la conexión al servidor MySQL
host = "127.0.0.1"
user = "root"
password = "Belladonna"
database = "qa_testing"

try:
    # Conectar al servidor MySQL
    connection = mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database=database
    )
    cursor = connection.cursor()

    # Insertar un nuevo registro en la tabla 'test_runs'
    script_name = "cancelar_hora"
    cursor.execute("""
        INSERT INTO test_runs (script_name)
        VALUES (%s)
    """, (script_name,))

    # Confirmar los cambios
    connection.commit()

    print("Registro insertado en la tabla")

except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Error en el nombre de usuario o contraseña")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("La base de datos no existe")
    else:
        print(err)
finally:
    if connection.is_connected():
        cursor.close()
        connection.close()
