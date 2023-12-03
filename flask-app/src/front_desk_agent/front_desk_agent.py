from flask import Blueprint, request, jsonify, make_response
import json
from src import db


front_desk_agent = Blueprint('front_desk_agent', __name__)

# Update customer preferences with a particular userID
@front_desk_agent.route('/Customer/<customerId>', methods=['PUT'])
def put_customer_pref(userID):
    try:
        pref = request.json  # Get the new preferences from the request body
        cursor = db.get_db().cursor()

        # Update the customer's preferences in the database
        update_query = "UPDATE Customers SET preferences = %s WHERE customerId = %s"
        cursor.execute(update_query, (json.dumps(pref), customerId))

        db.get_db().commit()  # Commit the transaction

        # Fetch the updated customer data to return in the response
        cursor.execute("SELECT * FROM Customers WHERE customerId = %s", (customerId,))
        row_headers = [x[0] for x in cursor.description]
        theData = cursor.fetchall()
        json_data = [dict(zip(row_headers, row)) for row in theData]

        response = make_response(jsonify(json_data))
        response.status_code = 200
        response.mimetype = 'application/json'
        return response
    except Exception as e:
        db.get_db().rollback()  # Rollback in case of any error
        return jsonify({"error": str(e)}), 500
    

@front_desk_agent.route('/bookings/new', methods=['POST'])
def add_booking():
    try:
        # Extract booking information from request body
        data = request.json
        customer_id = data['customer_id']
        room_num = data['room_num']
        hotel_id = data['hotel_id']
        occupancy_start_date = data['occupancy_start_date']
        occupancy_end_date = data['occupancy_end_date']
        
        # Check if customer exists
        cursor = db.get_db().cursor()
        cursor.execute("SELECT * FROM Customer WHERE CustomerId = %s", (customer_id,))
        customer = cursor.fetchone()
        if not customer:
            return jsonify({"error": "Customer not found"}), 404

        # Check if room is available
        cursor.execute("""
            SELECT * FROM Booking 
            WHERE RoomNum = %s AND HotelId = %s AND (
                (%s BETWEEN OccupancyStartDate AND OccupancyEndDate) OR 
                (%s BETWEEN OccupancyStartDate AND OccupancyEndDate)
            )
        """, (room_num, hotel_id, occupancy_start_date, occupancy_end_date))
        booking = cursor.fetchone()
        if booking:
            return jsonify({"error": "Room is not available for the selected dates"}), 400

        # Insert new booking
        cursor.execute("""
            INSERT INTO Booking (RoomNum, HotelId, CustomerId, OccupancyStartDate, OccupancyEndDate) 
            VALUES (%s, %s, %s, %s, %s)
        """, (room_num, hotel_id, customer_id, occupancy_start_date, occupancy_end_date))
        db.get_db().commit()

        return jsonify({"message": "Booking successfully added"}), 201
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

# Delete a customers preferences    
@front_desk_agent.route('/preferences/<customerID>', methods=['DELETE'])
def delete_customer_preferences(customerID):
    try:
        cursor = db.get_db().cursor()
        
        # First, check if the customer exists
        cursor.execute("SELECT * FROM Customer WHERE CustomerId = %s", (customerID,))
        customer = cursor.fetchone()
        if not customer:
            return jsonify({"error": "Customer not found"}), 404
        
        # If the customer exists, delete their preferences
        delete_query = "DELETE FROM Preference WHERE CustomerId = %s"
        cursor.execute(delete_query, (customerID,))
        db.get_db().commit()

        if cursor.rowcount == 0:
            return jsonify({"message": "No preferences found for the customer"}), 404

        return jsonify({"message": "Customer preferences deleted successfully"}), 200
    except Exception as e:
        db.get_db().rollback()  # Rollback in case of any error
        return jsonify({"error": str(e)}), 500