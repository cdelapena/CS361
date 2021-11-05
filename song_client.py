import requests
import json

url = f'http://localhost:9116/'
# Request: {'num_tracks':[number of tracks], 'date': [date that corresponds w/ sunday of any given week]}
# Response: {'artist_1' : 'song_1', 'artist_2':'song_2' ...}
query = {'num_tracks' : 25, 'date' : '2007-06-01'}
json_dump = json.dumps(query)
print(json_dump)
response = requests.post(url=url, json=json_dump)

data = response.json()
print(data)