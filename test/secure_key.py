import secrets

# Generate a secure key arbitrary
secure_key = secrets.token_hex(32)
print(secure_key)