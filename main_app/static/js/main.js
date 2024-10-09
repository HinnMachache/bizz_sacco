// JavaScript to detect the current page and highlight the active link
window.onload = function() {
    // Get the current URL path
    const path = window.location.pathname.split("/").pop();

    // Get all sidebar links
    const sidebarLinks = document.querySelectorAll('.sidebar ul li a');

    // Loop through each link
    sidebarLinks.forEach(link => {
        // Get the href attribute of the link
        const href = link.getAttribute('href');

        // Check if the href matches the current path
        if (href === path) {
            // Add 'active' class to the matching link
            link.classList.add('active');
        }
    });
};
// main.js
// main.js

document.addEventListener('DOMContentLoaded', () => {
    // Ensure elements exist before adding event listeners
    const searchInput = document.getElementById('search');
    const sortSelect = document.getElementById('sort');
    const transactionCards = Array.from(document.querySelectorAll('.transaction-card'));

    if (searchInput && sortSelect) {
        // Function to filter and sort transactions
        function filterAndSortTransactions() {
            const searchTerm = searchInput.value.toLowerCase();
            const sortBy = sortSelect.value;

            // Filter transactions
            transactionCards.forEach(card => {
                const name = card.querySelector('.transaction-name').textContent.toLowerCase();
                const shouldDisplay = name.includes(searchTerm);
                card.style.display = shouldDisplay ? 'block' : 'none';
            });

            // Sort transactions
            const sortedCards = transactionCards.filter(card => card.style.display === 'block').sort((a, b) => {
                const aValue = a.querySelector(`.transaction-${sortBy}`).textContent.trim();
                const bValue = b.querySelector(`.transaction-${sortBy}`).textContent.trim();

                if (sortBy === 'date') {
                    return new Date(bValue) - new Date(aValue);
                } else if (sortBy === 'amount') {
                    return parseFloat(bValue.replace(/KES\s|\,/g, '')) - parseFloat(aValue.replace(/KES\s|\,/g, ''));
                } else {
                    return aValue.localeCompare(bValue);
                }
            });

            // Append sorted cards to the list
            const transactionList = document.querySelector('.transaction-list');
            sortedCards.forEach(card => transactionList.appendChild(card));
        }

        // Event listeners
        searchInput.addEventListener('input', filterAndSortTransactions);
        sortSelect.addEventListener('change', filterAndSortTransactions);
    }
});

// Function to display the transaction popup
function showPopup(name, type, date, amount, description) {
    document.getElementById('popup-name').textContent = name;
    document.getElementById('popup-date-value').textContent = date;
    document.getElementById('popup-amount-value').textContent = amount;
    document.getElementById('popup-type-value').textContent = type;
    document.getElementById('popup-description-value').textContent = description;
    document.getElementById('transaction-popup').style.display = 'block';
}

// Function to close the transaction popup
function closePopup() {
    document.getElementById('transaction-popup').style.display = 'none';
}
