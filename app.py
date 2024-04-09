from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.get('/templates/job_search.html')
def job_search():
    return render_template('job_search.html')

@app.get('/templates/job_listing.html')
def job_listing():
    return render_template('job_listing.html')

@app.get('/templates/landing.html')
def landing():
    return render_template('landing.html')