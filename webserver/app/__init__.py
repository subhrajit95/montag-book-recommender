from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

# local imports
from config import app_config

# db variable initialization
db = SQLAlchemy()

login_manager = LoginManager()

def create_app(config_name):
	app = Flask(__name__, instance_relative_config=True)
	app.config.from_object(app_config[config_name])
	app.config.from_pyfile("config.py")
	app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://admin:pyth0nic@localhost/montag"
	app.secret_key = 'super secret key'

	with app.app_context():
		db.init_app(app)

	migrate = Migrate(app, db)

	login_manager.init_app(app)
	login_manager.login_view = "home.showSignin"

	from app import models

	@login_manager.user_loader
	def load_user(user_id):
		return models.User.query.filter(models.User.id == int(user_id)).first()

	from .home import home as home_blueprint
	app.register_blueprint(home_blueprint)

	return app
