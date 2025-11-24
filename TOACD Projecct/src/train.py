# src/train.py

import json
import numpy as np
from pathlib import Path
from sklearn.model_selection import train_test_split
from src.config import PROCESSED_DIR, MODEL_DIR, MAX_LEN
from src.keywords import LANG_KEYWORDS
from src.model import build_seq2seq

def train_language(lang: str):
    X = np.load(PROCESSED_DIR / f"{lang}_X.npy")
    Yin = np.load(PROCESSED_DIR / f"{lang}_Yin.npy")
    Yout = np.load(PROCESSED_DIR / f"{lang}_Yout.npy")
    stoi = json.load(open(PROCESSED_DIR / f"{lang}_stoi.json"))
    vocab_size = len(stoi)
    Yout = np.expand_dims(Yout, -1)
    Xtr, Xval, Yin_tr, Yin_val, Yout_tr, Yout_val = train_test_split(
        X, Yin, Yout, test_size=0.15, random_state=42
    )
    model = build_seq2seq(vocab_size, MAX_LEN)
    model.fit([Xtr, Yin_tr], Yout_tr,
              validation_data=([Xval, Yin_val], Yout_val),
              epochs=30, batch_size=64, verbose=2)
    out_dir = MODEL_DIR / f"typo_model_{lang}"
    out_dir.mkdir(exist_ok=True)
    model.save(out_dir / "model.keras")
    json.dump({"stoi": stoi, "max_len": MAX_LEN}, open(out_dir / "model_settings.json","w"), indent=2)
    print(f"[✓] Saved model for {lang}: {out_dir}")