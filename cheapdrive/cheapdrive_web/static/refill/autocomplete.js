function initAutocomplete() {
    const options = { types: ['address'] };
    const startingAutocomplete = new google.maps.places.Autocomplete(document.getElementById('id_starting_address'), options);
    const finishingAutocomplete = new google.maps.places.Autocomplete(document.getElementById('id_finishing_address'), options);
}

google.maps.event.addDomListener(window, 'load', initAutocomplete);
