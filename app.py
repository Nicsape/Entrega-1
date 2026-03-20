from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)
app.secret_key = 'clave_secreta_gimnasio'

# Configuración de la base de datos
def get_db_connection():
    try:
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='12345',
            database='Gimnasio',
            auth_plugin='mysql_native_password'
        )
        return conn
    except Error as e:
        print(f"Error de conexión: {e}")
        return None

def init_database():
    """Inicializa la base de datos y crea las tablas si no existen"""
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            
            # Crear tabla Inventario si no existe
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS Inventario (
                    CodigoInv INT PRIMARY KEY,
                    Producto VARCHAR(50),
                    Categoria VARCHAR(50),
                    Stock INT,
                    Precio DECIMAL(10,2)
                )
            ''')
            
            # Verificar si hay datos en Inventario
            cursor.execute("SELECT COUNT(*) FROM Inventario")
            count = cursor.fetchone()[0]
            
            if count == 0:
                # Insertar datos de ejemplo
                sample_data = [
                    (1, "Proteina", "Suplementos", 12, 96000.00),
                    (2, "Creatina", "Suplementos", 6, 82000.00),
                    (3, "Guantes", "Implementos", 17, 45000.00)
                ]
                cursor.executemany(
                    "INSERT INTO Inventario (CodigoInv, Producto, Categoria, Stock, Precio) VALUES (%s, %s, %s, %s, %s)",
                    sample_data
                )
                print("Datos de ejemplo insertados en Inventario")
            
            conn.commit()
            cursor.close()
            conn.close()
            print("Base de datos inicializada correctamente")
            
        except Error as e:
            print(f"Error inicializando BD: {e}")
    else:
        print("No se pudo conectar para inicializar la BD")

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/inventario')
def inventario():
    """Muestra el inventario"""
    conn = get_db_connection()
    inventario_items = []
    error = None
    
    if conn is None:
        error = "No se pudo conectar a la base de datos. Verifica que MySQL esté ejecutándose."
    else:
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT CodigoInv, Producto, Categoria, Stock, Precio FROM Inventario")
            inventario_items = cursor.fetchall()
            cursor.close()
            conn.close()
            
            print(f"Datos obtenidos: {len(inventario_items)} items")
            
        except Error as e:
            error = f"Error al obtener datos: {str(e)}"
    
    return render_template('inventario.html', inventario_items=inventario_items, error=error)

@app.route('/registrar_inventario', methods=['GET'])
def registrar_inventario():
    return render_template('registrar_inventario.html')

@app.route('/registrar_inventario', methods=['POST'])
def registrar_inventario_post():
    producto = request.form.get('producto')
    categoria = request.form.get('categoria')
    stock = request.form.get('stock')
    precio = request.form.get('precio')

    if not all([producto, categoria, stock, precio]):
        flash('Todos los campos son obligatorios.', 'error')
        return render_template('registrar_inventario.html', 
                             producto=producto, categoria=categoria, 
                             stock=stock, precio=precio)

    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            # Obtener el máximo código y sumar 1
            cursor.execute("SELECT MAX(CodigoInv) FROM Inventario")
            max_code = cursor.fetchone()[0]
            next_code = (max_code or 0) + 1
            
            cursor.execute(
                "INSERT INTO Inventario (CodigoInv, Producto, Categoria, Stock, Precio) VALUES (%s, %s, %s, %s, %s)",
                (next_code, producto, categoria, int(stock), float(precio))
            )
            conn.commit()
            flash('Producto agregado exitosamente!', 'success')
            cursor.close()
            conn.close()
        except Error as e:
            flash(f'Error al guardar: {str(e)}', 'error')
    else:
        flash('Error de conexión a la base de datos', 'error')
    
    return redirect(url_for('inventario'))

@app.route('/editar_inventario/<int:codigo_inv>', methods=['GET'])
def editar_inventario(codigo_inv):
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM Inventario WHERE CodigoInv = %s", (codigo_inv,))
            item = cursor.fetchone()
            cursor.close()
            conn.close()
            
            if item:
                return render_template('editar_inventario.html', item=item)
            else:
                flash('Producto no encontrado', 'error')
                return redirect(url_for('inventario'))
        except Error as e:
            flash(f'Error: {str(e)}', 'error')
            return redirect(url_for('inventario'))
    else:
        flash('Error de conexión', 'error')
        return redirect(url_for('inventario'))

@app.route('/editar_inventario/<int:codigo_inv>', methods=['POST'])
def editar_inventario_post(codigo_inv):
    producto = request.form.get('producto')
    categoria = request.form.get('categoria')
    stock = request.form.get('stock')
    precio = request.form.get('precio')

    if not all([producto, categoria, stock, precio]):
        flash('Todos los campos son obligatorios.', 'error')
        return redirect(url_for('editar_inventario', codigo_inv=codigo_inv))

    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE Inventario SET Producto = %s, Categoria = %s, Stock = %s, Precio = %s WHERE CodigoInv = %s",
                (producto, categoria, int(stock), float(precio), codigo_inv)
            )
            conn.commit()
            flash('Producto actualizado exitosamente!', 'success')
            cursor.close()
            conn.close()
        except Error as e:
            flash(f'Error al actualizar: {str(e)}', 'error')
    else:
        flash('Error de conexión', 'error')
    
    return redirect(url_for('inventario'))

@app.route('/eliminar_inventario/<int:codigo_inv>', methods=['POST'])
def eliminar_inventario(codigo_inv):
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM Inventario WHERE CodigoInv = %s", (codigo_inv,))
            conn.commit()
            flash('Producto eliminado exitosamente!', 'success')
            cursor.close()
            conn.close()
        except Error as e:
            flash(f'Error al eliminar: {str(e)}', 'error')
    else:
        flash('Error de conexión', 'error')
    
    return redirect(url_for('inventario'))

@app.route('/maquinas')
def maquinas():
    """Muestra las máquinas"""
    conn = get_db_connection()
    maquinas_list = []
    error = None
    
    if conn is None:
        error = "No se pudo conectar a la base de datos."
    else:
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT CodigoMaq, Nombre, Categoria FROM Maquinas")
            maquinas_list = cursor.fetchall()
            cursor.close()
            conn.close()
            
            print(f"Máquinas obtenidas: {len(maquinas_list)}")
            
        except Error as e:
            error = f"Error al obtener máquinas: {str(e)}"
    
    return render_template('maquinas.html', maquinas_list=maquinas_list, error=error)

@app.route('/registrar_maquina', methods=['GET'])
def registrar_maquina():
    return render_template('registrar_maquina.html')

@app.route('/registrar_maquina', methods=['POST'])
def registrar_maquina_post():
    nombre = request.form.get('nombre')
    categoria = request.form.get('categoria')

    if not all([nombre, categoria]):
        flash('Todos los campos son obligatorios.', 'error')
        return render_template('registrar_maquina.html', nombre=nombre, categoria=categoria)

    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            # Obtener el máximo código y sumar 1
            cursor.execute("SELECT MAX(CodigoMaq) FROM Maquinas")
            max_code = cursor.fetchone()[0]
            next_code = (max_code or 0) + 1
            
            cursor.execute(
                "INSERT INTO Maquinas (CodigoMaq, Nombre, Categoria) VALUES (%s, %s, %s)",
                (next_code, nombre, categoria)
            )
            conn.commit()
            flash('Máquina agregada exitosamente!', 'success')
            cursor.close()
            conn.close()
        except Error as e:
            flash(f'Error al guardar: {str(e)}', 'error')
    else:
        flash('Error de conexión a la base de datos', 'error')
    
    return redirect(url_for('maquinas'))

@app.route('/editar_maquina/<int:codigo_maq>', methods=['GET'])
def editar_maquina(codigo_maq):
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM Maquinas WHERE CodigoMaq = %s", (codigo_maq,))
            maquina = cursor.fetchone()
            cursor.close()
            conn.close()
            
            if maquina:
                return render_template('editar_maquina.html', maquina=maquina)
            else:
                flash('Máquina no encontrada', 'error')
                return redirect(url_for('maquinas'))
        except Error as e:
            flash(f'Error: {str(e)}', 'error')
            return redirect(url_for('maquinas'))
    else:
        flash('Error de conexión', 'error')
        return redirect(url_for('maquinas'))

@app.route('/editar_maquina/<int:codigo_maq>', methods=['POST'])
def editar_maquina_post(codigo_maq):
    nombre = request.form.get('nombre')
    categoria = request.form.get('categoria')

    if not all([nombre, categoria]):
        flash('Todos los campos son obligatorios.', 'error')
        return redirect(url_for('editar_maquina', codigo_maq=codigo_maq))

    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE Maquinas SET Nombre = %s, Categoria = %s WHERE CodigoMaq = %s",
                (nombre, categoria, codigo_maq)
            )
            conn.commit()
            flash('Máquina actualizada exitosamente!', 'success')
            cursor.close()
            conn.close()
        except Error as e:
            flash(f'Error al actualizar: {str(e)}', 'error')
    else:
        flash('Error de conexión', 'error')
    
    return redirect(url_for('maquinas'))

@app.route('/eliminar_maquina/<int:codigo_maq>', methods=['POST'])
def eliminar_maquina(codigo_maq):
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM Maquinas WHERE CodigoMaq = %s", (codigo_maq,))
            conn.commit()
            flash('Máquina eliminada exitosamente!', 'success')
            cursor.close()
            conn.close()
        except Error as e:
            flash(f'Error al eliminar: {str(e)}', 'error')
    else:
        flash('Error de conexión', 'error')
    
    return redirect(url_for('maquinas'))

@app.route('/usuarios')
def usuarios():
    """Muestra los usuarios"""
    conn = get_db_connection()
    usuarios_list = []
    error = None
    
    if conn is None:
        error = "No se pudo conectar a la base de datos."
    else:
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("""
                SELECT u.ID_Usuario, u.Nombre, u.Apellido, u.Telefono, u.Direccion, 
                       u.Edad, u.Seguro, u.Fecha_Registro,
                       m.Plan as Membresia_Plan, m.Costo as Membresia_Costo,
                       m.Duracion_meses as Membresia_Duracion
                FROM Usuario u
                LEFT JOIN Membresia m ON u.ID_Usuario = m.FK_idusuario
            """)
            usuarios_list = cursor.fetchall()
            cursor.close()
            conn.close()
            
            print(f"Usuarios obtenidos: {len(usuarios_list)}")
            
        except Error as e:
            error = f"Error al obtener usuarios: {str(e)}"
    
    return render_template('usuarios.html', usuarios_list=usuarios_list, error=error)

@app.route('/registrar_usuario', methods=['GET'])
def registrar_usuario():
    return render_template('registrar_usuario.html')

@app.route('/registrar_usuario', methods=['POST'])
def registrar_usuario_post():
    nombre = request.form.get('nombre')
    apellido = request.form.get('apellido')
    telefono = request.form.get('telefono')
    direccion = request.form.get('direccion')
    edad = request.form.get('edad')
    seguro = request.form.get('seguro')
    fecha_registro = request.form.get('fecha_registro')
    plan_membresia = request.form.get('plan_membresia')
    duracion_membresia = request.form.get('duracion_membresia')

    # Validación básica
    if not all([nombre, apellido, telefono, direccion, edad, seguro, fecha_registro]):
        flash('Todos los campos obligatorios deben ser completados.', 'error')
        return render_template('registrar_usuario.html', 
                             nombre=nombre, apellido=apellido, telefono=telefono,
                             direccion=direccion, edad=edad, seguro=seguro,
                             fecha_registro=fecha_registro, plan_membresia=plan_membresia,
                             duracion_membresia=duracion_membresia)

    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            
            # Obtener el próximo ID de usuario
            cursor.execute("SELECT MAX(ID_Usuario) FROM Usuario")
            max_id = cursor.fetchone()[0]
            next_id = (max_id or 0) + 11  # Incremento de 11 como en los datos de ejemplo
            
            # Insertar usuario
            cursor.execute(
                """INSERT INTO Usuario (ID_Usuario, Nombre, Apellido, Telefono, Direccion, 
                                      Edad, Seguro, Fecha_Registro) 
                   VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""",
                (next_id, nombre, apellido, telefono, direccion, int(edad), seguro, fecha_registro)
            )
            
            # Si se seleccionó un plan de membresía, insertarlo
            if plan_membresia and duracion_membresia:
                # Obtener el próximo ID de membresía
                cursor.execute("SELECT MAX(ID_Membresia) FROM Membresia")
                max_membresia_id = cursor.fetchone()[0]
                next_membresia_id = (max_membresia_id or 0) + 1
                
                # Calcular costo basado en el plan
                costos = {
                    'Básico': 50.00,
                    'Premium': 120.00,
                    'Anual': 200.00
                }
                costo = costos.get(plan_membresia, 50.00)
                
                cursor.execute(
                    """INSERT INTO Membresia (ID_Membresia, Plan, Costo, Duracion_meses, FK_idusuario) 
                       VALUES (%s, %s, %s, %s, %s)""",
                    (next_membresia_id, plan_membresia, costo, int(duracion_membresia), next_id)
                )
            
            conn.commit()
            flash('Usuario registrado exitosamente!', 'success')
            cursor.close()
            conn.close()
            
        except Error as e:
            flash(f'Error al guardar usuario: {str(e)}', 'error')
    else:
        flash('Error de conexión a la base de datos', 'error')
    
    return redirect(url_for('usuarios'))

@app.route('/editar_usuario/<int:id_usuario>', methods=['GET'])
def editar_usuario(id_usuario):
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor(dictionary=True)
            # Obtener datos del usuario
            cursor.execute("SELECT * FROM Usuario WHERE ID_Usuario = %s", (id_usuario,))
            usuario = cursor.fetchone()
            
            # Obtener datos de la membresía si existe
            cursor.execute("SELECT * FROM Membresia WHERE FK_idusuario = %s", (id_usuario,))
            membresia = cursor.fetchone()
            
            cursor.close()
            conn.close()
            
            if usuario:
                return render_template('editar_usuario.html', usuario=usuario, membresia=membresia)
            else:
                flash('Usuario no encontrado', 'error')
                return redirect(url_for('usuarios'))
        except Error as e:
            flash(f'Error: {str(e)}', 'error')
            return redirect(url_for('usuarios'))
    else:
        flash('Error de conexión', 'error')
        return redirect(url_for('usuarios'))

@app.route('/editar_usuario/<int:id_usuario>', methods=['POST'])
def editar_usuario_post(id_usuario):
    nombre = request.form.get('nombre')
    apellido = request.form.get('apellido')
    telefono = request.form.get('telefono')
    direccion = request.form.get('direccion')
    edad = request.form.get('edad')
    seguro = request.form.get('seguro')
    fecha_registro = request.form.get('fecha_registro')
    plan_membresia = request.form.get('plan_membresia')
    duracion_membresia = request.form.get('duracion_membresia')

    if not all([nombre, apellido, telefono, direccion, edad, seguro, fecha_registro]):
        flash('Todos los campos obligatorios deben ser completados.', 'error')
        return redirect(url_for('editar_usuario', id_usuario=id_usuario))

    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            
            # Actualizar usuario
            cursor.execute(
                """UPDATE Usuario SET Nombre = %s, Apellido = %s, Telefono = %s, 
                   Direccion = %s, Edad = %s, Seguro = %s, Fecha_Registro = %s 
                   WHERE ID_Usuario = %s""",
                (nombre, apellido, telefono, direccion, int(edad), seguro, fecha_registro, id_usuario)
            )
            
            # Manejar membresía
            if plan_membresia and duracion_membresia:
                # Verificar si ya existe una membresía
                cursor.execute("SELECT ID_Membresia FROM Membresia WHERE FK_idusuario = %s", (id_usuario,))
                membresia_existente = cursor.fetchone()
                
                costos = {
                    'Básico': 50.00,
                    'Premium': 120.00,
                    'Anual': 200.00
                }
                costo = costos.get(plan_membresia, 50.00)
                
                if membresia_existente:
                    # Actualizar membresía existente
                    cursor.execute(
                        """UPDATE Membresia SET Plan = %s, Costo = %s, Duracion_meses = %s 
                           WHERE FK_idusuario = %s""",
                        (plan_membresia, costo, int(duracion_membresia), id_usuario)
                    )
                else:
                    # Crear nueva membresía
                    cursor.execute("SELECT MAX(ID_Membresia) FROM Membresia")
                    max_membresia_id = cursor.fetchone()[0]
                    next_membresia_id = (max_membresia_id or 0) + 1
                    
                    cursor.execute(
                        """INSERT INTO Membresia (ID_Membresia, Plan, Costo, Duracion_meses, FK_idusuario) 
                           VALUES (%s, %s, %s, %s, %s)""",
                        (next_membresia_id, plan_membresia, costo, int(duracion_membresia), id_usuario)
                    )
            
            conn.commit()
            flash('Usuario actualizado exitosamente!', 'success')
            cursor.close()
            conn.close()
            
        except Error as e:
            flash(f'Error al actualizar: {str(e)}', 'error')
    else:
        flash('Error de conexión', 'error')
    
    return redirect(url_for('usuarios'))

@app.route('/eliminar_usuario/<int:id_usuario>', methods=['POST'])
def eliminar_usuario(id_usuario):
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            
            # Primero eliminar la membresía si existe (por la clave foránea)
            cursor.execute("DELETE FROM Membresia WHERE FK_idusuario = %s", (id_usuario,))
            
            # Luego eliminar el usuario
            cursor.execute("DELETE FROM Usuario WHERE ID_Usuario = %s", (id_usuario,))
            
            conn.commit()
            flash('Usuario eliminado exitosamente!', 'success')
            cursor.close()
            conn.close()
            
        except Error as e:
            flash(f'Error al eliminar: {str(e)}', 'error')
    else:
        flash('Error de conexión', 'error')
    
    return redirect(url_for('usuarios'))

@app.route('/personal')
def personal():
    """Muestra el personal"""
    conn = get_db_connection()
    personal_list = []
    error = None
    
    if conn is None:
        error = "No se pudo conectar a la base de datos."
    else:
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("""
                SELECT ID_Personal, Nombre, Apellido, Rol, Salario, Fecha_Contratacion 
                FROM Personal
            """)
            personal_list = cursor.fetchall()
            cursor.close()
            conn.close()
            
            print(f"Personal obtenido: {len(personal_list)}")
            
        except Error as e:
            error = f"Error al obtener personal: {str(e)}"
    
    return render_template('personal.html', personal_list=personal_list, error=error)

@app.route('/registrar_personal', methods=['GET'])
def registrar_personal():
    return render_template('registrar_personal.html')

@app.route('/registrar_personal', methods=['POST'])
def registrar_personal_post():
    nombre = request.form.get('nombre')
    apellido = request.form.get('apellido')
    rol = request.form.get('rol')
    salario = request.form.get('salario')
    fecha_contratacion = request.form.get('fecha_contratacion')

    if not all([nombre, apellido, rol, salario, fecha_contratacion]):
        flash('Todos los campos son obligatorios.', 'error')
        return render_template('registrar_personal.html', 
                             nombre=nombre, apellido=apellido, rol=rol,
                             salario=salario, fecha_contratacion=fecha_contratacion)

    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            
            # Obtener el próximo ID de personal
            cursor.execute("SELECT MAX(ID_Personal) FROM Personal")
            max_id = cursor.fetchone()[0]
            next_id = (max_id or 0) + 11  # Incremento de 11 como en los datos de ejemplo
            
            # Insertar personal
            cursor.execute(
                """INSERT INTO Personal (ID_Personal, Nombre, Apellido, Rol, Salario, Fecha_Contratacion) 
                   VALUES (%s, %s, %s, %s, %s, %s)""",
                (next_id, nombre, apellido, rol, float(salario), fecha_contratacion)
            )
            
            conn.commit()
            flash('Miembro del personal registrado exitosamente!', 'success')
            cursor.close()
            conn.close()
            
        except Error as e:
            flash(f'Error al guardar: {str(e)}', 'error')
    else:
        flash('Error de conexión a la base de datos', 'error')
    
    return redirect(url_for('personal'))

@app.route('/editar_personal/<int:id_personal>', methods=['GET'])
def editar_personal(id_personal):
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM Personal WHERE ID_Personal = %s", (id_personal,))
            personal = cursor.fetchone()
            cursor.close()
            conn.close()
            
            if personal:
                return render_template('editar_personal.html', personal=personal)
            else:
                flash('Miembro del personal no encontrado', 'error')
                return redirect(url_for('personal'))
        except Error as e:
            flash(f'Error: {str(e)}', 'error')
            return redirect(url_for('personal'))
    else:
        flash('Error de conexión', 'error')
        return redirect(url_for('personal'))

@app.route('/editar_personal/<int:id_personal>', methods=['POST'])
def editar_personal_post(id_personal):
    nombre = request.form.get('nombre')
    apellido = request.form.get('apellido')
    rol = request.form.get('rol')
    salario = request.form.get('salario')
    fecha_contratacion = request.form.get('fecha_contratacion')

    if not all([nombre, apellido, rol, salario, fecha_contratacion]):
        flash('Todos los campos son obligatorios.', 'error')
        return redirect(url_for('editar_personal', id_personal=id_personal))

    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute(
                """UPDATE Personal SET Nombre = %s, Apellido = %s, Rol = %s, 
                   Salario = %s, Fecha_Contratacion = %s 
                   WHERE ID_Personal = %s""",
                (nombre, apellido, rol, float(salario), fecha_contratacion, id_personal)
            )
            conn.commit()
            flash('Miembro del personal actualizado exitosamente!', 'success')
            cursor.close()
            conn.close()
        except Error as e:
            flash(f'Error al actualizar: {str(e)}', 'error')
    else:
        flash('Error de conexión', 'error')
    
    return redirect(url_for('personal'))

@app.route('/eliminar_personal/<int:id_personal>', methods=['POST'])
def eliminar_personal(id_personal):
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM Personal WHERE ID_Personal = %s", (id_personal,))
            conn.commit()
            flash('Miembro del personal eliminado exitosamente!', 'success')
            cursor.close()
            conn.close()
        except Error as e:
            flash(f'Error al eliminar: {str(e)}', 'error')
    else:
        flash('Error de conexión', 'error')
    
    return redirect(url_for('personal'))

@app.route('/distribuidores')
def distribuidores():
    """Muestra los distribuidores"""
    conn = get_db_connection()
    distribuidores_list = []
    error = None
    
    if conn is None:
        error = "No se pudo conectar a la base de datos."
    else:
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("""
                SELECT ID_Distribuidor, Nombre, Apellido, Telefono, Categoria 
                FROM Distribuidor
            """)
            distribuidores_list = cursor.fetchall()
            cursor.close()
            conn.close()
            
            print(f"Distribuidores obtenidos: {len(distribuidores_list)}")
            
        except Error as e:
            error = f"Error al obtener distribuidores: {str(e)}"
    
    return render_template('distribuidores.html', distribuidores_list=distribuidores_list, error=error)

@app.route('/registrar_distribuidor', methods=['GET'])
def registrar_distribuidor():
    return render_template('registrar_distribuidor.html')

@app.route('/registrar_distribuidor', methods=['POST'])
def registrar_distribuidor_post():
    nombre = request.form.get('nombre')
    apellido = request.form.get('apellido')
    telefono = request.form.get('telefono')
    categoria = request.form.get('categoria')

    if not all([nombre, apellido, telefono, categoria]):
        flash('Todos los campos son obligatorios.', 'error')
        return render_template('registrar_distribuidor.html', 
                             nombre=nombre, apellido=apellido, telefono=telefono,
                             categoria=categoria)

    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            
            # Obtener el próximo ID de distribuidor
            cursor.execute("SELECT MAX(ID_Distribuidor) FROM Distribuidor")
            max_id = cursor.fetchone()[0]
            next_id = (max_id or 0) + 1
            
            # Insertar distribuidor
            cursor.execute(
                """INSERT INTO Distribuidor (ID_Distribuidor, Nombre, Apellido, Telefono, Categoria) 
                   VALUES (%s, %s, %s, %s, %s)""",
                (next_id, nombre, apellido, telefono, categoria)
            )
            
            conn.commit()
            flash('Distribuidor registrado exitosamente!', 'success')
            cursor.close()
            conn.close()
            
        except Error as e:
            flash(f'Error al guardar: {str(e)}', 'error')
    else:
        flash('Error de conexión a la base de datos', 'error')
    
    return redirect(url_for('distribuidores'))

@app.route('/editar_distribuidor/<int:id_distribuidor>', methods=['GET'])
def editar_distribuidor(id_distribuidor):
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM Distribuidor WHERE ID_Distribuidor = %s", (id_distribuidor,))
            distribuidor = cursor.fetchone()
            cursor.close()
            conn.close()
            
            if distribuidor:
                return render_template('editar_distribuidor.html', distribuidor=distribuidor)
            else:
                flash('Distribuidor no encontrado', 'error')
                return redirect(url_for('distribuidores'))
        except Error as e:
            flash(f'Error: {str(e)}', 'error')
            return redirect(url_for('distribuidores'))
    else:
        flash('Error de conexión', 'error')
        return redirect(url_for('distribuidores'))

@app.route('/editar_distribuidor/<int:id_distribuidor>', methods=['POST'])
def editar_distribuidor_post(id_distribuidor):
    nombre = request.form.get('nombre')
    apellido = request.form.get('apellido')
    telefono = request.form.get('telefono')
    categoria = request.form.get('categoria')

    if not all([nombre, apellido, telefono, categoria]):
        flash('Todos los campos son obligatorios.', 'error')
        return redirect(url_for('editar_distribuidor', id_distribuidor=id_distribuidor))

    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute(
                """UPDATE Distribuidor SET Nombre = %s, Apellido = %s, Telefono = %s, Categoria = %s 
                   WHERE ID_Distribuidor = %s""",
                (nombre, apellido, telefono, categoria, id_distribuidor)
            )
            conn.commit()
            flash('Distribuidor actualizado exitosamente!', 'success')
            cursor.close()
            conn.close()
        except Error as e:
            flash(f'Error al actualizar: {str(e)}', 'error')
    else:
        flash('Error de conexión', 'error')
    
    return redirect(url_for('distribuidores'))

@app.route('/eliminar_distribuidor/<int:id_distribuidor>', methods=['POST'])
def eliminar_distribuidor(id_distribuidor):
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM Distribuidor WHERE ID_Distribuidor = %s", (id_distribuidor,))
            conn.commit()
            flash('Distribuidor eliminado exitosamente!', 'success')
            cursor.close()
            conn.close()
        except Error as e:
            flash(f'Error al eliminar: {str(e)}', 'error')
    else:
        flash('Error de conexión', 'error')
    
    return redirect(url_for('distribuidores'))

if __name__ == '__main__':
    # Inicializar la base de datos al iniciar la aplicación
    init_database()
    print("Servidor iniciado. Accede a: http://localhost:5000")
    app.run(debug=True)



