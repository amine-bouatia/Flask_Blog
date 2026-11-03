from importlib.resources import path
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager


db= SQLAlchemy()

def create_app():
    app = Flask(__name__)

    app.config["SECRET_KEY"]= "Admin1234"
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views,url_prefix="/")
    app.register_blueprint(auth,url_prefix="/")

    from .models import User, Post

   
    create_db(app)

 # For Login System Use login Manager
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login_Page'
    login_manager.init_app(app)
   
    @login_manager.user_loader
    def load_user(id):
      return User.query.get(int(id))
   


    return app



def create_db(app):
    if not path.exists("website/database.db"):
        with app.app_context():
            db.create_all()
        print("create db !")
