from flask import Flask, request, render_template, redirect
app = Flask(__name__)

import json
import re
import hashlib
import cloudinary
from cloudinary.uploader import upload as cl_upload
from cloudinary.utils import cloudinary_url
from cloudinary.api import delete_resources_by_tag, resources_by_tag
import urllib

prefix = "https://res.cloudinary.com/htbi9rn2y/raw/upload/"

cloudinary.config( 
  cloud_name = "htbi9rn2y", 
  api_key = "593376722374363", 
  api_secret = "Urn2V7cjocJ-XV96TsomUpoMBjQ" 
)

with open('ESV.json') as f1:
	data = json.load(f1)

with open('order.json') as f2:
	order = json.load(f2)

with open('index.json') as f3:
	book_index = json.load(f3)

with open('short_hand.json') as f4:
	short_hand = json.load(f4)

def upload(file_name, content=dict()):
	with open(file_name, 'w') as f:
		f.write(json.dumps(content))
		cl_upload(file_name, resource_type="raw", public_id=file_name)

def download(file_name, fallback=dict()):
	try:
		urllib.request.urlretrieve(prefix + file_name, file_name)
		with open(file_name) as f:
			result = json.load(f)
		return result
	except urllib.error.HTTPError e:
		if e.code == 404:
			inventory = dict()
			if fallback == "progress":
				for book in data:
					inventory[book] = dict()
					for chapter in data[book]:
						inventory[book][chapter] = dict()
						for verse in data[book][chapter]:
							inventory[book][chapter][verse] = 'false'
			upload(file_name, inventory)
		return dict()

@app.route('/files')
def files():
	result = get_users()
	for user in result:
		result[user]['status.json'] = get_progress(user)
		result[user]['notes'] = get_notes(user)
		result[user]['flash.json'] = get_flashcards(user)
	return json.dumps(result)

@app.route('/')
@app.route('/<username>')
def index(username=''):
	return render_template('index.html', user=username, email=get_email(username))

@app.route('/search/')
@app.route('/search/<reference>/')
@app.route('/search/<reference>/<flag>/')
@app.route('/search/<reference>/<flag>/<username>')
def search(reference='', flag='false', username=''):
	if flag == 'true':
		flag = True
	else:
		flag = False
	if reference:
		reference, passage = find_passage(reference, flag)
	else:
		return render_template('index.html', user=username, email=get_email(username))
	if passage:
		return show_passage(reference, passage, flag, username)
	else:
		return render_template('index.html', error='Cannot find passage', user=username, email=get_email(username))

@app.route('/register')
def register():
	username = request.args.get('reguname')
	password = request.args.get('regpsw')
	email = request.args.get('regemail')
	error = register_user(username, password, email)
	if error:
		return render_template('index.html', error=error)
	else:
		return redirect('/login?loguname=' + username + '&logpsw=' + password)

@app.route('/reset')
def reset():
	username = request.args.get('resuname')
	email = request.args.get('resemail')
	password = request.args.get('respsw')
	error = reset_user(username, password, email)
	if error:
		return render_template('index.html', error=error)
	else:
		return redirect('/login?loguname=' + username + '&logpsw=' + password)

def reset_user(username, password, email):
	users = get_users()
	if username not in users:
		return 'User not exists'
	elif email != users[username]['email']:
		return 'Email does not match'
	secret = get_secret(username, password)
	users[username]['secret'] = secret
	upload('users.json', users)
	get_progress(username)
	get_notes(username)
	get_flashcards(username)
	return ''

def get_secret(username, password):
	m = hashlib.sha256()
	info = "username: " + username + "; password: " + password
	info = info.encode('utf-8')
	m.update(info)
	return m.hexdigest()

def register_user(username, password, email):
	users = get_users()
	if not username or not password or not email:
		return 'Invalid inputs'
	elif email in [item['email'] for item in users.values()]:
		return 'This email is already registered'
	elif username in users:
		return 'This username is already registered'
	else:
		secret = get_secret(username, password)
		users[username] = {'secret':secret, 'email':email}
		upload('users.json', users)

		if not os.path.exists(username):
			os.makedirs(username)
		return ''

@app.route('/logout')
def logout():
	return redirect('/')

