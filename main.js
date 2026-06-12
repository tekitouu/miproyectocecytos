// Desvanecimiento automático de los mensajes Flash informativos de Flask
document.addEventListener("DOMContentLoaded", function() {  // Espera a que el DOM esté completamente cargado

    setTimeout(function() {  // Ejecuta la función después de 4 segundos (4000 ms)

        let alerts = document.querySelectorAll('.alert');  // Selecciona todos los elementos con clase "alert" (mensajes flash)

        alerts.forEach(function(alert) {  // Recorre cada alerta encontrada

            let bsAlert = new bootstrap.Alert(alert);  // Crea una instancia de Bootstrap Alert para controlarla programáticamente

            bsAlert.close();  // Cierra la alerta con animación de Bootstrap (fade out)
        });

    }, 4000);  // Tiempo de espera antes de cerrar automáticamente los mensajes
});