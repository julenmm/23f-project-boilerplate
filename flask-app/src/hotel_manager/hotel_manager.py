from flask import Blueprint, request, jsonify, make_response
import json
from src import db


hotel_manager = Blueprint('hotel manager', __name__)

# Get all customers from the DB
@hotel_manager.route('/Customers', methods=['GET'])
def get_customers():
    cursor = db.get_db().cursor()
    cursor.execute('select lastName, firstName from Customer;')
    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(row_headers, row)))
    return json_data

# Get customer detail for customer with particular userID
@hotel_manager.route('/Customers/<customerId>', methods=['GET'])
def get_customer(customerId):
    cursor = db.get_db().cursor()
    # Use parameterized queries to prevent SQL injection
    query = 'SELECT * FROM customers WHERE id = %s'
    cursor.execute(query, (customerId,))
    row_headers = [x[0] for x in cursor.description]  # this will extract row headers
    json_data = []
    theData = cursor.fetchall()
    for result in theData:
        json_data.append(dict(zip(row_headers, result)))
    # Use jsonify to return a proper JSON response
    return jsonify(json_data)
