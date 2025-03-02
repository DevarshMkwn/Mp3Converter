-- Step 1: Create a new MySQL user
CREATE USER 'auth_user'@'localhost' IDENTIFIED BY 'auth_pass';

-- Step 2: Create a new database for the Auth Service
CREATE DATABASE auth_db;

-- Step 3: Grant privileges to the user
GRANT ALL PRIVILEGES ON auth_db.* TO 'auth_user'@'localhost';

-- Step 4: Switch to the database
USE auth_db;

-- Step 5: Create the users table
CREATE TABLE users (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO users (email, password) VALUES ('johndoe@example.com', 'SecurePassword123');

-- Step 6: Apply changes
FLUSH PRIVILEGES;
