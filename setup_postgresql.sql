# R3ÆLƎR AI - PostgreSQL Setup Script
# Run this after resetting the user password in PostgreSQL

# For Windows: Save as setup_postgresql.sql and run with psql
# psql -U postgres < setup_postgresql.sql

-- Connect to the database
\connect postgres;

-- Drop old user if exists (be careful with production!)
-- DROP USER IF EXISTS r3aler_user_2025;

-- Create user with password
CREATE USER r3aler_user_2025 WITH PASSWORD 'R3AL3RAdmin816';

-- Create database if it doesn't exist
CREATE DATABASE r3aler_ai OWNER r3aler_user_2025;

-- Connect to the new database
\connect r3aler_ai;

-- Grant all privileges
GRANT ALL PRIVILEGES ON DATABASE r3aler_ai TO r3aler_user_2025;

-- Grant schema privileges
GRANT ALL PRIVILEGES ON SCHEMA public TO r3aler_user_2025;

-- Grant default privileges for future tables
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO r3aler_user_2025;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON SEQUENCES TO r3aler_user_2025;

-- Verify user was created
\du r3aler_user_2025;

-- Verify database was created
\l r3aler_ai;

-- Test connection (exit and run: psql -h 127.0.0.1 -U r3aler_user_2025 -d r3aler_ai)
