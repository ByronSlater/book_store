DROP TABLE IF EXISTS books CASCADE;

CREATE TABLE
    books (
        id INTEGER PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
        title VARCHAR,
        author_id INT
    );


DROP TABLE IF EXISTS authors CASCADE;

CREATE TABLE
    authors (
        id INTEGER PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
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
        id INTEGER PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
        username VARCHAR UNIQUE,
        password VARCHAR
    );
