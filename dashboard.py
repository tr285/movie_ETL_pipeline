import streamlit as st
import pandas as pd
import requests
import os
from dotenv import load_dotenv
import plotly.express as px
from streamlit_autorefresh import st_autorefresh

load_dotenv()

st.set_page_config(page_title="Live Movie Dashboard", layout="wide")

st.title("🎬 Live Movie Analytics Dashboard")

# 🔄 Auto refresh every 60 seconds
st_autorefresh(interval=60000, key="refresh")

API_KEY = os.getenv("API_KEY")

# ------------------ FETCH LIVE DATA ------------------
url = f"https://api.themoviedb.org/3/movie/popular?api_key={API_KEY}"
response = requests.get(url)
data = response.json()

movies = []

for m in data['results']:
    movies.append({
        "id": m.get('id'),
        "title": m.get('title'),
        "release_date": m.get('release_date'),
        "rating": m.get('vote_average'),
        "popularity": m.get('popularity')
    })

df = pd.DataFrame(movies)
df['release_date'] = pd.to_datetime(df['release_date'])

# ------------------ SIDEBAR ------------------
st.sidebar.title("🎛️ Filters")

search = st.sidebar.text_input("🔍 Search Movie")
min_rating = st.sidebar.slider("⭐ Min Rating", 0.0, 10.0, 5.0)

filtered_df = df[df['rating'] >= min_rating]

if search:
    filtered_df = filtered_df[filtered_df['title'].str.contains(search, case=False)]

# ------------------ KPI ------------------
col1, col2, col3 = st.columns(3)

col1.metric("🎥 Movies Loaded", len(filtered_df))
col2.metric("⭐ Avg Rating", round(filtered_df['rating'].mean(), 2))
col3.metric("🔥 Max Popularity", round(filtered_df['popularity'].max(), 2))

st.markdown("---")

# ------------------ TABLE ------------------
st.subheader("📊 Live Movie Data")
st.dataframe(filtered_df)

# ------------------ CHARTS ------------------
col1, col2 = st.columns(2)

top_movies = filtered_df.sort_values(by="rating", ascending=False).head(10)
fig1 = px.bar(top_movies, x="title", y="rating", title="Top Rated Movies")
col1.plotly_chart(fig1, use_container_width=True)

popular_movies = filtered_df.sort_values(by="popularity", ascending=False).head(10)
fig2 = px.bar(popular_movies, x="title", y="popularity", title="Most Popular Movies")
col2.plotly_chart(fig2, use_container_width=True)

# ------------------ INSIGHT ------------------
st.subheader("🧠 Insight")

if not filtered_df.empty:
    best = filtered_df.loc[filtered_df['rating'].idxmax()]
    st.success(f"Top Movie: {best['title']} ⭐ {best['rating']}")