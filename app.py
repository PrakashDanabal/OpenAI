from flask import Flask
from flask_sqlalchemy import SQLAlchemy
# import main
from google.cloud.sql.connector import Connector, IPTypes
import pytds
import sqlalchemy


# db = SQLAlchemy()

# SQLALCHEMY_DATABASE_URI = "mssql://sadmin:10231993@adding-and-q-281-3662a64f:us-central1:flaskdb/mdata?driver=SQL+Server+Native+Client+11.0" # File-based SQL database


# class User(db.Model, UserMixin):
#     __tablename__ = 'ehind_users'
#     id = db.Column(db.Integer, primary_key=True)
#     active = db.Column('is_active', db.Boolean(), nullable=False, server_default='1')
#     email = db.Column(db.String(100), nullable=False, unique=True)
#     email_confirmed_at = db.Column(db.DateTime())
#     password = db.Column(db.String(500), nullable=False, server_default='')
#     # User information
#     username = db.Column(db.String(20), unique=True)
#     Fullname = db.Column(db.String(100), nullable=False, server_default='')
#     SAP_reference = db.Column(db.String(100))
#     # Define the relationship to Role via UserRoles
#     phone_number = db.Column(db.String(45))
#     plant_id = db.Column(db.String(4))
#
#
app=Flask(__name__)

# def connect_unix_socket() -> sqlalchemy.engine.base.Engine:
#     """Initializes a Unix socket connection pool for a Cloud SQL instance of MySQL."""
#     # Note: Saving credentials in environment variables is convenient, but not
#     # secure - consider a more secure solution such as
#     # Cloud Secret Manager (https://cloud.google.com/secret-manager) to help
#     # keep secrets safe.
#     db_user = 'sadmin'  # e.g. 'my-database-user'
#     db_pass = '10231993'  # e.g. 'my-database-password'
#     db_name = 'mdata'  # e.g. 'my-database'
#     unix_socket_path = 'adding-and-q-281-3662a64f:us-central1:flaskdb'  # e.g. '/cloudsql/project:region:instance'
#
#     pool = sqlalchemy.create_engine(
#         # Equivalent URL:
#         # mysql+pymysql://<db_user>:<db_pass>@/<db_name>?unix_socket=<socket_path>/<cloud_sql_instance_name>
#         sqlalchemy.engine.url.URL.create(
#             drivername="mysql+pymysql",
#             username=db_user,
#             password=db_pass,
#             database=db_name,
#             query={"unix_socket": unix_socket_path},
#         ),
#         # ...
#     )
#     return pool


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
    if os.environ.get("DB_ROOT_CERT"):  # e.g. '/path/to/my/server-ca.pem'
        connect_args = {
            "cafile": os.environ["DB_ROOT_CERT"],
            "validate_host": False,
        }

    def getconn() -> pytds.Connection:
        conn = connector.connect(
            instance_connection_name,
            "pytds",
            user=db_user,
            password=db_pass,
            db=db_name,
            **connect_args
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
