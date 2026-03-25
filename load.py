import requests
import pandas as pd
import os
import mysql.connector


load_dotenv()

API_KEY = st.secrets["95b004a25357fddd1f5995fb9de2c79b"]

import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Movie Dashboard", layout="wide")

df = pd.read_csv("movies.csv")
df['release_date'] = pd.to_datetime(df['release_date'])

# Extract + Transform (reuse logic)
url = f"https://api.themoviedb.org/3/movie/popular?api_key={API_KEY}"

response = requests.get(url)
data = response.json()

clean_data = []

for movie in data['results']:
    movie_dict = (
        movie.get('id'),
        movie.get('title'),
        movie.get('release_date'),
        movie.get('vote_average'),
        movie.get('popularity')
    )
    clean_data.append(movie_dict)

# Load into DB
query = """
INSERT INTO movies (id, title, release_date, rating, popularity)
VALUES (%s, %s, %s, %s, %s)
"""

cursor.executemany(query, clean_data)

conn.commit()

print("✅ Data inserted successfully!")

cursor.close()
conn.close()

df = pd.DataFrame(clean_data)
df.to_csv("movies.csv", index=False)

print("✅ CSV file created!")