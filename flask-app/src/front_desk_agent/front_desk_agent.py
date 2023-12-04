from flask import Blueprint, request, jsonify, make_response
import json
from src import db


front_desk_agent = Blueprint('front_desk_agent', __name__)


@front_desk_agent.route('/Customers', methods=['GET'])
def get_customers():
    cursor = db.get_db().cursor()
    cursor.execute('select lastName, firstName, customerId from Customer;')
    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(row_headers, row)))
    return jsonify(json_data)

@front_desk_agent.route('/Preference', methods=['POST'])
def post_customer_pref():
    try:
        data = request.get_json()  # Get JSON data from the request body
        if not data or 'customerId' not in data or 'preference' not in data:
            return jsonify({"error": "Required data not provided"}), 400

        customerId = data['customerId']  # Extract customerId from JSON
        pref = data['preference']  # Extract preference from JSON

        cursor = db.get_db().cursor()

        # Check if preferences already exist for the customer
        check_query = "SELECT * FROM Preference WHERE customerId = %s;"
        cursor.execute(check_query, (customerId,))
        existing_pref = cursor.fetchone()

        if existing_pref:
            # Preferences already exist, update them
            update_query = "UPDATE Preference SET preference = %s WHERE customerId = %s;"
            cursor.execute(update_query, (pref, customerId))
            db.get_db().commit()  # Commit the transaction
            message = "Preferences updated successfully."
        else:
            # Insert the new preferences into the database
            insert_query = "INSERT INTO Preference (preference, customerId) VALUES (%s, %s);"
            cursor.execute(insert_query, (pref, customerId))
            db.get_db().commit()  # Commit the transaction
            message = "Preferences added successfully."

        # Fetch the updated preferences
        cursor.execute("SELECT * FROM Preference WHERE customerId = %s;", (customerId,))
        row_headers = [x[0] for x in cursor.description]
        theData = cursor.fetchall()
        json_data = [dict(zip(row_headers, row)) for row in theData]

        response = make_response(jsonify({"message": message, "data": json_data}), 200)
        response.mimetype = 'application/json'
        return response

    except Exception as e:
        db.get_db().rollback()  # Rollback in case of any error
        return jsonify({"error": str(e)}), 500


# add a customer  
@front_desk_agent.route('/addCustomer', methods=['PUT'])
def add_customer():
    cursor = db.get_db().cursor()
    try:
        # Extract booking information from request body
        data = request.json
        phone_numeber = data['phoneNumber']
        most_recent_stay = data['mostRecentStay']
        first_name = data['firstName']
        last_name = data['lastName']

        # Insert new booking
        cursor.execute("""
            INSERT INTO Customer (phoneNumber, mostRecentStay, firstName, lastName) 
            VALUES (%s, %s, %s, %s);
        """, (phone_numeber, most_recent_stay, first_name, last_name))
        db.get_db().commit()

        return jsonify({"message": "Customer successfully added", "booking_details": data}), 201

    except Exception as e:
        db.get_db().rollback()  # Rollback in case of any error
        return jsonify({"error": str(e)}), 500

# Get all the prefferences for all customers
@front_desk_agent.route('/get-preferences', methods=['GET'])
def get_preferences():
    cursor = db.get_db().cursor()
    cursor.execute('select customerId, preference from Preference;')
    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(row_headers, row)))
    return jsonify(json_data)

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
