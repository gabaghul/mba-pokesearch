
from flask import Flask
import pytesseract as ocr
import numpy as np
# import cv2
import pandas as pd
import requests
from flask import request
import pytesseract as ocr
import json
from PIL import Image
import urllib.request
from io import BytesIO
from flask_cors import CORS, cross_origin


app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
csv_path = 'csv/pokemon.csv'

api_poketcg_root = 'https://api.pokemontcg.io/v2/cards'
api_pokeapi_root = 'https://pokeapi.co/api/v2/pokemon'
x_api_key = '40616fa2-07af-49f7-aa06-3f87e21f50bf'

def _build_cors_preflight_response():
    response = make_response()
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add('Access-Control-Allow-Headers', "*")
    response.headers.add('Access-Control-Allow-Methods', "*")
    return response

def _corsify_actual_response(response):
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

@app.route('/', methods=['GET'])
@cross_origin()
def hello():
    return f'<a href="https://www.youtube.com/watch?v=dQw4w9WgXcQ">How i did this</a>'

@app.route('/search')
def search():
    if request.method == "POST":
        csv = pd.read_csv(csv_path)
        pokenames = csv.Name

        img_input = request.get_json().get('img')

        urllib.request.urlretrieve(img_input, "poke.png")
        img = Image.open("poke.png")

        extractedInformation = ocr.image_to_string(img, config='--psm 12')

        pokename, api_pokeapi_path, parsed = "","",""

        response = "couldnt find pokemon"

        for name in pokenames:
            if name in extractedInformation:
                pokename = name.lower()
                break
        if len(pokename) > 0:
            api_pokeapi_path=f'{api_pokeapi_root}/{pokename}'
            payload={}
            headers = {'X-Api-Key':x_api_key}

            response = requests.request("GET", api_pokeapi_path, headers=headers, data=payload)

            parsed = json.loads(response.text)
            # types = todos['types']
            # status = todos['stats']
            poketypes = []
            stats = []
            for poketype in parsed['types']:
                poketypes.append(poketype['type']['name'])

            for stat in parsed['stats']:
                stats.append({
                    "name": stat['stat']['name'],
                    "value": stat['base_stat']
                })
            response = {
                "name": pokename,
                "types" : poketypes,
                "stats" : stats
            }
        return response
    elif request.method == "OPTIONS":
        return _build_cors_preflight_response()
    else:
        raise RuntimeError("IM DUMB, I DONT KNOW HOW TO HANDLE THIS METHOD")