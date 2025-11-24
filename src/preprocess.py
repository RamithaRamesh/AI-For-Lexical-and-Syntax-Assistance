# src/preprocess.py

import json
import csv
import numpy as np
from pathlib import Path
from typing import Dict, Tuple
from src.config import DATASET_DIR, PROCESSED_DIR, MAX_LEN
from src.keywords import LANG_KEYWORDS

def build_vocab(csv_path: Path) -> Tuple[Dict[str,int], Dict[int,str]]:
    chars = set()
    with open(csv_path, "r", encoding="utf-8") as f:
        r = csv.reader(f)
        next(r)
        for t, c in r:
            chars.update(list(t))
            chars.update(list(c))
    chars = sorted(chars)
    vocab = ["<pad>","<sos>","<eos>"] + chars
    stoi = {ch:i for i,ch in enumerate(vocab)}
    itos = {i:ch for i,ch in enumerate(vocab)}
    return stoi, itos

def encode(s: str, stoi: Dict[str,int], max_len=MAX_LEN):
    seq = [stoi["<sos>"]] + [stoi.get(ch, stoi["<pad>"]) for ch in s] + [stoi["<eos>"]]
    seq = seq[:max_len] + [stoi["<pad>"]] * max(0, max_len - len(seq))
    return seq

def preprocess_all():
    for lang in LANG_KEYWORDS:
        csv_path = DATASET_DIR / f"typo_data_{lang}.csv"
        stoi, itos = build_vocab(csv_path)

        X = []
        Yin = []
        Yout = []

        with open(csv_path, "r", encoding="utf-8") as f:
            r = csv.reader(f)
            next(r)
            for typo, corr in r:
                enc_t = encode(typo, stoi)
                enc_c = encode(corr, stoi)

                X.append(enc_t)
                Yin.append(enc_c[:-1])
                Yout.append(enc_c[1:])

        X = np.array(X, dtype=np.int32)
        Yin = np.array(Yin, dtype=np.int32)
        Yout = np.array(Yout, dtype=np.int32)

        np.save(PROCESSED_DIR / f"{lang}_X.npy", X)
        np.save(PROCESSED_DIR / f"{lang}_Yin.npy", Yin)
        np.save(PROCESSED_DIR / f"{lang}_Yout.npy", Yout)

        json.dump(stoi, open(PROCESSED_DIR / f"{lang}_stoi.json","w"), indent=2)
        json.dump(itos, open(PROCESSED_DIR / f"{lang}_itos.json","w"), indent=2)

        print(f"[✓] Processed {lang}: X={X.shape}, Yin={Yin.shape}, Yout={Yout.shape}")