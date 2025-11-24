# src/utils.py

def reconstruct(tokens):
    out = ""
    no_space_before = {",",";",":",")","]","}","."}
    no_space_after = {"(","[","{"}
    ops = set("+-*/=%<>!&|")

    for i,t in enumerate(tokens):
        if i == 0:
            out += t
            continue
        prev = tokens[i-1]

        if t in no_space_before:
            out += t; continue
        if prev in no_space_after:
            out += t; continue
        if any(ch in ops for ch in t):
            out += " " + t; continue

        out += " " + t
    return out

def edit_distance(a, b):
    la, lb = len(a), len(b)
    dp = [[0] * (lb + 1) for _ in range(la + 1)]

    for i in range(la + 1):
        dp[i][0] = i
    for j in range(lb + 1):
        dp[0][j] = j

    for i in range(1, la + 1):
        for j in range(1, lb + 1):
            cost = 0 if a[i - 1] == b[j - 1] else 1
            dp[i][j] = min(
                dp[i - 1][j] + 1,
                dp[i][j - 1] + 1,
                dp[i - 1][j - 1] + cost
            )

    return dp[la][lb]