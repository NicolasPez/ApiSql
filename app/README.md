# API REST de Gestión de Tareas

Este proyecto es una API REST desarrollada con **FastAPI**, que permite a los usuarios registrarse, autenticarse y gestionar sus tareas personales (crear, leer, actualizar y eliminar tareas).
La autenticación se maneja mediante **JWT (JSON Web Tokens)**.

## Tecnologías utilizadas

- Python
- FastAPI
- SQLAlchemy Async
- SQLite
- JWT (auth)
- Pydantic

## Funcionalidades

- Registro y login de usuarios
- Creación de tareas personales por usuario
- Visualización de tareas propias
- Actualización y eliminación de tareas
- Autenticación protegida con JWT

## Instalación

1. Clonar el repositorio:
   ```bash
   git clone https://github.com/NicolasPez/ApiSql.git
   ```
2. Crear y activar un entorno virtual:

   ```bash
   python -m venv venv
   source venv/bin/activate  # en Linux/Mac
   venv\Scripts\activate     # en Windows
   ```
3. Instalar dependencias:
   ```
   pip install -r requirements.txt
   ```
4. Ejecutar el servidor:
   ```
   uvicorn main:app --reload
   ```
## Uso
Una vez iniciado el servidor, se accede a la documentación interactiva de la API en:

http://localhost:8000/docs

Desde ahí es posible registrar usuarios, loguearse y gestionar las tareas.
Se debe usar el token JWT para autenticarte antes de realizar acciones protegidas.


## Autor  
Desarrollado por Nicolás Perez Da Cruz  
GitHub: [@NicolasPez](https://github.com/NicolasPez)
