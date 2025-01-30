// JavaScript to handle modal content updates
const editModal = document.getElementById('editModal');
const editModalIdInput = editModal.querySelector('#edit-id');
const editModalNameInput = editModal.querySelector('#edit-name');
const editModalDetailsInput = editModal.querySelector('#edit-details');
const editModalQuantityInput = editModal.querySelector('#edit-quantity');
const editModalPackageSelect = editModal.querySelector('#edit-package');
const editModalLocationSelect = editModal.querySelector('#edit-location');
const editModalWorkerSelect = editModal.querySelector('#edit-worker')
editModal.addEventListener('show.bs.modal', event => {
    // Button that triggered the modal
    const button = event.relatedTarget;
    // Extract info from data-bs-* attributes
    const id = button.getAttribute('data-bs-id');
    const name = button.getAttribute('data-bs-name');
    const details = button.getAttribute('data-bs-details');
    const quantity = button.getAttribute('data-bs-quantity');
    const package_id = button.getAttribute('data-bs-package_id');
    const location_id = button.getAttribute('data-bs-location_id');
    // Update the modal's content
    editModalIdInput.value = id;
    editModalNameInput.value = name;
    editModalDetailsInput.value = details;
    editModalQuantityInput.value = quantity;
    editModalPackageSelect.value = package_id;
    editModalLocationSelect.value = location_id;
});

const entryModal = document.getElementById('entryModal');
const entryModalIdInput = entryModal.querySelector('#entry-id');
const entryModalNameInput = entryModal.querySelector('#entry-name');
const entryModalQuantityInput = entryModal.querySelector('#entry-quantity');
const entryModalActionInput = entryModal.querySelector('#entry-action');
const entryModalNewQuantityInput = entryModal.querySelector('#entry-new-quantity');
entryModal.addEventListener('show.bs.modal', event => {
    // Button that triggered the modal
    const button = event.relatedTarget;
    // Extract info from data-bs-* attributes
    const id = button.getAttribute('data-bs-id');
    const name = button.getAttribute('data-bs-name');
    const quantity = button.getAttribute('data-bs-quantity');
    // Update the modal's content
    entryModalIdInput.value = id;
    entryModalNameInput.value = name;
    entryModalQuantityInput.value = quantity;
    entryModalNewQuantityInput.value = 1;
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