const carLocations = {}; // Object to hold car locations
const markers = {}; // Object to hold markers

// Initialize the map and set the initial view
var map = L.map('map').setView([59.395720, 24.672221], 13);

// Add OpenStreetMap tiles to the map
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '© OpenStreetMap contributors'
}).addTo(map);

// Fetch car data from the API
fetch('http://127.0.0.1:5000/api/cars')
    .then(response => response.json())
    .then(data => {
        data.forEach(car => {
            carLocations[`car${car.id}`] = { name: car.name, latitude: car.latitude, longitude: car.longitude };
            markers[`car${car.id}`] = L.marker([car.latitude, car.longitude])
                .addTo(map)
                .bindPopup(`<b>${car.name}</b><br>Coordinates: ${car.latitude}, ${car.longitude}`);

            // Add to dropdown
            const option = document.createElement('option');
            option.value = `car${car.id}`;
            option.textContent = car.name;
            document.getElementById('carSelect').appendChild(option);
        });
    })
    .catch(error => console.error('Error fetching car data:', error));

// Function to smoothly fly to the selected car's location
function flyToCar() {
    const carId = document.getElementById('carSelect').value;
    if (carId && carLocations[carId]) {
        const { latitude, longitude } = carLocations[carId];
        map.flyTo([latitude, longitude], 17, { 
            animate: true,
            duration: 2
        });
        markers[carId].openPopup();
    } else {
        alert("Palun valige auto esmalt.");
    }
}
