window.addEventListener("load", function () {
    // Get otp container
    
    const OTPContainer = document.querySelector("#otp-input");

    const OTPValueContainer = document.querySelector("#otp-value");

    const continueButton = document.querySelector("#submit");
    const alertContainer = document.querySelector(".alert");
    
    continueButton.addEventListener("click", (e) => {
        e.preventDefault();  // Prevent the form from submitting
        updateValue(inputs);

        $.ajax({
            url: 'http://127.0.0.1:8000/auth/otp/', 
            type: 'POST', 
            data: {
                'code': OTPValueContainer.value,
                csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
            },
            success: function(response) {
                let userMessage = response.message;
                if (userMessage === 'error') {
                    // Update the alert to show the error message
                    alertContainer.innerHTML = response.error; // Display the error message
                } else {
                    // Redirect if success
                    window.location.href = 'http://127.0.0.1:8000/auth/home-page/';
                }
            },
            error: function(xhr, status, error) {
                console.error('Error:', error);
                // Handle errors that occur during the AJAX request itself
                // Optionally, show a user-friendly message
                alertContainer.classList.remove('alert-success');
                alertContainer.classList.add('alert-danger');
                alertContainer.innerHTML = 'An unexpected error occurred. Please try again.'; // Generic error message
            }
        });
    });

    // Focus first input
    const firstInput = OTPContainer.querySelector("input");
    firstInput.focus();

    // OTP Logic

    const updateValue = (inputs) => {
        OTPValueContainer.value = Array.from(inputs).reduce((acc, curInput) => acc.concat(curInput.value ? curInput.value : "*"), "");
    };

    const isValidInput = (inputValue) => {
        return Number(inputValue) === 0 && inputValue !== "0" ? false : true;
    };

    const setInputValue = (inputElement, inputValue) => {
        inputElement.value = inputValue;
    };

    const resetInput = (inputElement) => {
        setInputValue(inputElement, "");
    };

    const focusNext = (inputs, curIndex) => {
        const nextElement = curIndex < inputs.length - 1 ? inputs[curIndex + 1] : inputs[curIndex];

        nextElement.focus();
        nextElement.select();
    };

    const focusPrev = (inputs, curIndex) => {
        const prevElement = curIndex > 0 ? inputs[curIndex - 1] : inputs[curIndex];

        prevElement.focus();
        prevElement.select();
    };

    const focusIndex = (inputs, index) => {
        const element = index < inputs.length - 1 ? inputs[index] : inputs[inputs.length - 1];

        element.focus();
        element.select();
    };

    const handleValidMultiInput = (inputElement, inputValue, curIndex, inputs) => {
        const inputLength = inputValue.length;
        const numInputs = inputs.length;

        const endIndex = Math.min(curIndex + inputLength - 1, numInputs - 1);
        const inputsToChange = Array.from(inputs).slice(curIndex, endIndex + 1);
        inputsToChange.forEach((input, index) => setInputValue(input, inputValue[index]));
        focusIndex(inputs, endIndex);
    };

    const handleInput = (inputElement, inputValue, curIndex, inputs) => {
        if (!isValidInput(inputValue)) return handleInvalidInput(inputElement);
        if (inputValue.length === 1) handleValidSingleInput(inputElement, inputValue, curIndex, inputs);
        else handleValidMultiInput(inputElement, inputValue, curIndex, inputs);
    };

    const handleValidSingleInput = (inputElement, inputValue, curIndex, inputs) => {
        setInputValue(inputElement, inputValue.slice(-1));
        focusNext(inputs, curIndex);
    };

    const handleInvalidInput = (inputElement) => {
        resetInput(inputElement);
    };

    const handleKeyDown = (event, key, inputElement, curIndex, inputs) => {
        if (key === "Delete") {
            resetInput(inputElement);
            focusPrev(inputs, curIndex);
        }
        if (key === "ArrowLeft") {
            event.preventDefault();
            focusPrev(inputs, curIndex);
        }
        if (key === "ArrowRight") {
            event.preventDefault();
            focusNext(inputs, curIndex);
        }
    };

    const handleDelete = (inputElement, curIndex, inputs) => {};

    const handleKeyUp = (event, key, inputElement, curIndex, inputs) => {
        if (key === "Backspace") focusPrev(inputs, curIndex);
    };

    const inputs = OTPContainer.querySelectorAll("input:not(#otp-value)");
    inputs.forEach((input, index) => {
        input.addEventListener("input", (e) => handleInput(input, e.target.value, index, inputs));

        input.addEventListener("keydown", (e) => handleKeyDown(e, e.key, input, index, inputs));

        input.addEventListener("keyup", (e) => handleKeyUp(e, e.key, input, index, inputs));

        input.addEventListener("focus", (e) => e.target.select());
    });
});
