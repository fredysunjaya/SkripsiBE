import bcrypt

print(bcrypt.hashpw("83GPqqzD*f".encode("utf-8"), bcrypt.gensalt()).decode("utf-8"))
