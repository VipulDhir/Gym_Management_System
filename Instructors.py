import mysql
from flask import request,jsonify


def insert_data_to_database(instructor_id, instructor_name, specialty, contact_info, instructor_fees, duration_in_months):
    try:
        cnx = mysql.connector.connect(user='root', password='1234', host='localhost', database='Fitness')
        cursor = cnx.cursor()
        qry = "INSERT INTO Instructors (instructor_id, instructor_name, specialty, contact_info, instructor_fees, duration_in_months) VALUES (%s, %s, %s, %s, %s, %s)"
        data = (instructor_id, instructor_name, specialty, contact_info, instructor_fees, duration_in_months)
        cursor.execute(qry, data)
        cnx.commit()
        cursor.close()
        cnx.close()
        return True
    except mysql.connector.Error as err:
        print(err)
        return False


def add_instructor():
    try:
        request_data = request.get_json()
        instructor_id = request_data['instructor_id']
        instructor_name = request_data['instructor_name']
        specialty = request_data['specialty']
        contact_info = request_data['contact_info']
        instructor_fees = request_data['instructor_fees']
        duration_in_months = request_data['duration_in_months']

        if insert_data_to_database(instructor_id, instructor_name, specialty, contact_info, instructor_fees, duration_in_months):
            return jsonify({"message": "Instructor added successfully."})
        else:
            return jsonify({"message": "Failed to add instructor."}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 400


def fetch_data_by_specialty(specialty):
    try:
        cnx = mysql.connector.connect(user='root', password='1234', host='localhost', database='Fitness')
        cursor = cnx.cursor()

        # Fetch data using specialty
        qry = "SELECT * FROM Instructors WHERE specialty = %s"
        cursor.execute(qry, (specialty,))
        data = cursor.fetchall()

        cursor.close()
        cnx.close()

        return data

    except mysql.connector.Error as err:
        print(err)
        return None


# Your Flask route to fetch data by instructor specialty
def get_instructor_by_specialty():
    try:
        request_data = request.get_json()
        specialty = request_data['specialty']

        if not specialty:
            return jsonify({"error": "specialty is required in the request body."}), 400

        data = fetch_data_by_specialty(specialty)

        if data:
            columns = ['instructor_id', 'instructor_name', 'specialty', 'contact_info', 'instructor_fees', 'duration_in_months']
            records = [dict(zip(columns, row)) for row in data]
            return jsonify({"data": records})
        else:
            return jsonify({"message": "No data found."}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 500


def get_possible_combinations():
    try:
        request_data = request.get_json()
        specialty = request_data['specialty']
        plan_name = request_data['plan_name']
        budget = request_data['budget']

        if not specialty or not plan_name or budget is None:
            return jsonify({"error": "specialty, plan_name, and budget are required in the request body."}), 400

        cnx = mysql.connector.connect(user='root', password='1234', host='localhost', database='Fitness')
        cursor = cnx.cursor()

        # Fetch instructors and plans within the budget
        qry = "SELECT i.instructor_id, i.instructor_name, i.specialty, i.instructor_fees, mp.plan_id, mp.plan_name, mp.duration_in_months, mp.plan_cost FROM Instructors i, MembershipPlans mp WHERE i.specialty = %s AND mp.plan_name = %s AND i.instructor_fees + mp.plan_cost <= %s"
        cursor.execute(qry, (specialty, plan_name, budget))
        data = cursor.fetchall()

        cursor.close()
        cnx.close()

        columns = ['instructor_id', 'instructor_name', 'specialty', 'instructor_fees', 'plan_id', 'plan_name', 'duration_in_months', 'plan_cost']
        records = [dict(zip(columns, row)) for row in data]

        return jsonify({"combinations": records})

    except mysql.connector.Error as err:
        print(err)
        return jsonify({"error": "An error occurred while processing your request."}), 500

