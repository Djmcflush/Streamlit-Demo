# Streamlit-Demo
This Demo App is a user interface to access our ongoing Apis;

All the models served in the demo are production ready and have been wrapped in FastAPI's to allow
RestFul access to them


Tutorial:
Clone the repository 
0. Add your own Spotify Dev client_id, client_secret, oath in a file called client.py as variables
1. pip install -r reequirements
2. uvicorn model:app --reload
3. streamlit run main.py
4. Open Streamlit in your local Broswer (http://localhost:8501/)

Test out the FastAPI using http://127.0.0.1:8000/docs

Or Access the application via :
weblink
