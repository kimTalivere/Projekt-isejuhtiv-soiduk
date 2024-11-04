--
-- PostgreSQL database dump
--

-- Dumped from database version 13.2
-- Dumped by pg_dump version 16.4 (Ubuntu 16.4-0ubuntu0.24.04.2)

-- Started on 2024-10-08 14:46:44 EEST

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'SQL_ASCII';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- TOC entry 200 (class 1259 OID 16560)
-- Name: daily_routes; Type: TABLE; Schema: public; Owner: autolab
--

CREATE TABLE public.daily_routes (
    route_id smallint NOT NULL,
    date date NOT NULL,
    vehicle_id smallint NOT NULL,
    map_image text,
    distance_traveled real,
    sensor_ids integer[]
);


ALTER TABLE public.daily_routes OWNER TO autolab;

--
-- TOC entry 201 (class 1259 OID 16566)
-- Name: daily_routes_route_id_seq; Type: SEQUENCE; Schema: public; Owner: autolab
--

CREATE SEQUENCE public.daily_routes_route_id_seq
    AS smallint
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.daily_routes_route_id_seq OWNER TO autolab;

--
-- TOC entry 2298 (class 0 OID 0)
-- Dependencies: 201
-- Name: daily_routes_route_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: autolab
--

ALTER SEQUENCE public.daily_routes_route_id_seq OWNED BY public.daily_routes.route_id;


--
-- TOC entry 202 (class 1259 OID 16568)
-- Name: v_class; Type: TABLE; Schema: public; Owner: autolab
--

CREATE TABLE public.v_class (
    class_id integer NOT NULL,
    class_name character varying(50) NOT NULL
);


ALTER TABLE public.v_class OWNER TO autolab;

--
-- TOC entry 203 (class 1259 OID 16571)
-- Name: v_class_class_id_seq; Type: SEQUENCE; Schema: public; Owner: autolab
--

CREATE SEQUENCE public.v_class_class_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.v_class_class_id_seq OWNER TO autolab;

--
-- TOC entry 2299 (class 0 OID 0)
-- Dependencies: 203
-- Name: v_class_class_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: autolab
--

ALTER SEQUENCE public.v_class_class_id_seq OWNED BY public.v_class.class_id;


--
-- TOC entry 204 (class 1259 OID 16573)
-- Name: v_localization; Type: TABLE; Schema: public; Owner: autolab
--

CREATE TABLE public.v_localization (
    localization_id integer NOT NULL,
    parameter_id integer,
    vehicle_id integer,
    p_x character varying(255) NOT NULL,
    p_y character varying(255) NOT NULL,
    p_z character varying(255) NOT NULL,
    o_x character varying(255) NOT NULL,
    o_y character varying(255) NOT NULL,
    o_z character varying(255) NOT NULL,
    o_w character varying(255) NOT NULL,
    create_date character varying(255) NOT NULL,
    create_time character varying(255) NOT NULL,
    recorded_time timestamp with time zone DEFAULT CURRENT_TIMESTAMP NOT NULL
);


ALTER TABLE public.v_localization OWNER TO autolab;

--
-- TOC entry 205 (class 1259 OID 16580)
-- Name: v_localization_localization_id_seq; Type: SEQUENCE; Schema: public; Owner: autolab
--

CREATE SEQUENCE public.v_localization_localization_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.v_localization_localization_id_seq OWNER TO autolab;

--
-- TOC entry 2300 (class 0 OID 0)
-- Dependencies: 205
-- Name: v_localization_localization_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: autolab
--

ALTER SEQUENCE public.v_localization_localization_id_seq OWNED BY public.v_localization.localization_id;


--
-- TOC entry 206 (class 1259 OID 16582)
-- Name: v_log; Type: TABLE; Schema: public; Owner: autolab
--

CREATE TABLE public.v_log (
    log_id integer NOT NULL,
    parameter_id integer,
    vehicle_id integer,
    create_date character varying(255) NOT NULL,
    create_time character varying(255) NOT NULL,
    recorded_time timestamp with time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    jason_data json
);


ALTER TABLE public.v_log OWNER TO autolab;

--
-- TOC entry 207 (class 1259 OID 16589)
-- Name: v_log_log_id_seq; Type: SEQUENCE; Schema: public; Owner: autolab
--

CREATE SEQUENCE public.v_log_log_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.v_log_log_id_seq OWNER TO autolab;