@app.route('/login')
def login(username='', password=''):
	username = request.args.get('loguname')
	password = request.args.get('logpsw')
	error = auth(username, password)
	if error:
		return render_template('index.html', error=error)
	else:
		return render_template('index.html', user=username, email=get_email(username))

def get_users():
	users_dir = 'users.json'
	users = download(users_dir)
	return users

def auth(username, password):
	secret = get_secret(username, password)
	users = get_users()
	if username not in users:
		return 'User not exists'
	elif secret != users[username]['secret']:
		return 'Password does not match'
	else: 
		return ''

@app.route('/flashcards/')
@app.route('/flashcards/<username>')
def flash(username=''):
	if not username:
		return render_template('index.html', error='Please log in.')
	return display_flashcards(username)

def get_email(username):
	users = get_users()
	if username and username in users:
		return users[username]['email']
	else:
		return ''

def display_flashcards(username):
	flashcards = get_flashcards(username)
	html_str = """
<!doctype html>
<head>
<title>Read God's Word</title>
<meta http-equiv="content-type" content="text/html; charset=utf-8" />
<link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.1.1/css/bootstrap.min.css" integrity="sha384-WskhaSGFgHYWDcbwN70/dfYBj47jz9qbsMId/iRN3ewGhXQFZCSftd1LZCfmhktB" crossorigin="anonymous">
<link href="https://fonts.googleapis.com/css?family=Open+Sans|Source+Sans+Pro" rel="stylesheet">
<script language="JavaScript" type="text/javascript" src="https://code.jquery.com/jquery-3.3.1.min.js"></script>
<style>
	body {
	  margin: auto;
	  text-align: left;
	  font-weight: 300;
	  font-size: 16px;
	  font-family: 'Open Sans', sans-serif;
	  color: #121212;
	}

	/* Main content */
	.main {
		margin: 20px;
		margin-top: 60px; /* Add a top margin to avoid content overlay */
	}

	/* Add a black background color to the top navigation */
	.topnav {
		background-color: #333;
		overflow: hidden;
		position: fixed; /* Set the navbar to fixed position */
		top: 0; /* Position the navbar at the top of the page */
		width: 100%; /* Full width */
	}

	/* Style the links inside the navigation bar */
	.topnav a, input[type=button], input[type=submit], input[type=reset], button {
		float: left;
		color: #f2f2f2;
		text-align: center;
		padding: 14px 16px;
		text-decoration: none;
		font-weight: 300;
		font-size: 16px;
		font-family: 'Open Sans', sans-serif;
	}

	/* Change the color of links on hover */
	.topnav a:hover {
		background-color: #ddd;
		color: black;
	}

	/* Add a color to the active/current link */
	.topnav a.active, input[type=button], input[type=submit], input[type=reset], button {
		background-color: #4CAF50;
		color: white;
	}
	input[type=text], input[type=password], input[type=email] {
	  width: 100%;
	  padding: 12px 20px;
	  margin: 8px 0;
	  display: inline-block;
	  border: 1px solid #ccc;
	  box-sizing: border-box;
	  font-weight: 300;
	  font-size: 16px;
	  font-family: 'Open Sans', sans-serif;
	}

	input[type=button], input[type=submit], input[type=reset], button {
	  border: none;
	  margin: 4px 2px;
	  cursor: pointer;
	  float: none;
	}

	/* Set a style for all buttons */
	button {
	  width: 100%;
	}

	/* Add a hover effect for buttons */
	button:hover {
		opacity: 0.8;
	}

	.container {
	  height:120px;
	  width:600px;
	  margin:auto;
	  position:relative;
	}

	.flip-container {
	  perspective: 1000;
	  margin: 10px;
	  float: left;
	  cursor:pointer;
	}

	  .flippable {
		transition: 0.5s;
		transform-style: preserve-3d;
		position: relative;
	  }

	  .flipme {
		transform: rotateY(180deg);
	  }
	  
	

	.flip-container, .front, .back {
	  width: 500px;
	  height: 300px;
	  text-align: center;
	  overflow-wrap: break-word;
	  overflow: scroll;
	  font-size: 40px;
	  border-radius: 10px;
	}

	.front, .back {
		color: white;
		background:#4CAF50;
		backface-visibility: hidden;
		position: absolute;
		top: 0;
		left: 0;
	}

	.front {
	  z-index: 2;
	  line-height: 280px;
	}

	.center_p {
	  line-height: 1.5;
	  display: inline-block;
	  vertical-align: middle;
	}

	.back {
	  transform: rotateY(180deg);
	  padding: 50px;
	  font-size: 18px;
	  text-align: left;
	  white-space: pre-line;
	}
	/* The Modal (background) */
	.modal {
		display: none; /* Hidden by default */
		position: fixed; /* Stay in place */
		z-index: 1; /* Sit on top */
		left: 0;
		top: 0;
		width: 100%; /* Full width */
		height: 100%; /* Full height */
		overflow: auto; /* Enable scroll if needed */
		background-color: rgb(0,0,0); /* Fallback color */
		background-color: rgba(0,0,0,0.4); /* Black w/ opacity */
		padding-top: 60px;
	}

	/* The Close Button */
	.close {
		/* Position it in the top right corner outside of the modal */
		position: relative;
		right: -55px;
		top: -25px;
		font-weight: 300;
		font-size: 16px;
		font-family: 'Open Sans', sans-serif;
		text-shadow: none;
		opacity: 1.0;
	}

	/* Close button on hover */
	.close:hover,
	.close:focus {
		color: #4CAF50;
		cursor: pointer;
	}

	/* Add Zoom Animation */
	.animate {
		-webkit-animation: animatezoom 0.6s;
		animation: animatezoom 0.6s
	}

	@-webkit-keyframes animatezoom {
		from {-webkit-transform: scale(0)} 
		to {-webkit-transform: scale(1)}
	}

	@keyframes animatezoom {
		from {transform: scale(0)} 
		to {transform: scale(1)}
	}

	.login-page {
	  width: 360px;
	  padding: 8% 0 0;
	  margin: auto;
	}
	.form {
	  position: relative;
	  z-index: 1;
	  background: #FFFFFF;
	  max-width: 360px;
	  margin: 0 auto 100px;
	  padding: 45px;
	  text-align: center;
	  box-shadow: 0 0 20px 0 rgba(0, 0, 0, 0.2), 0 5px 5px 0 rgba(0, 0, 0, 0.24);
	}
	.form input {
	  outline: 0;
	  background: #f2f2f2;
	  width: 100%;
	  border: 0;
	  margin: 0 0 15px;
	  padding: 15px;
	  box-sizing: border-box;
	}
	.form button {
	  outline: 0;
	  background: #4CAF50;
	  width: 100%;
	  border: 0;
	  padding: 15px;
	  color: #FFFFFF;
	  -webkit-transition: all 0.3 ease;
	  transition: all 0.3 ease;
	  cursor: pointer;
	}
	.form button:hover,.form button:active,.form button:focus {
	  background: #43A047;
	}

</style>
</head>
<body>

<div class="topnav">
  <a href="/"""+username+"""">Reading</a>
  <a href="/notes/"""+username+"""">Notes</a>
  <a href="/progress/"""+username+"""">Progress</a>
  <a class="active" href="/flashcards/"""+username+"""">Flashcards</a>
  <a href="/help/"""+username+"""">Help</a>"""
	html_str += """
  <input style="margin:0;float:right;" type="button" onclick="document.getElementById('login').style.display='block'" value='"""+username+"""'>
				"""
	html_str += """
</div>
				"""
	html_str += """

<div id="login" class="modal">

  <!-- Modal Content -->
  <div class="animate">
	<div class="login-page">
	  <span onclick="document.getElementById('login').style.display='none'" 
class="close" title="Close Modal">Close</span>
	  <div class="form">
		<form class="logout-form" action="/logout">
		  <p style="text-align:left;"><b>Email: </b>"""+get_email(username)+"""</p>
		  <button>Log Out</button>
		</form>
	  </div>
	</div>
  </div>
</div>

<script>
// Get the modal
var modal = document.getElementById('login');

// When the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {
	if (event.target == modal) {
		modal.style.display = "none";
	}
}
</script>
				"""

	html_str += """

<div class="main">

<div class="container">
				"""
				
	html_str += show_flashcards(flashcards)
	html_str += """
</div>

</div>

<script>
	$(".flippable").click(function(){
	  $(this).toggleClass("flipme");
	});
</script>
</body>
</html>
				"""
	return html_str

