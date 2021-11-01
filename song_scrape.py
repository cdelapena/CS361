import requests
from bs4 import BeautifulSoup

url = "https://www.billboard.com/charts/hot-100/2021-10-26"
response = requests.get(url)

soup = BeautifulSoup(response.content, 'html.parser')
artist = BeautifulSoup(response.content, 'html.parser')

songs = soup.find_all(class_="chart-element__information__song text--truncate color--primary")
artists = soup.find_all(class_="chart-element__information__artist text--truncate color--secondary")

song_titles = [song.text.strip() for song in songs]
artist_list = [artist.text.strip() for artist in artists]

print(song_titles)
print(artist_list)