--
-- TOC entry 2302 (class 0 OID 0)
-- Dependencies: 207
-- Name: v_log_log_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: autolab
--

ALTER SEQUENCE public.v_log_log_id_seq OWNED BY public.v_log.log_id;


--
-- TOC entry 208 (class 1259 OID 16591)
-- Name: v_parameter; Type: TABLE; Schema: public; Owner: autolab
--

CREATE TABLE public.v_parameter (
    parameter_id integer NOT NULL,
    class_id integer,
    parameter_name character varying(50) NOT NULL,
    unit character varying(50) NOT NULL,
    frequency integer NOT NULL,
    ros_topic character varying(50) NOT NULL,
    describtion character varying(50) NOT NULL,
    range_function character varying(50) NOT NULL
);


ALTER TABLE public.v_parameter OWNER TO autolab;

--
-- TOC entry 209 (class 1259 OID 16594)
-- Name: v_parameter_parameter_id_seq; Type: SEQUENCE; Schema: public; Owner: autolab
--

CREATE SEQUENCE public.v_parameter_parameter_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.v_parameter_parameter_id_seq OWNER TO autolab;

--
-- TOC entry 2303 (class 0 OID 0)
-- Dependencies: 209
-- Name: v_parameter_parameter_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: autolab
--

ALTER SEQUENCE public.v_parameter_parameter_id_seq OWNED BY public.v_parameter.parameter_id;


--
-- TOC entry 210 (class 1259 OID 16596)
-- Name: vehicle; Type: TABLE; Schema: public; Owner: autolab
--

CREATE TABLE public.vehicle (
    vehicle_id integer NOT NULL,
    vehicle_name character varying(255) NOT NULL
);


ALTER TABLE public.vehicle OWNER TO autolab;

--
-- TOC entry 211 (class 1259 OID 16599)
-- Name: vehicle_vehicle_id_seq; Type: SEQUENCE; Schema: public; Owner: autolab
--

CREATE SEQUENCE public.vehicle_vehicle_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.vehicle_vehicle_id_seq OWNER TO autolab;

--
-- TOC entry 2305 (class 0 OID 0)
-- Dependencies: 211
-- Name: vehicle_vehicle_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: autolab
--

ALTER SEQUENCE public.vehicle_vehicle_id_seq OWNED BY public.vehicle.vehicle_id;


--
-- TOC entry 2137 (class 2604 OID 16601)
-- Name: daily_routes route_id; Type: DEFAULT; Schema: public; Owner: autolab
--

ALTER TABLE ONLY public.daily_routes ALTER COLUMN route_id SET DEFAULT nextval('public.daily_routes_route_id_seq'::regclass);


--
-- TOC entry 2138 (class 2604 OID 16602)
-- Name: v_class class_id; Type: DEFAULT; Schema: public; Owner: autolab
--

ALTER TABLE ONLY public.v_class ALTER COLUMN class_id SET DEFAULT nextval('public.v_class_class_id_seq'::regclass);


--
-- TOC entry 2139 (class 2604 OID 16603)
-- Name: v_localization localization_id; Type: DEFAULT; Schema: public; Owner: autolab
--

ALTER TABLE ONLY public.v_localization ALTER COLUMN localization_id SET DEFAULT nextval('public.v_localization_localization_id_seq'::regclass);


--
-- TOC entry 2141 (class 2604 OID 16604)
-- Name: v_log log_id; Type: DEFAULT; Schema: public; Owner: autolab
--

ALTER TABLE ONLY public.v_log ALTER COLUMN log_id SET DEFAULT nextval('public.v_log_log_id_seq'::regclass);


--
-- TOC entry 2143 (class 2604 OID 16605)
-- Name: v_parameter parameter_id; Type: DEFAULT; Schema: public; Owner: autolab
--

ALTER TABLE ONLY public.v_parameter ALTER COLUMN parameter_id SET DEFAULT nextval('public.v_parameter_parameter_id_seq'::regclass);


--
-- TOC entry 2144 (class 2604 OID 16606)
-- Name: vehicle vehicle_id; Type: DEFAULT; Schema: public; Owner: autolab
--

ALTER TABLE ONLY public.vehicle ALTER COLUMN vehicle_id SET DEFAULT nextval('public.vehicle_vehicle_id_seq'::regclass);


