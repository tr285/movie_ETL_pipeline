import streamlit as st
import mysql.connector
import pandas as pd

st.title("🎬 Movie ETL Dashboard")

# DB connection
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="tukaram143",
    database="movie_db"
)

query = "SELECT * FROM movies"
df = pd.read_sql(query, conn)

# Show data
st.subheader("📊 Movie Data")
st.dataframe(df)

# Top rated movies
st.subheader("⭐ Top Rated Movies")
top_movies = df.sort_values(by="rating", ascending=False).head(10)
st.dataframe(top_movies)

# Popular movies
st.subheader("🔥 Most Popular Movies")
popular_movies = df.sort_values(by="popularity", ascending=False).head(10)
st.dataframe(popular_movies)