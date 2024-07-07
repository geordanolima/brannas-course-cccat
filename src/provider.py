from settings import Settings
from src.database import Database


class DatabaseProvider:
    def __init__(self) -> None:
        self._settings = Settings()
        self.connection = Database(
            host=self._settings.DATABASE_HOST,
            port=self._settings.DATABASE_PORT,
            db_name=self._settings.DATABASE_NAME,
            user=self._settings.DATABASE_USER,
            password=self._settings.DATABASE_PASS,
        )
