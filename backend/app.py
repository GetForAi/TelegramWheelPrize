from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os

app = Flask(__name__)
CORS(app)

BALANCE_FILE = 'balances.json'

# Загружаем или создаём пустой файл
def load_balances():
    if not os.path.exists(BALANCE_FILE):
        return {}
    with open(BALANCE_FILE, 'r') as f:
        return json.load(f)

def save_balances(data):
    with open(BALANCE_FILE, 'w') as f:
        json.dump(data, f)

@app.route('/balance/<user_id>', methods=['GET'])
def get_balance(user_id):
    data = load_balances()
    return jsonify({'balance': data.get(user_id, 100)})

@app.route('/balance/<user_id>', methods=['POST'])
def update_balance(user_id):
    data = load_balances()
    json_data = request.get_json()
    amount = json_data.get('balance')
    data[user_id] = amount
    save_balances(data)
    return jsonify({'status': 'ok', 'balance': amount})

if __name__ == '__main__':
    app.run(debug=True)

