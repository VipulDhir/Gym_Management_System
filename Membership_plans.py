import mysql
from flask import request,jsonify


def insert_membership_plan_to_database(plan_id, plan_name, duration_in_months, plan_cost, description):
    try:
        cnx = mysql.connector.connect(user='root', password='1234', host='localhost', database='Fitness')
        cursor = cnx.cursor()
        qry = "INSERT INTO MembershipPlans (plan_id, plan_name, duration_in_months, plan_cost, description) VALUES (%s, %s, %s, %s, %s)"
        data = (plan_id, plan_name, duration_in_months, plan_cost, description)
        cursor.execute(qry, data)
        cnx.commit()
        cursor.close()
        cnx.close()
        return True
    except mysql.connector.Error as err:
        print(err)
        return False


def add_membership_plan():
    try:
        request_data = request.get_json()
        plan_id = request_data['plan_id']
        plan_name = request_data['plan_name']
        duration_in_months = request_data['duration_in_months']
        plan_cost = request_data['plan_cost']
        description = request_data['description']

        if insert_membership_plan_to_database(plan_id, plan_name, duration_in_months, plan_cost, description):
            return jsonify({"message": "Membership plan added successfully."})
        else:
            return jsonify({"message": "Failed to add membership plan."}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 400


def fetch_data_by_plan_name(plan_name):
    try:
        cnx = mysql.connector.connect(user='root', password='1234', host='localhost', database='Fitness')
        cursor = cnx.cursor()

        # Fetch data using plan_name
        qry = "SELECT * FROM MembershipPlans WHERE plan_name = %s"
        cursor.execute(qry, (plan_name,))
        data = cursor.fetchall()

        cursor.close()
        cnx.close()

        return data

    except mysql.connector.Error as err:
        print(err)
        return None


# Your Flask route to fetch data by plan name
def get_plan_by_name():
    try:
        request_data = request.get_json()
        plan_name = request_data['plan_name']

        if not plan_name:
            return jsonify({"error": "plan_name is required in the request body."}), 400

        data = fetch_data_by_plan_name(plan_name)

        if data:
            columns = ['plan_id', 'plan_name', 'duration_in_months', 'plan_cost', 'description']
            records = [dict(zip(columns, row)) for row in data]
            return jsonify({"data": records})
        else:
            return jsonify({"message": "No data found."}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 500