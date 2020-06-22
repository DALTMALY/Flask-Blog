#Import Flask for server
from flask import Flask
#import ORM of SQLAlchemy for sqlite database
from flask_sqlalchemy import SQLAlchemy
#Bcrypt is for encrypt passwords
from flask_bcrypt import Bcrypt
#flask_login provides user session management for Flask LoginManager is an instantiating the flask login extension
from flask_login import LoginManager
#The Flask-Mail extension provides a simple interface to set up SMTP with your Flask application and to send messages from your views and scripts
#Emails are managed through a Mail instance
from flask_mail import Mail
#from flaskblog folder, select "config.py" module, within that file sekect "Config" class
from flaskblog.config import Config

#Instancing Objects and save in a variable
db = SQLAlchemy()
bcrypt = Bcrypt()
#The most important part of an application that uses Flask-Login is the LoginManager class. You should create one for your application somewhere in your code, like this:
login_manager = LoginManager()
#"login_view" The name of the view to redirect to when the user needs to log in. (This can be an absolute URL as well, if your authentication machinery is external to your application.)
#"users" folder within it "login" function. The name of the log in view can be set as "LoginManager.login_view". 
login_manager.login_view = 'users.login'
#To customize the message category, set LoginManager.login_message_category:
login_manager.login_message_category = 'info'
#Emails are managed through a Mail instance
mail = Mail()

#We create a fuction that contains "Mail settings" parameters , That will receive as parameter the Class called "Config" inside "Config.py"
def create_app(config_class = Config):
    #__name__ is just a convenient way to get the import name of the place the app is defined. Flask uses the import name to know where to look up resources, templates, static files, instance folder, etc.
    #When using a package, if you define your app in __init__.py then the __name__ will still point at the "correct" place relative to where the resources are
    app = Flask(__name__)
    #To enable such a config you just have to call into from_object():
    app.config.from_object(Config)

    #to create the object once and configure the application. Object calls "create_app()":
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    #Importing functions inside different modules
    from flaskblog.users.routes import users
    from flaskblog.posts.routes import posts
    from flaskblog.main.routes import main
    from flaskblog.errors.handlers import errors
    
    #A Blueprint object works similarly to a Flask application object, but it is not actually an application. Rather it is a blueprint of how to construct or extend an application
    #So how do you register that blueprint? Like this:
    app.register_blueprint(users)
    app.register_blueprint(posts)
    app.register_blueprint(main)
    app.register_blueprint(errors)

    #Lauch server
    return app