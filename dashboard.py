import streamlit as st
import pandas as pd
import requests
import plotly.express as px

st.set_page_config(page_title="Live Movie Dashboard", layout="wide")

st.title("🎬 Live Movie Dashboard")

# 🔐 API key from Streamlit secrets
API_KEY = st.secrets["95b004a25357fddd1f5995fb9de2c79b"]

# Fetch live data
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

# KPI
col1, col2, col3 = st.columns(3)
col1.metric("🎥 Movies", len(df))
col2.metric("⭐ Avg Rating", round(df['rating'].mean(), 2))
col3.metric("🔥 Max Popularity", round(df['popularity'].max(), 2))

st.markdown("---")

# Table
st.dataframe(df)

# Charts
fig = px.bar(df.sort_values("rating", ascending=False).head(10),
             x="title", y="rating", title="Top Rated Movies")
st.plotly_chart(fig, use_container_width=True)