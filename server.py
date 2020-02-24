from flask import Flask, render_template, request, session, redirect, url_for
import secrets
import requests

app = Flask(__name__)
app.secret_key = str(secrets.randbits(64))

url = 'https://pokeapi.co/api/v2/pokemon/'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/pokemon', methods=['POST']) 
def pokemon_search():
    pokemon = request.form['pokemon']
    new_url = url + pokemon.lower()
    data = requests.get(str(new_url))

    if data.status_code != 200:
        return redirect('/showerror')

    session['pokemon'] = pokemon.capitalize()
    session['front_image'] = data.json()['sprites']['front_default']
    session['height'] = data.json()['height']
    session['weight'] = data.json()['weight']
    session['abilities'] = [i['ability']['name'] for i in data.json()['abilities']]
    session['pokemon_id'] = data.json()['id']

    return redirect("/show")

@app.route('/show')
def show():
    return render_template('pokemon.html')
    
@app.route('/showerror')
def show_error():
    return render_template('error.html')
    
if __name__ == "__main__":
    app.run(debug=True)