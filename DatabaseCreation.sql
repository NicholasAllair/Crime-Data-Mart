
CREATE TABLE public."Crime"
(	
	"CrimeKey" integer NOT NULL,
    "Crime_report_time" time without time zone,
    "crime_start_time" time without time zone,
    "crime_end_time" time without time zone,
    "Crime details" character(35) COLLATE pg_catalog."default",
    "Crime_Type" character(60) COLLATE pg_catalog."default",
    "Crime Category" character(60) COLLATE pg_catalog."default",
    "Crime SeverityIndex" integer,
    
    CONSTRAINT "Crime_pkey" PRIMARY KEY ("CrimeKey")
);




CREATE TABLE public."Crime Fact"
(
    "Date_key" integer NOT NULL,
    "Location_key" integer NOT NULL,
    "Crime_key" integer NOT NULL,
    "Event_key" integer NOT NULL,
    "Is_traffic" boolean NOT NULL,
    "Is_fatal" boolean NOT NULL,
    "Is_nighttime" boolean NOT NULL


);


CREATE TABLE public."Date"
(
    "Date_key" integer NOT NULL,
    "_day" integer,
    "_month" integer,
    "_year" integer,
    "is_weekend" boolean,
    "is_holiday" boolean,
    "holiday_name" character(50),
   
    CONSTRAINT "Date_pkey" PRIMARY KEY ("Date_key")
);



CREATE TABLE public."Location"
(
    "Location_key" integer NOT NULL ,
    "Location_name" character(50) ,
    "Longitude" numeric,
    "Latitude" numeric,
    "Neighbourhood" character(50) ,
    "Neighbourhood_stats" integer,
    "City" character(25),
    "Crime Rate" integer,
    CONSTRAINT "Location_pkey" PRIMARY KEY ("Location_key")
);