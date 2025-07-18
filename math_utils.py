def safe_div(a, b, default=0.0):
    return default if b == 0 else a / b
