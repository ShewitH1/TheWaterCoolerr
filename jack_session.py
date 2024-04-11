# import flask
# from flask import flash, Flask, Markup, render_template, redirect, request, url_for, UserManager 
# from flask_bootstrap import Bootstrap
# from flask_login import current_user, LoginManager, login_required, login_user, logout_user
# from flask_security import Mail
# import User

# import User

# app = Flask(__name__)
# bootstrap = Bootstrap(app)

# # flask user and login manager class calls 
# login_manager = LoginManager(app)       # handles user session management
# user_manager = UserManager(app, db, User)       # db is assumed database and User is assumed user model class

# #initialize login manager
# login_manager.init_app(app)

# #flask login user loader
# @login_manager.user_loader
# def load_user(user_id):
#     return User.query.get(user_id)  #returns none if user not found

# #flask login
# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     form = LoginForm()      # LoginForm is assumed class
#     if form.validate_on_submit():
#         login_user(User)
#         flask.flash('Logged in successfully.')
#         next = flask.request.args.get('next')
#         return flask.redirect(next or flask.url_for('index'))
#     else:
#         if form.is_submitted():
#             reset_url = url_for('reset_password')  # replace 'reset_password' with the name of your password reset function
#             flask.flash(Markup('Username/Password does not match any on file. <a href="{}">Forgot password?</a>'.format(reset_url)), 'error')
#         return render_template('login.html', form=form)
    
# #flask logout
# @app.get('/logout')
# @login_required
# def logout():
#     logout_user()
#     return redirect(url_for('login'))   # replace 'url_for('login'))' with the name of login page


# @app.get('/')
# @app.get('/index')
# def index():
#     return render_template('index.html')

# if __name__ == '__main__':
#     app.run(debug=True)