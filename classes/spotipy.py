
import os
from dotenv import load_dotenv

import spotipy
from spotipy.oauth2 import SpotifyOAuth


class SpotipyValues:
    """
    This Class stores the values from the SpotipyAPI Class
    """
    def __init__(self):
        
        self.spotify_status = str
        self.song_id = str
        self.song_name = str
        self.artist_name = str
        self.explicit_song = bool
        self.song_progress = None
        self.song_duration = None
        
        self.top_artists = []
    
    # --- Getters and Setters --- #
    # Status
    def set_spotify_status(self, status):
        self.spotify_status = status
        
    def get_spotify_status(self) -> str:
        return self.spotify_status
    
    # Song ID
    def set_song_id(self, song_id):
        self.song_id = song_id
        
    def get_song_id(self) -> str:
        return self.song_id

    # Song Name
    def set_song_name(self, song_name):
        self.song_name = song_name
        
    def get_song_name(self) -> str:
        return self.song_name

    # Artist Name
    def set_artist_name(self, artist_name):
        self.artist_name = artist_name
        
    def get_artist_name(self) -> str:
        return self.artist_name
    
    def set_top_artists(self, top_artists):
        self.top_artists = top_artists
        
    def get_top_artists(self):
        return self.top_artists

    # Explicit
    def set_explicit_song(self, explicit_song):
        self.explicit_song = explicit_song
        
    def get_explicit_song(self) -> bool:
        return self.explicit_song
    
    # Progress / Duration
    def set_song_progress(self, song_progress):
        self.song_progress = song_progress
        
    def get_song_progress(self):
        """Returns the progress of the current song

        Returns:
            int: Integer value of how far through the song the user is, in Seconds
        """
        return self.song_progress
    
    def set_song_duration(self, song_duration):
        self.song_duration = song_duration
        
    def get_song_duration(self):
        """Returns the duration of the song being listened to

        Returns:
            int: Integer value of the length of the current song, in Seconds
        """
        return self.song_duration
    


class SpotipyAPI:
    """
    This Class is an interface for the Spotify API
    """

    def __init__(self):
        # Loads the enviroment variables
        load_dotenv(dotenv_path="~/SpotiPi")

        self.client_id = os.getenv("CLIENT_ID")
        self.client_secret = os.getenv("CLIENT_SECRET")
        self.SPOTIFY_REDIRECT_URI = "http://localhost:8080"

        self.scope = "user-read-currently-playing", "user-top-read"


    def get_spotify_data(self):
        """
        Makes an API call and gets the spotify date

        Returns:
            String: Returns the json response from the call
        """

        spotify_data = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=self.client_id,
                                                                 client_secret=self.client_secret,
                                                                 redirect_uri=self.SPOTIFY_REDIRECT_URI,
                                                                 scope=self.scope,
                                                                 open_browser=True))

        #return spotify_data.current_user_playing_track()
        return spotify_data


    def get_currently_playing(self):
        """
        Calls the Spotify API and returns the 

        Returns:
            tuple: Returns an array of values depending on the result of the API call
                spotify_status: The status of Spotify -> playing, paused, stopped
                id: The id of the song currently playing
                song_name: The name of the song currently playing
                artist_name: The name of the songs artist(s)
                explicit: A boolean value showing if a song is explicit or not
                progress: How far through the song the user is (in miliseconds)
                duration: How long the song is (in miliseconds)
        """
        spotify_data = self.get_spotify_data()
        spotify_data = spotify_data.current_user_playing_track()

        if (type(spotify_data) is dict):
            # Get song name
            song_name = spotify_data['item']['name']

            if (spotify_data['is_playing']):
                status = "playing"

            else:
                status = "paused"

            # Get the artist(s)
            artist_name = ""

            for i in spotify_data['item']['artists']:
                artist_name += i['name'] + ", "

            return status, spotify_data['item']['id'], song_name, artist_name[:len(artist_name) - 2], spotify_data['item']['explicit'], spotify_data['progress_ms'], spotify_data['item']['duration_ms']

        else:

            return "stopped", "Paused", "------------"


    def get_top_artists(self):
        """
        Gets the users top artists.

        Returns:
            list: A list of the users top artists
        """
        
        spotify_data = self.get_spotify_data()

        #top_artists = spotify_data.current_user_top_artists(limit=10, offset=0, time_range='medium_term')['items']
        top_artists = spotify_data.current_user_top_artists(limit=10, offset=0, time_range='medium_term')['items']
        
        top_artists_list = []
        for i in range(len(top_artists)):
            top_artists_list.append(top_artists[i]['name'])

        return top_artists_list


    def is_playing(self):
        if (type(self.get_spotify_data()) is dict):
            return True
        else:
            return False