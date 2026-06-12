document.addEventListener('DOMContentLoaded', function() {  // Espera a que el DOM esté completamente cargado antes de ejecutar el script

    const selectUbicacion = document.getElementById('id_ubicacion');  // Select donde el usuario elige una ubicación
    const contenedorNuevaUbicacion = document.getElementById('contenedor-nueva-ubicacion');  // Contenedor del input "nueva ubicación"
    const inputNuevaUbicacion = document.getElementById('nueva_ubicacion');  // Input para escribir una ubicación personalizada

    // Verifica que todos los elementos existan en la página antes de continuar
    if (selectUbicacion && contenedorNuevaUbicacion && inputNuevaUbicacion) {

        selectUbicacion.addEventListener('change', function() {  // Detecta cambios en el select de ubicación

            if (this.value === 'otro') {  // Si el usuario selecciona "otro"

                // Muestra el campo de nueva ubicación
                contenedorNuevaUbicacion.classList.remove('d-none');  // Elimina clase Bootstrap que lo oculta

                // Hace obligatorio el campo de nueva ubicación
                inputNuevaUbicacion.setAttribute('required', 'required');  // Activa validación HTML

                inputNuevaUbicacion.focus();  // Coloca el cursor automáticamente en el input

            } else {  // Si selecciona cualquier otra opción

                // Oculta el campo de nueva ubicación
                contenedorNuevaUbicacion.classList.add('d-none');  // Agrega clase para ocultarlo

                // Desactiva la validación obligatoria
                inputNuevaUbicacion.removeAttribute('required');  // Quita atributo required

                // Limpia el valor del input
                inputNuevaUbicacion.value = '';  // Evita enviar datos residuales
            }
        });
    }
});