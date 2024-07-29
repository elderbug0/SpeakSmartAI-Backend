from flask import Flask, request, jsonify
from global_router import global_router
from logger import logger
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

# Middleware
@app.before_request
def log_request():  
    logger()

# Register Blueprints
app.register_blueprint(global_router, url_prefix='/api/v1')

@app.route('/api/v1/status', methods=['GET'])
def get_status():
    try:
        with open('process.txt', 'r') as file:
            status = file.read()
        return jsonify({'status': status})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)
