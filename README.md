# API de Reservas de Salas (FastAPI)

Una API RESTful robusta construida con **FastAPI** para gestionar la reserva de salas o espacios. Este proyecto incluye autenticación segura, manejo de base de datos relacional y control de concurrencia para evitar cruces de horarios.

## Características Principales

* **Autenticación y Seguridad:** Sistema de Login utilizando JSON Web Tokens (JWT) y encriptación de contraseñas con `bcrypt`.
* **Base de Datos Relacional:** Uso de **SQLite** y **SQLAlchemy** (ORM) con relaciones entre Usuarios, Salas y Reservas.
* **Control de Concurrencia:** Implementación de *bloqueo pesimista* (`with_for_update()`) en la base de datos para asegurar que dos personas no puedan reservar la misma sala en el mismo horario.
* **Validación de Datos:** Uso estricto de **Pydantic** (V2) para validar los datos de entrada y salida de la API.
* **Documentación Interactiva:** Documentación autogenerada con Swagger UI (OpenAPI).

## Tecnologías Utilizadas

* **Python 3.10+**
* **FastAPI** (Framework Web)
* **Uvicorn** (Servidor ASGI)
* **SQLAlchemy** (ORM)
* **SQLite** (Base de Datos)
* **Passlib & Python-Jose** (Seguridad y JWT)

## Instalación y Uso Local

Sigue estos pasos para ejecutar el proyecto en tu máquina local:

1. **Clonar el repositorio:**
   ```bash
   git clone [https://github.com/TuUsuario/reservation-app.git](https://github.com/TuUsuario/reservation-app.git)
   cd reservation-app

```

2. **Crear y activar un entorno virtual:**
```bash
python -m venv venv
# En Windows:
venv\Scripts\activate
# En macOS/Linux:
source venv/bin/activate

```


3. **Instalar las dependencias:**
```bash
pip install -r requirements.txt

```


4. **Ejecutar el servidor de desarrollo:**
```bash
uvicorn api.main:app --reload

```


5. **Probar la API:**
Abre tu navegador y ve a `http://127.0.0.1:8000/docs` para interactuar con la interfaz de Swagger.

## Endpoints Principales

* `POST /users/` - Registro de un nuevo usuario.
* `POST /login/` - Autenticación y generación del Token JWT.
* `POST /reservations/` - Creación de una reserva (Requiere Token).
* `GET /reservations/` - Lista de todas las reservas del sistema (Requiere Token).

## Autor

Desarrollado por **[ChristianAceved]** como parte de mi portafolio de desarrollo Backend.
