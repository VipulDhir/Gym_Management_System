import mysql.connector


def DatabaseCreate():
    cnx=mysql.connector.connect(user='root',password='1234',host='localhost')
    Cursor=cnx.cursor()
    Cursor.execute("CREATE DATABASE IF NOT EXISTS Fitness")
    Cursor.execute("")
    Cursor.close()
    cnx.close()


def TablesCreate():
    cnx=mysql.connector.connect(user='root',password='1234',host='localhost',database='Fitness')
    Cursor=cnx.cursor()
    Cursor.execute(
        "CREATE TABLE IF NOT EXISTS ProductRecord(P_id int(2), Pname varchar(20), Category varchar(20), Price int(10),Qty int(2))")
    Cursor.execute(
        "CREATE TABLE IF NOT EXISTS Member(Mno int(2), Mname varchar(20), Date_of_Buying Date, Addr varchar(24), Mob varchar(10))")
    Cursor.execute("CREATE TABLE IF NOT EXISTS Price(P_id int(2), Mno int(2), Total_Price int(15))")
    Cursor.close()
    cnx.close()
