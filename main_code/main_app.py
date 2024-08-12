import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from youtubesearchpython import VideosSearch
from pytube import YouTube
import os

class SpotifyDownloader:
    def __init__(self, uri):
        self.spotify_uri = uri
    
    def generate_lists(self):
        spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(client_id='7744baa8c2744135ad93fa9d6a62f9ba',
                                                                                        client_secret='31b5e1356a5544e788d54721d8330958'))
        results = spotify.playlist_items(self.spotify_uri)
        global all_songs
        all_songs = []
        for result in results['items']:
            songs_data = {}
            if result['track'] != None:
                if 'album' in result['track']:
                    # only download available songs
                    try:
                        if 'images' in result['track']['album'] and 'name' in result['track'] and 'artists' in result['track']:
                            songs_data['image'] = result['track']['album']['images'][0]['url']
                            songs_data['name'] = result['track']['name']
                            songs_data['artists'] = result['track']['artists'][0]['name']
                    except:
                        # directly skip songs that can't be reached
                        pass
            all_songs.append(songs_data)
        return all_songs
    
    def get_download_links(self):
        # get all songs' youtube url
        songs = self.generate_lists()
        songs_url = []
        for song in songs:
            videosSearch = VideosSearch(f"{song['artists']} - {song['name']}", limit=1)
            result = videosSearch.result()['result'][0]['id']
            print(f"Fetching from https://www.youtube.com/watch?v={result} ......")
            songs_url.append("https://www.youtube.com/watch?v=" + result)
        return songs_url

    def download_musics(self):
        # this function download the songs
        video_links = self.get_download_links()
        global all_songs
        for number, video_link in enumerate(video_links):
            yt = YouTube(video_link)
            print(f'Downloading {all_songs[number]["name"]}')
            music_file = yt.streams.get_audio_only()
            output_file = music_file.download(output_path="./audios")
            base, ext = os.path.splitext(output_file)
            new_file = base + '.mp3'
            os.rename(output_file, new_file)
        
        print("Completed! You can now find your songs in the 'audios' folder")  
        return True