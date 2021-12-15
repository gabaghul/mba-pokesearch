
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


app = Flask(__name__)
csv_path = 'csv/pokemon.csv'

api_poketcg_root = 'https://api.pokemontcg.io/v2/cards'
api_pokeapi_root = 'https://pokeapi.co/api/v2/pokemon'
x_api_key = '40616fa2-07af-49f7-aa06-3f87e21f50bf'

@app.route('/', methods=['GET'])
def hello():
    return f'<a href="https://www.youtube.com/watch?v=dQw4w9WgXcQ">How i did this</a>'

@app.route('/search', methods=['POST'])
def search():
    csv = pd.read_csv(csv_path)
    pokenames = csv.Name

    img_input = request.get_json().get('img')

    urllib.request.urlretrieve(img_input, "poke.png")
    img = Image.open("poke.png")

    extractedInformation = ocr.image_to_string(img, config='--psm 12')

    pokename, api_pokeapi_path, parsed = "","",""

    for name in pokenames:
        if name in extractedInformation:
            pokename = name.lower()
            break
    if len(pokename) > 0:
        api_pokeapi_path=f'{api_pokeapi_root}/{pokename}'
        print(api_pokeapi_path)
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