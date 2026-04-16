import bcrypt

print(bcrypt.hashpw("Wl4FJvNTT_".encode('utf-8'), bcrypt.gensalt()).decode('utf-8'))