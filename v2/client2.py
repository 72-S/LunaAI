from flask import Flask, request, jsonify, render_template
import requests

app = Flask(__name__)

API_URL = "http://127.0.0.1:5000/api/post"  # Replace with your actual API endpoint

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/send', methods=['POST'])
def send():
    data = request.json
    transcription = data.get('transcription')
    payload = {"prompt": transcription}
    try:
        response = requests.post(API_URL, json=payload)
        response.raise_for_status()
        return jsonify(response.json())
    except requests.exceptions.RequestException as e:
        return jsonify({"response": "Error connecting to API.", "speech": ""})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4000, debug=True)
