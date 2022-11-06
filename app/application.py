import os
import flask, flask_login
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_socketio import SocketIO
from configparser import ConfigParser

SOCKETIO = SocketIO()

login_manager = flask_login.LoginManager()
login_manager.session_protection = "strong"             #strong, basic, None
db = SQLAlchemy()
bcrypt = Bcrypt()
config = ConfigParser()
config.read('app/config.cfg')

basedir = os.path.abspath(os.path.dirname(__file__))

def create_app():
    app = flask.Flask(__name__)
    secret_key = config.get('flask_socketio', 'SECRET_KEY')
    app.secret_key = secret_key

    from app.main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    
    secret_key = config.get('SQLAlchemy', 'SECRET_KEY')
    app.secret_key = secret_key
    app.config['SQLALCHEMY_DATABASE_URI'] =\
       'sqlite:///' + os.path.join(basedir,'main', 'database.db')
    login_manager.init_app(app)
    db.init_app(app)
    bcrypt.init_app(app)


    SOCKETIO.init_app(app)
    return app