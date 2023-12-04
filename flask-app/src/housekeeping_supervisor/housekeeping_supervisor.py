from flask import Blueprint, request, jsonify, make_response
import json
from src import db


housekeeping_supervisor = Blueprint('housekeeping supervisor', __name__)

# get all rooms with their cleaned status for a hotel id
@housekeeping_supervisor.route('/roomsCleaned', methods=['GET'])
def get_rooms_cleaned():
    # Get hotelId from the request body
    data = request.get_json()
    hotel_id = data['hotelId']

    cursor = db.get_db().cursor()
    cursor.execute('SELECT roomNum, cleaned FROM rooms WHERE hotelId = %s', (hotel_id,))
    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(row_headers, row)))
    return json_data

# Return a list of all supply units in stock for a hotel
@housekeeping_supervisor.route('/supplies', methods=['GET'])
def get_supplies():
    # Get hotelId from the request body
    data = request.get_json()
    hotel_id = data['hotelId']

    cursor = db.get_db().cursor()
    cursor.execute('SELECT name, unitsInStock FROM Supplies WHERE hotelId = %s', (hotel_id,))
    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(row_headers, row)))
    the_response = make_response(jsonify(json_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response


# Return a list of all supply units in stock for a hotel
@housekeeping_supervisor.route('/shifts', methods=['POST'])  
def insert_employee_shift_times():
    # Get data from the request body
    data = request.get_json()
    employee_id = data['employeeId']
    start = data['start']
    end = data['end']

    cursor = db.get_db().cursor()
    # Use placeholder %s 
    cursor.execute('INSERT INTO Shift (employeeId, dateTimeStart, dateTimeEnd) VALUES (%s, %s, %s)', 
                   (employee_id, start, end))
    db.get_db().commit()  # Commit to the database
    
    #return success message
    return jsonify({"message": "Shift times updated successfully"}), 201

@housekeeping_supervisor.route('/updateTimeOff', methods=['PATCH'])
def update_time_off():
    # Get data from the request body
    data = request.get_json()
    employee_id = data['employeeId']
    date_to_update = data['date']
    new_time_off_status = data['timeOff']

    cursor = db.get_db().cursor()
    # Update the timeOff status for a specific date and employeeId
    cursor.execute('UPDATE Shift SET timeOff = %s WHERE employeeId = %s AND DATE(dateTimeStart) = %s', 
                   (new_time_off_status, employee_id, date_to_update))
    db.get_db().commit()  # Commit the transaction to the database

    # Return a success message
    return jsonify({"message": "Time off status updated successfully"}), 200



