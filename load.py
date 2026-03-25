import streamlit as st
import pandas as pd
import requests
import plotly.express as px

st.set_page_config(page_title="Live Movie Dashboard", layout="wide")

st.title("🎬 Live Movie Dashboard")

API_KEY = st.secrets["API_KEY"]

url = f"https://api.themoviedb.org/3/movie/popular?api_key={API_KEY}"
response = requests.get(url)
data = response.json()

movies = []

for m in data['results']:
    movies.append({
        "title": m.get('title'),
        "release_date": m.get('release_date'),
        "rating": m.get('vote_average'),
        "popularity": m.get('popularity')
    })

df = pd.DataFrame(movies)
df['release_date'] = pd.to_datetime(df['release_date'])