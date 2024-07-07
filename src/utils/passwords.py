import bcrypt


class Password:
    def cryptography_password(self, password: str):
        password = password.encode("utf-8")
        return bcrypt.hashpw(password, bcrypt.gensalt(5)).decode()

    def compare_password(self, hashed_password, password):
        password = password.encode("utf-8")
        return bcrypt.checkpw(password=password, hashed_password=hashed_password)
