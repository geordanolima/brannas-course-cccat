drop schema if exists cccat cascade;

create schema cccat;

create table cccat.account (
	account_id uuid primary key,
	name text not null,
	email text not null,
	password text not null,
	cpf text not null,
	car_plate text null,
	is_passenger boolean not null default false,
	is_driver boolean not null default false,
	created_at timestamp,
	updated_at timestamp
);

create table cccat.ride (
	ride_id uuid primary key,
	passenger_id uuid,
	driver_id uuid,
	status int,
	fare numeric,
	distance numeric,
	from_latitudeitude numeric,
	from_longitudeitude numeric,
	to_latitudeitude numeric,
	to_longitude numeric,
	created_at timestamp,
	updated_at timestamp
);
ALTER TABLE cccat.ride ADD CONSTRAINT passenger_account_fk FOREIGN KEY (passenger_id) REFERENCES cccat.account(account_id);
ALTER TABLE cccat.ride ADD CONSTRAINT driver_account_fk_1 FOREIGN KEY (driver_id) REFERENCES cccat.account(account_id);

create table cccat.position (
	position_id uuid primary key,
	ride_id uuid,
	latitude numeric,
	longitude numeric,
	created_at timestamp
);
ALTER TABLE cccat.position ADD CONSTRAINT ride_position_fk FOREIGN KEY (ride_id) REFERENCES cccat.ride(ride_id);
