const loanData = [
    { id: 1, name: 'Personal Loan', amount: 5000, status: 'approved' },
    { id: 2, name: 'Home Loan', amount: 20000, status: 'pending' },
    { id: 3, name: 'Car Loan', amount: 15000, status: 'approved' },
    { id: 4, name: 'Education Loan', amount: 8000, status: 'rejected' },
    { id: 5, name: 'Business Loan', amount: 30000, status: 'approved' },
    { id: 6, name: 'Debt Consolidation', amount: 12000, status: 'pending' },
    { id: 7, name: 'Medical Loan', amount: 6000, status: 'approved' },
    { id: 8, name: 'Travel Loan', amount: 4000, status: 'rejected' },
    { id: 9, name: 'Wedding Loan', amount: 10000, status: 'approved' },
    { id: 10, name: 'Vacation Loan', amount: 7000, status: 'pending' },
];

function renderLoans() {
    const activityLog = document.getElementById('activityLog');
    activityLog.innerHTML = '';
    loanData.forEach(loan => {
        const li = document.createElement('li');
        li.innerHTML = `<span class="activity-item">${loan.name}</span> - <span class="activity-amount">KSh ${loan.amount.toLocaleString()}</span> (${loan.status})`;
        activityLog.appendChild(li);
    });
}

function openAddLoanModal() {
    document.getElementById('addLoanModal').style.display = 'block';
}

function closeAddLoanModal() {
    document.getElementById('addLoanModal').style.display = 'none';
}

function addLoan(event) {
    event.preventDefault();
    const name = document.getElementById('loanName').value.trim();
    const amount = parseFloat(document.getElementById('loanAmount').value);
    const status = document.getElementById('loanStatus').value.trim();

    // Basic validation
    if (!name || isNaN(amount) || !status) {
        alert('Please fill in all fields correctly.');
        return;
    }

    const newLoan = {
        id: loanData.length + 1,
        name,
        amount,
        status
    };
    loanData.push(newLoan);
    renderLoans();
    updateCharts();
    closeAddLoanModal();
}

// Chart.js Initialization
const ctx1 = document.getElementById('loanStatusChart').getContext('2d');
const loanStatusChart = new Chart(ctx1, {
    type: 'pie',
    data: {
        labels: ['Approved', 'Pending', 'Rejected'],
        datasets: [{
            label: 'Loan Status',
            data: getLoanStatusCounts(),
            backgroundColor: ['rgba(54, 162, 235, 0.6)', 'rgba(75, 192, 192, 0.6)','rgba(153, 102, 255, 0.6)'],
        }]
    },
});

const ctx2 = document.getElementById('loanApprovalTrendChart').getContext('2d');
const loanApprovalTrendChart = new Chart(ctx2, {
    type: 'line',
    data: {
        labels: ['January', 'February', 'March', 'April', 'May', 'June'],
        datasets: [{
            label: 'Loan Approvals',
            data: [5, 10, 7, 12, 8, 15], // Sample data
            borderColor: '#4CAF50',
            borderWidth: 2,
            fill: false
        }]
    },
});

// New Chart: Total Loan Amounts
const ctx3 = document.getElementById('totalLoanAmountChart').getContext('2d');
const totalLoanAmountChart = new Chart(ctx3, {
    type: 'bar',
    data: {
        labels: loanData.map(loan => loan.name),
        datasets: [{
            label: 'Loan Amounts',
            data: loanData.map(loan => loan.amount),
            backgroundColor: '#2196F3',
        }]
    },
});

// Update the charts when loans change
function updateCharts() {
    loanStatusChart.data.datasets[0].data = getLoanStatusCounts();
    loanStatusChart.update();

    // Update the total loan amount chart
    totalLoanAmountChart.data.labels = loanData.map(loan => loan.name);
    totalLoanAmountChart.data.datasets[0].data = loanData.map(loan => loan.amount);
    totalLoanAmountChart.update();
}

function getLoanStatusCounts() {
    const approvedCount = loanData.filter(loan => loan.status === 'approved').length;
    const pendingCount = loanData.filter(loan => loan.status === 'pending').length;
    const rejectedCount = loanData.filter(loan => loan.status === 'rejected').length;
    return [approvedCount, pendingCount, rejectedCount];
}

// Render the loans on page load
renderLoans();
