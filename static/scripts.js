// JavaScript to handle modal content updates
const editModal = document.getElementById('editModal');
const editModalIdInput = editModal.querySelector('#edit-id');
const editModalNameInput = editModal.querySelector('#edit-name');
const editModalQuantityInput = editModal.querySelector('#edit-quantity');
const editModalPackageInput = editModal.querySelector('#edit-package');
const editModalLocationInput = editModal.querySelector('#edit-location');
editModal.addEventListener('show.bs.modal', event => {
    // Button that triggered the modal
    const button = event.relatedTarget;
    // Extract info from data-bs-* attributes
    const id = button.getAttribute('data-bs-id');
    const name = button.getAttribute('data-bs-name');
    const quantity = button.getAttribute('data-bs-quantity');
    const package = button.getAttribute('data-bs-package');
    const location = button.getAttribute('data-bs-location');
    // Update the modal's content
    editModalIdInput.value = id;
    editModalNameInput.value = name;
    editModalQuantityInput.value = quantity;
    editModalPackageInput.value = package;
    editModalLocationInput.value = location;
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
    entryModalNewQuantityInput.value = 0;
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

function filterTable() {
    const input = document.getElementById('searchInput');
    const filter = input.value.toLowerCase();
    const table = document.getElementById('inventoryTable');
    const rows = table.getElementsByTagName('tr');

    // Itera sobre las filas de la tabla (excluyendo el encabezado)
    for (let i = 1; i < rows.length; i++) {
        const cells = rows[i].getElementsByTagName('td');
        if (cells.length > 0) {
            const name = cells[1].textContent || cells[1].innerText;
            if (name.toLowerCase().indexOf(filter) > -1) {
                rows[i].style.display = ''; // Mostrar fila
            } else {
                rows[i].style.display = 'none'; // Ocultar fila
            }
        }
    }
}


// Código para mejorar el uso de la entrada "cantidad"
function changeQuantity(amount) {
    let currentValue = parseInt(entryModalNewQuantityInput.value) || 0;
    let maxValue = parseInt(entryModalQuantityInput.value) || 0;
    let action = entryModalActionInput.value || '';

    currentValue += amount;

    // Asegurarse de que no sea menor que 0
    if (currentValue < 0) {
        currentValue = 0;
    }
    
    // En caso de salidas, el max es la cantidad actual
    if (currentValue > maxValue && action == "subtract") {
        currentValue = maxValue
    }

    entryModalNewQuantityInput.value = currentValue;
}

function startChange(amount) {
    changeQuantity(amount);
    intervalId = setInterval(() => changeQuantity(amount), 100);
}

function stopChange() {
    clearInterval(intervalId);
}

function setZeroValue(){entryModalNewQuantityInput.value = 0;}
