-- Table: public.dependencia

-- DROP TABLE IF EXISTS public.dependencia;

CREATE TABLE IF NOT EXISTS public.dependencia
(
    id integer NOT NULL DEFAULT nextval('dependencia_id_seq'::regclass),
    repositorio character varying(255) COLLATE pg_catalog."default" NOT NULL,
    "groupId" character varying(255) COLLATE pg_catalog."default" NOT NULL,
    "artifactId" character varying(255) COLLATE pg_catalog."default" NOT NULL,
    version character varying(255) COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT dependencia_pkey PRIMARY KEY (id)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.dependencia
    OWNER to myuser;