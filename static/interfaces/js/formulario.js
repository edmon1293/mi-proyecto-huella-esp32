$(document).ready(function() {
    // Función para actualizar la etiqueta del input de archivo
    $('.custom-file-input').on('change', function() {
        var fileName = $(this).val().split('\\').pop();
        $(this).next('.custom-file-label').addClass("selected").html(fileName);
        
        // Validar el archivo
        validateFile(this);
    });

    // Agregar clase 'filled' al campo de teléfono cuando tenga contenido
    $('#telefono').on('input', function() {
        if ($(this).val().trim() !== '') {
            $(this).addClass('filled');
        } else {
            $(this).removeClass('filled');
        }
    });

    // Función para cambiar el color de fondo al escribir en las casillas
    $('input[type="text"], input[type="tel"], input[type="file"]').on('input', function() {
        if ($(this).val().trim() !== '') {
            $(this).addClass('filled');
        } else {
            $(this).removeClass('filled');
        }
    });

    // Animación de entrada y escritura de etiquetas
    $('.form-group').each(function(index) {
        var $formGroup = $(this);
        setTimeout(function() {
            $formGroup.addClass('visible');
            $formGroup.find('input, select').each(function() {
                var $input = $(this);
                var placeholderText = $input.attr('placeholder');
                if (placeholderText) {
                    $input.attr('placeholder', '');
                    var chars = placeholderText.split('');
                    var index = 0;
                    var interval = setInterval(function() {
                        if (index < chars.length) {
                            $input.attr('placeholder', $input.attr('placeholder') + chars[index]);
                            index++;
                        } else {
                            clearInterval(interval);
                        }
                    }, 100); // Velocidad de escritura rápida (ajustar según sea necesario)
                }
            });
        }, index * 200); // Retraso entre animaciones de cada campo (ajustar según sea necesario)
    });

    // Agregar animación a título y botón después de la animación de los campos
    setTimeout(function() {
        $('h2').addClass('visible');
        $('button[type="submit"]').addClass('visible');
    }, $('.form-group').length * 110 + 400); // Espera un tiempo extra después de la animación de los campos

    // Función para validar los archivos PDF
    function validateFile(input) {
        var file = input.files[0];
        var fileType = file ? file.type : '';
        var fileInputId = $(input).attr('id');
        var valid = fileType === 'application/pdf';

        // Mostrar u ocultar el mensaje de error
        if (!valid) {
            $('#' + fileInputId).addClass('is-invalid');
            $('#error' + fileInputId.charAt(fileInputId.length - 2).toUpperCase() + fileInputId.slice(-1)).show();
        } else {
            $('#' + fileInputId).removeClass('is-invalid');
            $('#error' + fileInputId.charAt(fileInputId.length - 2).toUpperCase() + fileInputId.slice(-1)).hide();
        }
    }

    // Mostrar alerta y redireccionar al enviar el formulario
    $('form').on('submit', function(event) {
        event.preventDefault(); // Prevenir el envío del formulario
        
        var valid = true;

        // Validar los archivos PDF
        $('.custom-file-input').each(function() {
            if (this.files.length > 0) {
                var fileType = this.files[0].type;
                if (fileType !== 'application/pdf') {
                    valid = false;
                    validateFile(this);
                }
            }
        });

        if (!valid) {
            Swal.fire({
                title: "Error",
                text: "Por favor, sube solo archivos PDF.",
                icon: "error",
                confirmButtonText: "OK"
            });
            return;
        }

        // Obtener los valores de los campos del formulario
        var nombre = $('#nombre').val();
        var apellido = $('#apellido').val();
        var domicilio = $('#domicilio').val();
        var codigoPostal = $('#codigoPostal').val();
        var telefono = $('#telefono').val();
        var universidad = $('#universidad').val();
        var carrera = $('#carrera').val();
        
        // Guardar los valores en localStorage
        localStorage.setItem('nombre', nombre);
        localStorage.setItem('apellido', apellido);
        localStorage.setItem('domicilio', domicilio);
        localStorage.setItem('codigoPostal', codigoPostal);
        localStorage.setItem('telefono', telefono);
        localStorage.setItem('universidad', universidad);
        localStorage.setItem('carrera', carrera);

        // Guardar los nombres de los archivos en localStorage
        var ine = $('#inputGroupFile01').val().split('\\').pop();
        var curp = $('#inputGroupFile02').val().split('\\').pop();
        var comprobanteDomicilio = $('#inputGroupFile03').val().split('\\').pop();
        var comprobanteEstudios = $('#inputGroupFile04').val().split('\\').pop();

        localStorage.setItem('ine', ine);
        localStorage.setItem('curp', curp);
        localStorage.setItem('comprobanteDomicilio', comprobanteDomicilio);
        localStorage.setItem('comprobanteEstudios', comprobanteEstudios);
        
        Swal.fire({
            title: "¡Tu Información Fue Recibida!",
            text: "¡Ahora eres parte de Archysoft!",
            icon: "success",
            confirmButtonText: "OK"
        }).then(function() {
            window.location.href = "/usuario/"; // Redirigir a usuario.html
        });
    });
});
