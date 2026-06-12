# Importa Flask, el framework principal para crear aplicaciones web en Python
from flask import Flask, render_template

# Importa la configuración central del proyecto (variables como DB, secret key, etc.)
from config import Config

# Importa el conector MySQL ya configurado para integrarlo con Flask
from controllers.db_controller import mysql

# Importa el Blueprint de autenticación (login, registro, logout)
from routes.auth import auth_bp

# Importa el Blueprint del módulo de usuario (funciones del usuario normal)
from routes.usuario import usuario_bp

# Importa el Blueprint del módulo administrativo (panel admin)
from routes.admin import admin_bp


def create_app():
    """Factoría de aplicación Flask: construye y configura la app completa."""

    # Crea la instancia principal de la aplicación Flask
    app = Flask(__name__)

    # Carga toda la configuración definida en la clase Config
    app.config.from_object(Config)

    # Inicializa la conexión MySQL dentro del contexto de la aplicación Flask
    mysql.init_app(app)

    # Registro de Blueprints: divide la app en módulos funcionales
    app.register_blueprint(auth_bp)     # Rutas de autenticación
    app.register_blueprint(usuario_bp)  # Rutas de usuario
    app.register_blueprint(admin_bp)    # Rutas de administración

    @app.route('/')  # Define la ruta principal del sitio web
    def index():
        """Renderiza la página de inicio pública."""
        return render_template('index.html')

    @app.errorhandler(404)  # Captura cualquier error de ruta no encontrada
    def page_not_found(e):
        """Manejador global para errores 404."""
        return render_template('base.html'), 404

    return app  # Devuelve la aplicación completamente configurada


# Crea la instancia global de la aplicación Flask
app = create_app()

# Punto de entrada del programa cuando se ejecuta directamente
if __name__ == '__main__':
    # Ejecuta el servidor en modo desarrollo con recarga automática
    app.run(debug=True, port=5000)