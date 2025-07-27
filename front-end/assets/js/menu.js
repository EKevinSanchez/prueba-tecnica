/*del ul con el id sidebarnav verificar desde la cookie el tipo de usuario y de los elementos li 
del menu que tenga la propiedad data-tipo-trabajador mostrar o no el elemento dependiendo del tipo de usuario*/
$(document).ready(function() {
    // Obtener los datos de la cookie datos_usuario
    const cookies = document.cookie.split(';');
    const datosUsuarioCookie = cookies.find(cookie => cookie.trim().startsWith('datos_usuario='));
    
    if (datosUsuarioCookie) {
        const datosUsuario = JSON.parse(decodeURIComponent(datosUsuarioCookie.split('=')[1]));
        
        // Verificar el tipo de usuario y mostrar/ocultar elementos del menú
        const tipoUsuario = datosUsuario.tipo_usuario; // Asumiendo que tipo_usuario es un número que identifica el tipo de usuario
        
        $('#sidebarnav li[data-tipo-trabajador]').each(function() {
        const tipoTrabajador = $(this).data('tipo-trabajador');
        if (tipoTrabajador !== tipoUsuario) {
            $(this).hide(); // Ocultar el elemento si no coincide con el tipo de usuario
        }
        });
    }
});
