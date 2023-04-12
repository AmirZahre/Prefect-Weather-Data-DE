DROP SCHEMA IF EXISTS public;
DROP TABLE IF EXISTS city, 
                    country, 
                    precipitation_type, 
                    raw_weather_daily, 
                    raw_weather_hourly, 
                    weather_daily, 
                    weather_hourly, 
                    weather_status;

CREATE SCHEMA public;

CREATE TABLE public.city (
    city_id character varying(255) NOT NULL,
    city character varying(255) NOT NULL,
    latitude numeric(8,6) NOT NULL,
    longitude numeric(9,6) NOT NULL,
    country_id character varying(255) NOT NULL
);

CREATE TABLE public.country (
    country_id character varying(255) NOT NULL,
    country character varying(255) NOT NULL
);

CREATE TABLE public.precipitation_type (
    precipitation_status_id integer NOT NULL,
    precipitation_state character varying(255) NOT NULL
);

CREATE TABLE public.raw_weather_daily (
    date character varying(255) NOT NULL,
    value double precision NOT NULL,
    parameter character varying(255) NOT NULL,
    latitude numeric(8,6) NOT NULL,
    longitude numeric(9,6) NOT NULL
);

CREATE TABLE public.raw_weather_hourly (
    date character varying(255) NOT NULL,
    value double precision NOT NULL,
    parameter character varying(255) NOT NULL,
    latitude numeric(8,6) NOT NULL,
    longitude numeric(9,6) NOT NULL
);

CREATE TABLE public.weather_daily (
    daily_weather_id character varying(255) NOT NULL,
    city_id character varying(255) NOT NULL,
    date DATE NOT NULL,
    precip_24h_mm double precision NOT NULL,
    precip_type_idx integer NOT NULL,
    sunrise_ux timestamp without time zone NOT NULL,
    sunset_ux timestamp without time zone NOT NULL,
    t_max_2m_24h_c double precision NOT NULL,
    t_mean_2m_24h_c double precision NOT NULL,
    t_min_2m_24h_c double precision NOT NULL,
    weather_code_24h_idx integer NOT NULL
);

CREATE TABLE public.weather_hourly (
    hourly_weather_id character varying(255) NOT NULL,
    city_id character varying(255) NOT NULL,
    date timestamp without time zone NOT NULL,
    relative_humidity_2m_p double precision NOT NULL,
    t_2m_c double precision NOT NULL,
    t_apparent_c double precision NOT NULL,
    weather_code_1h_idx bigint NOT NULL,
    wind_dir_2m_d double precision NOT NULL,
    wind_speed_2m_bft double precision NOT NULL,
    CONSTRAINT t_2m_c_range CHECK (((t_2m_c >= ('-100'::integer)::double precision) AND (t_2m_c <= (100)::double precision))),
    CONSTRAINT t_apparent_c_range CHECK (((t_2m_c >= ('-100'::integer)::double precision) AND (t_2m_c <= (100)::double precision)))
);

CREATE TABLE public.weather_status (
    weather_status_id bigint,
    weather_state text
);

ALTER TABLE ONLY public.city
    ADD CONSTRAINT city_pkey PRIMARY KEY (city_id);

ALTER TABLE ONLY public.country
    ADD CONSTRAINT country_pkey PRIMARY KEY (country_id);

ALTER TABLE ONLY public.precipitation_type
    ADD CONSTRAINT precipitation_type_pkey PRIMARY KEY (precipitation_status_id);

ALTER TABLE ONLY public.weather_daily
    ADD CONSTRAINT weather_daily_pkey PRIMARY KEY (daily_weather_id);

ALTER TABLE ONLY public.weather_hourly
    ADD CONSTRAINT weather_hourly_pkey PRIMARY KEY (hourly_weather_id);

ALTER TABLE ONLY public.weather_status
    ADD CONSTRAINT weather_status_id UNIQUE (weather_status_id);

ALTER TABLE ONLY public.city
    ADD CONSTRAINT city_country_id_fkey FOREIGN KEY (country_id) REFERENCES public.country(country_id) ON UPDATE CASCADE ON DELETE CASCADE;

ALTER TABLE ONLY public.weather_daily
    ADD CONSTRAINT weather_daily_city_id_fkey FOREIGN KEY (city_id) REFERENCES public.city(city_id) ON UPDATE CASCADE ON DELETE CASCADE;

ALTER TABLE ONLY public.weather_daily
    ADD CONSTRAINT weather_daily_precip_type_idx_fkey FOREIGN KEY (precip_type_idx) REFERENCES public.precipitation_type(precipitation_status_id) ON UPDATE CASCADE ON DELETE CASCADE;

ALTER TABLE ONLY public.weather_daily
    ADD CONSTRAINT weather_daily_weather_code_24h_idx_fkey FOREIGN KEY (weather_code_24h_idx) REFERENCES public.weather_status(weather_status_id) ON UPDATE CASCADE ON DELETE CASCADE;

ALTER TABLE ONLY public.weather_hourly
    ADD CONSTRAINT weather_hourly_city_id_fkey FOREIGN KEY (city_id) REFERENCES public.city(city_id) ON UPDATE CASCADE ON DELETE CASCADE;

ALTER TABLE ONLY public.weather_hourly
    ADD CONSTRAINT weather_hourly_weather_code_1h_idx_fkey FOREIGN KEY (weather_code_1h_idx) REFERENCES public.weather_status(weather_status_id) ON UPDATE CASCADE ON DELETE CASCADE;