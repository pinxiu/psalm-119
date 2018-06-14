from flask import Flask, request, render_template, redirect
app = Flask(__name__)

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/search/')
@app.route('/search/<reference>')
def search(reference=''):
	if reference:
		reference, passage = find_passage(reference)
	else:
		return render_template('index.html')
	if passage:
		return show_passage(reference, passage)
	else:
		return render_template('index.html', error='Cannot find passage')

@app.route('/progress/')
def progress():
	return render_template('progress.html', progress=display_progress())

import json
import re

with open('ESV.json') as f1:
	data = json.load(f1)

with open('order.json') as f2:
	order = json.load(f2)

with open('index.json') as f3:
	book_index = json.load(f3)

def display_progress():
	status = get_progress()
	return display(status)

def display(status):
	result = ''
	read, total = 0, 0
	for book in sorted(status, key=lambda b: int(order[b])):
		book_status = ''
		b_read, b_total = 0, 0
		for chapter in sorted(status[book], key=lambda c: int(c)):
			c_read = sum([1 for v in status[book][chapter].values() if v == 'true'])
			c_total = len(status[book][chapter])
			b_read += c_read
			b_total += c_total
			book_status += chapter + ': ' + "%.2f%%" % (100 * c_read / c_total) + ' | '
		book_status = book + ': ' + "%.2f%%" % (100 * b_read / b_total) + '\n' + book_status
		read += b_read
		total += b_total
		result += book_status
		result += '\n\n'
	return 'Total: ' + "%.2f%%" % (100 * read / total) + '\n\n\n' + result

def get_progress():
	with open('status.json') as s:
		status = json.load(s)
	return status

@app.route('/notes/')
def notes():
	return render_template('notes.html', notes=get_notes())

import os
from os import listdir

def get_notes():
	notes = ''
	for file_name in os.listdir('notes'):
		if file_name[0] == '.':
			continue
		with open('notes/' + file_name) as temp:
			notes += temp.read() + '\n\n'
	return notes

@app.route('/check/')
@app.route('/check/<reference>')
def check(reference=''):
	status = get_progress()
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
	with open('status.json', 'w') as o:
		o.write(json.dumps(status))
	return redirect('/')

def check_book(status, book, chapter1=None, verse1=None, chapter2=None, verse2=None):
	if chapter1 == None:
		chapter1 = '1'
	if chapter2 == None and verse2:
		chapter2 = chapter1
	elif chapter2 == None:
		chapter2 = max(data[book], key=lambda c: int(c))
	if chapter1 == chapter2:
		check_chapter(status, book, chapter1, verse1, verse2)
	else:
		check_chapter(status, book, chapter1, start=verse1)
		for chapter in range(int(chapter1) + 1, int(chapter2)):
			check_chapter(status, book, str(chapter))
		check_chapter(status, book, chapter2, end=verse2)
	return status

def check_chapter(status, book, chapter, start=None, end=None):
	if not start:
		start = '1'
	if not end:
		end = max(data[book][chapter], key=lambda v: int(v))
	for verse in range(int(start), int(end) + 1):
		check_verse(status, book, chapter, str(verse))
	return status

def check_verse(status, book, chapter, verse):
	status[book][chapter][verse] = 'true'
	return status

import datetime

@app.route('/submit/')
@app.route('/submit/<reference>/<note>')
def submit(reference='', note=''):
	if reference and note:
		note = reference + '\n' + note
		with open('notes/' + re.subn('\W', '_', reference + '_' + str(datetime.datetime.now())[:-7])[0] + '.txt', 'w') as f0:
			f0.write(note)
	return redirect('/search/' + reference)

def show_passage(reference, passage):
	return render_template('index.html', reference=reference, passage=passage)

def find_passage(reference):
	try:
		book1, chapter1, verse1, book2, chapter2, verse2 = parse(reference)	
		passage = ''
		if book2:
			if book1 == book2:
				passage = get_book(book1, chapter1, verse1, chapter2, verse2)
			else:
				passage = get_book(book1, chapter1=chapter1, verse1=verse1)
				for i in range(int(order[book1]) + 1, int(order[book2])):
					passage += get_book(book_index[str(i)])
				passage += get_book(book2, chapter2=chapter2, verse2=verse2)
		else:
			passage = get_book(book1, chapter1, verse1, chapter1, verse1)
		return fixed_reference(book1, chapter1, verse1, book2, chapter2, verse2), passage
	except KeyError:
		return None, None

def fixed_reference(book1, chapter1, verse1, book2, chapter2, verse2):
	if book1 == book2:
		book2 = None
	if not book2 and chapter1 == chapter2:
		chapter2 = None
	result = book1
	if chapter1:
		result += ' ' + chapter1
	if verse1:
		result += ':' + verse1
	if book2 or chapter2 or verse2:
		result += '-'
	if book2:
		result += book2
	if chapter2:
		if book2:
			result += ' '
		result += chapter2
	if verse2:
		if chapter2:
			result += ':'
		result += verse2
	return result

