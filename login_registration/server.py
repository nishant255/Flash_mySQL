from flask import Flask, request, redirect, render_template, session, flash
from mysqlconnection import MySQLConnector
from flask.ext.bcrypt import Bcrypt

import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

app = Flask(__name__)
bcrypt = Bcrypt(app)
app.secret_key = 'ThisIsLoginKey'
mysql = MySQLConnector(app,'the_wall')

# ==============================================================================
#                                   Render
# ==============================================================================

@app.route('/')
def index():
    print session.get('login')
    if session.get('login') == True:
        return render_template('success.html')

    return render_template('index.html')

@app.route('/register')
def register():

    return render_template('registration.html')

@app.route('/registration', methods=['POST'])
def registration():

    if len(request.form['first_name']) < 3:
        print len(request.form['first_name'])
        flash("First Name cannot be less than 3 Characters")
        return redirect('/register')

    elif len(request.form['last_name']) < 3:
        flash("Last Name cannot be less than 3 Characters")
        return redirect('/register')

    elif len(request.form['email']) < 5:
        flash("Email cannot be less than 5 Characters")
        return redirect('/register')

    elif not EMAIL_REGEX.match(request.form['email']):
        flash("Invalid Email Address")
        return redirect('/register')

    elif len(request.form['pass']) < 4:
        flash("Password Should be 4 or More Characters")
        return redirect('/register')

    elif request.form['pass'] != request.form['passconf']:
        flash("Password doesn't match")
        return redirect('/register')

    else:
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        password = request.form['pass']
        pw_hash = bcrypt.generate_password_hash(password)

        insert_query = "INSERT INTO wall (first_name, last_name, email, pw_hash, created_at) VALUES (:first_name, :last_name, :email, :pw_hash, NOW())"

        query_data = {
            'first_name': first_name,
            'last_name': last_name,
            'email': email,
            'pw_hash': pw_hash
        }
        mysql.query_db(insert_query, query_data)
        session['login'] = True

    return render_template('success.html')

@app.route('/login', methods=['POST'])
def login():

    if len(request.form['email']) < 5:
        flash("Email cannot be less than 5 Characters")
        return redirect('/')

    elif not EMAIL_REGEX.match(request.form['email']):
        flash("Invalid Email Address")
        return redirect('/')

    elif len(request.form['pass']) < 4:
        flash("Invalid Password")
        return redirect('/')

    else:
        email = request.form['email']
        password = request.form['pass']
        user_query = "SELECT * FROM wall WHERE email = :email LIMIT 1"
        query_data = { 'email': email }
        user = mysql.query_db(user_query, query_data)
        if bcrypt.check_password_hash(user[0]['pw_hash'], password):
            session['login'] = True
            print "Login"
        else:
            flash("Invalid Email or Password")
            return redirect('/')
    print session.get('login')
    return render_template('success.html')

# ==============================================================================
#                                   Process
# ==============================================================================

@app.route('/logout')
def logout():
    session.pop('login', None)

    return redirect('/')

app.run(debug=True)
