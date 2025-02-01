const editModal = document.getElementById('editModal');
const editModalIdInput = editModal.querySelector('#edit-id');
const editModalNameInput = editModal.querySelector('#edit-name');
const editModalBranchSelect = editModal.querySelector('#edit-branch');
const editModalPositionSelect = editModal.querySelector('#edit-position');
const editModalEmailInput = editModal.querySelector('#edit-email');
editModal.addEventListener('show.bs.modal', event => {
    // Button that triggered the modal
    const button = event.relatedTarget;
    // Extract info from data-bs-* attributes
    const id = button.getAttribute('data-bs-id');
    const name = button.getAttribute('data-bs-name');
    const branch = button.getAttribute('data-bs-branch');
    const position = button.getAttribute('data-bs-position');
    const email = button.getAttribute('data-bs-email');
    // Update the modal's content
    editModalIdInput.value = id;
    editModalNameInput.value = name;
    editModalBranchSelect.value = branch;
    editModalPositionSelect.value = position;
    editModalEmailInput.value = email;
});

const deleteModal = document.getElementById('deleteModal');
const deleteModalIdInput = deleteModal.querySelector('#delete-id');
const deleteModalNameInput = deleteModal.querySelector('#delete-name');
deleteModal.addEventListener('show.bs.modal', event => {
    const button = event.relatedTarget;
    const id = button.getAttribute('data-bs-id');
    const name = button.getAttribute('data-bs-name');
    deleteModalNameInput.textContent = name;
    deleteModalIdInput.value = id;
});