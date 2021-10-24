from bs4.element import SoupStrainer
import requests
import urllib
import shutil
from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap
from bs4 import BeautifulSoup
from urllib.request import urlopen, Request, urlretrieve

app = Flask(__name__)
Bootstrap(app)

def get_distance(startingcity, destinationcity):
    url = f'https://www.distance24.org/route.json?stops={startingcity}|{destinationcity}'
    response = requests.get(url).json()
    return response

def get_soup(airplane):
    url = f'https://www.airlines-inform.com/commercial-aircraft/{airplane}.html'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    return soup

def get_picture(soup, i):
    picture = soup.find(class_="setWOfMe")
    src = picture['src']
    r = requests.get(src)
    img_name = "img" + str(i) + ".jpg"
    # MUST place images in static folder. Don't use /static. Use "static" to prevent absolute/relative path issue
    with open("static/images/" + img_name, 'wb') as f:
        f.write(r.content)

    return src

def get_range(soup):
    string = soup.find("td", text="Range with max payload (km)")
    next_string = string.find_next("td")
    range = next_string.text.strip()
    # must reassign to self or spaces remain
    range = range.replace(' ', '')
    range = int(range)
    return range

def get_seats(soup):
    string = soup.find("td", text="Passengers (2-class)")
    if string is None:
        string = soup.find("td", text="Passengers (1-class)")
    if string is None:
        string = soup.find("td", text="Passengers (3-class)")
    next_string = string.find_next("td")
    seats = next_string.text.strip()
    return seats

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
    airplane_names = {"name" : ['airbus-a380', 'bombardier-cs100', 'bombardier-cs300', 'embraer-e195-e2']}
    #, 'airbus-a321neo', 'airbus-a330-300', , 'boeing-737-max-10', 'boeing-787-10', 
    #    'bombardier-cs100', 'bombardier-cs300', 'embraer-e195-e2']}

    # build dictionary of dictionaries using scraper
    airplane_details = {}
    for i in range(0, len(airplane_names["name"])): 
        # Create dictionary or will get keyerror0
        airplane_details[i] = {}
        airplane_details[i]["name"] = airplane_names["name"][i]
        soup = get_soup(airplane_names["name"][i])
        airplane_details[i]["picture"] = get_picture(soup, i) 
        airplane_details[i]["range"] = get_range(soup)
        airplane_details[i]["seats"] = get_seats(soup)

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