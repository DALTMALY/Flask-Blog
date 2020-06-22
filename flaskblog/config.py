#This module provides a portable way of using operating system dependent functionality. 
import os
#This class contains all our settings for "Mail" object and some settings of our app
class Config:
    #Using os module with environ variables
    #SECRET_KEY: variable for session of authentication
    SECRET_KEY = os.environ.get('SECRET_KEY')
    #SQLALCHEMY_DATABASE_URI: database address
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
    #settings for Mail, this is for "google emails"
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = '587'
    MAIL_USE_TLS = 'True'
    #Using os module with environ variables
    MAIL_USERNAME = os.environ.get('EMAIL_USER')
    MAIL_PASSWORD = os.environ.get('EMAIL_PASS')