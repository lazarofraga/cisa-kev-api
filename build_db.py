import sqlite3
import requests

# URL for the CISA KEV list
url = "https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json"

# Download the JSON data
response = requests.get(url)
if response.status_code != 200:
    print("Failed to download the KEV list.")
    exit(1)

kev_data = response.json()

# Connect to SQLite database (it will create the file if it doesn't exist)
conn = sqlite3.connect("kev_list.db")
cursor = conn.cursor()

# Create a table to store the KEV list
cursor.execute("""
CREATE TABLE IF NOT EXISTS vulnerabilities (
    cveID TEXT PRIMARY KEY,
    vendorProject TEXT,
    product TEXT,
    vulnerabilityName TEXT,
    dateAdded TEXT,
    shortDescription TEXT,
    requiredAction TEXT,
    dueDate TEXT,
    notes TEXT
)
""")

# Insert the KEV data into the table
for item in kev_data['vulnerabilities']:
    cursor.execute("""
    INSERT INTO vulnerabilities (
        cveID,
        vendorProject,
        product,
        vulnerabilityName,
        dateAdded,
        shortDescription,
        requiredAction,
        dueDate,
        notes)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        item['cveID'],
        item['vendorProject'],
        item['product'],
        item['vulnerabilityName'],
        item['dateAdded'],
        item['shortDescription'],
        item['requiredAction'],
        item['dueDate'],
        item.get('notes', '')  # Assuming 'notes' might be optional
    ))

# Commit the changes and close the connection
conn.commit()
conn.close()

print("KEV list downloaded and stored in SQLite database successfully.")
