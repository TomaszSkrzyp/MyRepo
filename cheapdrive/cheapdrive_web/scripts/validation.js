function validateAddress(address) {
    // Basic address validation (can be more complex)
    if (!address.includes(" ") || !address.includes(",")) {
        alert("Address should include at least one space.");
        return false;
    }
    return true;
}

function validateFuelAmount(fuelAmount) {
    // Check if the input is a valid number
    if (isNaN(parseFloat(fuelAmount)) || !isFinite(fuelAmount)) {
        alert("Amount of Fuel must be a valid number.");
        return false;
    }

    // Check if the amount of fuel is a positive number
    if (parseFloat(fuelAmount) <= 0) {
        alert("Amount of Fuel must be a positive number.");
        return false;
    }
    return true;
}
function confirm_no_fuel_overflow(cur_fuel,tank_size) {
    if (parseFloat(cur_fuel) > parseFloat(tank_size) ) {
        alert("Fuel amount in a vehicle cant be higher than it's tank size");
        return false;
    }
}
function validatePrice(price) {
    // Check if the input is a valid number
    if (isNaN(parseFloat(price)) || !isFinite(price)) {
        alert("Price must be a valid number.");
        return false;
    }

    // Check if the price is a non-negative number
    if (parseFloat(price) < 0) {
        alert("Price must be a non-negative number.");
        return false;
    }
    return true;
}