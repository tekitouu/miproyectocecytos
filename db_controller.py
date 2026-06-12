from flask_mysqldb import MySQL  # Importa la clase MySQL desde Flask-MySQLdb para conectar Flask con MySQL

mysql = MySQL()  # Crea una instancia global de MySQL que será configurada posteriormente en app.py

class DBController:  # Define la clase DBController para centralizar las operaciones con la base de datos
    """Abstracción para ejecutar consultas SQL de manera limpia y segura."""  # Documentación de la clase

    @staticmethod  # Indica que el método puede utilizarse sin crear una instancia de la clase
    def query(sql, args=(), fetchall=False, fetchone=False, commit=False):  # Método genérico para ejecutar consultas SQL
        cursor = mysql.connection.cursor()  # Crea un cursor para interactuar con la base de datos

        try:  # Inicia un bloque para manejar posibles errores durante la ejecución
            cursor.execute(sql, args)  # Ejecuta la consulta SQL utilizando los parámetros recibidos

            if commit:  # Verifica si la consulta requiere guardar cambios en la base de datos
                mysql.connection.commit()  # Confirma permanentemente los cambios realizados
                return cursor.lastrowid if cursor.lastrowid else cursor.rowcount  # Retorna el ID insertado o el número de filas afectadas

            if fetchall:  # Verifica si se deben obtener todos los registros resultantes
                return cursor.fetchall()  # Retorna todos los registros encontrados

            if fetchone:  # Verifica si se debe obtener un único registro
                return cursor.fetchone()  # Retorna el primer registro encontrado

        except Exception as e:  # Captura cualquier excepción que ocurra durante la consulta
            mysql.connection.rollback()  # Revierte los cambios realizados para evitar inconsistencias
            raise e  # Lanza nuevamente la excepción para que pueda ser manejada externamente

        finally:  # Se ejecuta siempre, ocurra o no un error
            cursor.close()  # Cierra el cursor para liberar recursos y evitar fugas de memoria