// Función para validar email
function validateEmail(email) {
    let missingChars = [];
    if (!email.includes("@")) {
        missingChars.push("@");
    }
    if (!email.includes(".")) {
        missingChars.push(".com");
    }
    return missingChars;
}

// Función para validar contraseña
function validatePassword(password) {
    let missingChars = [];

    // Validar longitud mínima de 8 caracteres
    if (password.length < 8) {
        missingChars.push("Min 8 caracteres");
    }

    // Validar caracteres numéricos
    if (!password.match(/\d/)) {
        missingChars.push("numéricos");
    }

    // Validar letras minúsculas
    if (!password.match(/[a-z]/)) {
        missingChars.push("minúsculas");
    }

    // Validar letras mayúsculas
    if (!password.match(/[A-Z]/)) {
        missingChars.push("mayúsculas");
    }

    // Validar caracteres especiales
    if (!password.match(/[!@#$%^&*(),.?":{}|<>]/)) {
        missingChars.push("!@#$%^&*");
    }

    return missingChars;
}

// Función para evaluar la seguridad de la contraseña
function evaluatePasswordStrength(password) {
    let strength = "Débil";
    let strengthColor = "red";
    let criteriaMet = 0;

    // Validar longitud mínima de 8 caracteres
    if (password.length >= 8) criteriaMet++;

    // Validar letras minúsculas
    if (password.match(/[a-z]/)) criteriaMet++;

    // Validar letras mayúsculas
    if (password.match(/[A-Z]/)) criteriaMet++;

    // Validar caracteres numéricos
    if (password.match(/\d/)) criteriaMet++;

    // Validar caracteres especiales
    if (password.match(/[!@#$%^&*(),.?":{}|<>]/)) criteriaMet++;

    // Evaluar la cantidad de criterios cumplidos
    if (criteriaMet === 5) {
        strength = "Segura";
        strengthColor = "green";
    } else if (criteriaMet >= 3) {
        strength = "Media";
        strengthColor = "#ffc107"; // Amarillo más suave y normal
    }

    return { strength, strengthColor };
}

// Evento para actualizar la barra de seguridad de la contraseña
function updatePasswordStrength() {
    var password = document.getElementById("registerPassword").value;
    var passwordStrengthBar = document.getElementById("passwordStrengthBar");
    var passwordStrengthText = document.getElementById("passwordStrengthText");

    var { strength, strengthColor } = evaluatePasswordStrength(password);

    passwordStrengthBar.style.width = strength === "Débil" ? "33%" : strength === "Media" ? "66%" : "100%";
    passwordStrengthBar.style.backgroundColor = strengthColor;
    passwordStrengthText.textContent = strength;
    passwordStrengthText.style.color = strengthColor;
}

// Función para manejar el inicio de sesión
function handleLogin(event) {
    event.preventDefault();

    var email = document.getElementById("email").value;
    var emailError = document.getElementById("emailError");
    var missingChars = validateEmail(email);

    if (missingChars.length > 0) {
        emailError.textContent = `Mmm... verifica que contenga "${missingChars.join(", ")}"`;
        return;
    } else {
        emailError.textContent = "";
    }

    var password = document.getElementById("password").value;
    var passwordError = document.getElementById("passwordError");
    var missingPasswordChars = validatePassword(password);

    if (missingPasswordChars.length > 0) {
        passwordError.textContent = `La contraseña no contiene "${missingPasswordChars.join(", ")}"`;
        return;
    } else {
        passwordError.textContent = "";
    }

    // Aquí se podría usar AJAX para enviar el formulario y manejar la respuesta
    Swal.fire({
        title: "¡Felicidades!",
        text: "¡El inicio de tu correo fue un éxito!",
        icon: "success",
        confirmButtonText: "OK"
    }).then(function() {
        // Redireccionar a otra página HTML después de cerrar SweetAlert
        window.location.href = "/formulario/";
    });
}

// Función para manejar el registro
function handleRegister(event) {
    event.preventDefault();

    var email = document.getElementById("registerEmail").value;
    var emailError = document.getElementById("registerEmailError");
    var missingChars = validateEmail(email);

    if (missingChars.length > 0) {
        emailError.textContent = `Mmm... verifica que contenga "${missingChars.join(", ")}"`;
        return;
    } else {
        emailError.textContent = "";
    }

    var password = document.getElementById("registerPassword").value;
    var passwordError = document.getElementById("registerPasswordError");
    var missingPasswordChars = validatePassword(password);

    if (missingPasswordChars.length > 0) {
        passwordError.textContent = `No contiene caracteres "${missingPasswordChars.join(", ")}"`;
        return;
    } else {
        passwordError.textContent = "";
    }

    Swal.fire({
        title: "¡Felicidades!",
        text: "¡Estas a un paso de formar parte de Archysoft!",
        icon: "success",
        confirmButtonText: "OK"
    }).then(function() {
        document.getElementById('registerFormContainer').classList.add('hidden');
        document.getElementById('loginFormContainer').classList.remove('hidden');
        document.getElementById('loginImage').src = '/static/interfaces/img/bugs bunny wallpaper.jpg';
    });

    document.getElementById("registerEmail").value = "";
    document.getElementById("registerPassword").value = "";
}

// Evento para cambiar entre texto y contraseña
function togglePassword(fieldId) {
    var passwordField = document.getElementById(fieldId);
    if (passwordField.type === "password") {
        passwordField.type = "text";
    } else {
        passwordField.type = "password";
    }
}

// Evento para abrir el formulario de registro
document.getElementById('createAccountLink').addEventListener('click', function(event) {
    event.preventDefault();

    document.querySelector('.login-content').style.transform = 'translateX(-100%)';

    setTimeout(function() {
        document.querySelector('.login-content').style.transform = 'translateX(100%)';

        setTimeout(function() {
            document.getElementById('loginFormContainer').classList.add('hidden');
            document.getElementById('registerFormContainer').classList.remove('hidden');
            document.getElementById('registerFormContainer').innerHTML = `
                <h2>Crea tu cuenta</h2>
                <form id="registerForm" onsubmit="handleRegister(event)">
                    <label for="registerEmail">Email:</label>
                    <input type="text" id="registerEmail" name="email" required>
                    <span id="registerEmailError" class="error-message"></span>

                    <label for="registerPassword">Contraseña:</label>
                    <input type="password" id="registerPassword" name="password" required oninput="updatePasswordStrength()">
                    <input type="checkbox" onclick="togglePassword('registerPassword')"> Mostrar contraseña
                    <span id="registerPasswordError" class="error-message"></span>

                    <div class="password-strength">
                        <div id="passwordStrengthBar" style="width: 0; height: 5px; background-color: red;"></div>
                    </div>
                    <span id="passwordStrengthText" class="password-strength-text">Débil</span>

                    <button type="submit" id="registerButton">Registrarse</button>
                </form>
            `;
            document.getElementById('loginImage').src = "/static/interfaces/img/log.jpg";

            document.querySelector('.login-content').style.transform = 'translateX(0)';
        }, 500);
    }, 500);
});
