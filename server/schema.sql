DROP TABLE IF EXISTS books CASCADE;

CREATE TABLE
    books (
        id SERIAL PRIMARY KEY,
        title VARCHAR,
        author_id INT
    );


DROP TABLE IF EXISTS authors CASCADE;

CREATE TABLE
    authors (
        id SERIAL PRIMARY KEY,
        name VARCHAR UNIQUE,
        dob DATE,
        wikidata_id VARCHAR,
        openlibrary_id VARCHAR,
        picture BYTEA,
        bio TEXT
    );


DROP TABLE IF EXISTS users CASCADE;

CREATE TABLE
    users (
        id SERIAL PRIMARY KEY,
        username VARCHAR UNIQUE,
        password VARCHAR
    );
