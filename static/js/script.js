// SignupForm Validation
//In Java Script to note, make sure you define all variables correctly and declare any function well before attempting to use it. The javascript will not identify the unused variable for u
const signUpForm = document.getElementById("signupForm"); //Calling the name
const errorElement = document.getElementById('errors');
const emailError = document.querySelector('.error.email-error');
const pwdError = document.querySelector('.error.pwd-error');




signUpForm.addEventListener('submit', (event) => {
    // Retrieve input values when the form is submitted
    event.preventDefault();  //Prevents page refresh on submit (To add on this remember adding a prevent default funciton before the form validation will prevent the form from being submitted twice)
    const firstName = document.getElementById('fname').value;
    const lastName = document.getElementById('lname').value;
    const email = document.getElementById('email').value;
    const password = document.getElementById('pwd').value;
    const passwordRepeat = document.getElementById('pwdRepeat').value;

    function validateEmail(email) {
      var re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
      return re.test(String(email).toLowerCase());//This will ensure the integrity of our database and the user won't be able to create an account if the email written is invalid
    }
  

    // Clear the previous error messages
    errorElement.innerHTML = "";
    emailError.innerHTML = "";
    pwdError.innerHTML = "";

    let messages = [];

    if (!validateEmail(email)){
      messages.push("Invalid email address");
    }

    

    if (firstName === '' || lastName === '' || idNo === '' || policeNumber === '' || email === '' || userId === '' || password === '' || passwordRepeat === '') {
        messages.push('All fields are required');
    }

    // Additional validation logic goes here...
    if (password !== passwordRepeat) {
        messages.push("Password does not match");
    }

    if (messages.length === 0) {
        signUpForm.disabled = true; // Disable form to prevent accidental resubmission
        setTimeout(() => {
          signUpForm.submit(); // Submit the form after a short delay
        }, 1000); // Delay submission by 1 second
      } else {
        // Display error messages
        errorElement.innerHTML = messages.join(', ');
        errorElement.classList.add('error-message');
        errorElement.style.display = 'block';
        event.preventDefault(); // Prevent form submission
      }
});



