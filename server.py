from flask import *
from Enigma import Enigma
import secrets, json, base64

app = Flask(__name__)
app.config['SECRET_KEY'] = secrets.token_hex(64)

@app.route("/")
def home():
    return render_template("index.html")


# the data in api endpoints are base64-encoded.
@app.route("/api/encrypt", methods=['POST'])
@app.route("/api/decrypt", methods=['POST'])
def enigma_manipulation():
    encoding = request.json.get('encoding', "latin-1")
    try:
        data = request.json.get('data', "")
        key = request.json.get('key', "")
        if data and key:
            data = base64.b64decode(data).decode(encoding)
            key = base64.b64decode(key).decode(encoding)
        else:
            return jsonify({"error": "Missing data or key"}), 400
        method = request.json.get('method', "")
        enigma = Enigma(password=key, text_encoding=encoding)
        if method == "encrypt":
            return json.dumps({"status": "ok", "result": enigma.cypher_text(data)})
        else:
            return json.dumps({"status": "ok", "result": enigma.decypher_text(data)})
    except Exception as e:
        return jsonify({"status": "error", "result": "Invalid JSON"}), 400

# api endpoint documentation
@app.route("/api/", methods=["GET"])
def api_docs():
    with open("api_docs.json", "r") as f:
        return f.read()


app.run(debug=False)

