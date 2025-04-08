from datetime import datetime
import json
import sqlite3


def get_json(file):
    # Load data from JSON file
    with open(file, 'r') as file:
        data = json.load(file)
    return data


def connect_push_db(json_file):
    # Connect to SQLite3 database (or create it)
    conn = sqlite3.connect('funddata.db')
    cursor = conn.cursor()

    # Create table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS portfolio (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    scheme_name TEXT,
    scheme_code INTEGER,
    date TEXT,
    mutual_fund_family TEXT,
    units INTEGER,
    latest_price INTEGER
    )
    ''')

    # Insert data into table
    data = get_json(json_file)
    for schemes in data:
        date = datetime.strptime(schemes['Date'], "%d-%b-%Y")
        date = datetime.strftime(date, "%Y-%m-%d")
        cursor.execute(f'''INSERT INTO portfolio (
                           scheme_code,
                           scheme_name,
                           date,
                           mutual_fund_family,
                           units,
                           latest_price)
                VALUES ({schemes['Scheme_Code']}, '{str(schemes["Scheme_Name"])}', '{date}',
                '{str(schemes["Mutual_Fund_Family"])}',{schemes['Units']},{schemes['Latest_Price']})''')

    # Commit changes and close connection
    conn.commit()
    conn.close()
    print("✅ Data successfully imported into SQLite database.")
