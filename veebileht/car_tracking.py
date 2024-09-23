from flask import Flask, jsonify
from flask_cors import CORS  # Import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Dummy car data (in a real app, you'd fetch this from a database)
cars = [
    {"id": 1, "name": "Auto 1", "latitude": 59.395720, "longitude": 24.672221},
    {"id": 2, "name": "Auto 2", "latitude": 59.294738,  "longitude": 24.605670},
    {"id": 3, "name": "Auto 3", "latitude": 51.515, "longitude": -0.08}
]

@app.route('/api/cars', methods=['GET'])
def get_cars():
    return jsonify(cars)

if __name__ == '__main__':
    app.run(debug=True)
