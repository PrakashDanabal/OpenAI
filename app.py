from flask import Flask
from flask_sqlalchemy import SQLAlchemy
# import main
from google.cloud.sql.connector import Connector, IPTypes
import pytds
import sqlalchemy


app=Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqldb://<db_user>:<db_password>@/<db_name>?unix_socket=/cloudsql/<connection_name>'

def connect_with_connector() -> sqlalchemy.engine.base.Engine:

    connector = Connector(IPTypes.PUBLIC)

    connect_args = {}

    def getconn() -> pytds.Connection:
        conn = connector.connect(
            'myflashdb',
            "pytds",
            user='sqlserver',
            password= '10231993',
            db='flaskTest',
        )
        return conn

    pool = sqlalchemy.create_engine(
        "mssql+pytds://",
        creator=getconn,
        # ...
    )
    return pool



@app.route('/')
def index():
    # data=main.get_reviews('https://www.amazon.in/product-reviews/B077BFH786/&reviewerType=all_reviews/ref=cm_cr_arp_d_viewpnt_rgt?filterByStar=critical&pageNumber=1')
    data='hello world'
    return str(data)


if __name__=='__main__':
    app.run(debug=False)
