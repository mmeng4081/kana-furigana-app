
from flask import Flask, request, jsonify, send_from_directory
import fugashi

tagger = fugashi.Tagger()
app = Flask(__name__)

@app.route("/")
def index():
    return send_from_directory('.', 'index.html')

@app.route("/convert", methods=["POST"])
def convert():
    data = request.get_json()
    text = data.get("text", "")
    words = tagger(text)
    result = ""
    for word in words:
        surface = word.surface
        reading = word.feature.get("Reading") or ""
        if reading and reading != surface:
            result += f"<ruby>{surface}<rt>{reading}</rt></ruby>"
        else:
            result += surface
    return jsonify({"html": result})

if __name__ == "__main__":
    app.run(debug=False)
