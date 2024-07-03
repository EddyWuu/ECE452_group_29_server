from flask import Flask, request, jsonify, g
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

print(f"DATABASE_URL: {os.getenv('DATABASE_URL')}")

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)

class User(db.Model):
    __tablename__ = 'users'
    profileID = db.Column(db.String, primary_key=True)
    firstName = db.Column(db.String, nullable=False)
    lastName = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    city = db.Column(db.String, nullable=False)
    country = db.Column(db.String, nullable=False)
    profilePicResId = db.Column(db.Integer, nullable=True)

class UserEvent(db.Model):
    __tablename__ = 'user_events'
    profileID = db.Column(db.String, db.ForeignKey('users.profileID'), primary_key=True)
    eventID = db.Column(db.String, primary_key=True)

class Unavailability(db.Model):
    __tablename__ = 'unavailabilities'
    profileID = db.Column(db.String, db.ForeignKey('users.profileID'), primary_key=True)
    date = db.Column(db.String, primary_key=True)
    startTime = db.Column(db.String, nullable=False)
    endTime = db.Column(db.String, nullable=False)

class Event(db.Model):
    __tablename__ = 'events'
    eventID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String, nullable=False)
    date = db.Column(db.String, nullable=False)
    time = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    host = db.Column(db.String, nullable=False)
    imageResId = db.Column(db.Integer, nullable=True)
    duration = db.Column(db.String, nullable=False)
    city = db.Column(db.String, nullable=False)
    country = db.Column(db.String, nullable=False)
    address = db.Column(db.String, nullable=False)
    datePosted = db.Column(db.String, nullable=False, default=datetime.utcnow)
    registered = db.Column(db.Boolean, default=False)
    isVolunteerEvent = db.Column(db.Boolean, default=False)


@app.before_request
def before_request():
    if not hasattr(g, 'first_request_done'):
        g.first_request_done = True
        create_tables()

def create_tables():
    db.create_all()

@app.route('/')
def index():
    return "Welcome nerds to my domain"


@app.route('/user', methods=['POST'])
def create_user():
    data = request.get_json()
    new_user = User(
        profileID=data['profileID'],
        firstName=data['firstName'],
        lastName=data['lastName'],
        email=data['email'],
        password=data['password'],
        city=data['city'],
        country=data['country'],
        profilePicResId=data.get('profilePicResId')
    )
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "User created successfully"}), 201

@app.route('/user/<profileID>', methods=['GET'])
def get_user(profileID):
    user = User.query.filter_by(profileID=profileID).first()
    if user:
        return jsonify({
            "profileID": user.profileID,
            "firstName": user.firstName,
            "lastName": user.lastName,
            "email": user.email,
            "city": user.city,
            "country": user.country,
            "profilePicResId": user.profilePicResId
        })
    else:
        return jsonify({"message": "User not found"}), 404

if __name__ == '__main__':
    app.run(debug=True, ssl_context=('cert.pem', 'key.pem'))
