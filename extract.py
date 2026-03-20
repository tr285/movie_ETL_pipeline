import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY")

url = f"https://api.themoviedb.org/3/movie/popular?api_key={API_KEY}"

response = requests.get(url)
data = response.json()

for movie in data['results'][:5]:
    print({
        "id": movie['id'],
        "title": movie['title'],
        "release_date": movie['release_date'],
        "rating": movie['vote_average']
    })