Sistema de Gestión de Gimnasio

Este proyecto es una aplicación web desarrollada en Python (Flask) que permite la gestión administrativa de un gimnasio, incluyendo el control de usuarios, máquinas, inventario, personal y distribuidores.

Además, se implementa una arquitectura de persistencia políglota, integrando:

🟦 Base de datos relacional (SQL)
🟩 Base de datos NoSQL (MongoDB)

Características

-Gestión de usuarios

-Gestión de máquinas (registro, edición y categorización)

-Gestión de inventario

-Gestión de personal

-Gestión de distribuidores

Nuevo módulo (NoSQL - MongoDB)
-Registro de notificaciones dinámicas
-Almacenamiento de datos en formato JSON flexible
-Soporte para contenido dinámico (texto, futuros campos multimedia)


Tecnologías utilizadas:

-Python (Flask)
-MySQL (DBeaver)
-MongoDB
-JSON
-Git y GitHub

Requisitos
Antes de ejecutar el proyecto, asegúrate de tener instalado:
Python 3.x
MongoDB (ejecutándose en local)
DBeaver o cualquier gestor de bases de datos SQL
Git

Instalación y ejecución
1. Clonar el repositorio
git clone https://github.com/Nicsape/Entrega-1.git
cd Entrega-1
2. Configurar la base de datos
Abrir DBeaver
Crear una nueva base de datos
Importar el archivo:
bd_gym.sql
Ejecutar el script SQL para crear las tablas
3. Configurar MongoDB
Asegurarse de que MongoDB esté corriendo en:
mongodb://localhost:27017/
La base de datos utilizada es:
Gym
Colección:
notificaciones
4. Instalar dependencias
pip install flask pymongo mysql-connector-python
5. Configurar la conexión a la base de datos

Editar el archivo de conexión en el proyecto (por ejemplo):

conexion = {
    "host": "localhost",
    "usuario": "root",
    "password": "12345",
    "database": "Gimnasio"
}
6. Ejecutar el proyecto

En la terminal:
python app.py

La integración de MongoDB permite manejar información dinámica de forma flexible, complementando el modelo relacional existente. Esto mejora la escalabilidad del sistema y permite gestionar datos con estructuras variables sin afectar el esquema SQL.
