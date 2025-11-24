# src/keywords.py

LANG_KEYWORDS = {
    "python": [
        "if","else","elif","print","for","while","return","def","input",
        "int","float","str","True","False","None","and","or","len",
        "range","break","continue","is","in","not","try","except",
        "finally","class","import","from","as","with","lambda","global",
        "nonlocal","pass","raise","yield","assert","async","await","del"
    ],

    "java": [
        "public","class","static","void","main","String","if","else","for",
        "while","return","int","float","boolean","try","catch","import",
        "package","new","this","extends","implements","throws","interface",
        "private","protected","final","abstract","continue","default","switch",
        "case","break","double","char","long","short","byte","super","null"
    ],

    "c": [
        "int","float","if","else","for","while","return","printf","scanf",
        "include","define","char","void","main","switch","case","break",
        "malloc","free","sizeof","struct","typedef","double","long","short",
        "unsigned","const","static","extern","NULL"
    ]
}

VALID_KEYWORDS = {lang: {kw.lower() for kw in kws} for lang, kws in LANG_KEYWORDS.items()}