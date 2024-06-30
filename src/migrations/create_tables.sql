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
	is_driver boolean not null default false
);

create table cccat.ride (
	ride_id uuid,
	passenger_id uuid,
	driver_id uuid,
	status int,
	fare numeric,
	distance numeric,
	from_lat numeric,
	from_long numeric,
	to_lat numeric,
	to_long numeric,
	date timestamp
);