def show_flashcards(flashcards):
	html_str = ""
	for reference in flashcards:
		passage = find_passage(reference)[1]
		_, reviewed, score, times = flashcards[reference]
		html_str += """
	<div class="flip-container" ontouchstart="this.classList.toggle('hover');">
	  <div class="flippable appcon ac">
		<div class="front"><div class="center_p">"""+reference+"""</div></div>
		<div class="back">"""+passage+"""</div>
	  </div>
	</div>
		  """
	return html_str

@app.route('/help/')
@app.route('/help/<username>')
def help(username=''):
	return render_template('help.html', user=username, email=get_email(username))

@app.route('/progress/')
@app.route('/progress/<username>')
def progress(username=''):
	if not username:
		return render_template('index.html', error='Please log in.')
	return display_progress(username)

def display_progress(username):
	status = get_progress(username)
	html_str = """
<!doctype html>
<head>
<title>Read God's Word</title>
<meta http-equiv="content-type" content="text/html; charset=utf-8" />
<link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.1.1/css/bootstrap.min.css" integrity="sha384-WskhaSGFgHYWDcbwN70/dfYBj47jz9qbsMId/iRN3ewGhXQFZCSftd1LZCfmhktB" crossorigin="anonymous">
<link href="https://fonts.googleapis.com/css?family=Open+Sans|Source+Sans+Pro" rel="stylesheet">
<script language="JavaScript" type="text/javascript" src="https://code.jquery.com/jquery-3.3.1.min.js"></script>
<style>
	body {
	  margin: auto;
	  text-align: left;
	  font-weight: 300;
	  font-size: 16px;
	  font-family: 'Open Sans', sans-serif;
	  color: #121212;
	}
	.grid-container {
	  display: grid;
	  grid-template-columns: repeat(auto-fill, minmax(90px, 1fr));
	}
	.grid-item {
	  padding: 2px;
	  text-align: right;
	}

	/* Main content */
	.main {
		margin: 20px;
		margin-top: 60px; /* Add a top margin to avoid content overlay */
	}

	.container {
		margin: auto;
		margin-bottom: 30px;
	}

	/* Add a black background color to the top navigation */
	.topnav {
		background-color: #333;
		overflow: hidden;
		position: fixed; /* Set the navbar to fixed position */
		top: 0; /* Position the navbar at the top of the page */
		width: 100%; /* Full width */
	}

	/* Style the links inside the navigation bar */
	.topnav a, input[type=button], input[type=submit], input[type=reset], button {
		float: left;
		color: #f2f2f2;
		text-align: center;
		padding: 14px 16px;
		text-decoration: none;
		font-weight: 300;
		font-size: 16px;
		font-family: 'Open Sans', sans-serif;
	}

	/* Change the color of links on hover */
	.topnav a:hover {
		background-color: #ddd;
		color: black;
	}

	/* Add a color to the active/current link */
	.topnav a.active, input[type=button], input[type=submit], input[type=reset], button {
		background-color: #4CAF50;
		color: white;
	}
	input[type=text], input[type=password], input[type=email] {
	  width: 100%;
	  padding: 12px 20px;
	  margin: 8px 0;
	  display: inline-block;
	  border: 1px solid #ccc;
	  box-sizing: border-box;
	  font-weight: 300;
	  font-size: 16px;
	  font-family: 'Open Sans', sans-serif;
	}

	input[type=button], input[type=submit], input[type=reset], button {
	  border: none;
	  margin: 4px 2px;
	  cursor: pointer;
	  float: none;
	}

	/* Set a style for all buttons */
	button {
	  width: 100%;
	}

	/* Add a hover effect for buttons */
	button:hover {
		opacity: 0.8;
	}

	/* Extra style for the cancel button (red) */
	.cancelbtn {
		width: auto;
		padding: 10px 18px;
		background-color: #f44336;
	}
	/* The Modal (background) */
	.modal {
		display: none; /* Hidden by default */
		position: fixed; /* Stay in place */
		z-index: 1; /* Sit on top */
		left: 0;
		top: 0;
		width: 100%; /* Full width */
		height: 100%; /* Full height */
		overflow: auto; /* Enable scroll if needed */
		background-color: rgb(0,0,0); /* Fallback color */
		background-color: rgba(0,0,0,0.4); /* Black w/ opacity */
		padding-top: 60px;
	}

	/* The Close Button */
	.close {
		/* Position it in the top right corner outside of the modal */
		position: relative;
		right: -55px;
		top: -25px;
		font-weight: 300;
		font-size: 16px;
		font-family: 'Open Sans', sans-serif;
		text-shadow: none;
		opacity: 1.0;
	}

	/* Close button on hover */
	.close:hover,
	.close:focus {
		color: #4CAF50;
		cursor: pointer;
	}

	/* Add Zoom Animation */
	.animate {
		-webkit-animation: animatezoom 0.6s;
		animation: animatezoom 0.6s
	}

	@-webkit-keyframes animatezoom {
		from {-webkit-transform: scale(0)} 
		to {-webkit-transform: scale(1)}
	}

	@keyframes animatezoom {
		from {transform: scale(0)} 
		to {transform: scale(1)}
	}

	.login-page {
	  width: 360px;
	  padding: 8% 0 0;
	  margin: auto;
	}
	.form {
	  position: relative;
	  z-index: 1;
	  background: #FFFFFF;
	  max-width: 360px;
	  margin: 0 auto 100px;
	  padding: 45px;
	  text-align: center;
	  box-shadow: 0 0 20px 0 rgba(0, 0, 0, 0.2), 0 5px 5px 0 rgba(0, 0, 0, 0.24);
	}
	.form input {
	  outline: 0;
	  background: #f2f2f2;
	  width: 100%;
	  border: 0;
	  margin: 0 0 15px;
	  padding: 15px;
	  box-sizing: border-box;
	}
	.form button {
	  outline: 0;
	  background: #4CAF50;
	  width: 100%;
	  border: 0;
	  padding: 15px;
	  color: #FFFFFF;
	  -webkit-transition: all 0.3 ease;
	  transition: all 0.3 ease;
	  cursor: pointer;
	}
	.form button:hover,.form button:active,.form button:focus {
	  background: #43A047;
	}
	.form .message {
	  margin: 15px 0 0;
	  color: #b3b3b3;
	  font-size: 12px;
	}
	.form .message a {
	  color: #4CAF50;
	  text-decoration: none;
	}
	.form .register-form {
	  display: none;
	}
	.form .reset-form {
	  display: none;
	}
</style>
</head>

<body>

<div class="topnav">
  <a href="/"""+username+"""">Reading</a>
  <a href="/notes/"""+username+"""">Notes</a>
  <a class="active" href="/progress/"""+username+"""">Progress</a>
  <a href="/flashcards/"""+username+"""">Flashcards</a>
  <a href="/help/"""+username+"""">Help</a>"""
	html_str += """
  <input style="margin:0;float:right;" type="button" onclick="document.getElementById('login').style.display='block'" value='"""+username+"""'>
				"""
	html_str += """
</div>
				"""
	html_str += """

<div id="login" class="modal">

  <!-- Modal Content -->
  <div class="animate">
	<div class="login-page">
	  <span onclick="document.getElementById('login').style.display='none'" 
class="close" title="Close Modal">Close</span>
	  <div class="form">
		<form class="logout-form" action="/logout">
		  <p style="text-align:left;"><b>Email: </b>"""+get_email(username)+"""</p>
		  <button>Log Out</button>
		</form>
	  </div>
	</div>
  </div>
</div>

<script>
// Get the modal
var modal = document.getElementById('login');

// When the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {
	if (event.target == modal) {
		modal.style.display = "none";
	}
}
</script>

				"""

	html_str += """

<div class="main">

<div class="container">
				"""
				
	html_str += display(status)
	html_str += """
</div>

</div>

</body>
</html>
				"""
	return html_str

