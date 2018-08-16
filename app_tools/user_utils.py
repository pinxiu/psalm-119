def reset_user(username, password, email):
	users = get_users()
	if username not in users:
		return 'User does not exist.'
	elif email != users[username]['email']:
		return 'Email does not match.'
	secret = get_secret(username, password)
	users[username]['secret'] = secret
	upload('users.json', users)
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
		return ''

def auth(username, password):
	secret = get_secret(username, password)
	users = get_users()
	if not os.path.exists(username):
		os.makedirs(username)
	if username not in users:
		return 'User not exists'
	elif secret != users[username]['secret']:
		return 'Password does not match'
	else: 
		return ''

def get_email(username):
	users = get_users()
	if username and username in users:
		return users[username]['email']
	else:
		return ''
		