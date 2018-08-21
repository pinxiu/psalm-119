from app_tools.general.user_utils import app_get_email
from flask import render_template

def show_passage(reference, passage, flag=False, username=''):
	if flag:
		number = 'Hide Verse Number'
	else:
		number = 'Show Verse Number'
	return render_template('index.html', reference=reference, passage=passage, number=number, user=username, email=app_get_email(username))

def show_user_not_login():
	return render_template('index.html', error='Please log in.')

def show_index_page(username):
	return render_template('index.html', user=username, email=app_get_email(username))

def show_index_error(error, username=''):
	return render_template('index.html', error=error, user=username, email=app_get_email(username))

def show_help_page(username):
	return render_template('help.html', user=username, email=app_get_email(username))

def show_note_page(username):
	return render_template('notes.html', notes=display_notes(username), user=username, email=app_get_email(username))