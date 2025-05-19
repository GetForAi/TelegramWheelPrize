from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os
import threading
import hmac
import hashlib

app = Flask(__name__)
CORS(app)

TOKEN = "ТВОЙ_ТОКЕН_ОТ_Бота"  # <-- вставь сюда актуальный токен от BotFather
BALANCE_FILE = 'balances.json'

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

def check_telegram_auth(data):
    check_hash = data.pop("hash")
    auth_data = [f"{k}={v}" for k, v in sorted(data.items())]
    data_check_string = "\n".join(auth_data)
    secret_key = hashlib.sha256(TOKEN.encode()).digest()
    hmac_string = hmac.new(secret_key, data_check_string.encode(), hashlib.sha256).hexdigest()
    return hmac_string == check_hash

@app.route("/auth", methods=["POST"])
def auth():
    data = request.json
    if not check_telegram_auth(data.copy()):
        return jsonify({"error": "unauthorized"}), 401
    user = {
        "id": data["id"],
        "username": data.get("username", "")
    }
    return jsonify({"ok": True, "user": user})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