def display(status):
	result = ''
	read, total = 0, 0
	for book in sorted(status, key=lambda b: int(order[b])):
		book_status = '<div class="grid-container">'
		b_read, b_total = 0, 0
		for chapter in sorted(status[book], key=lambda c: int(c)):
			c_read = sum([1 for v in status[book][chapter].values() if v == 'true'])
			c_total = len(status[book][chapter])
			b_read += c_read
			b_total += c_total
			book_status += create_label(chapter + ': ', "%.2f%%" % (100 * c_read / c_total))
		if book == 'Psalm':
			book = 'Psalms'
		elif book == "Song":
			book = "Song of Solomon"
		book_status = create_bar(book + ': ', "%.2f%%" % (100 * b_read / b_total)) + book_status + '</div>'
		read += b_read
		total += b_total
		result += book_status
		result += '\n\n'
	return create_bar('Total:', "%.2f%%" % (100 * read / total)) + result

def create_label(label, value):
	if value == "0.00%":
		btype = "badge badge-danger"
	elif value == "100.00%":
		btype = "badge badge-success"
	else:
		btype = "badge badge-warning"
	return """
	<div class="grid-item">
	  """+label+"""
	  <span class='"""+btype+"""'>"""+value+"""</span>
	</div>
		  """

def create_bar(label, value):
	if value == "0.00%":
		btype = "progress-bar bg-danger"
	elif value == "100.00%":
		btype = "progress-bar bg-success"
	else:
		btype = "progress-bar bg-warning"
	return """
	</div>
	<div class="container">
	  <h4>"""+label+"""</h4>
	  <div class="progress">
		<div class='"""+btype+"""'role="progressbar" aria-valuenow='"""+value[:-1]+"""' aria-valuemin="0" aria-valuemax="100" style="width:"""+value+"""">
		  <span>"""+value+""" Complete</span>
		</div>
	  </div>
		  """

