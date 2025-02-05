const activateModal = document.getElementById('activateModal');
const activateModalIdInput = activateModal.querySelector('#activate-id');
const activateModalNameInput = activateModal.querySelector('#activate-name');
activateModal.addEventListener('show.bs.modal', event => {
    const button = event.relatedTarget;
    const id = button.getAttribute('data-bs-id');
    const name = button.getAttribute('data-bs-name');
    activateModalNameInput.textContent = name;
    activateModalIdInput.value = id;
});