# src/typo_generator.py

import csv
import random
import string
from pathlib import Path
from typing import List, Tuple
from src.config import DATASET_DIR
from src.keywords import LANG_KEYWORDS

keyboard_neighbors = {
    'a': 'qwsz','b': 'vghn','c': 'xdfv','d': 'serfcx','e': 'wsdr','f': 'rtgvcd',
    'g': 'tyhbvf','h': 'yujnbg','i': 'ujko','j': 'uikmnh','k': 'iolmj','l': 'kop',
    'm': 'njk','n': 'bhjm','o': 'iklp','p': 'ol','q': 'wa','r': 'edft','s': 'awedxz',
    't': 'rfgy','u': 'yhji','v': 'cfgb','w': 'qesa','x': 'zsdc','y': 'tghu','z': 'asx'
}

ALPHABET = string.ascii_lowercase

def replace_with_neighbor(ch: str) -> str:
    low = ch.lower()
    if low in keyboard_neighbors:
        choice = random.choice(keyboard_neighbors[low])
        return choice.upper() if ch.isupper() else choice
    return random.choice(ALPHABET)

def generate_typo(word: str) -> str:
    ops = ["swap_adjacent","delete","insert_neighbor","replace_neighbor",
           "replace_random","double_char","transpose","case_change"]
    op = random.choice(ops)
    s = list(word)

    try:
        if op == "swap_adjacent":
            if len(s) > 1:
                i = random.randint(0, len(s)-2)
                s[i], s[i+1] = s[i+1], s[i]

        elif op == "delete":
            if len(s) > 0:
                del s[random.randint(0, len(s)-1)]

        elif op == "insert_neighbor":
            idx = random.randint(0, len(s))
            ch = s[idx-1] if idx > 0 else random.choice(ALPHABET)
            s.insert(idx, replace_with_neighbor(ch))

        elif op == "replace_neighbor":
            i = random.randint(0, len(s)-1)
            s[i] = replace_with_neighbor(s[i])

        elif op == "replace_random":
            i = random.randint(0, len(s)-1)
            s[i] = random.choice(ALPHABET)

        elif op == "double_char":
            i = random.randint(0, len(s)-1)
            s.insert(i, s[i])

        elif op == "transpose":
            if len(s) > 1:
                i, j = random.sample(range(len(s)), 2)
                s[i], s[j] = s[j], s[i]

        elif op == "case_change":
            i = random.randrange(len(s))
            s[i] = s[i].upper() if s[i].islower() else s[i].lower()

    except:
        pass

    typo = "".join(s)
    return typo if typo != word else typo + random.choice(ALPHABET)

def make_typos_for_word(word: str, count: int) -> List[str]:
    typos = set()
    while len(typos) < count:
        t = generate_typo(word)
        if t != word:
            typos.add(t)
    return list(typos)

def generate_lang_dataset(lang: str):
    pairs = []
    for kw in LANG_KEYWORDS[lang]:
        typos = make_typos_for_word(kw, 40)
        for t in typos:
            pairs.append((t, kw))
    return pairs

def create_csv_datasets():
    for lang in LANG_KEYWORDS:
        pairs = generate_lang_dataset(lang)
        path = DATASET_DIR / f"typo_data_{lang}.csv"
        with open(path, "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow(["typo","correct"])
            w.writerows(pairs)
        print(f"[✓] {lang}: {len(pairs)} samples → {path}")