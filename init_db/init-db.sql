-- Create the database (This step is typically done through a PostgreSQL client or administrative interface)
-- CREATE DATABASE levseq;

-- Connect to the database (This is a step you'd do through your client, command line, or connection string in your application)
\c levseq;

-- Create the roles table
CREATE TABLE roles (
    id SERIAL PRIMARY KEY,
    role_name VARCHAR(255) NOT NULL UNIQUE,
    description TEXT
);

-- Create the users table
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    role_id INT,
    username VARCHAR(80) UNIQUE NOT NULL,
    email VARCHAR(80) UNIQUE NOT NULL,
    password BYTEA, -- Corresponds to LargeBinary in SQLAlchemy
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
    first_name VARCHAR(30),
    last_name VARCHAR(30),
    active BOOLEAN DEFAULT FALSE,
    is_admin BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (role_id) REFERENCES roles(id)
);

-- Create the groups table
CREATE TABLE groups (
    id SERIAL PRIMARY KEY,
    user_id INT,
    owner_id INT,
    group_name VARCHAR(255),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (owner_id) REFERENCES users(id)
);

-- Create the batch experiments table, this has the overarching ID for the database
CREATE TABLE batch (
    id SERIAL PRIMARY KEY,
    user_created INT,
    group_id INT,
    name VARCHAR(255),
    meta text,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    date_last_edited TIMESTAMP WITH TIME ZONE,
    FOREIGN KEY (user_created) REFERENCES users(id),
    FOREIGN KEY (group_id) REFERENCES groups(id)
);

-- Create the experiments table
CREATE TABLE experiments (
    id SERIAL PRIMARY KEY,
    user_created INT,
    group_id INT,
    batch_id INT,
    name VARCHAR(255),
    meta text,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    date_last_edited TIMESTAMP WITH TIME ZONE,
    FOREIGN KEY (batch_id) REFERENCES batch(id),
    FOREIGN KEY (user_created) REFERENCES users(id),
    FOREIGN KEY (group_id) REFERENCES groups(id)
);

-- Create the data table
CREATE TABLE data (
    id SERIAL PRIMARY KEY,
    user_created INT,
    group_id INT,
    experiment_id INT,
    type VARCHAR(255),
    data text,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    date_edited TIMESTAMP WITH TIME ZONE,
    FOREIGN KEY (user_created) REFERENCES users(id),
    FOREIGN KEY (group_id) REFERENCES groups(id),
    FOREIGN KEY (experiment_id) REFERENCES experiments(id)
);

-- Dummy values for testing

-- Roles
INSERT INTO roles (role_name, description) VALUES ('Admin', 'Administrator with full access');
INSERT INTO roles (role_name, description) VALUES ('Editor', 'Can edit existing entries');
INSERT INTO roles (role_name, description) VALUES ('Viewer', 'Can only view entries');

-- Users
-- INSERT INTO users (id, username, email, password, first_name, last_name, active, is_admin) VALUES
-- (1, 'adminuser', 'admin@example.com', 'password', 'Admin', 'User', TRUE, TRUE),
-- (2, 'editoruser', 'editor@example.com', 'password', 'Editor', 'User', TRUE, FALSE),
-- (3, 'vieweruser', 'viewer@example.com', 'password', 'Viewer', 'User', TRUE, FALSE);
--
-- -- Groups
-- INSERT INTO groups (id, user_id, owner_id, group_name, created_at) VALUES
-- (1, 1, 1, 'public', NOW()),
-- (2, 1, 1, 'private', NOW());
--
-- -- Experiments
-- INSERT INTO experiments (id, user_created, group_id, name, meta, created_at, date_last_edited) VALUES
-- (1, 1, 1, 'Experiment 1', '{"description": "First experiment description"}', NOW(), NOW()),
-- (2, 2, 2, 'Experiment 2', '{"description": "Second experiment description"}', NOW(), NOW());

-- Data
-- INSERT INTO data (user_created, group_id, experiment_id, type, data, created_at, date_edited) VALUES
-- (1, 1, 1, 'Type A', '{"value": 100}', NOW(), NOW()),
-- (2, 1, 2, 'Type B', '{"value": 200}', NOW(), NOW()),
-- (3, 2, 1, 'Type C', '{"value": 300}', NOW(), NOW()),
-- (1, 2, 2, 'Type D', '{"value": 400}', NOW(), NOW());

-- Fixing things
-- DROP TABLE IF EXISTS groups CASCADE;
-- DROP TABLE IF EXISTS batch CASCADE;
-- DROP TABLE IF EXISTS experiments CASCADE;
-- DROP TABLE IF EXISTS roles CASCADE;
-- DROP TABLE IF EXISTS users CASCADE;
-- DROP TABLE IF EXISTS data CASCADE;