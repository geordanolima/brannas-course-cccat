from datetime import datetime

from settings import Settings
from src.database import Database
from src.domain.entities import PositionEntitie
from src.domain.models.position import Position
from src.domain.repositories import PositionRepository


class PositionDatabaseRepository(PositionRepository):
    table: str = "{}.position".format(Settings().DATABASE_SCHEMA)

    def __init__(self, db: Database) -> None:
        self.db = db

    def insert_position(self, position: Position):
        self.db.db_query(sql=self._sql_insert_position(position=position))
        return self.get_position_by_id(position_id=position.position_id)

    def get_position_by_id(self, position_id: str) -> Position:
        position = self.db.db_get_dict(sql=self._sql_get_position_by_id(position_id=position_id))
        if position:
            return PositionEntitie(**position[0]).object()
        return None

    def get_position_by_ride(self, ride_id: str) -> list[Position]:
        result = []
        positions = self.db.db_get_dict(sql=self._sql_get_position_by_ride(ride_id=ride_id))
        for position in positions:
            result.append(PositionEntitie(**position[0]).object())
        return result

    def _sql_insert_position(position: Position) -> str:
        sql = """INSERT INTO {table} (position_id, ride_id, latitude, longitude, created_at)
        VALUES({position_id}::uuid, {ride_id}::uuid, {latitude}, {longitude}, '{created_at}');"""
        return sql.format(
            position_id=position.position_id,
            ride_id=position.ride_id,
            latitude=position.latitude,
            longitude=position.longitude,
            created_at=datetime.now()
        )

    def _sql_get_position_by_id(self, position_id: str):
        sql = """SELECT * FROM {table} WHERE position_id = '{position_id}'::uuid; """
        return sql.format(table=self.table, position_id=position_id)

    def _sql_get_position_by_ride(self, ride_id: str):
        sql = """SELECT * FROM {table} WHERE ride_id = '{ride_id}'::uuid; """
        return sql.format(table=self.table, ride_id=ride_id)
