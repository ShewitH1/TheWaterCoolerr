from flask import Flask, abort, redirect, render_template, request, session, jsonify
from dotenv import load_dotenv
from flask_bcrypt import Bcrypt

from repositories import profile_repository, job_repository, application_repository

load_dotenv()

app = Flask(__name__)

bcrypt = Bcrypt(app)

app.secret_key = b'd8585dc38f97d4df573395d28ec223123af2fc139ec8183a0d1c2954ef7f2b51'

@app.route('/')
def index():
    # Session & Page Variable Tracking
    sessionProfile = None
    if 'sessionProfile' in session:
        sessionProfile = session['sessionProfile']
        session['next'] = request.url
    else:
        session['next'] = request.url

    return render_template('index.html', sessionProfile=sessionProfile)


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
            
            session['sessionProfile'] = profile_repository.get_user_by_login(username)
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
        print(request.form)
        payload_tag = request.form.get('payload_tag')
        if payload_tag == 'basic':
            if request.form.get('profile_type') == 'user':
                user_id = request.form.get('profile_id')
                user_email = request.form.get('email')
                password = request.form.get('pass')
                firstname = request.form.get('firstname')
                lastname = request.form.get('lastname')
                hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
                profile_repository.create_new_user_profile(user_id, user_email, hashed_password, firstname, lastname)
                return jsonify({'message':'new user profile created successfully', 'user_id':user_id});
            elif payload_tag == 'company':
                company_id = request.form.get('company_id')
                company_login = request.form.get('login')
                password = request.form.get('pass')
                company_name = request.form.get('company_name')
                hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
                profile_repository.create_new_company_profile(company_id, company_login, hashed_password, company_name)
                return jsonify({'message':'new user profile created successfully', 'company_id':company_id});
            else:
                return jsonify({'message':'failed to create new profile'})
        elif request.form.get('payload_tag') == 'extra':
            if request.form.get('profileType') == 'user':
                user_id = request.form.get('id')
                user_bio = None
                user_profile = None
                user_banner = None
                if 'profile_bio' in request.form:
                    user_bio = request.form.get('profile_bio')
                    profile_repository.update_profile_bio('user', user_id, user_bio)
                if 'profile_picture' in request.files:
                    newProfile = request.files['profile_picture']
                    user_profile = 'static/img/users/' + newProfile.filename
                    newProfile.save(user_profile)
                    profile_repository.update_profile_image('user', user_id, user_profile)
                if 'profile_banner' in request.files:
                    newBanner = request.files['profile_banner']
                    user_banner = 'static/img/users/' + newBanner.filename
                    newBanner.save(user_banner)
                    profile_repository.update_profile_banner('user', user_id, user_banner)
            elif request.form.get('profileType') == 'company':
                company_id = request.form.get('id')
                company_bio = None
                company_profile = None
                company_banner = None
                if 'profile_bio' in request.form:
                    user_bio = request.form.get('profile_bio')
                    profile_repository.update_profile_bio('user', company_id, company_bio)
                if 'profile_picture' in request.files:
                    newProfile = request.files['profile_picture']
                    user_profile = 'static/img/companies/' + newProfile.filename
                    newProfile.save(user_profile)
                    profile_repository.update_profile_image('user', company_id, company_profile)
                if 'profile_banner' in request.files:
                    newBanner = request.files['profile_banner']
                    user_banner = 'static/img/companies/' + newBanner.filename
                    newBanner.save(user_banner)
                    profile_repository.update_profile_banner('user', company_id, company_banner)
            return jsonify({'message':'extras added succesfully', 'redirect':'/login'})
        else:
            print('failed')
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

@app.route('/profile', methods=['GET'])
def profile():

    # Session & Page Variable Tracking
    sessionProfile = None
    if 'sessionProfile' in session:
        sessionProfile = session['sessionProfile']
        session['next'] = request.url
    else:
        session['next'] = request.url

    profileType = request.args.get('profileType')
    print(profileType)
    profileId = request.args.get('id')
    print(profileId)
    if profileType == 'user':
        profile = profile_repository.get_user_profile_by_id(profileId)
        print(profile)
        return render_template('user_profile.html', sessionProfile=sessionProfile, profile=profile)
    elif profileType == 'company':
        profile = profile_repository.get_company_profile_by_id(profileId)
    else:
        abort(400)
@app.post('/signupUser')
def signupUser():
    print('none')

# Posts the jobs to the job posting page
@app.get('/job_search.html')
def job_search():
    job_title = request.args.get('job_title')
    posting_date = request.args.get('posting_date')
    description = request.args.get('description')
    salary = request.args.get('salary')
    company_id = request.args.get('company_id')
    job_postings = job_repository.search_job_posting(job_title, posting_date, description, salary, company_id)
    if job_postings is False:
        job_postings = []
    return render_template('job_search.html', job_postings=job_postings)

# Creates a new job posting
@app.post('/create_job_posting')
def create_job_posting_route():
    job_title = request.form.get('job_title')
    posting_date = request.form.get('posting_date')
    description = request.form.get('description')
    salary = request.form.get('salary')
    company_id = request.form.get('company_id')
    job_id = job_repository.create_job_posting(job_title, posting_date, description, salary, company_id)
    if job_id is False:
        abort(500, description="Error creating job posting")
    return redirect(url_for('job_listing'))

# Updates a job posting
@app.post('/update_job_posting')
def update_job_posting_route():
    posting_id = request.form.get('posting_id')
    job_title = request.form.get('job_title')
    posting_date = request.form.get('posting_date')
    description = request.form.get('description')
    salary = request.form.get('salary')
    company_id = request.form.get('company_id')
    success = job_repository.update_job_posting(posting_id, job_title, posting_date, description, salary, company_id)
    if not success:
        abort(500, description="Error updating job posting")
    return redirect(url_for('job_listing'))

# Deletes a job posting
@app.post('/delete_job_posting')
def delete_job_posting_route():
    posting_id = request.form.get('posting_id')
    success = job_repository.delete_job_posting(posting_id)
    if not success:
        abort(500, description="Error deleting job posting")
    return redirect(url_for('job_listing'))

# Searches for job postings
@app.get('/search_job_posting')
def search_job_posting_route():
    job_title = request.args.get('job_title')
    posting_date = request.args.get('posting_date')
    description = request.args.get('description')
    salary = request.args.get('salary')
    company_id = request.args.get('company_id')
    job_postings = job_repository.search_job_posting(job_title, posting_date, description, salary, company_id)
    if job_postings is False:
        abort(500, description="Error searching job postings")
    return render_template('job_search.html', job_postings=job_postings)

@app.get('/job_listing.html')
def job_listing():
    return render_template('job_listing.html')