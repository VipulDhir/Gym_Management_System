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
        "CREATE TABLE IF NOT EXISTS ProductRecord(P_id int(2) PRIMARY KEY, Pname varchar(20), Category varchar(20), Price int(10),Qty int(2), Machine_level varchar(20) )")
    Cursor.execute(
        "CREATE TABLE IF NOT EXISTS Member(Mno int(2) PRIMARY KEY , Mname varchar(20), Addr varchar(24), Mob varchar(10))")
    Cursor.execute(
        "CREATE TABLE IF NOT EXISTS Orders(Order_id int(2) PRIMARY KEY , Cart_id int(2) ,Mno int(2), P_id int(2), Order_date DATE, Quantity_bought int(2),Total_Price int(15) , FOREIGN KEY (Mno) REFERENCES Member(mno), FOREIGN KEY (P_id) REFERENCES ProductRecord(P_id) , FOREIGN KEY (Cart_id) REFERENCES Cart(Cart_id))")
    Cursor.execute("CREATE TABLE IF NOT EXISTS Cart(Cart_id int(2) PRIMARY KEY , P_id int(2), Mno int(2), Quantity_bought int(2), FOREIGN KEY (Mno) REFERENCES Member(mno), FOREIGN KEY (P_id) REFERENCES ProductRecord(P_id))")
    Cursor.execute("CREATE TABLE IF NOT EXISTS MembershipPlans ( plan_id int(2) PRIMARY KEY, plan_name VARCHAR(50), duration_in_months  int(2) , plan_cost int(15) , description TEXT )")
    Cursor.execute("CREATE TABLE IF NOT EXISTS Instructors ( instructor_id int(2) PRIMARY KEY, instructor_name VARCHAR(50), instructor_fees int(10) ,duration_in_months int(2), specialty VARCHAR(50), contact_info VARCHAR(100))")
    Cursor.close()
    cnx.close()