def get_progress(username):
	status_dir = username + '/status.json'
	status = download(status_dir, fallback="progress")
	return status

def get_flashcards(username):
	flash_dir = username + '/flash.json'
	flashcards = download(flash_dir)
	return flashcards

@app.route('/notes/')
@app.route('/notes/<username>')
def notes(username=''):
	if not username:
		return render_template('index.html', error='Please log in.')
	return render_template('notes.html', notes=display_notes(username), user=username, email=get_email(username))

import os
from os import listdir

def create_flashcard(reference):
	# reference, reviewed, score, visited_times
	return [reference, False, 0.0, 0]

def display_notes(username):
	notes = get_notes(username)
	for timestamp in notes:
		notes += notes[timestamp]['reference'] + '\n' + notes[timestamp]['content'] + '\n\n'
	return re.subn('<br>', '\n', notes)[0]

def get_notes(username):
	note_dir = username + '/notes.json'
	notes = download(note_dir)
	return notes
	
@app.route('/store/')
@app.route('/store/<reference>/')
@app.route('/store/<reference>/<flag>/')
@app.route('/store/<reference>/<flag>/<username>')
def store(reference='', flag=False, username=''):
	if not username:
		return render_template('index.html', error='Please log in.')
	flashcards = get_flashcards(username)
	if reference and reference not in flashcards:
		flashcards[reference] = create_flashcard(reference)
		upload(username + '/flash.json', flashcards)
	return redirect('/search/' + reference + '/' + flag + '/' + username)

