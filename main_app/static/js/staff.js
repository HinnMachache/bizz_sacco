const staffMembers = [
    { id: 1, name: 'Alice Brown', email: 'alice@example.com', position: 'Manager', status: 'active' },
    { id: 2, name: 'Bob White', email: 'bob@example.com', position: 'Developer', status: 'inactive' },
    { id: 3, name: 'Charlie Black', email: 'charlie@example.com', position: 'Designer', status: 'active' },
    { id: 4, name: 'David Green', email: 'david@example.com', position: 'Marketing', status: 'inactive' },
    { id: 5, name: 'Eve Blue', email: 'eve@example.com', position: 'Sales', status: 'active' },
    { id: 6, name: 'Frank Yellow', email: 'frank@example.com', position: 'HR', status: 'active' },
    { id: 7, name: 'Grace Red', email: 'grace@example.com', position: 'Admin', status: 'inactive' },
    { id: 8, name: 'Hank Orange', email: 'hank@example.com', position: 'Support', status: 'active' },
];

function renderStaff() {
    const staffBody = document.getElementById('staffBody');
    staffBody.innerHTML = '';
    staffMembers.forEach(member => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${member.name}</td>
            <td>${member.email}</td>
            <td>${member.position}</td>
            <td><span class="status ${member.status}">${member.status.charAt(0).toUpperCase() + member.status.slice(1)}</span></td>
            <td>
                <button class="action-button" onclick="viewStaff(${member.id})"><i class="fas fa-eye"></i> View</button>
            </td>
        `;
        staffBody.appendChild(row);
    });
}

function filterStaff() {
    const searchInput = document.getElementById('search').value.toLowerCase();
    const filteredStaff = staffMembers.filter(member => 
        member.name.toLowerCase().includes(searchInput) ||
        member.email.toLowerCase().includes(searchInput)
    );
    renderFilteredStaff(filteredStaff);
}

function renderFilteredStaff(filteredStaff) {
    const staffBody = document.getElementById('staffBody');
    staffBody.innerHTML = '';
    filteredStaff.forEach(member => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${member.name}</td>
            <td>${member.email}</td>
            <td>${member.position}</td>
            <td><span class="status ${member.status}">${member.status.charAt(0).toUpperCase() + member.status.slice(1)}</span></td>
            <td>
                <button class="action-button" onclick="viewStaff(${member.id})"><i class="fas fa-eye"></i> View</button>
            </td>
        `;
        staffBody.appendChild(row);
    });
}

function viewStaff(id) {
    // Logic to view staff details
}

function openAddStaffModal() {
    document.getElementById('addStaffModal').style.display = 'block';
}

function closeAddStaffModal() {
    document.getElementById('addStaffModal').style.display = 'none';
}

function addStaff(event) {
    event.preventDefault();
    const name = document.getElementById('staffName').value;
    const email = document.getElementById('staffEmail').value;
    const position = document.getElementById('staffPosition').value;
    const newStaff = {
        id: staffMembers.length + 1,
        name,
        email,
        position,
        status: 'active', // Default status
    };
    staffMembers.push(newStaff);
    renderStaff();
    closeAddStaffModal();
}

renderStaff();
