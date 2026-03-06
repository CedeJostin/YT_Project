import requests
import json
from datetime import date
import os
from dotenv import load_dotenv


load_dotenv(dotenv_path='./.env')

API_KEY = os.getenv('API_KEY')
CHANNEL_HANDLE = 'MrBeast'
maxResults = 50


def get_playlist_id():
    try:

        url =  f'https://youtube.googleapis.com/youtube/v3/channels?part=contentDetails&forHandle={CHANNEL_HANDLE}&key={API_KEY}'

        response = requests.get(url)
        response.raise_for_status
        data = response.json()

        print(json.dumps(data, indent=4))

        channel_items = data['items'][0]
        channel_playlist_id = channel_items['contentDetails']['relatedPlaylists']['uploads']
        print(f'Channel Playlist ID: {channel_playlist_id}')
        return channel_playlist_id
    except requests.exceptions.RequestException as e:
        print(f'Error fetching channel details: {e}')
        raise e
    



def get_video_ids(playlistId):

    videos_ids = []

    pageToken = None

    base_url = f"https://youtube.googleapis.com/youtube/v3/playlistItems?part=contentDetails&maxResults={maxResults}&playlistId={playlistId}&key={API_KEY}"

    try:
        while True:
            url = base_url 
            if pageToken:
                url += f"&pageToken={pageToken}"
            response = requests.get(url)
            response.raise_for_status()
            data = response.json() 

            for item in data.get('items', []):
                video_id = item['contentDetails']['videoId']
                videos_ids.append(video_id)

            pageToken = data.get('nextPageToken')

            if not pageToken:
                break
        return videos_ids
    except requests.exceptions.RequestException as e:
        raise e
    



def extract_video_data(video_id_lst):
     
    extracted_data = []

    def batch_list(video_id_lst, batch_size):
     for video_id in range(0,len(video_id_lst), batch_size):
        yield video_id_lst[video_id:video_id + batch_size]
    
    try:

        for batch in batch_list(video_id_lst, maxResults):
            video_ids_str = ','.join(batch)
            url = f'https://youtube.googleapis.com/youtube/v3/videos?part=contentDetails&part=snippet&part=statistics&id={video_ids_str}&key={API_KEY}'
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()

            for item in data.get('items', []):

                video_data = {
                    'videoId': item['id'],
                    'title': item['snippet']['title'],
                    'publishedAt': item['snippet']['publishedAt'],
                    'viewCount': item['statistics'].get('viewCount', 0),
                    'likeCount': item['statistics'].get('likeCount', 0),
                    'commentCount': item['statistics'].get('commentCount', 0)
                }
                
                extracted_data.append(video_data)

        return extracted_data
    except requests.exceptions.RequestException as e:
        raise e

def save_to_json(extracted_data):
    file_path = f"./data/YT_data_{date.today()}.json"

    with open(file_path, 'w', encoding='utf-8') as json_outfile:
        json.dump(extracted_data, json_outfile, indent=4, ensure_ascii=False)

if __name__ == "__main__":
    playlistId = get_playlist_id()
    video_id_lst = get_video_ids(playlistId)
    video_data = extract_video_data(video_id_lst)
    save_to_json(video_data)