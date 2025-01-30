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