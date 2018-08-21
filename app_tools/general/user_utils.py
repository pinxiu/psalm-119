def app_register_user(username, password, email):
	return register_user(username, password, email)

def app_reset_user(username, password, email):
	return reset_user(username, password, email)

def app_login_user(username, password):
	return login_user(username, password)

def app_auth_user(username):
	return auth_user(username)

def app_get_email(username):
	return get_email(username)

def app_get_all_info():
	return get_all_info()


#############################
# internal helper functions #
#############################

from app_tools.general.io_utils import app_upload, app_download, app_initialize_user, app_get_user_info
from app_tools.static.constants import users_file
from werkzeug.exceptions import BadRequest, Unauthorized
import hashlib
import json

def get_users():
	users = app_download(users_file)
	return users

def get_secret(username, password):
	m = hashlib.sha256()
	info = "username: " + username + "; password: " + password
	info = info.encode('utf-8')
	m.update(info)
	return m.hexdigest()

def reset_user(username, password, email):
	users = get_users()
	if username not in users:
		raise BadRequest('User does not exist.')
	elif email != users[username]['email']:
		raise BadRequest('Email does not match.')
	secret = get_secret(username, password)
	users[username]['secret'] = secret
	app_upload(users_file, users)
	return ''

def register_user(username, password, email):
	users = get_users()
	if not username or not password or not email:
		raise BadRequest('Please fill in all the required fields.')
	elif email in [item['email'] for item in users.values()]:
		raise BadRequest('This email is already registered.')
	elif username in users:
		raise BadRequest('This username is already registered.')
	else:
		secret = get_secret(username, password)
		users[username] = {'secret':secret, 'email':email}
		app_upload(users_file, users)
		app_initialize_user(username)
		return ''

def login_user(username, password):
	secret = get_secret(username, password)
	users = get_users()
	if username not in users:
		raise Unauthorized('User not exists.')
	elif secret != users[username]['secret']:
		raise Unauthorized('Password does not match.')

def auth_user(username):
	if not username:
		raise Unauthorized("Please log in.")

def get_email(username):
	users = get_users()
	if username and username in users:
		return users[username]['email']
	else:
		return ''
		
def get_all_info():
	result = get_users()
	for user in result:
		# ignore .DS_Store files
		if user[0] == '.':
			continue
		result[user].update(app_get_user_info(user))
	return json.dumps(result)

