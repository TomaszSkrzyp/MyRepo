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

function getFuelInputType() {
    const litersChecked = document.getElementById('id_cur_fuel_liters_check').checked;
    const percentageChecked = document.getElementById('id_cur_fuel_percentage_check').checked;

    if (litersChecked) {
        return 'liters';
    } else if (percentageChecked) {
        return 'percentage';
    } else {
        return null; // Handle the case where neither is checked (optional)
    }
}

function submitform() {

    let form = document.getElementById('load-data-form');
    // Perform client-side validation here
    if (!validateForm()) return;

    form.submit();
}


function validateForm() {
    // Get form data using IDs that match your Django form field IDs.
    const startingAddress = document.getElementById('id_starting_address').value;
    const finishingAddress = document.getElementById('id_finishing_address').value;
    const tankSize = document.getElementById('id_tank_size').value;
    const fuelType = document.getElementById('id_fuel_type').value;
    const currency = document.getElementById('id_currency').value;
    const fuelConsumption = document.getElementById('id_fuel_consumption_per_100km').value;
    const priceOfFuel = document.getElementById('id_price_of_fuel').value;
    const fuelInputType = getFuelInputType();
    const curFuel = document.getElementById('id_cur_fuel').value;
    const curFuelPercentage = document.getElementById('id_cur_fuel_percentage').value;

    //Validate
    if (!validateAddress(startingAddress)) return false;
    if (!validateAddress(finishingAddress)) return false;
    if (!validateNumber(tankSize, "Tank Size")) return false;
    if (!validateNumber(fuelConsumption, "Fuel Consumption")) return false;
    if (!validateNumber(priceOfFuel, "Price of Fuel")) return false;
   
    if (fuelInputType === null) {alert("Please select a fuel input type.");return false;}

    return true;
}
