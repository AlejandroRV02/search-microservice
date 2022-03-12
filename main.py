from http.client import BAD_REQUEST, INTERNAL_SERVER_ERROR
import os
import requests
from flask import Flask, request, jsonify, make_response

app = Flask(__name__)

@app.route('/searchComics')
def searchComics():
    try:
        args = request.args
        search = args.get("search")
        comic = args.get("comic")
        character = args.get("character")
            
        URL = os.environ.get('MARVEL_API_URL')
        API_KEY = os.environ.get('API_KEY')
        HASH = os.environ.get('HASH') 
        characters_endpoint = 'characters'
        comics_endpoint = 'comics'

        valid_req = True if (comic == '0' and character == '1') or (comic == '1' and character == '0') else False
        if not valid_req: 
            return make_response(jsonify({"msg":"Parameter values not valid"}), 400)

        params = {"ts": 1, "apikey": API_KEY, "hash":HASH}
        
        if search != None:
            if character == '1':
                params['name'] = search
                personaje_req = requests.get(f'{URL}{characters_endpoint}', params=params).json()

                if len(personaje_req['data']['results']) == 0:
                    return make_response(jsonify({"personaje": {}, "comics": []}),200)

                personaje = {}
                personaje['id'] = personaje_req['data']['results'][0]['id']
                personaje['name'] = personaje_req['data']['results'][0]['name']
                personaje['appearances'] = personaje_req['data']['results'][0]['comics']['returned']
                personaje['image'] = f"{personaje_req['data']['results'][0]['thumbnail']['path']}"

                comics_url = personaje_req['data']['results'][0]['comics']['collectionURI']
                comics = []
                del params['name']
                comics_req = requests.get(comics_url, params=params).json()

                for comic in comics_req['data']['results']:
                    comic_to_append = {}
                    comic_to_append['id'] = comic['id']
                    comic_to_append['title'] = comic['title']
                    comic_to_append['image'] = f"{comic['thumbnail']['path']}"
                    comic_to_append['onsaleDate'] = comic['dates'][0]['date']

                    comics.append(comic_to_append)
                    
                return make_response(jsonify({"personaje": personaje, "comics": comics}), 200)

            if comic == '1':
                params['title'] = search

                comics_req = requests.get(f'{URL}{comics_endpoint}', params=params).json()

                if len(comics_req['data']['results']) == 0:
                    return make_response(jsonify([]), 200)

                commic_res = {}
                commic_res['id'] = comics_req['data']['results'][0]['id']
                commic_res['title'] = comics_req['data']['results'][0]['title']
                commic_res['image'] = comics_req['data']['results'][0]['thumbnail']['path']
                commic_res['onsaleDate'] = comics_req['data']['results'][0]['dates'][0]['date']

                return make_response(jsonify(commic_res), 200)

        if search == None:
            params['limit'] = 50
            personajes_req = requests.get(f'{URL}{characters_endpoint}', params=params).json()

            personajes = []

            for personaje in personajes_req['data']['results']:
                personaje_to_append = {}
                personaje_to_append['id'] = personaje['id']
                personaje_to_append['name'] = personaje['name']
                personaje_to_append['image'] = personaje['thumbnail']['path']
                personaje_to_append['appearances'] = personaje['comics']['available']

                personajes.append(personaje_to_append)

            return make_response(jsonify(personajes),200)

    except Exception as e:
        return make_response(jsonify({"error": f"An error occured: {e}"}), 500)

@app.errorhandler(404)
def on_not_found(error):
    return make_response(jsonify({"msg":"Resource not found"}), 404)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)