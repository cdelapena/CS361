from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap

app = Flask(__name__)
Bootstrap(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/result', methods=['GET', 'POST'])
def result():
    return render_template('result.html', startingcity = request.form['starting-city'], 
    destinationcity = request.form['destination-city'],
    priority = request.form['gridRadios'])

if __name__ == '__main__' :
    app.run(debug=True)