import time
import atexit
import requests
import lob
import os

# Config
from os.path import join, dirname
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from dotenv import load_dotenv
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)
app = Flask(__name__)
CORS(app)
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
lob.api_key = os.environ['LOB_KEY']
db = SQLAlchemy(app)

# Models
class Users(db.Model):
	_id = db.Column(db.Integer, primary_key=True)

	id = db.Column(db.String(20), nullable=False, unique=True)
	company = db.Column(db.String(80), nullable=True)
	date_created = db.Column(db.String(80), nullable=False, default=datetime.utcnow)
	description = db.Column(db.String(), nullable=False)
	email = db.Column(db.String(120), nullable=False, unique=True)
	name = db.Column(db.String(120), nullable=False, unique=True)
	phone = db.Column(db.String(120), nullable=False)
	address_city = db.Column(db.String(80), nullable=False)
	address_country = db.Column(db.String(80), nullable=False)
	address_line1 = db.Column(db.String(120), nullable=False)
	address_line2 = db.Column(db.String(80))
	address_state = db.Column(db.String(80), nullable=False)
	address_zip = db.Column(db.String(20), nullable=False)
	anniversary = db.Column(db.Integer, nullable=False)
	password = db.Column(db.String(60), nullable=False)

	def __repr__(self):
		return '<User {}>'.format(self.name)

# Accepts a user object and sends an anniversary postcard through the lob API
def send_postcard(user):
	 lob.Postcard.create(
		description='Test Postcard',
		metadata={
				'campaign': 'Member Anniversary'
		},
		to_address=user.id,
		front="""
			<html>
				<head>
					<style>
						@font-face {
							font-family: 'Loved by the King';
							src: url('https://s3-us-west-2.amazonaws.com/lob-assets/LovedbytheKing.ttf');
						}
					</style>
				</head>
				<body><h1>Hi {{name}}</h1></body>
			</html>""",
		merge_variables={
				'name': user.name
		},
		back="<h1>Happy Anniversary!</h1>"
	)

# Queries database for all users with anniversaries on this date and returns as a list
def get_anniversary_users():
	# render today's date to match format of anniversary stored on db
	today = datetime.now()
	anniversary_date = int(str(today.month) + str(today.day))
	# query database for users with an anniversary on this date
	return Users.query.filter_by(anniversary=anniversary_date).all()

# Sends all users with anniversaries on this date a postcard
def send_cards_anniversary_users():
	rows = get_anniversary_users()
	for row in rows:
		# send post to Lob with user record
		send_postcard(row)

	return rows

# Initialize Scheduler
scheduler = BackgroundScheduler()
scheduler.add_job(send_cards_anniversary_users, trigger='interval', seconds=30)
scheduler.start()

# Routes
@app.route('/')
def home():
	return render_template('index.html')

@app.route('/api/all_users')
def get_all_users():
	users = Users.query.all()
	userStore = []
	for user in users:
		userStore.append({
			'id': user.id,
			'name': user.name,
			'location': user.address_city + ', ' + user.address_state,
			'anniversary': user.anniversary,
		})
	return jsonify(userStore)


@app.route('/deliveries')
def get_delivered_users():
	users = ''
	for user in get_anniversary_users():
		users += '<li>' + user.name + '</li>'
	return 'These users had anniversaries today:<br><ul>{}</ul>'.format(users)

if __name__ == '__main__':
	app.run()

atexit.register(lambda: scheduler.shutdown())
