import mysql.connector
from flask import request,jsonify
import random


def insert_data_to_database(P_id, Pname, Category, Price, Qty, Machine_level):
    try:
        cnx = mysql.connector.connect(user='root', password='1234', host='localhost', database='Fitness')
        cursor = cnx.cursor()
        qry = "INSERT INTO ProductRecord (P_id, Pname, Category, Price, Qty , Machine_level) VALUES (%s, %s, %s, %s, %s ,%s)"
        data = (P_id, Pname, Category, Price, Qty, Machine_level)
        cursor.execute(qry, data)
        cnx.commit()
        cursor.close()
        cnx.close()
        return True
    except mysql.connector.Error as err:
        print(err)
        return False


def add_data():
    try:
        request_data = request.get_json()
        P_id = request_data['P_id']
        Pname = request_data['Pname']
        Category = request_data['Category']
        Price = request_data['Price']
        Qty = request_data['Qty']
        Machine_level =request_data['Machine_level']

        if insert_data_to_database(P_id, Pname, Category, Price, Qty, Machine_level):
            return jsonify({"message": "Record Inserted successfully."})
        else:
            return jsonify({"message": "Failed to insert record."}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 400


def fetch_data_from_database():
    try:
        cnx = mysql.connector.connect(user='root', password='1234', host='localhost', database='Fitness')
        cursor = cnx.cursor()
        qry = "SELECT * FROM ProductRecord"
        cursor.execute(qry)
        data = cursor.fetchall()
        cursor.close()
        cnx.close()
        return data
    except mysql.connector.Error as err:
        print(err)
        return None


def get_data():
    data = fetch_data_from_database()
    if data:
        columns = ['P_id', 'Pname', 'Category', 'Price', 'Qty','Machine_level']
        records = [dict(zip(columns, row)) for row in data]
        return jsonify({"data": records})
    else:
        return jsonify({"message": "Failed to fetch data."}), 500


def delete_data_from_database(P_id):
    try:
        cnx = mysql.connector.connect(user='root', password='1234', host='localhost', database='Fitness')
        cursor = cnx.cursor()
        qry = "DELETE FROM ProductRecord WHERE P_id = %s"
        del_rec = (P_id,)
        cursor.execute(qry, del_rec)
        cnx.commit()
        cursor.close()
        cnx.close()
        return cursor.rowcount
    except mysql.connector.Error as err:
        print(err)
        return -1


def delete_data():
    try:
        request_data = request.get_json()
        P_id = request_data['P_id']

        if not P_id:
            return jsonify({"message": "P_id is required in the request body."}), 400

        rows_deleted = delete_data_from_database(P_id)

        if rows_deleted > 0:
            return jsonify({"message": f"{rows_deleted} record(s) deleted successfully."})
        elif rows_deleted == 0:
            return jsonify({"message": "No records found to delete."}), 404
        else:
            return jsonify({"message": "Failed to delete record."}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 400


def update_data():
    try:
        data = request.get_json()
        P_id = data.get('P_id')
        Pname = data.get('Pname')
        Category = data.get('Category')
        Price = data.get('Price')
        Qty = data.get('Qty')
        Machine_level =data.get('Machine_level')

        cnx = mysql.connector.connect(user='root',password='1234',host='localhost',database='Fitness')
        cursor = cnx.cursor()
        query = "SELECT * FROM ProductRecord WHERE P_id = %s"
        cursor.execute(query, (P_id,))
        product = cursor.fetchone()

        if product:
            qry = "UPDATE ProductRecord SET Pname=%s, Category=%s, Price=%s, Qty=%s , Machine_level=%s WHERE P_id=%s"
            data = (Pname, Category, Price, Qty, Machine_level, P_id)
            cursor.execute(qry, data)
            cnx.commit()
            cursor.close()
            cnx.close()
            return jsonify({"message": "Record updated successfully."}), 200
        else:
            return jsonify({"message": "Product not found."}), 404

    except mysql.connector.Error as err:
        print(err)
        return jsonify({"error": "An error occurred while processing your request."}), 500

def get_machines_by_budget_and_level():
    try:
        data = request.get_json()
        machine_level = data.get('machine_level')
        budget = data.get('budget')

        if machine_level is None or budget is None:
            return jsonify({"error": "machine_level and budget are required in the request body."}), 400

        return get_machines_within_budget(machine_level, budget)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

def get_machines_within_budget(machine_level, budget):
    try:
        cnx = mysql.connector.connect(user='root', password='1234', host='localhost', database='Fitness')
        cursor = cnx.cursor()
        qry = "SELECT * FROM ProductRecord WHERE Machine_level = %s AND Price <= %s"
        data = (machine_level, budget)
        cursor.execute(qry, data)
        machines = cursor.fetchall()
        cursor.close()
        cnx.close()

        filtered_machines = []
        columns = ['P_id', 'Pname', 'Machine_level', 'Price']

        for machine in machines:
            filtered_machines.append(dict(zip(columns, machine)))

        selected_machines = []
        total_cost = 0

        while total_cost <= budget and filtered_machines:
            machine = random.choice(filtered_machines)
            machine_cost = machine['Price']
            if total_cost + machine_cost <= budget:
                selected_machines.append(machine)
                total_cost += machine_cost
            filtered_machines.remove(machine)

        if not selected_machines:
            return jsonify({"message": "No machines found within the given budget and level."}), 404

        return jsonify(selected_machines), 200

    except mysql.connector.Error as err:
        print(err)
        return jsonify({"error": "An error occurred while processing your request."}), 500


