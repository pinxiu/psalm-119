from flask import Flask, request, render_template, redirect
app = Flask(__name__)

import json
import re
import hashlib
import urllib

import os
from os import listdir
import random
import datetime

from io_utils import *
from load_source import *

@app.route('/files')
def files():
	result = get_users()
	for user in result:
		if user[0] == '.':
			continue
		result[user]['status.json'] = get_progress(user)
		result[user]['notes.json'] = get_notes(user)
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

@app.route('/flashcards/')
@app.route('/flashcards/<username>')
def flash(username=''):
	if not username:
		return render_template('index.html', error='Please log in.')
	return display_flashcards(username)

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

@app.route('/notes/')
@app.route('/notes/<username>')
def notes(username=''):
	if not username:
		return render_template('index.html', error='Please log in.')
	return render_template('notes.html', notes=display_notes(username), user=username, email=get_email(username))

@app.route('/quiz/')
@app.route('/quiz/<username>')
def quiz(username=''):
	if not username:
		return render_template('index.html', error='Please log in.')
	return display_quiz(username)
	
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
		notes[str(datetime.datetime.now())] = result
		upload(note_dir, notes)
	return redirect('/search/' + reference + '/' + flag + '/' + username)

@app.route('/feed/')
@app.route('/feed/<note>/')
@app.route('/feed/<note>/<username>')
def feed(note='', username=''):
	if note:
		feed_dir = 'feedback.json'
		feed = download(feed_dir)
		result = dict()
		result['username'] = username
		result['content'] = note
		feed[str(datetime.datetime.now())] = result
		upload(feed_dir, feed)
	return redirect('/feedback/' + username)

@app.route('/feedback/')
@app.route('/feedback/<username>')
def feedback(username=''):
	return render_template('feedback.html', user=username, email=get_email(username))

@app.route('/view')
def view():
	result = get_feedback()
	return json.dumps(result)

