import NswAPI_call
import sqlite3

def ingest_data_to_database(fuel_data):
    """
    Ingests the provided fuel data into a SQLite database.
    
    This function connects to a SQLite database (or creates one if it doesn't exist),
    sets up the necessary tables, and populates those tables with data from the
    provided fuel_data dictionary.
    
    The function creates two tables: 'stations' and 'prices', with the respective 
    fields matching the keys of the dictionary.
    
    Args:
        fuel_data (dict): A dictionary containing lists of station and price data.
    """
    conn = sqlite3.connect('fuel_data.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS stations (
            brandid TEXT,
            stationid TEXT,
            brand TEXT,
            code TEXT PRIMARY KEY,
            name TEXT,
            address TEXT,
            latitude REAL,
            longitude REAL
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS prices (
            stationcode TEXT,
            fueltype TEXT,
            price REAL,
            lastupdated TEXT,
            PRIMARY KEY (stationcode, fueltype, lastupdated)
        )
    ''')

    for station in fuel_data['stations']:
        cursor.execute('''
            INSERT OR REPLACE INTO stations (brandid, stationid, brand, code, name, address, latitude, longitude)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            station['brandid'],
            station['stationid'],
            station['brand'],
            station['code'],
            station['name'],
            station['address'],
            station['location']['latitude'],
            station['location']['longitude']
        ))

    
    for price in fuel_data['prices']:
        cursor.execute('''
            INSERT OR REPLACE INTO prices (stationcode, fueltype, price, lastupdated)
            VALUES (?, ?, ?, ?)
        ''', (
            price['stationcode'],
            price['fueltype'],
            price['price'],
            price['lastupdated']
        ))

    conn.commit()
    conn.close()
    

def main():
    """
    Main function to orchestrate the data ingestion process.
    
    This function first fetches the fuel data using the NswAPI_call module and 
    then ingests the fetched data into the SQLite database. If the fuel data cannot
    be fetched, an error message is printed.
    """
    fuel_data = NswAPI_call.main()
    if fuel_data:
        ingest_data_to_database(fuel_data)
    else:
        print("Failed to fetch fuel data.")

if __name__ == "__main__":
    main()