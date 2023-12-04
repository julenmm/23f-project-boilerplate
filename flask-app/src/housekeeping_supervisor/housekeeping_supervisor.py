from flask import Blueprint, request, jsonify
import json
from src import db


housekeeping_supervisor = Blueprint('housekeeping supervisor', __name__)



# get all rooms for one hotel
@housekeeping_supervisor.route('/roomsCleaned', methods=['GET'])
def get_rooms_cleaned():
    cursor = db.get_db().cursor()

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



