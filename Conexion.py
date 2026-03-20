import mysql.connector
from mysql.connector import Error
# --- Configuración (REEMPLAZA ESTOS VALORES) ---
HOST = "localhost"
USER = "root"
PASSWORD = "12345"
DATABASE = "Gimnasio" # Asegúrate de que esta DB exista
# -----------------------------------------------

def crear_conexion(host, user, password, db):
    """Establece la conexión a la base de datos."""
    conexion = None
    try:
        conexion = mysql.connector.connect(
            host=host,
            user=user,
            passwd=password,
            database=db
        )
        if conexion.is_connected():
            print("✅ Conexión a MySQL exitosa.")
    except Error as e:
        print(f"❌ Error al conectar: '{e}'")
    return conexion

# Llamamos a la función para establecer la conexión
conn = crear_conexion(HOST, USER, PASSWORD, DATABASE)

def ejecutar_comando(conexion, comando_sql, datos=None):
    """Ejecuta una sentencia SQL (INSERT, UPDATE, DELETE)."""
    cursor = conexion.cursor()
    try:
        if datos:
            # Usamos %s para pasar los datos de forma segura (previene inyección SQL)
            cursor.execute(comando_sql, datos)
        else:
            cursor.execute(comando_sql)

        conexion.commit() # Guarda los cambios
        print(f"✨ Comando ejecutado con éxito. Filas afectadas: {cursor.rowcount}")
    except Error as e:
        print(f"❌ Error al ejecutar el comando: '{e}'")
    finally:
        cursor.close()

def ejecutar_comando(conexion, comando_sql, datos=None):
    """Ejecuta una sentencia SQL (INSERT, UPDATE, DELETE)."""
    cursor = conexion.cursor()
    try:
        if datos:
            # Usamos %s para pasar los datos de forma segura (previene inyección SQL)
            cursor.execute(comando_sql, datos)
        else:
            cursor.execute(comando_sql)

        conexion.commit() # Guarda los cambios
        print(f"✨ Comando ejecutado con éxito. Filas afectadas: {cursor.rowcount}")
    except Error as e:
        print(f"❌ Error al ejecutar el comando: '{e}'")
    finally:
        cursor.close()
 
print("--- 1. CREAR (INSERTAR) REGISTROS ---")

# Comando SQL para insertar maquina
insert_sql = "INSERT INTO maquinas (CodigoMaq, Nombre, Categoria) VALUES (%s, %s, %s)"
# Datos del primera maquina (tupla)
maquina_1 = (4, "Sentadilla jacka", "Pierna")
#ejecutar_comando(conn, insert_sql, maquina_1)

# Comando SQL para insertar distribuidor
insert_sqlDistri = "INSERT INTO distribuidor (ID_Distribuidor, Nombre, Apellido, Telefono, Categoria) VALUES (%s, %s, %s, %s, %s)"
# Datos del primer distribuidor (tupla)
distribuidor_1 = (4, "Sebastian", "Gil", "3132802339", "Bebidas")
ejecutar_comando(conn, insert_sqlDistri, distribuidor_1)

# Comando SQL para insertar inventario
insert_sql = "INSERT INTO inventario (CodigoInv, Producto, Categoria, Stock, Precio) VALUES (%s, %s, %s, %s, %s)"
# Datos del primer objeto en el inventario (tupla)
ObjetoInventario_1 = (4, "Sobre de creatina", "Suplementos", 12, 15000)
#ejecutar_comando(conn, insert_sql, ObjetoInventario_1)

# Comando SQL para insertar membresia
insert_sql = "INSERT INTO membresia (ID_Membresia, Plan, Costo, Duracion_meses) VALUES (%s, %s, %s, %s)"
# Datos del primera membresia (tupla)
membresia_1 = (4, "2 Meses", 30, 2)
#ejecutar_comando(conn, insert_sql, membresia_1)

# Comando SQL para insertar personal
insert_sqlPersonal = "INSERT INTO personal (ID_Personal, Nombre, Apellido, Rol, Salario, Fecha_Contratacion) VALUES (%s, %s, %s, %s, %s, %s)"
# Datos del primer personal (tupla)
personal_1 = (4, "Diego", "Vivas", "Entrenador", 2500, "2022-10-21")
ejecutar_comando(conn, insert_sqlPersonal, personal_1)

# Comando SQL para insertar usuario
insert_sqlUsuario = "INSERT INTO usuario (ID_Usuario, Nombre, Apellido, Telefono, Direccion, Edad, Seguro, Fecha_Registro) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
# Datos del primer usuario (tupla)
usuario_1 = (4, "Juan", "Gutierrez", "3184220536", "Calle 8 #32-11Sur", 20, "Sura", "2023-11-18")
ejecutar_comando(conn, insert_sqlUsuario, usuario_1)