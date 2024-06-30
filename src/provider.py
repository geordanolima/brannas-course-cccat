
from database import Database
from settings import Settings


class DatabaseProvider:
    def __init__(self) -> None:
        self._settings = Settings()
        self.connection = Database(
            host=self.settings.DATABASE_HOST,
            port=self.settings.DATABASE_PORT,
            db_name=self.settings.DATABASE_NAME,
            user=self.settings.DATABASE_USER,
            password=self.settings.DATABASE_PASS,
        )
