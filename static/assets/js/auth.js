// register section 

document.getElementById('form-auth').addEventListener('submit', function(event) {
    
    // Clear previous errors
    const errorAlert = document.getElementById('error-alert');
    errorAlert.innerHTML = '';
    errorAlert.style.display = 'none'; // Hide the alert initially


    const input = document.getElementById('username').value;
    const password = document.getElementById('password').value;
    const rePasswordElement = document.getElementById('rePassword');



    let errorMessages = [];

    if (rePasswordElement !== null) {
        const rePassword = rePasswordElement.value;

        if (password !== rePassword) {
            errorMessages.push("تکرار کلمه عبور با رمز عبور مغایرت دارد.");
        }
        
    } else {
        // Handle the case where the element does not exist
    }
    
    // Determine the type of input (email or phone number)
    if (validateEmail(input)) {

    } else if (validateAndFormatPhoneNumber(input)) {
    } else {
        errorMessages.push("لطفا یک ایمیل یا شماره معتبر مانند *******0902 وارد کنید.");
    }

    // Validate Password Length
    if (password.length < 8 || password.length > 15) {
        errorMessages.push("رمز باید بین 8 تا 15 کاراکتر باشد.");
    }

    // Validate Password and Re-Password

    if (errorMessages.length > 0) {
        // Show error messages
        errorAlert.innerHTML = errorMessages.join('<br>');
        errorAlert.style.display = 'block'; // Show the alert
        event.preventDefault(); // Prevent form submission if there are errors
    }

});


    // otp login
$(document).ready(function() {
    $("#sms-login-btn").on("click", function(e) {
        e.preventDefault(); 
        
        // Clear previous errors
        const errorAlert = document.getElementById('error-alert');
        errorAlert.innerHTML = '';
        errorAlert.style.display = 'none'; // Hide the alert initially


        const input = document.getElementById('username').value;

        let errorMessages = [];
        
        // Determine the type of input (email or phone number)
        if (validateEmail(input)) {
            // 
        } else if (validateAndFormatPhoneNumber(input)) {
            // 
        } else {
            errorMessages.push("لطفا یک ایمیل یا شماره معتبر مانند *******0902 وارد کنید.");
        }

        if (errorMessages.length > 0) {
            // Show error messages
            errorAlert.innerHTML = errorMessages.join('<br>');
            errorAlert.style.display = 'block'; // Show the alert
            e.preventDefault(); // Prevent form submission if there are errors
        }
        else{
            $.ajax({
                url: 'http://127.0.0.1:8000/auth/otp-generate/', 
                type: 'POST', 
                data: {
                    'username': input,
                    csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
                },
                success: function(response) {
                    let userMessage = response.message;
                    if (userMessage === 'error') {
                        // Display the error message to the user
                        errorMessages.push(response.error);
                        errorAlert.innerHTML = errorMessages.join('<br>');
                        errorAlert.style.display = 'block'; // Show the alert
                        e.preventDefault()
                    } else {
                        // Redirect if success
                        window.location.href = 'http://127.0.0.1:8000/auth/otp/';
                    }
                },
                error: function(xhr, status, error) {
                    console.error('Error:', error);
                    // Handle errors that occur during the AJAX request itself
                    // Optionally, show a user-friendly message
                }
            });
        }
    });
});

function validateEmail(email) {
    const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailPattern.test(email);
}

function validateAndFormatPhoneNumber(phoneNumber) {
    // Remove all non-numeric characters
    const cleanedNumber = phoneNumber.replace(/\D/g, '');

    // Ensure the cleaned number is purely numeric and matches the correct length
    if (cleanedNumber.length !== phoneNumber.length) {
        // The original input contains non-numeric characters
        return false;
    }

    // Match local phone number format (09 followed by 9 digits)
    const localPhonePattern = /^09\d{9}$/;

    // Check if the number starts with a country code and strip it if needed
    const internationalPhonePattern = /^(?:\+98|0)?(\d{10})$/;

    if (localPhonePattern.test(cleanedNumber)) {
        return true;
    }

    const match = internationalPhonePattern.exec(cleanedNumber);
    if (match) {
        const localNumber = '0' + match[1];
        return localPhonePattern.test(localNumber);
    }

    return false;
}