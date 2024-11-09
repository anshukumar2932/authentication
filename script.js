// Redirect to login page
function redirectToLogin() {
    window.location.href = "login.html";
}

// Toggle Password Visibility
function togglePassword(inputId) {
    const passwordField = document.getElementById(inputId);
    if (passwordField.type === "password") {
        passwordField.type = "text";
    } else {
        passwordField.type = "password";
    }
}

// Form Validation
document.getElementById('signupForm').addEventListener('submit', function (event) {
    event.preventDefault();
    validateSignupForm();
});

document.getElementById('loginForm').addEventListener('submit', function (event) {
    event.preventDefault();
    validateLoginForm();
});

function validateSignupForm() {
    const emailOrPhone = document.getElementById('emailOrPhone').value;
    const password = document.getElementById('password').value;
    let isValid = true;

    // Validate email or phone
    if (!validateEmailOrPhone(emailOrPhone)) {
        showError('emailOrPhoneError', 'Invalid email or mobile number');
        isValid = false;
    } else {
        hideError('emailOrPhoneError');
    }

    // Validate password
    if (password === '') {
        showError('passwordError', 'Password cannot be empty');
        isValid = false;
    } else {
        hideError('passwordError');
    }

    if (isValid) {
        alert('Sign up successful!');
        // Proceed further
    }
}

function validateLoginForm() {
    const emailOrPhone = document.getElementById('loginEmailOrPhone').value;
    const password = document.getElementById('loginPassword').value;
    let isValid = true;

    // Validate email or phone
    if (!validateEmailOrPhone(emailOrPhone)) {
        showError('loginEmailOrPhoneError', 'Invalid email or mobile number');
        isValid = false;
    } else {
        hideError('loginEmailOrPhoneError');
    }

    // Validate password
    if (password === '') {
        showError('loginPasswordError', 'Password cannot be empty');
        isValid = false;
    } else {
        hideError('loginPasswordError');
    }

    if (isValid) {
        alert('Login successful!');
        // Proceed further
    }
}

// Validate Email or Phone format
function validateEmailOrPhone(input) {
    const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    const phonePattern = /^\d{10}$/;
    return emailPattern.test(input) || phonePattern.test(input);
}

// Show/Hide Error
function showError(elementId, message) {
    const errorElement = document.getElementById(elementId);
    errorElement.textContent = message;
    errorElement.style.display = 'block';
}

function hideError(elementId) {
    const errorElement = document.getElementById(elementId);
    errorElement.style.display = 'none';
}
