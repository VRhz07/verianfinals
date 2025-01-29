import sqlite3
import os

# Get the current directory
current_dir = os.path.dirname(os.path.abspath(__file__))

# Construct the path to the database file
db_path = os.path.join(current_dir, 'db.sqlite3')

# Connect to the SQLite database
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Query to get all table names
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")

# Fetch all results
tables = cursor.fetchall()

# Print the table names
print("Existing tables in the database:")
for table in tables:
    print(table[0])

# Count the number of tables
table_count = len(tables)
print(f"\nTotal number of tables: {table_count}")

# Close the connection
conn.close()

print("\nDatabase inspection completed.")