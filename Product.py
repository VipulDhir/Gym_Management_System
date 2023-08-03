import mysql.connector
from flask import request,jsonify


def insert_data_to_database(P_id, Pname, Category, Price, Qty):
    try:
        cnx = mysql.connector.connect(user='root', password='1234', host='localhost', database='Fitness')
        cursor = cnx.cursor()
        qry = "INSERT INTO ProductRecord (P_id, Pname, Category, Price, Qty) VALUES (%s, %s, %s, %s, %s)"
        data = (P_id, Pname, Category, Price, Qty)
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

        if insert_data_to_database(P_id, Pname, Category, Price, Qty):
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
        columns = ['P_id', 'Pname', 'Category', 'Price', 'Qty']
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

