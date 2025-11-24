# src/tokenization.py
import re

def tokenize_code_simple(code: str):
    return re.findall(r"[A-Za-z_][A-Za-z0-9_]*|==|!=|>=|<=|->|[-+*/=<>]|[0-9]+|[:;(){}.,]", code)