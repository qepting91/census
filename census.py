import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import folium
from streamlit_folium import folium_static
import pydeck as pdk

st.title('Census Data Exploration')

st.write('This analysis will use data aggregated on the zip code level, available from, https://catalog.data.gov/dataset/demographic-statistics-by-zip-code')


# Load the CSV to inspect its structure
sample_data = pd.read_csv('demolatlong.csv', nrows=10)

# Define appropriate data types for each column
column_dtypes = {
    "JURISDICTION NAME": "int",
    "City": "category",
    "State": "category",
    "Country": "category",
    "Timezone": "category",
    "Area Code": "str"  # We'll keep this as string due to the comma-separated values
}

# For other columns which are more of counts and percentages, set them as appropriate data types
for col in sample_data.columns:
    if "COUNT" in col:
        column_dtypes[col] = "int"
    elif "PERCENT" in col:
        column_dtypes[col] = "float"
    elif col in ["Latitude", "Longitude"]:
        column_dtypes[col] = "float"

# Reload the data with the specified data types
df = pd.read_csv('demolatlong.csv', dtype=column_dtypes)
df['JURISDICTION NAME'] = df['JURISDICTION NAME'].astype(str)

data_overview_toggle = st.toggle('Show Data Overview')
if data_overview_toggle:
    selected_columns = st.multiselect(
        "Select columns to view statistics", df.columns, default=["COUNT PARTICIPANTS", "COUNT FEMALE", "COUNT MALE"]
    )
    if selected_columns:
        st.write(df[selected_columns].describe())
st.divider()

# Title of the app
st.title("Demographic Statistics By Zip Code")

def create_heatmap(df):
    df = df.dropna(subset=["Latitude", "Longitude"])
    m = folium.Map(location=[df["Latitude"].mean(), df["Longitude"].mean()], zoom_start=10)
    heatmap_data = df[["Latitude", "Longitude"]].values.tolist()
    folium.plugins.HeatMap(heatmap_data).add_to(m)
    return m

heatmap = create_heatmap(df)

# Display basic statistics for selected columns
statistics_toggle = st.toggle('Census Participant Density by Zip Code')
if statistics_toggle:
    st.write('''
        This map displays Census participation Density by Zip Code.
    ''')
    folium_static(heatmap)
    

pr_alien_zipcodes = df[df['COUNT PERMANENT RESIDENT ALIEN'] > 0][['JURISDICTION NAME', 'COUNT PERMANENT RESIDENT ALIEN', 'Latitude', 'Longitude']]
pr_alien_map = folium.Map(location=[40.730610, -73.935242], zoom_start=10)

for idx, row in pr_alien_zipcodes.iterrows():
    folium.CircleMarker(
        location=[row['Latitude'], row['Longitude']],
        radius=5,
        color='blue',
        fill=True,
        fill_color='blue',
        fill_opacity=0.6,
        popup=f"ZIP Code: {row['JURISDICTION NAME']}<br>Count: {row['COUNT PERMANENT RESIDENT ALIEN']}"
    ).add_to(pr_alien_map)

    folium.Marker(
        location=[row['Latitude'], row['Longitude']],
        icon=folium.DivIcon(html=f"<div style='font-size: 10pt; color: black;'>{row['COUNT PERMANENT RESIDENT ALIEN']}</div>")
    ).add_to(pr_alien_map)

st.divider()

st.title('Show Distribution of Permanent Resident Aliens by Zip Code')

pr_alien_toggle= st.toggle("Distribution of Permanent Resident Aliens by Zip Code")
if pr_alien_toggle:
    st.write('''
        This map displays ZIP codes with non-zero counts of permanent resident aliens. The blue markers represent these ZIP codes, 
        with their sizes indicating the number of permanent resident aliens in that area. 
        From the visualization, there's a noticeable concentration of markers in New York City, especially in the Brooklyn and Queens boroughs, 
        with a few markers dispersed in other regions outside of NYC.
    ''')
    folium_static(pr_alien_map)

    
def plot_gender_distribution(df):
    # Drop rows with missing latitude or longitude
    df = df.dropna(subset=["Latitude", "Longitude"])

    # Calculate gender balance color
    # Positive values indicate female dominance, negative values indicate male dominance
    df["gender_balance"] = df["PERCENT FEMALE"] - df["PERCENT MALE"]

    # Define color scale: Blue for male dominance, Pink for female dominance, Grey for equal balance
    color_scale = [
        [0, 'blue'],  # Blue for male dominance
        [0.5, 'grey'],  # Grey for equal balance
        [1, 'pink']  # Pink for female dominance
    ]

    # Plot
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

    st.pydeck_chart(gender_map)

# Check if the user wants to view the gender distribution plot
if st.button("Show Gender Distribution by Location"):
    plot_gender_distribution(df)
st.subheader("Blue for male dominance, Pink for female dominance, Grey for equal balance")
