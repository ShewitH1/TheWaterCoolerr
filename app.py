from flask import Flask, abort, redirect, render_template, request, session, jsonify, url_for
from dotenv import load_dotenv
from flask_bcrypt import Bcrypt
from datetime import datetime, date
import re
import os

from repositories import profile_repository, job_repository, application_repository
from datetime import datetime

load_dotenv()

app = Flask(__name__)

bcrypt = Bcrypt(app)

app.secret_key = b'd8585dc38f97d4df573395d28ec223123af2fc139ec8183a0d1c2954ef7f2b51'

def get_session_profile():
    sessionProfile = None
    if 'sessionProfile' in session:
        sessionProfile = session['sessionProfile']
        session['next'] = request.url
    else:
        session['next'] = request.url
    return sessionProfile

@app.route('/')
def index():
    # Session & Page Variable Tracking
    sessionProfile = None
    if 'sessionProfile' in session:
        sessionProfile = session['sessionProfile']
        sessionType = session.get('type')
        session['next'] = request.url
    else:
        session['next'] = request.url

    return render_template('index.html', sessionProfile=sessionProfile)


# user login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get("username")
        #print(username)
        password = request.form.get("password")
        #print(password)
        user_record = profile_repository.get_user_by_login(username)
        if user_record is not None:
            if not bcrypt.check_password_hash(user_record['hashed_password'], password):
                return redirect('/login')
            session['sessionProfile'] = profile_repository.get_user_by_login(username)
            session['type'] = 'user'  # Set session type here
            if session['next'] is not None:
                return redirect(session['next'])
            else:
                return index()
        company_record = profile_repository.get_company_by_login(username)
        if company_record is not None:
            if not bcrypt.check_password_hash(company_record['hashed_password'], password):
                return redirect('/login')
            session['sessionProfile'] = profile_repository.get_company_profile_by_id(company_record['company_id'])
            #print(session['sessionProfile'])
            session['type'] = 'company'
            if session['next'] is not None:
                return redirect(session['next'])
            else:
                return index()
        else:
            return render_template("login.html", account_not_exists="TRUE")
    else:
        return render_template('login.html')

# user/company signup
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
                create_status = profile_repository.create_new_user_profile(user_id, user_email, hashed_password, firstname, lastname)
                return jsonify({'message':'new user profile created successfully', 'user_id':user_id});
            elif request.form.get('profile_type') == 'company':
                company_id = request.form.get('company_id')
                company_login = request.form.get('login')
                password = request.form.get('pass')
                company_name = request.form.get('company_name')
                hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
                create_status = profile_repository.create_new_company_profile(company_id, company_login, hashed_password, company_name)
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
                    user_profile, link = findUserFileName(newProfile)
                    newProfile.save(user_profile)
                    profile_repository.update_profile_image('user', user_id, link)
                if 'profile_banner' in request.files:
                    newBanner = request.files['profile_banner']
                    user_banner, link = findUserFileName(newBanner)
                    newBanner.save(user_banner)
                    profile_repository.update_profile_banner('user', user_id, link)
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
                    user_profile, link = findCompanyFileName(newProfile)
                    newProfile.save(user_profile)
                    profile_repository.update_profile_image('user', company_id, link)
                if 'profile_banner' in request.files:
                    newBanner = request.files['profile_banner']
                    user_banner, link = findCompanyFileName(newBanner)
                    newBanner.save(user_banner)
                    profile_repository.update_profile_banner('user', company_id, link)
            return jsonify({'message':'extras added succesfully', 'redirect':'/login'})
        else:
            print('failed')
    else:
        return render_template('signup.html')

#user logout
@app.route('/logout', methods=['GET'])
def logout():
    next_url = session.get('next', '/')
    session.clear()
    return redirect(next_url)

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
    #print(profileType)
    profileId = request.args.get('id')
    #print(profileId)
    if profileType == 'user':
        profile = profile_repository.get_user_profile_by_id(profileId)
        work = profile_repository.get_all_workplace_experience_by_profile(profileId)
        education = profile_repository.get_all_education_experience_by_profile(profileId)
        return render_template('user_profile.html', sessionProfile=sessionProfile, profile=profile, work=work, education=education)
    elif profileType == 'company':
        profile = profile_repository.get_company_profile_by_id(profileId)
        #print(profile)
        return render_template('company_profile.html', sessionProfile=sessionProfile, profile=profile)
    else:
        abort(400)

