
function renderStaff() {
    const staffBody = document.getElementById('staffBody');
    staffBody.innerHTML = '';
    staffMembers.forEach(member => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${member.username}</td>
            <td>${member.admin_id}</td>
            <td>${member.email}</td>
            <td>
                <button class="action-button" onclick="viewStaff(${member.admin_id})"><i class="fas fa-eye"></i> View</button>
            </td>
        `;
        staffBody.appendChild(row);
    });
}

function filterStaff() {
    const searchInput = document.getElementById('search').value.toLowerCase();
    const filteredStaff = staffMembers.filter(member => 
        member.username.toLowerCase().includes(searchInput) ||
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
            <td>${member.username}</td>
            <td>${member.admin_id}</td>
            <td>${member.email}</td>
            <td>
                <button class="action-button" onclick="viewStaff(${member.admin_id})"><i class="fas fa-eye"></i> View</button>
            </td>
        `;
        staffBody.appendChild(row);
    });
}

renderStaff();
