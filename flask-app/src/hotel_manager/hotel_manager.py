from flask import Blueprint, request, jsonify, make_response
import json
from src import db


customers = Blueprint('customers', __name__)

# Get all customers from the DB
@customers.route('/customers', methods=['GET'])
def get_customers():
    cursor = db.get_db().cursor()
    cursor.execute('select company, last_name,\
        first_name, job_title, business_phone from customers')
    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(row_headers, row)))
    the_response = make_response(jsonify(json_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

# Get customer detail for customer with particular userID
@customers.route('/customers/<userID>', methods=['GET'])
def get_customer(userID):
    cursor = db.get_db().cursor()
    cursor.execute('select * from customers where id = {0}'.format(userID))
    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(row_headers, row)))
    the_response = make_response(jsonify(json_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

rooms = Blueprint("rooms", __name__)

@rooms.route('/rooms/occupancy', methods=['GET'])
def get_rooms_occupancy():
    try:
        cursor = db.get_db().cursor()
        current_date = datetime.datetime.now().date()  # Get the current date

        # Query to select room information and occupancy status
        query = """
        SELECT Room.roomNum, Room.hotelId, Room.cleaned, Room.occupancy, Room.yearlyMaintenance, Room.roomPrice,
               CASE
                   WHEN Booking.roomNum IS NOT NULL AND Booking.hotelId = Room.hotelId AND 
                        Booking.occupancyStartDate <= %s AND Booking.occupancyEndDate >= %s 
                   THEN TRUE
                   ELSE FALSE
               END as IsOccupied
        FROM Room
        LEFT JOIN Booking ON Room.roomNum = Booking.roomNum AND Room.hotelId = Booking.hotelId
        AND (Booking.occupancyStartDate <= %s AND Booking.occupancyEndDate >= %s)
        GROUP BY Room.roomNum, Room.hotelId
        ORDER BY Room.hotelId, Room.roomNum
        """
        cursor.execute(query, (current_date, current_date, current_date, current_date))
        row_headers = [x[0] for x in cursor.description]  # Extract column headers
        results = cursor.fetchall()
        
        # Convert query results to json format
        json_data = []
        for result in results:
            room_data = dict(zip(row_headers, result))
            room_data['IsOccupied'] = bool(room_data['IsOccupied'])  # Convert to boolean
            json_data.append(room_data)

        return jsonify(json_data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500