@app.route('/editProfile', methods=['POST'])
def editProfile():
    if request.method == 'POST':
        data = request.json
        editProfileID = data.get('profile_id')
        type = data.get('type')
        sessionProfile = None
        if 'sessionProfile' in session:
            sessionProfile = session['sessionProfile']
            session['next'] = request.url
        else:
            session['next'] = request.url
        if type == 'user':
            if sessionProfile['profile_id'] == editProfileID:
                editProfileData = profile_repository.get_user_profile_by_id(editProfileID)
                work = profile_repository.get_all_workplace_experience_by_profile(editProfileID)
                education = profile_repository.get_all_education_experience_by_profile(editProfileID)
                sectors = ["Information Technology", "Sales", "Marketing", "Construction", "Manufacturing", "Healthcare", "First Responder"]
                levels = ["Certification", "GED", "Bachelors", "Masters", "PhD"]
                htmlData=render_template("user_profile_edit.html", profile=editProfileData, sessionProfile=sessionProfile, work=work, education=education, sectors=sectors, levels=levels)
                return jsonify({'message':'extras added succesfully', 'html':htmlData, 'url':'editProfile'})
            else:
                return jsonify({'message':'edit authentication failed'})
        elif type == 'company':
            if sessionProfile['company_id'] == editProfileID:
                editProfileData = profile_repository.get_company_profile_by_id(editProfileID)
                htmlData=render_template("company_profile_edit.html", profile=editProfileData, sessionProfile=sessionProfile)
                return jsonify({'message':'extras added succesfully', 'html':htmlData, 'url':'editProfile'})
            else:
                return jsonify({'message':'edit authentication failed'})

@app.route('/updateProfile', methods=['POST'])
def updateProfile():
    if request.method == 'POST':
        user_id = request.form.get('profile_id')
        type = request.form.get('type')
        if type == 'user':
            record = profile_repository.get_user_profile_by_id(user_id)
            if record is None:
                return jsonify({"message":"Profile update failed, invalid ID"})
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
                profile_repository.update_profile_lastname(user_id, lastname)
            if 'profile_bio' in request.form:
                user_bio = request.form.get('profile_bio')
                profile_repository.update_profile_bio('user', user_id, user_bio)
            if 'profile_picture' in request.files:
                newProfile = request.files['profile_picture']
                user_profile, link = findUserFileName(newProfile)
                old_profile_picture = 'static/' + record['profile_image']
                if 'static/img/users/' in old_profile_picture:
                    if os.path.exists(old_profile_picture):
                        os.remove(old_profile_picture)
                newProfile.save(user_profile)
                profile_repository.update_profile_image(type, user_id, link)
            if 'profile_banner' in request.files:
                newBanner = request.files['profile_banner']
                user_banner, link = findUserFileName(newBanner)
                old_banner = 'static/' + record['profile_banner']
                if 'static/img/users/' in old_banner:
                    if os.path.exists(old_banner):
                        os.remove(old_banner)
                newBanner.save(user_banner)
                profile_repository.update_profile_banner(type, user_id, link)
            return jsonify({"message":"profile successfully updated!", "redirect":"/profile?profileType=user&id=" + user_id})
        elif type == 'company':
            record = profile_repository.get_company_profile_by_id(user_id)
            if 'name' in request.form:
                newName = request.form.get('name')
                status = profile_repository.update_company_name(user_id, newName)
                if status == -4:
                    return jsonify({'message':'Failed to update company name, missing id', 'response':'failure-id'})
                elif status == -3:
                    return jsonify({'message':'Failed to update company name, missing name', 'response':'failure-name'})
                elif status == -2:
                    return jsonify({'message':'Failed to update company name, company id does not exist', 'response':'failure-id-exist'})
                elif status == -1:
                    return jsonify({'message':'Failed to update company name, database error', 'response':'failure-data'})
            if 'company_bio' in request.form:
                newBio = request.form.get('company_bio')
                status = profile_repository.update_profile_bio(type, user_id, newBio)
                if status == -4:
                    return jsonify({'message':'Failed to update company bio, missing id', 'response':'failure-id'})
                elif status == -3:
                    return jsonify({'message':'Failed to update company bio, missing profile type', 'response':'failure-type'})
                elif status == -2:
                    return jsonify({'message':'Failed to update company bio, missing bio', 'response':'failure-bio'})
                elif status == -5:
                    return jsonify({'message':'Failed to update company bio, invalid profile type', 'response':'failure-type-invalid'})
                elif status == -6:
                    return jsonify({'message':'Failed to update company bio, company id does not exist', 'response':'failure-id-exists'})
            if 'company_image' in request.files:
                newImage = request.files['company_image']
                company_image, link = findCompanyFileName(newImage)
                old_profile_picture = 'static/' + record['company_image']
                if 'static/img/company/' in old_profile_picture:
                    if os.path.exists(old_profile_picture):
                        os.remove(old_profile_picture)
                newImage.save(company_image)
                profile_repository.update_profile_image(type, user_id, link)
            if 'company_banner' in request.files:
                newBanner = request.files['company_banner']
                company_banner, link = findCompanyFileName(newBanner)
                old_banner_picture = 'static/' + record['company_banner']
                if 'static/img/company/' in old_banner_picture:
                    if os.path.exists(old_banner_picture):
                        os.remove(old_banner_picture)
                newBanner.save(company_banner)
                profile_repository.update_profile_banner(type, user_id, link)
            if 'about_img_1' in request.files:
                newAboutIMG1 = request.files['about_img_1']
                about_image_1, link = findCompanyFileName(newAboutIMG1)
                old_record = record['about_img_1']
                if old_record is not None:
                    old_about_image_1 = 'static/' + record['about_img_1']
                    if 'static/img/company/' in old_about_image_1:
                        if os.path.exists(old_about_image_1):
                            os.remove(old_about_image_1)
                newAboutIMG1.save(about_image_1)
                profile_repository.update_about_img(user_id, link, id=0)
            if 'about_img_2' in request.files:
                newAboutIMG2 = request.files['about_img_2']
                about_image_2, link = findCompanyFileName(newAboutIMG2)
                old_record = record['about_img_2']
                if old_record is not None:
                    old_about_image_2 = 'static/' + record['about_img_1']
                    if 'static/img/company/' in old_about_image_2:
                        if os.path.exists(old_about_image_2):
                            os.remove(old_about_image_2)
                newAboutIMG2.save(about_image_2)
                profile_repository.update_about_img(user_id, link, id=1)
            if 'about_img_3' in request.files:
                newAboutIMG3 = request.files['about_img_3']
                about_image_3, link = findCompanyFileName(newAboutIMG3)
                old_record = record['about_img_3']
                if old_record is not None:
                    old_about_image_3 = 'static/' + record['about_img_1']
                    if 'static/img/company/' in old_about_image_3:
                        if os.path.exists(old_about_image_3):
                            os.remove(old_about_image_3)
                newAboutIMG3.save(about_image_3)
                profile_repository.update_about_img(user_id, link, id=2)
            return jsonify({"message":"profile successfully updated!", "redirect":"/profile?profileType=company&id=" + user_id})
        else:
            return jsonify({"message":"failure to update profile, invalid type."})

