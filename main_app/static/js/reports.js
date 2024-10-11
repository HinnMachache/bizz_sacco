// JavaScript functionality for dropdown menu toggle
function toggleDropdown() {
    const dropdownMenu = document.getElementById('dropdownMenu');
    
    // Toggle the display of the dropdown menu
    if (dropdownMenu.style.display === 'block') {
        dropdownMenu.style.display = 'none';
    } else {
        dropdownMenu.style.display = 'block';
    }
}

// Close dropdown if clicked outside
document.addEventListener('click', function (event) {
    const dropdownMenu = document.getElementById('dropdownMenu');
    const profileIcon = document.querySelector('.profile-icon');
    
    // Check if the click was outside of the dropdown and profile icon
    if (!profileIcon.contains(event.target) && !dropdownMenu.contains(event.target)) {
        dropdownMenu.style.display = 'none';
    }
});


document.addEventListener('DOMContentLoaded', () => {
    // Total Loans Chart
    const totalLoansChart = new Chart(document.getElementById('totalLoansChart'), {
        type: 'bar',
        data: {
            labels: ['January', 'February', 'March', 'April', 'May', 'June'],
            datasets: [{
                label: 'Total Loans',
                data: [10, 15, 8, 12, 20, 18],
                backgroundColor: 'rgba(75, 192, 192, 0.2)',
                borderWidth: 1,
                borderColor: 'rgba(75, 192, 192, 1)',
                hoverBackgroundColor: '#66bb6a',
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    display: true,
                    position: 'top',
                },
                tooltip: {
                    enabled: true,
                    backgroundColor: '#333',
                    titleColor: '#fff',
                    bodyColor: '#fff'
                }
            }
        }
    });

    // Members Growth Chart
    const membersGrowthChart = new Chart(document.getElementById('membersGrowthChart'), {
        type: 'line',
        data: {
            labels: ['January', 'February', 'March', 'April', 'May', 'June'],
            datasets: [{
                label: 'New Members',
                data: [5, 10, 15, 20, 25, 30],
                borderColor: '#2196f3',
                fill: true,
                backgroundColor: 'rgba(33, 150, 243, 0.2)',
                tension: 0.4,
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    display: true,
                    position: 'top',
                },
                tooltip: {
                    enabled: true,
                    backgroundColor: '#333',
                    titleColor: '#fff',
                    bodyColor: '#fff'
                }
            }
        }
    });

    // Revenue Chart
    const revenueChart = new Chart(document.getElementById('revenueChart'), {
        type: 'doughnut',
        data: {
            labels: ['Loan Interest', 'Membership Fees', 'Fines', 'Other'],
            datasets: [{
                data: [55, 25, 10, 10],
                backgroundColor: ['rgba(54, 162, 235, 0.6)', 'rgba(75, 192, 192, 0.6)','rgba(153, 102, 255, 0.6)', '#4bc0c0'],
                hoverOffset: 10,
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    display: true,
                    position: 'top',
                },
                tooltip: {
                    enabled: true,
                    backgroundColor: '#333',
                    titleColor: '#fff',
                    bodyColor: '#fff'
                }
            }
        }
    });

    // Loan Approval vs. Rejection Chart
    const loanStatusChart = new Chart(document.getElementById('loanStatusChart'), {
        type: 'pie',
        data: {
            labels: ['Approved', 'Rejected'],
            datasets: [{
                data: [75, 25],
                backgroundColor: ['rgba(54, 162, 235, 0.6)', 'rgba(153, 102, 255, 0.6)'],
                hoverOffset: 8,
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    display: true,
                    position: 'top',
                },
                tooltip: {
                    enabled: true,
                    backgroundColor: '#333',
                    titleColor: '#fff',
                    bodyColor: '#fff'
                }
            }
        }
    });
});
