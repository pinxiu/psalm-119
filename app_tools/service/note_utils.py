def app_submit_note(reference, note):
	return submit_note(reference, note)

#############################
# internal helper functions #
#############################

from app_tools.static.constants import notes_file
from app_tools.general.io_utils import app_upload, app_download

def get_notes(username):
	note_dir = username + '/' + notes_file
	notes = app_download(note_dir)
	return notes

def display_notes(username):
	notes = get_notes(username)
	result = ''
	for timestamp in notes:
		if timestamp[0] == '.':
			continue
		result += notes[timestamp]['reference'] + '\n' + notes[timestamp]['content'] + '\n\n'
	return re.subn('<br>', '\n', result)[0]

def submit_note(reference='', note=''):
	if reference and note:
		note_dir = username + '/' + notes_file
		notes = app_download(note_dir)
		result = dict()
		result['reference'] = reference
		result['content'] = note
		notes[str(datetime.datetime.now())] = result
		app_upload(note_dir, notes)