import sqlite3

# Connect to the database
conn = sqlite3.connect("users.db")
cursor = conn.cursor()

# Add a new user
new_username = "admin"
new_password = "admin123"

try:
    cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", 
                  (new_username, new_password))
    conn.commit()
    print(f"User '{new_username}' added successfully")
except sqlite3.Error as e:
    print(f"Error adding user: {e}")

# Verify all users
print("\nAll users in database:")
cursor.execute("SELECT * FROM users")
users = cursor.fetchall()
for user in users:
    print(f"User ID: {user[0]}, Username: {user[1]}, Password: {user[2]}")

conn.close() 