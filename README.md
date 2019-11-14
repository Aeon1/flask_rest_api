# Flask Rest Api
### modulos python
```sh
flask
psycopg2
```

### sql de tabla
```sh
CREATE TABLE public.personas
(
  id integer NOT NULL DEFAULT nextval('personas_id_seq'::regclass),
  nombre character varying(50),
  fecha_nacimiento date,
  puesto character varying(75)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE public.personas
  OWNER TO postgres;
```

