import pandas as pd
import sqlite3
import plotly.express as px
import pandas as pd
import streamlit as st
from streamlit_lottie import st_lottie

st.set_page_config(layout='wide')

@st.cache_data(ttl=300)
def get_data_from_database():
    """
    Fetches station and price data from the SQLite database 'fuel_data.db' and 
    returns it as pandas DataFrames.
    
    This function connects to the database, retrieves all records from the 
    'stations' and 'prices' tables, and returns them as two separate pandas 
    DataFrames. It uses Streamlit's caching mechanism to optimize performance 
    and reduce redundant database calls.
    
    Returns:
        tuple: A tuple containing two DataFrames, one for stations data and one 
               for prices data.
    """
    conn = sqlite3.connect('fuel_data.db')
    cursor = conn.cursor()

    stations_query = 'SELECT * FROM stations'
    stations_df = pd.read_sql_query(stations_query, conn)

    prices_query = 'SELECT * FROM prices'
    prices_df = pd.read_sql_query(prices_query, conn)
    conn.close()
    
    return stations_df, prices_df

def main():
    """
    Main function to run the Streamlit app for visualizing fuel price data.
    
    This function:
    1. Fetches the necessary data using the get_data_from_database function.
    2. Processes the data for visualization, including merging tables, date and 
       time parsing, and data sorting.
    3. Uses Plotly and Streamlit to create and display various visualizations, 
       including fuel price trends, fuel type distributions, geographic 
       distributions, and lists of most expensive and cheapest stations.
    """
    stations_df, prices_df = get_data_from_database()
    result = prices_df.merge(stations_df[['name','code','latitude','longitude']], left_on='stationcode', right_on='code')

    result['date'] = pd.to_datetime(result['lastupdated'], format="%d/%m/%Y %H:%M:%S").dt.date
    result['time'] = pd.to_datetime(result['lastupdated'], format="%d/%m/%Y %H:%M:%S").dt.time
    result.drop(columns=['lastupdated'], inplace=True)
    result = result.sort_values(by='date',ascending=False)
    latest_date = result['date'].iloc[0]
    latest_time = result['time'].iloc[0]
    st.title(f"Fuel Price Dashboard (Updated as of {latest_date} at {latest_time})")
    selected_fueltype = st.selectbox('Select Fuel Type', result['fueltype'].unique())



    col1, col2, col3 = st.columns(3)
    with col1:
        # 1. Fuel Price Trend Over Time
        st.header("Fuel Price Trend Over Time")
        fuel_time_chart = px.line(result[result['fueltype'] == selected_fueltype], 
                                x="date", y="price", title=f"Price Trend for {selected_fueltype}")
        fuel_time_chart.update_layout(width=400, height=400)

        st.plotly_chart(fuel_time_chart, use_container_width=False)
    
    with col2:
        st.header("Fuel Type Distribution")
        fuel_dist = px.histogram(result, x="fueltype", title="Distribution of Fuel Types")
        fuel_dist.update_layout(width=400, height=400)
        st.plotly_chart(fuel_dist,use_container_width=False)
    
    with col3:
        st.header("Price Distribution")
        price_dist = px.histogram(result[result['fueltype'] == selected_fueltype], x="price",
                                title=f"Price Distribution for {selected_fueltype}")
        price_dist.update_layout(width=400, height=400)
        st.plotly_chart(price_dist, use_container_width=False)
    
    col5, col6 = st.columns(2)

    with col5:
        st.header("Geographic Distribution of Stations")
        map_chart = px.scatter_mapbox(result[result['fueltype'] == selected_fueltype], lat="latitude", lon="longitude",
                                    color="price", size="price", hover_data=['name', 'price'],
                                    color_continuous_scale=px.colors.cyclical.IceFire, mapbox_style="open-street-map")
        st.plotly_chart(map_chart)
    
    with col6:
        # 5. Most Expensive & Cheapest Stations
        columns_to_display = ['stationcode', 'name', 'price', 'date']
        st.header("Most Expensive & Cheapest Stations")
        top_expensive = result[result['fueltype'] == selected_fueltype].nlargest(5, 'price')[columns_to_display]
        top_cheap = result[result['fueltype'] == selected_fueltype].nsmallest(5, 'price')[columns_to_display]
        sub_col1, sub_col2 = st.columns(2)
        top_expensive['dummy_index'] = ""
        top_cheap['dummy_index'] = ""
        with sub_col1:
            st.write("Most Expensive Stations")
            st.table(top_expensive.set_index("dummy_index"))
        with sub_col2:
            st.write("Cheapest Stations")
            st.table(top_cheap.set_index("dummy_index"))

    
if __name__ == '__main__':
    main()
