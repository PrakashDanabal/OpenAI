# imports
from flask import Flask, request, make_response
from flask_sqlalchemy import SQLAlchemy

# initializing Flask app
app = Flask(__name__)

# Google Cloud SQL (change this accordingly)
PASSWORD = "10231993"
PUBLIC_IP_ADDRESS = "34.42.62.12"
DBNAME = "mdata"
PROJECT_ID = "adding-and-q-281-61174c4e"
INSTANCE_NAME = "adding-and-q-281-61174c4e:us-central1:flaskdb"

# configuration
# app.config["SECRET_KEY"] = "yoursecretkey"


app.config[
    "SQLALCHEMY_DATABASE_URI"] = f"mssql+pyodbc://sadmin:{PASSWORD}@{PUBLIC_IP_ADDRESS}/{DBNAME}?unix_socket =/cloudsql/{PROJECT_ID}:{INSTANCE_NAME}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True

db = SQLAlchemy(app)


# User ORM for SQLAlchemy
class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)


@app.route('/add', methods=['POST'])
def add():
    # getting name and email
    name = request.form.get('name')
    email = request.form.get('email')

    # checking if user already exists
    user = Users.query.filter_by(email=email).first()

    if not user:
        try:
            # creating Users object
            user = Users(
                name=name,
                email=email
            )
            # adding the fields to users table
            db.session.add(user)
            db.session.commit()
            # response
            responseObject = {
                'status': 'success',
                'message': 'Successfully registered.'
            }

            return make_response(responseObject, 200)
        except:
            responseObject = {
                'status': 'fail',
                'message': 'Some error occurred !!'
            }

            return make_response(responseObject, 400)

    else:
        # if user already exists then send status as fail
        responseObject = {
            'status': 'fail',
            'message': 'User already exists !!'
        }

        return make_response(responseObject, 403)


@app.route('/view')
def view():
    # fetches all the users
    users = Users.query.all()
    # response list consisting user details
    response = list()

    for user in users:
        response.append({
            "name": user.name,
            "email": user.email
        })

    return make_response({
        'status': 'success',
        'message': response
    }, 200)


if __name__ == "__main__":
    # serving the app directly
    app.debug=True
    app.run()
