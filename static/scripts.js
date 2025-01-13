// JavaScript to handle modal content updates
const editModal = document.getElementById('editModal');
const editModalIdInput = editModal.querySelector('#edit-id');
const editModalNameInput = editModal.querySelector('#edit-name');
const editModalDetailsInput = editModal.querySelector('#edit-details');
const editModalQuantityInput = editModal.querySelector('#edit-quantity');
const editModalPackageSelect = editModal.querySelector('#edit-package');
const editModalLocationSelect = editModal.querySelector('#edit-location');
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

    // Se cargan las listas de opciones de Empaques y Ubicación
    loadOptions(package_id, location_id);
    
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

    // Asegurarse de que no sea menor que 1
    if (currentValue <= 0) {
        currentValue = 1;
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

function setZeroValue(){entryModalNewQuantityInput.value = 1;}

async function loadOptions(package_id, location_id) {
    try {
        // Obtener datos desde la API
        const response = await fetch('/get_package_location');
        const data = await response.json();

        // Limpiar las opciones actuales
        editModalPackageSelect.innerHTML = '';
        editModalLocationSelect.innerHTML = '';

        // Agregar cada empaque como una nueva opción
        data.package.forEach(package => {
            const option = document.createElement('option');
            option.value = package.id; // Asignar el valor del Empaque_id
            option.textContent = package.nombre; // Texto visible
            editModalPackageSelect.appendChild(option);
        });

        // Agregar cada ubicación como una nueva opción
        data.location.forEach(location => {
            const option = document.createElement('option');
            option.value = location.id; // Asignar el valor del Empaque_id
            option.textContent = location.nombre; // Texto visible
            editModalLocationSelect.appendChild(option);
        });

        // Se establece la opción original por defecto
        editModalPackageSelect.value = package_id;
        editModalLocationSelect.value = location_id;

    } catch(error) {
        console.error('Error al cargar la lista',error);
    }
}