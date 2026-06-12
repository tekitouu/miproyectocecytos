from flask import Blueprint, render_template, request, redirect, url_for, flash, session  # Importa herramientas de Flask para rutas, plantillas, formularios, redirección, mensajes y sesión
from controllers.db_controller import DBController  # Importa el controlador de base de datos
from utils.decorators import role_required  # Decorador para restringir acceso por roles (seguridad por permisos)
from datetime import datetime  # Librería para generar fechas y timestamps

usuario_bp = Blueprint('usuario', __name__, url_prefix='/usuario')  # Blueprint que agrupa todas las rutas del usuario

@usuario_bp.route('/dashboard')  # Ruta del panel principal del usuario
@role_required('usuario')  # Solo usuarios con rol 'usuario' pueden acceder
def dashboard():  # Función del dashboard del usuario

    uid = session['user_id']  # Obtiene el ID del usuario desde la sesión

    # Contadores individuales del usuario
    mis_problemas = DBController.query(
        "SELECT COUNT(*) as total FROM problema WHERE id_usuario = %s",
        (uid,),
        fetchone=True
    )['total']  # Cuenta problemas reportados por el usuario

    mis_sugerencias = DBController.query(
        "SELECT COUNT(*) as total FROM sugerencia WHERE id_usuario = %s",
        (uid,),
        fetchone=True
    )['total']  # Cuenta sugerencias enviadas por el usuario
    
    return render_template(
        'usuario/dashboard.html',
        mis_problemas=mis_problemas,
        mis_sugerencias=mis_sugerencias
    )  # Renderiza el dashboard con métricas


@usuario_bp.route('/perfil', methods=['GET', 'POST'])  # Ruta para ver y editar perfil
@role_required('usuario')  # Solo usuarios autenticados con rol usuario
def perfil():  # Función de perfil

    uid = session['user_id']  # ID del usuario logueado

    if request.method == 'POST':  # Si se envía formulario de actualización
        nombre = request.form.get('nombre')  # Nuevo nombre

        DBController.query(
            "UPDATE usuario SET nombre = %s WHERE id_usuario = %s",
            (nombre, uid),
            commit=True
        )  # Actualiza nombre en base de datos

        session['user_name'] = nombre  # Actualiza nombre en sesión
        flash('Perfil actualizado con éxito.', 'success')  # Mensaje de confirmación
        return redirect(url_for('usuario.perfil'))  # Recarga perfil

    user_data = DBController.query(
        "SELECT * FROM usuario WHERE id_usuario = %s",
        (uid,),
        fetchone=True
    )  # Obtiene datos actuales del usuario

    return render_template('usuario/perfil.html', usuario=user_data)  # Renderiza perfil


@usuario_bp.route('/servicios')  # Ruta para ver servicios disponibles
@role_required('usuario')  # Acceso restringido a usuarios
def servicios():  # Función de servicios

    search = request.args.get('search', '')  # Obtiene término de búsqueda si existe

    if search:  # Si hay búsqueda
        query = """
            SELECT * FROM servicio
            WHERE estado = 'Activo'
            AND (nombre LIKE %s OR descripcion LIKE %s)
        """  # Query filtrada

        servicios_list = DBController.query(
            query,
            (f"%{search}%", f"%{search}%"),
            fetchall=True
        )  # Ejecuta búsqueda filtrada

    else:
        servicios_list = DBController.query(
            "SELECT * FROM servicio WHERE estado = 'Activo'",
            fetchall=True
        )  # Lista todos los servicios activos

    return render_template(
        'usuario/servicios.html',
        servicios=servicios_list,
        search=search
    )  # Renderiza vista


