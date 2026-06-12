# Importa el módulo os para acceder a variables de entorno del sistema operativo
import os


class Config:
    """Clase de configuración centralizada para la aplicación Flask."""

    # Llave secreta usada por Flask para sesiones, cookies seguras y protección CSRF
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'cecytos_secret_key_sostenible_2026'

    # Host del servidor MySQL (se toma de variable de entorno si existe, si no usa localhost)
    MYSQL_HOST = os.environ.get('MYSQL_HOST') or 'localhost'

    # Usuario de la base de datos MySQL
    MYSQL_USER = os.environ.get('MYSQL_USER') or 'root'

    # Contraseña del usuario MySQL
    MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD') or 'root123'

    # Nombre de la base de datos que usa el sistema
    MYSQL_DB = os.environ.get('MYSQL_DB') or 'cecytos_db'

    # Tipo de cursor: DictCursor devuelve resultados como diccionarios en lugar de tuplas
    MYSQL_CURSORCLASS = 'DictCursor'