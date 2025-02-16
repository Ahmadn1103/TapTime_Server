from flask import Flask, request, jsonify 
import requests
from datetime import datetime

app = Flask ('TapTime')

GOOGLE_SHEETS_URL = "https://script.google.com/macros/s/AKfycbyPKl3rK-TvfqVMVqnQFtkXf9FFHTqIZRIo92nnIHxFOI9Jt7eBe283uY2BV67_50Hl/exec"

@app.route('/clock', methods=['POST'])
def clock_in_out():
    data = request.json
    data["time"] = datetime.now().isoformat()

    response = requests.post(GOOGLE_SHEETS_URL, json=data)
    if response.status_code == 200:
        return jsonify({"message": "Success"}), 200
    return jsonify({"message": "Error"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)