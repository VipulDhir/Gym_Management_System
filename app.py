import Database

from Cart import add_to_cart
from Instructors import add_instructor,get_instructor_by_specialty,get_possible_combinations
from Members import insert_member,delete_member,update_member,search_member
from Membership_plans import add_membership_plan,get_plan_by_name
from Orders import add_to_orders,get_last_3_months_orders
from Product import add_data,delete_data,get_data,update_data,get_machines_by_budget_and_level


from flask import Flask, redirect, url_for, request
from google_auth_oauthlib.flow import Flow


app=Flask(__name__)

Database.DatabaseCreate()
Database.TablesCreate()

# API FROM PRODUCT.py
app.add_url_rule('/add_data',view_func=add_data,methods=['POST'])
app.add_url_rule('/get_data',view_func=get_data,methods=['GET'])
app.add_url_rule('/delete_data',view_func=delete_data,methods=['DELETE'])
app.add_url_rule('/update_data',view_func=update_data,methods=['PUT'])
app.add_url_rule('/get_machines_by_budget_and_level',view_func=get_machines_by_budget_and_level,methods=['POST'])


# API FROM MEMBERS.py
app.add_url_rule('/insert_member',view_func=insert_member,methods=['POST'])
app.add_url_rule('/delete_member',view_func=delete_member,methods=['DELETE'])
app.add_url_rule('/update_member',view_func=update_member,methods=['PUT'])
app.add_url_rule('/search_member',view_func=search_member,methods=['GET'])


# API FROM CART.py
app.add_url_rule('/add_to_cart',view_func=add_to_cart,methods=['POST'])


# API FROM ORDERS.py
app.add_url_rule('/add_to_orders',view_func=add_to_orders,methods=['POST'])
app.add_url_rule('/get_last_3_months_orders',view_func=get_last_3_months_orders,methods=['GET'])


# API FROM MEMBERSHIP_PLANS.py
app.add_url_rule('/add_membership_plan',view_func=add_membership_plan,methods=['POST'])
app.add_url_rule('/get_plan_by_name',view_func=get_plan_by_name,methods=['GET'])


# API FROM INSTRUCTOR.py
app.add_url_rule('/add_instructor',view_func=add_instructor,methods=['POST'])
app.add_url_rule('/get_instructor_by_specialty',view_func=get_instructor_by_specialty,methods=['GET'])
app.add_url_rule('/get_possible_combinations',view_func=get_possible_combinations,methods=['POST'])


# Replace these with your client ID and secret

CLIENT_ID = 'ur client id'
CLIENT_SECRET = 'ur client secret'
REDIRECT_URI = 'http://localhost:5000/callback'


import os
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'


@app.route('/')
def home():
    flow = Flow.from_client_secrets_file(
        'client_secret.json',  # Path to your OAuth credentials JSON file
        scopes=['openid', 'profile', 'email'],
        redirect_uri=REDIRECT_URI
    )

    authorization_url, _ = flow.authorization_url(
        access_type='offline',
        prompt='consent'
    )
    return redirect(authorization_url)


@app.route('/callback')
def callback():
    flow = Flow.from_client_secrets_file(
        'client_secret.json',  # Path to your OAuth credentials JSON file
        scopes=None,
        redirect_uri=REDIRECT_URI
    )

    flow.fetch_token(
        authorization_response=request.url
    )

    credentials = flow.credentials

    # You can now use 'credentials' to access Google APIs

    return "Logged in successfully!"


# @app.route('/')
# def hello_world():
#     return 'This is my first API call!'


if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')
