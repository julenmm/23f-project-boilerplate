from flask import Blueprint, request, jsonify, make_response
import json
from src import db


front_desk_agent = Blueprint('front_desk_agent', __name__)


@front_desk_agent.route('/Customers', methods=['GET'])
def get_customers():
    cursor = db.get_db().cursor()
    cursor.execute('select lastName, firstName from Customer;')
    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(row_headers, row)))
    return jsonify(json_data)

# Add customer preferences for a particular userID
@front_desk_agent.route('/Preference/<customerId>', methods=['POST'])
def post_customer_pref(customerId):
    try:
        pref = request.json  # Get the new preferences from the request body
        cursor = db.get_db().cursor()

        # Check if preferences already exist for the customer
        check_query = "SELECT * FROM Preference WHERE customerId = %s;"
        cursor.execute(check_query, (customerId,))
        existing_pref = cursor.fetchone()

        if existing_pref:
            # Preferences already exist, you can choose to update or return a message
            return jsonify({"message": "Preferences already exist for this customer."}), 409
        else:
            # Insert the new preferences into the database
            insert_query = "INSERT INTO Preference (preferences, customerId) VALUES (%s, %s);"
            cursor.execute(insert_query, (json.dumps(pref), customerId))
            db.get_db().commit()  # Commit the transaction

            # Fetch the newly added preferences to return in the response
            cursor.execute("SELECT * FROM Preference WHERE customerId = %s;", (customerId,))
            row_headers = [x[0] for x in cursor.description]
            theData = cursor.fetchall()
            json_data = [dict(zip(row_headers, row)) for row in theData]

            response = make_response(jsonify(json_data))
            response.status_code = 201
            response.mimetype = 'application/json'
            return response

    except Exception as e:
        db.get_db().rollback()  # Rollback in case of any error
        return jsonify({"error": str(e)}), 500

    
@front_desk_agent.route('/bookings', methods=['POST'])
def add_booking():
    try:
        # Extract booking information from request body
        data = request.json
        customer_id = data['customer_id']
        room_num = data['room_num']
        hotel_id = data['hotel_id']
        occupancy_start_date = data['occupancy_start_date']
        occupancy_end_date = data['occupancy_end_date']

        # Validate date order
        if occupancy_start_date >= occupancy_end_date:
            return jsonify({"error": "Occupancy start date must be before end date"}), 400

        # Check if customer exists
        cursor = db.get_db().cursor()
        cursor.execute("SELECT * FROM Customer WHERE CustomerId = %s;", (customer_id,))
        customer = cursor.fetchone()
        if not customer:
            return jsonify({"error": "Customer not found"}), 404

        # Check if room is available
        cursor.execute("""
            SELECT * FROM Booking 
            WHERE RoomNum = %s AND HotelId = %s AND (
                (OccupancyStartDate < %s AND OccupancyEndDate > %s) OR
                (OccupancyStartDate < %s AND OccupancyEndDate > %s)
            )
        """, (room_num, hotel_id, occupancy_end_date, occupancy_start_date, occupancy_start_date, occupancy_end_date))
        booking = cursor.fetchone()
        if booking:
            return jsonify({"error": "Room is not available for the selected dates"}), 400

        # Insert new booking
        cursor.execute("""
            INSERT INTO Booking (RoomNum, HotelId, CustomerId, OccupancyStartDate, OccupancyEndDate) 
            VALUES (%s, %s, %s, %s, %s);
        """, (room_num, hotel_id, customer_id, occupancy_start_date, occupancy_end_date))
        db.get_db().commit()

        return jsonify({"message": "Booking successfully added", "booking_details": data}), 201

    except Exception as e:
        db.get_db().rollback()  # Rollback in case of any error
        return jsonify({"error": str(e)}), 500

# Get all the prefferences for all customers
@front_desk_agent.route('/preferences', methods=['GET'])
def get_preferences():
    try:
        cursor = db.get_db().cursor()
        # Query to select all preferences along with customer information
        query = """
        SELECT Customer.FirstName, Customer.LastName, Preference.Preference
        FROM Customer
        INNER JOIN Preference ON Customer.CustomerId = Preference.CustomerId
        """
        cursor.execute(query)
        row_headers = [x[0] for x in cursor.description]  # this will extract row headers
        results = cursor.fetchall()
        
        # Convert query to json format
        json_data = []
        for result in results:
            json_data.append(dict(zip(row_headers, result)))

        return jsonify(json_data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Delete a customer's preferences    
@front_desk_agent.route('/preferences/<customerID>', methods=['DELETE'])
def delete_customer_preferences(customerID):
    try:
        cursor = db.get_db().cursor()
        
        # First, check if the customer exists
        cursor.execute("SELECT * FROM Customer WHERE CustomerId = %s;", (customerID,))
        customer = cursor.fetchone()
        if not customer:
            return jsonify({"error": "Customer not found"}), 404
        
        # If the customer exists, delete their preferences
        delete_query = "DELETE FROM Preference WHERE CustomerId = %s;"
        cursor.execute(delete_query, (customerID,))
        db.get_db().commit()

        if cursor.rowcount == 0:
            return jsonify({"message": "No preferences found for the customer"}), 404

        return jsonify({"message": "Customer preferences deleted successfully"}), 200
    except Exception as e:
        db.get_db().rollback()  # Rollback in case of any error
        return jsonify({"error": str(e)}), 500
