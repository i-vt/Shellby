// theme.js

// Initialize the theme toggle
function initializeTheme() {
    const toggleButton = document.querySelector('.toggle-button');

    // Add a click event listener to the toggle button
    toggleButton.addEventListener('click', toggleTheme);
}

// Toggle between light and dark mode
function toggleTheme() {
    const body = document.body;
    const toggleButton = document.querySelector('.toggle-button');

    // Toggle the 'light-mode' class on the body
    body.classList.toggle('light-mode');

    // Update the button text based on the current mode
    if (body.classList.contains('light-mode')) {
        toggleButton.textContent = 'Switch to Dark Mode';
    } else {
        toggleButton.textContent = 'Switch to Light Mode';
    }
}

