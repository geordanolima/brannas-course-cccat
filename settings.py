import os

class Settings():
    DATABASE_NAME: str = os.getenv("DATABASE_NAME", "app")
    DATABASE_HOST: str = os.getenv("DATABASE_HOST", "localhost")
    DATABASE_PORT: int = os.getenv("DATABASE_PORET", 54321)
    DATABASE_USER: str = os.getenv("DATABASE_USER", "test")
    DATABASE_PASS: str = os.getenv("DATABASE_PASS", "test")
