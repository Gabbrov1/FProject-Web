import os
from flask import Flask, jsonify, request, redirect, url_for
from flask_cors import CORS
from DBhelper import *


def create_app():
    app = Flask(__name__)
    CORS(app, origins=os.getenv('CORS', 'http://localhost:3000'))  # Default to localhost:3000 if not set
    global SQLDB
    global MONGODB
    
    SQLDB = DBHelper(db_type=db_Types.MSSQL)
    MONGODB = DBHelper(db_type=db_Types.POSTGRESQL)
    
    return app

app = create_app()

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy"}) 




@app.route('/auth/login/', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    with (SQLDB.connect()):
        user = SQLDB.get_user_by_username(username)
        if user and SQLDB.check_password(password, user['password']):
            return jsonify({"message": "Login successful", "user_id": user['id']}), 200
        else:
            return jsonify({"message": "Invalid username or password"}), 401

    












if __name__ == "__main__":
    app.run(debug=True)