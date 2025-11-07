document.addEventListener('DOMContentLoaded', function() {
    var nombre = localStorage.getItem('nombre') || "Nombre no disponible";
    var apellido = localStorage.getItem('apellido') || "Apellido no disponible";
    var domicilio = localStorage.getItem('domicilio') || "Domicilio no disponible";
    var codigoPostal = localStorage.getItem('codigoPostal') || "C.P. no disponible";
    var telefono = localStorage.getItem('telefono') || "Teléfono no disponible";
    var universidad = localStorage.getItem('universidad') || "Universidad no disponible";
    var carrera = localStorage.getItem('carrera') || "Carrera no disponible";
    var ine = localStorage.getItem('ine') || "No subido";
    var curp = localStorage.getItem('curp') || "No subido";
    var comprobanteDomicilio = localStorage.getItem('comprobanteDomicilio') || "No subido";
    var comprobanteEstudios = localStorage.getItem('comprobanteEstudios') || "No subido";
    
    document.querySelector('.profile-info h2').textContent = `${nombre} ${apellido}`;
    document.querySelector('.profile-info p').textContent = domicilio;

    var infoContainer = document.querySelector('.profile-info');
    var additionalInfo = `
        <p>Teléfono: ${telefono}</p>
        <p>Universidad: ${universidad}</p>
        <p>Carrera: ${carrera}</p>
        <p>INE: ${ine}</p>
        <p>CURP: ${curp}</p>
        <p>Comprobante de Domicilio: ${comprobanteDomicilio}</p>
        <p>Comprobante de Estudios: ${comprobanteEstudios}</p>
    `;
    infoContainer.insertAdjacentHTML('beforeend', additionalInfo);

    // Funcionalidad para la subida de imagen
    var imageUploadInput = document.getElementById('imageUpload');
    var imageContainer = document.getElementById('imageContainer');
    var profileImage = document.getElementById('profileImage');

    imageContainer.addEventListener('click', function() {
        imageUploadInput.click();
    });

    imageUploadInput.addEventListener('change', function(event) {
        var file = event.target.files[0];
        if (file) {
            var reader = new FileReader();
            reader.onload = function(e) {
                profileImage.src = e.target.result;
            };
            reader.readAsDataURL(file);
        }
    });
});
