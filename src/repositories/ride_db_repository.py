from datetime import datetime

from settings import Settings
from src.database import Database
from src.domain.entities import RideEntitie
from src.domain.repositories import RideRepository
from src.domain.models import Ride
from src.presenter.errors import ErrorStatusNotAllowed


class RideDatabaseRepository(RideRepository):
    table: str = "{}.ride".format(Settings().DATABASE_SCHEMA)

    def __init__(self, db: Database) -> None:
        self._db = db

    def insert_ride(self, ride: Ride) -> Ride:
        self._db.db_query(self._sql_insert_ride(ride=ride))
        return self.get_ride_by_id(id=ride.ride_id, response=True)

    def get_rides_by_driver(self, driver_id: str, status_in: int, limit: int) -> list[Ride]:
        rides = self._db.db_get_dict(
            sql=self._sql_get_rides_by_driver(driver_id=driver_id, status_in=status_in, limit=limit)
        )
        result = []
        for ride in rides:
            result.append(RideEntitie(**ride).object())
        return result

    def get_rides_by_passenger(self, passenger_id: str, status_not_in: list[int], limit: int) -> list[Ride]:
        rides = self._db.db_get_dict(
            sql=self._sql_get_rides_by_passenger(passenger_id=passenger_id, status_not_in=status_not_in, limit=limit)
        )
        result = []
        for ride in rides:
            result.append(RideEntitie(**ride).object())
        return result

    def update_status_ride(self, ride: Ride, new_status: int) -> Ride:
        self._db.db_query(sql=self._sql_update_status_ride(ride=ride, new_status=new_status))
        return self.get_ride_by_id(id=ride.ride_id, response=True)

    def update_fare_ride(self, ride: Ride, fare: float, distance: float, new_status) -> Ride:
        self._db.db_query(
            sql=self._sql_update_fare_ride(ride=ride, fare=fare, distance=distance, new_status=new_status)
        )
        return self.get_ride_by_id(id=ride.ride_id, response=True)

    def update_rate_repository(self, ride: Ride, rate: int, new_status: int) -> Ride:
        self._db.db_query(sql=self._sql_update_rate(ride=ride, rate=rate, status=new_status))
        return self._sql_get_ride_by_id(id=ride.ride_id)
    
    def update_driver_ride(self, ride: Ride, id_driver: int, new_status: int):
        return self._db.db_query(sql=self._sql_update_driver_ride(ride=ride, id_driver=id_driver, status=new_status))

    def get_ride_by_id(self, id: str, response: bool = False) -> Ride:
        ride = self._db.db_get_dict(self._sql_get_ride_by_id(id=id))
        if ride:
            return RideEntitie(**ride[0]).object(response=response)
        return {}

    def _sql_get_ride_by_id(self, id: str):
        sql = """SELECT * FROM {table} WHERE ride_id = '{id}'::uuid; """
        return sql.format(table=self.table, id=id)

    def _sql_insert_ride(self, ride: Ride) -> str:
        sql = """INSERT INTO {table}
            (ride_id, passenger_id, driver_id, status, fare, distance,
            from_latitude,from_longitude, to_latitude, to_longitude, created_at, updated_at)
            VALUES
            (
                '{ride_id}'::uuid, '{passenger_id}'::uuid, '{driver_id}'::uuid,
                {status}, {fare}, {distance}, {from_latitude},
                {from_longitude}, {to_latitude}, {to_longitude}, '{created_at}', Null
            );
        """
        return sql.format(
            table=self.table,
            ride_id=ride.ride_id,
            passenger_id=ride.passenger_id,
            driver_id=ride.driver_id,
            status=ride.status,
            fare=ride.fare,
            distance=ride.distance,
            from_latitude=ride.from_latitude,
            from_longitude=ride.from_longitude,
            to_latitude=ride.to_latitude,
            to_longitude=ride.to_longitude,
            created_at=datetime.now(),
        ).replace("'None'", "Null").replace("None", "Null")

    def _sql_get_rides_by_driver(self, driver_id: str, status_in: list[int], limit: int = 50) -> str:
        sql = """SELECT * FROM {table}
        WHERE driver_id = '{driver_id}'::uuid
          AND status in {status}
        LIMIT {limit}"""
        return sql.format(table=self.table, driver_id=driver_id, status=tuple(status_in), limit=limit)

    def _sql_get_rides_by_passenger(
        self, passenger_id: str, status_not_in: list[int], limit: int = 50
    ) -> str:
        sql = """SELECT * FROM {table}
        WHERE passenger_id = '{passenger_id}'::uuid
          AND status not in {status}
        LIMIT {limit}"""
        return sql.format(table=self.table, status=tuple(status_not_in), passenger_id=passenger_id, limit=limit)

    def _sql_update_status_ride(self, ride: Ride, new_status: int) -> str:
        sql = """UPDATE {table} SET "status" = {new_status}, updated_at = '{updated_at}'
        WHERE "ride_id" = '{ride_id}'::uuid;"""
        return sql.format(table=self.table, new_status=new_status, ride_id=ride.ride_id, updated_at=datetime.now())

    def _sql_update_fare_ride(self, ride: Ride, fare: float, distance: float, new_status: int):
        sql = """UPDATE {table} SET
        fare={fare}, distance={distance}, "status" = {new_status}, updated_at = '{updated_at}'
        WHERE "ride_id" = '{ride_id}'::uuid;"""
        return sql.format(
            table=self.table,
            fare=fare,
            distance=distance,
            new_status=new_status,
            updated_at=datetime.now(),
            ride_id=ride.ride_id
        )

    def _sql_update_driver_ride(self, ride: Ride, id_driver: str, status: int) -> str:
        sql = """UPDATE {table} SET "driver_id" = '{driver_id}'::uuid, "status" = {status}, updated_at = '{updated_at}'
        WHERE "ride_id" = '{ride_id}'::uuid;"""
        return sql.format(
            table=self.table, driver_id=id_driver, ride_id=ride.ride_id, status=status, updated_at=datetime.now()
        )

    def _sql_update_rate(self, ride: Ride, rate: int, status: int):
        sql = """UPDATE {table} SET rate = {rate}, updated_at = '{updated_at}', "status" = {status}
        WHERE "ride_id"='{ride_id}'::uuid;"""
        return sql.format(table=self.table, rate=rate, updated_at=datetime.now(), ride_id=ride.ride_id, status=status)
