import requests
from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap

app = Flask(__name__)
Bootstrap(app)

def get_distance(startingcity, destinationcity):
    url = f'https://www.distance24.org/route.json?stops={startingcity}|{destinationcity}'
    response = requests.get(url).json()
    return response

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/result', methods=['GET', 'POST'])
def result():
    startingcity = request.form['starting-city']
    destinationcity = request.form['destination-city']
    priority = request.form['gridRadios']

    distance = get_distance(startingcity, destinationcity)
    km = distance["distance"]
    miles = int(km * 0.621371)

    # check min range
    # check if same city

    return render_template('result.html', distance=distance, miles=miles, startingcity=startingcity, destinationcity=destinationcity, priority=priority)
    #vars = render_template('result.html', startingcity = request.form['starting-city'], 
    #destinationcity = request.form['destination-city'],
    #priority = request.form['gridRadios'])

    #return vars

if __name__ == '__main__' :
    app.run(debug=True)