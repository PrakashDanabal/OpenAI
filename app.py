from flask import Flask
from flask_sqlalchemy import SQLAlchemy
# import main
from google.cloud.sql.connector import Connector, IPTypes
import pytds
import sqlalchemy as db

class User(db.Model, UserMixin):
    __tablename__ = 'ehind_users'
    id = db.Column(db.Integer, primary_key=True)
    active = db.Column('is_active', db.Boolean(), nullable=False, server_default='1')
    email = db.Column(db.String(100), nullable=False, unique=True)
    email_confirmed_at = db.Column(db.DateTime())
    password = db.Column(db.String(500), nullable=False, server_default='')
    # User information
    username = db.Column(db.String(20), unique=True)
    Fullname = db.Column(db.String(100), nullable=False, server_default='')
    SAP_reference = db.Column(db.String(100))
    # Define the relationship to Role via UserRoles
    phone_number = db.Column(db.String(45))
    plant_id = db.Column(db.String(4))


app=Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqldb://<db_user>:<db_password>@/<db_name>?unix_socket=/cloudsql/<connection_name>'
# Copyright 2022 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


def connect_with_connector() -> sqlalchemy.engine.base.Engine:
    """
    Initializes a connection pool for a Cloud SQL instance of SQL Server.

    Uses the Cloud SQL Python Connector package.
    """
    # Note: Saving credentials in environment variables is convenient, but not
    # secure - consider a more secure solution such as
    # Cloud Secret Manager (https://cloud.google.com/secret-manager) to help
    # keep secrets safe.

    instance_connection_name = 'adding-and-q-281-20299c19:us-central1:flasktable'
    db_user = 'sqlserver'
    db_pass = '10231993'  # e.g. 'my-db-password'
    db_name = 'gitsql'  # e.g. 'my-database'

    ip_type = IPTypes.PUBLIC

    connector = Connector(ip_type)

    connect_args = {}
    # If your SQL Server instance requires SSL, you need to download the CA
    # certificate for your instance and include cafile={path to downloaded
    # certificate} and validate_host=False. This is a workaround for a known issue.
    # if os.environ.get("DB_ROOT_CERT"):  # e.g. '/path/to/my/server-ca.pem'
    #     connect_args = {
    #         "cafile": os.environ["DB_ROOT_CERT"],
    #         "validate_host": False,
    #     }

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
        # [START_EXCLUDE]
        # Pool size is the maximum number of permanent connections to keep.
        pool_size=5,
        # Temporarily exceeds the set pool_size if no connections are available.
        max_overflow=2,
        # The total number of concurrent connections for your application will be
        # a total of pool_size and max_overflow.
        # 'pool_timeout' is the maximum number of seconds to wait when retrieving a
        # new connection from the pool. After the specified amount of time, an
        # exception will be thrown.
        pool_timeout=30,  # 30 seconds
        # 'pool_recycle' is the maximum number of seconds a connection can persist.
        # Connections that live longer than the specified amount of time will be
        # re-established
        pool_recycle=1800,  # 30 minutes
        # [END_EXCLUDE]
    )
    return pool


# [END cloud_sql_sqlserver_sqlalchemy_connect_connector]

print(connect_with_connector())



@app.route('/')
def index():
    # data=main.get_reviews('https://www.amazon.in/product-reviews/B077BFH786/&reviewerType=all_reviews/ref=cm_cr_arp_d_viewpnt_rgt?filterByStar=critical&pageNumber=1')
    data='hello world'
    return str(data)


if __name__=='__main__':
    app.run(debug=False)
