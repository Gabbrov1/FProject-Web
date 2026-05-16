import os
from flask import Flask, json, jsonify, request, redirect, url_for
from flask_cors import CORS
from DBhelper import *


import AuthHelper as auth
from embedingsHelper import CodeEmbeddingDB





def create_app():
    app = Flask(__name__)
    CORS(app, origins=["http://localhost:4321"])
    global SQLDB
    global MONGODB
    global VECTORDB
    
    SQLDB = DBHelper(db_type=db_Types.MSSQL)
    MONGODB = DBHelper(db_type=db_Types.POSTGRESQL)
    VECTORDB = CodeEmbeddingDB()
    if os.path.exists("./Saves/embedingSaves.pickle.gz"):
        VECTORDB.load()  # only load if file exists
    
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
        if user and auth.check_password(password, user['password']):
            return jsonify({"message": "Login successful", "user_id": user['id'], "username":user['username']}), 200
        else:
            return jsonify({"message": "Invalid username or password"}), 401
        
        

@app.route('/upload/', methods=['POST'])
def upload_json():
    
    # Bunch of checks to see if the file is the right type
    # Check if it's a file upload
    if 'file' in request.files:
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        try:
            data = json.load(file)
        except json.JSONDecodeError:
            return jsonify({'error': 'Invalid JSON file'}), 400
    elif request.is_json:
        body = request.get_json()
        data = body.get("files", [])
    else:
        return jsonify({'error': 'No JSON data or file provided'}), 400  
    
    VECTORDB.upload(data)
    
    return({"result":"Data Saved."}),200


@app.route("/api/query", methods=["GET"])
def query_route():
    q = request.args.get("q")
    if not q:
        return jsonify({"error": "No query provided"}), 400

    raw = VECTORDB.query(q)
    results = [
        {
            "name": doc["name"],
            "source": doc["source"],
            "similarity": float(sim)  # convert float32 to Python float
        }
        for doc, sim in raw
    ]
    return jsonify({"results": results})


if __name__ == "__main__":
    app.run(debug=True)