import sqlite3
import os

# Create data directory if it doesn't exist
os.makedirs('data', exist_ok=True)

# Connect to database (creates it if it doesn't exist)
conn = sqlite3.connect('data/realer_ai.db')
cursor = conn.cursor()

# Create tables
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY, 
    username TEXT UNIQUE NOT NULL, 
    password_hash TEXT NOT NULL, 
    email TEXT,
    role TEXT NOT NULL DEFAULT 'user'
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS treadmill_logs (
    id INTEGER PRIMARY KEY, 
    ip TEXT NOT NULL, 
    metadata TEXT, 
    geolocation TEXT, 
    threat_score INTEGER, 
    created_at TEXT NOT NULL
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS auth_attempts (
    id INTEGER PRIMARY KEY, 
    ip TEXT NOT NULL, 
    success BOOLEAN NOT NULL, 
    created_at TEXT NOT NULL
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS heart_storage (
    id INTEGER PRIMARY KEY, 
    user_id TEXT NOT NULL, 
    insight TEXT NOT NULL, 
    created_at TEXT NOT NULL
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS conversations (
    id INTEGER PRIMARY KEY,
    user_id TEXT NOT NULL,
    user_message TEXT NOT NULL,
    ai_response TEXT NOT NULL,
    created_at TEXT NOT NULL
)
''')

conn.commit()
conn.close()

print("Database created successfully!")