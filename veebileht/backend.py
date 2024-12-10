from flask import Flask, jsonify
import psycopg2
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Database connection parameters
# Make sure to update these parameters according to your actual database configuration.
# 'dbname': The name of the PostgreSQL database you are connecting to.
# 'user': The username used to connect to the database.
# 'password': The password for the specified database user.
# 'host': The host/IP address where your database server is running.
# 'port': The port on which your PostgreSQL server is listening (default is often 5432).

db_params = {
    'dbname': 'auto',       # Replace 'auto' with your actual database name
    'user': 'postgres',     # Replace 'postgres' with your actual database username
    'password': 'password', # Replace 'password' with the actual password for the user above
    'host': 'localhost',    # Replace 'localhost' with the IP or hostname of your database server
    'port': '5432'          # Replace '5432' with the actual port number if different from the default
}

# Parameter ID to Name Mapping
parameter_names = {
    33: "battery_percentage",
    34: "set_turning_lights",
    35: "hazzard_lights",
    36: "high_beam",
    37: "marker_lights",
    38: "brake_lights",
    45: "emergency_brake",
    63: "current_velocity",
    65: "driving_mode",
    74: "gnss",
    77: "camera_front",
    78: "camera_back",
    40: "door_status"
}

# Function to fetch all parameters for a specific vehicle
def fetch_all_parameters(vehicle_id):
    conn = None
    try:
        conn = psycopg2.connect(**db_params)
        cursor = conn.cursor()

        query = """
            SELECT parameter_id, jason_data
            FROM v_log
            WHERE vehicle_id = %s;
        """
        cursor.execute(query, (vehicle_id,))
        results = cursor.fetchall()

        # Convert results to a list of dictionaries
        parameters = [
            {
                'id': row[0],
                'name': parameter_names.get(row[0], "unknown"),  # Map parameter_id to name
                'data': row[1],
            } for row in results
        ]
        return parameters

    except psycopg2.DatabaseError as e:
        print(f"Error: {e}")
        return None

    finally:
        if conn:
            conn.close()

# Route to fetch all vehicles with latitude, longitude, and current_velocity from v_log
@app.route('/api/vehicles', methods=['GET'])
def get_vehicles():
    conn = None
    try:
        conn = psycopg2.connect(**db_params)
        cursor = conn.cursor()

        # Query to fetch vehicle data along with GNSS information and velocity from v_log
        query = """
                SELECT DISTINCT ON (v.vehicle_id) 
                v.vehicle_id AS vehicle_id, 
                v.vehicle_name AS vehicle_name, 
                jl_lat.jason_data->>'latitude' AS latitude, 
                jl_lat.jason_data->>'longitude' AS longitude,
                (jl_vel.jason_data::text)::numeric AS velocity -- First cast to text, then to numeric
            FROM vehicle v
            LEFT JOIN v_log jl_lat 
                ON v.vehicle_id = jl_lat.vehicle_id AND jl_lat.parameter_id = 74
            LEFT JOIN v_log jl_vel 
                ON v.vehicle_id = jl_vel.vehicle_id AND jl_vel.parameter_id = 63
            ORDER BY v.vehicle_id, jl_lat.recorded_time DESC, jl_vel.recorded_time DESC;

        """
        cursor.execute(query)
        results = cursor.fetchall()

        # Convert results to a list of dictionaries
        vehicles = [
            {
                'vehicle_id': row[0],
                'vehicle_name': row[1],
                'latitude': float(row[2]) if row[2] else None,
                'longitude': float(row[3]) if row[3] else None,
                'current_velocity': float(row[4]) if row[4] else None
            } for row in results
        ]

        return jsonify(vehicles)

    except psycopg2.DatabaseError as e:
        print(f"Database error: {e}")
        return jsonify({'error': 'Database error', 'details': str(e)}), 500

    finally:
        if conn:
            conn.close()

