from flask import Blueprint
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from google.cloud.sql.connector import Connector

#there is no hope
### hope it works
db = SQLAlchemy()

INSTANCE_CONNECTION_NAME='adding-and-q-281-800e631e:us-central1:flaskdb'
DB_USER='sqlserver'
DB_PASS='10231993'
DB_NAME='mdata'



def getconn():
    conn = connector.connect(
        INSTANCE_CONNECTION_NAME,
        "pytds",
        user=DB_USER,
        password=DB_PASS,
        db=DB_NAME
    )
    return conn


def create_app():
    app = Flask(__name__)

    # Flask-SQLAlchemy settings
    # app.config['SQLALCHEMY_DATABASE_URI']= "mssql://sa:10231993@localhost:49993/MData_PMO?driver=SQL+Server+Native+Client+11.0"  # File-based SQL database
    app.config['SQLALCHEMY_DATABASE_URI']= getconn()
    # app.config['SQLALCHEMY_BINDS'] = {
    #     'random': "mssql://sqlserver:10231993@localhost:49993/MData_PMO?driver=SQL+Server+Native+Client+11.0"
    # }
    # app.config['SQLALCHEMY_DATABASE_URI']= "mssql://sa:10231993@localhost:49993/MData_PMO?driver=SQL+Server+Native+Client+11.0"  # File-based SQL database
    # app.config['SQLALCHEMY_BINDS'] = {
    #     'random': "mssql://sa:10231993@localhost:49993/MData_PMO?driver=SQL+Server+Native+Client+11.0"
    # }
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Avoids SQLAlchemy warning
    db.init_app(app)
    with app.app_context():
        db.create_all()
    app.register_blueprint(main)
    app.debug = True
    app.run(port=8080)
    return app








class User(db.Model):
    __tablename__ = 'Tracker_Users'
    id = db.Column(db.Integer, primary_key=True)
    active = db.Column('is_active', db.Boolean(), nullable=False, server_default='1')
    email = db.Column(db.String(255), nullable=False, unique=True)
    email_confirmed_at = db.Column(db.DateTime())
    password = db.Column(db.String(128))



main = Blueprint('main', __name__)



@main.route('/')
def signup():

    return 'Completed'


if __name__=="__main__":
    create_app()