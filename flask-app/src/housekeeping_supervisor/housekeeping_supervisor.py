from flask import Blueprint, request, jsonify
import json
from src import db
from datetime import datetime


housekeeping_supervisor = Blueprint('housekeeping supervisor', __name__)


# Return a list of all rooms in all hotels and their cleaning status
@housekeeping_supervisor.route('/rooms_cleaned', methods=['GET'])
def get_rooms_cleaned():
    try:
        cursor = db.get_db().cursor()

        # Execute a query to get information about all rooms in all hotels
        cursor.execute('SELECT roomNum, cleaned, hotelId FROM Room;')
        row_headers = [x[0] for x in cursor.description]  # Get column headers
        json_data = []
        theData = cursor.fetchall()

        # Creating a JSON response with the fetched data
        for row in theData:
            json_data.append(dict(zip(row_headers, row)))

        return jsonify(json_data)
    except Exception as e:  
        return jsonify({'error': str(e)}), 500


# get all supply units in stock for a hotel
@housekeeping_supervisor.route('/supplies_in_stock', methods=['GET'])
def get_supplies():
    try:
        cursor = db.get_db().cursor()

        # Execute a query to get all supplies from all hotels
        cursor.execute('SELECT name, unitsInStock, hotelId FROM Supplies;')
        row_headers = [x[0] for x in cursor.description]  # Get column headers
        json_data = []
        theData = cursor.fetchall()

        # Creating a JSON response with the fetched data
        for row in theData:
            json_data.append(dict(zip(row_headers, row)))

        return jsonify(json_data)
    except Exception as e:
        # Return an error response with a 500 Internal Server Error status
        return jsonify({'error': str(e)}), 500




# Add a new shift
@housekeeping_supervisor.route('/shifts', methods=['POST'])  
def insert_employee_shift_times():
    data = request.get_json()

    if not data or 'employeeId' not in data or 'start' not in data  or 'end' not in data:
        return jsonify({"error": "Required data not provided"}), 400

    employee_id = data['employeeId']
    start = data['start']
    end = data['end']

    # Validate and convert date format for MySQL
    try:
        start_date = datetime.strptime(start, '%Y-%m-%dT%H:%M:%S')
        end_date = datetime.strptime(end, '%Y-%m-%dT%H:%M:%S')
        start_mysql_format = start_date.strftime('%Y-%m-%d %H:%M:%S')
        end_mysql_format = end_date.strftime('%Y-%m-%d %H:%M:%S')
    except ValueError:
        return jsonify({"error": "Invalid date format"}), 400

    # Check if the employee already has a shift during this time
    cursor = db.get_db().cursor()
    try:
        cursor.execute("""
            SELECT COUNT(1) FROM Shift 
            WHERE employeeId = %s AND (
                (dateTimeStart BETWEEN %s AND %s) OR 
                (dateTimeEnd BETWEEN %s AND %s)
            )
        """, (employee_id, start_mysql_format, end_mysql_format, start_mysql_format, end_mysql_format))

        if cursor.fetchone()[0] > 0:
            return jsonify({"error": "Employee already has a shift during this time"}), 409

        # Insert the new shift
        cursor.execute("""
            INSERT INTO Shift (employeeId, dateTimeStart, dateTimeEnd) 
            VALUES (%s, %s, %s)
        """, (employee_id, start_mysql_format, end_mysql_format))
        db.get_db().commit()
        return jsonify({"message": "Shift times updated successfully"}), 201

    except Exception as e:
        db.get_db().rollback()
        return jsonify({"error": str(e)}), 500

