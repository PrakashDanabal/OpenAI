
from google.cloud.sql.connector import Connector
import sqlalchemy
from sqlalchemy import Column, Float, Integer, String, Table

INSTANCE_CONNECTION_NAME='adding-and-q-281-4dad58e7:us-central1:flaskdb'
print(f"Your instance connection name is: {'adding-and-q-281-4dad58e7:us-central1:flaskdb'}")
DB_USER = "sqlserver"
# verify password for 'sqlserver' user is set (already set for those that created a Cloud SQL instance within this notebook)
try:
  assert sqlserver_pass
except:
  sqlserver_pass = input("Please provide the password for your 'sqlserver' database user: ")
DB_PASS = '10231993'
DB_NAME = "mdata"



connector = Connector()

# function to return the database connection object
def getconn():
    conn = connector.connect(
        INSTANCE_CONNECTION_NAME,
        "pytds",
        user=DB_USER,
        password=DB_PASS,
        db=DB_NAME
    )
    return conn

# create connection pool with 'creator' argument to our connection object function
pool = sqlalchemy.create_engine(
    "mssql+pytds://",
    creator=getconn,
)


inspector = sqlalchemy.inspect(pool)
if not inspector.has_table("ratings"):
    metadata = sqlalchemy.MetaData()
    Table(
        "ratings",
        metadata,
        Column("id", Integer, primary_key=True, nullable=False),
        Column("name", String(255), nullable=False),
        Column("origin", String(255), nullable=False),
        Column("rating", Float, nullable=False),
    )
    metadata.create_all(pool)

# connect to connection pool
with pool.connect() as db_conn:
  # insert data into our ratings table
  insert_stmt = sqlalchemy.text(
      "INSERT INTO ratings (name, origin, rating) VALUES (:name, :origin, :rating)",
  )

  # insert entries into table
  db_conn.execute(insert_stmt, parameters={"name": "HOTDOG", "origin": "Germany", "rating": 7.5})
  db_conn.execute(insert_stmt, parameters={"name": "BÀNH MÌ", "origin": "Vietnam", "rating": 9.1})
  db_conn.execute(insert_stmt, parameters={"name": "CROQUE MADAME", "origin": "France", "rating": 8.3})

  # commit transaction (SQLAlchemy v2.X.X is commit as you go)
  db_conn.commit()

  # query and fetch ratings table
  results = db_conn.execute(sqlalchemy.text("SELECT * FROM ratings")).fetchall()

  # show results
  for row in results:
    print(row)
