from datetime import datetime, timedelta

import mysql.connector
from flask import jsonify, request


def add_to_orders():
    try:
        data = request.get_json()
        P_id = data.get('P_id')
        Mno = data.get('Mno')
        order_id = data.get('order_id')
        order_date = data.get('order_date')
        cart_id = data.get('cart_id')

        if P_id is None or Mno is None or order_date is None or cart_id is None:
            return jsonify({"error": "P_id, Mno, order_date, and cart_id are required in the request body."}), 400

        cnx = mysql.connector.connect(user='root', password='1234', host='localhost', database='Fitness')
        cursor = cnx.cursor()

        # Fetch the quantity_bought and P_id from Cart table using cart_id
        qry_cart = "SELECT Quantity_bought, P_id FROM Cart WHERE Cart_id = %s"
        cursor.execute(qry_cart, (cart_id,))
        cart_data = cursor.fetchone()

        if not cart_data:
            return jsonify({"error": "Cart data not found."}), 404

        quantity_bought = cart_data[0]
        cart_product_id = cart_data[1]

        # Fetch product data using P_id from Cart table
        qry_product = "SELECT * FROM ProductRecord WHERE P_id = %s"
        cursor.execute(qry_product, (cart_product_id,))
        product = cursor.fetchone()

        if not product:
            return jsonify({"error": "Product not found."}), 404

        # Fetch member data using Mno
        qry_member = "SELECT * FROM Member WHERE Mno = %s"
        cursor.execute(qry_member, (Mno,))
        member = cursor.fetchone()

        if not member:
            return jsonify({"error": "Member not found."}), 404

        # Calculate the total price based on quantity bought and product price
        total_price = product[3] * quantity_bought

        # Insert data into Orders table
        qry_insert = "INSERT INTO Orders (Order_id, cart_id, Mno, P_id,  Order_date, Quantity_bought, Total_Price) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        data_insert = (order_id,cart_id, Mno, cart_product_id, order_date, quantity_bought, total_price)
        cursor.execute(qry_insert, data_insert)
        cnx.commit()
        cursor.close()
        cnx.close()

        return jsonify({"message": "Order added successfully.", "order_id": order_id}), 200

    except mysql.connector.Error as err:
        print(err)
        return jsonify({"error": "An error occurred while processing your request."}), 500


def get_last_3_months_orders():
    try:
        mno=request.args.get('mno')

        if mno is None:
            return jsonify({"error": "mno is required as a query parameter."}),400

        cnx=mysql.connector.connect(user='root',password='1234',host='localhost',database='Fitness')
        cursor=cnx.cursor()

        three_months_ago=(datetime.now() - timedelta(days=90)).date()

        qry="SELECT * FROM Orders WHERE Mno = %s AND Order_date >= %s"
        data=(mno,three_months_ago)
        cursor.execute(qry,data)
        orders=cursor.fetchall()
        cursor.close()
        cnx.close()

        if not orders:
            return jsonify({"message": "No orders found within the last 3 months for the member."}),404

        columns=['Order_id','Mno','P_id','Order_date','Quantity_bought','Total_Price']
        records=[dict(zip(columns,row)) for row in orders]

        return jsonify({"data": records}),200

    except mysql.connector.Error as err:
        print(err)
        return jsonify({"error": "An error occurred while processing your request."}),500
