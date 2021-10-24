import requests
from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap
from bs4 import BeautifulSoup
from urllib.request import urlopen, Request, urlretrieve
import urllib

app = Flask(__name__)
Bootstrap(app)

def get_distance(startingcity, destinationcity):
    url = f'https://www.distance24.org/route.json?stops={startingcity}|{destinationcity}'
    response = requests.get(url).json()
    return response

def scrape_plane(airplane):
    url = f'https://www.airlines-inform.com/commercial-aircraft/{airplane}.html'
    response = requests.get(url)

    soup = BeautifulSoup(response.content, 'html.parser')

    picture = soup.find(class_="setWOfMe")
 
    return picture['src']

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/reset', methods=['GET'])
def reset():
    return render_template('index.html')

@app.route('/result', methods=['GET', 'POST'])
def result():
    startingcity = request.form['starting-city']
    destinationcity = request.form['destination-city']
    priority = request.form['gridRadios']
    airplane_names = {"name" : ['airbus-a320neo', 'airbus-a321neo', 'airbus-a330-300', 'boeing-737-max-10', 'boeing-787-10', 
        'bombardier-cs100', 'bombardier-cs300', 'embraer-e195-e2']}

    # build dictionary of dictionaries using scraper
    airplane_details = {}
    for i in range(0, len(airplane_names["name"])): 
        # Create dictionary or will get keyerror0
        airplane_details[i] = {}
        airplane_details[i]["name"] = airplane_names["name"][i]
        airplane_details[i]["picture"] = scrape_plane(airplane_names["name"][i])

    distance = get_distance(startingcity, destinationcity)
    km = distance["distance"]
    miles = int(km * 0.621371)

    # check min range
    # check if same city

    return render_template('result.html', distance=distance, miles=miles, startingcity=startingcity, 
    destinationcity=destinationcity, priority=priority, airplane_details=airplane_details)
    #vars = render_template('result.html', startingcity = request.form['starting-city'], 
    #destinationcity = request.form['destination-city'],
    #priority = request.form['gridRadios'])

    #return vars

if __name__ == '__main__' :
    app.run(debug=True)