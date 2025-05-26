--
-- PostgreSQL database dump
--

-- Dumped from database version 17.4
-- Dumped by pg_dump version 17.4

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: infracciones; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.infracciones (
    id integer NOT NULL,
    patente text,
    fecha_hora timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    tipo text NOT NULL,
    descripcion text
);


ALTER TABLE public.infracciones OWNER TO postgres;

--
-- Name: infracciones_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.infracciones_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.infracciones_id_seq OWNER TO postgres;

--
-- Name: infracciones_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.infracciones_id_seq OWNED BY public.infracciones.id;


--
-- Name: registro_accesos; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.registro_accesos (
    id integer NOT NULL,
    patente text,
    fecha_hora timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    metodo text,
    resultado text,
    captura_url text,
    CONSTRAINT registro_accesos_metodo_check CHECK ((metodo = ANY (ARRAY['automatico'::text, 'manual'::text]))),
    CONSTRAINT registro_accesos_resultado_check CHECK ((resultado = ANY (ARRAY['autorizado'::text, 'denegado'::text])))
);


ALTER TABLE public.registro_accesos OWNER TO postgres;

--
-- Name: registro_accesos_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.registro_accesos_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.registro_accesos_id_seq OWNER TO postgres;

--
-- Name: registro_accesos_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.registro_accesos_id_seq OWNED BY public.registro_accesos.id;


--
-- Name: solicitudes_manuales; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.solicitudes_manuales (
    id integer NOT NULL,
    patente text,
    fecha_hora timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    estado text DEFAULT 'pendiente'::text,
    autorizado_por integer,
    CONSTRAINT solicitudes_manuales_estado_check CHECK ((estado = ANY (ARRAY['pendiente'::text, 'autorizado'::text, 'rechazado'::text])))
);


ALTER TABLE public.solicitudes_manuales OWNER TO postgres;

--
-- Name: solicitudes_manuales_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.solicitudes_manuales_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.solicitudes_manuales_id_seq OWNER TO postgres;

--
-- Name: solicitudes_manuales_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.solicitudes_manuales_id_seq OWNED BY public.solicitudes_manuales.id;


--
-- Name: usuarios; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.usuarios (
    id integer NOT NULL,
    nombre text NOT NULL,
    apellido text NOT NULL,
    email text NOT NULL
);


ALTER TABLE public.usuarios OWNER TO postgres;

--
-- Name: usuarios_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.usuarios_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.usuarios_id_seq OWNER TO postgres;

--
-- Name: usuarios_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.usuarios_id_seq OWNED BY public.usuarios.id;


--
-- Name: vehiculos; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.vehiculos (
    patente text NOT NULL,
    marca text,
    modelo text,
    autorizado boolean DEFAULT false,
    bloqueado boolean DEFAULT false,
    "dueño_id" integer
);


ALTER TABLE public.vehiculos OWNER TO postgres;

--
-- Name: infracciones id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.infracciones ALTER COLUMN id SET DEFAULT nextval('public.infracciones_id_seq'::regclass);


--
-- Name: registro_accesos id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.registro_accesos ALTER COLUMN id SET DEFAULT nextval('public.registro_accesos_id_seq'::regclass);


--
-- Name: solicitudes_manuales id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.solicitudes_manuales ALTER COLUMN id SET DEFAULT nextval('public.solicitudes_manuales_id_seq'::regclass);


--
-- Name: usuarios id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.usuarios ALTER COLUMN id SET DEFAULT nextval('public.usuarios_id_seq'::regclass);


--
-- Data for Name: infracciones; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.infracciones (id, patente, fecha_hora, tipo, descripcion) FROM stdin;
\.


--
-- Data for Name: registro_accesos; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.registro_accesos (id, patente, fecha_hora, metodo, resultado, captura_url) FROM stdin;
\.


--
-- Data for Name: solicitudes_manuales; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.solicitudes_manuales (id, patente, fecha_hora, estado, autorizado_por) FROM stdin;
\.


--
-- Data for Name: usuarios; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.usuarios (id, nombre, apellido, email) FROM stdin;
\.


--
-- Data for Name: vehiculos; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.vehiculos (patente, marca, modelo, autorizado, bloqueado, "dueño_id") FROM stdin;
\.


--
-- Name: infracciones_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.infracciones_id_seq', 1, false);


--
-- Name: registro_accesos_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.registro_accesos_id_seq', 1, false);


--
-- Name: solicitudes_manuales_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.solicitudes_manuales_id_seq', 1, false);


--
-- Name: usuarios_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.usuarios_id_seq', 1, false);


--
-- Name: infracciones infracciones_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.infracciones
    ADD CONSTRAINT infracciones_pkey PRIMARY KEY (id);


--
-- Name: registro_accesos registro_accesos_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.registro_accesos
    ADD CONSTRAINT registro_accesos_pkey PRIMARY KEY (id);


--
-- Name: solicitudes_manuales solicitudes_manuales_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.solicitudes_manuales
    ADD CONSTRAINT solicitudes_manuales_pkey PRIMARY KEY (id);


--
-- Name: usuarios usuarios_email_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.usuarios
    ADD CONSTRAINT usuarios_email_key UNIQUE (email);


--
-- Name: usuarios usuarios_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.usuarios
    ADD CONSTRAINT usuarios_pkey PRIMARY KEY (id);


--
-- Name: vehiculos vehiculos_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.vehiculos
    ADD CONSTRAINT vehiculos_pkey PRIMARY KEY (patente);


--
-- Name: infracciones infracciones_patente_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.infracciones
    ADD CONSTRAINT infracciones_patente_fkey FOREIGN KEY (patente) REFERENCES public.vehiculos(patente) ON DELETE CASCADE;


--
-- Name: registro_accesos registro_accesos_patente_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.registro_accesos
    ADD CONSTRAINT registro_accesos_patente_fkey FOREIGN KEY (patente) REFERENCES public.vehiculos(patente) ON DELETE SET NULL;


--
-- Name: solicitudes_manuales solicitudes_manuales_autorizado_por_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.solicitudes_manuales
    ADD CONSTRAINT solicitudes_manuales_autorizado_por_fkey FOREIGN KEY (autorizado_por) REFERENCES public.usuarios(id);


--
-- Name: solicitudes_manuales solicitudes_manuales_patente_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.solicitudes_manuales
    ADD CONSTRAINT solicitudes_manuales_patente_fkey FOREIGN KEY (patente) REFERENCES public.vehiculos(patente);


--
-- Name: vehiculos vehiculos_dueño_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.vehiculos
    ADD CONSTRAINT "vehiculos_dueño_id_fkey" FOREIGN KEY ("dueño_id") REFERENCES public.usuarios(id) ON DELETE CASCADE;


--
-- PostgreSQL database dump complete
--

