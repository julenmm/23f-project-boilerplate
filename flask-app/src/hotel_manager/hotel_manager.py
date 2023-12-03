from flask import Blueprint, request, jsonify, make_response
import json
from src import db


hotel_manager = Blueprint('hotel manager', __name__)

# Get all customers from the DB
@hotel_manager.route('/Customers', methods=['GET'])
def get_customers():
    cursor = db.get_db().cursor()
    cursor.execute('select lastName, firstName, customerId from Customer;')
    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(row_headers, row)))
    return json_data

# Get all em from the DB
@hotel_manager.route('/Employee', methods=['GET'])
def get_employees():
    cursor = db.get_db().cursor()
    cursor.execute('select lastName, firstName, employeeId from Employee;')
    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(row_headers, row)))
    return json_data


# Delete customer detail for customer with particular userID
@hotel_manager.route('/delete_employee', methods=['DELETE'])
def delete_employee():
    req_data = request.get_json()
    employee_Id = req_data['employeeId']
    cursor = db.get_db().cursor()
    delete_employee_stmt = 'DELETE FROM Employee WHERE employeeId = ' + str(employee_Id)
    cursor.execute(delete_employee_stmt)
    # Commit the changes to the database
    db.get_db().commit()
    # Return a success message
    return "Deleted Successfully"
