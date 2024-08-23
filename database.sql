DROP TABLE IF EXISTS url_checks;
DROP TABLE IF EXISTS urls;

CREATE TABLE urls (
	id bigserial NOT NULL,
	name varchar NULL,
	created_at date NULL,
	CONSTRAINT urls_pk PRIMARY KEY (id)
);

CREATE TABLE url_checks (
	id bigserial NOT NULL,
	url_id int8 NOT NULL,
	status_code int4 NULL,
	h1 varchar NULL,
	title varchar NULL,
	description varchar NULL,
	created_at date NULL,
	CONSTRAINT url_checks_fk FOREIGN KEY (url_id) REFERENCES urls(id)
);
