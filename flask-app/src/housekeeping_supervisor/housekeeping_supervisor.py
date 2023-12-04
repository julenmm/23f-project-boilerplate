from flask import Blueprint, request, jsonify
import json
from src import db
from datetime import datetime


housekeeping_supervisor = Blueprint('housekeeping supervisor', __name__)



# get all rooms for one hotel
@housekeeping_supervisor.route('/rooms_cleaned', methods=['GET'])
def get_rooms_cleaned():
    cursor = db.get_db().cursor()
    if not data or 'hotelId' not in data:
        return jsonify({"error": "Required data not provided"}), 400

     # Extract booking information from request body
    data = request.json
    hotelId= data['hotelId']
    
    cursor.execute('select roomNum, cleaned from Room WHERE hotelId = %s;', (hotelId))
    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(row_headers, row)))
    return jsonify(json_data)

# get all supply units in stock for a hotel
@housekeeping_supervisor.route('/supplies_in_stock', methods=['GET'])
def get_supplies():
    cursor = db.get_db().cursor()
    if not data or 'hotelId' not in data:
        return jsonify({"error": "Required data not provided"}), 400

    # Get hotelId from the request body
    data = request.json
    hotelId = data['hotelId']

    cursor.execute('select name, unitsInStock FROM Supplies WHERE hotelId = %s;', (hotelId))
    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(row_headers, row)))
    return jsonify(json_data)



# Return a list of all supply units in stock for a hotel
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

@housekeeping_supervisor.route('/update_time_off', methods=['PATCH'])
def update_time_off():
    # Get data from the request body
    data = request.get_json()
    employee_id = data['employeeId']
    date_to_update = data['date']
    new_time_off_status = data['timeOff']

    cursor = db.get_db().cursor()
    # Update the timeOff status for a specific date and employeeId
    cursor.execute("""
    UPDATE Shift 
    SET timeOff = %s 
    WHERE employeeId = %s AND 
          DATE(dateTimeStart) = %s
    """, (new_time_off_status, employee_id, date_to_update))


    db.get_db().commit()  # Commit the transaction to the database

    # Return a success message
    return jsonify({"message": "Time off status updated successfully"}), 200

# deletes a cleeaning emplot
@housekeeping_supervisor.route('/fire_cleaning', methods=['DELETE'])
def fire_cleaning_employee():
    cursor = db.get_db().cursor()
    try:
        # Extract employee information from request body
        data = request.json
        employee_id = data['employeeId']

        # Check if there is an employee with the given employeeId and if the role is 'Housekeeper'
        cursor.execute("""
            SELECT * FROM Employee WHERE employeeId = %s AND role = 'Housekeeper';
        """, (employee_id,))
        employee = cursor.fetchone()

        if not employee:
            # If no employee found with the role 'Housekeeper', return an error message
            return jsonify({"error": "No Housekeeper found with the given ID"}), 404

        # If employee with role 'Housekeeper' exists, proceed with deletion
        cursor.execute("""
            DELETE FROM Employee WHERE employeeId = %s;
        """, (employee_id,))
        db.get_db().commit()

        # Return a success message
        return jsonify({"message": "Housekeeping employee successfully removed"}), 200

    except Exception as e:
        db.get_db().rollback()  # Rollback in case of any error
        return jsonify({"error": str(e)}), 500

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

