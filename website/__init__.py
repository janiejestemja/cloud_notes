from os import path

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()
DB_NAME = "database.db"

def create_app():
    # Initialize flask
    app = Flask(__name__)

    # Encryption of Cookie and Seesion Data
    app.config["SECRET_KEY"] = "secret_key"

    # Configuration of Database
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DB_NAME}"
    db.init_app(app)

    # Registering Blueprints
    from .views import views
    from .auth import auth
    from .imagefiles import imagefiles
    from .textfiles import textfiles

    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")
    app.register_blueprint(imagefiles, url_prefix="/")
    app.register_blueprint(textfiles, url_prefix="/")

    # Loading models for database tables
    from .models import User, Note
    # Creation of database if it does not exist
    if not path.exists("instance/" + DB_NAME):
        with app.app_context():
            db.create_all()
        print("Database created.")

    # Manage not logged in users
    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    # Return the app
    return app
