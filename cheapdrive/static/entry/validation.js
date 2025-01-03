function validateAddress(address) {
    //  Add proper address validation here.  This is highly context-dependent.
    //  Consider using a third-party library or a more robust regex if needed.
    //  For now, a simple check for non-empty string:
    if (!address || address.trim() === "") {
        alert("Address cannot be empty.");
        return false;
    }
    return true;
}

function validateNumber(value, fieldName) {
    const num = parseFloat(value);
    if (isNaN(num) || !isFinite(num)) {
        alert(`${fieldName} must be a valid number.`);
        return false;
    }
    if (num < 0) {
        alert(`${fieldName} must be a non-negative number.`);
        return false;
    }
    return true;
}

function validateFuelAmount(fuelAmount, tankSize) {
    if (!validateNumber(fuelAmount, "Fuel amount")) return false;
    if (tankSize && parseFloat(fuelAmount) > parseFloat(tankSize)) {
        alert("Fuel amount cannot exceed tank size.");
        return false;
    }
    return true;
}

function validatePercentage(percentage) {
    if (!validateNumber(percentage, "Fuel percentage")) return false;
    if (parseFloat(percentage) > 100) {
        alert("Fuel percentage cannot exceed 100%.");
        return false;
    }
    return true;
}


function submitform() {
    const form = document.getElementById('form');
    const startingAddress = document.getElementById('starting_address').value;
    const finishingAddress = document.getElementById('finishing_address').value;
    const tankSize = document.getElementById('tank_size').value;
    const fuelType = document.getElementById('fuel_type').value;
    const curFuelInputType = document.querySelector('input[name="cur_fuel_input_type"]:checked').value;
    const curFuel = document.getElementById('cur_fuel').value;
    const curFuelPercentage = document.getElementById('cur_fuel_percentage').value;
    const fuelConsumptionPer100km = document.getElementById('fuel_consumption_per_100km').value;
    const priceOfFuel = document.getElementById('price_of_fuel').value;


    if (!validateAddress(startingAddress)) return;
    if (!validateAddress(finishingAddress)) return;

    if (curFuelInputType !== '0' && curFuelInputType !== '1') {
        alert("Please select a fuel input type.");
        return;
    }

    if (!validateNumber(tankSize, "Tank size")) return;

    if (curFuelInputType === '0') {
        if (!validateFuelAmount(curFuel, tankSize)) return;
    } else {
        if (!validatePercentage(curFuelPercentage)) return;
        if (!validateFuelAmount(curFuelPercentage * parseFloat(tankSize) / 100, tankSize)) return;
    }

    if (!validateNumber(fuelConsumptionPer100km, "Fuel consumption")) return;
    if (!validateNumber(priceOfFuel, "Price of fuel")) return;


    form.submit();
}

const fuelInputRadios = document.querySelectorAll('input[name="cur_fuel_input_type"]');
const curFuelLitersInput = document.getElementById('cur_fuel');
const curFuelPercentageInput = document.getElementById('cur_fuel_percentage');

fuelInputRadios.forEach(radio => {
    radio.addEventListener('change', (event) => {
        const selectedValue = event.target.value;
        curFuelLitersInput.disabled = selectedValue === '1';
        curFuelPercentageInput.disabled = selectedValue === '0';
        curFuelLitersInput.value = curFuelLitersInput.disabled ? '' : curFuelLitersInput.value;
        curFuelPercentageInput.value = curFuelPercentageInput.disabled ? '' : curFuelPercentageInput.value;
    });
});

