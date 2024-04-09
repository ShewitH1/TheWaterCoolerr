from flask import Flask, abort, redirect, render_template, request
from dotenv import load_dotenv
from flask_bcrypt import Bcrypt

from repositories import profile_repository

load_dotenv()

app = Flask(__name__)

bcrypt = Bcrypt(app)

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


# Login & Account Creation
@app.route('/login', methods=['GET'])
def login():
    return render_template('login.html')

@app.route('/signup', methods=['GET','POST'])
def signup():
    if request.method == 'POST':
        profileType = request.form.get('profileType')
        if profileType == 'user':
            user_id = request.form.get('profileID')
            user_email = request.form.get('email')
            password = request.form.get('password')
            firstname = request.form.get('firstname')
            lastname = request.form.get('lastname')
        elif profileType == 'company':
            company_id = request.form.get('companyID')
            company_login = request.form.get('companyLogin')
            password = request.form.get('password')
            company_name = request.form.get('companyName')
        else:
            print('none')
    else:
        return render_template('signup.html')

@app.post('/signupUser')
def signupUser():
    print('none')