from flask import Flask
from flask_sqlalchemy import SQLAlchemy
# import main
from google.cloud.sql.connector import Connector, IPTypes
import pytds
import sqlalchemy




app=Flask(__name__)

def connect_with_connector() -> sqlalchemy.engine.base.Engine:
    """
    Initializes a connection pool for a Cloud SQL instance of SQL Server.

    Uses the Cloud SQL Python Connector package.
    """
    # Note: Saving credentials in environment variables is convenient, but not
    # secure - consider a more secure solution such as
    # Cloud Secret Manager (https://cloud.google.com/secret-manager) to help
    # keep secrets safe.

    instance_connection_name = 'adding-and-q-281-3662a64f:us-central1:flaskdb'  # e.g. 'project:region:instance'
    db_user = 'sadmin'  # e.g. 'my-db-user'
    db_pass = '10231993'  # e.g. 'my-db-password'
    db_name = 'mdata'  # e.g. 'my-database'

    ip_type = IPTypes.PUBLIC

    connector = Connector(ip_type)

    connect_args = {}
    # If your SQL Server instance requires SSL, you need to download the CA
    # certificate for your instance and include cafile={path to downloaded
    # certificate} and validate_host=False. This is a workaround for a known issue.

    def getconn() -> pytds.Connection:
        conn = connector.connect(
            instance_connection_name,
            "pytds",
            user=db_user,
            password=db_pass,
            db=db_name
        )
        return conn

    pool = sqlalchemy.create_engine(
        "mssql+pytds://",
        creator=getconn,
        # ...
    )
    return pool

# db_user = 'sadmin'
# db_password = '10231993'
# db_name = 'mdata'
# db_socket_dir = '/cloudsql'
# cloud_sql_connection_name = 'adding-and-q-281-3662a64f:us-central1:flaskdb'
#
# # Configure the SQLAlchemy URI for Google Cloud SQL
# db_uri = f"mssql://{db_user}:{db_password}@/{db_name}?unix_socket=/cloudsql/{cloud_sql_connection_name}"
# app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#
# # db = SQLAlchemy(app)
# db = connect_unix_socket()

db=connect_with_connector()
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)

db.create_all()

if not User.query.first():
    sample_user = User(username='Sample User')
    db.session.add(sample_user)
    db.session.commit()





@app.route('/')
def index():
    # data=main.get_reviews('https://www.amazon.in/product-reviews/B077BFH786/&reviewerType=all_reviews/ref=cm_cr_arp_d_viewpnt_rgt?filterByStar=critical&pageNumber=1')
    user = User.query.first()

    if user:
        username = user.username
    else:
        username = 'No user found'

    return username


if __name__=='__main__':
    app.run(debug=False)
