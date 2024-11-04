// Wait until the DOM is fully loaded
document.addEventListener("DOMContentLoaded", function() {
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
                    .bindPopup(`<b>${car.name}</b><br>Koordinaadid: ${car.latitude}, ${car.longitude}`);

                // Add to dropdown
                const option = document.createElement('option');
                option.value = `car${car.id}`;
                option.textContent = car.name;
                document.getElementById('carSelect').appendChild(option);
            });
        })
        .catch(error => console.error('Error fetching car data:', error));

    // Fetch battery percentage from the API
    function fetchBatteryPercentage() {
    fetch('http://127.0.0.1:5000/api/battery_percentage')
        .then(response => response.json())
        .then(data => {
            if (data.parameter_name) {
                // Display battery percentage and range_function
                document.getElementById('batteryInfo').textContent = `Aku:  ${data.range_function} %`;
            } else {
                document.getElementById('batteryInfo').textContent = "Battery information not available.";
            }
        })
        .catch(error => console.error('Error fetching battery percentage:', error));
    }


    // Use onclick directly on the button
    document.querySelector('button').onclick = function () {
        const carId = document.getElementById('carSelect').value;
        if (carId && carLocations[carId]) {
            const { name, latitude, longitude } = carLocations[carId];

            // Fly to the car's location
            map.flyTo([latitude, longitude], 17, { 
                animate: true,
                duration: 2
            });

            // Show car info
            document.getElementById('carName').textContent = name;
            document.getElementById('coordinates').textContent = `(${latitude}, ${longitude})`;

            // Fetch and display battery percentage for the selected car
            fetchBatteryPercentage(carId.replace('car', ''));
        } else {
            alert("Please select a car first.");
        }
    };
});
