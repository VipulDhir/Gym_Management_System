import uuid
import mysql
from flask import jsonify,request


def add_to_cart():
    try:
        data = request.get_json()
        P_id = data.get('P_id')
        Mno = data.get('Mno')
        cart_id = data.get('cart_id')  # Provide your desired cart_id value
        quantity_bought = data.get('quantity_bought')  # Get the desired quantity

        if P_id is None or Mno is None or cart_id is None or quantity_bought is None:
            return jsonify({"error": "P_id, Mno, cart_id, and quantity_bought are required in the request body."}), 400

        cnx = mysql.connector.connect(user='root', password='1234', host='localhost', database='Fitness')
        cursor = cnx.cursor()

        # Fetch product data using P_id
        qry_product = "SELECT * FROM ProductRecord WHERE P_id = %s"
        cursor.execute(qry_product, (P_id,))
        product = cursor.fetchone()

        if not product:
            return jsonify({"error": "Product not found."}), 404

        # Fetch member data using Mno
        qry_member = "SELECT * FROM Member WHERE Mno = %s"
        cursor.execute(qry_member, (Mno,))
        member = cursor.fetchone()

        if not member:
            return jsonify({"error": "Member not found."}), 404

        # Insert data into Cart table
        qry_insert = "INSERT INTO Cart (Cart_id, P_id, Mno, Quantity_bought) VALUES (%s, %s, %s, %s)"
        data_insert = (cart_id, P_id, Mno, quantity_bought)  # Use the provided quantity
        cursor.execute(qry_insert, data_insert)
        cnx.commit()
        cursor.close()
        cnx.close()

        return jsonify({"message": "Product added to cart successfully.", "cart_id": cart_id}), 200

    except mysql.connector.Error as err:
        print(err)
        return jsonify({"error": "An error occurred while processing your request."}), 500