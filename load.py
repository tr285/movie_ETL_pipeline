import requests
import os
import mysql.connector
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY")

# DB connection
conn = mysql.connector.connect(
    host="localhost",
    user="etl_user",
    password="tukaram143",
    database="movie_db"
)
cursor = conn.cursor()

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