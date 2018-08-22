from app_tools.general.book_utils import app_find_passage, app_display_reference
from app_tools.general.display_utils import *
from app_tools.general.user_utils import app_get_all_info, app_auth_user, \
app_login_user, app_register_user, app_reset_user
from app_tools.service.feedback_utils import app_display_feedback, app_submit_feedback
from app_tools.service.flashcard_utils import app_store_flashcard
from app_tools.service.note_utils import app_submit_note
from app_tools.service.progress_utils import app_display_progress, app_update_progress
from flask import Flask, request, redirect
from werkzeug.exceptions import HTTPException

app = Flask(__name__)

@app.route('/files')
def files():
	return app_get_all_info()

@app.route('/')
@app.route('/<username>')
def index(username=''):
	return show_index_page(username)

@app.route('/search/')
@app.route('/search/<reference>/')
@app.route('/search/<reference>/<flag>/')
@app.route('/search/<reference>/<flag>/<username>')
def search(reference='', flag='false', username=''):
	if not reference:
		return redirect('/' + username)
	passage = app_find_passage(reference, flag == 'true')
	if passage:
		return show_passage(app_display_reference(reference), passage, flag == 'true', username)
	else:
		return show_index_error('Cannot find passage', username)

@app.route('/register')
def register():
	username = request.args.get('reguname')
	password = request.args.get('regpsw')
	email = request.args.get('regemail')
	error = app_register_user(username, password, email)
	if error:
		return show_index_error(error)
	else:
		return redirect('/login?loguname=' + username + '&logpsw=' + password)

@app.route('/reset')
def reset():
	username = request.args.get('resuname')
	email = request.args.get('resemail')
	password = request.args.get('respsw')
	error = app_reset_user(username, password, email)
	if error:
		return show_index_error(error)
	else:
		return redirect('/login?loguname=' + username + '&logpsw=' + password)

@app.route('/logout')
def logout():
	return redirect('/')

@app.route('/login')
def login(username='', password=''):
	username = request.args.get('loguname')
	password = request.args.get('logpsw')
	error = app_login_user(username, password)
	if error:
		return show_index_error(error)
	else:
		return redirect('/' + username)

@app.route('/flashcards/')
@app.route('/flashcards/<username>')
def flash(username=''):
	app_auth_user(username)
	return display_flashcards(username)

@app.route('/help/')
@app.route('/help/<username>')
def help(username=''):
	return show_help_page(username)

@app.route('/progress/')
@app.route('/progress/<username>')
def progress(username=''):
	app_auth_user(username)
	return app_display_progress(username)

@app.route('/notes/')
@app.route('/notes/<username>')
def notes(username=''):
	app_auth_user(username)
	return show_note_page(username)

@app.route('/quiz/')
@app.route('/quiz/<username>')
def quiz(username=''):
	app_auth_user(username)
	return display_quiz(username)
	
@app.route('/store/')
@app.route('/store/<reference>/')
@app.route('/store/<reference>/<flag>/')
@app.route('/store/<reference>/<flag>/<username>')
def store(reference='', flag=False, username=''):
	app_auth_user(username)
	app_store_flashcard(reference, username)
	return redirect('/search/' + reference + '/' + flag + '/' + username)

@app.route('/check/')
@app.route('/check/<reference>/')
@app.route('/check/<reference>/<username>')
def check(reference='', username=''):
	app_auth_user(username)
	if reference:
		app_update_progress(username, reference)
	return redirect('/' + username)

@app.route('/submit/')
@app.route('/submit/<reference>/<note>/')
@app.route('/submit/<reference>/<note>/<flag>/')
@app.route('/submit/<reference>/<note>/<flag>/<username>')
def submit(reference='', note='', flag=False, username=''):
	app_auth_user(username)
	app_submit_note(reference, note)
	return redirect('/search/' + reference + '/' + flag + '/' + username)

@app.route('/feed/')
@app.route('/feed/<note>/')
@app.route('/feed/<note>/<username>')
def feed(note='', username=''):
	app_submit_feedback(note, username)
	return redirect('/feedback/' + username)

@app.route('/feedback/')
@app.route('/feedback/<username>')
def feedback(username=''):
	return show_feedback_page(username)

@app.route('/view')
def view():
	return app_display_feedback()

@app.errorhandler(HTTPException)
def handle_error(e):
    return show_index_error(e)

