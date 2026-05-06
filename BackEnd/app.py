import os
from flask import Flask, jsonify, request, redirect, url_for
from flask_cors import CORS

app = Flask(__name__)

CORS(app, origins=os.getenv('CORS', 'http://localhost:3000'))  # Default to localhost:3000 if not set



@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy"}) 

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    












if __name__ == "__main__":
    app.run(debug=True)