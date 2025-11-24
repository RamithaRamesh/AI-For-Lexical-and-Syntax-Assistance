# src/inference.py

import json
import numpy as np
from tensorflow.keras.models import load_model

from src.config import MODEL_DIR
from src.tokenization import tokenize_code_simple
from src.keywords import LANG_KEYWORDS
from src.utils import edit_distance

MODEL_CACHE = {}

def load_language_model(lang: str):
    if lang in MODEL_CACHE:
        return MODEL_CACHE[lang]
    model_path = MODEL_DIR / f"typo_model_{lang}" / "model.keras"
    settings_path = MODEL_DIR / f"typo_model_{lang}" / "model_settings.json"
    model = load_model(model_path)
    settings = json.load(open(settings_path, "r"))
    stoi = settings["stoi"]
    itos = {v: k for k, v in stoi.items()}
    max_len = settings["max_len"]
    MODEL_CACHE[lang] = (model, stoi, itos, max_len)
    return MODEL_CACHE[lang]


def decode_lstm(model, stoi, itos, max_len, word):
    pad = stoi["<pad>"]
    sos = stoi["<sos>"]
    eos = stoi["<eos>"]
    enc = [sos] + [stoi.get(c, pad) for c in word] + [eos]
    enc = enc[:max_len] + [pad] * (max_len - len(enc))
    enc = np.array([enc], dtype=np.int32)
    dec_input = [sos]
    decoded = []

    for step in range(max_len - 1):
        dec_padded = dec_input[:max_len - 1]
        dec_padded = dec_padded + [pad] * (max_len - 1 - len(dec_padded))
        dec_padded = np.array([dec_padded], dtype=np.int32)
        preds = model.predict([enc, dec_padded], verbose=0)
        next_id = int(np.argmax(preds[0, step]))
        if next_id == eos:
            break
        decoded.append(itos.get(next_id, ""))
        dec_input.append(next_id)
        if len(dec_input) >= (max_len - 1):
            break
    return "".join(decoded)


def find_best_keyword(token, language, max_dist=2):
    token = token.lower()
    best_word = None
    best_d = 999
    for kw in LANG_KEYWORDS[language]:
        d = edit_distance(token, kw.lower())
        if d < best_d:
            best_d = d
            best_word = kw
    if best_d <= max_dist:
        return best_word
    return None


def correct_snippet(lang: str, code: str):
    model, stoi, itos, max_len = load_language_model(lang)
    keywords_lower = {k.lower() for k in LANG_KEYWORDS[lang]}
    tokens = tokenize_code_simple(code)
    corrected = []
    for tok in tokens:
        if tok.lower() in keywords_lower:
            corrected.append(tok)
            continue
        pred = decode_lstm(model, stoi, itos, max_len, tok)
        if pred.lower() in keywords_lower:
            corrected.append(pred)
        else:
            corrected.append(tok)
    return " ".join(corrected)
