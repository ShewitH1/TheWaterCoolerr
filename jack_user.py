# #user.py

# from flask_login import UserMixin

# # user model class
# # super class UserMixin implements the methods required by flask-login
# # i.e. is_authenticated(), is_active(), is_anonymous(), get_id()
# class User(UserMixin):
#     def __init__(self, profile_id, username, email, password, first_name, last_name, profile_image, profile_banner, profile_bio, workplace_experience, education):
#         super().__init__()
#         self.profile_id = profile_id
#         self.username = username
#         self.email = email
#         self.password = password
#         self.first_name = first_name
#         self.last_name = last_name
#         self.profile_image = profile_image
#         self.profile_banner = profile_banner
#         self.profile_bio = profile_bio
#         self.workplace_experience = workplace_experience
#         self.education = education

#     # Getters
#     def get_profile_id(self):
#         return self.profile_id

#     def get_username(self):
#         return self.username

#     def get_email(self):
#         return self.email

#     def get_password(self):
#         return self.password

#     def get_first_name(self):
#         return self.first_name

#     def get_last_name(self):
#         return self.last_name

#     def get_profile_image(self):
#         return self.profile_image

#     def get_profile_banner(self):
#         return self.profile_banner

#     def get_profile_bio(self):
#         return self.profile_bio

#     def get_workplace_experience(self):
#         return self.workplace_experience

#     def get_education(self):
#         return self.education

#     # Setters
#     def set_profile_id(self, profile_id):
#         self.profile_id = profile_id

#     def set_username(self, username):
#         self.username = username

#     def set_email(self, email):
#         self.email = email

#     def set_password(self, password):
#         self.password = password

#     def set_first_name(self, first_name):
#         self.first_name = first_name

#     def set_last_name(self, last_name):
#         self.last_name = last_name

#     def set_profile_image(self, profile_image):
#         self.profile_image = profile_image

#     def set_profile_banner(self, profile_banner):
#         self.profile_banner = profile_banner

#     def set_profile_bio(self, profile_bio):
#         self.profile_bio = profile_bio

#     def set_workplace_experience(self, workplace_experience):
#         self.workplace_experience = workplace_experience

#     def set_education(self, education):
#         self.education = education