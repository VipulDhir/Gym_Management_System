import Database
from flask import Flask

from Members import insert_member,delete_member,update_member,search_member
from Price import calculate_total_price,get_total_price
from Product import add_data,delete_data,get_data,update_data

app=Flask(__name__)

Database.DatabaseCreate()
Database.TablesCreate()

# API FROM PRODUCT.py
app.add_url_rule('/add_data',view_func=add_data,methods=['POST'])
app.add_url_rule('/get_data',view_func=get_data,methods=['GET'])
app.add_url_rule('/delete_data',view_func=delete_data,methods=['DELETE'])
app.add_url_rule('/update_data',view_func=update_data,methods=['PUT'])

# API FROM MEMBERS.py
app.add_url_rule('/insert_member',view_func=insert_member,methods=['POST'])
app.add_url_rule('/delete_member',view_func=delete_member,methods=['POST'])
app.add_url_rule('/update_member',view_func=update_member,methods=['PUT'])
app.add_url_rule('/search_member',view_func=search_member,methods=['GET'])

# API FROM PRICE.py
app.add_url_rule('/calculate_total_price',view_func=calculate_total_price,methods=['POST'])
app.add_url_rule('/get_total_price',view_func=get_total_price,methods=['GET'])


@app.route('/')
def hello_world():
    return 'This is my first API call!'


if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')
