import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY")

url = f"https://api.themoviedb.org/3/movie/popular?api_key={API_KEY}"

response = requests.get(url)
data = response.json()

clean_data = []

for movie in data['results']:
    movie_dict = {
        "id": movie.get('id'),
        "title": movie.get('title'),
        "release_date": movie.get('release_date'),
        "rating": movie.get('vote_average'),
        "popularity": movie.get('popularity')
    }
    
    clean_data.append(movie_dict)

# print first 5 cleaned records
for item in clean_data[:5]:
    print(item)