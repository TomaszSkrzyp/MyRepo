// Get references to the checkboxes, inputs, and visualisation element
const litersCheckbox = document.getElementById('id_cur_fuel_liters_check');
const litersInput = document.getElementById('id_cur_fuel');
const percentageCheckbox = document.getElementById('id_cur_fuel_percentage_check');
const percentageInput = document.getElementById('id_cur_fuel_percentage');
const fuelAmountDisplay = document.getElementById('fuel-amount-display');


// Function to update the visibility of the visualisation
function toggleVisualisation() {
    if (percentageCheckbox.checked) {
        fuelAmountDisplay.style.display = 'inline'; // Show the visualisation

        updateFuelAmountDisplay();
    } else {
        fuelAmountDisplay.style.display = 'none'; // Hide the visualisation
    }
}

// Function to initialize the state of checkboxes and inputs
function initializeCheckboxes() {
    // Ensure only the liters checkbox is checked on page load
    litersCheckbox.checked = true;
    percentageCheckbox.checked = false;

    // Update the inputs accordingly
    updateCheckboxesAndInputs();
    toggleVisualisation(); // Ensure visualisation state is correct on page load
}

// Function to update inputs and ensure mutual exclusivity
function updateCheckboxesAndInputs() {
    // Enable or disable inputs based on the checkboxes
    litersInput.disabled = !litersCheckbox.checked;
    if (litersInput.disabled) {
        litersInput.value = ''; // Clear the value if input is disabled
    }

    percentageInput.disabled = !percentageCheckbox.checked;
    if (percentageInput.disabled) {
        percentageInput.value = ''; // Clear the value if input is disabled
    }

    // Ensure mutual exclusivity between checkboxes
    percentageCheckbox.checked = !litersCheckbox.checked;
}

// Event listener for liters checkbox
litersCheckbox.addEventListener('change', () => {
    if (litersCheckbox.checked) {
        percentageCheckbox.checked = false; // Uncheck the percentage checkbox
    }
    updateCheckboxesAndInputs(); // Update the input states
    toggleVisualisation(); // Update the visualisation state
});

// Event listener for percentage checkbox
percentageCheckbox.addEventListener('change', () => {
    if (percentageCheckbox.checked) {
        litersCheckbox.checked = false; // Uncheck the liters checkbox
    }
    updateCheckboxesAndInputs(); // Update the input states
    toggleVisualisation(); // Update the visualisation state
});

// Initialize the checkboxes and visualisation on page load
initializeCheckboxes();