@app.route('/check/')
@app.route('/check/<reference>/')
@app.route('/check/<reference>/<username>')
def check(reference='', username=''):
	if not username:
		return render_template('index.html', error='Please log in.')
	status = get_progress(username)
	if reference:
		book1, chapter1, verse1, book2, chapter2, verse2 = parse(reference)
		if book2:
			if book1 == book2:
				check_book(status, book1, chapter1, verse1, chapter2, verse2)
			else:
				check_book(status, book1, chapter1=chapter1, verse1=verse1)
				for i in range(int(order[book1]) + 1, int(order[book2])):
					check_book(status, book_index[str(i)])
				check_book(status, book2, chapter2=chapter2, verse2=verse2)
		else:
			check_book(status, book1, chapter1, verse1, chapter1, verse1)
	upload(username + '/status.json', status)
	return redirect('/' + username)

def check_book(status, book, chapter1=None, verse1=None, chapter2=None, verse2=None):
	if chapter1 == None:
		chapter1 = '1'
	if chapter2 == None and verse2:
		chapter2 = chapter1
	elif chapter2 == None:
		chapter2 = max(data[book], key=lambda c: int(c))
	if chapter1 == chapter2:
		check_chapter(status, book, chapter1, verse1, verse2)
	else:
		check_chapter(status, book, chapter1, start=verse1)
		for chapter in range(int(chapter1) + 1, int(chapter2)):
			check_chapter(status, book, str(chapter))
		check_chapter(status, book, chapter2, end=verse2)
	return status

