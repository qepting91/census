import pandas as pd
import pgeocode

def get_lat_lon(zip_code, country_code="US"):
    nomi = pgeocode.Nominatim(country_code)
    location = nomi.query_postal_code(zip_code)
    return location.latitude, location.longitude

# Read the CSV file
df = pd.read_csv("demographics.csv")

# Add latitude and longitude columns to the DataFrame
df["Latitude"], df["Longitude"] = zip(*df["JURISDICTION NAME"].apply(get_lat_lon))

# Save the updated DataFrame to a new CSV file
df.to_csv("demographics_with_lat_lon.csv", index=False)