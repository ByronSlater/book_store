DROP TABLE IF EXISTS books CASCADE;

CREATE TABLE
    books (
        id SERIAL PRIMARY KEY,
        title VARCHAR UNIQUE,
        author_id INT
    );


DROP TABLE IF EXISTS authors CASCADE;

CREATE TABLE
    authors (
        id SERIAL PRIMARY KEY,
        name VARCHAR,
        dob VARCHAR
    );
