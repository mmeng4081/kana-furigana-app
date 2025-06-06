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
        try:
            reading = word.feature[6]  # 第 7 欄通常是 Reading
        except IndexError:
            reading = ""
        if reading and reading != surface:
            result += f"<ruby>{surface}<rt>{reading}</rt></ruby>"
        else:
            result += surface
    return jsonify({"html": result})

if __name__ == "__main__":
    app.run(debug=False)
