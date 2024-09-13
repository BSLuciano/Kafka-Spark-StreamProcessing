CREATE DATABASE IF NOT EXISTS project_streaming;
USE project_streaming;

CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    gender VARCHAR(10),
    name_title VARCHAR(20),
    name_first VARCHAR(50),
    name_last VARCHAR(50),
    street_number INT,
    street_name VARCHAR(100),
    city VARCHAR(50),
    state VARCHAR(50),
    country VARCHAR(50),
    postcode VARCHAR(20),
    email VARCHAR(100),
    dob_date TIMESTAMP,
    uuid VARCHAR(100),
    age INT,
    phone VARCHAR(20),
    cell VARCHAR(20),
    picture_large TEXT
);