def findUserFileName(file):
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
        accessPath = savePath[7:]
        return savePath, accessPath
    else:
        accessPath = savePath[7:]
        return savePath, accessPath

def findCompanyFileName(file):
    filename = file.filename.rsplit('.', 1)[0]
    fileType = file.filename.rsplit('.', 1)[1]
    filename = filename[:-1]
    if "png" == fileType or "PNG" == fileType:
        filetype = ".png" 
    if "jpg" == fileType or "JPG" == fileType:
        filetype = ".jpg"
    extension = 'static/img/company/'
    savePath = extension + filename + filetype
    i = 0
    if (os.path.exists(savePath)):
        while os.path.exists(savePath):
            savePath = extension + filename + "_" + str(i) + filetype
            i+=1
        accessPath = savePath[7:]
        return savePath, accessPath
    else:
        accessPath = savePath[7:]
        return savePath, accessPath

@app.route('/addWorkExperience', methods=['POST'])
def addWork():
    if request.method == 'POST':
        data = request.json
        profileID = data.get('profile_id')
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
        exp_id = data['work_experience_id']
        if exp_id is None:
            return jsonify({'message':'Failed to update work experience, missing id', 'response':'failure-id'})
        title = data['job_title']
        if title == '':
            return jsonify({'message':'Failed to update work experience, missing title', 'response':'failure-title'})
        cmpy_name = data['company_name']
        if cmpy_name == '':
            return jsonify({'message':'Failed to update work experience, missing company name', 'response':'failure-name'})
        sector = data['job_sector']
        start_date = data['start_date']
        curr_date = date.today()
        if start_date == '':
            return jsonify({'message':'Failed to update education experience, missing start-date', 'response':'failure-date'})
        else:
            logic_start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
            if logic_start_date > curr_date:
                return jsonify({'message':'Failed to update education exeprience, invalid start-date (start date cannot be greater than current date)', 'response':'failure-greater-date'})
        end_date = data['end_date']
        if end_date == '':
            end_date = "Present"
        else:
            logic_end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
            if logic_end_date > curr_date:
                return jsonify({'message':'Failed to update work experience, invalid end-date (end date cannot be greater than current date)', 'response':'failure-greater-date-end'})
        description = data['description']
        water_cooler = data['waterCooler']
        if water_cooler == "true":
            water_cooler = True
        else:
            water_cooler = False
        status = profile_repository.update_work_experience_by_id(exp_id, title, cmpy_name, sector, start_date, end_date, description, water_cooler)
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
        
