from flask import Flask, request, jsonify
from Members import fetch_member_from_database
import mysql.connector


# API endpoint to calculate and update the total price for a product and member
def calculate_total_price():
    try:
        data = request.get_json()
        P_id = data.get('P_id')
        Mno = data.get('Mno')

        if P_id is None or Mno is None:
            return jsonify({"error": "P_id and Mno are required in the request body."}), 400

        cnx = mysql.connector.connect(user='root', password='1234', host='localhost', database='Fitness')
        cursor = cnx.cursor()
        qry = "SELECT Price, Qty FROM ProductRecord WHERE P_id = %s"
        cursor.execute(qry, (P_id,))
        product = cursor.fetchone()

        if not product:
            return jsonify({"error": "Product not found."}), 404

        price, quantity = product

        members_data = fetch_member_from_database()
        print(members_data)
        member_found = False

        for member in members_data:
            if member[0] == Mno:
                member_found = True
                break

        if not member_found:
            return jsonify({"error": "Member not found."}), 404

        total_price = price * quantity

        qry = "INSERT INTO Price (P_id, Mno, Total_Price) VALUES (%s, %s, %s) ON DUPLICATE KEY UPDATE Total_Price=%s"
        data = (P_id, Mno, total_price, total_price)
        cursor.execute(qry, data)
        cnx.commit()
        cursor.close()
        cnx.close()
        return jsonify({"P_id": P_id, "Mno": Mno, "Total_Price": total_price}), 200

    except mysql.connector.Error as err:
        print(err)
        return jsonify({"error": "An error occurred while processing your request."}), 500


# API endpoint to get the total price for all products and members
def get_total_price():
    try:
        cnx = mysql.connector.connect(user='root', password='1234', host='localhost', database='Fitness')
        cursor = cnx.cursor()
        qry = "SELECT * FROM Price"
        cursor.execute(qry)
        data = cursor.fetchall()
        cursor.close()
        cnx.close()
        return jsonify({"data": data})

    except mysql.connector.Error as err:
        print(err)
        return jsonify({"error": "An error occurred while fetching data."}), 500