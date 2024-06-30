from ..database import Database
from ..domain.constants import RideStatusEnum
from ..domain.entities import RideEntitie
from ..domain.repositories import RideRepository
from ..domain.models import Ride


class RideDatabaseRepository(RideRepository):
    table: str = "cccat17.ride"

    def __init__(self, db: Database) -> None:
        self._db = db

    def insert_ride(self, ride: Ride) -> Ride:
        return self._db.db_query(self._sql_insert_ride(ride=ride))

    def get_rides_by_driver(self, driver_id: str, status: RideStatusEnum, limit: int) -> list[Ride]:
        rides = self._db.db_get_dict(sql=self._sql_get_rides_by_driver(driver_id=driver_id, status=status, limit=limit))
        result = []
        for ride in rides:
            result.append(RideEntitie(**ride).object())
        return result

    def get_rides_by_passenger(self, driver_id: str, status_not_in: list[RideStatusEnum], limit: int) -> list[Ride]:
        rides = self._db.db_get_dict(
            sql=self._sql_get_rides_by_passenger(driver_id=driver_id, status_not_in=status_not_in, limit=limit)
        )
        result = []
        for ride in rides:
            result.append(RideEntitie(**ride).object())
        return result

    def update_status_ride(self, ride: Ride, new_status: RideStatusEnum) -> Ride:
        return self._db.db_query(sql=self._sql_update_status_ride(ride=ride, new_status=new_status))

    def _sql_insert_ride(self, ride: Ride) -> str:
        sql = """INSERT INTO {table}
            (ride_id, passenger_id, driver_id, status, fare, distance, from_lat, from_long, to_lat, to_long, "date")
            VALUES
            (
                {ride_id}, {passenger_id}, {driver_id},
                {status}, {fare}, {distance}, {from_lat},
                {from_long}, {to_lat}, {to_long}, "{date}"
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
            from_lat=ride.from_lat,
            from_long=ride.from_long,
            to_lat=ride.to_lat,
            to_long=ride.to_long,
            date=ride.date,
        )

    def _sql_get_rides_by_driver(self, driver_id: str, status: RideStatusEnum, limit: int = 50) -> str:
        sql = """SELECT * FROM {table}
        WHERE driver_id = {driver_id}
          AND status in ({status})
        LIMIT {limit}"""
        return sql.format(table=self.table, driver_id=driver_id, status=status, limit=limit)

    def _sql_get_rides_by_passenger(
        self, passenger_id: str, status_not_in: list[RideStatusEnum], limit: int = 50
    ) -> str:
        sql = """SELECT * FROM {table}
        WHERE passenger_id = {passenger_id}
          AND status not in ({status})
        LIMIT {limit}"""
        status = []
        for item in status_not_in:
            status.append(item)
        return sql.format(table=self.table, passenger_id=passenger_id, limit=limit)

    def _sql_update_status_ride(self, ride: Ride, new_status: RideStatusEnum) -> str:
        sql = """UPDATE {table} SET "status" = {new_status} WHERE "ride_id" = '{ride_id}'::uuid;"""
        return sql.format(table=self.table, new_status=new_status, ride_id=ride.ride_id)