--
-- TOC entry 2146 (class 2606 OID 120653)
-- Name: daily_routes daily_routes_pkey; Type: CONSTRAINT; Schema: public; Owner: autolab
--

ALTER TABLE ONLY public.daily_routes
    ADD CONSTRAINT daily_routes_pkey PRIMARY KEY (route_id);


--
-- TOC entry 2148 (class 2606 OID 120655)
-- Name: v_class v_class_pkey; Type: CONSTRAINT; Schema: public; Owner: autolab
--

ALTER TABLE ONLY public.v_class
    ADD CONSTRAINT v_class_pkey PRIMARY KEY (class_id);


--
-- TOC entry 2150 (class 2606 OID 120657)
-- Name: v_localization v_localization_pkey; Type: CONSTRAINT; Schema: public; Owner: autolab
--

ALTER TABLE ONLY public.v_localization
    ADD CONSTRAINT v_localization_pkey PRIMARY KEY (localization_id);


--
-- TOC entry 2153 (class 2606 OID 120659)
-- Name: v_log v_log_pkey; Type: CONSTRAINT; Schema: public; Owner: autolab
--

ALTER TABLE ONLY public.v_log
    ADD CONSTRAINT v_log_pkey PRIMARY KEY (log_id);


--
-- TOC entry 2155 (class 2606 OID 120661)
-- Name: v_parameter v_parameter_pkey; Type: CONSTRAINT; Schema: public; Owner: autolab
--

ALTER TABLE ONLY public.v_parameter
    ADD CONSTRAINT v_parameter_pkey PRIMARY KEY (parameter_id);


--
-- TOC entry 2157 (class 2606 OID 120663)
-- Name: vehicle vehicle_pkey; Type: CONSTRAINT; Schema: public; Owner: autolab
--

ALTER TABLE ONLY public.vehicle
    ADD CONSTRAINT vehicle_pkey PRIMARY KEY (vehicle_id);


--
-- TOC entry 2151 (class 1259 OID 120664)
-- Name: index_on_param_id_and_record_time; Type: INDEX; Schema: public; Owner: autolab
--

CREATE INDEX index_on_param_id_and_record_time ON public.v_log USING btree (parameter_id, recorded_time);


--
-- TOC entry 2158 (class 2606 OID 120665)
-- Name: v_localization v_localization_parameter_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: autolab
--

ALTER TABLE ONLY public.v_localization
    ADD CONSTRAINT v_localization_parameter_id_fkey FOREIGN KEY (parameter_id) REFERENCES public.v_parameter(parameter_id);


--
-- TOC entry 2159 (class 2606 OID 120670)
-- Name: v_localization v_localization_vehicle_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: autolab
--

ALTER TABLE ONLY public.v_localization
    ADD CONSTRAINT v_localization_vehicle_id_fkey FOREIGN KEY (vehicle_id) REFERENCES public.vehicle(vehicle_id);


--
-- TOC entry 2160 (class 2606 OID 120675)
-- Name: v_log v_log_parameter_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: autolab
--

ALTER TABLE ONLY public.v_log
    ADD CONSTRAINT v_log_parameter_id_fkey FOREIGN KEY (parameter_id) REFERENCES public.v_parameter(parameter_id);


--
-- TOC entry 2161 (class 2606 OID 120680)
-- Name: v_log v_log_vehicle_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: autolab
--

ALTER TABLE ONLY public.v_log
    ADD CONSTRAINT v_log_vehicle_id_fkey FOREIGN KEY (vehicle_id) REFERENCES public.vehicle(vehicle_id);


--
-- TOC entry 2162 (class 2606 OID 120685)
-- Name: v_parameter v_parameter_class_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: autolab
--

ALTER TABLE ONLY public.v_parameter
    ADD CONSTRAINT v_parameter_class_id_fkey FOREIGN KEY (class_id) REFERENCES public.v_class(class_id);


--
-- TOC entry 2301 (class 0 OID 0)
-- Dependencies: 206
-- Name: TABLE v_log; Type: ACL; Schema: public; Owner: autolab
--

GRANT SELECT ON TABLE public.v_log TO postgres;


--
-- TOC entry 2304 (class 0 OID 0)
-- Dependencies: 210
-- Name: TABLE vehicle; Type: ACL; Schema: public; Owner: autolab
--

GRANT SELECT ON TABLE public.vehicle TO postgres;


-- Completed on 2024-10-08 14:46:45 EEST

--
-- PostgreSQL database dump complete
--

