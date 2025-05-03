from flask import Flask, request, jsonify, send_from_directory, render_template_string
import os
from datetime import datetime

app = Flask(__name__, static_folder='.', static_url_path='')

RESULT_DIR = os.path.join(os.path.dirname(__file__), 'user_results')
os.makedirs(RESULT_DIR, exist_ok=True)

@app.route('/save_result', methods=['POST'])
def save_result():
    data = request.get_json()
    if not data:
        return jsonify({'status': 'fail', 'msg': 'No data received'}), 400
    os.makedirs(RESULT_DIR, exist_ok=True)
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f'user_result_{timestamp}_{os.urandom(3).hex()}.json'
    filepath = os.path.join(RESULT_DIR, filename)
    with open(filepath, 'w', encoding='utf-8') as f:
        import json
        json.dump(data, f, ensure_ascii=False, indent=2)
    return jsonify({'status': 'success', 'filename': filename})

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/<path:filename>')
def static_files(filename):
    return send_from_directory('.', filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)