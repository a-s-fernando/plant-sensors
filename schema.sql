DROP TABLE IF EXISTS sunlight_for_plant;
DROP TABLE IF EXISTS record;
DROP TABLE IF EXISTS sunlight_value;
DROP TABLE IF EXISTS botanist;
DROP TABLE IF EXISTS plant;
DROP TABLE IF EXISTS plant_cycle;
DROP TABLE IF EXISTS country;
DROP TABLE IF EXISTS continent;

CREATE TABLE IF NOT EXISTS continent(
	continent_id INT GENERATED ALWAYS AS IDENTITY,
	name VARCHAR(50) NOT NULL UNIQUE,
	PRIMARY KEY (continent_id)
);

CREATE TABLE IF NOT EXISTS country(
	country_id INT GENERATED ALWAYS AS IDENTITY,
	continent_id INT NOT NULL,
	name VARCHAR(50) NOT NULL UNIQUE,
	PRIMARY KEY (country_id),
	FOREIGN KEY (continent_id) REFERENCES continent(continent_id)
);

CREATE TABLE IF NOT EXISTS plant_cycle(
	plant_cycle_id INT GENERATED ALWAYS AS IDENTITY,
	value VARCHAR(50) NOT NULL UNIQUE,
	PRIMARY KEY (plant_cycle_id)
);

CREATE TABLE IF NOT EXISTS plant(
	plant_id INT GENERATED ALWAYS AS IDENTITY,
	name VARCHAR (50) NOT NULL UNIQUE,
	country_id INT NOT NULL,
	plant_cycle_id INT,
	PRIMARY KEY (plant_id),
	FOREIGN KEY (country_id) REFERENCES country(country_id),
	FOREIGN KEY (plant_cycle_id) REFERENCES plant_cycle(plant_cycle_id)
);

CREATE TABLE IF NOT EXISTS botanist(
	botanist_id INT GENERATED ALWAYS AS IDENTITY,
	first_name VARCHAR (50) NOT NULL,
	last_name VARCHAR (50) NOT NULL,
	email VARCHAR (100) NOT NULL,
	PRIMARY KEY (botanist_id)
);

CREATE TABLE IF NOT EXISTS sunlight_value(
	sunlight_id INT GENERATED ALWAYS AS IDENTITY,
	value VARCHAR (50) NOT NULL UNIQUE,
	PRIMARY KEY (sunlight_id)
);

CREATE TABLE IF NOT EXISTS record(
	record_id INT GENERATED ALWAYS AS IDENTITY,
	recording_taken TIMESTAMP NOT NULL,
	botanist_id INT NOT NULL,
	plant_id INT NOT NULL,
	last_watered TIMESTAMP NOT NULL,
	soil_moisture FLOAT NOT NULL,
	temperature FLOAT NOT NULL,
	PRIMARY KEY (record_id),
	FOREIGN KEY (botanist_id) REFERENCES botanist(botanist_id),
	FOREIGN KEY (plant_id) REFERENCES plant(plant_id)
);

CREATE TABLE IF NOT EXISTS sunlight_for_plant(
	plant_id INT NOT NULL,
	sunlight_id INT NOT NULL,
	UNIQUE (sunlight_id, plant_id),
	FOREIGN KEY (plant_id) REFERENCES plant(plant_id),
	FOREIGN KEY (sunlight_id) REFERENCES sunlight_value(sunlight_id)
);
