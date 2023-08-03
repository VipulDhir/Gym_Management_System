import Database
from flask import Flask

from Product import add_data,delete_data,get_data

app = Flask(__name__)


Database.DatabaseCreate()
Database.TablesCreate()

app.add_url_rule('/add_data',view_func=add_data,methods=['POST'])
app.add_url_rule('/get_data',view_func=get_data,methods=['GET'])
app.add_url_rule('/delete_data',view_func=delete_data,methods=['DELETE'])


@app.route('/')
def hello_world():
    return 'This is my first API call!'


if __name__ == '__main__':
    app.run(debug=True)