import requests
import json
import os
from dotenv import load_dotenv


load_dotenv(dotenv_path='./.env')

API_KEY = os.getenv('API_KEY')
CHANNEL_HANDLE = 'MrBeast'

url =  f'https://youtube.googleapis.com/youtube/v3/channels?part=contentDetails&forHandle={CHANNEL_HANDLE}&key={API_KEY}'

response = requests.get(url)

print(response.json())

data = response.json()
 
print(json.dumps(data, indent=4)) 