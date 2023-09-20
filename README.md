
# Census Data Exploration

This project is a Streamlit application that provides an interactive exploration of census data aggregated at the zip code level. The data is enriched with geocoding to provide latitude and longitude coordinates for each zip code, enabling geographical visualizations.

## Files in the Project

1. `census.py`: Main Streamlit application file. Handles data loading, processing, and visualization.
2. `latlong.py`: Utility file to convert zip codes into latitude and longitude using the pgeocode library.
3. `Demographic_Statistics_By_Zip_Code.csv`: Raw demographic data aggregated by zip code.
4. `demolatlong.csv`: Enriched demographic data with added geographical coordinates.
5. `requirements.txt`: Lists all the Python dependencies required to run the project.

## How to Run

1. Ensure you have Python installed.
2. Install the required dependencies:
```
pip install -r requirements.txt
```
3. Run the Streamlit app:
```
streamlit run census.py
```

## License

MIT License

Copyright (c) 2023 [qepting91]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