@app.route('/api/vehicle_parameters/<int:vehicle_id>/<int:parameter_id>', methods=['GET'])
def get_vehicle_parameter(vehicle_id, parameter_id):
    conn = None
    try:
        conn = psycopg2.connect(**db_params)
        cursor = conn.cursor()

        # Updated query to include the timestamp
        query = """
            SELECT parameter_id, jason_data, recorded_time
            FROM v_log
            WHERE vehicle_id = %s AND parameter_id = %s
            ORDER BY recorded_time DESC
            LIMIT 1;  -- Retrieve the most recent entry
        """
        cursor.execute(query, (vehicle_id, parameter_id))
        result = cursor.fetchone()

        if result:
            parameter = {
                'id': result[0],
                'name': parameter_names.get(result[0], "unknown"),
                'data': result[1],  # JSON data
                'timestamp': result[2].isoformat() if result[2] else None  # Format timestamp as ISO
            }
            return jsonify(parameter)
        else:
            return jsonify({'error': 'Parameter not found for this vehicle'}), 404

    except psycopg2.DatabaseError as e:
        print(f"Error: {e}")
        return jsonify({'error': 'Database error'}), 500

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

# New route to fetch historical route data for a specific vehicle
@app.route('/api/vehicle_route/<int:vehicle_id>', methods=['GET'])
def get_vehicle_route(vehicle_id):
    conn = None
    try:
        conn = psycopg2.connect(**db_params)
        cursor = conn.cursor()

        # Query to fetch historical location data for the vehicle
        query = """
            SELECT recorded_time, jason_data->>'latitude' AS latitude, jason_data->>'longitude' AS longitude
            FROM v_log
            WHERE vehicle_id = %s AND parameter_id = 74
            ORDER BY recorded_time ASC;
        """
        cursor.execute(query, (vehicle_id,))
        results = cursor.fetchall()

        # Convert results to a list of dictionaries
        route = [
            {
                'timestamp': row[0],
                'latitude': float(row[1]),
                'longitude': float(row[2])
            } for row in results
        ]

        return jsonify(route)

    except psycopg2.DatabaseError as e:
        print(f"Error: {e}")
        return jsonify({'error': 'Database error', 'details': str(e)}), 500

    finally:
        if conn:
            conn.close()

# New route to fetch the latest camera images for a specific vehicle
@app.route('/api/vehicle_cameras/<int:vehicle_id>', methods=['GET'])
def get_vehicle_cameras(vehicle_id):
    conn = None
    try:
        conn = psycopg2.connect(**db_params)
        cursor = conn.cursor()

        # Query to fetch the latest camera images for front and back cameras
        query = """
            SELECT parameter_id, jason_data
            FROM v_log
            WHERE vehicle_id = %s AND parameter_id IN (77, 78)
            ORDER BY recorded_time DESC;
        """
        cursor.execute(query, (vehicle_id,))
        results = cursor.fetchall()

        # Convert results to a dictionary with front and back camera images
        camera_images = {}
        for row in results:
            # Sanitize image name or jason_data by replacing ":" with "-"
            sanitized_data = row[1].replace(":", "-") if isinstance(row[1], str) else row[1]
            
            if row[0] == 77:
                camera_images['camera_front'] = sanitized_data
            elif row[0] == 78:
                camera_images['camera_back'] = sanitized_data

        return jsonify(camera_images)

    except psycopg2.DatabaseError as e:
        print(f"Error: {e}")
        return jsonify({'error': 'Database error', 'details': str(e)}), 500

    finally:
        if conn:
            conn.close()

    
@app.route('/api/parameter_names', methods=['GET'])
def get_parameter_names():
    return jsonify([{'id': key, 'name': value} for key, value in parameter_names.items()])

@app.route('/api/vehicle_parameters/<int:vehicle_id>/<int:parameter_id>/history', methods=['GET'])
def get_vehicle_parameter_history(vehicle_id, parameter_id):
    conn = None
    try:
        conn = psycopg2.connect(**db_params)
        cursor = conn.cursor()

        # Query to fetch the last 25 records for the parameter
        query = """
            SELECT recorded_time, jason_data
            FROM v_log
            WHERE vehicle_id = %s AND parameter_id = %s
            ORDER BY recorded_time DESC
            LIMIT 25;
        """
        cursor.execute(query, (vehicle_id, parameter_id))
        results = cursor.fetchall()

        # Format results as a list of dictionaries
        history = [
            {
                'timestamp': row[0].isoformat(),
                'data': row[1]
            } for row in results
        ]

        return jsonify(history)

    except psycopg2.DatabaseError as e:
        print(f"Error: {e}")
        return jsonify({'error': 'Database error', 'details': str(e)}), 500

    finally:
        if conn:
            conn.close()


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
