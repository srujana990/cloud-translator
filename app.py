import os
from flask import Flask, request, jsonify, render_template
from deep_translator import GoogleTranslator
from langdetect import detect
import re

app = Flask(__name__)

# Supported target languages
SUPPORTED_LANGUAGES = {
    "en", "es", "fr", "de", "it", "pt", "hi", "te", "kn"
}

def is_valid_text(text):
    if not any(c.isalpha() for c in text):
        return False
    alpha_count = sum(c.isalpha() for c in text)
    return alpha_count >= 5

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
        target_lang = data.get("target_lang")

        if not text:
            return jsonify({"error": "Text cannot be empty."}), 400
        if not is_valid_text(text):
            return jsonify({"error": "Enter a proper text to translate."}), 400
        if target_lang not in SUPPORTED_LANGUAGES:
            return jsonify({"error": "Unsupported target language selected."}), 400

        detected_lang = detect(text)

        if detected_lang == target_lang:
            return jsonify({"error": "Source and target languages cannot be the same."}), 400

        translated_text = GoogleTranslator(source=detected_lang, target=target_lang).translate(text)

        return jsonify({
            "translated_text": translated_text,
            "detected_lang": detected_lang
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