def get_book(book, chapter1=None, verse1=None, chapter2=None, verse2=None):
	passage = ''
	if chapter1 == None:
		chapter1 = '1'
	if chapter2 == None and verse2:
		chapter2 = chapter1
	elif chapter2 == None:
		chapter2 = max(data[book], key=lambda c: int(c))
	if chapter1 == chapter2:
		passage = get_chapter(book, chapter1, verse1, verse2)
	else:
		passage = get_chapter(book, chapter1, start=verse1)
		for chapter in range(int(chapter1) + 1, int(chapter2)):
			passage += get_chapter(book, str(chapter))
		passage += get_chapter(book, chapter2, end=verse2)
	return passage + '\n'

def get_chapter(book, chapter, start=None, end=None):
	passage = ''
	if not start:
		start = '1'
	if not end:
		end = max(data[book][chapter], key=lambda v: int(v))
	for verse in range(int(start), int(end) + 1):
		passage += get_verse(book, chapter, str(verse))
	return passage + '\n'

def get_verse(book, chapter, verse):
	result = data[book][chapter][verse]
	result = re.subn('(?P<prefix>\w[^\w\s-])(?P<suffix>\w)', '\g<prefix> \g<suffix>', result)[0] + '\n'
	return re.subn("' s", "'s", result)[0]

def parse(reference):
	m = re.match('^\s*(?P<book1>[1-3]?\s*[a-zA-Z]+)\s*(?P<chapter1>[0-9]+)?\s*:?\s*(?P<verse1>[0-9]+)?\s*(-?\s*(?P<book2>[1-3]?\s*[a-zA-Z]+)?\s*((?P<chapter2>[0-9]+)\s*:)?\s*(?P<verse2>[0-9]+)?)?', reference)
	book1, chapter1, verse1, book2, chapter2, verse2 = m.group('book1'), m.group('chapter1'), m.group('verse1'), m.group('book2'), m.group('chapter2'), m.group('verse2')
	if verse1 == None and chapter2 == None and verse2:
		chapter2 = verse2
		verse2 = None
	book1 = fix_name(book1)
	if book2 or chapter2 or verse2:
		if book2 == None:
			book2 = book1
		book2 = fix_name(book2)
	return order_fix(book1, chapter1, verse1, book2, chapter2, verse2)

def fix_name(book):
	m = re.match('(?P<number>[1-3])?\s*(?P<book>[a-zA-Z]+)', book)
	book_name = m.group('book')
	if 'a' <= book_name[0] <= 'z':
		book_name = book_name[0].upper() + book_name[1:]
	for i in range(len(book_name) - 1):
		if 'A' <= book_name[i+1] <= 'Z':
			book_name[i+1] = book_name[:i+1] + book_name[i+1].lower() + book_name[i+2:]
	if m.group('number'):
		return m.group('number') + ' ' + book_name
	else:
		return book_name

def order_fix(book1, chapter1, verse1, book2, chapter2, verse2):
	if book2 and order[book1] > order[book2]:
		tempb, tempc, tempv = book2, chapter2, verse2
		book2, chapter2, verse2 = book1, chapter1, verse1
		book1, chapter1, verse1 = tempb, tempc, tempv
	if book1 == book2 and chapter1 and chapter2 and int(chapter1) > int(chapter2):
		tempc, tempv = chapter2, verse2
		chapter2, verse2 = chapter1, verse1
		chapter1, verse1 = tempc, tempv
	if book1 == book2 and chapter1 and chapter2 and int(chapter1) == int(chapter2) and verse1 and verse2 and int(verse1) > int(verse2):
		tempv = verse2
		verse2 = verse1
		verse1 = tempv
	return book1, chapter1, verse1, book2, chapter2, verse2

# assert parse('1John') == ('1 John', None, None, None, None, None)
# assert parse('1    John3') == ('1 John', '3', None, None, None, None)
# assert parse('  1  John 3:2') == ('1 John','3', '2', None, None, None)
# assert parse('1 John3: 2- 1') == ('1 John', '3', '1', '1 John', '3', '2')
# assert parse('1 John 3:1-2:3') == ('1 John', '2', '3', '1 John', '3', '1')
# assert parse('1 John 3-2:3') == ('1 John', '2', '3', '1 John', '3', None)
# assert parse('1 John 10-2') == ('1 John', '2', None, '1 John', '10', None)
# assert parse('1 John - 2John') == ('1 John', None, None, '2 John', None, None)

# print(find_passage('2 Timothy - 1 Timothy'))
