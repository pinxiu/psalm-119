def app_generate():
	return 

#############################
# internal helper functions #
#############################

from app_tools.static.constants import notes_file
from app_tools.general.io_utils import app_upload, app_download

def get_notes(username):
	note_dir = username + '/' + notes_file
	notes = download(note_dir)
	return notes

def display_notes(username):
	notes = get_notes(username)
	result = ''
	for timestamp in notes:
		if timestamp[0] == '.':
			continue
		result += notes[timestamp]['reference'] + '\n' + notes[timestamp]['content'] + '\n\n'
	return re.subn('<br>', '\n', result)[0]