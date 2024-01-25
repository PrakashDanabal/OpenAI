from flask import Flask
from flask_sqlalchemy import SQLAlchemy
# import main

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)


app=Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqldb://<db_user>:<db_password>@/<db_name>?unix_socket=/cloudsql/<connection_name>'
app.config['SQLALCHEMY_DATABASE_URI'] = "mssql://sa:10231993@localhost:1433/BTS??unix_socket=/cloudsql/deploying-wo-201-25818191:us-central1:myflaskapp1" # File-based SQL database
db = SQLAlchemy(app)


@app.route('/')
def index():
    # data=main.get_reviews('https://www.amazon.in/product-reviews/B077BFH786/&reviewerType=all_reviews/ref=cm_cr_arp_d_viewpnt_rgt?filterByStar=critical&pageNumber=1')
    data='hello world'
    return str(data)


if __name__=='__main__':
    app.run(debug=False)
