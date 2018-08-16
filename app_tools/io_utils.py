# I/O tools

def upload(file_name, content=dict()):
	# if content == dict():
	# 	content['.ignore'] = 'ignore'
	with open("current/" + file_name, 'w') as f:
		f.write(json.dumps(content))
		# cl_upload(file_name, resource_type="raw", public_id=file_name)

def download(file_name, fallback=dict()):
	try:
		# urllib.request.urlretrieve(prefix + file_name, file_name)
		with open("current/" + file_name) as f:
			result = json.load(f)
		return result
	except Exception:
		inventory = dict()
		if fallback == "progress":
			for book in data:
				inventory[book] = dict()
				for chapter in data[book]:
					inventory[book][chapter] = dict()
					for verse in data[book][chapter]:
						inventory[book][chapter][verse] = 'false'
		# else:
		# 	inventory['.ignore'] = data
		upload(file_name, inventory)
		return inventory

# states I/O

def get_progress(username):
	status_dir = username + '/status.json'
	status = download(status_dir, fallback="progress")
	return status

def get_flashcards(username):
	flash_dir = username + '/flash.json'
	flashcards = download(flash_dir)
	return flashcards

def get_notes(username):
	note_dir = username + '/notes.json'
	notes = download(note_dir)
	return notes

def get_feedback():
	feed_dir = 'feedback.json'
	feed = download(feed_dir)
	return feed

def get_users():
	users_dir = 'users.json'
	users = download(users_dir)
	return users

