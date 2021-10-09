import requests 
import streamlit as st
import json
import pandas as pd
from model import Verified_artists
released_music = st.expander(label="Select Artist with Released Music")
sidebar =st.sidebar
with sidebar:
    sidebar.subheader('Verified Artists')
    for x in Verified_artists:
        sidebar.write(x)
with released_music:
    released_music.subheader("Closest artist to me")
    Artist = st.text_area('Enter Artist here', value='Wale')
    start  = st.button("Find my Comparison")
    if start:
        with st.spinner('Finding Comparison'):
            res = requests.post(f"http://127.0.0.1:8000/predict?data={Artist}")
            predictions = res.json()
            released_music.write(predictions)
        released_music.success("Here's some Comprable artists")
Unreleased_music = st.expander(label='Upload Unreleased Music')
with Unreleased_music:
    Unreleased_music.write('WORK IN PROGRESS')
    Unreleased_music.subheader('Lets preprocess your unreleased song')
    file  =st.file_uploader('Select MP3')
    
    