# Updates time off for housekeeping employee
@housekeeping_supervisor.route('/update_time_off', methods=['PATCH'])
def update_time_off():
    try:
        # Get data from the request body
        data = request.get_json()

        # Validate required fields
        if not data or 'employee_id' not in data or 'date_to_update' not in data or 'new_time_off_status' not in data:
            return jsonify({"error": "Required data not provided"}), 400

        employee_id = data['employee_id']
        date_to_update = data['date_to_update']
        new_time_off_status = data['new_time_off_status']

        # Check for valid data types or formats, if necessary
        # ... [Data validation logic here]

        cursor = db.get_db().cursor()

        # Update the timeOff status for a specific date and employeeId
        cursor.execute("""
        UPDATE Shift 
        SET timeOff = %s 
        WHERE employeeId = %s AND 
              DATE(dateTimeStart) = %s
        """, (new_time_off_status, employee_id, date_to_update))

        db.get_db().commit()  # Commit the transaction to the database

        return jsonify({"message": "Time off status updated successfully"}), 200

    except Exception as e:
        # Rollback in case of an error
        db.get_db().rollback()
        return jsonify({"error": str(e)}), 500

# Deletes a cleaning emplot
@housekeeping_supervisor.route('/fire_cleaning', methods=['DELETE'])
def fire_cleaning_employee():
    try:
        cursor = db.get_db().cursor()
        # Extract employee information from request body
        data = request.get_json()
        if not data or 'employeeId' not in data:
            return jsonify({"error": "Employee ID is required"}), 400

        employee_id = data['employeeId']

        # Check if there is an employee with the given employeeId and if the role is 'Housekeeper'
        cursor.execute("""
            SELECT * FROM Employee WHERE employeeId = %s AND role = 'Housekeeper';
        """, (employee_id,))
        employee = cursor.fetchone()

        if not employee:
            return jsonify({"error": "No Housekeeper found with the given ID"}), 404

        # Proceed with deletion
        cursor.execute("DELETE FROM Employee WHERE employeeId = %s;", (employee_id,))
        db.get_db().commit()
        return jsonify({"message": "Housekeeping employee successfully removed"}), 200

    except Exception as e:
        db.get_db().rollback()
        return jsonify({"error": str(e)}), 500

# Changes cleaning status of room
@housekeeping_supervisor.route('/change_room_cleaned', methods=['PUT'])
def change_room_cleaned():
    cursor = db.get_db().cursor()
    try:
        # Extract room data from request body
        data = request.get_json()
        if not data or 'roomNum' not in data or 'hotelId' not in data or 'cleaned' not in data:
            return jsonify({"error": "Required data not provided"}), 400

        room_num = data['roomNum']
        hotel_id = data['hotelId']
        cleaned = data['cleaned']

        if not isinstance(cleaned, bool):
            return jsonify({'error': 'Invalid cleaned status'}), 400

        # Check if the room exists in the database
        cursor.execute("""
            SELECT COUNT(1) FROM Room 
            WHERE roomNum = %s AND hotelId = %s
        """, (room_num, hotel_id))
        
        if cursor.fetchone()[0] == 0:
            return jsonify({'error': 'Room not found'}), 404

        # Update the room's cleaned status
        cursor.execute("""
            UPDATE Room 
            SET cleaned = %s 
            WHERE roomNum = %s AND hotelId = %s
        """, (cleaned, room_num, hotel_id))

        db.get_db().commit()

        return jsonify({'message': 'Room cleaned status updated successfully'}), 200

    except Exception as e:
        db.get_db().rollback()  # Rollback in case of any error
        return jsonify({'error': str(e)}), 500

# Get list of housekeeping employees
@housekeeping_supervisor.route('/get_housekeepers', methods=['GET'])
def get_housekeepers():
    try:
        cursor = db.get_db().cursor()
        cursor.execute("SELECT lastName, firstName, employeeId FROM Employee WHERE role = 'Housekeeper';")
        row_headers = [x[0] for x in cursor.description]
        json_data = []
        theData = cursor.fetchall()
        for row in theData:
            json_data.append(dict(zip(row_headers, row)))
        return jsonify(json_data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Get shift 
@housekeeping_supervisor.route('/shift', methods=['GET'])
def get_shift():
    try:
        cursor = db.get_db().cursor()
        cursor.execute('SELECT timeOff, dateTimeEnd, employeeId, dateTimeStart FROM Shift;')
        row_headers = [x[0] for x in cursor.description]
        json_data = []
        theData = cursor.fetchall()
        for row in theData:
            json_data.append(dict(zip(row_headers, row)))
        return jsonify(json_data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
