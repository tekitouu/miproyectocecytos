from flask import Blueprint, render_template, request, redirect, url_for, flash  # Importa herramientas de Flask para rutas, plantillas, formularios, redirecciones y mensajes
from controllers.db_controller import DBController  # Importa el controlador de base de datos personalizado
from utils.decorators import role_required  # Importa el decorador para restringir acceso por roles

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')  # Crea un Blueprint para agrupar todas las rutas administrativas

# Función interna de ayuda para no repetir el código de los contadores en cada ruta
def obtener_estadisticas():  # Define una función para obtener estadísticas generales del sistema
    return {  # Retorna un diccionario con los contadores
        'usuarios': DBController.query("SELECT COUNT(*) as t FROM usuario WHERE rol='usuario'", fetchone=True)['t'],  # Cuenta usuarios normales
        'servicios': DBController.query("SELECT COUNT(*) as t FROM servicio", fetchone=True)['t'],  # Cuenta servicios registrados
        'problemas': DBController.query("SELECT COUNT(*) as t FROM problema", fetchone=True)['t'],  # Cuenta problemas reportados
        'ubicaciones': DBController.query("SELECT COUNT(*) as t FROM ubicacion", fetchone=True)['t'],  # Cuenta ubicaciones registradas
        'sugerencias': DBController.query("SELECT COUNT(*) as t FROM sugerencia", fetchone=True)['t']  # Cuenta sugerencias enviadas
    }

@admin_bp.route('/dashboard')  # Define la ruta del panel principal
@role_required('admin')  # Permite acceso únicamente a administradores
def dashboard():  # Función asociada a la ruta dashboard
    stats = obtener_estadisticas()  # Obtiene estadísticas generales
    return render_template('admin/dashboard.html', stats=stats)  # Renderiza la vista dashboard

# ==================== CRUD USUARIOS ====================

@admin_bp.route('/usuarios')  # Ruta para listar usuarios
@role_required('admin')  # Restringe acceso a administradores
def usuarios():  # Función para mostrar usuarios
    stats = obtener_estadisticas()  # Obtiene estadísticas generales
    lista = DBController.query("SELECT id_usuario, nombre, correo, rol, fecha_registro FROM usuario", fetchall=True)  # Consulta todos los usuarios
    return render_template('admin/usuarios.html', usuarios=lista, stats=stats)  # Envía datos a la plantilla

@admin_bp.route('/usuarios/eliminar/<int:id>')  # Ruta para eliminar un usuario según su ID
@role_required('admin')  # Restringe acceso a administradores
def eliminar_usuario(id):  # Función para eliminar usuario
    DBController.query("DELETE FROM usuario WHERE id_usuario = %s", (id,), commit=True)  # Ejecuta eliminación en la base de datos
    flash('Usuario eliminado del sistema.', 'info')  # Muestra mensaje informativo
    return redirect(url_for('admin.usuarios'))  # Redirige al listado de usuarios

# ==================== CRUD SERVICIOS ====================

@admin_bp.route('/servicios', methods=['GET', 'POST'])  # Ruta para listar y registrar servicios
@role_required('admin')  # Restringe acceso a administradores
def servicios():  # Función principal de servicios

    if request.method == 'POST':  # Verifica si se envió un formulario
        nombre = request.form.get('nombre')  # Obtiene nombre del servicio
        descripcion = request.form.get('descripcion')  # Obtiene descripción del servicio
        estado = request.form.get('estado')  # Obtiene estado del servicio

        DBController.query(
            "INSERT INTO servicio (nombre, descripcion, estado) VALUES (%s, %s, %s)",
            (nombre, descripcion, estado),
            commit=True
        )  # Inserta un nuevo servicio

        flash('Servicio creado con éxito.', 'success')  # Mensaje de éxito
        return redirect(url_for('admin.servicios'))  # Redirección al listado

    stats = obtener_estadisticas()  # Obtiene estadísticas
    lista = DBController.query("SELECT * FROM servicio", fetchall=True)  # Obtiene todos los servicios
    return render_template('admin/servicios.html', servicios=lista, stats=stats)  # Muestra la vista

@admin_bp.route('/servicios/editar/<int:id>', methods=['POST'])  # Ruta para editar un servicio
@role_required('admin')  # Restringe acceso a administradores
def editar_servicio(id):  # Función de edición
    nombre = request.form.get('nombre')  # Obtiene nuevo nombre
    descripcion = request.form.get('descripcion')  # Obtiene nueva descripción
    estado = request.form.get('estado')  # Obtiene nuevo estado

    DBController.query(
        "UPDATE servicio SET nombre=%s, descripcion=%s, estado=%s WHERE id_servicio=%s",
        (nombre, descripcion, estado, id),
        commit=True
    )  # Actualiza los datos del servicio

    flash('Servicio actualizado.', 'success')  # Mensaje de confirmación
    return redirect(url_for('admin.servicios'))  # Regresa al listado

@admin_bp.route('/servicios/eliminar/<int:id>')  # Ruta para eliminar servicio
@role_required('admin')  # Restringe acceso a administradores
def eliminar_servicio(id):  # Función de eliminación
    DBController.query("DELETE FROM servicio WHERE id_servicio = %s", (id,), commit=True)  # Elimina el servicio
    flash('Servicio removido.', 'warning')  # Muestra mensaje de advertencia
    return redirect(url_for('admin.servicios'))  # Regresa al listado

