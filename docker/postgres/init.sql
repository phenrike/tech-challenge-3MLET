
CREATE TABLE producao (
    id_producao SERIAL PRIMARY KEY,
    ds_produto VARCHAR(255) NOT NULL,
    tp_produto VARCHAR(50) NOT NULL,
    dt_ano INTEGER NOT NULL,
    qt_producao FLOAT NOT NULL
);

INSERT INTO producao (ds_Produto, tp_Produto, dt_Ano, qt_Producao)
VALUES ('Arroz', 'Cereal', 2023, 1500.75);


-- DROP SCHEMA public;

DROP SCHEMA IF EXISTS public CASCADE;

CREATE SCHEMA public AUTHORIZATION pg_database_owner;

-- DROP SEQUENCE public.tbl_comercializacao_id_comercializacao_seq;

CREATE SEQUENCE public.tbl_comercializacao_id_comercializacao_seq
	INCREMENT BY 1
	MINVALUE 1
	MAXVALUE 2147483647
	START 1
	CACHE 1
	NO CYCLE;
-- DROP SEQUENCE public.tbl_cultivo_id_cultivo_seq;

CREATE SEQUENCE public.tbl_cultivo_id_cultivo_seq
	INCREMENT BY 1
	MINVALUE 1
	MAXVALUE 2147483647
	START 1
	CACHE 1
	NO CYCLE;
-- DROP SEQUENCE public.tbl_exportacao_id_exportacao_seq;

CREATE SEQUENCE public.tbl_exportacao_id_exportacao_seq
	INCREMENT BY 1
	MINVALUE 1
	MAXVALUE 2147483647
	START 1
	CACHE 1
	NO CYCLE;
-- DROP SEQUENCE public.tbl_importacao_id_importacao_seq;

CREATE SEQUENCE public.tbl_importacao_id_importacao_seq
	INCREMENT BY 1
	MINVALUE 1
	MAXVALUE 2147483647
	START 1
	CACHE 1
	NO CYCLE;
-- DROP SEQUENCE public.tbl_processamento_id_processamento_seq;

CREATE SEQUENCE public.tbl_processamento_id_processamento_seq
	INCREMENT BY 1
	MINVALUE 1
	MAXVALUE 2147483647
	START 1
	CACHE 1
	NO CYCLE;
-- DROP SEQUENCE public.tbl_prod_imp_exp_id_tipo_prod_imp_exp_seq;

CREATE SEQUENCE public.tbl_prod_imp_exp_id_tipo_prod_imp_exp_seq
	INCREMENT BY 1
	MINVALUE 1
	MAXVALUE 2147483647
	START 1
	CACHE 1
	NO CYCLE;
-- DROP SEQUENCE public.tbl_producao_id_producao_seq;

CREATE SEQUENCE public.tbl_producao_id_producao_seq
	INCREMENT BY 1
	MINVALUE 1
	MAXVALUE 2147483647
	START 1
	CACHE 1
	NO CYCLE;
-- DROP SEQUENCE public.tbl_tipo_cultivo_id_tipo_cultivo_seq;

CREATE SEQUENCE public.tbl_tipo_cultivo_id_tipo_cultivo_seq
	INCREMENT BY 1
	MINVALUE 1
	MAXVALUE 2147483647
	START 1
	CACHE 1
	NO CYCLE;
-- DROP SEQUENCE public.tbl_tipo_uva_id_tipo_uva_seq;

CREATE SEQUENCE public.tbl_tipo_uva_id_tipo_uva_seq
	INCREMENT BY 1
	MINVALUE 1
	MAXVALUE 2147483647
	START 1
	CACHE 1
	NO CYCLE;-- public.tbl_comercializacao definição

-- Drop table

-- DROP TABLE public.tbl_comercializacao;

CREATE TABLE public.tbl_comercializacao (
	id_comercializacao serial4 NOT NULL,
	ds_produto varchar(100) NOT NULL,
	tp_produto varchar(100) NOT NULL,
	dt_ano date NOT NULL,
	qt_comercializacao numeric(10, 2) NULL,
	CONSTRAINT tbl_comercializacao_pkey PRIMARY KEY (id_comercializacao)
);


-- public.tbl_prod_imp_exp definição

-- Drop table

-- DROP TABLE public.tbl_prod_imp_exp;

CREATE TABLE public.tbl_prod_imp_exp (
	id_tipo_prod_imp_exp serial4 NOT NULL,
	ds_tipo_prod_imp_exp varchar(100) NOT NULL,
	CONSTRAINT tbl_prod_imp_exp_pkey PRIMARY KEY (id_tipo_prod_imp_exp)
);


