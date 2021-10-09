from tensorflow.keras.models import load_model
import tensorflow_similarity as tfsim

from tensorflow_similarity.utils import tf_cap_memory
from tensorflow_similarity.layers import MetricEmbedding # row wise L2 norm
from tensorflow_similarity.losses import MultiSimilarityLoss  # specialized similarity loss
from tensorflow_similarity.models import SimilarityModel # TF model with additional features
from tensorflow_similarity.samplers import MultiShotMemorySampler  # sample data 
from tensorflow_similarity.samplers import select_examples  # select n example per class
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import tensorflow as tf
import numpy as np 
import pandas as pd
import requests
import uvicorn
from Ktizo_Spotify_backend import Get_artist
import joblib
from tensorflow.keras.optimizers import Adam
import uuid
from sklearn.preprocessing import MinMaxScaler


print('TensorFlow:', tf.__version__)
print('TensorFlow Similarity', tfsim.__version__)
distance = 'cosine' 
loss = MultiSimilarityLoss(distance=distance)

lr = 0.00001  #@param {type:"number"}
path = "Closest_Artist/"
scaler_path = "Closest_Artist/Data_transformer.save"
model = load_model(filepath=path, custom_objects={'loss': loss})
model.load_index(path)
#model.compile(optimizer=Adam(lr), loss=loss)
model.index_summary()
data_transformer = MinMaxScaler()
raw_data = pd.read_csv('Verified_artists.csv')
raw_data.drop(columns=['identity','Song_Name'], inplace=True)
data_transformer.fit(raw_data)
#data_transformer = joblib.load(scaler_path)
app = FastAPI()

Verified_artists = ['Ariana Grande'
    ,'Beyonce'
    ,'Bruno Mars'
    ,'Bryson Tiller'
    ,'Childish Gambino'
    ,'Chris Brown'
    ,'Ciara'
    ,'Daniel Caesar'
    ,'Doja Cat'
    ,'Drake'
    ,'Ella Mai'
    ,'Frank Ocean'
    ,'H.E.R.'
    ,'Janelle Monae'
    ,'Jhene Aiko'
    ,'Jorja Smith'
    ,'Kehlani'
    ,'Khalid'
    ,'Miguel'
    ,'Partynextdoor'
    ,'Rihanna'
    ,'Solange'
    ,'Summer Walker'
    ,'SZA'
    ,'Teyana Taylor'
    ,'The Weeknd'
    ,'Tory Lanez'
    ,'Ty Dolla Sign'
    ,'Usher']
artist_num = dict(zip(list(range(len(Verified_artists))),Verified_artists))
Classes = [0,  1,  2,  3,  4,  5,  6,  7,  8,  9, 10, 11, 12, 13, 14, 15, 16,
                17, 18, 19, 20, 22, 23, 21, 24, 25, 26, 27, 28]

def get_features(artist_name):
    data = Get_artist(artist=artist_name)
    Y_test = [5]* len(data)
    song_names = data['Song_Name']
    x_test = data.drop(columns=['identity','Song_Name'],inplace=False)
    x_test['Unnamed: 0'] = 0
    col_order = ['Unnamed: 0','danceability', 'energy', 'key', 'loudness', 'mode', 'speechiness',
       'acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo',
       'duration_ms', 'time_signature', 'track.num_samples', 'track.duration',
       'track.offset_seconds', 'track.window_seconds',
       'track.analysis_sample_rate', 'track.analysis_channels',
       'track.end_of_fade_in', 'track.start_of_fade_out', 'track.loudness',
       'track.tempo', 'track.tempo_confidence', 'track.time_signature',
       'track.time_signature_confidence', 'track.key', 'track.key_confidence',
       'track.mode', 'track.mode_confidence']
    x_test = x_test[col_order]
    x_test = data_transformer.transform(x_test)
    x_display, y_display = select_examples(x_test, Y_test, Classes)
    return x_display, song_names
    
def predict(x_display, song_names):
    num_neighboors = 5
    nns = model.lookup(x_display, k=num_neighboors)
    nns_mapped = {}
    for idx, x in enumerate(nns):
        nns_mapped[song_names[idx]] =  {"Percentage_Match" :1-x[0].distance,"Predicted_Artist": artist_num[x[0].label]}
    return nns_mapped


@app.post("/predict")
async def get_prediction(data):
    features, songs = get_features(artist_name=data)
    return predict(features, songs)


@app.get("/")
async def root():
    return {"message": "Hello World"}

if __name__== "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000)