from flask import Flask, abort, redirect, render_template, request, session
from dotenv import load_dotenv
from flask_bcrypt import Bcrypt

from repositories import profile_repository

load_dotenv()

app = Flask(__name__)

bcrypt = Bcrypt(app)

app.secret_key = b'd8585dc38f97d4df573395d28ec223123af2fc139ec8183a0d1c2954ef7f2b51'

@app.route('/')
@app.route('/index')
def index():
    name = None
    user = None
    if 'user' in session:
        user = session['user']
        name = session['firstname']
        session['next'] = request.url
    else:
        session['next'] = request.url
    return render_template('index.html', user=user, name=name)


# Login & Account Creation
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get("username")
        print(username)
        password = request.form.get("password")
        print(password)
        account_record = profile_repository.get_user_by_login(username)
        print(account_record)
        if account_record is not None:
            if not bcrypt.check_password_hash(account_record['hashed_password'], password):
                return redirect('/login')
            
            session['user'] = username
            session['firstname'] = account_record['firstname']
            session['password'] = password
            if session['next'] is not None:
                return redirect(session['next'])
            else:
                return index()
        else:
            return render_template("login.html", account_not_exists="TRUE")
    else:
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
            # <TODO> add more validation later through python or js, give user feedback if duplicate login, id, etc.
            hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
            profile_repository.create_new_user_profile(user_id, user_email, hashed_password, firstname, lastname)
            return redirect('/login')
        elif profileType == 'company':
            company_id = request.form.get('companyID')
            company_login = request.form.get('companyLogin')
            password = request.form.get('password')
            company_name = request.form.get('companyName')
            # <TODO> add more validation later through python or js, give user feedback if duplicate login, id, etc.
            hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
            profile_repository.create_new_company_profile(company_id, company_login, hashed_password, company_name)
            return redirect('/login')
        else:
            return redirect('/signup')
    else:
        return render_template('signup.html')

@app.route('/logout', methods=['GET'])
def logout():
    redirect_link = None
    if session['next'] is not None:
        redirect_link = session['next']

    session.clear()
    if redirect_link is not None:
        return redirect(redirect_link)
    else:
        return redirect('/')
    
@app.post('/signupUser')
def signupUser():
    print('none')
