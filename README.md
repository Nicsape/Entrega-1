Sistema de Gestión de Gimnasio

Este proyecto es una aplicación web desarrollada en Python que permite la gestión administrativa de un gimnasio, incluyendo el control de usuarios, máquinas, inventario, personal y distribuidores.

Características

Gestión de usuarios

Gestión de máquinas (registro, edición y categorización)

Gestión de inventario

Gestión de personal

Gestión de distribuidores

Integración con base de datos SQL

Tecnologías utilizadas

Python

SQL (gestionado con DBeaver)

JSON

Git y GitHub

Requisitos

Antes de ejecutar el proyecto, asegúrate de tener instalado:

Python 3.x

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

3. Configurar la conexión a la base de datos

Editar el archivo de conexión en el proyecto (por ejemplo):

conexion = {
    "host": "localhost",
    "usuario": "root",
    "password": "12345",
    "database": "Gimnasio"
}
4. Ejecutar el proyecto

En la terminal:

python app.py
