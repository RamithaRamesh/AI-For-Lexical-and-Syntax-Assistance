from flask import Flask, request, jsonify
from flask_cors import CORS

from src.inference import load_language_model, decode_lstm, find_best_keyword
from src.tokenization import tokenize_code_simple
from src.keywords import LANG_KEYWORDS as KEYWORD_DATABASE
from src.utils import edit_distance

app = Flask(__name__)
CORS(app)

LANGUAGES = ["python", "java", "c"]

@app.route("/api/checkcode", methods=["POST"])
def check_code():
    data = request.json or {}
    user_code = data.get("code", "")
    language = data.get("language", "").lower()

    if language == "cplusplus":
        language = "c"

    if language not in LANGUAGES:
        return jsonify({"error": "Unsupported language"}), 400

    if not user_code.strip():
        return jsonify({"error": "Empty code"}), 400

    model, stoi, itos, max_len = load_language_model(language)
    valid_keywords = {kw.lower() for kw in KEYWORD_DATABASE[language]}

    errors = []
    lines = user_code.splitlines()

    for line_num, line in enumerate(lines, start=1):
        tokens = tokenize_code_simple(line)

        for tok in tokens:
            t = tok.lower()

            if t in valid_keywords:
                continue
            if not tok.isalpha():
                continue

            prediction = decode_lstm(model, stoi, itos, max_len, tok)
            best_kw = find_best_keyword(tok, language)

            final = None
            if prediction.lower() in valid_keywords:
                final = prediction
            elif best_kw:
                final = best_kw

            if final and final.lower() != t:
                errors.append({
                    "line": line_num,
                    "typo": tok,
                    "suggestion": final
                })

    return jsonify({"errors": errors})

if __name__ == "__main__":
    print("Starting Flask backend...")
    app.run(host="127.0.0.1", port=5001, debug=True)