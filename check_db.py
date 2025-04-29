import sqlite3
import os

print(f"Current directory: {os.getcwd()}")
print(f"Database file exists: {os.path.exists('users.db')}")

# Connect to the database
conn = sqlite3.connect("users.db")
cursor = conn.cursor()

# Check database structure
print("\nDatabase tables:")
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()
for table in tables:
    print(f"Table: {table[0]}")
    cursor.execute(f"PRAGMA table_info({table[0]})")
    columns = cursor.fetchall()
    for col in columns:
        print(f"  Column: {col[1]} ({col[2]})")

# Check existing users
print("\nExisting users:")
try:
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    if users:
        for user in users:
            print(f"User ID: {user[0]}, Username: {user[1]}, Password: {user[2]}")
    else:
        print("No users found in the database")
except sqlite3.OperationalError as e:
    print(f"Error querying users: {e}")

# Add a test user
print("\nAdding a test user:")
try:
    cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", 
                  ("testuser", "password"))
    conn.commit()
    print("Test user added successfully")
except sqlite3.Error as e:
    print(f"Error adding user: {e}")

# Verify the user was added
print("\nVerifying users after insert:")
try:
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    for user in users:
        print(f"User ID: {user[0]}, Username: {user[1]}, Password: {user[2]}")
except sqlite3.Error as e:
    print(f"Error querying users: {e}")

conn.close()
print("\nDatabase check complete") 