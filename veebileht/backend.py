from flask import Flask, jsonify
import psycopg2
from flask_cors import CORS  # Import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Database connection parameters
db_params = {
    'dbname': 'auto',
    'user': 'postgres',
    'password': 'password',
    'host': '37.157.64.223',  # Update with your actual database IP
    'port': '5432'
}

# Fetch vehicle data from the database
def fetch_vehicle_data(vehicle_id):
    conn = None
    try:
        conn = psycopg2.connect(**db_params)
        cursor = conn.cursor()

        query = """
            SELECT v.vehicle_name, loc.p_x, loc.p_y
            FROM vehicle v
            JOIN v_localization loc ON v.vehicle_id = loc.vehicle_id
            WHERE v.vehicle_id = %s
            ORDER BY loc.recorded_time DESC
            LIMIT 1;
        """
        cursor.execute(query, (vehicle_id,))
        result = cursor.fetchone()

        if result:
            vehicle_name, p_x, p_y = result
            return {
                'id': vehicle_id,
                'name': vehicle_name,
                'latitude': p_x,
                'longitude': p_y
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
            SELECT parameter_name, unit, range_function
            FROM v_parameter
            WHERE class_id = 1 AND parameter_name = 'battery_percentage'
            LIMIT 1;
        """
        cursor.execute(query)
        result = cursor.fetchone()

        if result:
            parameter_name, unit, range_function = result
            return {
                'parameter_name': parameter_name,
                'unit': unit,
                'range_function': range_function  # Include the range_function in the response
            }
        else:
            return None

    except psycopg2.DatabaseError as e:
        print(f"Error: {e}")
        return None

    finally:
        if conn:
            conn.close()


# Route to fetch battery percentage data without vehicle_id
@app.route('/api/battery_percentage', methods=['GET'])
def get_battery_percentage():
    battery_data = fetch_battery_percentage()  # No need for vehicle_id

    if battery_data:
        return jsonify(battery_data)  # Send full battery data, including range_function
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
