from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

class User:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def add_user(cls,data):
        query="INSERT INTO users(first_name,last_name,email,password) VALUES (%(first_name)s,%(last_name)s,%(email)s,%(password)s)"
        return connectToMySQL('users').query_db( query, data)

    @classmethod
    def validate(cls,data):
        valid = True
        query="SELECT * FROM users WHERE email = %(email)s"
        results = connectToMySQL('users').query_db( query, data )
        if len(results) >= 1:
            flash("Email already taken.","register")
            valid = False
        if len(data['first_name']) < 3:
            flash("First name must be at least 3 characters","register")
            valid =  False
        if len(data['last_name']) < 3:
            flash("Last name must be at least 3 characters","register")
            valid =  False
        if len(data['password']) < 8:
            flash("Password must be at least 8 characters","register")
            valid =  False
        if data['password'] != data['confirm']:
            flash("Passwords don't match","register")
            valid = False
        return valid

    @classmethod
    def log_in(cls,data):
        query="SELECT * FROM users WHERE email = %(email)s"
        results = connectToMySQL('users').query_db( query, data )
        return cls(results[0])
        
