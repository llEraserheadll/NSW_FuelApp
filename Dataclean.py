import pandas as pd
import sqlite3

def fetch_data_from_db():
    """
    Fetches station and price data from the SQLite database 'fuel_data.db'.
    
    This function connects to the database and retrieves all records from the 
    'stations' and 'prices' tables. The data is then returned as two separate
    pandas DataFrames.
    
    Returns:
        tuple: A tuple containing two DataFrames, one for stations data and one 
               for prices data.
    """
    conn = sqlite3.connect('fuel_data.db')
    cursor = conn.cursor()

    stations_query = 'SELECT * FROM stations'
    stations_data = pd.read_sql_query(stations_query, conn)

    prices_query = 'SELECT * FROM prices'
    prices_data = pd.read_sql_query(prices_query, conn)
    conn.close()  
    
    return stations_data, prices_data

def process_data(stations_data, prices_data):
    """
    Processes the provided stations and prices data.
    
    This function:
    1. Converts the provided data into pandas DataFrames.
    2. Ensures uniform capitalization for station names and addresses.
    3. Handles missing values by filling them with zeroes.
    4. Enforces specific data types for each column.
    
    Args:
        stations_data (DataFrame): DataFrame containing raw stations data.
        prices_data (DataFrame): DataFrame containing raw prices data.
    
    Returns:
        tuple: A tuple containing two processed DataFrames, one for stations data 
               and one for prices data.
    """
    # Convert to DataFrame
    stations_df = pd.DataFrame(stations_data, columns=['brandid', 'stationid', 'brand', 'code', 'name', 'address', 'latitude', 'longitude'])
    prices_df = pd.DataFrame(prices_data, columns=['stationcode', 'fueltype', 'price', 'lastupdated'])

    #This below will make sure all the text fields in use as station name and address are uniformly capitalized in their first letter
    stations_df['address'] = stations_df['address'].str.title()
    stations_df['name'] = stations_df['name'].str.title() 

    #Handling Missing values
    stations_df.fillna(0, inplace=True)
    prices_df.fillna(0, inplace=True)

    # Verify data types and enforcing it
    stations_df = stations_df.astype({
        'brandid': 'str',
        'stationid': 'str',
        'brand': 'str',
        'code': 'str',
        'name': 'str',
        'address': 'str',
        'latitude': 'float64',
        'longitude': 'float64'
    })
    
    prices_df = prices_df.astype({
        'stationcode': 'int64',
        'fueltype': 'str',
        'price': 'float64',
        'lastupdated': 'str'  
    })

    return stations_df, prices_df

def reupload_to_db(stations_df, prices_df):
    """
    Re-uploads processed data back to the SQLite database 'fuel_data.db'.
    
    This function connects to the database and:
    1. Deletes existing records from the 'stations' and 'prices' tables.
    2. Inserts the processed data into the respective tables.
    
    Args:
        stations_df (DataFrame): Processed DataFrame containing stations data.
        prices_df (DataFrame): Processed DataFrame containing prices data.
    """
    conn = sqlite3.connect('fuel_data.db')
    cursor = conn.cursor()

    # Clearing old data
    cursor.execute('DELETE FROM stations')
    cursor.execute('DELETE FROM prices')

    # Inserting clean data into 'stations' table
    stations_df.to_sql('stations', conn, if_exists='append', index=False)

    # Inserting clean data into 'prices' table
    prices_df.to_sql('prices', conn, if_exists='append', index=False)

    conn.commit()
    conn.close()

stations_data, prices_data = fetch_data_from_db()
processed_stations, processed_prices = process_data(stations_data, prices_data)
reupload_to_db(processed_stations, processed_prices)