import pandas as pd
import numpy as np
import spotipy
import json
from spotipy.oauth2 import SpotifyClientCredentials

client_id = 'd7989c7227bd4d06b83f94e9d55b1597'#; // Your client id
client_secret = '5e5b3c3c46f240cea016773789d0b73e'#; // Your secret
oath = 'BQBXA0YYt2LN2ecdTbkLGpBNU7ZuUJsfykzbYmWyhC994y0UnzLBSzy3DA6wasm5OIt_K0UvzpqXTJ0C04vbtN3VtZ9dOsdduP1SowucpjqsV_CVY3lq3F8MuQz9XfVzR7dzIsko0MSUHhYOw_OaRXDG95DUKQ0_bpo'


client_credentials_manager = SpotifyClientCredentials(client_id=client_id,client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
sp.trace = False


def grab_artist_tracks(artist_name):
    results = sp.search(q=artist_name, limit=50)
    tids = []
    songs = []
    for i, t in enumerate(results['tracks']['items']):
        #print(' ', i, t['name'])
        songs.append(t['name'])
        tids.append(t['uri'])
    return tids,songs

def get_features(tids, identity):
    columns = ['danceability','energy','key','loudness','mode','speechiness','acousticness',
          'instrumentalness', 'liveness','valence','tempo','duration_ms','time_signature'
          ,'track.num_samples','track.duration', 'track.offset_seconds',
           'track.window_seconds',
          'track.analysis_sample_rate', 'track.analysis_channels', "track.end_of_fade_in",
    "track.start_of_fade_out","track.loudness",   "track.tempo",  
           "track.tempo_confidence",   "track.time_signature",
           "track.time_signature_confidence",  "track.key",  "track.key_confidence",  "track.mode", 
           "track.mode_confidence" ]
    analysis = {}
    features = sp.audio_features(tids)
    analysis = [sp.audio_analysis(tid) for tid in tids]
    output_features = pd.json_normalize(features)
    output_analysis = pd.json_normalize(analysis)
    output_df = pd.concat([output_features,output_analysis], axis=1)
    columns += ['identity']
    output_df['identity'] = identity
    return output_df[columns]


def Get_artist(artist):
    Comps_tracks, artist_song_names__ = grab_artist_tracks(artist)
    g = get_features(tids=Comps_tracks, identity=artist)
    g['Song_Name'] = artist_song_names__
    return g

