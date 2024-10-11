// Toggle Dropdown Function
function toggleDropdown() {
    const dropdown = document.getElementById('dropdownMenu');
    const isExpanded = dropdown.style.display === 'block';
    dropdown.style.display = isExpanded ? 'none' : 'block';
    // Update ARIA attribute for accessibility
    document.querySelector('button[onclick="toggleDropdown()"]').setAttribute('aria-expanded', !isExpanded);
}

// Sample data for charts
const loanApprovalData = {
    labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
    datasets: [{
        label: 'Loans Approved',
        data: [10, 15, 20, 25, 30, 35],
        borderColor: 'rgba(54, 162, 235, 1)', // Light Blue for line
        backgroundColor: 'rgba(54, 162, 235, 0.2)', // Light Blue for area under the line
    }]
};

const memberGrowthData = {
    labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
    datasets: [{
        label: 'Members Growth',
        data: [100, 110, 120, 130, 140, 150],
        backgroundColor: 'rgba(75, 192, 192, 0.2)', // Aqua for bars
        borderColor: 'rgba(75, 192, 192, 1)', // Aqua for bar borders
        borderWidth: 1
    }]
};

const pendingVsApprovedData = {
    labels: ['Approved', 'Pending'],
    datasets: [{
        label: 'Loan Status',
        data: [25, 5],
        backgroundColor: [
            'rgba(54, 162, 235, 0.6)', // Light Blue
            'rgba(75, 192, 192, 0.6)'  // Aqua
        ],
        hoverOffset: 4
    }]
};

const userEngagementData = {
    labels: ['Daily Logins', 'Active Users', 'New Registrations'],
    datasets: [{
        label: 'User Engagement',
        data: [50, 75, 10],
        backgroundColor: [
            'rgba(54, 162, 235, 0.6)', // Light Blue
            'rgba(75, 192, 192, 0.6)',  // Aqua
            'rgba(153, 102, 255, 0.6)' // Purple
        ],
        hoverOffset: 4
    }]
};

// Function to create charts
function createChart(ctx, type, data) {
    return new Chart(ctx, {
        type: type,
        data: data,
        options: {
            responsive: true,
            maintainAspectRatio: false,
            tooltips: {
                mode: 'index',
                intersect: false,
            },
        }
    });
}

// Initialize charts
const loanApprovalChartCtx = document.getElementById('loanApprovalChart').getContext('2d');
const memberGrowthChartCtx = document.getElementById('memberGrowthChart').getContext('2d');
const pendingVsApprovedChartCtx = document.getElementById('pendingVsApprovedChart').getContext('2d');
const userEngagementChartCtx = document.getElementById('userEngagementChart').getContext('2d');

// Create charts with consistent sizes and styles
createChart(loanApprovalChartCtx, 'line', loanApprovalData);
createChart(memberGrowthChartCtx, 'bar', memberGrowthData);
createChart(pendingVsApprovedChartCtx, 'doughnut', pendingVsApprovedData);
createChart(userEngagementChartCtx, 'doughnut', userEngagementData);
