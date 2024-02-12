from flask import Flask, render_template_string, render_template, jsonify
from flask import render_template
from flask import json
from datetime import datetime
from urllib.request import urlopen
import sqlite3
                                                                                                                                       
app = Flask(__name__)     

@app.route('/commits/')
def show_commits():
    response = requests.get('https://api.github.com/repos/OpenRSI/5MCSI_Metriques/commits')
    commits_data = response.json()
    
    # Extraire les minutes des timestamps de commit
    commits_per_minute = {}
    for commit in commits_data:
        commit_date_str = commit['commit']['author']['date']
        commit_date = datetime.strptime(commit_date_str, '%Y-%m-%dT%H:%M:%SZ')
        minute = commit_date.strftime('%Y-%m-%d %H:%M')
        if minute in commits_per_minute:
            commits_per_minute[minute] += 1
        else:
            commits_per_minute[minute] = 1
    
    # Préparer les données pour le graphique
    data_for_chart = [['Minute', 'Commits']]
    for minute, count in commits_per_minute.items():
        data_for_chart.append([minute, count])
    
    return render_template('graphique_commits.html', data_for_chart=data_for_chart)

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
