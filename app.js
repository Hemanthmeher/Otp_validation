document.addEventListener("DOMContentLoaded", function () {
    let otpInputs = document.querySelectorAll(".otp-input input");

    otpInputs.forEach((input, index) => {
        input.addEventListener("input", function () {
            // Allow only one digit
            this.value = this.value.replace(/[^0-9]/g, "").substring(0, 1);

            // Move to next input if a number is entered
            if (this.value.length === 1 && index < otpInputs.length - 1) {
                otpInputs[index + 1].focus();
            }
        });

        input.addEventListener("keydown", function (e) {
            // Move back if Backspace is pressed on an empty input
            if (e.key === "Backspace" && this.value.length === 0 && index > 0) {
                otpInputs[index - 1].focus();
            }
        });
    });
});

// Combine OTP inputs before form submission
function combineOTP() {
    let otp = "";
    document.querySelectorAll(".otp-input input").forEach(input => {
        otp += input.value;
    });
    document.getElementById("otp").value = otp; // Store in hidden input
}
