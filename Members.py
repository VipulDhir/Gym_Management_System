from flask import request, jsonify
from mysql.connector import errorcode
import mysql.connector
from datetime import date,datetime,timedelta


def insert_member():
    try:
        data = request.get_json()
        mno = data.get('mno')
        mname = data.get('mname')
        addr = data.get('addr')
        mob = data.get('mob')

        cnx = mysql.connector.connect(user='root', password='1234', host='localhost', database='Fitness')
        cursor = cnx.cursor()
        qry = "INSERT INTO Member VALUES(%s, %s, %s, %s)"
        data = (mno, mname, addr, mob)
        cursor.execute(qry, data)
        cnx.commit()
        cursor.close()
        cnx.close()
        return jsonify({"message": "Record Inserted."}), 200

    except mysql.connector.Error as err:
        if err.errno == mysql.connector.errorcode.ER_ACCESS_DENIED_ERROR:
            return jsonify({"error": "Something is wrong with your user name or password"}), 500
        elif err.errno == mysql.connector.errorcode.ER_BAD_DB_ERROR:
            return jsonify({"error": "Database does not exist"}), 500
        else:
            return jsonify({"error": str(err)}), 500


def delete_member_from_database(mno):
    if not mno:
        return "Member Code (mno) is missing or empty."

    try:
        cnx = mysql.connector.connect(user='root', password='1234', host='localhost', database='Fitness')
        cursor = cnx.cursor()
        qry = """DELETE FROM Member WHERE MNO = %s"""
        del_rec = (mno,)
        cursor.execute(qry, del_rec)
        cnx.commit()
        cursor.close()
        cnx.close()
        return cursor.rowcount, "Record(s) Deleted Successfully."
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            return "Something is wrong with your user name or password"
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            return "Database does not exist"
        else:
            return str(err)


def delete_member():
    data = request.get_json()
    if 'mno' in data:
        mno = data['mno']
        result = delete_member_from_database(mno)
        return jsonify({"result": result})
    else:
        return jsonify({"error": "Member Code (mno) not provided."}), 400


def update_member_from_database(data):
    try:
        cnx=mysql.connector.connect(user='root',password='1234',host='localhost',database='Fitness')
        cursor=cnx.cursor()

        mno=data['mno']
        mname=data['mname']
        addr=data['addr']
        mob=data['mob']

        query="SELECT * FROM member WHERE mno = %s"
        rec_srch=(mno,)
        cursor.execute(query,rec_srch)

        if not cursor.fetchall():
            return "Member with provided Member Code not found."

        qry="UPDATE member SET mname=%s, addr=%s, mob=%s WHERE mno=%s"
        data=(mname,addr,mob,mno)
        cursor.execute(qry,data)
        cnx.commit()
        cursor.close()
        cnx.close()

        return cursor.rowcount,"Record(s) Updated Successfully."
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            return "Something is wrong with your user name or password"
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            return "Database does not exist"
        else:
            return str(err)


def update_member():
    data=request.get_json()
    if 'mno' in data and 'mname' in data and 'addr' in data and 'mob' in data:
        result=update_member_from_database(data)
        return jsonify({"result": result})
    else:
        return jsonify({"error": "Required data missing."}),400


def fetch_member_from_database():
    try:
        cnx = mysql.connector.connect(user='root', password='1234', host='localhost', database='Fitness')
        cursor = cnx.cursor()
        qry = "SELECT * FROM Member"
        cursor.execute(qry)
        data = cursor.fetchall()
        cursor.close()
        cnx.close()
        return data
    except mysql.connector.Error as err:
        print(err)
        return None


def search_member():
    data = fetch_member_from_database()
    if data:
        columns = ['mno', 'mname', 'addr','mob']
        records = [dict(zip(columns, row)) for row in data]
        return jsonify({"data": records})
    else:
        return jsonify({"message": "Failed to fetch data."}), 500