# ==================== CRUD PROBLEMAS ====================

@admin_bp.route('/problemas')  # Ruta para visualizar problemas
@role_required('admin')  # Restringe acceso a administradores
def problemas():  # Función para listar problemas

    stats = obtener_estadisticas()  # Obtiene estadísticas

    lista = DBController.query("""
        SELECT p.*, u.nombre as usuario_nombre, s.nombre as servicio_nombre
        FROM problema p
        JOIN usuario u ON p.id_usuario = u.id_usuario
        LEFT JOIN problema_servicio ps ON p.id_problema = ps.id_problema
        LEFT JOIN servicio s ON ps.id_servicio = s.id_servicio
        ORDER BY p.fecha_reporte DESC
    """, fetchall=True)  # Consulta problemas con usuario y servicio asociado

    return render_template('admin/problemas.html', problemas=lista, stats=stats)  # Renderiza la vista

@admin_bp.route('/problemas/editar/<int:id>', methods=['POST'])  # Ruta para actualizar estado del problema
@role_required('admin')  # Restringe acceso a administradores
def editar_problema(id):  # Función de edición
    estado = request.form.get('estado')  # Obtiene el nuevo estado

    DBController.query(
        "UPDATE problema SET estado = %s WHERE id_problema = %s",
        (estado, id),
        commit=True
    )  # Actualiza estado

    flash('Estado del problema actualizado correctamente.', 'success')  # Mensaje de éxito
    return redirect(url_for('admin.problemas'))  # Regresa al listado

@admin_bp.route('/problemas/eliminar/<int:id>')  # Ruta para eliminar problema
@role_required('admin')  # Restringe acceso a administradores
def eliminar_problema(id):  # Función de eliminación
    DBController.query("DELETE FROM problema WHERE id_problema = %s", (id,), commit=True)  # Elimina problema
    flash('Reporte de problema eliminado.', 'danger')  # Mensaje de eliminación
    return redirect(url_for('admin.problemas'))  # Regresa al listado

# ==================== CRUD UBICACIONES ====================

@admin_bp.route('/ubicaciones', methods=['GET', 'POST'])  # Ruta para gestionar ubicaciones
@role_required('admin')  # Restringe acceso a administradores
def ubicaciones():  # Función principal de ubicaciones

    if request.method == 'POST':  # Comprueba si se envió formulario
        nombre = request.form.get('nombre')  # Obtiene nombre de ubicación
        direccion = request.form.get('direccion')  # Obtiene dirección
        descripcion = request.form.get('descripcion')  # Obtiene descripción

        DBController.query(
            "INSERT INTO ubicacion (nombre, direccion, descripcion) VALUES (%s, %s, %s)",
            (nombre, direccion, descripcion),
            commit=True
        )  # Inserta nueva ubicación

        flash('Nueva ubicación añadida al mapa sustentable.', 'success')  # Mensaje de éxito
        return redirect(url_for('admin.ubicaciones'))  # Regresa al listado

    stats = obtener_estadisticas()  # Obtiene estadísticas
    lista = DBController.query("SELECT * FROM ubicacion", fetchall=True)  # Consulta todas las ubicaciones

    return render_template('admin/ubicaciones.html', ubicaciones=lista, stats=stats)  # Renderiza vista

@admin_bp.route('/ubicaciones/editar/<int:id>', methods=['POST'])  # Ruta para editar ubicación
@role_required('admin')  # Restringe acceso a administradores
def editar_ubicacion(id):  # Función de edición

    nombre = request.form.get('nombre')  # Obtiene nombre actualizado
    direccion = request.form.get('direccion')  # Obtiene dirección actualizada
    descripcion = request.form.get('descripcion')  # Obtiene descripción actualizada

    DBController.query(
        "UPDATE ubicacion SET nombre=%s, direccion=%s, descripcion=%s WHERE id_ubicacion=%s",
        (nombre, direccion, descripcion, id),
        commit=True
    )  # Actualiza ubicación

    flash('Ubicación editada correctamente.', 'success')  # Mensaje de éxito
    return redirect(url_for('admin.ubicaciones'))  # Regresa al listado

@admin_bp.route('/ubicaciones/eliminar/<int:id>')  # Ruta para eliminar ubicación
@role_required('admin')  # Restringe acceso a administradores
def eliminar_ubicacion(id):  # Función de eliminación
    DBController.query("DELETE FROM ubicacion WHERE id_ubicacion = %s", (id,), commit=True)  # Elimina ubicación
    flash('Ubicación removida del sistema.', 'warning')  # Mensaje de advertencia
    return redirect(url_for('admin.ubicaciones'))  # Regresa al listado

# ==================== CONSULTAR SUGERENCIAS ====================

@admin_bp.route('/sugerencias')  # Ruta para visualizar sugerencias
@role_required('admin')  # Restringe acceso a administradores
def sugerencias():  # Función que lista sugerencias

    stats = obtener_estadisticas()  # Obtiene estadísticas

    lista = DBController.query("""
        SELECT s.*, u.nombre as usuario_nombre, u.correo as usuario_correo
        FROM sugerencia s
        JOIN usuario u ON s.id_usuario = u.id_usuario
        ORDER BY s.fecha DESC
    """, fetchall=True)  # Obtiene sugerencias junto con datos del usuario

    return render_template('admin/sugerencias.html', sugerencias=lista, stats=stats)  # Renderiza la plantilla de sugerencias