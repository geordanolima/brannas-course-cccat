import bcrypt


def cryptography_password(password: str):
    password = password.encode("utf-8")
    return bcrypt.hashpw(password, bcrypt.gensalt(5))


def compare_password(hashed_password, password):
    password = password.encode("utf-8")
    return bcrypt.checkpw(password=password, hashed_password=hashed_password)
