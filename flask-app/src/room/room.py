from flask import Blueprint, jsonify, request

# Create a Blueprint for rooms
rooms_bp = Blueprint('rooms', __name__)

# Route for getting a list of all rooms with their current occupancy status
@rooms_bp.route('/Room', methods=['GET'])
def get_rooms():
    # Implement logic to fetch room data
    rooms = [
        {"name": "Jessica", "occupancy_status": 1},
        {"name": "Susan", "occupancy_status": 1},
        {"name": "Amir", "occupancy_status": 1}
    ]
    return jsonify(rooms)

# Route for getting a list of all rooms with their cleaning status
@rooms_bp.route('/Room/Cleaning', methods=['GET'])
def get_cleaning_status():
    # Implement logic to fetch cleaning status data
    cleaning_status = [
        {"name": "Carlos", "cleaning_status": 1},
        {"name": "Susan", "cleaning_status": 2}
    ]
    return jsonify(cleaning_status)

# Additional routes can be added here for POST, PUT, DELETE

