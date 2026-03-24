import streamlit as st
import mysql.connector
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Movie Dashboard", layout="wide")

# ------------------ SIDEBAR ------------------
st.sidebar.title("🎛️ Controls")

# DB connection
conn = mysql.connector.connect(
    host="localhost",
    user="etl_user",
    password="password123",
    database="movie_db"
)

query = "SELECT * FROM movies"
df = pd.read_sql(query, conn)

# Convert date
df['release_date'] = pd.to_datetime(df['release_date'])

# Sidebar filters
search = st.sidebar.text_input("🔍 Search Movie")

min_rating = st.sidebar.slider("⭐ Min Rating", 0.0, 10.0, 5.0)

start_date = st.sidebar.date_input("📅 Start Date", df['release_date'].min())
end_date = st.sidebar.date_input("📅 End Date", df['release_date'].max())

# Apply filters
filtered_df = df[
    (df['rating'] >= min_rating) &
    (df['release_date'] >= pd.to_datetime(start_date)) &
    (df['release_date'] <= pd.to_datetime(end_date))
]

if search:
    filtered_df = filtered_df[filtered_df['title'].str.contains(search, case=False)]

# ------------------ HEADER ------------------
st.title("🎬 Movie Analytics Dashboard")

# ------------------ KPI CARDS ------------------
col1, col2, col3 = st.columns(3)

col1.metric("🎥 Total Movies", len(filtered_df))
col2.metric("⭐ Avg Rating", round(filtered_df['rating'].mean(), 2))
col3.metric("🔥 Max Popularity", round(filtered_df['popularity'].max(), 2))

st.markdown("---")

# ------------------ DOWNLOAD BUTTON ------------------
csv = filtered_df.to_csv(index=False).encode('utf-8')
st.download_button("📥 Download Data", csv, "movies.csv", "text/csv")

# ------------------ TABLE ------------------
st.subheader("📊 Movie Data")
st.dataframe(filtered_df)

# ------------------ CHARTS ------------------

col1, col2 = st.columns(2)

# Top Rated Movies
top_movies = filtered_df.sort_values(by="rating", ascending=False).head(10)
fig1 = px.bar(top_movies, x="title", y="rating", title="Top Rated Movies", color="rating")
col1.plotly_chart(fig1, use_container_width=True)

# Most Popular Movies
popular_movies = filtered_df.sort_values(by="popularity", ascending=False).head(10)
fig2 = px.bar(popular_movies, x="title", y="popularity", title="Most Popular Movies", color="popularity")
col2.plotly_chart(fig2, use_container_width=True)

# ------------------ LINE CHART ------------------
st.subheader("📈 Rating Trend Over Time")
fig3 = px.line(filtered_df.sort_values("release_date"), x="release_date", y="rating")
st.plotly_chart(fig3, use_container_width=True)

# ------------------ INSIGHTS ------------------
st.subheader("🧠 Insights")

if not filtered_df.empty:
    top_movie = filtered_df.loc[filtered_df['rating'].idxmax()]
    st.success(f"Top Rated Movie: {top_movie['title']} ⭐ {top_movie['rating']}")

    popular_movie = filtered_df.loc[filtered_df['popularity'].idxmax()]
    st.info(f"Most Popular Movie: {popular_movie['title']} 🔥 {popular_movie['popularity']}")
else:
    st.warning("No data available for selected filters")