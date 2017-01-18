import re
from flask import Flask, request, render_template, session, flash, redirect
from mysqlconnection import MySQLConnector
app = Flask(__name__)
mysql = MySQLConnector(app,'email_valid')
@app.route('/')
def index():

    dis_type = "None"
    dis_type2 = "None"
    query = "SELECT * FROM emails"                           # define your query
    emails = mysql.query_db(query)
    print emails
    return render_template('index.html', emails=emails, dis_type = dis_type, dis_type2 = dis_type2)

@app.route('/email_submit', methods=['POST'])
def create():
    # Write query as a string. Notice how we have multiple values
    # we want to insert into our query.


    query = "INSERT INTO emails (email, created_at, updated_at) VALUES (:email, NOW(), NOW())"
    # We'll then create a dictionary of data from the POST data received.

    data = {
             'email': request.form['email'],
           }

    email_verify = request.form['email']

    email_pattern =  re.match('[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})', email_verify)
    print email_pattern
    if email_pattern == None:
        return render_template('index.html', message = "Enter A Valid Email Address", dis_type2 = "None", dis_type="None")
    else:
        mysql.query_db(query, data)
        query = "SELECT * FROM emails"                           # define your query
        emails = mysql.query_db(query)
    # if request.form['email'] ==
    # Run query, with dictionary values injected into the query.
    return render_template('index.html', emails = emails, dis_type2 = " ", dis_type = " ")

# @app.route('/email_submit/<email_id>')
# def show(email_id):
#     # Write query to select specific user by id. At every point where
#     # we want to insert data, we write ":" and variable name.
#     query = "SELECT * FROM emails WHERE id = :specific_id"
#     # Then define a dictionary with key that matches :variable_name in query.
#     data = {'specific_id': email_id}
#     # Run query with inserted data.
#     emails = mysql.query_db(query, data)
#     # Friends should be a list with a single object,
#     # so we pass the value at [0] to our template under alias one_friend.
#     return render_template('index.html', one_friend=emails[0])

@app.route('/truncate')
def trunc():
    query = "truncate TABLE emails;"
    mysql.query_db(query)
    return redirect('/')
app.run(debug=True)