-- public.tbl_producao definição

-- Drop table

-- DROP TABLE public.tbl_producao;

CREATE TABLE public.tbl_producao (
	id_producao serial4 NOT NULL,
	ds_produto varchar(100) NOT NULL,
	tp_produto varchar(100) NOT NULL,
	dt_ano integer NOT NULL,
	qt_producao numeric(15, 2) NULL,
	CONSTRAINT tbl_producao_pkey PRIMARY KEY (id_producao)
);


-- public.tbl_tipo_cultivo definição

-- Drop table

-- DROP TABLE public.tbl_tipo_cultivo;

CREATE TABLE public.tbl_tipo_cultivo (
	id_tipo_cultivo serial4 NOT NULL,
	ds_tipo_cultivo varchar(100) NOT NULL,
	CONSTRAINT tbl_tipo_cultivo_pkey PRIMARY KEY (id_tipo_cultivo)
);


-- public.tbl_tipo_uva definição

-- Drop table

-- DROP TABLE public.tbl_tipo_uva;

CREATE TABLE public.tbl_tipo_uva (
	id_tipo_uva serial4 NOT NULL,
	ds_tipo_uva varchar(100) NOT NULL,
	CONSTRAINT tbl_tipo_uva_pkey PRIMARY KEY (id_tipo_uva)
);


-- public.tbl_cultivo definição

-- Drop table

-- DROP TABLE public.tbl_cultivo;

CREATE TABLE public.tbl_cultivo (
	id_cultivo serial4 NOT NULL,
	ds_cultivo varchar(100) NOT NULL,
	id_tipo_cultivo int4 NOT NULL,
	id_tipo_uva int4 NOT NULL,
	CONSTRAINT tbl_cultivo_pkey PRIMARY KEY (id_cultivo),
	CONSTRAINT fk_tipo_cultivo FOREIGN KEY (id_tipo_cultivo) REFERENCES public.tbl_tipo_cultivo(id_tipo_cultivo),
	CONSTRAINT fk_tipo_uva FOREIGN KEY (id_tipo_uva) REFERENCES public.tbl_tipo_uva(id_tipo_uva)
);


-- public.tbl_exportacao definição

-- Drop table

-- DROP TABLE public.tbl_exportacao;

CREATE TABLE public.tbl_exportacao (
	id_exportacao serial4 NOT NULL,
	id_tipo_prod_imp_exp int4 NOT NULL,
	ds_pais varchar(100) NOT NULL,
	dt_ano date NOT NULL,
	qt_exportacao numeric(10, 2) NULL,
	vl_exportacao numeric(10, 2) NULL,
	CONSTRAINT tbl_exportacao_pkey PRIMARY KEY (id_exportacao),
	CONSTRAINT fk_id_tipo_prod_exp FOREIGN KEY (id_tipo_prod_imp_exp) REFERENCES public.tbl_prod_imp_exp(id_tipo_prod_imp_exp)
);


-- public.tbl_importacao definição

-- Drop table

-- DROP TABLE public.tbl_importacao;

CREATE TABLE public.tbl_importacao (
	id_importacao serial4 NOT NULL,
	id_tipo_prod_imp_exp int4 NOT NULL,
	ds_pais varchar(100) NOT NULL,
	dt_ano date NOT NULL,
	qt_importacao numeric(10, 2) NULL,
	vl_importacao numeric(10, 2) NULL,
	CONSTRAINT tbl_importacao_pkey PRIMARY KEY (id_importacao),
	CONSTRAINT fk_id_tipo_prod_imp FOREIGN KEY (id_tipo_prod_imp_exp) REFERENCES public.tbl_prod_imp_exp(id_tipo_prod_imp_exp)
);


-- public.tbl_processamento definição

-- Drop table

-- DROP TABLE public.tbl_processamento;

CREATE TABLE public.tbl_processamento (
	id_processamento serial4 NOT NULL,
	id_cultivo int4 NOT NULL,
	dt_ano date NOT NULL,
	qt_processamento numeric(10, 2) NULL,
	CONSTRAINT tbl_processamento_pkey PRIMARY KEY (id_processamento),
	CONSTRAINT fk_id_cultivo FOREIGN KEY (id_cultivo) REFERENCES public.tbl_cultivo(id_cultivo)
);

-- public.tbl_usuario definição

-- Drop table

-- DROP TABLE public.tbl_usuario;

CREATE TABLE public.tbl_usuario (
	username varchar(255) NOT NULL,
	password varchar(255) NOT NULL,
    CONSTRAINT tbl_usuario_pkey PRIMARY KEY (username)
);
