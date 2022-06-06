from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    from app.routes import bp
    app.register_blueprint(bp)

    app.config['SQLALCHEMY_DATABASE_URI'] = 'mariadb+mariadbconnector://kumohcheck:checkuser@192.168.50.87:3307/kumohcheck'
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    with app.app_context():
        db.app = app
        db.init_app(app)
        
    return app