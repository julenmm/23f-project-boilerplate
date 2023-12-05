from flask import Blueprint, request, jsonify, make_response
import json
from src import db


hotel_manager = Blueprint('hotel manager', __name__)

# Get all employee from the DB
@hotel_manager.route('/employee', methods=['GET'])
def get_employee():
    try:
        cursor = db.get_db().cursor()
        cursor.execute('SELECT lastName, firstName, employeeId FROM Employee;')
        row_headers = [x[0] for x in cursor.description]
        json_data = []
        theData = cursor.fetchall()
        for row in theData:
            json_data.append(dict(zip(row_headers, row)))
        return jsonify(json_data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# Get all employees and phonenumber
@hotel_manager.route('/employee_number', methods=['GET'])
def get_employees_phone_number():
    try:
        cursor = db.get_db().cursor()
        cursor.execute('SELECT lastName, firstName, employeeId, phoneNumber FROM Employee;')
        row_headers = [x[0] for x in cursor.description]
        json_data = []
        theData = cursor.fetchall()
        for row in theData:
            json_data.append(dict(zip(row_headers, row)))
        return jsonify(json_data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Delete customer detail for customer with particular userID
@hotel_manager.route('/delete_employee', methods=['DELETE'])
def delete_employee():
    try:
        req_data = request.get_json()
        employee_Id = req_data['employeeId']
        cursor = db.get_db().cursor()
        delete_employee_stmt = 'DELETE FROM Employee WHERE employeeId = %s'
        cursor.execute(delete_employee_stmt, (employee_Id,))
        db.get_db().commit()
        return "Deleted Successfully"
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# add an employee  
@hotel_manager.route('/add_employee', methods=['PUT'])
def add_employee():
    cursor = db.get_db().cursor()
    try:
        # Extract employee information from request body
        data = request.get_json()
        phoneNumber = data.get("phoneNumber")
        weeklyHours = data.get("weeklyHours")
        approvedDaysOff = data.get("approvedDaysOff")
        requestedDaysOffStart = data.get("requestedDaysOffStart")
        requestedDaysOffEnd = data.get("requestedDaysOffEnd")
        firstName = data.get("firstName")  # Make sure the key matches exactly with the JSON key
        lastName = data.get("lastName")
        hourlyPay = data.get("hourlyPay")
        role = data.get("role")
        hotelId = data.get("hotelId")

        # Insert new employee - Make sure the number of %s placeholders matches the number of columns
        cursor.execute("""
            INSERT INTO Employee (phoneNumber, weeklyHours, approvedDaysOff, requestedDaysOffStart, requestedDaysOffEnd, firstName, lastName, hourlyPay, role, hotelId) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
        """, (phoneNumber, weeklyHours, approvedDaysOff, requestedDaysOffStart, requestedDaysOffEnd, firstName, lastName, hourlyPay, role, hotelId))
        db.get_db().commit()

        return jsonify({"message": "Employee successfully added", "information": data}), 201

    except Exception as e:
        db.get_db().rollback()  # Rollback in case of any error
        return jsonify({"error": str(e)}), 500

# delete an employee
@hotel_manager.route('/delete_employee', methods=['DELETE'])
def delete_customer():
    try:
        cursor = db.get_db().cursor()
        
        # Extract booking information from request body
        data = request.json
        employeeId = data['employeeId']

        # First, check if the employee exists
        cursor.execute("SELECT * FROM Employee WHERE employeeId = %s;", employeeId)
        employee = cursor.fetchone()
        if not employee:
            return jsonify({"error": "Employee not found"}), 404
        
        # If the Employee exists, delete their preferences
        delete_query = "DELETE FROM Employee WHERE employeeId = %s;"
        cursor.execute(delete_query, employeeId)
        db.get_db().commit()

        if cursor.rowcount == 0:
            return jsonify({"message": "No Employee with that id found"}), 404

        return jsonify({"message": "Employee deleted successfully"}), 200
    except Exception as e:
        db.get_db().rollback()  # Rollback in case of any error
        return jsonify({"error": str(e)}), 500
    

# get shift 
@hotel_manager.route('/shift', methods=['GET'])
def get_shift():
    try:
        cursor = db.get_db().cursor()
        cursor.execute('SELECT timeOff, dateTimeEnd, employeeId, dateTimeStart FROM Shift;')
        row_headers = [x[0] for x in cursor.description]
        json_data = []
        theData = cursor.fetchall()
        for row in theData:
            json_data.append(dict(zip(row_headers, row)))
        return jsonify(json_data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500



@hotel_manager.route('/add_shift', methods=['POST'])
def add_employee_shift():
    try:
        data = request.get_json()  # Get JSON data from the request body
        if not data or 'employeeId' not in data or 'dateTimeStart' not in data or 'dateTimeEnd' not in data:
            return jsonify({"error": "Required data not provided"}), 400

        employee_id = data['employeeId']  # Extract employeeId from JSON
        new_start_time = data['dateTimeStart']  # Extract new shift start time from JSON
        new_end_time = data['dateTimeEnd']  # Extract new shift end time from JSON

        cursor = db.get_db().cursor()

        # Insert a new shift
        insert_query = "INSERT INTO Shift (employeeId, dateTimeStart, dateTimeEnd) VALUES (%s, %s, %s);"
        cursor.execute(insert_query, (employee_id, new_start_time, new_end_time))
        db.get_db().commit()  # Commit the transaction

        message = "Shift added successfully."

        # Fetch the added shift
        check_query = "SELECT * FROM Shift WHERE employeeId = %s AND dateTimeStart = %s;"
        cursor.execute(check_query, (employee_id, new_start_time))
        row_headers = [x[0] for x in cursor.description]  # Extract row headers
        theData = cursor.fetchall()
        json_data = [dict(zip(row_headers, row)) for row in theData]

        response = make_response(jsonify({"message": message, "data": json_data}), 201)
        response.mimetype = 'application/json'
        return jsonify(json_data)

    except Exception as e:
        db.get_db().rollback()  # Rollback in case of any error
        return jsonify({"error": str(e)}), 500
