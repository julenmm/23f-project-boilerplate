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

# Get all employee from the DB
@hotel_manager.route('/Employee', methods=['GET'])
def get_employee():
    cursor = db.get_db().cursor()
    cursor.execute('select lastName, firstName, employeeId from Employee;')
    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(row_headers, row)))
    return json_data


# Get all em and phonenumber
@hotel_manager.route('/Employee_number', methods=['GET'])
def get_employees_phone_number():
    cursor = db.get_db().cursor()
    cursor.execute('select lastName, firstName, employeeId, phoneNumber from Employee;')
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


@hotel_manager.route('/add_employee', methods=['POST'])
def add_employee(employeeId):
    # get the new emloyee details from the request
    employeeId = request.json.get("add_employeeId", None) 
    firstName = request.json.get("add_firstname", None)
    lastName = request.json.get("add_lastname", None)
    phoneNumber = request.json.get("add_phoneNumber", None)
    weeklyHours = request.json.get("add_weeklyHours", None) 
    hourlypay = request.json.get("add_hourlyPay", None) 

    # get a cursor object from the database
    cursor = db.get_db().cursor()
    # construct the insert statement
    insert_stmt = 'INSERT INTO Employee (employeeId, firstName, lastName, phoneNumber, weeklyHours, hourlypay) VALUES (' + str(employeeId) + ', "' + firstName + '", "'+ lastName + '", "' + str(phoneNumber) + ', ' + str(weeklyHours)+ ', ' + str(hourlypay) + ')'
    # execute the query
    cursor.execute(insert_stmt)
    # commit the changes to the database
    db.get_db().commit()

    # return a success message
    return "employee added successfully"