def check_chapter(status, book, chapter, start=None, end=None):
	if not start:
		start = '1'
	if not end:
		end = max(data[book][chapter], key=lambda v: int(v))
	for verse in range(int(start), int(end) + 1):
		check_verse(status, book, chapter, str(verse))
	return status

def check_verse(status, book, chapter, verse):
	status[book][chapter][verse] = 'true'
	return status

import datetime

@app.route('/submit/')
@app.route('/submit/<reference>/<note>/')
@app.route('/submit/<reference>/<note>/<flag>/')
@app.route('/submit/<reference>/<note>/<flag>/<username>')
def submit(reference='', note='', flag=False, username=''):
	if not username:
		return render_template('index.html', error='Please log in.')
	if reference and note:
		note_dir = username + '/notes.json'
		notes = download(note_dir)
		result = dict()
		result['reference'] = reference
		result['content'] = note
		notes[datetime.datetime.now())[:-7])] = result
		upload(note_dir, notes)
	return redirect('/search/' + reference + '/' + flag + '/' + username)

def show_passage(reference, passage, flag=False, username=''):
	if flag:
		number = 'Hide Verse Number'
	else:
		number = 'Show Verse Number'
	return render_template('index.html', reference=reference, passage=passage, number=number, user=username, email=get_email(username))

def find_passage(reference, flag=False):
	try:
		book1, chapter1, verse1, book2, chapter2, verse2 = parse(reference)
		passage = ''
		if book2:
			if book1 == book2:
				passage = get_book(book1, chapter1, verse1, chapter2, verse2, flag=flag)
			else:
				passage = get_book(book1, chapter1=chapter1, verse1=verse1, flag=flag)
				for i in range(int(order[book1]) + 1, int(order[book2])):
					passage += get_book(book_index[str(i)], flag=flag)
				passage += get_book(book2, chapter2=chapter2, verse2=verse2, flag=flag)
		else:
			passage = get_book(book1, chapter1, verse1, chapter1, verse1, flag=flag)
		return fixed_reference(book1, chapter1, verse1, book2, chapter2, verse2), passage
	except KeyError:
		return None, None

def fixed_reference(book1, chapter1, verse1, book2, chapter2, verse2):
	if book1 == book2:
		book2 = None
	if not book2 and chapter1 == chapter2:
		chapter2 = None
	if book1 == 'Psalm' and not chapter1:
		book1 = 'Psalms'
	if book2 == 'Psalm' and not chapter2:
		book2 = 'Psalms'
	if book1 == 'Song':
		book1 = 'Song of Solomon'
	if book2 == 'Song':
		book2 = 'Song of Solomon'
	result = book1
	if chapter1:
		result += ' ' + chapter1
	if verse1:
		result += ':' + verse1
	if book2 or chapter2 or verse2:
		result += '-'
	if book2:
		result += book2
	if chapter2:
		if book2:
			result += ' '
		result += chapter2
	if verse2:
		if chapter2:
			result += ':'
		result += verse2	
	return result

def get_book(book, chapter1=None, verse1=None, chapter2=None, verse2=None, flag=False):
	passage = ''
	if chapter1 == None:
		chapter1 = '1'
	if chapter2 == None and verse2:
		chapter2 = chapter1
	elif chapter2 == None:
		chapter2 = max(data[book], key=lambda c: int(c))
	if chapter1 == chapter2:
		passage += get_chapter(book, chapter1, verse1, verse2, flag=flag)
	else:
		passage += get_chapter(book, chapter1, start=verse1, flag=flag)
		for chapter in range(int(chapter1) + 1, int(chapter2)):
			passage += get_chapter(book, str(chapter), flag=flag)
		passage += get_chapter(book, chapter2, end=verse2, flag=flag)
	return passage + '\n'

