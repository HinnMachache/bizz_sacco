// members.js

// Sample data with 10 members
let members = [
    { name: 'John Doe', email: 'john@example.com', status: 'Active' },
    { name: 'Jane Smith', email: 'jane@example.com', status: 'Inactive' },
    { name: 'Alice Johnson', email: 'alice@example.com', status: 'Active' },
    { name: 'Bob Brown', email: 'bob@example.com', status: 'Active' },
    { name: 'Charlie Davis', email: 'charlie@example.com', status: 'Inactive' },
    { name: 'Diana Evans', email: 'diana@example.com', status: 'Active' },
    { name: 'Ethan Foster', email: 'ethan@example.com', status: 'Active' },
    { name: 'Fiona Green', email: 'fiona@example.com', status: 'Inactive' },
    { name: 'George Harris', email: 'george@example.com', status: 'Active' },
    { name: 'Hannah Ivers', email: 'hannah@example.com', status: 'Inactive' },
];

// Function to open the modal for adding a new member
function openAddMemberModal() {
    document.getElementById("addMemberModal").style.display = "block";
}

// Function to close the modal
function closeAddMemberModal() {
    document.getElementById("addMemberModal").style.display = "none";
}

// Function to add a member
function addMember(event) {
    event.preventDefault();
    const name = document.getElementById('memberName').value;
    const email = document.getElementById('memberEmail').value;
    const photo = document.getElementById('memberPhoto').files[0];

    // You can handle the image upload here

    members.push({ name, email, status: 'Active' }); // Default status
    document.getElementById('addMemberForm').reset();
    closeAddMemberModal();
    updateMembersTable();
}

// Function to filter members based on search input
function filterMembers() {
    const query = document.getElementById('search').value.toLowerCase();
    const filteredMembers = members.filter(member => member.name.toLowerCase().includes(query));
    updateMembersTable(filteredMembers);
}

// Function to update the members table
function updateMembersTable(filteredMembers = members) {
    const membersBody = document.getElementById('membersBody');
    membersBody.innerHTML = ''; // Clear the current rows
    filteredMembers.forEach(member => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${member.name}</td>
            <td>${member.email}</td>
            <td>${member.status}</td>
            <td>
                <button onclick="editMember('${member.name}')"><i class="fas fa-edit"></i> Edit</button>
                <button onclick="deleteMember('${member.name}')"><i class="fas fa-trash-alt"></i> Delete</button>
            </td>
        `;
        membersBody.appendChild(row);
    });
}

// Function to edit a member (to be implemented)
function editMember(name) {
    alert('Edit member: ' + name);
}

// Function to delete a member
function deleteMember(name) {
    members = members.filter(member => member.name !== name);
    updateMembersTable();
}

// Close the modal if the user clicks outside of it
window.onclick = function(event) {
    const modal = document.getElementById("addMemberModal");
    if (event.target === modal) {
        closeAddMemberModal();
    }
};

// Initial population of the members table
updateMembersTable();
