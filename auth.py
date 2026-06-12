from flask import Blueprint, render_template, request, redirect, url_for, flash, session  # Importa herramientas de Flask para rutas, templates, formularios, redirecciones, mensajes y manejo de sesión
from controllers.db_controller import DBController  # Importa el controlador personalizado para ejecutar consultas a la base de datos
from datetime import datetime  # Importa datetime para generar fechas de registro

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')  # Crea un Blueprint para agrupar rutas de autenticación bajo /auth

@auth_bp.route('/register', methods=['GET', 'POST'])  # Define ruta de registro, acepta GET (mostrar formulario) y POST (enviar datos)
def register():  # Función que maneja el registro de usuarios

    if request.method == 'POST':  # Verifica si el formulario fue enviado
        nombre = request.form.get('nombre')  # Obtiene el nombre del formulario
        correo = request.form.get('correo')  # Obtiene el correo del formulario
        password = request.form.get('password')  # Obtiene la contraseña del formulario
        
        # Validar si el correo ya existe
        user_exists = DBController.query(
            "SELECT id_usuario FROM usuario WHERE correo = %s",
            (correo,),
            fetchone=True
        )  # Busca si ya existe un usuario con ese correo

        if user_exists:  # Si el usuario ya existe
            flash('El correo electrónico ya se encuentra registrado.', 'danger')  # Mensaje de error
            return redirect(url_for('auth.register'))  # Redirige al formulario de registro
        
        # Obtener la fecha y hora actual en formato de cadena para la base de datos
        fecha_actual = datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # Genera timestamp de registro
        
        # Guardar usuario con contraseña en texto plano y su fecha de registro
        DBController.query(
            "INSERT INTO usuario (nombre, correo, contraseña, rol, fecha_registro) VALUES (%s, %s, %s, 'usuario', %s)",
            (nombre, correo, password, fecha_actual),
            commit=True
        )  # Inserta el nuevo usuario en la base de datos

        flash('Registro exitoso. Ahora puedes iniciar sesión.', 'success')  # Mensaje de éxito
        return redirect(url_for('auth.login'))  # Redirige al login
        
    return render_template('auth/register.html')  # Muestra la vista de registro si es GET


@auth_bp.route('/login', methods=['GET', 'POST'])  # Define ruta de login
def login():  # Función que maneja el inicio de sesión

    if request.method == 'POST':  # Verifica si se envió el formulario
        correo = request.form.get('correo')  # Obtiene correo ingresado
        password = request.form.get('password')  # Obtiene contraseña ingresada
        
        user = DBController.query(
            "SELECT * FROM usuario WHERE correo = %s",
            (correo,),
            fetchone=True
        )  # Busca el usuario en la base de datos

        # Validación directa usando texto plano (sin hashing, lo cual es inseguro en producción)
        if user and user['contraseña'] == password:  # Verifica credenciales
            session['user_id'] = user['id_usuario']  # Guarda ID del usuario en sesión
            session['user_name'] = user['nombre']  # Guarda nombre en sesión
            session['user_role'] = user['rol']  # Guarda rol en sesión
            
            flash(f'¡Bienvenido de nuevo, {user["nombre"]}!', 'success')  # Mensaje de bienvenida

            if user['rol'] == 'admin':  # Si es administrador
                return redirect(url_for('admin.dashboard'))  # Redirige al panel admin
            
            return redirect(url_for('usuario.dashboard'))  # Si no, al dashboard de usuario
        else:
            flash('Credenciales incorrectas. Intenta nuevamente.', 'danger')  # Error de login
            
    return render_template('auth/login.html')  # Muestra formulario de login


@auth_bp.route('/logout')  # Ruta para cerrar sesión
def logout():  # Función de logout
    session.clear()  # Borra toda la sesión del usuario
    flash('Has cerrado sesión correctamente.', 'info')  # Mensaje informativo
    return redirect(url_for('index'))  # Redirige a la página principal