@app.route('/addEducationExperience', methods=['POST'])
def addEducation():
    if request.method == 'POST':
        data = request.json
        profileID = data.get('profile_id')
        new_edu_id = profile_repository.create_new_education_experience(profileID)
        if new_edu_id is not None:
            levels = ["Certification", "GED", "Bachelors", "Masters", "PhD"]
            return jsonify({'message':'new education experience id created','eduExpID':new_edu_id, 'levels':levels})
        else:
            return jsonify({'message':'failed to create new education experience id'})

@app.route('/updateEducationExperience', methods=['POST'])
def updateEducation():
    if request.method == 'POST':
        data = request.json
        exp_id = data['education_experience_id']
        if exp_id is None:
            return jsonify({'message':'Failed to update education experience, missing id', 'response':'failure-id'})
        institution = data['institution_name']
        if institution == '':
            return jsonify({'message':'Failed to update education experience, missing institution name', 'response':'failure-inst'})
        level = data['education_level']
        if level == '':
            return jsonify({'message':'Failed to update education experience, missing education level', 'response':'failure-level'})
        area = data['study_area']
        start_date = data['start_date']
        curr_date = date.today()
        if start_date == '':
            return jsonify({'message':'Failed to update education experience, missing start-date', 'response':'failure-date'})
        else:
            logic_date = datetime.strptime(start_date, '%Y-%m-%d').date()
            if logic_date > curr_date:
                return jsonify({'message':'Failed to update education exeprience, invalid start-date (start date cannot be greater than current date)', 'response':'failure-greater-date'})
        end_date = data['end_date']
        if end_date == '':
            end_date = "Present"
        else:
            logic_end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
            if logic_end_date > curr_date:
                return jsonify({'message':'Failed to update education experience, invalid end-date (end date cannot be greater than current date)', 'response':'failure-greater-date-end'})
        status = profile_repository.update_education_experience_by_id(exp_id, institution, level, area, start_date, end_date)
        if status == 1:
            return jsonify({'message':'Updated education experience successfully!', 'response':'success'})
        elif status == -1:
            return jsonify({'message':'Failed to update education experience, missing title', 'response':'failure-title'})
        elif status == -2:
            return jsonify({'message':'Failed to update education experience, missing id', 'response':'failure-id'})

@app.route('/deleteEducationExperience', methods=['POST'])
def deleteEducation():
    if request.method == 'POST':
        data=request.json
        exp_id = data['education_experience_id']
        if exp_id is None:
            return jsonify({'message':'Failed to delete education experience, missing id', 'response':'failure-id'})
        status = profile_repository.delete_education_experience_by_id(exp_id)
        if status == 1:
            return jsonify({'message':'Successfully deleted education experience', 'response':'success'})

# Posts the jobs to the job posting page
@app.get('/job_search.html')
def job_search():
    job_postings = job_repository.get_job_postings()
    print(job_postings)
    if not job_postings:
        job_postings = []
    sessionProfile = get_session_profile()
    return render_template('job_search.html', sessionProfile=sessionProfile, job_postings=job_postings)

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
    job_title = request.args.get('job_title')
    posting_id = request.args.get('posting_id')
    company_id = request.args.get('company_id')
    location = request.args.get('location')
    company = request.args.get('company')
    posting_date = request.args.get('posting_date')
    salary = request.args.get('salary')
    job_description = request.args.get('job_description')
    job_postings = job_repository.indi_job_posting()
    return render_template('job_listing.html', sessionProfile=get_session_profile(), job_posting=job_postings)

@app.get('/list/<int:posting_id>')
def get_joblist(posting_id):
    job = job_repository.get_job_posting_for_table(posting_id)
    return render_template('listing_page.html', list2=job)

