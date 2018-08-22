def app_download(file_name, fallback=dict()):
	return download(file_name, fallback)

def app_get_user_info(username):
	return get_user_info(username)

def app_initialize_user(username):
	return initialize(username)

def app_json_dump(content):
	return json_dump(content)

def app_upload(file_name, content=dict()):
	return upload(file_name, content)

#############################
# internal helper functions #
#############################

from app_tools.static.constants import app_initialize_progress, app_users_file, app_status_file, \
app_notes_file, app_flashcards_file

import json
import os

prefix = 'resources/web/current/'

def upload(file_name, content=dict()):
	file_name = prefix + file_name
	check_path(file_name)
	with open(file_name, 'w') as f:
		f.write(json.dumps(content))

def download(file_name, fallback=dict()):
	try:
		with open(prefix + file_name) as f:
			result = json.load(f)
		return result
	except Exception:
		upload(file_name, fallback)
		return fallback

def check_path(file_name):
	if not os.path.exists(os.path.dirname(file_name)):
	    os.makedirs(os.path.dirname(file_name))

def initialize(username):
	upload(username + '/' + app_status_file, app_initialize_progress())
	upload(username + '/' + app_notes_file)
	upload(username + '/' + app_flashcards_file)

def get_user_info(username):
	result = dict()
	result[app_status_file] = download(username + '/' + app_status_file, app_initialize_progress())
	result[app_notes_file] = download(username + '/' + app_notes_file)
	result[app_flashcards_file] = download(username + '/' + app_flashcards_file)
	return result
	
def json_dump(content):
	return json.dumps(content)