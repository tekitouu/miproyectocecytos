document.addEventListener('DOMContentLoaded', function() {  // Espera a que el DOM esté completamente cargado antes de ejecutar el script

    const canvasElement = document.getElementById('graficaPastel');  // Obtiene el canvas donde se dibujará la gráfica

    // Verificamos si el canvas existe en la página actual antes de renderizar
    if (canvasElement) {  // Evita errores si la página no contiene la gráfica

        // Recuperamos los datos inyectados desde Flask mediante atributos data-*
        const usuarios = parseInt(canvasElement.getAttribute('data-usuarios')) || 0;  // Total de usuarios
        const servicios = parseInt(canvasElement.getAttribute('data-servicios')) || 0;  // Total de servicios
        const problemas = parseInt(canvasElement.getAttribute('data-problemas')) || 0;  // Total de incidencias/problemas
        const ubicaciones = parseInt(canvasElement.getAttribute('data-ubicaciones')) || 0;  // Total de ubicaciones
        const sugerencias = parseInt(canvasElement.getAttribute('data-sugerencias')) || 0;  // Total de sugerencias

        const ctx = canvasElement.getContext('2d');  // Contexto 2D del canvas para dibujar

        new Chart(ctx, {  // Crea una nueva gráfica usando Chart.js
            type: 'pie',  // Tipo de gráfica: pastel

            data: {  // Datos de la gráfica
                labels: ['Usuarios', 'Servicios', 'Incidencias', 'Ubicaciones', 'Sugerencias'],  // Etiquetas de cada segmento

                datasets: [{
                    label: 'Cantidad',  // Nombre del dataset
                    data: [usuarios, servicios, problemas, ubicaciones, sugerencias],  // Valores dinámicos

                    backgroundColor: [  // Colores de cada segmento
                        '#212529', // Negro oscuro (Usuarios)
                        '#198754', // Verde (Servicios)
                        '#ffc107', // Amarillo (Incidencias)
                        '#0dcaf0', // Azul (Ubicaciones)
                        '#6c757d'  // Gris (Sugerencias)
                    ],

                    borderWidth: 1  // Grosor del borde de cada segmento
                }]
            },

            options: {  // Configuración visual de la gráfica
                responsive: true,  // Se adapta al tamaño del contenedor
                maintainAspectRatio: false,  // Permite control de tamaño personalizado

                plugins: {
                    legend: {  // Configuración de la leyenda
                        position: 'bottom'  // Ubicación inferior
                    }
                }
            }
        });
    }
});