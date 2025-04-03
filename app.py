import os
from flask import Flask, request, jsonify, render_template
from deep_translator import GoogleTranslator

app = Flask(__name__)

# Supported languages
SUPPORTED_LANGUAGES = {"en", "es", "fr", "de", "it", "pt", "hi"}

@app.route("/")
def welcome():
    return render_template("welcome.html")

@app.route("/translator")
def translator():
    return render_template("index.html")

@app.route("/translate", methods=["POST"])
def translate():
    try:
        data = request.get_json()

        if not data:
            return jsonify({"error": "Invalid request. Please send JSON data."}), 400

        text = data.get("text", "").strip()
        source_lang = data.get("source_lang")
        target_lang = data.get("target_lang")

        if not text:
            return jsonify({"error": "Text cannot be empty."}), 400
        if source_lang not in SUPPORTED_LANGUAGES or target_lang not in SUPPORTED_LANGUAGES:
            return jsonify({"error": "Unsupported language selected."}), 400

        translated_text = GoogleTranslator(source=source_lang, target=target_lang).translate(text)
        return jsonify({"translated_text": translated_text})

    except Exception as e:
        return jsonify({"error": f"Translation failed: {str(e)}"}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))  # Use Render's assigned PORT
    app.run(host="0.0.0.0", port=port)
