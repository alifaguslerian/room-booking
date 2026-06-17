-- Active: 1781500825804@@127.0.0.1@3311@room_booking
CREATE DATABASE IF NOT EXISTS room_booking;

USE room_booking;

CREATE TABLE
    users (
        id INT AUTO_INCREMENT PRIMARY KEY,
        username VARCHAR(50) NOT NULL UNIQUE,
        email VARCHAR(100) NOT NULL UNIQUE,
        password_hash VARCHAR(255) NOT NULL,
        role ENUM ('admin', 'user') DEFAULT 'user',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );

CREATE TABLE
    rooms (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(100) NOT NULL,
        location VARCHAR(100) NOT NULL,
        capacity INT NOT NULL,
        facilities TEXT,
        status ENUM ('available', 'maintenance') DEFAULT 'available',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );

CREATE TABLE
    bookings (
        id INT AUTO_INCREMENT PRIMARY KEY,
        user_id INT NOT NULL,
        room_id INT NOT NULL,
        title VARCHAR(100) NOT NULL,
        date DATE NOT NULL,
        start_time TIME NOT NULL,
        end_time TIME NOT NULL,
        status ENUM ('pending', 'approved', 'rejected', 'cancelled') DEFAULT 'pending',
        notes TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE,
        FOREIGN KEY (room_id) REFERENCES rooms (id) ON DELETE CASCADE
    );

-- default admin account (password: admin123)
INSERT INTO
    users (username, email, password_hash, role)
VALUES
    (
        'admin',
        'admin@roombooking.com',
        'scrypt:32768:8:1$placeholder$replacethisafterrunningsetup',
        'admin'
    );