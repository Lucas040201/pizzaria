CREATE DATABASE pizza;

USE pizza;


CREATE TABLE address (
    id SERIAL PRIMARY KEY,
    cep VARCHAR(8),
    number VARCHAR(5),
    district VARCHAR(50),
    street VARCHAR(100),
    uf VARCHAR(2)
);

CREATE TABLE roles (
    id SERIAL PRIMARY KEY,
    role_name VARCHAR(50)
);


CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50),
    password VARCHAR(50),
    email VARCHAR(50),
    phone VARCHAR(100),
    address_id BIGINT NOT NULL,
    role_id BIGINT NOT NULL
);

ALTER TABLE users ADD CONSTRAINT fk_address FOREIGN KEY(address_id) REFERENCES address(id);
ALTER TABLE users ADD CONSTRAINT fk_role FOREIGN KEY(role_id) REFERENCES roles(id);

INSERT INTO roles (role_name) values ('admin'), ('customer');

Insert INTO address (cep, number, district, street, uf) VALUES ('01133000', '315', 'Bom Retiro', 'Av. Rudge', 'SP');
insert into users (name, password, email, phone, address_id, role_id)  values





