from flask import Flask, jsonify
import psycopg2
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Database connection parameters
db_params = {
    'dbname': 'auto',
    'user': 'postgres',
    'password': 'password',
    'host': '37.157.64.223',  # Update with your actual database IP
    'port': '5432'
}

# Fetch vehicle location data from the database
def fetch_vehicle_data(vehicle_id):
    conn = None
    try:
        conn = psycopg2.connect(**db_params)
        cursor = conn.cursor()

        # Query to get coordinates from the v_parameter table
        query = """
            SELECT v.vehicle_id, v.vehicle_name, p.parameter_value
            FROM vehicle v
            JOIN v_parameter p ON v.vehicle_id = p.vehicle_id
            WHERE p.parameter_name = 'gnss' AND v.vehicle_id = %s
            LIMIT 1;
        """
        cursor.execute(query, (vehicle_id,))
        result = cursor.fetchone()

        if result:
            vehicle_id, vehicle_name, parameter_value = result
            # Split the parameter_value to get latitude and longitude
            latitude, longitude = map(float, parameter_value.split())
            return {
                'id': vehicle_id,
                'name': vehicle_name,
                'latitude': latitude,
                'longitude': longitude
            }
        else:
            return None

    except psycopg2.DatabaseError as e:
        print(f"Error: {e}")
        return None

    finally:
        if conn:
            conn.close()

# Fetch battery percentage data from the database
def fetch_battery_percentage():
    conn = None
    try:
        conn = psycopg2.connect(**db_params)
        cursor = conn.cursor()

        query = """
            SELECT parameter_name, unit, parameter_value
            FROM v_parameter
            WHERE class_id = 1 AND parameter_name = 'battery_percentage'
            LIMIT 1;
        """
        cursor.execute(query)
        result = cursor.fetchone()

        if result:
            parameter_name, unit, parameter_value = result
            return {
                'parameter_name': parameter_name,
                'unit': unit,
                'parameter_value': parameter_value  
            }
        else:
            return None

    except psycopg2.DatabaseError as e:
        print(f"Error: {e}")
        return None

    finally:
        if conn:
            conn.close()

# Fetch all parameters for a specific vehicle
def fetch_all_parameters(vehicle_id):
    conn = None
    try:
        conn = psycopg2.connect(**db_params)
        cursor = conn.cursor()

        query = """
            SELECT parameter_name, unit, parameter_value
            FROM v_parameter
            WHERE vehicle_id = %s;
        """
        cursor.execute(query, (vehicle_id,))
        results = cursor.fetchall()

        # Convert results to a list of dictionaries
        parameters = [
            {
                'name': row[0],
                'unit': row[1],
                'value': row[2]
            } for row in results
        ]
        return parameters

    except psycopg2.DatabaseError as e:
        print(f"Error: {e}")
        return None

    finally:
        if conn:
            conn.close()

# Route to fetch all parameters for a vehicle
@app.route('/api/vehicle_parameters/<int:vehicle_id>', methods=['GET'])
def get_vehicle_parameters(vehicle_id):
    parameters = fetch_all_parameters(vehicle_id)
    if parameters:
        return jsonify(parameters)
    else:
        return jsonify({'error': 'No parameters found for this vehicle'}), 404

# Route to fetch battery percentage data without vehicle_id
@app.route('/api/battery_percentage', methods=['GET'])
def get_battery_percentage():
    battery_data = fetch_battery_percentage()  # No need for vehicle_id

    if battery_data:
        return jsonify(battery_data)  # Send full battery data
    else:
        return jsonify({'error': 'No battery data found'}), 404

# Route to fetch car data
@app.route('/api/cars', methods=['GET'])
def get_car_data():
    vehicle_ids = [1, 2, 3]  # Example vehicle IDs
    cars = []

    for vehicle_id in vehicle_ids:
        car_data = fetch_vehicle_data(vehicle_id)
        if car_data:
            cars.append(car_data)

    if cars:
        return jsonify(cars)
    else:
        return jsonify({'error': 'No cars found'}), 404

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
