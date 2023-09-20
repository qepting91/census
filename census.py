import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import folium
from streamlit_folium import folium_static
import pydeck as pdk

# Setting the Streamlit title and description
st.title('Census Data Exploration')
st.write('This analysis will use data aggregated on the zip code level, available from, https://catalog.data.gov/dataset/demographic-statistics-by-zip-code')

# Function to load data
def load_data():
    # Define appropriate data types for each column
    column_dtypes = {
        "JURISDICTION NAME": "int",
        "City": "category",
        "State": "category",
        "Country": "category",
        "Timezone": "category",
        "Area Code": "str"
    }
    # Reload the data with the specified data types
    df = pd.read_csv('demolatlong.csv', dtype=column_dtypes)
    df['JURISDICTION NAME'] = df['JURISDICTION NAME'].astype(str)
    return df

df = load_data()

# Data overview section
if st.checkbox('Show Data Overview'):
    selected_columns = st.multiselect(
        "Select columns to view statistics", df.columns, default=["COUNT PARTICIPANTS", "COUNT FEMALE", "COUNT MALE"]
    )
    if selected_columns:
        st.write(df[selected_columns].describe())

st.divider()

# Heatmap visualization
def create_heatmap(df):
    df = df.dropna(subset=["Latitude", "Longitude"])
    m = folium.Map(location=[df["Latitude"].mean(), df["Longitude"].mean()], zoom_start=10)
    heatmap_data = df[["Latitude", "Longitude"]].values.tolist()
    folium.plugins.HeatMap(heatmap_data).add_to(m)
    return m

if st.checkbox('Census Participant Density by Zip Code'):
    st.write('This map displays Census participation Density by Zip Code.')
    heatmap = create_heatmap(df)
    folium_static(heatmap)

# Permanent resident alien visualization
def create_pr_alien_map(df):
    pr_alien_zipcodes = df[df['COUNT PERMANENT RESIDENT ALIEN'] > 0][['JURISDICTION NAME', 'COUNT PERMANENT RESIDENT ALIEN', 'Latitude', 'Longitude']]
    m = folium.Map(location=[40.730610, -73.935242], zoom_start=10)
    for _, row in pr_alien_zipcodes.iterrows():
        folium.CircleMarker(
            location=[row['Latitude'], row['Longitude']],
            radius=5,
            color='blue',
            fill=True,
            fill_color='blue',
            fill_opacity=0.6,
            popup=f"ZIP Code: {row['JURISDICTION NAME']}<br>Count: {row['COUNT PERMANENT RESIDENT ALIEN']}"
        ).add_to(m)
        folium.Marker(
            location=[row['Latitude'], row['Longitude']],
            icon=folium.DivIcon(html=f"<div style='font-size: 10pt; color: black;'>{row['COUNT PERMANENT RESIDENT ALIEN']}</div>")
        ).add_to(m)
    return m

if st.checkbox('Show Distribution of Permanent Resident Aliens by Zip Code'):
    st.write('''
        This map displays ZIP codes with non-zero counts of permanent resident aliens. The blue markers represent these ZIP codes, 
        with their sizes indicating the number of permanent resident aliens in that area. 
        From the visualization, there's a noticeable concentration of markers in New York City, especially in the Brooklyn and Queens boroughs, 
        with a few markers dispersed in other regions outside of NYC.
    ''')
    pr_alien_map = create_pr_alien_map(df)
    folium_static(pr_alien_map)

# Gender distribution visualization
def plot_gender_distribution(df):
    df = df.dropna(subset=["Latitude", "Longitude"])
    df["gender_balance"] = df["PERCENT FEMALE"] - df["PERCENT MALE"]
    color_scale = [
        [0, 'blue'],
        [0.5, 'grey'],
        [1, 'pink']
    ]
    view_state = pdk.ViewState(
        latitude=df["Latitude"].mean(),
        longitude=df["Longitude"].mean(),
        zoom=10,
        pitch=0
    )
    gender_layer = pdk.Layer(
        "ScatterplotLayer",
        data=df,
        get_position=["Longitude", "Latitude"],
        get_color="gender_balance",
        get_radius="COUNT PARTICIPANTS * 10",
        pickable=True,
        opacity=0.6,
        stroked=True,
        filled=True,
        radius_scale=6,
        radius_min_pixels=5,
        radius_max_pixels=100,
        line_width_min_pixels=1,
        color_scale=color_scale
    )
    gender_map = pdk.Deck(
        map_style="mapbox://styles/mapbox/light-v9",
        initial_view_state=view_state,
        layers=[gender_layer]
    )
    return gender_map_show()

if st.checkbox('Show Gender Distribution by Location'):
    gender_map = plot_gender_distribution(df)
    st.write('This map displays gender distribution by area, separated by the colors blue, pink, and grey.')
    st.pydeck_chart(gender_map_show())
