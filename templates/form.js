const signUpButton = document.getElementById('signUp');
const signInButton = document.getElementById('signIn');
const container = document.getElementById('container');

signUpButton.addEventListener('click', () =>
    container.classList.add('right-panel-active'));

signInButton.addEventListener('click', () =>
    container.classList.remove('right-panel-active'));

// Add this to your existing JavaScript code
document.getElementById('instructionsButton').addEventListener('click', function() {
    var instructionBox = document.getElementById('instructionBox');
    instructionBox.style.display = 'block';
});

document.getElementById('closeButton').addEventListener('click', function() {
    var instructionBox = document.getElementById('instructionBox');
    instructionBox.style.display = 'none';
});
