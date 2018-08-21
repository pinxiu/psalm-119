def app_upload(file_name, content=dict()):
	return upload(file_name, content)

def app_download(file_name, fallback=dict()):
	return download(file_name, fallback)

def app_initialize_user(username):
	return initialize(username)

def app_get_user_info(username):
	return get_user_info(username)

#############################
# internal helper functions #
#############################

import json
import os

from app_tools.static.constants import *
from app_tools.service.progress_utils import app_initialize_progress

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
	upload(username + '/' + status_file, app_initialize_progress())
	upload(username + '/' + notes_file)
	upload(username + '/' + flashcards_file)

def get_user_info(username):
	result = dict()
	result[status_file] = download(username + '/' + status_file, app_initialize_progress())
	result[notes_file] = download(username + '/' + notes_file)
	result[flashcards_file] = download(username + '/' + flashcards_file)
	return result
	