@usuario_bp.route('/problemas', methods=['GET', 'POST'])  # Ruta para reportar problemas
@role_required('usuario')  # Solo usuarios autenticados
def problemas():  # Función de reportes

    uid = session['user_id']  # ID del usuario

    if request.method == 'POST':  # Si envía formulario
        titulo = request.form.get('titulo')  # Título del problema
        descripcion = request.form.get('descripcion')  # Descripción
        id_servicio = request.form.get('id_servicio')  # Servicio relacionado
        id_ubicacion = request.form.get('id_ubicacion')  # Ubicación seleccionada
        
        fecha_actual = datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # Timestamp del reporte

        # LÓGICA DE UBICACIÓN MANUAL ("OTRO")
        if id_ubicacion == 'otro':  # Si el usuario escribió ubicación manual
            nueva_ub = request.form.get('nueva_ubicacion')  # Nueva ubicación

            if nueva_ub:  # Si existe valor
                DBController.query(
                    """
                    INSERT INTO ubicacion (nombre, direccion, descripcion)
                    VALUES (%s, 'Ingresada por usuario', 'Añadida desde reportes')
                    """,
                    (nueva_ub,),
                    commit=True
                )  # Inserta ubicación personalizada

                last_ub_res = DBController.query(
                    "SELECT LAST_INSERT_ID() as last_id",
                    fetchone=True
                )  # Obtiene último ID insertado

                id_ubicacion = last_ub_res['last_id'] if last_ub_res else None  # Guarda ID generado
            else:
                id_ubicacion = None  # Si no hay valor, se anula

        if id_servicio == '':  # Normaliza campo vacío
            id_servicio = None

        DBController.query(
            """
            INSERT INTO problema (id_usuario, titulo, descripcion, estado, fecha_reporte)
            VALUES (%s, %s, %s, 'Pendiente', %s)
            """,
            (uid, titulo, descripcion, fecha_actual),
            commit=True
        )  # Inserta problema principal

        if id_servicio:  # Si hay servicio asociado
            last_id_res = DBController.query(
                "SELECT LAST_INSERT_ID() as last_id",
                fetchone=True
            )  # Obtiene ID del problema recién creado

            prob_id = last_id_res['last_id'] if last_id_res else None  # Extrae ID

            if prob_id:  # Inserta relación en tabla intermedia
                DBController.query(
                    "INSERT INTO problema_servicio (id_problema, id_servicio) VALUES (%s, %s)",
                    (prob_id, id_servicio),
                    commit=True
                )

        flash('Reporte de problema enviado correctamente.', 'success')  # Mensaje de éxito
        return redirect(url_for('usuario.problemas'))  # Redirige al listado

    mis_problemas = DBController.query(
        """
        SELECT p.*, s.nombre as servicio_nombre
        FROM problema p
        LEFT JOIN problema_servicio ps ON p.id_problema = ps.id_problema
        LEFT JOIN servicio s ON ps.id_servicio = s.id_servicio
        WHERE p.id_usuario = %s
        ORDER BY p.fecha_reporte DESC
        """,
        (uid,),
        fetchall=True
    )  # Historial del usuario

    servicios_disponibles = DBController.query(
        "SELECT id_servicio, nombre FROM servicio WHERE estado = 'Activo'",
        fetchall=True
    )  # Servicios activos

    ubicaciones_disponibles = DBController.query(
        "SELECT id_ubicacion, nombre FROM ubicacion",
        fetchall=True
    )  # Ubicaciones disponibles

    return render_template(
        'usuario/problemas.html',
        problemas=mis_problemas,
        servicios=servicios_disponibles,
        ubicaciones=ubicaciones_disponibles
    )  # Renderiza vista


@usuario_bp.route('/sugerencias', methods=['GET', 'POST'])  # Ruta sugerencias
@role_required('usuario')  # Solo usuarios
def sugerencias():  # Función sugerencias

    uid = session['user_id']  # ID usuario

    if request.method == 'POST':  # Si envía formulario
        titulo = request.form.get('titulo')  # Título
        descripcion = request.form.get('descripcion')  # Descripción

        fecha_actual = datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # Fecha actual

        DBController.query(
            """
            INSERT INTO sugerencia (id_usuario, titulo, descripcion, fecha)
            VALUES (%s, %s, %s, %s)
            """,
            (uid, titulo, descripcion, fecha_actual),
            commit=True
        )  # Inserta sugerencia

        flash('Sugerencia enviada, ¡Gracias por tu aporte verde!', 'success')  # Mensaje
        return redirect(url_for('usuario.sugerencias'))  # Redirige

    mis_sug = DBController.query(
        "SELECT * FROM sugerencia WHERE id_usuario = %s ORDER BY fecha DESC",
        (uid,),
        fetchall=True
    )  # Lista sugerencias usuario

    return render_template('usuario/sugerencias.html', sugerencias=mis_sug)  # Renderiza


@usuario_bp.route('/ubicaciones')  # Ruta de ubicaciones
@role_required('usuario')  # Solo usuarios
def ubicaciones():  # Función ubicaciones

    lista = DBController.query("SELECT * FROM ubicacion", fetchall=True)  # Consulta todas ubicaciones

    return render_template('usuario/ubicaciones.html', ubicaciones=lista)  # Renderiza vista