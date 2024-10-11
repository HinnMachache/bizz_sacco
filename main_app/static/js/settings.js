// script.js

// Function to toggle the dropdown menu
function toggleDropdown() {
    const dropdown = document.getElementById("dropdownMenu");
    dropdown.classList.toggle("show");
}

// Close the dropdown if clicked outside
window.onclick = function(event) {
    if (!event.target.matches('.profile-icon')) {
        const dropdowns = document.getElementsByClassName("dropdown-menu");
        for (let i = 0; i < dropdowns.length; i++) {
            const openDropdown = dropdowns[i];
            if (openDropdown.classList.contains('show')) {
                openDropdown.classList.remove('show');
            }
        }
    }
};

// Function to handle form submissions (for demonstration)
document.querySelectorAll('.settings-form').forEach(form => {
    form.addEventListener('submit', function(e) {
        e.preventDefault(); // Prevent default form submission
        alert('Settings updated!'); // For demo purposes, show an alert
        // Here, you can handle the form data (e.g., send it to the server)
    });
});
