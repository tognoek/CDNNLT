CREATE DATABASE vietnambooking;
USE vietnambooking;
CREATE TABLE hot_destination (
    id_post INT PRIMARY KEY,
    tour_type_category VARCHAR(255),
    image VARCHAR(255),
    name VARCHAR(255),
    url VARCHAR(255),
    type VARCHAR(50),
    count INT
);
CREATE TABLE list_tour (
    id_post INT PRIMARY KEY,
    name VARCHAR(255),
    image VARCHAR(255),
    url VARCHAR(255),
    type VARCHAR(50),
    count INT
);
CREATE TABLE list_tour_all (
    id_post INT PRIMARY KEY,
    name VARCHAR(255),
    url VARCHAR(255),
    category VARCHAR(50),
    price DECIMAL(30, 2),
    image VARCHAR(255),
    type VARCHAR(50),
    location VARCHAR(255),
    code VARCHAR(255)
);