def get_chapter(book, chapter, start=None, end=None, flag=False):
	if flag:
		passage = book + ' ' + chapter + '\n\n'
	else:
		passage = ''
	if not start:
		start = '1'
	if not end:
		end = max(data[book][chapter], key=lambda v: int(v))
	for verse in range(int(start), int(end) + 1):
		passage += get_verse(book, chapter, str(verse), flag=flag)
	return passage + '\n'

def get_verse(book, chapter, verse, flag=False):
	if flag:
		result = verse + ' '
	else:
		result = ''
	result += data[book][chapter][verse]
	result = re.subn('(?P<prefix>\w[^\w\s-])(?P<suffix>\w)', '\g<prefix> \g<suffix>', result)[0] + '\n'
	return re.subn("' s", "'s", result)[0]

def parse(reference):
	reference = fix_number(reference)
	reference = fix_space(reference)
	reference = fix_signs(reference)
	m = re.match('^\s*(?P<book1>[1-3]?\s*[a-zA-Z]+)\s*(?P<chapter1>[0-9]+)?\s*:?\s*(?P<verse1>[0-9]+)?\s*(-?\s*(?P<book2>[1-3]?\s*[a-zA-Z]+)?\s*((?P<chapter2>[0-9]+)\s*:)?\s*(?P<verse2>[0-9]+)?)?', reference)
	book1, chapter1, verse1, book2, chapter2, verse2 = m.group('book1'), m.group('chapter1'), m.group('verse1'), m.group('book2'), m.group('chapter2'), m.group('verse2')
	if verse1 == None and chapter2 == None and verse2:
		chapter2 = verse2
		verse2 = None
	book1 = fix_name(book1)
	if book2 or chapter2 or verse2:
		if book2 == None:
			book2 = book1
		book2 = fix_name(book2)
	return order_fix(book1, chapter1, verse1, book2, chapter2, verse2)

def fix_number(reference):
	reference = reference.lower()
	reference = re.subn('first', '1',reference)[0]
	reference = re.subn('second', '2',reference)[0]
	reference = re.subn('third', '3',reference)[0]
	reference = re.subn('iii ', '3',reference)[0]
	reference = re.subn('ii ', '2',reference)[0]
	reference = re.subn('i ', '1',reference)[0]
	reference = re.subn('1st', '1',reference)[0]
	reference = re.subn('2nd', '2',reference)[0]
	reference = re.subn('3rd', '3',reference)[0]
	return reference

def fix_space(reference):
	reference = re.subn('the revelation', 'revelation',reference)[0]
	reference = re.subn('song of solomon', 'song',reference)[0]
	reference = re.subn('song of songs', 'song',reference)[0]
	reference = re.subn('canticle of canticles ', 'song',reference)[0]
	return reference

def fix_signs(reference):
	correct_ref = ''
	for c in reference:
		if c != ':' and c != '-' and c != ' ' and not ('a' <= c <= 'z') and not ('0' <= c <= '9'):
			continue
		correct_ref += c
	return correct_ref

def fix_name(book):
	m = re.match('(?P<number>[1-3])?\s*(?P<book>[a-zA-Z]+)', book)
	book_name = m.group('book')
	book_name = book_name[0].upper() + book_name[1:]
	if m.group('number'):
		book_name = m.group('number') + ' ' + book_name
	return short_hand[book_name]

def order_fix(book1, chapter1, verse1, book2, chapter2, verse2):
	if book2 and order[book1] > order[book2]:
		tempb, tempc, tempv = book2, chapter2, verse2
		book2, chapter2, verse2 = book1, chapter1, verse1
		book1, chapter1, verse1 = tempb, tempc, tempv
	if book1 == book2 and chapter1 and chapter2 and int(chapter1) > int(chapter2):
		tempc, tempv = chapter2, verse2
		chapter2, verse2 = chapter1, verse1
		chapter1, verse1 = tempc, tempv
	if book1 == book2 and chapter1 and chapter2 and int(chapter1) == int(chapter2) and verse1 and verse2 and int(verse1) > int(verse2):
		tempv = verse2
		verse2 = verse1
		verse1 = tempv
	return book1, chapter1, verse1, book2, chapter2, verse2