@app.route('/company_login', methods=['GET', 'POST'])
def company_login():
    if request.method == 'POST':
        company_login = request.form.get("company_login")
        print(company_login)
        password = request.form.get("password")
        print(password)
        account_record = profile_repository.get_company_by_login(company_login)
        print(account_record)
        if account_record is not None:
            if not bcrypt.check_password_hash(account_record['hashed_password'], password):
                return redirect('/login')
            
            session['sessionProfile'] = profile_repository.get_company_by_login(company_login)
            session['password'] = password
            session['type'] = 'company'  # Set session type here

            if session['next'] is not None:
                return redirect(session['next'])
            else:
                return index()
        else:
            return render_template("login.html", account_not_exists="TRUE")
    else:
        return render_template('login.html')

@app.route('/application_portal')
def application_portal():
    sessionProfile = get_session_profile()
    #print(sessionProfile)
    if sessionProfile is None:
        return redirect('/login')
    if 'company_id' in sessionProfile and sessionProfile['company_id'] is not None:
        print("Current sesh ID: " + sessionProfile['company_id'])
        return render_template('app_dashboard_company.html', sessionProfile=sessionProfile, name=sessionProfile.get('name'), applicants=application_repository.get_applications_for_company(sessionProfile.get('company_id')))
    elif 'profile_id' in sessionProfile and sessionProfile['profile_id'] is not None:
        print("Current sesh ID: " + sessionProfile['profile_id'])
        return render_template('app_dashboard.html', sessionProfile=sessionProfile, name=sessionProfile.get('firstname'), applications=application_repository.get_applications_for_user(sessionProfile.get('profile_id')))

@app.route('/application_portal/<posting_id>/<user_id>')
def application_portal_answers(posting_id, user_id):
    answers = application_repository.get_user_answers_for_posting(user_id, posting_id)
    questions = application_repository.get_questions_for_application(posting_id)
    return render_template('app_dashboard_company.html', sessionProfile=get_session_profile(), answers=answers, questions=questions, posting_id=posting_id, user_id=user_id, users_name=application_repository.get_users_full_name(user_id))

@app.route('/application_portal/<posting_id>/<user_id>/accept')
def application_portal_accept(posting_id, user_id):
    sessionProfile = None
    if 'sessionProfile' in session:
        sessionProfile = session['sessionProfile']
        session['next'] = request.url
    else:
        session['next'] = request.url
    application_repository.set_application_status(posting_id, user_id, 'accepted')
    return redirect('/application_portal')

@app.route('/application_portal/<posting_id>/<user_id>/reject')
def application_portal_reject(posting_id, user_id):
    sessionProfile = get_session_profile()
    application_repository.set_application_status(posting_id, user_id, 'rejected')
    return redirect('/application_portal')

@app.route('/apply/<posting_id>')
def apply(posting_id):
    sessionProfile = get_session_profile()
    # can carry the case of both not logged in AND not having a profile_id (company)
    if (sessionProfile.get('profile_id') == None):
        return redirect('/application_portal')
    questions = application_repository.get_questions_for_application(posting_id)
    return render_template('application.html', questions=questions, posting_id=posting_id, sessionProfile=sessionProfile)

@app.route('/create_application')
def create_application():
    sessionProfile = get_session_profile()
    if sessionProfile == None:
        return redirect('/login')
    return render_template('create_application.html', sessionProfile=sessionProfile)

@app.post('/submit_job_posting')
def submit_job_posting():
    sessionProfile = get_session_profile()
    if sessionProfile == None:
        return redirect('/login')
    title = request.form.get('title')
    description = request.form.get('description')
    salary = request.form.get('salary')
    questions = request.form.getlist('question[]')
    company_id = sessionProfile.get('company_id')
    if (not title or not description or not salary or not questions or not company_id):
        abort(400, description="Missing form data")
    posting_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    posting_id = job_repository.create_job_posting(title, posting_date, description, salary, company_id)
    if application_repository.add_questions_to_posting(posting_id, questions):
        print("Added questions to posting.")
    else:
        print("Failed to add questions to posting.")
    return redirect('/application_portal')

@app.post('/submit_application/<posting_id>')
def submit_application(posting_id):
    sessionProfile = get_session_profile()
    profile_id = sessionProfile.get('profile_id')
    # must be logged in to apply.....
    if not profile_id:
        return redirect('/login')
    answers = {re.search(r'\[(.*?)\]', key).group(1): request.form[key] for key in request.form.keys() if key.startswith('answers')} # regex magic
    # basic form validation
    if not posting_id or not profile_id or not answers:
        abort(400, description="Missing form data")
    success = application_repository.submit_application(profile_id, posting_id, answers)
    if not success:
        abort(500, description="Error submitting application")
    return redirect('/application_portal')
