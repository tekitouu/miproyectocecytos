from functools import wraps  # Permite conservar metadata original de la función decorada (nombre, docstring, etc.)
from flask import session, flash, redirect, url_for  # session: manejo de sesión; flash: mensajes UI; redirect/url_for: control de rutas

def login_required(f):
    """Decorador que restringe el acceso a rutas solo para usuarios autenticados."""

    @wraps(f)  # Evita que la función decorada pierda su identidad original
    def decorated_function(*args, **kwargs):

        if 'user_id' not in session:
            # Si no existe user_id en sesión, el usuario no está autenticado
            flash('Por favor, inicia sesión para acceder a esta sección.', 'danger')  # Mensaje de error al usuario
            return redirect(url_for('auth.login'))  # Redirección forzada al login

        return f(*args, **kwargs)  # Si está autenticado, ejecuta la función original sin modificaciones

    return decorated_function  # Retorna la función envuelta con la validación


def role_required(role):
    """Decorador parametrizable para validar el rol ('admin' o 'usuario') del cliente."""

    def decorator(f):

        @wraps(f)  # Mantiene identidad original de la función decorada
        def decorated_function(*args, **kwargs):

            if 'user_id' not in session:
                # Validación base: si no hay sesión, no puede ni intentar validar rol
                flash('Inicia sesión primero.', 'danger')  # Mensaje para usuario no autenticado
                return redirect(url_for('auth.login'))  # Redirección al login

            if session.get('user_role') != role:
                # Validación de autorización: compara rol guardado en sesión
                flash('No tienes autorización para ver este apartado.', 'warning')  # Acceso denegado por rol
                return redirect(url_for('index'))  # Redirección a página principal

            return f(*args, **kwargs)  # Si pasa ambas validaciones, ejecuta la función protegida

        return decorated_function  # Devuelve la función envuelta con control de rol

    return decorator  # Devuelve el decorador parametrizado