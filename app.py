from flask import Flask, abort, redirect, render_template, request, session, jsonify, url_for
from dotenv import load_dotenv
from flask_bcrypt import Bcrypt
import os

from repositories import profile_repository, job_repository

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
        work = profile_repository.get_all_workplace_experience_by_profile(profileId)
        print(profile)
        print(sessionProfile)
        print(work)
        return render_template('user_profile.html', sessionProfile=sessionProfile, profile=profile, work=work)
    elif profileType == 'company':
        profile = profile_repository.get_company_profile_by_id(profileId)
    else:
        abort(400)

@app.route('/editProfile', methods=['POST'])
def editProfile():
    if request.method == 'POST':
        data = request.json
        print(request)
        editProfileID = data.get('profile_id')
        sessionProfile = None
        if 'sessionProfile' in session:
            sessionProfile = session['sessionProfile']
            session['next'] = request.url
        else:
            session['next'] = request.url
        if sessionProfile['profile_id'] == editProfileID:
            editProfileData = profile_repository.get_user_profile_by_id(editProfileID)
            work = profile_repository.get_all_workplace_experience_by_profile(editProfileID)
            sectors = ["Information Technology", "Sales", "Marketing", "Construction", "Manufacturing", "Healthcare", "First Responder"]
            htmlData=render_template("user_profile_edit.html", profile=editProfileData, sessionProfile=sessionProfile, work=work, sectors=sectors)
            return jsonify({'message':'extras added succesfully', 'html':htmlData, 'url':'editProfile'})
        else:
            return jsonify({'message':'edit authentication failed'})

@app.route('/updateProfile', methods=['POST'])
def updateProfile():
    if request.method == 'POST':
        user_id = request.form.get('profile_id')
        firstname = None
        lastname = None
        user_bio = None
        user_profile = None
        user_banner = None
        if 'firstname' in request.form:
            firstname = request.form.get('firstname')
            profile_repository.update_profile_firstname(user_id, firstname)
        if 'lastname' in request.form:
            lastname = request.form.get('lastname')
            profile_repository.update_profile_firstname(user_id, lastname)
        if 'profile_bio' in request.form:
            user_bio = request.form.get('profile_bio')
            profile_repository.update_profile_bio('user', user_id, user_bio)
        if 'profile_picture' in request.files:
            newProfile = request.files['profile_picture']
            user_profile, link = findFileName(newProfile)
            newProfile.save(user_profile)
            profile_repository.update_profile_image('user', user_id, link)
        if 'profile_banner' in request.files:
            newBanner = request.files['profile_banner']
            user_banner, link = findFileName(newBanner)
            newBanner.save(user_banner)
            profile_repository.update_profile_banner('user', user_id, link)
        return jsonify({"message":"profile successfully updated!", "redirect":"/profile?profileType=user&id=" + user_id})

def findFileName(file):
    filename = file.filename.rsplit('.', 1)[0]
    fileType = file.filename.rsplit('.', 1)[1]
    filename = filename[:-1]
    if "png" == fileType or "PNG" == fileType:
        filetype = ".png" 
    if "jpg" == fileType or "JPG" == fileType:
        filetype = ".jpg"
    extension = 'static/img/users/'
    savePath = extension + filename + filetype
    i = 0
    if (os.path.exists(savePath)):
        while os.path.exists(savePath):
            savePath = extension + filename + "_" + str(i) + filetype
            i+=1
        print(savePath)
        accessPath = savePath[7:]
        print(accessPath)
        return savePath, accessPath
    else:
        print(savePath)
        accessPath = savePath[7:]
        print(accessPath)
        return savePath, accessPath

@app.route('/addWorkExperience', methods=['POST'])
def addWork():
    if request.method == 'POST':
        data = request.json
        profileID = data.get('profile_id')
        print(profileID)
        new_work_id = profile_repository.create_new_workplace_experience(profileID)
        if new_work_id is not None:
            sectors = ["Information Technology", "Sales", "Marketing", "Construction", "Manufacturing", "Healthcare", "First Responder"]
            return jsonify({'message':'new work experience id created','workExpID':new_work_id, 'sectors':sectors})
        else:
            return jsonify({'message':'failed to create new workplace ID'})

@app.route('/updateWorkExperience', methods=['POST'])
def updateWork():
    if request.method == 'POST':
        data = request.json
        print(data)
        exp_id = data['work_experience_id']
        if exp_id is None:
            return jsonify({'message':'Failed to update work experience, missing id', 'response':'failure-id'})
        title = data['job_title']
        print(title)
        if title is '':
            return jsonify({'message':'Failed to update work experience, missing title', 'response':'failure-title'})
        cmpy_name = data['company_name']
        if cmpy_name is '':
            return jsonify({'message':'Failed to update work experience, missing company name', 'response':'failure-name'})
        sector = data['job_sector']
        start_date = data['start_date']
        if start_date is '':
            return jsonify({'message':'Failed to update work experience, missing start-date', 'response':'failure-date'})
        end_date = data['end_date']
        if end_date is '':
            end_date = "Present"
        description = data['description']
        water_cooler = data['waterCooler']
        if water_cooler == "true":
            water_cooler = True
        else:
            water_cooler = False
        status = profile_repository.update_work_experience_by_id(exp_id, title, cmpy_name, sector, start_date, end_date, description, water_cooler)
        print(status)
        if status == 1:
            return jsonify({'message':'Updated work experience successfully!', 'response':'success'})
        elif status == -1:
            return jsonify({'message':'Failed to update work experience, missing title', 'response':'failure-title'})
        elif status == -2:
            return jsonify({'message':'Failed to update work experience, missing id', 'response':'failure-id'})

@app.route('/deleteWorkExperience', methods=['POST'])
def deleteWork():
    if request.method == 'POST':
        data=request.json
        exp_id = data['work_experience_id']
        if exp_id is None:
            return jsonify({'message':'Failed to delete work experience, missing id', 'response':'failure-id'})
        status = profile_repository.delete_work_experience_by_id(exp_id)
        if status == 1:
            return jsonify({'message':'Successfully deleted work experience', 'response':'success'})
@app.post('/signupUser')
def signupUser():
    print('none')

@app.get('/job_search.html')
def job_search():
    posting_id = request.args.get('posting_id')
    all_jobs = job_repository.get_job_posting_for_table(posting_id)
    if not all_jobs:
        all_jobs = []
    return render_template('job_search.html', job_posting=all_jobs)


@app.get('/job_listing.html')
def job_listing():
    return render_template('job_listing.html')