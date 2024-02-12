from flask import Flask, render_template_string, render_template, jsonify
from flask import render_template
from flask import json
from datetime import datetime
from urllib.request import urlopen
import sqlite3
                                                                                                                                       
app = Flask(__name__)     

@app.route('/commits/')
def commits():
    # Configuration pour GitHub API
    conn = http.client.HTTPSConnection("api.github.com")
    headers = { 'User-Agent': 'MyApp' }

    # Remplacez '<your-username>' et '<your-repo>' par vos informations
    conn.request("GET", "/repos/<corinamoussou>/<5MCSI_Metriques>/commits", headers=headers)

    response = conn.getresponse()
    raw_data = response.read()
    commits_data = json.loads(raw_data.decode("utf-8"))

    # Préparer les données pour l'histogramme
    commit_counts = {}
    for commit in commits_data:
        commit_date = datetime.strptime(commit['commit']['author']['date'], '%Y-%m-%dT%H:%M:%SZ')
        minute = commit_date.strftime('%Y-%m-%d %H:%M')
        commit_counts[minute] = commit_counts.get(minute, 0) + 1

    # Convertir les données en format compatible avec Google Charts
    data_for_chart = [['Minute', 'Nombre de Commits']]
    for minute, count in sorted(commit_counts.items()):
        data_for_chart.append([minute, count])

    # Vous devez créer un template HTML pour afficher les données
    return render_template('commits_histogram.html', data_for_chart=data_for_chart)

@app.route("/histogramme/")
def mongraphique2():
    return render_template("histogramme.html")

@app.route("/rapport/")
def mongraphique():
    return render_template("graphique.html")

@app.route('/paris/')
def meteo():
    response = urlopen('https://samples.openweathermap.org/data/2.5/forecast?lat=0&lon=0&appid=xxx')
    raw_content = response.read()
    json_content = json.loads(raw_content.decode('utf-8'))
    results = []
    for list_element in json_content.get('list', []):
        dt_value = list_element.get('dt')
        temp_day_value = list_element.get('main', {}).get('temp') - 273.15 # Conversion de Kelvin en °c 
        results.append({'Jour': dt_value, 'temp': temp_day_value})
    return jsonify(results=results)

@app.route("/contact/")
def MaPremiereAPI():
    return render_template("formulaire.html")
                                                                                                                                       
@app.route('/')
def hello_world():
    return render_template('hello.html') #comm4
  
if __name__ == "__main__":
  app.run(debug=True)
