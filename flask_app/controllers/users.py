from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
from flask_app.models.user import User

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=["POST"])
def register():
    data = {
            'first_name':request.form['first_name'],
            'last_name':request.form['last_name'],
            'email':request.form['email'],
            'password':request.form['password'],
            'confirm':request.form['confirm']
        }
    if User.validate(data) == True:
        pw_hash = bcrypt.generate_password_hash(request.form['password'])
        data.update({'password':pw_hash})
        User.add_user(data)
        return ("success")
    else:
        return redirect('/')

@app.route('/log_in', methods=["POST"])
def log_in():
    data={
        'email':request.form['email']
    }
    user = User.log_in(data)
    if bcrypt.check_password_hash(user.password, request.form['password']):
        session['user_id'] = user.id
        return ("logged in")
    else:
        return ("FAIL")
