from flask import Flask, jsonify, request
import jwt
import datetime
import uuid

app = Flask(__name__)

SECRET_KEY = "secret"
ALGORITHM = "HS256"
#curl -X POST http://localhost:5000/token
@app.route("/token", methods=["POST"])
def generate_token():
    payload = {
        "jti": str(uuid.uuid1()),
        "user_id": 1,
        "exp": datetime.datetime.now(datetime.UTC) + datetime.timedelta(minutes=5)
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    return jsonify({"token": token})
#curl -H "Token: <token>" http://localhost:5000/protected
@app.route("/protected", methods=["GET", "POST"])
def protected():
    # Get token from custom header "Token" or query parameter
    token = request.headers.get("Token") 
    
    if not token:
        return jsonify({"error": "Missing token"}), 401

    try:
        decoded = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return jsonify({"message": "Access granted", "user": decoded["user_id"]})
    except Exception as e:
        return jsonify({"error": "Invalid token"}), 401

if __name__ == "__main__":
    app.run(debug=True)